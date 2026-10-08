#!/usr/bin/env python3
"""Export the posts and reels shared in one Instagram DM thread to JSON.

DMs are read through the Instagram Android app API (i.instagram.com), using the Firefox login.
If that fails, new messages are read through headless Firefox instead (export_chat_browser.py);
--browser forces that route. Older history is only read through the app API.
"""

import argparse
import base64
import json
import logging
import random
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import unquote

import requests
from yt_dlp.cookies import extract_cookies_from_browser

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger("ig_chat_export")

IG_API_BASE = "https://www.instagram.com/api/v1"
IG_APP_ID = "936619743392459"
IG_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
HEADERS = {"User-Agent": IG_USER_AGENT, "X-IG-App-ID": IG_APP_ID}

# Since 2026-10-07 the website answers every /direct_v2/ call with a 404 "not logged in" page,
# while the Android app API still serves them. DM calls go there; other calls stay on the website.
DM_API_BASE = "https://i.instagram.com/api/v1"
DM_APP_ID = "567067343352427"
DM_USER_AGENT = "Instagram 361.0.0.35.82 Android (34/14; 420dpi; 1080x2340; samsung; SM-S918B; dm3q; qcom; en_US; 674675155)"

# Firefox ESR on this Pi keeps profiles under ~/.config/mozilla, which yt-dlp does not search.
FIREFOX_PROFILE = Path.home() / ".config/mozilla/firefox/413ffz8o.default-esr"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
DEFAULT_CHAT = "iambogle"  # Shemeir Bogle

IG_URL_PATTERN = re.compile(r"https?://(?:www\.)?instagram\.com/(?:p|reel|reels|tv)/[\w-]+/?\S*")
IG_PATH_PATTERN = re.compile(r"instagram\.com/(p|reel|reels|tv)/([\w-]+)")

# Pipeline status kept on every record. Stages set these; the exporter only adds them.
STATUS_DEFAULTS = {
    "downloaded": False,
    "transcribed": False,
    "described": False,
    "error": False,
    "files": [],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "chat",
        nargs="?",
        default=DEFAULT_CHAT,
        help=f"Username or thread title of the chat. Default: {DEFAULT_CHAT}",
    )
    parser.add_argument(
        "--firefox-profile",
        default=str(FIREFOX_PROFILE),
        help=f"Firefox profile path to read the Instagram login cookies from. Default: {FIREFOX_PROFILE}",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help=f"Directory for the JSON output. Default: {OUTPUT_DIR}",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Re-scan the whole chat from the newest message. Saved links and their status are kept.",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Optional maximum number of message pages to fetch (for testing).",
    )
    parser.add_argument(
        "--backfill-pages",
        type=int,
        default=None,
        help="Read all new messages, then at most N pages of older history (0 reads none). The next run "
             "continues the history from there. Used by run_pipeline.py.",
    )
    parser.add_argument(
        "--browser",
        action="store_true",
        help="Read new messages through headless Firefox (export_chat_browser.py) instead of the app API. "
             "This also happens on its own when the app API fails.",
    )
    return parser.parse_args()


def load_firefox_cookies(profile: str) -> dict:
    """Read Instagram cookies from the logged in Firefox profile."""
    jar = extract_cookies_from_browser("firefox", profile)
    cookies = {
        cookie.name: cookie.value
        for cookie in jar
        if cookie.domain.endswith("instagram.com")
    }
    if "sessionid" not in cookies:
        raise RuntimeError("No Instagram sessionid cookie in Firefox. Log into Instagram in Firefox first.")
    return cookies


def dm_headers(cookies: dict) -> dict:
    """App API headers: the app sends the session as a bearer token instead of cookies."""
    token = json.dumps(
        {"ds_user_id": cookies["ds_user_id"], "sessionid": unquote(cookies["sessionid"])}, separators=(",", ":")
    )
    return {
        "User-Agent": DM_USER_AGENT,
        "X-IG-App-ID": DM_APP_ID,
        "Authorization": "Bearer IGT:2:" + base64.b64encode(token.encode()).decode(),
        "X-IG-Capabilities": "3brTv10=",
        "X-IG-Connection-Type": "WIFI",
        "Accept-Language": "en-US",
    }


def dm_api_get(cookies: dict, path: str, params: Optional[dict] = None) -> dict:
    """GET a /direct_v2/ endpoint through the app API."""
    return api_get(cookies, path, params, base=DM_API_BASE, headers=dm_headers(cookies))


