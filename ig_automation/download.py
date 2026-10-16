#!/usr/bin/env python3
"""Download the media of the posts in an export file into one folder per post.

Paced so Instagram does not flag the account (it blocked it on 2026-10-08): at most --daily-cap posts in any
24 hours, 20 to 60 seconds between posts, none during --quiet-hours. When Instagram logs the session out it
writes output/LOGGED_OUT and stops; no download starts again until that file is deleted.
"""

import argparse
import json
import logging
import random
import re
import socket
import subprocess
import sys
import tempfile
import time
import wave
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import requests

from export_chat_links import (
    FIREFOX_PROFILE,
    HEADERS,
    IG_API_BASE,
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
LOGGED_OUT_FILE = OUTPUT_DIR / "LOGGED_OUT"
LOGGED_OUT_EXIT = 77  # tells run_pipeline.py to stop everything
ATTEMPTS_FILE = OUTPUT_DIR / "download_attempts.json"  # when each post was tried, for the daily cap
CAP_RETRY_FILE = OUTPUT_DIR / "download_cap_retry.json"
NETWORK_WAIT = 600  # longest wait for the network to come back, in seconds

# Errors that can mean Instagram sent the request to its login page or a challenge. A single broken post can
# also fail like this, so the session is checked before the run stops.
LOGIN_SIGNS = (
    "exceeded 30 redirects", "failed to parse json", "login required", "login_required", "checkpoint",
    "challenge", "rate-limit", "rate limit", "please wait a few minutes", "http error 401", "http error 403",
    "http error 429", "http 401", "http 403", "http 429",
)
NETWORK_SIGNS = (
    "failed to resolve", "nameresolutionerror", "temporary failure in name resolution", "max retries exceeded",
    "connection reset", "connection aborted", "network is unreachable", "timed out", "read timed out",
)
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
    parser.add_argument("--min-sleep", type=float, default=20.0, help="Minimum pause between posts, in seconds. Default: 20")
    parser.add_argument("--max-sleep", type=float, default=60.0, help="Maximum pause between posts, in seconds. Default: 60")
    parser.add_argument(
        "--daily-cap",
        type=int,
        default=75,
        help="Most posts tried in any 24 hours, counting every run. 0 turns the cap off. Default: 75",
    )
    parser.add_argument(
        "--quiet-hours",
        default="23-8",
        help="Local hours with no downloads, START-END. Empty turns it off. Default: 23-8 (11 pm to 8 am)",
    )
    return parser.parse_args()


def classify(error: str) -> str:
    """'login' (maybe logged out or blocked), 'network' (the Pi is offline) or 'post' (only this post failed)."""
    text = error.lower()
    if any(sign in text for sign in NETWORK_SIGNS):
        return "network"
    if any(sign in text for sign in LOGIN_SIGNS):
        return "login"
    return "post"


def session_ok(cookies: dict, record: dict) -> tuple[bool, str]:
    """One request without following redirects: is the Instagram session still logged in?"""
    path = f"/media/{media_id(record['shortcode'])}/info/"
    try:
        resp = requests.get(
            f"{IG_API_BASE}{path}", headers=HEADERS, cookies=cookies, timeout=20, allow_redirects=False
        )
    except requests.RequestException as exc:
        return True, f"session check failed to connect ({short_error(exc)})"
    if resp.is_redirect:
        return False, f"the API redirects to {resp.headers.get('Location')}"
    text = resp.text[:300].lower()
    if resp.status_code in (401, 403, 429) or any(s in text for s in ("login_required", "checkpoint", "challenge")):
        return False, f"HTTP {resp.status_code}: {resp.text[:200]}"
    return True, f"HTTP {resp.status_code}"


def mark_logged_out(reason: str) -> None:
    LOGGED_OUT_FILE.write_text(
        f"{datetime.now():%Y-%m-%d %H:%M} {reason}\n"
        "Log in to instagram.com in Firefox, close Firefox, run tests/download_test.py, then delete this file.\n"
    )


def network_up() -> bool:
    try:
        socket.gethostbyname("www.instagram.com")
        return True
    except OSError:
        return False


def wait_for_network(max_wait: int) -> bool:
    started = time.monotonic()
    while time.monotonic() - started < max_wait:
        if network_up():
            return True
        time.sleep(30)
    return network_up()


def in_quiet_hours(spec: str, now: datetime) -> bool:
    if not spec:
        return False
    start, end = (int(part) for part in spec.split("-"))
    hour = now.hour
    return start <= hour < end if start < end else hour >= start or hour < end


def recent_attempts() -> list:
    """Times (epoch seconds) of the posts tried in the last 24 hours."""
    try:
        times = json.loads(ATTEMPTS_FILE.read_text())
    except (OSError, ValueError):
        times = []
    cutoff = time.time() - 24 * 3600
    return [t for t in times if t > cutoff]


def note_attempt() -> None:
    times = recent_attempts() + [time.time()]
    tmp = ATTEMPTS_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(times))
    tmp.replace(ATTEMPTS_FILE)


