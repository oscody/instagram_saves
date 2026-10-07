#!/usr/bin/env python3
"""Download the media of the posts in an export file into one folder per post."""

import argparse
import json
import logging
import random
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests

from export_chat_links import (
    FIREFOX_PROFILE,
    HEADERS,
    OUTPUT_DIR,
    SENT_AT_FORMAT,
    api_get,
    load_firefox_cookies,
    media_to_link,
)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger("ig_download")

DEFAULT_JSON = OUTPUT_DIR / "iambogle.json"
IG_DIR = Path(__file__).resolve().parent.parent / "IG"
TITLE_MAX_CHARS = 50
SHORTCODE_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        type=Path,
        default=DEFAULT_JSON,
        help=f"Export file to read and update. Default: {DEFAULT_JSON}",
    )
    parser.add_argument(
        "--ig-dir",
        type=Path,
        default=IG_DIR,
        help=f"Folder that holds one subfolder per post. Default: {IG_DIR}",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Download at most N posts (the newest that still need it).",
    )
    parser.add_argument(
        "--retry-failed",
        action="store_true",
        help="Also try posts whose error field is set.",
    )
    parser.add_argument(
        "--shortcode",
        action="append",
        help="Only consider this post. Can be given more than once.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List the posts that would be downloaded, then stop.",
    )
    parser.add_argument(
        "--firefox-profile",
        default=str(FIREFOX_PROFILE),
        help=f"Firefox profile to read the Instagram login cookies from. Default: {FIREFOX_PROFILE}",
    )
    parser.add_argument("--min-sleep", type=float, default=5.0, help="Minimum pause between posts, in seconds.")
    parser.add_argument("--max-sleep", type=float, default=12.0, help="Maximum pause between posts, in seconds.")
    return parser.parse_args()


def make_title(caption: str) -> str:
    """First caption line without hashtags, mentions, emoji and symbols, cut to about 50 characters."""
    line = next((l for l in (caption or "").splitlines() if l.strip()), "")
    line = re.sub(r"[#@][\w.]+", " ", line)
    line = re.sub(r"[^\w\s]|_", "", line)
    words = line.split()
    title = ""
    for word in words:
        candidate = f"{title} {word}".strip()
        if len(candidate) > TITLE_MAX_CHARS:
            break
        title = candidate
    if not title and words:
        title = words[0][:TITLE_MAX_CHARS]
    return title


def post_dir(ig_dir: Path, record: dict) -> Path:
    """The post's folder, named by when it was shared so folders sort in date order.

    For example IG/2026-10-05_2332_DeArCx4K4x6 (24 hour time, local).
    """
    sent_at = datetime.strptime(record["sent_at"], SENT_AT_FORMAT)
    return ig_dir / f"{sent_at:%Y-%m-%d_%H%M}_{record['shortcode']}"


def base_name(record: dict) -> str:
    title = make_title(record.get("caption", ""))
    return f"{record['shortcode']} - {title}" if title else record["shortcode"]


def media_id(shortcode: str) -> int:
    number = 0
    for char in shortcode[:11]:
        number = number * 64 + SHORTCODE_ALPHABET.index(char)
    return number


def files_present(record: dict, folder: Path) -> bool:
    files = record.get("files") or []
    return bool(files) and all((folder / name).exists() for name in files)


def needs_download(record: dict, ig_dir: Path, retry_failed: bool) -> bool:
    if record.get("error") and not retry_failed:
        return False
    if not record.get("downloaded"):
        return True
    # Trust the folder: a post marked downloaded whose files are gone is downloaded again.
    return not files_present(record, post_dir(ig_dir, record))


def run(cmd: list) -> None:
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        lines = [l for l in (result.stderr or result.stdout).splitlines() if l.strip()]
        errors = [l for l in lines if "ERROR" in l] or lines
        raise RuntimeError(errors[-1].strip() if errors else f"{cmd[0]} exited with code {result.returncode}")


def download_video(record: dict, folder: Path, base: str, firefox_profile: str) -> list:
    """Reel or single video: yt-dlp for the mp4, ffmpeg for the mp3 that transcribe uses."""
    video = folder / f"{base}.mp4"
    audio = folder / f"{base}.mp3"
    run([
        sys.executable, "-m", "yt_dlp",
        "--cookies-from-browser", f"firefox:{firefox_profile}",
        "--remux-video", "mp4",
        "--no-playlist",
        "--quiet", "--no-warnings",
        "--force-overwrites",
        # Titles hold only letters, digits and spaces, so there is no "%" to escape.
        "--output", str(folder / f"{base}.%(ext)s"),
        record["url"],
    ])
    if not video.exists():
        raise RuntimeError("yt-dlp finished but wrote no mp4")
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-vn", "-ar", "16000", "-ac", "1", str(audio)])
    return [video.name, audio.name]


