#!/usr/bin/env python3
"""Export the posts and reels shared in one Instagram DM thread to JSON."""

import argparse
import json
import logging
import random
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

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

# Firefox ESR on this Pi keeps profiles under ~/.config/mozilla, which yt-dlp does not search.
FIREFOX_PROFILE = Path.home() / ".config/mozilla/firefox/413ffz8o.default-esr"
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
DEFAULT_CHAT = "iambogle"  # Shemeir Bogle

IG_URL_PATTERN = re.compile(r"https?://(?:www\.)?instagram\.com/(?:p|reel|reels|tv)/[\w-]+/?\S*")


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
        help="Start over: ignore the saved file and re-scan the whole chat.",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Optional maximum number of message pages to fetch (for testing).",
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


def api_get(cookies: dict, path: str, params: Optional[dict] = None) -> dict:
    """GET an Instagram API endpoint, backing off on rate limits."""
    for attempt in range(5):
        resp = requests.get(
            f"{IG_API_BASE}{path}",
            headers=HEADERS,
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
        inbox = api_get(cookies, "/direct_v2/inbox/", params)["inbox"]
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
            if IG_URL_PATTERN.match(target):
                links.append({"url": target, "author": xma.get("header_title_text"), "caption": xma.get("title_text", "")})

    # Plain text and link messages can also carry pasted Instagram URLs.
    text = item.get("text") or (item.get("link") or {}).get("text") or ""
    for url in IG_URL_PATTERN.findall(text):
        links.append({"url": url, "message_text": text})

    return links


SENT_AT_FORMAT = "%b %d, %Y, %I:%M %p"  # local time, e.g. "Oct 05, 2026, 11:32 PM"


def build_record(item: dict, link: dict) -> dict:
    sent_at = datetime.fromtimestamp(int(item["timestamp"]) / 1_000_000).astimezone()
    return {
        "sent_at": sent_at.strftime(SENT_AT_FORMAT),
        "item_type": item.get("item_type"),
        **link,
    }


def load_existing(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {"links": [], "scan": {}}


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
        self.usernames = {str(u["pk"]): u["username"] for u in thread.get("users", [])}
        self.out_path = out_path
        # Keyed by URL, so a post shared more than once is listed once (its newest share).
        self.records = {r["url"]: r for r in existing.get("links", [])}
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
        return api_get(self.cookies, f"/direct_v2/threads/{self.thread_id}/", params)["thread"]

    def add_item(self, item: dict) -> None:
        links = extract_links(item)
        if not links and item.get("item_type") not in SKIP_TYPES:
            self.unhandled[item["item_type"]] = self.unhandled.get(item["item_type"], 0) + 1
        for link in links:
            if link["url"] not in self.records:
                self.records[link["url"]] = build_record(item, link)
                self.added += 1

    def save(self) -> None:
        links = sorted(
            self.records.values(),
            key=lambda r: datetime.strptime(r["sent_at"], SENT_AT_FORMAT),
            reverse=True,
        )
        output = {
            "thread_id": self.thread_id,
            "thread_title": self.thread.get("thread_title"),
            "participants": list(self.usernames.values()),
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

    def backfill(self, max_pages: Optional[int]) -> None:
        """Walk back through older history from the resume cursor (or the top on a first run)."""
        cursor = self.scan.get("resume_cursor")
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


def main() -> int:
    args = parse_args()

    cookies = load_firefox_cookies(args.firefox_profile)
    logger.info("✓ Firefox cookies loaded")

    thread = find_thread(cookies, args.chat)
    logger.info(f"✓ Found thread '{thread.get('thread_title')}' ({thread['thread_id']})")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    out_path = args.output_dir / f"{args.chat.lstrip('@')}.json"
    existing = {"links": [], "scan": {}} if args.full else load_existing(out_path)
    exporter = ChatExporter(cookies, thread, out_path, existing)

    try:
        if "newest_us" in exporter.scan:
            exporter.catch_up(args.max_pages)
        if not exporter.scan.get("history_complete"):
            logger.info("Older history not fully scanned yet, continuing backfill")
            exporter.backfill(args.max_pages)
    except PageLimitReached:
        logger.info(f"Stopping after {exporter.pages} pages (--max-pages); the next run continues from here")

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