def api_get(
    cookies: dict, path: str, params: Optional[dict] = None, base: str = IG_API_BASE, headers: Optional[dict] = None
) -> dict:
    """GET an Instagram API endpoint, backing off on rate limits."""
    for attempt in range(5):
        resp = requests.get(
            f"{base}{path}",
            headers=headers or HEADERS,
            cookies=cookies,
            params=params,
            timeout=20,
        )
        if resp.status_code == 200:
            return resp.json()
        if resp.status_code in (429, 500, 502, 503):
            wait = 30 * (attempt + 1)
            logger.warning(f"HTTP {resp.status_code} on {path}, retrying in {wait}s")
            time.sleep(wait)
            continue
        raise RuntimeError(f"HTTP {resp.status_code} on {path}: {resp.text[:200]}")
    raise RuntimeError(f"Gave up on {path} after repeated rate limiting")


def find_thread(cookies: dict, chat: str) -> dict:
    """Page through the inbox until a thread matches the username or title."""
    wanted = chat.lower().lstrip("@")
    cursor = None
    while True:
        params = {"limit": 20}
        if cursor:
            params["cursor"] = cursor
        inbox = dm_api_get(cookies, "/direct_v2/inbox/", params)["inbox"]
        for thread in inbox.get("threads", []):
            usernames = [u.get("username", "").lower() for u in thread.get("users", [])]
            title = (thread.get("thread_title") or "").lower()
            if wanted in usernames or wanted == title:
                return thread
        if not inbox.get("has_older") or not inbox.get("oldest_cursor"):
            raise RuntimeError(f"No DM thread found for '{chat}'")
        cursor = inbox["oldest_cursor"]
        time.sleep(random.uniform(1.0, 2.5))


def media_to_link(media: dict) -> dict:
    """Build a link record from an Instagram media object, matching sync.py URLs."""
    code = media.get("code")
    media_type = media.get("media_type")
    if media_type == 2:
        post_type, url = "Reel", f"https://instagram.com/reel/{code}/"
    elif media_type == 8:
        post_type, url = "Carousel", f"https://instagram.com/p/{code}/"
    elif media_type == 1:
        post_type, url = "Post", f"https://instagram.com/p/{code}/"
    else:
        post_type, url = "Other", f"https://instagram.com/p/{code}/"
    caption = media.get("caption") or {}
    return {
        "url": url,
        "shortcode": code,
        "type": post_type,
        "author": (media.get("user") or {}).get("username"),
        "caption": caption.get("text", ""),
    }


def link_from_url(url: str) -> Optional[dict]:
    """Reduce a pasted or shared Instagram URL to the standard form, keyed by shortcode."""
    match = IG_PATH_PATTERN.search(url)
    if not match:
        return None
    kind, code = match.groups()
    if kind in ("reel", "reels"):
        return {"url": f"https://instagram.com/reel/{code}/", "shortcode": code, "type": "Reel"}
    # /p/ links can be a photo or a carousel; the download stage reads the real type.
    return {"url": f"https://instagram.com/p/{code}/", "shortcode": code, "type": "Post"}


def extract_links(item: dict) -> list:
    """Return the shared post/reel links in one message, if any."""
    item_type = item.get("item_type")
    links = []

    if item_type == "clip":
        media = (item.get("clip") or {}).get("clip")
        if media:
            links.append(media_to_link(media))
    elif item_type == "media_share":
        media = (item.get("direct_media_share") or {}).get("media") or item.get("media_share")
        if media:
            links.append(media_to_link(media))
    elif item_type == "felix_share":
        media = (item.get("felix_share") or {}).get("video")
        if media:
            links.append(media_to_link(media))
    elif item_type.startswith("xma"):
        for xma in item.get(item_type) or []:
            target = xma.get("target_url") or ""
            link = link_from_url(target) if IG_URL_PATTERN.match(target) else None
            if link:
                links.append({**link, "author": xma.get("header_title_text"), "caption": xma.get("title_text", "")})

    # Plain text and link messages can also carry pasted Instagram URLs.
    text = item.get("text") or (item.get("link") or {}).get("text") or ""
    for url in IG_URL_PATTERN.findall(text):
        link = link_from_url(url)
        if link:
            links.append({**link, "message_text": text})

    return links


SENT_AT_FORMAT = "%b %d, %Y, %I:%M %p"  # local time, e.g. "Oct 05, 2026, 11:32 PM"


def build_record(item: dict, link: dict) -> dict:
    sent_at = datetime.fromtimestamp(int(item["timestamp"]) / 1_000_000).astimezone()
    record = {
        "sent_at": sent_at.strftime(SENT_AT_FORMAT),
        "item_type": item.get("item_type"),
        **link,
    }
    add_missing_status(record)
    return record


