#!/usr/bin/env python3
"""Sync Instagram saved posts to markdown notes."""

import argparse
import json
import logging
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests
from yt_dlp.cookies import extract_cookies_from_browser

# Configure logging
log_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

file_handler = logging.FileHandler("sync.log")
file_handler.setFormatter(log_formatter)

logger = logging.getLogger("ig_sync")
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Instagram API config
IG_API_BASE = "https://www.instagram.com/api/v1"
IG_APP_ID = "936619743392459"
IG_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

STATE_FILE = "state.json"
NOTES_DIR = Path("/Users/bogle/Dev/test-stuff/instagram_saves/IG/Notes")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sync Instagram saved posts to markdown notes.")
    parser.add_argument(
        "--notes-dir",
        type=Path,
        default=NOTES_DIR,
        help=f"Directory for markdown notes. Default: {NOTES_DIR}",
    )
    parser.add_argument(
        "--firefox-profile",
        default=None,
        help="Firefox profile name/path to read the Instagram login cookies from.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional maximum number of new notes to create.",
    )
    return parser.parse_args()


def load_firefox_cookies(profile: Optional[str]) -> dict:
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


def load_state() -> dict:
    """Load state (already synced media IDs)."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {"synced_ids": []}
    return {"synced_ids": []}


def save_state(state: dict) -> None:
    """Save state to file."""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def sanitize_filename(value: str) -> str:
    """Return a filesystem-safe filename stem."""
    cleaned = re.sub(r'[\\/*?:"<>|]', "", value)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    cleaned = cleaned.strip(".")
    return cleaned[:80] or "untitled"


def build_note_title(post: dict, author: str, code: str) -> str:
    """Build a human-readable title from the caption when possible."""
    caption_text = post.get("caption", {}).get("text", "") if post.get("caption") else ""
    for line in caption_text.splitlines():
        stripped = line.strip()
        if stripped:
            return sanitize_filename(stripped)
    return sanitize_filename(f"{author}-{code}")


def validate_instagram_session(cookies: dict) -> bool:
    """Validate Instagram session."""
    try:
        headers = {
            "User-Agent": IG_USER_AGENT,
            "X-IG-App-ID": IG_APP_ID,
        }
        resp = requests.get(
            f"{IG_API_BASE}/accounts/edit/web_form_data/",
            headers=headers,
            cookies=cookies,
            timeout=10
        )
        if resp.status_code == 200:
            logger.info("✓ Instagram session validated")
            return True
        else:
            logger.error(f"Instagram session validation failed: {resp.status_code}")
            return False
    except Exception as e:
        logger.error(f"Instagram session validation error: {e}")
        return False


def fetch_saved_posts(cookies: dict) -> list:
    """Fetch all saved posts with pagination."""
    posts = []
    headers = {
        "User-Agent": IG_USER_AGENT,
        "X-IG-App-ID": IG_APP_ID,
    }

    next_max_id = None
    page = 0

    while True:
        page += 1
        url = f"{IG_API_BASE}/feed/saved/posts/?count=50"
        if next_max_id:
            url += f"&max_id={next_max_id}"

        try:
            logger.info(f"Fetching saved posts page {page}...")
            resp = requests.get(
                url,
                headers=headers,
                cookies=cookies,
                timeout=10
            )
            resp.raise_for_status()
            data = resp.json()

            items = data.get("items", [])
            posts.extend(items)
            logger.debug(f"  Fetched {len(items)} items")

            if not data.get("more_available"):
                break

            next_max_id = data.get("next_max_id")
            time.sleep(1)  # Rate limit

        except Exception as e:
            logger.error(f"Error fetching saved posts: {e}")
            break

    logger.info(f"Total saved posts fetched: {len(posts)}")
    return posts


def fetch_collections(cookies: dict) -> dict:
    """Fetch collection names indexed by ID."""
    headers = {
        "User-Agent": IG_USER_AGENT,
        "X-IG-App-ID": IG_APP_ID,
    }

    collection_map = {}

    try:
        logger.info("Fetching collections...")
        resp = requests.get(
            f"{IG_API_BASE}/collections/list/",
            params={"collection_types": json.dumps(["ALL_MEDIA_AUTO_COLLECTION", "PRODUCT_AUTO_COLLECTION", "MEDIA"])},
            headers=headers,
            cookies=cookies,
            timeout=10
        )
        resp.raise_for_status()
        data = resp.json()

        for collection in data.get("items", []):
            collection_id = collection.get("id")
            collection_name = collection.get("name", "Unknown")
            collection_map[collection_id] = collection_name

        logger.info(f"Fetched {len(collection_map)} collections")
        return collection_map

    except Exception as e:
        logger.error(f"Error fetching collections: {e}")
        return {}


def extract_post_info(post: dict, collections: dict) -> Optional[dict]:
    """Extract relevant info from Instagram post object."""
    try:
        media_id = post.get("pk")
        if not media_id:
            return None

        media_type = post.get("media_type")
        code = post.get("code")
        caption_text = post.get("caption", {}).get("text", "") if post.get("caption") else ""

        # Build URL based on media type
        if media_type == 8:  # Carousel
            post_type = "Carousel"
            url = f"https://instagram.com/p/{code}/"
        elif media_type == 2:  # Video (Reel)
            post_type = "Reel"
            url = f"https://instagram.com/reel/{code}/"
        elif media_type == 1:  # Photo
            post_type = "Post"
            url = f"https://instagram.com/p/{code}/"
        else:
            post_type = "Other"
            url = f"https://instagram.com/p/{code}/"

        # Get author
        user = post.get("user", {})
        author = user.get("username", "unknown")

        note_title = build_note_title(post, author, code)

        # Get collection (check which collections contain this post)
        collection_name = None
        for coll_id, coll_name in collections.items():
            # Try to match; if this was in the collection it would be tagged
            # For now, mark as unset - would need full collection contents to properly map
            pass
        collection_name = collection_name or "Saved"

        # Truncate caption
        caption = caption_text[:1900] if caption_text else ""

        return {
            "media_id": str(media_id),
            "note_title": note_title,
            "url": url,
            "type": post_type,
            "author": author,
            "caption": caption,
            "collection": collection_name,
            "code": code,
        }

    except Exception as e:
        logger.error(f"Error extracting post info: {e}")
        return None


def build_note_path(post_info: dict) -> Path:
    """Build a unique note path for a post."""
    filename = sanitize_filename(post_info["note_title"])
    path = NOTES_DIR / f"{filename}.md"
    if path.exists():
        path = NOTES_DIR / f"{filename}-{post_info['media_id']}.md"
    return path


def create_markdown_note(post_info: dict) -> bool:
    """Create a markdown note for a saved post."""
    try:
        NOTES_DIR.mkdir(parents=True, exist_ok=True)
        note_path = build_note_path(post_info)
        saved_at = datetime.utcnow().isoformat() + "Z"
        body = [
            f"# {post_info['note_title']}",
            "",
            f"- URL: {post_info['url']}",
            f"- Author: @{post_info['author']}",
            f"- Type: {post_info['type']}",
            f"- Media ID: {post_info['media_id']}",
            f"- Collection: {post_info['collection']}",
            f"- Saved At: {saved_at}",
            "",
            "## Caption",
            "",
            post_info["caption"] or "_No caption_",
            "",
        ]
        note_path.write_text("\n".join(body), encoding="utf-8")
        logger.debug(f"  ✓ Created markdown note {note_path.name}")
        return True

    except Exception as e:
        logger.error(f"Error creating markdown note: {e}")
        return False


def main() -> int:
    """Main sync function."""
    global NOTES_DIR
    args = parse_args()
    NOTES_DIR = args.notes_dir

    logger.info("=" * 60)
    logger.info("Instagram → Markdown Sync Started")
    logger.info("=" * 60)

    try:
        # Load Instagram cookies from Firefox
        cookies = load_firefox_cookies(args.firefox_profile)
        logger.info("✓ Firefox cookies loaded")

        # Validate Instagram session
        if not validate_instagram_session(cookies):
            logger.error("Failed to validate Instagram session. Log into Instagram in Firefox again.")
            return 1

        # Load state
        state = load_state()
        synced_ids = set(state["synced_ids"])
        logger.info(f"Loaded state: {len(synced_ids)} already synced")

        # Fetch data
        saved_posts = fetch_saved_posts(cookies)
        collections = fetch_collections(cookies)

        # Process posts
        new_count = 0
        skipped_count = 0
        error_count = 0

        for post in saved_posts:
            if args.limit is not None and new_count >= args.limit:
                break

            post_data = post.get("media", post)
            media_id = post_data.get("pk")
            if not media_id:
                skipped_count += 1
                continue

            if str(media_id) in synced_ids:
                skipped_count += 1
                continue

            post_info = extract_post_info(post_data, collections)
            if not post_info:
                error_count += 1
                continue

            if create_markdown_note(post_info):
                synced_ids.add(str(media_id))
                new_count += 1
            else:
                error_count += 1

        # Save updated state
        state["synced_ids"] = list(synced_ids)
        save_state(state)

        # Summary
        logger.info("=" * 60)
        logger.info(
            f"Sync complete: {new_count} new | {skipped_count} skipped | "
            f"{len(saved_posts)} total | {error_count} errors"
        )
        logger.info("=" * 60)
        return 0 if error_count == 0 else 1

    except Exception as e:
        logger.error(f"Sync failed: {e}", exc_info=True)
        logger.error("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