def best(versions: list) -> str:
    return max(versions, key=lambda v: v.get("width", 0) * v.get("height", 0))["url"]


def save_url(url: str, path: Path) -> None:
    resp = requests.get(url, headers=HEADERS, timeout=60, stream=True)
    if resp.status_code != 200:
        raise RuntimeError(f"HTTP {resp.status_code} fetching media file")
    tmp = path.with_name(path.name + ".part")
    with open(tmp, "wb") as fh:
        for chunk in resp.iter_content(1 << 16):
            fh.write(chunk)
    tmp.replace(path)


def download_images(media: dict, folder: Path, base: str) -> list:
    """Photo or carousel, straight from the media info. Links expire, so they are fetched now."""
    if media.get("media_type") == 8:
        slides = media.get("carousel_media") or []
        names = [f"{base}_{n}" for n in range(1, len(slides) + 1)]
    else:
        slides, names = [media], [base]
    files = []
    for slide, name in zip(slides, names):
        if slide.get("video_versions"):
            path = folder / f"{name}.mp4"
            save_url(best(slide["video_versions"]), path)
        else:
            path = folder / f"{name}.jpg"
            save_url(best(slide["image_versions2"]["candidates"]), path)
        files.append(path.name)
    return files


def download_post(record: dict, ig_dir: Path, cookies: dict, firefox_profile: str) -> None:
    folder = post_dir(ig_dir, record)
    folder.mkdir(parents=True, exist_ok=True)
    base = base_name(record)

    if record.get("type") == "Reel":
        files = download_video(record, folder, base, firefox_profile)
    else:
        # /p/ links can be a photo, a carousel or a video; the media info says which.
        info = api_get(cookies, f"/media/{media_id(record['shortcode'])}/info/")
        items = info.get("items") or []
        if not items:
            raise RuntimeError("Post not found (deleted or private)")
        record["type"] = media_to_link(items[0])["type"]
        if items[0].get("media_type") == 2:
            files = download_video(record, folder, base, firefox_profile)
        else:
            files = download_images(items[0], folder, base)

    record["files"] = files
    record["downloaded"] = True
    record["error"] = False


def short_error(exc: Exception) -> str:
    text = str(exc).strip()
    # api_get errors end with the response body; the status line is enough.
    return text.split(": ", 1)[0] if text.startswith("HTTP ") else text[:300]


def save(data: dict, path: Path) -> None:
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    tmp.replace(path)


def main() -> int:
    args = parse_args()
    if args.min_sleep > args.max_sleep:
        raise SystemExit("--min-sleep must be less than or equal to --max-sleep.")

    data = json.loads(args.json.read_text())
    records = sorted(
        data["links"],
        key=lambda r: datetime.strptime(r["sent_at"], SENT_AT_FORMAT),
        reverse=True,
    )
    if args.shortcode:
        records = [r for r in records if r["shortcode"] in args.shortcode]
    todo = [r for r in records if needs_download(r, args.ig_dir, args.retry_failed)]
    if args.limit is not None:
        todo = todo[:args.limit]
    logger.info(f"{len(todo)} posts to download")

    if args.dry_run:
        for record in todo:
            print(f"{record['sent_at']}  {record['type']:<8}  {base_name(record)}")
        return 0
    if not todo:
        return 0

    cookies = load_firefox_cookies(args.firefox_profile)
    logger.info("✓ Firefox cookies loaded")
    args.ig_dir.mkdir(parents=True, exist_ok=True)

    done = failed = 0
    for index, record in enumerate(todo, start=1):
        if index > 1:
            time.sleep(random.uniform(args.min_sleep, args.max_sleep))
        logger.info(f"[{index}/{len(todo)}] {record['type']} {record['shortcode']}")
        try:
            download_post(record, args.ig_dir, cookies, args.firefox_profile)
            done += 1
            logger.info(f"  ✓ {len(record['files'])} files in {post_dir(args.ig_dir, record)}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            record["downloaded"] = False
            record["error"] = short_error(exc)
            logger.warning(f"  ✗ {record['error']}")
        save(data, args.json)

    logger.info(f"Done. Downloaded: {done} | Failed: {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("Interrupted; posts finished so far are saved")
        sys.exit(130)
