#!/usr/bin/env python3
"""Comment the keyword on "comment to get it" posts, then ask you on Telegram to finish in the DM.

For posts in output/dead_ends.json on the `comment_to_get` list with status `queued` (dead_ends.py).
Plan: vault note `ZAIHub/Vault knowledge library/Plan - IG dead ends process by claude`, "Step 4 design".

What one run does, for at most one post:

1. Picks the next queued post, Focus topics first.
2. Opens it in headless Firefox on a throwaway copy of the logged in profile (like export_chat_browser.py).
3. Follows the account if you do not follow it yet. Many creators only send the DM to followers.
4. Types the keyword as a comment and posts it.
5. Marks the post `commented_waiting` and sends a Telegram message (through Hermes): open the DM on your
   phone and tap the button. The DM buttons only show in the phone app, so a person finishes it.
6. You paste what you got after `Link:` in the vault list; dead_ends.py makes it `received`.

It also follows up, with no Instagram requests: one Telegram reminder after REMIND_DAYS without a link,
and `needs_you` after GIVE_UP_DAYS.

Limits, so it does not look like a bot: at most 2 or 3 comments a day (picked per day), only between
START_HOUR and END_HOUR, at least MIN_GAP_MINUTES apart, and each run only comments about half the time.

Safety stop: a login page, a challenge, an Instagram warning, or a comment that does not show up pauses
all commenting for PAUSE_DAYS (output/COMMENT_PAUSED) and sends a Telegram alert. It also does nothing while
downloads are blocked, logged out or paused (output/BLOCKED, LOGGED_OUT, PAUSED).

    python comment_gated.py --status              # limits, pause, what is next. No Instagram requests
    python comment_gated.py --probe CODE          # open the post and report what it sees. Clicks nothing
    python comment_gated.py --shortcode CODE --now  # comment on this post now (ignores hours, gap and chance)
    python comment_gated.py                       # what the pipeline runs: maybe comment on one post
    python comment_gated.py --resume              # lift the pause by hand

Run it with the venv Python (it needs selenium): ../Instagram-Saves-Engine/.venv/bin/python
"""

import argparse
import fcntl
import json
import logging
import os
import random
import shutil
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

import dead_ends

HERE = Path(__file__).resolve().parent
OUTPUT_DIR = HERE / "output"
STATE_FILE = OUTPUT_DIR / "comment_state.json"  # every comment made, for the daily limit
PAUSED_FILE = OUTPUT_DIR / "COMMENT_PAUSED"  # JSON {"until": ..., "reason": ...}
SHOTS_DIR = OUTPUT_DIR / "comment_shots"  # a screenshot per comment or failure, newest 40 kept
PIPELINE_LOCK = OUTPUT_DIR / "pipeline.lock"
LOG_FILE = OUTPUT_DIR / "pipeline.log"
# Files of the download side. Commenting stops while any of them exists.
OTHER_STOPS = [OUTPUT_DIR / "BLOCKED", OUTPUT_DIR / "LOGGED_OUT", OUTPUT_DIR / "PAUSED"]
# The account Firefox is logged into, which posts the comments and gets the DMs. Other people comment the same
# keyword, so a comment only counts as ours when it sits next to this name.
OWN_USERNAME = os.environ.get("IG_USERNAME", "djboglemusic")
# Your main account. If it already commented the keyword by hand, nothing is posted and its DM is the one to check.
MAIN_USERNAME = os.environ.get("IG_MAIN_USERNAME", "iambogle")
FIREFOX_PROFILE = Path.home() / ".config/mozilla/firefox/413ffz8o.default-esr"

DAILY_MIN, DAILY_MAX = 2, 3  # comments per day; the day's number is picked from the date
START_HOUR, END_HOUR = 9, 21  # local time; never at night
MIN_GAP_MINUTES = 90
RUN_CHANCE = 0.5  # share of pipeline runs that comment, so the times vary
PAUSE_DAYS = 7
REMIND_DAYS = 3  # days after the comment before one Telegram reminder
GIVE_UP_DAYS = 7  # days after the comment before the post moves to needs_you

