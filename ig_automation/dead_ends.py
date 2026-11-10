#!/usr/bin/env python3
"""Track posts the pipeline could not finish, in one JSON array: output/dead_ends.json.

Two lists share the file, told apart by `list`:

* `comment_to_get`: the creator only sends the resource after a comment or DM ("Comment RESET and I'll
  send it"). Statuses: queued, commented_waiting, received, needs_you, closed, resolved.
* `other`: every other dead end: a pipeline stage failed (download, transcribe, describe), research
  failed, or research found nothing. Statuses: open, retrying, needs_you, closed, resolved.

There is one entry per post and stage (`shortcode` + `stage`). Entries are added or updated by:

* research.py, right after each post (`update_from_research`), and
* sync(), which run_pipeline.py calls once per run, and `python3 dead_ends.py` runs by hand. It reads the
  export file (stage errors) and output/research.json (verdicts), so it also catches anything added
  while research.py was not running this code.

Statuses set by you or by later automation (commented_waiting, received, needs_you, closed) are never
overwritten. When the stage later works (an error clears, a verdict is no longer Unresolved), the entry
becomes `resolved`, unless it was closed. Nothing is ever deleted, so the file is also the history.

    python3 dead_ends.py            # sync, then print the counts
    python3 dead_ends.py --list     # also print each open entry
"""

import argparse
import fcntl
import json
import os
import re
import unicodedata
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUTPUT_DIR = HERE / "output"
DEAD_ENDS_FILE = OUTPUT_DIR / "dead_ends.json"
LOCK_FILE = OUTPUT_DIR / "dead_ends.lock"
EXPORT_FILE = OUTPUT_DIR / "iambogle.json"
RESEARCH_FILE = OUTPUT_DIR / "research.json"
IG_DIR = HERE.parent / "IG"
TOPICS_FILE = HERE.parent / "knowledge_library" / "topics.json"
PROFILE_FILE = HERE.parent / "interest_feed" / "profile.json"
# The vault notes for both lists. First folder that exists is the vault; IG_VAULT overrides it.
VAULT_GUESSES = [Path.home() / "Dev/obsidian/Bogle", Path.home() / "Work/obsidian/Bogle", Path.home() / "obsidian/Bogle",
                 Path.home() / "Work/2025Secondbrain"]
VAULT_DIR = Path("ZAIHub/Vault knowledge library")
VAULT_NOTES = {"comment_to_get": "IG dead ends - comment to get it", "other": "IG dead ends - other"}

RETRY_DAYS = (3, 20)  # days until the first and second research retry (chosen 2026-11-10); retries for posts whose resource may go public later
THIN_WORDS = 15  # fewer words of speech plus on screen text than this is thin input
# Statuses a person or later automation set. sync() and research.py leave them alone.
KEPT = {"commented_waiting", "received", "needs_you", "closed"}
OPEN = {"queued", "open", "retrying", "commented_waiting", "needs_you"}

# "Comment RESET", "comment the word 'CODE'", "Comment “GHOST” and I'll send...", "type SEARCH below"
KEYWORD_RE = re.compile(
    r"""\b(?:comment(?:ing)?|type|reply|drop|dm)(?:\s+(?:or|and)\s+dm)?(?:\s+me)?\s+(?:down\s+)?(?:below\s+)?"""
    r"""(?:the\s+word[,:]?\s+|with\s+)?["'“”‘’(\[«]?([A-Za-z0-9#@_-]{2,25})["'“”‘’)\]»]?""", re.I)
NOT_KEYWORDS = {"below", "down", "the", "a", "an", "and", "if", "for", "this", "it", "me", "your", "my", "in", "on",
                "with", "here", "now", "yes", "section", "box", "please", "or", "to", "from", "word", "dm", "us",
                "you", "them", "if", "below", "down", "and"}
