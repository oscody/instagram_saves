#!/usr/bin/env python3
"""Look in the comments, the bio and GitHub before a dead end is left to you. Reads only, posts nothing.

For dead ends in output/dead_ends.json that need you (status needs_you), and open "link in bio" and "in the
comments" posts. Plan: vault note `ZAIHub/Vault knowledge library/Plan - IG dead ends process by claude`,
"Proposal: read the comments before Needs you" (built 2026-11-11).

Why: the "skill that updates your other skills" post (@bytesofbree, DawXrcisz6U) was left to you because
research found no public copy, but the skill was on the creator's GitHub all along.

What one run does, per post:

1. GitHub (free, no Instagram request): looks up the creator's handle on GitHub and compares their repos with
   the post's title and text. A repo that matches well is a find.
2. Instagram, looking only: opens the post in headless Firefox (the logged in profile copy that
   comment_gated.py uses) and reads the creator's own comments, the pinned comment and the caption; then opens
   the creator's profile and reads the bio link. Nothing is clicked, typed, liked or followed.
3. Sorts the post:
   * a link from the creator's comment, or a strong GitHub match: Received, with the link and where it came from
   * a comment keyword in the creator's comment (comment to get it list): Queued for an automatic comment
   * a bio link for a "link in bio" post: Received
   * other links found (a bio link on any other post, a weaker GitHub match): kept as hints in the history,
     and the post stays with you
   Every checked post gets "comments checked" in its history and is not checked again (use --again).
4. Sends one Telegram message with what it found, if it found anything.

Limits: at most 3 posts a run and 6 a day on Instagram (GitHub has no limit here), only from 9 AM to 9 PM.
Any login page, challenge or Instagram warning pauses this and commenting for 7 days (comment_gated.pause).
It also waits while commenting is paused, or downloads are blocked, logged out or paused.

    python check_comments.py --list               # which posts would be checked. No requests
    python check_comments.py --github-only        # only the GitHub look, every post. No Instagram requests
    python check_comments.py                      # GitHub and Instagram, up to 3 posts
    python check_comments.py --shortcode CODE     # one post (any status), ignores hours and the daily limit
    python check_comments.py --dry-run            # do the looks, print what it would change, save nothing
"""
import argparse
import json
import logging
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import dead_ends

HERE = Path(__file__).resolve().parent
OUTPUT_DIR = HERE / "output"
STATE_FILE = OUTPUT_DIR / "comment_checks.json"  # Instagram looks per day, for the daily limit
LOG_FILE = OUTPUT_DIR / "pipeline.log"

PER_RUN = 3
PER_DAY = 6
START_HOUR, END_HOUR = 9, 21
CHECKED = "comments checked"
TARGET_TYPES = {"link_in_bio", "in_comments", "in_the_comments"}
STOP_WORDS = {"the", "and", "for", "with", "that", "this", "your", "you", "from", "into", "how", "what", "why", "are",
              "can", "use", "using", "make", "made", "get", "all", "any", "one", "two", "new", "free", "best", "top",
              "guide", "list", "post", "reel", "video", "tips", "tip", "about", "other", "more", "most", "just",
              "will", "have", "has", "not", "but", "like", "it's", "its", "who", "when", "where", "which", "out",
              "their", "they", "them", "than", "then", "there", "here", "every", "each", "very", "only", "own"}
GITHUB_STRONG = 2  # title words a repo must share with the post to count as found
GITHUB_HEADERS = {"Accept": "application/vnd.github+json", "User-Agent": "ig-dead-ends-check"}

logger = logging.getLogger("ig_check_comments")

# A real Instagram stop sign: text in a pop up or alert, not in the post or its comments (people joke about
# "Your account has been restricted" in comments, which stopped the first run on 2026-11-11).
WARNING_JS = r"""
const re = /Try Again Later|Action Blocked|We restrict certain activity|We limit how often|Confirm it'?s you|suspicious activity|automated behavior|Your account has been/i;
for (const el of document.querySelectorAll('[role="dialog"], [role="alertdialog"], [role="alert"]')) {
  const m = (el.innerText || '').match(re);
  if (m) return m[0];
}
return null;
"""


def check_safe(driver, seen: dict) -> None:
    """comment_gated.check_safe, but a warning only counts in a pop up or alert."""
    import comment_gated as cg

    cg.check_safe({**seen, "warning": driver.execute_script(WARNING_JS)})
DEBUG = False
DEBUG_FILE = OUTPUT_DIR / "check_comments_last.json"  # what the last look read, with --debug