logger = logging.getLogger("ig_comment")

# What the page shows. Returns the facts the Python side decides on. Clicks nothing.
LOOK_JS = r"""
const text = (document.body.innerText || '');
const has = (re) => re.test(text);
const visible = (el) => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
const buttons = [...document.querySelectorAll('button, div[role="button"]')].filter(visible);
const label = (el) => (el.innerText || '').trim();
const box = [...document.querySelectorAll('textarea, [contenteditable="true"]')].filter(visible)
  .find(el => /comment/i.test(el.getAttribute('aria-label') || el.getAttribute('placeholder') || ''));
return {
  url: location.href,
  title: document.title,
  login: /\/accounts\/login/.test(location.pathname) || !!document.querySelector('input[name="username"]'),
  challenge: /\/challenge|\/accounts\/suspended|\/accounts\/disabled/.test(location.pathname),
  warning: (text.match(/Try Again Later|Action Blocked|We restrict certain activity|We limit how often|Confirm it'?s you|suspicious activity|automated behavior|Your account has been|couldn'?t post comment/i) || [null])[0],
  gone: has(/Sorry, this page isn'?t available|Post isn'?t available|may have been removed|Page Not Found/i),
  comments_off: has(/Comments on this post have been limited|Comments are turned off|Commenting has been turned off/i),
  follow: buttons.some(b => label(b) === 'Follow'),
  following: buttons.some(b => /^(Following|Requested)$/.test(label(b))),
  box: !!box,
  box_tag: box ? box.tagName : null,
  post_button: buttons.some(b => label(b) === 'Post'),
};
"""

CLICK_FOLLOW_JS = r"""
const visible = (el) => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
const b = [...document.querySelectorAll('button, div[role="button"]')].filter(visible)
  .find(el => (el.innerText || '').trim() === 'Follow');
if (!b) return false;
b.scrollIntoView({block: 'center'});
b.click();
return true;
"""

FIND_BOX_JS = r"""
const visible = (el) => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
return [...document.querySelectorAll('textarea, [contenteditable="true"]')].filter(visible)
  .find(el => /comment/i.test(el.getAttribute('aria-label') || el.getAttribute('placeholder') || '')) || null;
"""

FIND_POST_JS = r"""
const visible = (el) => { const r = el.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
return [...document.querySelectorAll('button, div[role="button"]')].filter(visible)
  .find(el => (el.innerText || '').trim() === 'Post') || null;
"""

# How many comments by our own account have exactly this text (any letter case). Other people comment the
# same keyword, so the text alone proves nothing: the comment must sit next to a link to our profile.
OUR_COMMENTS_JS = r"""
const want = arguments[0].trim().toLowerCase();
const me = arguments[1].toLowerCase();
let count = 0;
for (const el of document.querySelectorAll('span, div')) {
  if (el.children.length !== 0 || (el.textContent || '').trim().toLowerCase() !== want) continue;
  let box = el;
  for (let i = 0; i < 7 && box.parentElement; i++) {
    box = box.parentElement;
    const mine = [...box.querySelectorAll('a[href]')].some(a => a.getAttribute('href').toLowerCase() === '/' + me + '/');
    if (mine) { if ((box.innerText || '').length < 300) count++; break; }
  }
}
return count;
"""


class SafetyStop(Exception):
    """Instagram showed a login page, a challenge or a warning, or the comment did not go through."""


class AlreadyCommented(Exception):
    """Our account already commented this keyword on the post, by hand. Nothing is posted again."""


class PostProblem(Exception):
    """This post cannot be commented on (gone, comments off). Not a reason to pause."""


# ---------------------------------------------------------------- state and limits


def read_json(path: Path, fallback):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return fallback


def load_state() -> dict:
    state = read_json(STATE_FILE, {})
    state.setdefault("comments", [])
    return state


def save_state(state: dict) -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=1, ensure_ascii=False) + "\n")
    tmp.replace(STATE_FILE)