DM_RE = re.compile(r"\b(dm|dms|direct message|inbox|sent after|send (?:it|you|em|them)|i'?ll send|link sent)\b", re.I)
IN_COMMENTS_RE = re.compile(r"\b(in the comments|pinned comment|first comment|comment section)\b", re.I)
BIO_RE = re.compile(r"\blink in (?:my |the )?bio\b", re.I)
PAYWALL_RE = re.compile(r"\b(paywall|paid|course|membership|subscription|skool|patreon|gumroad|purchase|\$\d+)\b", re.I)
GONE_RE = re.compile(r"\b(404|deleted|removed|private|no longer (?:available|exists)|not available|unavailable|gone)\b",
                     re.I)
UNNAMED_RE = re.compile(r"\b(never names?|not named|no name|unnamed|does not (?:say|name)|doesn't (?:say|name)|"
                        r"unclear which|could not identify|can'?t identify)\b", re.I)


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def plain(text: str) -> str:
    """Fancy bold and italic letters (𝗖𝗼𝗱𝗲) back to plain text, so keywords match."""
    return unicodedata.normalize("NFKC", text or "")


@contextmanager
def locked():
    """Hold the file lock while reading and writing, since research.py and the pipeline can overlap."""
    OUTPUT_DIR.mkdir(exist_ok=True)
    with LOCK_FILE.open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield


def load() -> list:
    try:
        data = json.loads(DEAD_ENDS_FILE.read_text())
        return data if isinstance(data, list) else []
    except (OSError, ValueError):
        return []


def save(entries: list) -> None:
    entries.sort(key=lambda e: (e["list"] != "comment_to_get", not e.get("focus"), e["status"] not in OPEN,
                                e.get("added_at", "")))
    tmp = DEAD_ENDS_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(entries, indent=1, ensure_ascii=False) + "\n")
    tmp.replace(DEAD_ENDS_FILE)


# ---------------------------------------------------------------- post details


def post_folder(shortcode: str) -> Path | None:
    return next((f for f in IG_DIR.glob(f"*_{shortcode}") if f.is_dir()), None)


def post_text(shortcode: str, record: dict) -> dict:
    """Caption, transcript and on screen text for a post, as plain text."""
    folder = post_folder(shortcode)

    def read(pattern: str) -> str:
        if not folder:
            return ""
        return "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in sorted(folder.glob(pattern)))
    return {"caption": plain(record.get("caption") or ""), "transcript": plain(read("*_transcript.txt")),
            "screen": plain(read("*_ocr.txt"))}


def comment_keyword(texts: dict) -> str | None:
    """The word the creator asks you to comment, from the caption first, then the transcript and screen."""
    for name in ("caption", "transcript", "screen"):
        for match in KEYWORD_RE.finditer(texts[name]):
            word = match.group(1).strip("#@")
            if word.lower() not in NOT_KEYWORDS and not word.isdigit():
                return word
    return None


def focus_shortcodes() -> set:
    """Posts in the Focus topics (interest_feed/profile.json library_topics)."""
    try:
        profile = json.loads(PROFILE_FILE.read_text())
        topics = profile["topics"]
        slugs = {s for t in (topics.values() if isinstance(topics, dict) else topics) for s in t.get("library_topics", [])}
        data = json.loads(TOPICS_FILE.read_text())
        return {code for t in data["topics"] if t["slug"] in slugs for code in t["sources"]}
    except (OSError, ValueError, KeyError, TypeError):
        return set()


# ---------------------------------------------------------------- sorting a dead end


