#!/usr/bin/env python3
"""Sync shared reels/posts from an Instagram export DM thread to markdown notes."""

import argparse
import html as html_module
import json
import logging
import os
import re
from pathlib import Path
from typing import Optional

SCRIPT_DIR = Path(__file__).resolve().parent

# Configure logging
log_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

file_handler = logging.FileHandler(SCRIPT_DIR / "sync_export.log")
file_handler.setFormatter(log_formatter)

logger = logging.getLogger("ig_export_sync")
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

DEFAULT_MESSAGE_HTML = Path(
    "/Users/bogle/Dev/test-stuff/instagram_saves/"
    "instagram-djboglemusic-2026-07-10-Rk6cAOgC/your_instagram_activity/"
    "messages/inbox/shemeirbogle_448720033191192/message_1.html"
)
DEFAULT_OUTPUT_ROOT = Path("/Users/bogle/Dev/test-stuff/instagram_saves/IG_export")

STATE_FILE = SCRIPT_DIR / "state_export.json"

# One message block: sender <h2>, body, trailing timestamp div
MESSAGE_PATTERN = re.compile(
    r'<h2 class="[^"]*_a6-h[^"]*">(?P<sender>[^<]*)</h2>'
    r'(?P<body>.*?)'
    r'<div class="[^"]*_a6-o[^"]*">(?P<timestamp>[^<]*)</div>',
    re.DOTALL,
)

# Shared post/reel inside a message body: [caption div,] author div, link div
SHARE_PATTERN = re.compile(
    r'(?:<div>(?P<caption>[^<]*)</div>)?'
    r'<div>(?P<author>[^<]*)</div>'
    r'<div><a target="_blank" href="(?P<url>https://www\.instagram\.com/'
    r'(?P<kind>reel|p)/(?P<code>[^/?"]+)[^"]*)">',
    re.DOTALL,
)


def fix_mojibake(text: str) -> str:
    """Meta exports encode UTF-8 bytes as latin-1; undo that and decode entities."""
    try:
        text = text.encode("latin-1").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        pass
    return html_module.unescape(text)


def load_state() -> dict:
    """Load state (already synced media codes)."""
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


def build_note_title(caption: str, author: str, code: str) -> str:
    """Build a human-readable title from the caption when possible."""
    for line in caption.splitlines():
        stripped = line.strip()
        if stripped:
            return sanitize_filename(stripped)
    return sanitize_filename(f"{author}-{code}")


def extract_shares(html: str, include_posts: bool) -> list:
    """Extract shared reel/post info from the export HTML, in file order (newest first)."""
    shares = []
    for message in MESSAGE_PATTERN.finditer(html):
        share = SHARE_PATTERN.search(message.group("body"))
        if not share:
            continue

        kind = share.group("kind")
        if kind == "p" and not include_posts:
            continue

        code = share.group("code")
        author = fix_mojibake(share.group("author")).strip()
        caption = fix_mojibake(share.group("caption") or "").strip()
        post_type = "Reel" if kind == "reel" else "Post"
        url = f"https://instagram.com/{kind}/{code}/"

        # Media ID is the first segment of the share link's id / carousel_share_child_media_id param
        id_match = re.search(r"[?&](?:carousel_share_child_media_)?id=(\d+)", share.group("url"))
        media_id = id_match.group(1) if id_match else code

        shares.append({
            "media_id": media_id,
            "note_title": build_note_title(caption, author, code),
            "url": url,
            "type": post_type,
            "author": author,
            "caption": caption[:1900],
            "code": code,
            "sender": fix_mojibake(message.group("sender")).strip(),
            "shared_at": message.group("timestamp").strip(),
        })

    return shares


def build_note_path(notes_dir: Path, post_info: dict) -> Path:
    """Build a unique note path for a post."""
    filename = sanitize_filename(post_info["note_title"])
    path = notes_dir / f"{filename}.md"
    if path.exists():
        path = notes_dir / f"{filename}-{post_info['media_id']}.md"
    return path


def create_markdown_note(notes_dir: Path, post_info: dict) -> bool:
    """Create a markdown note for a shared post."""
    try:
        notes_dir.mkdir(parents=True, exist_ok=True)
        note_path = build_note_path(notes_dir, post_info)
        body = [
            f"# {post_info['note_title']}",
            "",
            f"- URL: {post_info['url']}",
            f"- Author: @{post_info['author']}",
            f"- Type: {post_info['type']}",
            f"- Media ID: {post_info['media_id']}",
            f"- Collection: DM Export",
            f"- Sender: {post_info['sender']}",
            f"- Shared At: {post_info['shared_at']}",
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync shared reels from an Instagram export DM thread to markdown notes."
    )
    parser.add_argument(
        "--message-html",
        type=Path,
        default=DEFAULT_MESSAGE_HTML,
        help=f"Path to the export message_N.html. Default: {DEFAULT_MESSAGE_HTML}",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help=f"Output root (Notes/ and Media/ created inside). Default: {DEFAULT_OUTPUT_ROOT}",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Only sync the first N new shares (for testing).",
    )
    parser.add_argument(
        "--reels-only",
        action="store_true",
        help="Only sync shared /reel/ links, skipping /p/ posts (photos/carousels).",
    )
    return parser.parse_args()


def main():
    """Main sync function."""
    args = parse_args()
    notes_dir = args.output_root / "Notes"
    media_dir = args.output_root / "Media"

    logger.info("=" * 60)
    logger.info("Instagram DM Export → Markdown Sync Started")
    logger.info("=" * 60)

    try:
        html = args.message_html.read_text(encoding="utf-8")
        logger.info(f"✓ Loaded {args.message_html.name} ({len(html):,} bytes)")

        state = load_state()
        synced_ids = set(state["synced_ids"])
        logger.info(f"Loaded state: {len(synced_ids)} already synced")

        shares = extract_shares(html, include_posts=not args.reels_only)
        logger.info(f"Found {len(shares)} shared {'reels' if args.reels_only else 'posts/reels'}")

        notes_dir.mkdir(parents=True, exist_ok=True)
        media_dir.mkdir(parents=True, exist_ok=True)

        new_count = 0
        skipped_count = 0
        error_count = 0

        for post_info in shares:
            if args.limit is not None and new_count >= args.limit:
                break

            if post_info["media_id"] in synced_ids:
                skipped_count += 1
                continue

            if create_markdown_note(notes_dir, post_info):
                synced_ids.add(post_info["media_id"])
                new_count += 1
            else:
                error_count += 1

        state["synced_ids"] = list(synced_ids)
        save_state(state)

        logger.info("=" * 60)
        logger.info(
            f"Sync complete: {new_count} new | {skipped_count} skipped | "
            f"{len(shares)} total | {error_count} errors"
        )
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Sync failed: {e}", exc_info=True)
        logger.error("=" * 60)


if __name__ == "__main__":
    main()