def paused_until() -> "datetime | None":
    """When the commenting pause ends, or None. An expired pause file is removed."""
    data = read_json(PAUSED_FILE, None)
    if not data:
        return None
    try:
        until = datetime.fromisoformat(data["until"])
    except (KeyError, ValueError, TypeError):
        return datetime.max  # unreadable file: stay paused until someone looks
    if until <= datetime.now():
        PAUSED_FILE.unlink(missing_ok=True)
        return None
    return until


def daily_limit(day: str) -> int:
    return random.Random(f"comments-{day}").randint(DAILY_MIN, DAILY_MAX)


def why_not_now(state: dict, now: "datetime | None" = None) -> "str | None":
    """The reason commenting should not happen right now, or None when it may."""
    now = now or datetime.now()
    until = paused_until()
    if until:
        return f"commenting is paused until {until:%Y-%m-%d %H:%M}"
    for path in OTHER_STOPS:
        if path.exists():
            return f"{path.name} exists (downloads are stopped), so commenting waits too"
    if not START_HOUR <= now.hour < END_HOUR:
        return f"outside commenting hours ({START_HOUR}:00 to {END_HOUR}:00)"
    today = now.date().isoformat()
    done_today = [c for c in state["comments"] if c["at"].startswith(today)]
    if len(done_today) >= daily_limit(today):
        return f"today's limit is reached ({len(done_today)} of {daily_limit(today)})"
    if state["comments"]:
        last = datetime.fromisoformat(state["comments"][-1]["at"]).replace(tzinfo=None)
        if now - last < timedelta(minutes=MIN_GAP_MINUTES):
            return f"the last comment was {int((now - last).total_seconds() // 60)} minutes ago (minimum gap {MIN_GAP_MINUTES})"
    return None


def next_post(entries: list, shortcode: "str | None" = None) -> "dict | None":
    """The next queued post with a keyword: Focus topics first, then the oldest."""
    queued = [e for e in entries if e["list"] == "comment_to_get" and e["status"] == "queued" and e.get("keyword")]
    if shortcode:
        return next((e for e in queued if e["shortcode"] == shortcode), None)
    queued.sort(key=lambda e: (not e.get("focus"), e.get("added_at", "")))
    return queued[0] if queued else None


def send(text: str) -> bool:
    from status_report import send_hermes

    sent, error = send_hermes(text)
    if not sent:  # Hermes sometimes fails once (seen 2026-11-10); the message matters, so try again
        time.sleep(20)
        sent, error = send_hermes(text)
    if not sent:
        logger.error(f"Could not send the Telegram message: {error}")
    return sent


def pause(reason: str) -> None:
    until = datetime.now() + timedelta(days=PAUSE_DAYS)
    PAUSED_FILE.write_text(json.dumps({"until": until.isoformat(timespec="seconds"), "reason": reason}, indent=1) + "\n")
    logger.error(f"Commenting paused until {until:%Y-%m-%d %H:%M}: {reason}")
    send(f"IG comments: paused for {PAUSE_DAYS} days.\nWhy: {reason}\nNothing else was posted. "
         f"To start again sooner: python comment_gated.py --resume")


# ---------------------------------------------------------------- the browser part


def human_pause(low: float, high: float) -> None:
    time.sleep(random.uniform(low, high))


def keep_shot(driver, name: str) -> "Path | None":
    try:
        SHOTS_DIR.mkdir(parents=True, exist_ok=True)
        path = SHOTS_DIR / f"{datetime.now():%Y-%m-%d_%H%M%S}_{name}.png"
        driver.save_screenshot(str(path))
        for old in sorted(SHOTS_DIR.glob("*.png"))[:-40]:
            old.unlink(missing_ok=True)
        return path
    except Exception:  # noqa: BLE001 - a screenshot must never break the run
        return None


def look(driver) -> dict:
    return driver.execute_script(LOOK_JS)