# The creator's own comments (and the pinned one), the caption, and every outside link on the page. Reads only.
READ_POST_JS = r"""
const author = (arguments[0] || '').toLowerCase();
const texts = [], links = new Set();
const seen = new Set();
for (const a of document.querySelectorAll('a[href]')) {
  if ((a.getAttribute('href') || '').toLowerCase() !== '/' + author + '/') continue;
  if (a.closest('header, nav, footer')) continue;
  let box = a;
  for (let i = 0; i < 6 && box.parentElement; i++) {
    box = box.parentElement;
    const t = (box.innerText || '').trim();
    if (t.length > 25 && t.length < 2500) {
      if (!seen.has(box)) {
        seen.add(box);
        texts.push(t);
        for (const l of box.querySelectorAll('a[href]')) {
          const h = l.href || '';
          if (!/^https?:\/\/(www\.)?instagram\.com\//.test(h) || /l\.instagram\.com/.test(h)) links.add(h);
        }
      }
      break;
    }
  }
}
return {texts: texts, pinned: /Pinned/i.test(document.body.innerText || ''), links: [...links]};
"""


# The bio and its links on a profile page. Reads only.
READ_PROFILE_JS = r"""
const header = document.querySelector('main header') || document.querySelector('header') || document.body;
const links = [...header.querySelectorAll('a[href]')].map(a => a.href)
  .filter(h => h && (!/^https?:\/\/(www\.)?instagram\.com\//.test(h) || /l\.instagram\.com/.test(h)));
return {bio: (header.innerText || '').slice(0, 1500), links: [...new Set(links)]};
"""


def now() -> datetime:
    return datetime.now()


def unwrap(url: str) -> str:
    """Instagram wraps outside links (l.instagram.com/?u=...); return the real address, without tracking."""
    from comment_gated import clean_link

    parts = urlsplit(url)
    if parts.netloc.endswith("l.instagram.com"):
        url = parse_qs(parts.query).get("u", [url])[0]
    return clean_link(url)


def is_useful(url: str) -> bool:
    from comment_gated import outside

    host = urlsplit(url).netloc.lower()
    return outside(url) and not host.endswith(("threads.net", "threads.com", "meta.com", "whatsapp.com"))


def words(text: str) -> set:
    return {w for w in re.findall(r"[a-z0-9][a-z0-9+.-]{2,}", (text or "").lower()) if w not in STOP_WORDS}


# ---------------------------------------------------------------- which posts


def targets(entries: list, again: bool = False, shortcode: str | None = None) -> list:
    if shortcode:
        return [e for e in entries if e["shortcode"] == shortcode]
    out = []
    for e in entries:
        wanted = e["status"] == "needs_you" or (e["status"] in ("open", "retrying") and e.get("type") in TARGET_TYPES)
        done = any(h.get("event", "").startswith(CHECKED) for h in e.get("history", []))
        if wanted and (again or not done) and e.get("author"):
            out.append(e)
    return sorted(out, key=lambda e: (not e.get("focus"), e.get("added_at") or ""))


def post_words(entry: dict) -> set:
    folder = dead_ends.post_folder(entry["shortcode"])
    text = entry.get("title") or ""
    if folder:
        for note in folder.glob("*_description.md"):
            body = note.read_text(encoding="utf-8", errors="ignore")
            text += " " + (re.search(r"^# (.+)$", body, re.M).group(1) if re.search(r"^# (.+)$", body, re.M) else "")
            caption = body.split("## Caption", 1)[1][:600] if "## Caption" in body else ""
            text += " " + caption
    return words(text)


# ---------------------------------------------------------------- GitHub


