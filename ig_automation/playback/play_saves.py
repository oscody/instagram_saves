#!/usr/bin/env python3
"""Play the downloaded Instagram saves back to back on the Pi's screen, like a feed.

Reels play through, photos and carousel slides show for a few seconds each. The mpv script
saves_log.lua (next to this file) handles the keys and logs every like, skip and full watch
to output/watch_log.jsonl. This script builds the playlist from that log and iambogle.json.

Read only: it never writes iambogle.json (the pipeline owns it) and never talks to Instagram.

Examples:
  play_saves.py                         unseen posts first, newest first
  play_saves.py --topic ai --type reel  only AI reels
  play_saves.py --order liked-first     authors I liked come first
  play_saves.py --dry-run --limit 20    print the list instead of playing it
  play_saves.py --report                likes, skips and finishes per author and post type
"""

import argparse
import json
import os
import random
import re
import subprocess
import sys
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # download.py lives in ig_automation/
from download import DEFAULT_JSON, IG_DIR, OUTPUT_DIR, post_dir
from export_chat_links import SENT_AT_FORMAT

HERE = Path(__file__).resolve().parent
LUA_SCRIPT = HERE / "saves_log.lua"
WATCH_LOG = OUTPUT_DIR / "watch_log.jsonl"
PLAYLIST = OUTPUT_DIR / "playlist.m3u"
PLAYLIST_INDEX = OUTPUT_DIR / "playlist_index.json"
DURATIONS = OUTPUT_DIR / "video_durations.json"  # cache, so ffprobe runs once per video

IMAGE_SECONDS = 6
MEDIA_SUFFIXES = {".mp4", ".jpg", ".jpeg", ".png", ".webp"}
SKIPS_TO_HIDE = 2  # posts skipped this many times drop out unless --include-skipped
TYPES = {"reel": "Reel", "carousel": "Carousel", "post": "Post"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Play the Instagram saves on the Pi's screen with mpv.")
    parser.add_argument(
        "--order",
        choices=["newest", "oldest", "random", "liked-first", "unseen-first"],
        default="unseen-first",
        help="Play order. Default: unseen-first (unseen posts first, newest first within each group).",
    )
    parser.add_argument("--topic", help='Only posts whose title, summary or caption mention this, e.g. "ai".')
    parser.add_argument("--type", choices=sorted(TYPES), help="Only this post type.")
    parser.add_argument("--author", help="Only posts by this author.")
    parser.add_argument("--limit", type=int, help="Play at most this many posts.")
    parser.add_argument(
        "--include-skipped",
        action="store_true",
        help=f"Also play posts skipped {SKIPS_TO_HIDE} or more times.",
    )
    parser.add_argument("--image-seconds", type=float, default=IMAGE_SECONDS, help="How long photos and slides stay up.")
    parser.add_argument("--dry-run", action="store_true", help="Print the playlist and exit without playing.")
    parser.add_argument("--report", action="store_true", help="Print likes, skips and finishes, then exit.")
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON, help=f"Posts file (read only). Default: {DEFAULT_JSON}")
    parser.add_argument("--ig-dir", type=Path, default=IG_DIR, help=f"Folder with one subfolder per post. Default: {IG_DIR}")
    return parser.parse_args()


def load_posts(json_path: Path, ig_dir: Path) -> list[dict]:
    """Downloaded posts whose media is on disk, each with the full paths of its media in play order."""
    links = json.loads(json_path.read_text())["links"]
    posts = []
    for record in links:
        if not record.get("downloaded") or not record.get("files"):
            continue
        folder = post_dir(ig_dir, record)
        # The .mp3 and frame grabs are pipeline outputs, not part of the post.
        media = [folder / name for name in record["files"] if Path(name).suffix.lower() in MEDIA_SUFFIXES and "_frame" not in name]
        if not media or not all(path.exists() for path in media):
            continue
        posts.append({**record, "media": media, "sent": datetime.strptime(record["sent_at"], SENT_AT_FORMAT)})
    return posts