def check_safe(seen: dict) -> None:
    if seen["login"]:
        raise SafetyStop("Firefox is not logged into Instagram (login page)")
    if seen["challenge"]:
        raise SafetyStop(f"Instagram asked for a check ({seen['url']})")
    if seen["warning"]:
        raise SafetyStop(f"Instagram showed a warning: {seen['warning']}")


def open_post(driver, shortcode: str) -> dict:
    """Open the post page and wait until it shows the comment box, a stop sign, or the wait runs out."""
    driver.get(f"https://www.instagram.com/p/{shortcode}/")
    seen = {}
    deadline = time.monotonic() + 40
    while time.monotonic() < deadline:
        time.sleep(3)
        seen = look(driver)
        if seen["box"] or seen["login"] or seen["challenge"] or seen["warning"] or seen["gone"] or seen["comments_off"]:
            break
    return seen


def follow_and_comment(driver, entry: dict) -> dict:
    """Follow if needed, post the keyword. Returns {"followed": bool}. Raises SafetyStop or PostProblem."""
    from selenium.webdriver.common.keys import Keys

    keyword = entry["keyword"]
    seen = open_post(driver, entry["shortcode"])
    check_safe(seen)
    if seen["gone"]:
        raise PostProblem("the post is gone or private")
    if seen["comments_off"]:
        raise PostProblem("comments are turned off or limited on this post")
    if not seen["box"]:
        raise SafetyStop("the comment box did not show on the post page (Instagram may have changed the page)")
    human_pause(4, 9)  # look at the post first
    before = driver.execute_script(OUR_COMMENTS_JS, keyword, OWN_USERNAME)
    if before:
        raise AlreadyCommented(f"@{OWN_USERNAME} already commented '{keyword}' on this post")
    if driver.execute_script(OUR_COMMENTS_JS, keyword, MAIN_USERNAME):
        raise AlreadyCommented(f"@{MAIN_USERNAME} already commented '{keyword}' on this post")

    followed = False
    if seen["follow"] and not seen["following"]:
        if driver.execute_script(CLICK_FOLLOW_JS):
            human_pause(3, 6)
            after = look(driver)
            check_safe(after)
            followed = after["following"] or not after["follow"]
            if not followed:
                raise SafetyStop("the Follow button did not change after the click")
            logger.info(f"  Followed @{entry.get('author')}")
            human_pause(2, 5)

    box = driver.execute_script(FIND_BOX_JS)
    if box is None:
        raise SafetyStop("the comment box went away before typing")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", box)
    box.click()
    human_pause(1, 2)
    box = driver.execute_script(FIND_BOX_JS) or box  # Instagram swaps the box for a new one on focus
    for char in keyword:
        box.send_keys(char)
        time.sleep(random.uniform(0.08, 0.3))
    human_pause(1, 3)
    button = driver.execute_script(FIND_POST_JS)
    if button is not None:
        button.click()
    else:
        box.send_keys(Keys.ENTER)

    deadline = time.monotonic() + 25
    shows = False
    while time.monotonic() < deadline:
        time.sleep(2.5)
        after = look(driver)
        check_safe(after)
        if driver.execute_script(OUR_COMMENTS_JS, keyword, OWN_USERNAME) > before:
            shows = True
            break
    if not shows:
        raise SafetyStop(f"the comment '{keyword}' did not show up on the post after posting")
    return {"followed": followed}


def with_browser(work, name: str):
    """Run work(driver) in headless Firefox on a copy of the profile; always close it and keep a screenshot."""
    from export_chat_browser import open_firefox

    driver, workdir = open_firefox(str(FIREFOX_PROFILE))
    try:
        try:
            return work(driver)
        finally:
            shot = keep_shot(driver, name)
            if shot:
                logger.info(f"  Screenshot: {shot}")
    finally:
        driver.quit()
        shutil.rmtree(workdir, ignore_errors=True)


def pipeline_lock():
    """The pipeline's lock, so a comment never overlaps a download or chat export. None when it is taken.

    Inside a pipeline run (IG_PIPELINE=1) the pipeline already holds it.
    """
    if os.environ.get("IG_PIPELINE"):
        return True
    lock = PIPELINE_LOCK.open("a")
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        lock.close()
        return None
    return lock


