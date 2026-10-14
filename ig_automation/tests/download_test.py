#!/usr/bin/env python3
"""Test the download step on a few posts without touching the real data.

Read only: it never writes iambogle.json or the IG/ folders, so it is safe while the pipeline runs.
Posts are downloaded into output/download_test/ instead, and the folder is emptied at the start of each run.

It runs these checks in order and stops at the first one that fails, since later ones can't pass without it:
  1. DNS: www.instagram.com resolves (the Wi-Fi drop on Oct 8 failed here).
  2. Cookies: Firefox has an Instagram sessionid.
  3. Login: the API accepts the session (a redirect here means Instagram logged it out or wants a challenge).
  4. Downloads: one Reel, one Post and one Carousel, using download.py's own code, then checks the files.

By default it picks posts that downloaded fine before, so a failure points at the setup, not the post.
"""

import argparse
import copy
import json
import logging
import shutil
import socket
import subprocess
import sys
import time
from pathlib import Path

import requests

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

from download import DEFAULT_JSON, FIREFOX_PROFILE, base_name, download_post, media_id, post_dir, short_error
from export_chat_links import HEADERS, IG_API_BASE, load_firefox_cookies

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger("ig_download_test")

OUT_DIR = HERE / "output" / "download_test"
TYPES = ("Reel", "Post", "Carousel")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON, help=f"Export file to read. Default: {DEFAULT_JSON}")
    parser.add_argument(
        "--shortcode",
        action="append",
        help="Test this post instead of the default picks. Can be given more than once.",
    )
    parser.add_argument(
        "--failed",
        action="store_true",
        help="Pick posts that failed to download instead of ones that worked, to see if they work now.",
    )
    parser.add_argument("--per-type", type=int, default=1, help="Posts to test of each type. Default: 1")
    parser.add_argument(
        "--firefox-profile",
        default=str(FIREFOX_PROFILE),
        help=f"Firefox profile to read the Instagram login cookies from. Default: {FIREFOX_PROFILE}",
    )
    parser.add_argument("--sleep", type=float, default=5.0, help="Pause between posts, in seconds. Default: 5")
    return parser.parse_args()


def check_dns() -> None:
    address = socket.gethostbyname("www.instagram.com")
    logger.info(f"✓ DNS: www.instagram.com is {address}")


def check_login(cookies: dict, record: dict) -> None:
    """Fetch one post's media info without following redirects, so a logged out session shows where it goes."""
    path = f"/media/{media_id(record['shortcode'])}/info/"
    resp = requests.get(
        f"{IG_API_BASE}{path}", headers=HEADERS, cookies=cookies, timeout=20, allow_redirects=False
    )
    if resp.is_redirect:
        raise RuntimeError(
            f"API redirects to {resp.headers.get('Location')}. The Firefox session is logged out or "
            "Instagram wants a challenge: open instagram.com in Firefox and log in again."
        )
    if resp.status_code != 200:
        raise RuntimeError(f"HTTP {resp.status_code} on {path}: {resp.text[:200]}")
    try:
        resp.json()
    except ValueError:
        raise RuntimeError(f"API answered 200 but not with JSON: {resp.text[:200]!r}") from None
    logger.info("✓ Login: the API accepted the session")


def pick_records(links: list, args: argparse.Namespace) -> list:
    if args.shortcode:
        found = [r for r in links if r["shortcode"] in args.shortcode]
        missing = set(args.shortcode) - {r["shortcode"] for r in found}
        if missing:
            raise SystemExit(f"Not in {args.json}: {', '.join(sorted(missing))}")
        return found
    picks = []
    for post_type in TYPES:
        if args.failed:
            # LLM errors happen after the download, so they say nothing about downloading.
            pool = [r for r in links if r.get("type") == post_type and r.get("error")
                    and not r.get("downloaded") and not str(r["error"]).startswith("LLM")]
        else:
            pool = [r for r in links if r.get("type") == post_type and r.get("downloaded") and r.get("files")]
        picks += pool[:args.per_type]
    return picks


def media_streams(path: Path) -> set:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True,
    )
    return set(result.stdout.split())


def check_files(record: dict, folder: Path) -> list:
    """Problems with the downloaded files; an empty list means they look right."""
    problems = []
    files = record.get("files") or []
    if not files:
        return ["no files were written"]
    for name in files:
        path = folder / name
        if not path.exists() or path.stat().st_size == 0:
            problems.append(f"{name} is missing or empty")
        elif path.suffix == ".mp4" and "video" not in media_streams(path):
            problems.append(f"{name} has no video stream")
        elif path.suffix == ".mp3" and "audio" not in media_streams(path):
            problems.append(f"{name} has no audio stream")
        elif path.suffix == ".jpg" and path.read_bytes()[:3] != b"\xff\xd8\xff":
            problems.append(f"{name} is not a JPEG")
    if record.get("type") == "Reel" and not any(n.endswith(".mp3") for n in files):
        problems.append("Reel has no mp3 for transcribe")
    return problems


def test_download(record: dict, cookies: dict, firefox_profile: str) -> tuple:
    """Download a copy of the record into OUT_DIR. Returns (ok, message)."""
    test_record = copy.deepcopy(record)
    start = time.monotonic()
    try:
        download_post(test_record, OUT_DIR, cookies, firefox_profile)
    except Exception as exc:  # noqa: BLE001
        return False, short_error(exc)
    seconds = time.monotonic() - start
    folder = post_dir(OUT_DIR, test_record)
    problems = check_files(test_record, folder)
    if problems:
        return False, "; ".join(problems)
    size = sum((folder / n).stat().st_size for n in test_record["files"]) / 1e6
    return True, f"{len(test_record['files'])} files, {size:.1f} MB in {seconds:.0f}s"


def main() -> int:
    args = parse_args()
    links = json.loads(args.json.read_text())["links"]
    records = pick_records(links, args)
    if not records:
        raise SystemExit("No posts match, nothing to test.")

    try:
        check_dns()
    except OSError as exc:
        logger.error(f"✗ DNS: {exc}. The Pi is offline or the Wi-Fi dropped.")
        return 1
    try:
        cookies = load_firefox_cookies(args.firefox_profile)
        logger.info("✓ Cookies: Firefox has an Instagram sessionid")
    except Exception as exc:  # noqa: BLE001
        logger.error(f"✗ Cookies: {exc}")
        return 1
    try:
        check_login(cookies, records[0])
    except Exception as exc:  # noqa: BLE001
        logger.error(f"✗ Login: {exc}")
        return 1

    shutil.rmtree(OUT_DIR, ignore_errors=True)
    OUT_DIR.mkdir(parents=True)
    results = []
    for index, record in enumerate(records, start=1):
        if index > 1:
            time.sleep(args.sleep)
        logger.info(f"[{index}/{len(records)}] {record['type']} {base_name(record)}")
        ok, message = test_download(record, cookies, args.firefox_profile)
        (logger.info if ok else logger.warning)(f"  {'✓' if ok else '✗'} {message}")
        results.append((record, ok, message))

    passed = sum(ok for _, ok, _ in results)
    print(f"\n{passed} of {len(results)} downloads passed. Files are in {OUT_DIR}")
    for record, ok, message in results:
        print(f"  {'PASS' if ok else 'FAIL'}  {record['type']:<8}  {record['shortcode']}  {message}")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("Interrupted")
        sys.exit(130)
