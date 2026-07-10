#!/usr/bin/env python3
"""Extract and save reel frames only — no Claude call.

For each IG/Media/<note>/reel.mp4 this writes scene-change frames into a
frames/ subfolder next to the video, so you can inspect them before running
describe_video.py. Shares the extraction logic with describe_video.py.
"""

import argparse
import sys
from pathlib import Path

from describe_video import (
    DEFAULT_MEDIA_DIR,
    FRAMES_DIRNAME,
    VIDEO_FILENAME,
    extract_frames,
    find_videos,
    list_frames,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract and save reel frames into a frames/ subfolder (no API call)."
    )
    parser.add_argument(
        "--media-dir",
        type=Path,
        default=DEFAULT_MEDIA_DIR,
        help=f"Directory containing media folders. Default: {DEFAULT_MEDIA_DIR}",
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        default=10,
        help="Maximum number of frames to save per video. Default: 10",
    )
    parser.add_argument(
        "--scene-threshold",
        type=float,
        default=0.4,
        help="Scene-change sensitivity (0-1); lower captures more frames. Default: 0.4",
    )
    parser.add_argument(
        "--frame-width",
        type=int,
        default=1024,
        help="Downscale frames to this width (never upscales). Default: 1024",
    )
    parser.add_argument(
        "--refresh-frames",
        action="store_true",
        help="Re-extract frames even if a frames/ folder already has them.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional maximum number of videos to process.",
    )
    return parser.parse_args()


def process_video(video_path: Path, args: argparse.Namespace) -> tuple[bool, str]:
    frames_dir = video_path.with_name(FRAMES_DIRNAME)
    existing = list_frames(frames_dir)
    if existing and not args.refresh_frames:
        return False, f"{len(existing)} frames already saved in {frames_dir}"

    frames_dir.mkdir(exist_ok=True)
    for stale in list_frames(frames_dir):
        stale.unlink()

    frames = extract_frames(
        video_path=video_path,
        out_dir=frames_dir,
        scene_threshold=args.scene_threshold,
        max_frames=args.max_frames,
        frame_width=args.frame_width,
    )
    if not frames:
        return False, "no frames extracted"
    return True, f"{len(frames)} frames -> {frames_dir}"


def main() -> int:
    args = parse_args()
    if not args.media_dir.exists():
        raise SystemExit(f"Media directory does not exist: {args.media_dir}")

    videos = find_videos(args.media_dir)
    if args.limit is not None:
        videos = videos[: args.limit]

    if not videos:
        print(f"No {VIDEO_FILENAME} files found under {args.media_dir}")
        return 0

    generated_count = 0
    skipped_count = 0
    error_count = 0

    for index, video_path in enumerate(videos, start=1):
        print(f"[{index}/{len(videos)}] Extracting frames for {video_path}")
        try:
            generated, message = process_video(video_path, args)
            print(f"  {message}")
            if generated:
                generated_count += 1
            else:
                skipped_count += 1
        except Exception as exc:  # noqa: BLE001
            error_count += 1
            print(f"  error: {exc}")

    print(
        f"Done. Generated: {generated_count} | Skipped: {skipped_count} | Errors: {error_count}"
    )
    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