# ---------------------------------------------------------------- one run


def set_entry(shortcode: str, change) -> None:
    with dead_ends.locked():
        entries = dead_ends.load()
        entry = dead_ends.find(entries, shortcode, "research")
        if entry:
            change(entry)
            entry["updated_at"] = dead_ends.now()
            dead_ends.save(entries)


def comment_once(shortcode: "str | None" = None, force: bool = False) -> str:
    """Maybe comment on one post. Returns a short line saying what happened."""
    state = load_state()
    reason = why_not_now(state)
    if reason and not (force and not paused_until() and not any(p.exists() for p in OTHER_STOPS)):
        return f"No comment this run: {reason}"
    entry = next_post(dead_ends.load(), shortcode)
    if not entry:
        return "No comment this run: nothing is queued" + (f" under {shortcode}" if shortcode else "")
    if not force and random.random() > RUN_CHANCE:
        return "No comment this run: skipped on purpose, so the times vary"
    lock = pipeline_lock()
    if lock is None:
        return "No comment this run: the pipeline is running"

    code, keyword, author = entry["shortcode"], entry["keyword"], entry.get("author") or "the creator"
    logger.info(f"Commenting '{keyword}' on {code} (@{author})")
    try:
        result = with_browser(lambda driver: follow_and_comment(driver, entry), code)
    except AlreadyCommented as exc:
        stamp = dead_ends.now()
        set_entry(code, lambda e: (e.update(status="commented_waiting", commented_at=stamp),
                                   e["history"].append({"at": stamp, "event": f"{exc}; nothing posted again"})))
        send(f"IG comments: {exc} (@{author}), so I did not post it again.\n{entry.get('title') or code}\n{entry['url']}\n\n"
             "Your part: on your phone, check the DM from this creator in the account that commented, and tap the "
             "button. Then paste what you got "
             "after \"Link:\" for this post in the vault note \"IG dead ends - comment to get it\".")
        return f"Nothing posted on {code}: {exc}. Telegram message sent"
    except PostProblem as exc:
        stamp = dead_ends.now()
        set_entry(code, lambda e: (e.update(status="needs_you"),
                                   e["history"].append({"at": stamp, "event": f"needs you: could not comment, {exc}"})))
        return f"Could not comment on {code}: {exc}. Moved to Needs you"
    except SafetyStop as exc:
        pause(f"{exc} (post {code})")
        return f"SAFETY STOP on {code}: {exc}"
    except Exception as exc:  # noqa: BLE001 - anything unexpected in the browser also stops commenting
        pause(f"unexpected error: {type(exc).__name__}: {str(exc)[:200]} (post {code})")
        return f"SAFETY STOP on {code}: {type(exc).__name__}: {str(exc)[:200]}"

    stamp = dead_ends.now()
    state["comments"].append({"at": stamp, "shortcode": code, "keyword": keyword, "author": author,
                              "followed": result["followed"]})
    save_state(state)
    follow_note = ", followed the account first" if result["followed"] else ""
    set_entry(code, lambda e: (e.update(status="commented_waiting", commented_at=stamp),
                               e["history"].append({"at": stamp, "event": f"commented '{keyword}'{follow_note}"})))
    send(f"IG comments: I commented \"{keyword}\" on @{author}'s post{follow_note}.\n"
         f"{entry.get('title') or code}\n{entry['url']}\n\n"
         f"Your part: open Instagram on your phone, switch to @{OWN_USERNAME}, open the DM from this creator "
         "and tap the button. "
         "Then paste what you got after \"Link:\" for this post in the vault note "
         "\"IG dead ends - comment to get it\".")
    return f"Commented '{keyword}' on {code} (@{author}){follow_note}. Telegram message sent"