def load_existing(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {"links": [], "scan": {}}


def add_missing_status(record: dict) -> bool:
    """Give an older record the status fields it lacks. Existing values are never changed."""
    missing = [key for key in STATUS_DEFAULTS if key not in record]
    for key in missing:
        value = STATUS_DEFAULTS[key]
        record[key] = list(value) if isinstance(value, list) else value
    return bool(missing)


class PageLimitReached(Exception):
    """Raised when --max-pages stops a run early."""


SKIP_TYPES = ("text", "link", "action_log", "like", "reel_share", "placeholder")


class ChatExporter:
    """Scans a DM thread page by page, adding new links and saving after every page.

    The "scan" block in the output file records what has been covered:
      newest_us        newest message scanned
      oldest_us        oldest message scanned (everything between the two is covered)
      resume_cursor    where to continue the backfill of older history
      history_complete True once the scan has reached the start of the chat
    """

    def __init__(self, cookies: dict, thread: dict, out_path: Path, existing: dict):
        self.cookies = cookies
        self.thread = thread
        self.thread_id = thread["thread_id"]
        # The chat's id in Instagram's new DM system, which the browser fallback reads.
        self.thread_v2_id = thread.get("thread_v2_id") or existing.get("thread_v2_id")
        self.participants = [u["username"] for u in thread.get("users", [])] or existing.get("participants", [])
        self.out_path = out_path
        # Keyed by shortcode, so a post shared more than once, or linked as both /p/ and
        # /reel/, is listed once (its newest share).
        self.records = {}
        for record in existing.get("links", []):
            key = record.get("shortcode") or (link_from_url(record["url"]) or {}).get("shortcode") or record["url"]
            self.records.setdefault(key, record)
        self.upgraded = sum(add_missing_status(r) for r in self.records.values())
        self.scan = existing.get("scan", {})
        self.added = 0
        self.pages = 0
        self.unhandled = {}

    def fetch_page(self, cursor: Optional[str]) -> dict:
        if self.pages:
            time.sleep(random.uniform(1.5, 3.5))
        params = {"limit": 50}
        if cursor:
            params["cursor"] = cursor
        self.pages += 1
        return dm_api_get(self.cookies, f"/direct_v2/threads/{self.thread_id}/", params)["thread"]

    def add_item(self, item: dict) -> None:
        links = extract_links(item)
        if not links and item.get("item_type") not in SKIP_TYPES:
            self.unhandled[item["item_type"]] = self.unhandled.get(item["item_type"], 0) + 1
        for link in links:
            if link["shortcode"] not in self.records:
                self.records[link["shortcode"]] = build_record(item, link)
                self.added += 1

    def save(self) -> None:
        links = sorted(
            self.records.values(),
            key=lambda r: datetime.strptime(r["sent_at"], SENT_AT_FORMAT),
            reverse=True,
        )
        output = {
            "thread_id": self.thread_id,
            "thread_v2_id": self.thread_v2_id,
            "thread_title": self.thread.get("thread_title"),
            "participants": self.participants,
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "scan": self.scan,
            "link_count": len(links),
            "links": links,
        }
        tmp = self.out_path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(output, indent=2, ensure_ascii=False))
        tmp.replace(self.out_path)

    def catch_up(self, max_pages: Optional[int]) -> None:
        """Fetch messages newer than the last scan, stopping at already-scanned ones."""
        known_newest = self.scan["newest_us"]
        cursor, newest = None, known_newest
        while True:
            data = self.fetch_page(cursor)
            reached_known = False
            for item in data.get("items", []):
                ts = int(item["timestamp"])
                if ts <= known_newest:
                    reached_known = True
                    break
                newest = max(newest, ts)
                self.add_item(item)
            logger.info(f"  new messages, page {self.pages}: {self.added} new links")
            if reached_known or not data.get("has_older") or not data.get("oldest_cursor"):
                # The covered range now runs unbroken from the newest message down.
                self.scan["newest_us"] = newest
                self.save()
                return
            if max_pages and self.pages >= max_pages:
                # Gap between this page and the known range; keep links but not the marker.
                self.save()
                raise PageLimitReached
            cursor = data["oldest_cursor"]

    def browser_catch_up(self, profile: str) -> None:
        """catch_up through headless Firefox, for when the app API fails. Reads new messages only."""
        from export_chat_browser import read_chat

        if not self.thread_v2_id:
            raise RuntimeError("No thread_v2_id in the export file yet; the browser fallback needs one app API run first")
        known_newest = self.scan["newest_us"]
        items, reached_known = read_chat(profile, self.thread.get("thread_title"), self.thread_v2_id, known_newest)
        newest = known_newest
        for item in items:
            if int(item["timestamp"]) > known_newest:
                newest = max(newest, int(item["timestamp"]))
                self.add_item(item)
        if reached_known:
            self.scan["newest_us"] = newest
        else:
            # Same as a page limit in catch_up: keep the links, leave the marker so the gap is read again.
            logger.warning("Browser did not scroll back to the last scanned message; the next run reads the gap again")
        self.save()
        logger.info(f"  browser: {len(items)} shared posts read, {self.added} new links")

    def backfill(self, max_pages: Optional[int], backfill_pages: Optional[int] = None) -> None:
        """Walk back through older history from the resume cursor (or the top on a first run)."""
        cursor = self.scan.get("resume_cursor")
        start_page = self.pages
        while True:
            data = self.fetch_page(cursor)
            for item in data.get("items", []):
                ts = int(item["timestamp"])
                self.scan.setdefault("newest_us", ts)
                self.scan["oldest_us"] = min(self.scan.get("oldest_us", ts), ts)
                self.add_item(item)
            if not data.get("has_older") or not data.get("oldest_cursor"):
                self.scan["history_complete"] = True
                self.scan.pop("resume_cursor", None)
                self.save()
                logger.info(f"  history, page {self.pages}: {self.added} new links")
                logger.info("✓ Reached the start of the chat")
                return
            cursor = self.scan["resume_cursor"] = data["oldest_cursor"]
            self.save()
            logger.info(f"  history, page {self.pages}: {self.added} new links")
            if max_pages and self.pages >= max_pages:
                raise PageLimitReached
            if backfill_pages and self.pages - start_page >= backfill_pages:
                logger.info(f"Read {backfill_pages} pages of older history (--backfill-pages); the next run continues from here")
                return