def github_get(url: str):
    req = urllib.request.Request(url, headers=GITHUB_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise


def handle_variants(author: str) -> list:
    base = author.strip("@").lower()
    variants = [base, base.replace(".", ""), base.replace("_", ""), base.replace(".", "-"), base.replace("_", "-"),
                re.sub(r"[._]+(ai|dev|tech|codes?|official|hq)$", "", base)]
    return list(dict.fromkeys(v for v in variants if v))


def check_github(entry: dict, fetch=github_get) -> dict:
    """Repos of the creator on GitHub that match the post. {"user", "strong": [...], "weak": [...]}."""
    want = post_words(entry)
    for handle in handle_variants(entry["author"]):
        try:
            user = fetch(f"https://api.github.com/users/{handle}")
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            return {"error": f"GitHub: {exc}"}
        if not user or user.get("type") not in ("User", "Organization"):
            continue
        # Same person? The GitHub profile should mention the Instagram handle, or the name should match.
        repos = fetch(f"https://api.github.com/users/{handle}/repos?per_page=100&sort=updated") or []
        scored = []
        for repo in repos:
            if repo.get("fork"):
                continue
            have = words(f"{repo.get('name', '').replace('-', ' ').replace('_', ' ')} {repo.get('description') or ''} "
                         f"{' '.join(repo.get('topics') or [])}")
            stems = {w.rstrip("s") for w in have}
            shared = {w.rstrip("s") for w in want} & stems  # skill and skills count once
            if shared:
                scored.append((len(shared), repo["html_url"], sorted(shared)))
        scored.sort(reverse=True)
        strong = [s for s in scored if s[0] >= GITHUB_STRONG]
        weak = [s for s in scored if s[0] < GITHUB_STRONG]
        # One repo only, and it shares a word: that is very likely the one.
        if not strong and len([r for r in repos if not r.get("fork")]) == 1 and weak:
            strong, weak = weak, []
        return {"user": user["html_url"], "strong": strong[:3], "weak": weak[:3]}
    return {"user": None, "strong": [], "weak": []}


# ---------------------------------------------------------------- Instagram


def why_not_now(state: dict, force: bool) -> str | None:
    import comment_gated as cg

    until = cg.paused_until()
    if until:
        return f"commenting is paused until {until:%Y-%m-%d %H:%M}, so looking waits too"
    for path in cg.OTHER_STOPS:
        if path.exists():
            return f"{path.name} exists (downloads are stopped)"
    if force:
        return None
    if not START_HOUR <= now().hour < END_HOUR:
        return f"outside hours ({START_HOUR}:00 to {END_HOUR}:00)"
    today = now().date().isoformat()
    if state.get(today, 0) >= PER_DAY:
        return f"today's limit is reached ({PER_DAY} posts)"
    return None


def read_instagram(driver, entry: dict) -> dict:
    """Open the post, then the creator's profile, and read them. Raises comment_gated.SafetyStop on a warning."""
    import comment_gated as cg

    seen = cg.open_post(driver, entry["shortcode"])
    check_safe(driver, seen)
    if seen.get("gone"):
        return {"gone": True}
    cg.human_pause(2, 4)
    post = driver.execute_script(READ_POST_JS, entry["author"])
    cg.human_pause(4, 9)
    driver.get(f"https://www.instagram.com/{entry['author']}/")
    time.sleep(6)
    check_safe(driver, cg.look(driver))
    profile = driver.execute_script(READ_PROFILE_JS)
    if DEBUG:
        DEBUG_FILE.write_text(json.dumps({"post": post, "profile": profile}, indent=1, ensure_ascii=False))
    return {"gone": False, "texts": post["texts"], "post_links": post["links"],
            "bio": profile["bio"], "bio_links": profile["links"]}


HEADER_RE = re.compile(r"^(?:\S+\n\s*\n)?(?:Edited\n•\n)?\d+[smhdwy]\n", re.M)


def saved_caption(entry: dict) -> str:
    folder = dead_ends.post_folder(entry["shortcode"])
    for note in (folder.glob("*_description.md") if folder else []):
        body = note.read_text(encoding="utf-8", errors="ignore")
        if "## Caption" in body:
            return body.split("## Caption", 1)[1].split("\n## ", 1)[0]
    return ""


def squash(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def creator_comments(entry: dict, ig: dict) -> list:
    """The creator's own comments, longest first: not the caption, not the account header, not the footer."""
    caption = squash(saved_caption(entry))
    out = []
    for text in ig.get("texts", []):
        if text.startswith("More posts from"):
            continue
        body = text.split("\n", 1)[1] if text.lower().startswith(entry["author"].lower()) and "\n" in text else text
        body = re.sub(r"^\s*(?:Edited\s*•\s*)?\d+[smhdwy]\s*", "", body.strip()).strip()
        body = re.sub(r"\n(?:Reply|See translation|Like|\d+ likes?)\s*$", "", body).strip()
        key = squash(body)
        if not key or re.search(r"(?m)^(Follow|Following|Original audio)$", body):
            continue
        if caption and (key[:80] in caption or caption[:80] in key):
            continue  # the caption, shown as the first comment
        if body not in out:
            out.append(body)
    return sorted(out, key=len, reverse=True)


def judge(entry: dict, ig: dict | None, gh: dict) -> dict:
    """What to do with a post: {"status", "link", "source", "keyword", "text", "hints"}."""
    hints = []
    if ig and not ig.get("gone"):
        long = [c for c in creator_comments(entry, ig) if len(c) >= 200]
        if long:
            from comment_gated import URL_RE

            links = [u for u in dict.fromkeys(unwrap(u) for u in URL_RE.findall(long[0])) if is_useful(u)]
            return {"status": "received", "text": long[0], "link": links[0] if links else None,
                    "source": "the creator's own comment", "hints": links[1:3]}
        texts = "\n".join(ig["texts"])
        from comment_gated import URL_RE

        in_comments = [unwrap(u) for u in URL_RE.findall(texts)] + [unwrap(u) for u in ig["post_links"]]
        in_comments = [u for u in dict.fromkeys(in_comments) if is_useful(u)]
        if in_comments:
            return {"status": "received", "link": in_comments[0], "source": "the creator's comment or caption",
                    "hints": in_comments[1:4] + [s[1] for s in gh.get("strong", [])]}
    if gh.get("strong"):
        best = gh["strong"][0]
        return {"status": "received", "link": best[1], "source": f"the creator's GitHub (matches: {', '.join(best[2])})",
                "hints": [s[1] for s in gh["strong"][1:]]}
    if ig and not ig.get("gone"):
        keyword = dead_ends.comment_keyword({"caption": "\n".join(ig["texts"]), "transcript": "", "screen": ""})
        if keyword and entry["list"] == "comment_to_get" and not entry.get("keyword"):
            return {"status": "queued", "keyword": keyword, "source": "the creator's comment", "hints": []}
        bio = [u for u in dict.fromkeys(unwrap(u) for u in ig["bio_links"]) if is_useful(u)]
        if bio and entry.get("type") == "link_in_bio":
            return {"status": "received", "link": bio[0], "source": "the creator's bio", "hints": bio[1:3]}
        hints += bio[:2]
    hints += [w[1] for w in gh.get("weak", [])[:2]]
    if gh.get("user") and not hints:
        hints.append(gh["user"])
    return {"status": None, "hints": hints}


def save_comment(entry: dict, text: str, dry_run: bool) -> str:
    """Write the creator's comment next to the post's other files. Returns the path from the repo, for the note."""
    folder = dead_ends.post_folder(entry["shortcode"])
    if not folder:
        folder = dead_ends.IG_DIR / entry["shortcode"]
    path = folder / f"{entry['shortcode']}_creator_comment.txt"
    if not dry_run:
        folder.mkdir(parents=True, exist_ok=True)
        path.write_text(f"Comment by @{entry['author']} on https://www.instagram.com/p/{entry['shortcode']}/ "
                        f"(read {now():%Y-%m-%d} by check_comments.py)\n\n{text}\n", encoding="utf-8")
    return f"IG/{folder.name}/{path.name}"


def apply(entry: dict, verdict: dict, ig: dict | None, gh: dict, dry_run: bool = False) -> str:
    stamp = dead_ends.now()
    looked = "GitHub" + (" and Instagram" if ig is not None else "")
    note = f"{CHECKED} ({looked})"
    if verdict["status"] == "received" and verdict.get("text"):
        saved = save_comment(entry, verdict["text"], dry_run)
        link = verdict.get("link") or f"creator's comment, saved in {saved}"
        entry.update(status="received", received_link=link, received_from=verdict["source"])
        note += f": the creator's comment has it ({len(verdict['text'])} characters), saved in {saved}"
    elif verdict["status"] == "received":
        entry.update(status="received", received_link=verdict["link"], received_from=verdict["source"])
        note += f": found {verdict['link']} in {verdict['source']}"
    elif verdict["status"] == "queued":
        entry.update(status="queued", keyword=verdict["keyword"])
        note += f": keyword {verdict['keyword']} in {verdict['source']}, queued for an automatic comment"
    elif ig and ig.get("gone"):
        note += ": the post is gone"
    else:
        note += ": nothing found"
    if verdict.get("hints"):
        note += "; maybe: " + ", ".join(verdict["hints"][:4])
    if gh.get("error"):
        note += f"; {gh['error']}"
    entry["history"].append({"at": stamp, "event": note[:600]})
    entry["comments_checked_at"] = stamp
    entry["updated_at"] = stamp
    return note


# ---------------------------------------------------------------- one run


def run(github_only: bool, shortcode: str | None, again: bool, dry_run: bool, limit: int) -> int:
    import comment_gated as cg

    entries = dead_ends.load()
    todo = targets(entries, again or bool(shortcode), shortcode)
    if not todo:
        print("Nothing to check")
        return 0
    state = cg.read_json(STATE_FILE, {})
    reason = None if github_only else why_not_now(state, force=bool(shortcode))
    if reason and not github_only:
        print(f"Instagram look skipped: {reason}. Doing the GitHub look only.")
    use_ig = not github_only and reason is None
    lock = cg.pipeline_lock() if use_ig else True
    if use_ig and lock is None:
        print("The pipeline is running; the Instagram look waits. Doing the GitHub look only.")
        use_ig = False

    results, ig_left = [], min(limit, PER_DAY - state.get(now().date().isoformat(), 0)) if use_ig else 0
    if shortcode:
        ig_left = 1 if use_ig else 0
    for entry in todo:
        gh = check_github(entry)
        time.sleep(1)
        ig = None
        if ig_left > 0:
            try:
                ig = cg.with_browser(lambda d: read_instagram(d, entry), f"look_{entry['shortcode']}")
            except cg.SafetyStop as exc:
                cg.pause(f"looking at comments: {exc}")
                print(f"Stopped: {exc}")
                ig_left = 0
            except Exception as exc:  # noqa: BLE001 - one bad page must not stop the run
                logger.exception(f"Could not read {entry['shortcode']}")
                print(f"{entry['shortcode']}: could not read the page ({exc})")
            else:
                ig_left -= 1
                day = now().date().isoformat()
                state[day] = state.get(day, 0) + 1
                if not dry_run:
                    OUTPUT_DIR.mkdir(exist_ok=True)
                    STATE_FILE.write_text(json.dumps(state, indent=1) + "\n")
        elif use_ig:
            # This run's Instagram looks are used up: leave the post for the next run, unless GitHub found it.
            if judge(entry, None, gh)["status"] is None:
                print(f"{entry['shortcode']}: GitHub found nothing; the Instagram look is left for the next run")
                continue
        verdict = judge(entry, ig, gh)
        results.append((entry, verdict, ig, gh))

    lines = []
    with dead_ends.locked():
        fresh = dead_ends.load()
        for entry, verdict, ig, gh in results:
            if ig is None and verdict["status"] is None:
                # Found nothing without reading Instagram: not checked yet, since the comments are still unread.
                print(f"{entry['shortcode']}: GitHub found nothing" + (f" (hints: {', '.join(verdict['hints'])})" if verdict["hints"] else ""))
                continue
            target = dead_ends.find(fresh, entry["shortcode"], entry["stage"])
            if not target:
                continue
            note = apply(target if not dry_run else json.loads(json.dumps(target)), verdict, ig, gh, dry_run)
            print(f"{entry['shortcode']}: {note}")
            if verdict["status"]:
                label = "Received" if verdict["status"] == "received" else "Queued"
                lines.append(f"* {label}: {entry.get('title') or entry['shortcode']} (@{entry['author']})\n  "
                             f"{verdict.get('link') or ('full text saved in the post folder' if verdict.get('text') else 'comment ' + verdict.get('keyword', ''))}\n  from {verdict['source']}")
        if not dry_run:
            dead_ends.save(fresh)
    if lines and not dry_run:
        cg.send("🔎 Dead ends: found in the comments, bio or GitHub\n\n" + "\n".join(lines) +
                "\n\nCheck them in the dead ends notes. A wrong one: clear its Link: line and untick it.")
    if lock not in (True, None):
        lock.close()
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--list", action="store_true", help="which posts would be checked; no requests")
    p.add_argument("--github-only", action="store_true", help="only the GitHub look; no Instagram requests")
    p.add_argument("--shortcode", help="check this one post")
    p.add_argument("--again", action="store_true", help="also posts that were checked before")
    p.add_argument("--dry-run", action="store_true", help="do the looks, save nothing, send nothing")
    p.add_argument("--limit", type=int, default=PER_RUN, help=f"Instagram looks this run (default {PER_RUN})")
    p.add_argument("--debug", action="store_true", help=f"save what the pages showed to {DEBUG_FILE.name}")
    args = p.parse_args(argv)
    global DEBUG
    DEBUG = args.debug
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s",
                        handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()] if LOG_FILE.parent.exists() else None)
    if args.list:
        for e in targets(dead_ends.load(), args.again, args.shortcode):
            print(f"{e['shortcode']}  {e['status']:10} {e.get('type', ''):12} @{e['author']}: {e.get('title', '')[:60]}")
        return 0
    return run(args.github_only, args.shortcode, args.again, args.dry_run, args.limit)


if __name__ == "__main__":
    sys.exit(main())
