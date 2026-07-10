#!/usr/bin/env python3
"""Download Instagram media referenced by markdown notes and extract audio."""

import argparse
import random
import re
import subprocess
import sys
import time
from pathlib import Path


IG_ROOT = Path("/Users/bogle/Dev/test-stuff/instagram_saves/IG")
DEFAULT_NOTES_DIR = IG_ROOT / "Notes"
DEFAULT_MEDIA_DIR = IG_ROOT / "Media"
URL_PATTERN = re.compile(r"^- URL:\s+(?P<url>https?://\S+)\s*$", re.MULTILINE)
VIDEO_EXTENSIONS = (".mp4", ".mkv", ".webm", ".mov")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download Instagram media from markdown notes and extract audio."
    )
    parser.add_argument(
        "--notes-dir",
        type=Path,
        default=DEFAULT_NOTES_DIR,
        help=f"Directory containing markdown notes. Default: {DEFAULT_NOTES_DIR}",
    )
    parser.add_argument(
        "--media-dir",
        type=Path,
        default=DEFAULT_MEDIA_DIR,
        help=f"Directory for downloaded media. Default: {DEFAULT_MEDIA_DIR}",
    )
    parser.add_argument(
        "--firefox-profile",
        default=None,
        help="Optional Firefox profile name/path for yt-dlp --cookies-from-browser.",
    )
    parser.add_argument(
        "--firefox-container",
        default=None,
        help="Optional Firefox container name for yt-dlp --cookies-from-browser.",
    )
    parser.add_argument(
        "--min-sleep",
        type=float,
        default=5.0,
        help="Minimum sleep between download requests in seconds.",
    )
    parser.add_argument(
        "--max-sleep",
        type=float,
        default=12.0,
        help="Maximum sleep between download requests in seconds.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional maximum number of notes to process.",
    )
    return parser.parse_args()


def run_command(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, check=True)


def ensure_dependencies() -> None:
    version_flags = {
        "yt-dlp": "--version",
        "ffmpeg": "-version",
    }
    for tool, version_flag in version_flags.items():
        try:
            subprocess.run(
                [tool, version_flag],
                check=True,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError as exc:
            raise SystemExit(f"{tool} is not installed or not on PATH.") from exc


def update_ytdlp() -> None:
    try:
        run_command(["yt-dlp", "--update-to", "master"])
    except subprocess.CalledProcessError as exc:
        if exc.returncode != 100:
            raise
        print(
            "yt-dlp self-update is unavailable for this install; "
            "reinstalling master build with pip."
        )
        run_command(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--upgrade",
                "--force-reinstall",
                "git+https://github.com/yt-dlp/yt-dlp.git@master",
            ]
        )


def find_note_files(notes_dir: Path) -> list[Path]:
    return sorted(path for path in notes_dir.rglob("*.md") if path.is_file())


def extract_url(note_path: Path) -> str | None:
    content = note_path.read_text(encoding="utf-8")
    match = URL_PATTERN.search(content)
    if not match:
        return None
    return match.group("url")


def build_cookie_selector(profile: str | None, container: str | None) -> str:
    selector = "firefox"
    if profile:
        selector += f":{profile}"
    if container:
        selector += f"::{container}"
    return selector


def get_output_dir(note_path: Path, notes_dir: Path, media_dir: Path) -> Path:
    relative_parent = note_path.relative_to(notes_dir).parent
    target_dir = media_dir / relative_parent / note_path.stem
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir


def find_downloaded_video(output_dir: Path) -> Path | None:
    for ext in VIDEO_EXTENSIONS:
        candidate = output_dir / f"reel{ext}"
        if candidate.exists():
            return candidate
    return None


def download_video(url: str, output_dir: Path, cookie_selector: str) -> Path:
    output_template = output_dir / "reel.%(ext)s"
    cmd = [
        "yt-dlp",
        "--cookies-from-browser",
        cookie_selector,
        "--output",
        str(output_template),
        url,
    ]
    run_command(cmd)
    video_path = find_downloaded_video(output_dir)
    if video_path is None:
        raise RuntimeError(f"yt-dlp completed but no video file was found in {output_dir}")
    return video_path


def extract_audio(video_path: Path, audio_path: Path) -> None:
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(video_path),
        "-vn",
        "-ar",
        "16000",
        "-ac",
        "1",
        str(audio_path),
    ]
    run_command(cmd)


def process_note(
    note_path: Path,
    notes_dir: Path,
    media_dir: Path,
    cookie_selector: str,
) -> tuple[bool, str]:
    url = extract_url(note_path)
    if not url:
        return False, "missing URL"

    output_dir = get_output_dir(note_path, notes_dir, media_dir)
    audio_path = output_dir / "audio.mp3"
    if audio_path.exists():
        return False, "audio already exists"

    video_path = find_downloaded_video(output_dir)
    if video_path is None:
        video_path = download_video(url, output_dir, cookie_selector)

    extract_audio(video_path, audio_path)
    return True, f"saved to {output_dir}"


def main() -> int:
    args = parse_args()
    if args.min_sleep > args.max_sleep:
        raise SystemExit("--min-sleep must be less than or equal to --max-sleep.")
    if not args.notes_dir.exists():
        raise SystemExit(f"Notes directory does not exist: {args.notes_dir}")

    ensure_dependencies()
    update_ytdlp()

    cookie_selector = build_cookie_selector(args.firefox_profile, args.firefox_container)
    note_files = find_note_files(args.notes_dir)
    if args.limit is not None:
        note_files = note_files[:args.limit]

    downloaded_count = 0
    skipped_count = 0
    error_count = 0

    for index, note_path in enumerate(note_files, start=1):
        print(f"[{index}/{len(note_files)}] Processing {note_path}")
        try:
            downloaded, message = process_note(
                note_path=note_path,
                notes_dir=args.notes_dir,
                media_dir=args.media_dir,
                cookie_selector=cookie_selector,
            )
            print(f"  {message}")
            if downloaded:
                downloaded_count += 1
                sleep_for = random.uniform(args.min_sleep, args.max_sleep)
                print(f"  sleeping {sleep_for:.1f}s")
                time.sleep(sleep_for)
            else:
                skipped_count += 1
        except subprocess.CalledProcessError as exc:
            error_count += 1
            print(f"  command failed with exit code {exc.returncode}")
        except Exception as exc:  # noqa: BLE001
            error_count += 1
            print(f"  error: {exc}")

    print(
        f"Done. Downloaded: {downloaded_count} | Skipped: {skipped_count} | Errors: {error_count}"
    )
    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