def next_allowed_time(slot: datetime, quiet_hours: str) -> datetime:
    """Move a cap reopening time out of quiet hours while preserving its local timezone."""
    if not quiet_hours or not in_quiet_hours(quiet_hours, slot):
        return slot
    start, end = (int(part) for part in quiet_hours.split("-"))
    today_at_end = slot.replace(hour=end, minute=0, second=0, microsecond=0)
    if start > end and slot.hour >= start:
        return today_at_end + timedelta(days=1)
    return today_at_end


def save_cap_retry(slot: datetime, quiet_hours: str) -> datetime:
    retry_at = next_allowed_time(slot, quiet_hours)
    CAP_RETRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = CAP_RETRY_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps({"next_attempt_at": retry_at.isoformat(), "reason": "rolling 24 hour download cap"}, indent=2) + "\n")
    tmp.replace(CAP_RETRY_FILE)
    return retry_at


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
        # Look like Firefox, the browser the cookies come from, not like a Python script.
        "--impersonate", "firefox",
        # The share in the chat often has no caption; the info file has the real one.
        "--write-info-json",
        "--remux-video", "mp4",
        "--no-playlist",
        "--quiet", "--no-warnings",
        "--force-overwrites",
        # Titles hold only letters, digits and spaces, so there is no "%" to escape.
        "--output", str(folder / f"{base}.%(ext)s"),
        record["url"],
    ])
    info_file = folder / f"{base}.info.json"
    if info_file.exists():
        try:
            caption = json.loads(info_file.read_text()).get("description") or ""
        except ValueError:
            caption = ""
        info_file.unlink()
        if caption and not record.get("caption"):
            record["caption"] = caption
    if not video.exists():
        raise RuntimeError("yt-dlp finished but wrote no mp4")
    # Some Reels are silent (Instagram serves only a video stream), so there is nothing to transcribe.
    if not has_audio_stream(video):
        audio.unlink(missing_ok=True)
        return [video.name]
    run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-vn", "-ar", "16000", "-ac", "1", str(audio)])
    return [video.name, audio.name]


def has_audio_stream(video: Path) -> bool:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", str(video)],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe could not read {video.name}")
    return bool(result.stdout.strip())