def load_for_run(out_path: Path, full: bool) -> dict:
    existing = load_existing(out_path)
    if full:
        # Forget how far the chat was read, but keep the links: they hold pipeline status.
        existing["scan"] = {}
    return existing


def export_with_api(args: argparse.Namespace, cookies: dict, out_path: Path) -> ChatExporter:
    thread = find_thread(cookies, args.chat)
    logger.info(f"✓ Found thread '{thread.get('thread_title')}' ({thread['thread_id']})")
    exporter = ChatExporter(cookies, thread, out_path, load_for_run(out_path, args.full))
    if exporter.upgraded:
        logger.info(f"Added status fields to {exporter.upgraded} saved links")

    try:
        if "newest_us" in exporter.scan:
            exporter.catch_up(args.max_pages)
        if not exporter.scan.get("history_complete") and args.backfill_pages != 0:
            logger.info("Older history not fully scanned yet, continuing backfill")
            exporter.backfill(args.max_pages, args.backfill_pages)
    except PageLimitReached:
        logger.info(f"Stopping after {exporter.pages} pages (--max-pages); the next run continues from here")
    return exporter


def export_with_browser(args: argparse.Namespace, cookies: dict, out_path: Path) -> ChatExporter:
    existing = load_for_run(out_path, args.full)
    if "newest_us" not in existing.get("scan", {}):
        raise RuntimeError("The browser fallback only reads new messages; it needs an earlier export to start from")
    thread = {"thread_id": existing.get("thread_id"), "thread_title": existing.get("thread_title")}
    exporter = ChatExporter(cookies, thread, out_path, existing)
    exporter.browser_catch_up(args.firefox_profile)
    logger.info("Older history is not read in browser mode; the app API backfill continues it")
    return exporter


def main() -> int:
    args = parse_args()

    cookies = load_firefox_cookies(args.firefox_profile)
    logger.info("✓ Firefox cookies loaded")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_path = args.output_dir / f"{args.chat.lstrip('@')}.json"

    exporter = None
    if not args.browser:
        try:
            exporter = export_with_api(args, cookies, out_path)
        except (RuntimeError, requests.RequestException, KeyError) as e:
            reason = (str(e).splitlines() or [""])[0]
            logger.warning(f"App API export failed ({reason}); falling back to reading the chat in Firefox")
    if exporter is None:
        exporter = export_with_browser(args, cookies, out_path)

    if exporter.unhandled:
        logger.info(f"Message types with no links extracted: {exporter.unhandled}")
    logger.info(f"✓ {exporter.added} new links, {len(exporter.records)} total in {out_path}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("Interrupted; progress up to the last finished page is saved")
        sys.exit(130)
    except Exception as e:
        logger.error(str(e))
        sys.exit(1)