def follow_ups(now: "datetime | None" = None) -> list:
    """Reminder, then needs_you, for posts that were commented on but have no link yet. No Instagram requests."""
    now = now or datetime.now()
    done = []
    remind = []
    with dead_ends.locked():
        entries = dead_ends.load()
        for entry in entries:
            if entry["list"] != "comment_to_get" or entry["status"] != "commented_waiting" or not entry.get("commented_at"):
                continue
            days = (now - datetime.fromisoformat(entry["commented_at"]).replace(tzinfo=None)).days
            stamp = dead_ends.now()
            if days >= GIVE_UP_DAYS:
                entry.update(status="needs_you", updated_at=stamp)
                entry["history"].append({"at": stamp, "event": f"needs you: no link {days} days after the comment"})
                done.append(f"{entry['shortcode']}: no link after {days} days, moved to Needs you")
            elif days >= REMIND_DAYS and not entry.get("reminded_at"):
                entry.update(reminded_at=stamp, updated_at=stamp)
                entry["history"].append({"at": stamp, "event": "Telegram reminder sent"})
                remind.append(entry)
                done.append(f"{entry['shortcode']}: reminder sent")
        if done:
            dead_ends.save(entries)
    if remind:
        lines = "\n".join(f"* @{e.get('author')}, keyword \"{e['keyword']}\": {e['url']}" for e in remind)
        send(f"IG comments: reminder. I commented on these {REMIND_DAYS} or more days ago and no link is saved yet. "
             f"Open the DM on your phone (account @{OWN_USERNAME}), tap the button, and paste the link in the vault list:\n{lines}")
    return done


def status_lines() -> list:
    state = load_state()
    entries = dead_ends.load()
    today = datetime.now().date().isoformat()
    done_today = sum(c["at"].startswith(today) for c in state["comments"])
    queued = [e for e in entries if e["list"] == "comment_to_get" and e["status"] == "queued" and e.get("keyword")]
    waiting = [e for e in entries if e["list"] == "comment_to_get" and e["status"] == "commented_waiting"]
    upcoming = next_post(entries)
    return [
        f"Comments today: {done_today} of {daily_limit(today)} | all time: {len(state['comments'])}",
        f"Right now: {why_not_now(state) or 'a comment may go out'}",
        f"Queued: {len(queued)} | Commented, waiting for you: {len(waiting)}",
        f"Next: {upcoming['shortcode']} '{upcoming['keyword']}' @{upcoming.get('author')}" if upcoming else "Next: nothing queued",
    ]


def probe(shortcode: str) -> int:
    """Open the post and print what the page shows. Clicks and types nothing."""
    lock = pipeline_lock()
    if lock is None:
        print("The pipeline is running; try again when it has finished")
        return 1
    seen = with_browser(lambda driver: open_post(driver, shortcode), f"probe_{shortcode}")
    for key, value in seen.items():
        print(f"{key:13} {value}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--status", action="store_true", help="Print the limits, the pause and the next post. No Instagram requests.")
    parser.add_argument("--probe", metavar="CODE", help="Open this post and print what the page shows. Clicks nothing.")
    parser.add_argument("--shortcode", metavar="CODE", help="Comment on this queued post instead of the next one.")
    parser.add_argument("--now", action="store_true",
                        help="Ignore the hours, the daily limit, the gap and the chance. A pause or a download stop still holds.")
    parser.add_argument("--resume", action="store_true", help="Lift the commenting pause.")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S",
                        handlers=[logging.StreamHandler(sys.stdout)])
    if not os.environ.get("IG_PIPELINE") and not args.status:
        file_log = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_log.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"))
        logger.addHandler(file_log)
    if args.resume:
        PAUSED_FILE.unlink(missing_ok=True)
        print("Commenting pause lifted")
        return 0
    if args.status:
        print("\n".join(status_lines()))
        return 0
    if args.probe:
        return probe(args.probe)
    logger.info("=== comment_gated.py")
    for line in follow_ups():
        logger.info(f"  {line}")
    outcome = comment_once(args.shortcode, force=args.now)
    logger.info(f"  {outcome}")
    return 2 if outcome.startswith("SAFETY STOP") else 0


if __name__ == "__main__":
    raise SystemExit(main())