def load_watch_log() -> dict[str, dict]:
    """Per shortcode: how often it was skipped, finished or watched in part, and whether it was liked."""
    history: dict[str, dict] = defaultdict(lambda: Counter())
    if not WATCH_LOG.exists():
        return history
    for line in WATCH_LOG.read_text().splitlines():
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        stats = history[entry["shortcode"]]
        stats[entry["event"]] += 1
        if entry.get("liked"):
            stats["liked"] = 1
    return history


def seen(stats: Counter) -> bool:
    # A quit in the middle is not a verdict, so the post still counts as unseen and comes back first.
    return any(stats[event] for event in ("finished", "partial", "skip", "like"))


def video_durations(paths: list[Path]) -> dict[str, float]:
    """Length of each video in seconds, from the cache or ffprobe."""
    cache = json.loads(DURATIONS.read_text()) if DURATIONS.exists() else {}
    missing = [str(p) for p in paths if p.suffix == ".mp4" and str(p) not in cache]

    def probe(path: str) -> tuple[str, float]:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
            capture_output=True,
            text=True,
        )
        try:
            return path, float(result.stdout.strip())
        except ValueError:
            return path, 0.0

    if missing:
        print(f"Reading the length of {len(missing)} videos (once, then cached)...", file=sys.stderr)
        with ThreadPoolExecutor(max_workers=4) as pool:
            cache.update(pool.map(probe, missing))
        DURATIONS.write_text(json.dumps(cache, indent=1))
    return cache


def author_scores(posts: list[dict], history: dict[str, Counter]) -> Counter:
    """Likes count double and skips count against, so authors I like float up."""
    scores: Counter = Counter()
    for post in posts:
        stats = history.get(post["shortcode"])
        if stats:
            scores[post["author"]] += 2 * stats["liked"] + stats["finished"] - stats["skip"]
    return scores


def select(posts: list[dict], history: dict[str, Counter], args: argparse.Namespace) -> list[dict]:
    chosen = []
    for post in posts:
        stats = history.get(post["shortcode"], Counter())
        if args.type and post["type"] != TYPES[args.type]:
            continue
        if args.author and post.get("author", "").lower() != args.author.lower().lstrip("@"):
            continue
        if args.topic:
            # Whole words, so "ai" does not match "Jamaica".
            text = " ".join(post.get(key) or "" for key in ("ai_title", "summary", "caption"))
            if not re.search(rf"\b{re.escape(args.topic)}\b", text, re.IGNORECASE):
                continue
        if not args.include_skipped and stats["skip"] >= SKIPS_TO_HIDE:
            continue
        chosen.append(post)

    newest_first = sorted(chosen, key=lambda p: p["sent"], reverse=True)
    if args.order == "newest":
        ordered = newest_first
    elif args.order == "oldest":
        ordered = newest_first[::-1]
    elif args.order == "random":
        ordered = random.sample(chosen, len(chosen))
    elif args.order == "liked-first":
        scores = author_scores(posts, history)
        ordered = sorted(newest_first, key=lambda p: -scores[p["author"]])
    else:  # unseen-first
        ordered = sorted(newest_first, key=lambda p: seen(history.get(p["shortcode"], Counter())))
    return ordered[: args.limit] if args.limit else ordered


def write_playlist(posts: list[dict], durations: dict[str, float], image_seconds: float) -> None:
    """The .m3u lists every file; the index tells saves_log.lua which files belong to which post."""
    lines, index = ["#EXTM3U"], []
    for post in posts:
        index.append(
            {
                "shortcode": post["shortcode"],
                "first": len(lines) - 1,  # 0 based playlist position of the post's first file
                "count": len(post["media"]),
                "video_s": round(sum(durations.get(str(p), 0.0) for p in post["media"] if p.suffix == ".mp4"), 1),
                "images": sum(1 for p in post["media"] if p.suffix != ".mp4"),
                "type": post["type"],
                "author": post.get("author", ""),
                "title": post.get("ai_title") or post.get("caption", "")[:80],
                "summary": post.get("summary", ""),
                "url": post["url"],
            }
        )
        lines.extend(str(path) for path in post["media"])
    PLAYLIST.write_text("\n".join(lines) + "\n")
    PLAYLIST_INDEX.write_text(json.dumps({"image_seconds": image_seconds, "posts": index}, indent=1))