def classify_research(result: dict, texts: dict) -> tuple[str, str, str | None]:
    """(list, type, keyword) for a research result that found nothing."""
    reason = plain(result.get("not_found") or "") + " " + plain(result.get("verdict_reason") or "")
    keyword = comment_keyword(texts)
    asks_dm = DM_RE.search(texts["caption"]) or DM_RE.search(reason)
    if keyword and (asks_dm or re.search(r"\bcomment", texts["caption"] + reason, re.I)):
        return "comment_to_get", "gated", keyword
    if asks_dm or re.search(r"\b(comment|dm)\b.{0,40}\b(send|link|guide|get)\b", reason, re.I):
        return "comment_to_get", "gated", None  # gated, but the keyword is unclear
    if IN_COMMENTS_RE.search(texts["caption"]) or IN_COMMENTS_RE.search(reason):
        return "other", "in_comments", None
    if BIO_RE.search(texts["caption"]) or BIO_RE.search(reason):
        return "other", "link_in_bio", None
    if PAYWALL_RE.search(reason):
        return "other", "paywalled", None
    if GONE_RE.search(reason):
        return "other", "gone", None
    if UNNAMED_RE.search(reason):
        return "other", "unnamed", None
    if len((texts["transcript"] + " " + texts["screen"]).split()) < THIN_WORDS:
        return "other", "thin_input", None
    return "other", "not_found", None


def stage_of(record: dict) -> str:
    """The pipeline stage a failed post is stuck at."""
    if not record.get("downloaded"):
        return "download"
    if not record.get("transcribed"):
        return "transcribe"
    return "describe"


def stage_type(stage: str, error: str) -> str:
    if stage == "download" and GONE_RE.search(error):
        return "gone"
    return f"{stage}_failed"


# ---------------------------------------------------------------- adding and resolving


def find(entries: list, shortcode: str, stage: str) -> dict | None:
    return next((e for e in entries if e["shortcode"] == shortcode and e["stage"] == stage), None)


def upsert(entries: list, shortcode: str, stage: str, list_name: str, kind: str, reason: str,
           record: dict | None = None, keyword: str | None = None, covered_by: list | None = None,
           focus: bool = False) -> str:
    """Add or update one dead end. Returns 'added', 'updated' or 'kept'."""
    record = record or {}
    stamp = now()
    entry = find(entries, shortcode, stage)
    if entry is None:
        status = ("queued" if keyword else "needs_you") if list_name == "comment_to_get" else "open"
        retry = None
        if stage == "research" and kind in ("not_found", "unnamed", "thin_input"):
            retry = (datetime.now() + timedelta(days=RETRY_DAYS[0])).date().isoformat()
        entry = {
            "shortcode": shortcode,
            "list": list_name,
            "stage": stage,
            "type": kind,
            "status": status,
            "reason": reason,
            "keyword": keyword,
            "focus": focus,
            "url": record.get("url") or f"https://instagram.com/p/{shortcode}/",
            "author": record.get("author"),
            "title": record.get("ai_title"),
            "covered_by": covered_by or [],
            "next_retry": retry,
            "attempts": [],
            "added_at": stamp,
            "updated_at": stamp,
            "history": [{"at": stamp, "event": f"added: {kind}"}],
        }
        if list_name == "comment_to_get" and not keyword:
            entry["history"].append({"at": stamp, "event": "needs you: comment keyword unclear"})
        entries.append(entry)
        return "added"
    changed = False
    if entry["status"] == "resolved":  # it failed again
        entry["status"] = ("queued" if keyword else "needs_you") if list_name == "comment_to_get" else "open"
        entry["history"].append({"at": stamp, "event": f"failed again: {kind}"})
        changed = True
    if entry["status"] not in KEPT:
        for key, value in (("list", list_name), ("type", kind), ("reason", reason), ("keyword", keyword or entry.get("keyword"))):
            if entry.get(key) != value:
                entry[key] = value
                changed = True
    for key, value in (("focus", focus), ("covered_by", covered_by or entry.get("covered_by") or [])):
        if entry.get(key) != value:
            entry[key] = value
            changed = True
    if changed:
        entry["updated_at"] = stamp
    return "updated" if changed else "kept"


def resolve(entries: list, shortcode: str, stage: str, why: str) -> bool:
    entry = find(entries, shortcode, stage)
    if not entry or entry["status"] in ("resolved", "closed", "received"):
        return False
    entry["status"] = "resolved"
    entry["updated_at"] = now()
    entry["history"].append({"at": entry["updated_at"], "event": f"resolved: {why}"})
    return True


