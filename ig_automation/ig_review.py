"""Telegram review loop: one item per message, your replies mark items reviewed, unanswered items come back.

Plan (vault): ZAIHub/Vault knowledge library/Plan - Telegram review loop by claude.md

Four kinds of item, each with its own id letter, numbered once and never reused:

* P: a playbook tip, in the order of the playbook review sheet in the vault (move or delete lines there to change it)
* D: an interest digest pick, from the digest notes in ZAIHub/Interest digest, oldest note first
* F: a Focus topics item, from the Focus topics note
* X: a dead end that needs you, from output/dead_ends.json (read only), Focus posts first

Each message starts with the id (for example "P14"). Reply to the message in Telegram, with anything, and the
item counts as reviewed. Some words do more: "save" ticks Would save on a digest pick, "later" brings it back, and
"try", "doing", "drop" and "skip" are written next to the item. A message that is not a reply counts only if it
names the id with a word, like "reviewed P14".

Replies are read from the Hermes history (~/.hermes/state.db), opened read only. Nothing in Hermes is changed, and
Hermes keeps answering your messages as usual. Ticking a pick or a tip in the vault counts as reviewed too.

An item sent with no reply is logged as "no reply" and comes back 3 days later; new items fill the days in between.

Commands:
    ig_review.py send playbook|digest|focus|deadend   check replies, then send the next item of that kind
    ig_review.py check                                  read new replies and vault ticks
    ig_review.py answer "reviewed P14"                  record an answer by hand (the same as a Telegram reply)
    ig_review.py sheet                                  create or extend the playbook review sheet
    ig_review.py status                                 counts per kind
Add --dry-run to send to print the message instead of sending it.
"""
import argparse
import fcntl
import json
import os
import re
import sqlite3
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
OUTPUT_DIR = HERE / "output"
QUEUE_FILE = OUTPUT_DIR / "review_queue.json"
LOG_FILE = OUTPUT_DIR / "review_log.json"
LOCK_FILE = OUTPUT_DIR / "review.lock"
DEAD_ENDS_FILE = OUTPUT_DIR / "dead_ends.json"
PLAYBOOK_FILE = REPO / "knowledge_library" / "Instagram playbook.md"

VAULT = Path(os.environ.get("IG_VAULT", Path.home() / "Work/2025Secondbrain"))
LIBRARY = VAULT / "ZAIHub" / "Vault knowledge library"
DIGEST_DIR = VAULT / "ZAIHub" / "Interest digest"
FOCUS_NOTE = LIBRARY / "Focus topics - coding agents and agent skills by claude.md"
SHEET_NOTE = LIBRARY / "IG playbook review sheet by claude.md"
QUEUE_NOTE = LIBRARY / "IG review queue by claude.md"
PLAN_NOTE = "Plan - Telegram review loop by claude"

HERMES_BIN = os.environ.get("HERMES_SEND_BIN", str(Path.home() / ".local/bin/hermes"))
HERMES_TARGET = os.environ.get("HERMES_STATUS_TARGET", "telegram")
HERMES_DB = Path(os.environ.get("HERMES_STATE_DB", Path.home() / ".hermes/state.db"))
HERMES_CHAT = os.environ.get("HERMES_REVIEW_CHAT", "6261465035")

COME_BACK_DAYS = 3
LETTERS = {"playbook": "P", "digest": "D", "focus": "F", "deadend": "X"}
KINDS = {v: k for k, v in LETTERS.items()}
ICONS = {"playbook": "📘", "digest": "📰", "focus": "🎯", "deadend": "🧱"}
# Playbook sections sent first, in this order; the rest follow in playbook order.
FIRST_SECTIONS = ["Coding Agent Configuration and Workflows", "Agent Skills, Memory and Knowledge Libraries",
                  "Claude Usage, Settings and Claims"]
SKIP_SECTIONS = {"Contradictions"}
WORDS = {"save": "save", "saved": "save", "later": "later", "try": "try", "doing": "doing", "drop": "drop",
         "skip": "skip", "pass": "skip", "no": "skip", "nah": "skip", "done": "done", "reviewed": "reviewed",
         "seen": "reviewed", "ok": "reviewed", "okay": "reviewed", "read": "reviewed", "got": "reviewed"}
ID_RE = re.compile(r"\b([PDFX])(\d{1,5})\b")
WORD_ID_RE = re.compile(r"\b(" + "|".join(WORDS) + r")\b[\s:,]*((?:[PDFX]\d{1,5}[\s,]*(?:and\s+)?)+)", re.I)
QUOTE_RE = re.compile(r'^\[Replying to: "(.*?)"\]\s*(.*)$', re.S)
TELEGRAM_MAX = 3500