def print_report(posts: list[dict], history: dict[str, Counter]) -> None:
    by_code = {post["shortcode"]: post for post in posts}
    per_author: dict[str, Counter] = defaultdict(Counter)
    per_type: dict[str, Counter] = defaultdict(Counter)
    for code, stats in history.items():
        post = by_code.get(code)
        if not post:
            continue
        for key in ("liked", "finished", "partial", "skip"):
            per_author[post["author"]][key] += stats[key]
            per_type[post["type"]][key] += stats[key]

    def table(title: str, rows: dict[str, Counter]) -> None:
        print(f"\n{title}")
        print(f"  {'':32} {'liked':>6} {'done':>6} {'part':>6} {'skip':>6}")
        for name, c in sorted(rows.items(), key=lambda kv: (-kv[1]["liked"], -kv[1]["finished"], kv[1]["skip"])):
            print(f"  {name[:32]:32} {c['liked']:6} {c['finished']:6} {c['partial']:6} {c['skip']:6}")

    watched = sum(1 for stats in history.values() if seen(stats))
    print(f"Watched {watched} of {len(posts)} downloaded posts.")
    table("Per post type", per_type)
    table("Per author", per_author)

    always_skip = [a for a, c in per_author.items() if c["skip"] >= 2 and not c["liked"] and not c["finished"]]
    always_like = [a for a, c in per_author.items() if c["liked"] >= 2 and not c["skip"]]
    print(f"\nAuthors I always skip: {', '.join(sorted(always_skip)) or '-'}")
    print(f"Authors I always like: {', '.join(sorted(always_like)) or '-'}")
    undescribed = [code for code, stats in history.items() if stats["liked"] and code in by_code and not by_code[code].get("described")]
    print(f"Liked but not described yet: {', '.join(undescribed) or '-'}")


def play(image_seconds: float) -> int:
    env = dict(os.environ)
    # Started over SSH: open the video on the Pi's own screen.
    env.setdefault("WAYLAND_DISPLAY", "wayland-0")
    env.setdefault("XDG_RUNTIME_DIR", f"/run/user/{os.getuid()}")
    command = [
        "mpv",
        "--fs",
        "--force-window=immediate",
        "--loop-playlist=no",
        "--keep-open=no",
        f"--image-display-duration={image_seconds}",
        "--hwdec=no",  # the Pi 5 has no hardware decoder for VP9 or H.264
        "--save-position-on-quit",
        f"--script={LUA_SCRIPT}",
        f"--script-opts=saves_log-index={PLAYLIST_INDEX},saves_log-log={WATCH_LOG}",
        f"--playlist={PLAYLIST}",
    ]
    return subprocess.call(command, env=env)


def main() -> int:
    args = parse_args()
    posts = load_posts(args.json, args.ig_dir)
    history = load_watch_log()

    if args.report:
        print_report(posts, history)
        return 0

    chosen = select(posts, history, args)
    if not chosen:
        print("No posts match.", file=sys.stderr)
        return 1

    if args.dry_run:
        for post in chosen:
            stats = history.get(post["shortcode"], Counter())
            mark = "♥" if stats["liked"] else ("·" if seen(stats) else " ")
            print(f"{mark} {post['sent']:%Y-%m-%d} {post['type']:8} @{post.get('author', ''):24} {post.get('ai_title') or ''}")
        print(f"\n{len(chosen)} posts", file=sys.stderr)
        return 0

    durations = video_durations([path for post in chosen for path in post["media"]])
    write_playlist(chosen, durations, args.image_seconds)
    print(f"Playing {len(chosen)} posts. Keys: l like, n/→ next, p/← previous, i info, o link, +/- photo time, q quit.")
    return play(args.image_seconds)


if __name__ == "__main__":
    sys.exit(main())