def covered(result: dict) -> list:
    """Saved posts research found with the same or a similar resource."""
    return [{"shortcode": p["shortcode"], "relation": p["relation"]} for p in result.get("ig_posts") or []]


def apply_research(entries: list, shortcode: str, result: dict, record: dict, focus: set) -> str | None:
    """Add, update or resolve the research entry for one post. Returns what happened, or None."""
    if result.get("error"):
        return upsert(entries, shortcode, "research", "other", "research_failed", str(result["error"])[:300],
                      record, focus=shortcode in focus)
    if result.get("verdict") == "unresolved":
        texts = post_text(shortcode, record)
        list_name, kind, keyword = classify_research(result, texts)
        reason = " ".join(plain(result.get("not_found") or result.get("verdict_reason") or "").split())[:400]
        return upsert(entries, shortcode, "research", list_name, kind, reason, record, keyword,
                      covered(result), shortcode in focus)
    if result.get("verdict"):
        return "resolved" if resolve(entries, shortcode, "research", f"verdict {result['verdict']}") else None
    return None


def update_from_research(shortcode: str, result: dict) -> None:
    """research.py calls this after each post (or failed post)."""
    try:
        links = json.loads(EXPORT_FILE.read_text())["links"]
        record = next((r for r in links if r.get("shortcode") == shortcode), {})
    except (OSError, ValueError, KeyError):
        record = {}
    with locked():
        entries = load()
        apply_research(entries, shortcode, result, record, focus_shortcodes())
        save(entries)


def sync() -> dict:
    """Bring the file up to date from the export file and research.json. Code only, no network."""
    counts = {"added": 0, "updated": 0, "resolved": 0}
    links = json.loads(EXPORT_FILE.read_text())["links"]
    by_code = {r["shortcode"]: r for r in links if r.get("shortcode")}
    try:
        research = json.loads(RESEARCH_FILE.read_text())
    except (OSError, ValueError):
        research = {}
    focus = focus_shortcodes()
    vault = find_vault()
    with locked():
        entries = load()
        if vault:
            counts["answers"] = read_answers(entries, vault)
        # Pipeline stages: a post with an error is stuck at the first stage it has not finished.
        for code, record in by_code.items():
            stuck = stage_of(record) if record.get("error") else None
            if stuck:
                error = " ".join(str(record["error"]).split())[:300]
                what = upsert(entries, code, stuck, "other", stage_type(stuck, error), error, record,
                              focus=code in focus)
                counts[what] = counts.get(what, 0) + 1
            for stage in ("download", "transcribe", "describe"):
                if stage != stuck and resolve(entries, code, stage, "the stage worked"):
                    counts["resolved"] += 1
        # Research.
        for code, result in research.items():
            if isinstance(result, dict):
                what = apply_research(entries, code, result, by_code.get(code, {}), focus)
                if what:
                    counts[what] = counts.get(what, 0) + 1
        save(entries)
        if vault:
            write_notes(entries, vault)
    counts.pop("kept", None)
    return counts


# ---------------------------------------------------------------- vault notes


def find_vault() -> Path | None:
    for path in [os.environ.get("IG_VAULT"), *VAULT_GUESSES]:
        if path and Path(path).expanduser().is_dir():
            return Path(path).expanduser()
    return None


ENTRY_RE = re.compile(r"^\* \[( |x|X)\] .*?\(`([A-Za-z0-9_-]{6,20})`", re.M)
LINK_RE = re.compile(r"^\t\* Link: *(\S.*)?$", re.M)