# ------------------------------------------------------------------ time and files

def now() -> datetime:
    return datetime.now().astimezone()


def stamp(t: datetime | None = None) -> str:
    return (t or now()).isoformat(timespec="seconds")


def parse(s: str) -> datetime:
    return datetime.fromisoformat(s)


def load_json(path: Path, default):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(path)


def load_queue() -> dict:
    q = load_json(QUEUE_FILE, {})
    q.setdefault("items", {})
    q.setdefault("next_number", {letter: 1 for letter in KINDS})
    q.setdefault("replies_checked_until", now().timestamp())
    return q


def log(event: str, item: dict | None = None, **extra) -> None:
    entries = load_json(LOG_FILE, [])
    row = {"at": stamp(), "event": event}
    if item:
        row.update(id=item["id"], kind=item["kind"], title=item["title"])
    row.update(extra)
    entries.append(row)
    save_json(LOG_FILE, entries)


def short(text: str, limit: int) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= limit else text[: limit - 3].rstrip() + "..."


def plain(text: str) -> str:
    """Markdown to plain text for Telegram: links become their label, bold and code marks go."""
    text = re.sub(r"Web: \[([^\]]+)\]\(([^)]+)\)", r"\2", text)
    text = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", text)
    text = re.sub(r"\[\[([^\]]+)\]\]", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", text)
    return text.replace("**", "").replace("`", "")


# ------------------------------------------------------------------ sources

def playbook_tips() -> list[dict]:
    """Tips in the playbook, with their section, steps and evidence line."""
    tips, section, tip = [], None, None
    for number, line in enumerate(PLAYBOOK_FILE.read_text(encoding="utf-8").splitlines(), 1):
        if line.startswith("## "):
            section, tip = line[3:].strip(), None
        elif line.startswith("### ") and section and section not in SKIP_SECTIONS:
            tip = {"title": line[4:].strip(), "section": section, "steps": [], "evidence": "", "line": number}
            tips.append(tip)
        elif tip is not None:
            if re.match(r"^\d+\. ", line):
                tip["steps"].append(line)
            elif line.startswith("**Evidence:**"):
                tip["evidence"] = line[len("**Evidence:**"):].strip()
            elif line.startswith(("**Selected source:**", "**Merged sources:**")):
                m = re.search(r"\((https?://[^)]+)\)", line)
                if line.startswith("**Selected") and m:
                    tip["source"] = m.group(1)
                tip.setdefault("shortcodes", []).extend(re.findall(r"\[([A-Za-z0-9_-]{11})\]", line))
    return tips


SHEET_LINE_RE = re.compile(r"^\* \[( |x|X)\] \*\*(.+?)\*\*")


def sheet_order() -> list[tuple[str, bool]]:
    """(tip title, ticked) in the order of the review sheet."""
    if not SHEET_NOTE.exists():
        return []
    return [(m.group(2), m.group(1) != " ") for m in map(SHEET_LINE_RE.match, SHEET_NOTE.read_text(encoding="utf-8").splitlines()) if m]


def build_sheet() -> str:
    """Create the review sheet, or add tips that are not on it yet under "Added later". Never reorders."""
    tips = playbook_tips()
    if not SHEET_NOTE.exists():
        order = FIRST_SECTIONS + [s for s in dict.fromkeys(t["section"] for t in tips) if s not in FIRST_SECTIONS]
        today = now().strftime("%Y-%m-%d")
        lines = ["---", "name: IG playbook review sheet by claude", f"created: {today}", "---", "",
                 "#instaLearning #todo", "", "# IG playbook review sheet", "",
                 f"The order the Telegram review loop sends playbook tips in, top to bottom: two a day, at 5 AM and 9 PM. "
                 f"Plan: [[{PLAN_NOTE}]].", "",
                 "* Move a line to change when it is sent. Delete a line to never get it",
                 "* A tick means reviewed: tick it here, or reply to the tip's message in Telegram. Your reply word "
                 "(try, doing, later, drop) is written after the title",
                 "* The tips themselves are in Outside vault: `/home/homepi/Work/ig/instagram_saves/knowledge_library/Instagram playbook.md`",
                 "", f"Tips: {len(tips)}. Built {today}.", ""]
        for section in order:
            part = [t for t in tips if t["section"] == section]
            if part:
                lines += [f"## {section} ({len(part)})", ""] + [f"* [ ] **{t['title']}**" for t in part] + [""]
        SHEET_NOTE.write_text("\n".join(lines), encoding="utf-8")
        return f"Created the review sheet with {len(tips)} tips"
    have = {title for title, _ in sheet_order()}
    new = [t for t in tips if t["title"] not in have]
    if not new:
        return "Review sheet is up to date"
    text = SHEET_NOTE.read_text(encoding="utf-8").rstrip("\n")
    if "\n## Added later" not in text:
        text += "\n\n## Added later\n"
    text += "\n" + "\n".join(f"* [ ] **{t['title']}** ({t['section']})" for t in new) + "\n"
    SHEET_NOTE.write_text(text, encoding="utf-8")
    return f"Added {len(new)} new tips to the review sheet"


PICK_RE = re.compile(r"^\* \*\*(.+?)\*\*: (.*?)(?: \^[a-z0-9-]+)?$")


def digest_picks() -> list[dict]:
    """Picks from every digest note, oldest note first, with whether Would save is ticked."""
    picks = []
    for note in sorted(DIGEST_DIR.glob("claude - interest digest *.md")):
        date = note.stem.rsplit(" ", 1)[-1]
        topic, pick = "", None
        for line in note.read_text(encoding="utf-8").splitlines():
            if line.startswith("### "):
                topic = line[4:].strip()
            elif m := PICK_RE.match(line):
                pick = {"name": m.group(1), "what": m.group(2), "topic": topic, "note": note.name, "date": date,
                        "url": "", "why": "", "ticked": False}
                picks.append(pick)
            elif pick and line.startswith(("\t", "  ")):
                body = line.strip()
                if re.match(r"^\* \[[xX]\] ", body):
                    pick["ticked"] = True
                elif body.startswith("* Why you would care:"):
                    pick["why"] = body.split(":", 1)[1].strip()
                elif body.startswith("* Web:") and (u := re.search(r"\((https?://[^)]+)\)\s*$", body)):
                    pick["url"] = u.group(1)
            elif line.strip() and not line.startswith(("\t", "  ")):
                pick = None
    return picks


FOCUS_ITEM_RE = re.compile(r"^(?:\d+\.|\*) \*\*(.+?)\*\*\s*(.*?)(?: \^[a-z0-9-]+)?$")


def focus_items() -> list[dict]:
    """Items under "Act on first" and "Next after that" in each Focus section."""
    items, focus, part = [], "", None
    for line in FOCUS_NOTE.read_text(encoding="utf-8").splitlines():
        if line.startswith("### "):
            focus, part = line[4:].strip(), None
            if not focus.startswith("Focus"):
                focus = ""
        elif focus and line.startswith("**"):
            part = line.replace("*", "").split("(")[0].strip()
            part = part if part in ("Act on first", "Next after that") else None
        elif focus and part == "Act on first" and (m := FOCUS_ITEM_RE.match(line)) and line[0].isdigit():
            items.append({"title": m.group(1).rstrip("."), "text": m.group(2), "focus": focus, "status": ""})
        elif focus and part == "Act on first" and items and line.strip().startswith("* **Status"):
            items[-1]["status"] = line.strip()[2:]
        elif focus and part == "Next after that" and line.startswith("* "):
            body = re.sub(r" \^[a-z0-9-]+$", "", line[2:])
            title = body.split(",")[0].split(". ")[0]
            items.append({"title": short(plain(title), 80), "text": body, "focus": focus, "status": ""})
    return items


def dead_ends() -> list[dict]:
    """Open dead ends that need you, Focus posts first, oldest first. Read only."""
    entries = [e for e in load_json(DEAD_ENDS_FILE, []) if e.get("status") == "needs_you"]
    return sorted(entries, key=lambda e: (not e.get("focus"), e.get("added_at") or ""))


# ------------------------------------------------------------------ queue

def candidates(kind: str) -> list[dict]:
    """(key, title, data, done in vault) for every item of a kind, in send order."""
    out = []
    if kind == "playbook":
        tips = {t["title"]: t for t in playbook_tips()}
        for title, ticked in sheet_order():
            if title in tips:
                out.append({"key": f"playbook:{title}", "title": title, "data": tips[title], "done_in_vault": ticked})
    elif kind == "digest":
        for p in digest_picks():
            out.append({"key": f"digest:{p['url'] or p['name']}", "title": p["name"], "data": p, "done_in_vault": p["ticked"]})
    elif kind == "focus":
        for f in focus_items():
            out.append({"key": f"focus:{f['title']}", "title": f["title"], "data": f, "done_in_vault": False})
    elif kind == "deadend":
        for e in dead_ends():
            out.append({"key": f"deadend:{e['shortcode']}:{e.get('stage', '')}", "title": e.get("title") or e["shortcode"],
                        "data": e, "done_in_vault": False})
    return out


def item_for(q: dict, kind: str, c: dict) -> dict:
    item = q["items"].get(c["key"])
    if item is None:
        letter = LETTERS[kind]
        number = q["next_number"].get(letter, 1)
        q["next_number"][letter] = number + 1
        item = {"id": f"{letter}{number}", "kind": kind, "key": c["key"], "title": c["title"], "status": "new",
                "sends": [], "replies": [], "added_at": stamp()}
        q["items"][c["key"]] = item
    return item


def pick_next(q: dict, kind: str) -> tuple[dict, dict] | None:
    """An unanswered item that is due to come back, else the next new one."""
    cands = candidates(kind)
    t = now()
    due = []
    for c in cands:
        item = q["items"].get(c["key"])
        if c["done_in_vault"] or not item or item["status"] not in ("sent", "later"):
            continue
        if t - parse(item["sends"][-1]["at"]) >= timedelta(days=COME_BACK_DAYS):
            due.append((parse(item["sends"][-1]["at"]), c, item))
    if due:
        _, c, item = min(due, key=lambda d: d[0])
        if item["status"] == "sent":
            log("no reply", item, sent_at=item["sends"][-1]["at"])
        return c, item
    for c in cands:
        if c["done_in_vault"]:
            continue
        item = q["items"].get(c["key"])
        if item is None or item["status"] == "new":
            return c, item_for(q, kind, c)
    return None


def by_id(q: dict) -> dict:
    return {item["id"]: item for item in q["items"].values()}


# ------------------------------------------------------------------ messages

SUMMARY_FILE = OUTPUT_DIR / "review_summaries.json"
SUMMARY_MODEL = os.environ.get("IG_REVIEW_MODEL", "haiku")
SUMMARY_PROMPT = """Rewrite this playbook tip as a short Telegram message for one person, in plain simple words.
Use exactly this layout, plain text, no markdown, no headings, under 450 characters:

<a short plain title>

What it is: <one sentence>

* <step, under 12 words>
* <step, under 12 words>
* <step, under 12 words>

Trust: <a few words: how much to trust it, from the evidence line>

Keep commands and names exactly as written (like /init or CLAUDE.md). Drop post ids, hype and side details.
Do not use em dashes. Output only the message.

Tip title: {title}
Section: {section}
Steps:
{steps}
Evidence: {evidence}"""


def strip_ids(text: str) -> str:
    return re.sub(r"\s*\((?:[A-Za-z0-9_-]{11}(?:, )?)+\)", "", text)


IG_DIR = REPO / "IG"


def saved_post(shortcode: str) -> str:
    """One line for a saved post: who posted it, when you saved it, its IG folder and link."""
    folder = next(iter(sorted(IG_DIR.glob(f"*_{shortcode}"))), None)
    link = f"instagram.com/p/{shortcode}"
    if not folder:
        return f"* {link}"
    author = ""
    for note in folder.glob("*_description.md"):
        if m := re.search(r'^author: "?([^"\n]+)"?', note.read_text(encoding="utf-8", errors="ignore"), re.M):
            author = m.group(1).strip()
            break
    try:
        saved = datetime.strptime(folder.name[:10], "%Y-%m-%d").strftime("%b %d")
    except ValueError:
        saved = ""
    who = f"@{author}" if author and author.lower() not in ("none", "null") else "unknown account"
    return f"* {who}, saved {saved}: {link}\n  IG/{folder.name}"


def short_tip(d: dict) -> str:
    """Fallback without AI: the title, the first 3 steps shortened, and the first sentence of the evidence."""
    steps = "\n".join(short(plain(strip_ids(s)), 130) for s in d["steps"][:3])
    trust = plain(d["evidence"]).split(". ")[0].rstrip(".")
    return f"{d['title']}\n\n{steps}\n\nTrust: {short(trust, 120)}"


def rewrite(key: str, prompt: str) -> str | None:
    """A plain words version from a small model, saved under `key` so a resend reads the same. None if it fails."""
    cache = load_json(SUMMARY_FILE, {})
    if key in cache:
        return cache[key]
    try:
        r = subprocess.run(["claude", "-p", prompt, "--model", SUMMARY_MODEL, "--safe-mode", "--strict-mcp-config",
                            "--tools", "", "--no-session-persistence", "--output-format", "text"],
                           cwd=HERE, capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.TimeoutExpired):
        return None
    text = (r.stdout or "").strip().replace("\u2014", ",")
    if r.returncode != 0 or not 40 < len(text) < 1200:
        return None
    cache[key] = text
    save_json(SUMMARY_FILE, cache)
    return text


def simple_tip(d: dict) -> str | None:
    return rewrite(d["title"], SUMMARY_PROMPT.format(title=d["title"], section=d["section"], evidence=strip_ids(d["evidence"]),
                                                     steps="\n".join(strip_ids(s) for s in d["steps"])))


FOCUS_PROMPT = """Rewrite this to-do item as a short Telegram message for one person, in plain simple words.
Use exactly this layout, plain text, no markdown, no headings, under 450 characters:

<a short plain title>

What it is: <one sentence>

* <step, under 12 words>
* <step, under 12 words>
* <step, under 12 words>

Done so far: <one short line from the status, or "nothing yet">

Keep commands and names exactly as written (like /doctor or CLAUDE.md). Leave out links and post names.
Do not use em dashes. Output only the message.

Item: {title}
Details: {text}
Status: {status}"""


def simple_focus(d: dict) -> str | None:
    return rewrite("focus:" + d["title"], FOCUS_PROMPT.format(title=plain(d["title"]), text=plain(d["text"]),
                                                              status=plain(d["status"]) or "none"))


def focus_sources(d: dict) -> list[str]:
    """Saved posts and web pages named in a Focus item."""
    raw = d["text"]
    codes = list(dict.fromkeys(re.findall(r"instagram\.com/(?:reel|p)/([A-Za-z0-9_-]{11})", raw)))
    webs = [u for u in re.findall(r"\((https?://[^)]+)\)", raw) if "instagram.com" not in u]
    return [saved_post(c) for c in codes[:3]] + [f"* {u}" for u in list(dict.fromkeys(webs))[:2]]


def message(kind: str, item: dict, c: dict) -> str:
    d, n = c["data"], len(item["sends"])
    again = f" (again, sent {n} times before)" if n else ""
    if kind == "playbook":
        cands = candidates("playbook")
        place = next((i for i, x in enumerate(cands, 1) if x["key"] == c["key"]), 0)
        body = simple_tip(d) or short_tip(d)
        text = f"{ICONS[kind]} {item['id']} Playbook tip{again} ({place} of {len(cands)})\n{body}"
        saves = [saved_post(sc) for sc in d.get("shortcodes", [])[:4]]
        text += f"\n\nIn the playbook: {d['section']}, line {d['line']}"
        if saves:
            text += "\n\nFrom your saves:\n" + "\n".join(saves)
        hint = "try, doing, later or drop"
    elif kind == "digest":
        text = (f"{ICONS[kind]} {item['id']} Interest digest pick{again}\n{d['name']}\n({d['topic']}, digest {d['date']})\n\n"
                f"{short(plain(d['what']), 500)}\n\nWhy you would care: {short(plain(d['why']), 300)}\n{d['url']}")
        hint = "save (would save it), skip or later"
    elif kind == "focus":
        body = simple_focus(d)
        if not body:
            status = f"\n\n{short(plain(d['status']), 300)}" if d["status"] else ""
            body = f"{plain(d['title'])}\n\n{short(plain(d['text']), 500)}{status}"
        text = f"{ICONS[kind]} {item['id']} Focus topic{again} ({d['focus'].split(':')[0]})\n{body}"
        sources = focus_sources(d)
        if sources:
            text += "\n\nFrom your saves and links:\n" + "\n".join(sources)
        hint = "done, doing, later or skip"
    else:
        what = d.get("keyword")
        comment = f"Comment: {what}" if what else "Comment: keyword unclear, check the post"
        who = f" by @{d['author']}" if d.get("author") else ""
        focus = ", Focus topic" if d.get("focus") else ""
        text = (f"{ICONS[kind]} {item['id']} Dead end, needs you{again}\n{c['title']}{who}\n({'comment to get it' if d.get('list') == 'comment_to_get' else 'other dead end'}{focus})\n\n"
                f"{comment}\nMissing: {short(d.get('reason') or '', 500)}\n{d.get('url', '')}\n\n"
                "To fix it, paste what you get after Link: in the dead ends note.")
        hint = "reviewed, later or skip"
    text += f"\n\nReply to this message to mark it reviewed ({hint})."
    return text[:TELEGRAM_MAX]


def send_text(text: str, tries: int = 3, wait: int = 60) -> tuple[bool, str]:
    """Send with `hermes send`; tries again after a minute, since Telegram sometimes drops the connection."""
    import time
    error = ""
    for attempt in range(tries):
        try:
            r = subprocess.run([HERMES_BIN, "send", "--to", HERMES_TARGET, "--quiet"], input=text, text=True,
                               capture_output=True, timeout=90)
            if r.returncode == 0:
                return True, ""
            error = (r.stderr or r.stdout or f"hermes send exited with code {r.returncode}").strip()
        except (OSError, subprocess.TimeoutExpired) as exc:
            error = str(exc)
        if attempt < tries - 1:
            time.sleep(wait)
    return False, error


# ------------------------------------------------------------------ answers

def apply_answer(q: dict, item: dict, word: str, text: str, source: str) -> str:
    """Record one answer on an item and mirror it in the vault where there is a place for it."""
    word = word or "reviewed"
    item["replies"].append({"at": stamp(), "word": word, "text": short(text, 300), "source": source})
    item["status"] = "later" if word == "later" else "reviewed"
    item["answered_at"] = stamp()
    if item["kind"] == "digest" and word == "save":
        tick_digest(item)
    if item["kind"] == "playbook" and word != "later":
        tick_sheet(item["title"], "" if word in ("reviewed", "done") else word)
    log(f"answer: {word}", item, source=source, text=short(text, 300))
    return f"{item['id']} {word}"


def tick_digest(item: dict) -> None:
    for p in digest_picks():
        if f"digest:{p['url'] or p['name']}" != item["key"]:
            continue
        note = DIGEST_DIR / p["note"]
        lines = note.read_text(encoding="utf-8").splitlines(keepends=True)
        inside = False
        for i, line in enumerate(lines):
            if (m := PICK_RE.match(line.rstrip("\n"))):
                inside = m.group(1) == p["name"]
            elif inside and re.match(r"^\s+\* \[ \] Would save", line):
                lines[i] = line.replace("[ ]", "[x]", 1)
                note.write_text("".join(lines), encoding="utf-8")
                return


def tick_sheet(title: str, word: str) -> None:
    if not SHEET_NOTE.exists():
        return
    lines = SHEET_NOTE.read_text(encoding="utf-8").splitlines(keepends=True)
    for i, line in enumerate(lines):
        m = SHEET_LINE_RE.match(line)
        if m and m.group(2) == title:
            new = line.replace("[ ]", "[x]", 1).rstrip("\n")
            if word and f"· {word}" not in new:
                new += f" · {word}"
            lines[i] = new + "\n"
            SHEET_NOTE.write_text("".join(lines), encoding="utf-8")
            return


def first_word(text: str) -> str:
    for w in re.findall(r"[a-z]+", text.lower())[:4]:
        if w in WORDS:
            return WORDS[w]
    return "reviewed"


def answers_in(text: str, ids: dict) -> list[tuple[dict, str]]:
    """Items and words named in a message. A reply to a review message counts with any text."""
    found = []
    m = QUOTE_RE.match(text)
    if m:
        quoted, reply = m.groups()
        qm = ID_RE.search(quoted[:12])
        if qm and (item := ids.get(qm.group(0))):
            found.append((item, first_word(reply)))
        text = reply
    for wm in WORD_ID_RE.finditer(text):
        for idm in ID_RE.finditer(wm.group(2)):
            if (item := ids.get(idm.group(0))) and all(item is not f[0] for f in found):
                found.append((item, WORDS[wm.group(1).lower()]))
    return found


def answer_text(q: dict, text: str, source: str = "manual") -> list[str]:
    ids = by_id(q)
    return [apply_answer(q, item, word, text, source) for item, word in answers_in(text, ids)]


def hermes_messages(since: float) -> list[tuple[float, str]]:
    """Your Telegram messages to Hermes after `since`, read only."""
    if not HERMES_DB.exists():
        return []
    try:
        con = sqlite3.connect(f"file:{HERMES_DB}?mode=ro", uri=True, timeout=10)
        rows = con.execute(
            "select m.timestamp, m.content from messages m join sessions s on s.id = m.session_id "
            "where s.source = 'telegram' and s.chat_id = ? and m.role = 'user' and m.timestamp > ? "
            "and m.platform_message_id is not null order by m.timestamp", (HERMES_CHAT, since)).fetchall()
        con.close()
    except sqlite3.Error as exc:
        log("could not read Hermes replies", error=str(exc))
        return []
    return [(ts, content or "") for ts, content in rows]


def check(q: dict) -> list[str]:
    done = []
    # 1. Telegram replies. A message counts for an item only if it came after the item was sent.
    seen = set()
    for ts, content in hermes_messages(q["replies_checked_until"]):
        if (ts, content) in seen:
            continue
        seen.add((ts, content))
        ids = {i: item for i, item in by_id(q).items()
               if item["sends"] and parse(item["sends"][0]["at"]).timestamp() <= ts}
        for item, word in answers_in(content, ids):
            # Hermes may already have recorded this reply with `ig_review.py answer`: do not count it twice.
            last_send = parse(item["sends"][-1]["at"]).timestamp()
            if any(r["word"] == word and parse(r["at"]).timestamp() >= min(ts, last_send) - 60 for r in item["replies"]):
                continue
            done.append(apply_answer(q, item, word, content, "telegram"))
        q["replies_checked_until"] = max(q["replies_checked_until"], ts)
    # 2. Ticks in the vault (digest Would save, review sheet).
    for kind in ("playbook", "digest"):
        for c in candidates(kind):
            item = q["items"].get(c["key"])
            if c["done_in_vault"] and item and item["status"] in ("new", "sent", "later"):
                item["status"] = "reviewed"
                item["answered_at"] = stamp()
                item["replies"].append({"at": stamp(), "word": "ticked", "text": "", "source": "vault"})
                log("answer: ticked in the vault", item)
                done.append(f"{item['id']} ticked")
    return done


# ------------------------------------------------------------------ queue note

def block_id(item: dict) -> str | None:
    """Give a digest pick a block id (like ^d1) in its digest note, so the queue note can embed it. Returns the note."""
    pick = next((p for p in digest_picks() if f"digest:{p['url'] or p['name']}" == item["key"]), None)
    if not pick:
        return None
    note = DIGEST_DIR / pick["note"]
    tag = f"^{item['id'].lower()}"
    lines = note.read_text(encoding="utf-8").splitlines(keepends=True)
    for i, line in enumerate(lines):
        m = PICK_RE.match(line.rstrip("\n"))
        if m and m.group(1) == pick["name"]:
            if not re.search(r" \^[a-z0-9-]+$", line.rstrip("\n")):
                lines[i] = line.rstrip("\n") + f" {tag}\n"
                note.write_text("".join(lines), encoding="utf-8")
            else:
                tag = line.rstrip("\n").rsplit(" ", 1)[1]
            return f"{note.stem}#{tag}"
    return None


def focus_block_id(item: dict) -> str | None:
    """Give a Focus item a block id (like ^f1) in the Focus note, so the queue note can embed it."""
    title = item["key"].split(":", 1)[1]
    lines = FOCUS_NOTE.read_text(encoding="utf-8").splitlines(keepends=True)
    for i, line in enumerate(lines):
        body = line.rstrip("\n")
        m = FOCUS_ITEM_RE.match(body)
        hit = (m and m.group(1).rstrip(".") == title and body[0].isdigit()) or \
              (body.startswith("* ") and short(plain(body[2:].split(",")[0].split(". ")[0]), 80) == title)
        if hit:
            if (old := re.search(r" (\^[a-z0-9-]+)$", body)):
                return f"{FOCUS_NOTE.stem}#{old.group(1)}"
            tag = f"^{item['id'].lower()}"
            lines[i] = body + f" {tag}\n"
            FOCUS_NOTE.write_text("".join(lines), encoding="utf-8")
            return f"{FOCUS_NOTE.stem}#{tag}"
    return None


def where(item: dict) -> str:
    """Where an item lives, as sub bullets for the queue note: the vault note, then the post or page."""
    kind, key = item["kind"], item["key"]
    out = []
    if kind == "playbook":
        pass  # the review sheet link is on the item's own line
    elif kind == "digest":
        if (target := block_id(item)):
            out.append(f"\t* ![[{target}]]")
    elif kind == "focus":
        if (target := focus_block_id(item)):
            out.append(f"\t* ![[{target}]]")
        else:
            out.append(f"\t* Focus note: [[{FOCUS_NOTE.stem}]]")
    elif kind == "deadend":
        entry = next((e for e in load_json(DEAD_ENDS_FILE, []) if key.startswith(f"deadend:{e['shortcode']}:")), None)
        if entry:
            note = "IG dead ends - comment to get it" if entry.get("list") == "comment_to_get" else "IG dead ends - other"
            out.append(f"\t* Dead ends: [[{note}]]")
            if entry.get("url"):
                out.append(f"\t* Post: Web: [{entry['shortcode']} (instagram.com)]({entry['url']})")
    return "\n".join(out)


def label(item: dict) -> str:
    if item["kind"] == "playbook":
        return f"[[IG playbook review sheet by claude]] - {item['title']}"
    return item["title"]


def write_queue_note(q: dict) -> None:
    items = list(q["items"].values())
    t = now()
    waiting = sorted((i for i in items if i["status"] in ("sent", "later")), key=lambda i: i["sends"][-1]["at"])
    lines = ["---", "name: IG review queue by claude", f"created: {t.strftime('%Y-%m-%d')}", "---", "",
             "#instaLearning", "", "# IG review queue", "",
             f"Rebuilt by Outside vault: `/home/homepi/Work/ig/instagram_saves/ig_automation/ig_review.py` after every "
             f"send and reply check. Plan: [[{PLAN_NOTE}]]. Playbook order: [[IG playbook review sheet by claude]].", "",
             f"Updated: {t.strftime('%Y-%m-%d %I:%M %p')}.", "", "## Counts", ""]
    for kind, letter in LETTERS.items():
        mine = [i for i in items if i["kind"] == kind]
        total = len(candidates(kind))
        lines.append(f"* {ICONS[kind]} {kind.capitalize()}: {sum(i['status'] == 'reviewed' for i in mine)} reviewed, "
                     f"{sum(i['status'] in ('sent', 'later') for i in mine)} waiting for a reply, "
                     f"{total - sum(i['status'] != 'new' for i in mine)} not sent yet")
    lines += ["", f"## Waiting for a reply ({len(waiting)})", "",
              "Sent and not answered yet. Each comes back 3 days after it was last sent.", ""]
    for i in waiting:
        last = parse(i["sends"][-1]["at"])
        back = (last + timedelta(days=COME_BACK_DAYS)).strftime("%b %d")
        note = "you said later" if i["status"] == "later" else "no reply"
        lines.append(f"* **{i['id']}** {label(i)}: sent {len(i['sends'])}x, last {last.strftime('%b %d %I %p')}, "
                     f"{note}, back {back}")
        if (w := where(i)):
            lines.append(w)
    recent = sorted((i for i in items if i["status"] == "reviewed"), key=lambda i: i.get("answered_at", ""), reverse=True)[:15]
    lines += ["", "## Reviewed lately", ""]
    for i in recent:
        lines.append(f"* **{i['id']}** {label(i)}: {i['replies'][-1]['word'] if i['replies'] else 'reviewed'} "
                     f"({parse(i['answered_at']).strftime('%b %d')})")
        if (w := where(i)):
            lines.append(w)
    if not recent:
        lines.append("* Nothing yet")
    QUEUE_NOTE.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ------------------------------------------------------------------ main

def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("send")
    s.add_argument("kind", choices=list(LETTERS))
    s.add_argument("--dry-run", action="store_true", help="print the message, send nothing, save nothing")
    sub.add_parser("check")
    a = sub.add_parser("answer")
    a.add_argument("text")
    sub.add_parser("sheet")
    sub.add_parser("status")
    rs = sub.add_parser("resend", help="send an item again now, by id (for example P1)")
    rs.add_argument("id")
    args = p.parse_args(argv)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOCK_FILE, "w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        q = load_queue()
        if args.cmd == "sheet":
            print(build_sheet())
            return 0
        if args.cmd == "answer":
            done = answer_text(q, args.text)
            print(", ".join(done) or "No item id found (use one like P14, D3, F2 or X5)")
        elif args.cmd == "check":
            done = check(q)
            print(", ".join(done) or "No new answers")
        elif args.cmd == "resend":
            item = by_id(q).get(args.id.upper())
            c = next((x for x in candidates(item["kind"]) if x["key"] == item["key"]), None) if item else None
            if not c:
                print(f"No item {args.id}")
                return 1
            ok, error = send_text(message(item["kind"], item, c))
            if not ok:
                print(f"Send failed: {error}", file=sys.stderr)
                return 1
            item["sends"].append({"at": stamp()})
            item["status"] = "sent" if item["status"] == "new" else item["status"]
            log("resent", item)
            print(f"Sent {item['id']} again")
        elif args.cmd == "status":
            for kind in LETTERS:
                mine = [i for i in q["items"].values() if i["kind"] == kind]
                print(f"{kind}: {len(candidates(kind))} items, {sum(i['status'] == 'reviewed' for i in mine)} reviewed, "
                      f"{sum(i['status'] in ('sent', 'later') for i in mine)} waiting")
            return 0
        elif args.cmd == "send":
            if args.kind == "playbook" and not SHEET_NOTE.exists():
                print(build_sheet())
            if not args.dry_run:
                done = check(q)
                if done:
                    print("Answers: " + ", ".join(done))
            picked = pick_next(q, args.kind)
            if not picked:
                print(f"Nothing to send for {args.kind}")
                if not args.dry_run:
                    save_json(QUEUE_FILE, q)
                    write_queue_note(q)
                return 0
            c, item = picked
            text = message(args.kind, item, c)
            if args.dry_run:
                print(text)
                return 0
            ok, error = send_text(text)
            if not ok:
                log("send failed", item, error=error)
                save_json(QUEUE_FILE, q)
                print(f"Send failed: {error}", file=sys.stderr)
                return 1
            item["sends"].append({"at": stamp()})
            item["status"] = "sent"
            log("sent", item, times=len(item["sends"]))
            print(f"Sent {item['id']}: {item['title']}")
        save_json(QUEUE_FILE, q)
        write_queue_note(q)
    return 0


if __name__ == "__main__":
    sys.exit(main())