def prepare_carousel_audio(record: dict, folder: Path) -> bool:
    """Extract local video-slide audio in slide order for the existing transcription stage.

    One combined MP3 keeps the post-level transcript contract. Source offsets are
    retained in the record; silent slides are omitted. No Instagram requests.
    Returns True only when new audio was prepared.
    """
    if record.get("type") != "Carousel":
        return False
    files = record.get("files") or []
    existing = next((name for name in files if name.endswith(".mp3")), None)
    if existing and (folder / existing).exists():
        return False
    videos = [folder / name for name in files if name.endswith(".mp4")]
    sources = [video for video in videos if has_audio_stream(video)]
    if not sources:
        return False
    audio = folder / f"{record['shortcode']}_carousel_audio.mp3"
    offsets = []
    with tempfile.TemporaryDirectory(prefix=".carousel-audio-", dir=folder) as temp:
        temp = Path(temp)
        combined = temp / "combined.wav"
        frames_written = 0
        with wave.open(str(combined), "wb") as output:
            output.setparams((1, 2, 16000, 0, "NONE", "not compressed"))
            for index, video in enumerate(sources):
                clip = temp / f"{index}.wav"
                run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video),
                     "-map", "0:a:0", "-vn", "-ar", "16000", "-ac", "1",
                     "-c:a", "pcm_s16le", str(clip)])
                start = frames_written / 16000
                with wave.open(str(clip), "rb") as source:
                    frames_written += source.getnframes()
                    while chunk := source.readframes(65536):
                        output.writeframesraw(chunk)
                offsets.append({"file": video.name, "start_seconds": start,
                                "end_seconds": frames_written / 16000})
            # wave writes the final frame count when the output is closed.
        prepared = temp / "combined.mp3"
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(combined),
             "-c:a", "libmp3lame", "-b:a", "64k", str(prepared)])
        prepared.replace(audio)
    record["files"] = [name for name in files if not name.endswith(".mp3")] + [audio.name]
    record["carousel_audio_sources"] = offsets
    record["transcribed"] = False
    record["described"] = False  # the old note remains until a refreshed one is ready
    record.pop("transcribed_by", None)
    return True


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
        link = media_to_link(items[0])
        record["type"] = link["type"]
        if link["caption"] and not record.get("caption"):
            record["caption"] = link["caption"]
        if items[0].get("media_type") == 2:
            files = download_video(record, folder, base, firefox_profile)
        else:
            files = download_images(items[0], folder, base)

    record["files"] = files
    prepare_carousel_audio(record, folder)
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
    if args.quiet_hours and not re.fullmatch(r"\d{1,2}-\d{1,2}", args.quiet_hours):
        raise SystemExit("--quiet-hours must look like 23-8, or be empty.")

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
    CAP_RETRY_FILE.unlink(missing_ok=True)
    if not todo:
        return 0
    if LOGGED_OUT_FILE.exists():
        logger.error(f"Not downloading: {LOGGED_OUT_FILE} exists. {LOGGED_OUT_FILE.read_text().strip()}")
        return LOGGED_OUT_EXIT

    cookies = load_firefox_cookies(args.firefox_profile)
    logger.info("✓ Firefox cookies loaded")
    args.ig_dir.mkdir(parents=True, exist_ok=True)

    done = failed = 0
    code = 0
    for index, record in enumerate(todo, start=1):
        if in_quiet_hours(args.quiet_hours, datetime.now()):
            logger.info(f"Quiet hours ({args.quiet_hours}), stopping; the rest waits for the next run")
            break
        if args.daily_cap and len(recent_attempts()) >= args.daily_cap:
            next_slot = datetime.fromtimestamp(min(recent_attempts()) + 24 * 3600).astimezone()
            retry_at = save_cap_retry(next_slot, args.quiet_hours)
            logger.info(f"Daily cap reached ({args.daily_cap} posts in 24 h), next slot at {next_slot:%a %H:%M}")
            if retry_at != next_slot:
                logger.info(f"Quiet hours apply, retry scheduled for {retry_at:%a %H:%M}")
            break
        if index > 1:
            time.sleep(random.uniform(args.min_sleep, args.max_sleep))
        logger.info(f"[{index}/{len(todo)}] {record['type']} {record['shortcode']}")
        note_attempt()
        try:
            download_post(record, args.ig_dir, cookies, args.firefox_profile)
            done += 1
            logger.info(f"  ✓ {len(record['files'])} files in {post_dir(args.ig_dir, record)}")
        except Exception as exc:  # noqa: BLE001
            error = short_error(exc)
            kind = classify(error)
            folder = post_dir(args.ig_dir, record)
            if folder.is_dir() and not any(folder.iterdir()):
                folder.rmdir()  # a failed download leaves no empty folder behind
            if kind == "network":
                # The post was never really tried, so it gets no error and the next run tries it again.
                logger.warning(f"  ✗ network: {error}")
                if not wait_for_network(NETWORK_WAIT):
                    logger.error(f"No network for {NETWORK_WAIT // 60} min, stopping")
                    code = 1
                    break
                continue
            if kind == "login":
                ok, detail = session_ok(cookies, record)
                if not ok:
                    logger.error(f"  ✗ {error}")
                    logger.error(f"Instagram logged the session out ({detail}). Stopping, wrote {LOGGED_OUT_FILE}")
                    mark_logged_out(detail)
                    code = LOGGED_OUT_EXIT
                    break
            failed += 1
            record["downloaded"] = False
            record["error"] = error
            logger.warning(f"  ✗ {error}")
        finally:
            save(data, args.json)

    logger.info(f"Done. Downloaded: {done} | Failed: {failed} | Tried in the last 24 h: {len(recent_attempts())}")
    return code or (0 if failed == 0 else 1)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("Interrupted; posts finished so far are saved")
        sys.exit(130)