def read_answers(entries: list, vault: Path) -> int:
    """Apply what you ticked or filled in the vault notes. A link means received; a tick alone means closed."""
    changed = 0
    for list_name, name in VAULT_NOTES.items():
        path = vault / VAULT_DIR / f"{name}.md"
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        starts = [m for m in ENTRY_RE.finditer(text)]
        for i, match in enumerate(starts):
            block = text[match.start():starts[i + 1].start() if i + 1 < len(starts) else len(text)]
            link = (LINK_RE.search(block).group(1) or "").strip() if LINK_RE.search(block) else ""
            ticked = match.group(1).lower() == "x"
            code = match.group(2)
            for entry in entries:
                if entry["shortcode"] != code or entry["list"] != list_name or entry["status"] in ("resolved",):
                    continue
                stamp = now()
                if link and entry.get("received_link") != link:
                    entry.update(status="received", received_link=link, updated_at=stamp)
                    entry["history"].append({"at": stamp, "event": f"received by you: {link[:200]}"})
                    changed += 1
                elif ticked and not link and entry["status"] not in ("closed", "received"):
                    entry.update(status="closed", updated_at=stamp)
                    entry["history"].append({"at": stamp, "event": "closed by you in the vault list"})
                    changed += 1
    return changed


TYPE_LABELS = {
    "gated": "Comment to get it", "not_found": "Not found yet", "unnamed": "Tool never named",
    "thin_input": "Almost no text to work from", "paywalled": "Paywalled", "link_in_bio": "Link in bio",
    "in_comments": "In the comments", "gone": "Deleted or private", "research_failed": "Research failed",
    "download_failed": "Download failed", "transcribe_failed": "Transcribe failed", "describe_failed": "Describe failed",
}
STATUS_ORDER = ["needs_you", "queued", "commented_waiting", "open", "retrying", "received", "closed"]
STATUS_LABELS = {"needs_you": "Needs you", "queued": "Queued for an automatic comment",
                 "commented_waiting": "Commented, waiting for the DM", "open": "Open", "retrying": "Retrying",
                 "received": "Received", "closed": "Closed"}


def clean(text: str) -> str:
    """One line, no em dashes (vault rule)."""
    return " ".join((text or "").replace("\u2014", ", ").split())


def entry_lines(entry: dict) -> list[str]:
    title = clean(entry.get("title") or entry["shortcode"])
    who = f", @{entry['author']}" if entry.get("author") else ""
    tick = "x" if entry["status"] in ("received", "closed") else " "
    head = f"* [{tick}] **{title}**: Web: [post (instagram.com)]({entry['url']}) (`{entry['shortcode']}`{who})"
    lines = [head]
    if entry["list"] == "comment_to_get":
        lines.append(f"\t* Comment: `{entry['keyword']}`" if entry.get("keyword") else "\t* Comment: keyword unclear, check the post")
    else:
        lines.append(f"\t* Type: {TYPE_LABELS.get(entry['type'], entry['type'])}")
    if entry.get("reason"):
        reason = clean(entry["reason"])
        if len(reason) > 220:
            reason = reason[:220].rsplit(" ", 1)[0].rstrip(",.;:") + "..."
        lines.append(f"\t* Missing: {reason}")
    if entry.get("covered_by"):
        codes = ", ".join(f"`{c['shortcode']}` ({c['relation']})" for c in entry["covered_by"])
        lines.append(f"\t* Already saved: {codes}")
    if entry.get("next_retry") and entry["status"] in OPEN:
        lines.append(f"\t* Next automatic retry: {entry['next_retry']}")
    lines.append(f"\t* Link: {entry.get('received_link') or ''}".rstrip())
    return lines


def note_text(entries: list, list_name: str, created: str) -> str:
    mine = [e for e in entries if e["list"] == list_name and e["status"] != "resolved"]
    title = VAULT_NOTES[list_name]
    open_count = sum(e["status"] in OPEN for e in mine)
    if list_name == "comment_to_get":
        intro = ("Posts where the creator only sends the resource after a comment or DM. Automatic comments will "
                 "work through the queue (not built yet); anything that fails moves to Needs you.")
    else:
        intro = ("Every other post the pipeline or research could not finish: a stage failed, or research found "
                 "nothing. Posts that may go public later are retried automatically (3 days, then 20 days).")
    out = [
        "---", f"name: {title}", f"created: {created}", "---", "",
        "#instaLearning #todo", "",
        f"# {title}", "",
        f"Built by Outside vault: `{HERE / 'dead_ends.py'}` from Outside vault: `{DEAD_ENDS_FILE}`. "
        "Rebuilt on every pipeline run. Plan: [[Plan - IG dead ends process by claude]].", "",
        intro, "",
        "**How to answer:** paste what you got after `Link:` (it becomes Received), or tick the box with no link "
        "to close it (not worth it, or skip). The next pipeline run reads your answers.", "",
        f"Open: {open_count}. Updated: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}.", "",
    ]
    for focus_part, heading in ((True, "Focus topics"), (False, "Everything else")):
        part = [e for e in mine if bool(e.get("focus")) == focus_part]
        out += [f"## {heading} ({len(part)})", ""]
        if not part:
            out += ["* none", ""]
            continue
        # Comment list: by status. Other list: open posts by type, then received and closed.
        if list_name == "comment_to_get":
            groups = [(STATUS_LABELS[st], [e for e in part if e["status"] == st]) for st in STATUS_ORDER]
        else:
            done = ("received", "closed")
            groups = [(f"Needs you: {TYPE_LABELS.get(t, t)}" if any(e["status"] == "needs_you" for e in part if e["type"] == t)
                       else TYPE_LABELS.get(t, t),
                       [e for e in part if e["type"] == t and e["status"] not in done]) for t in TYPE_LABELS]
            groups += [(STATUS_LABELS[st], [e for e in part if e["status"] == st]) for st in done]
        for heading, group in groups:
            if not group:
                continue
            out += [f"### {heading} ({len(group)})", ""]
            for entry in sorted(group, key=lambda e: e.get("added_at", ""), reverse=True):
                out += entry_lines(entry)
            out.append("")
    return "\n".join(out).rstrip() + "\n"


def write_notes(entries: list, vault: Path) -> None:
    """Rebuild both vault notes. A note is only written when it changed, apart from its Updated line."""
    folder = vault / VAULT_DIR
    if not folder.is_dir():
        return
    for list_name, name in VAULT_NOTES.items():
        path = folder / f"{name}.md"
        old = path.read_text(encoding="utf-8") if path.exists() else ""
        created = re.search(r"^created: (\S+)", old, re.M)
        text = note_text(entries, list_name, created.group(1) if created else datetime.now().date().isoformat())
        strip = lambda t: re.sub(r"Updated: [^\n]*", "", t)  # noqa: E731
        if strip(text) != strip(old):
            path.write_text(text, encoding="utf-8")


def summary(entries: list | None = None) -> dict:
    """Open entries per list, and how many need you."""
    entries = load() if entries is None else entries
    open_entries = [e for e in entries if e["status"] in OPEN]
    return {
        "comment_to_get": sum(e["list"] == "comment_to_get" for e in open_entries),
        "other": sum(e["list"] == "other" for e in open_entries),
        "needs_you": sum(e["status"] == "needs_you" for e in open_entries),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--list", action="store_true", help="Print each open entry after syncing.")
    args = parser.parse_args()
    counts = sync()
    entries = load()
    print(f"Synced {DEAD_ENDS_FILE}: {counts}")
    by = {}
    for e in entries:
        by.setdefault((e["list"], e["type"], e["status"]), 0)
        by[(e["list"], e["type"], e["status"])] += 1
    for (list_name, kind, status), n in sorted(by.items()):
        print(f"  {list_name:15} {kind:16} {status:18} {n}")
    print(f"Open: {summary(entries)}")
    if args.list:
        for e in entries:
            if e["status"] in OPEN:
                print(f"{e['shortcode']:12} {e['list']:15} {e['type']:14} {e['status']:12} "
                      f"{(e.get('keyword') or ''):10} {'focus ' if e.get('focus') else ''}{e['reason'][:80]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
