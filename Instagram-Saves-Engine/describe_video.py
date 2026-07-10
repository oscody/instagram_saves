#!/usr/bin/env python3
"""Describe downloaded reels with Claude vision and save descriptions to each media folder.

Extracts scene-change frames from each reel.mp4, sends them (plus the audio
transcript, if present) to Claude, and writes description.txt alongside the video.
"""

import argparse
import base64
import subprocess
import sys
from pathlib import Path


IG_ROOT = Path("/Users/bogle/Dev/test-stuff/instagram_saves/IG")
DEFAULT_MEDIA_DIR = IG_ROOT / "Media"
VIDEO_FILENAME = "reel.mp4"
TRANSCRIPT_FILENAME = "transcript.txt"
DESCRIPTION_FILENAME = "description.txt"
FRAMES_DIRNAME = "frames"
DEFAULT_MODEL = "claude-sonnet-5"

PROMPT = (
    "These images are frames sampled in order from a short Instagram reel. "
    "Using the frames (and the audio transcript below, if provided) describe "
    "what happens in the video: the setting, who or what appears, any on-screen "
    "text or captions, actions, and the overall point of the clip. Write a "
    "concise paragraph or two. Do not mention that you are looking at frames."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Describe reel.mp4 files with Claude vision and write description.txt alongside them."
    )
    parser.add_argument(
        "--media-dir",
        type=Path,
        default=DEFAULT_MEDIA_DIR,
        help=f"Directory containing media folders. Default: {DEFAULT_MEDIA_DIR}",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Claude model to use. Default: {DEFAULT_MODEL}",
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        default=10,
        help="Maximum number of frames to send per video. Default: 10",
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
        "--max-tokens",
        type=int,
        default=1024,
        help="Maximum tokens in the generated description. Default: 1024",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Re-describe even if a description already exists.",
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


def find_videos(media_dir: Path) -> list[Path]:
    return sorted(path for path in media_dir.rglob(VIDEO_FILENAME) if path.is_file())


def list_frames(frames_dir: Path) -> list[Path]:
    return sorted(frames_dir.glob("frame_*.jpg"))


def load_client():
    try:
        import anthropic
    except ImportError as exc:
        raise SystemExit(
            "The anthropic SDK is not installed. Install it with: pip install anthropic"
        ) from exc
    return anthropic


def scale_filter(frame_width: int) -> str:
    # Downscale to frame_width but never upscale; keep height even for the encoder.
    return f"scale='min({frame_width},iw)':-2"


def extract_frames(
    video_path: Path,
    out_dir: Path,
    scene_threshold: float,
    max_frames: int,
    frame_width: int,
) -> list[Path]:
    scale = scale_filter(frame_width)

    # First pass: scene-change frames (plus the very first frame).
    scene_filter = f"select='eq(n\\,0)+gt(scene\\,{scene_threshold})',{scale}"
    subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-i", str(video_path),
            "-vf", scene_filter,
            "-fps_mode", "vfr",
            "-frames:v", str(max_frames),
            str(out_dir / "frame_%03d.jpg"),
        ],
        check=True,
    )
    frames = sorted(out_dir.glob("frame_*.jpg"))

    # Fallback: a nearly-static clip yields too few scene changes, so sample
    # frames at a fixed cadence instead.
    if len(frames) < 3:
        for stale in frames:
            stale.unlink()
        interval_filter = f"fps=1/2,{scale}"
        subprocess.run(
            [
                "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
                "-i", str(video_path),
                "-vf", interval_filter,
                "-fps_mode", "vfr",
                "-frames:v", str(max_frames),
                str(out_dir / "frame_%03d.jpg"),
            ],
            check=True,
        )
        frames = sorted(out_dir.glob("frame_*.jpg"))

    return frames


def build_content(frames: list[Path], transcript: str | None) -> list[dict]:
    content: list[dict] = []
    for frame in frames:
        data = base64.standard_b64encode(frame.read_bytes()).decode("utf-8")
        content.append(
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": data,
                },
            }
        )
    text = PROMPT
    if transcript:
        text += f"\n\nAudio transcript:\n{transcript}"
    content.append({"type": "text", "text": text})
    return content


def describe(client, model: str, max_tokens: int, content: list[dict]) -> str:
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        thinking={"type": "disabled"},
        messages=[{"role": "user", "content": content}],
    )
    if response.stop_reason == "refusal":
        raise RuntimeError("Claude declined to describe this video (safety refusal).")
    return "".join(block.text for block in response.content if block.type == "text").strip()


def process_video(
    client,
    video_path: Path,
    args: argparse.Namespace,
) -> tuple[bool, str]:
    description_path = video_path.with_name(DESCRIPTION_FILENAME)
    if description_path.exists() and not args.overwrite:
        return False, "description already exists"

    transcript_path = video_path.with_name(TRANSCRIPT_FILENAME)
    transcript = (
        transcript_path.read_text(encoding="utf-8").strip()
        if transcript_path.exists()
        else None
    )

    frames_dir = video_path.with_name(FRAMES_DIRNAME)
    frames = list_frames(frames_dir)
    if frames and not args.refresh_frames:
        frame_note = f"{len(frames)} cached frames"
    else:
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
        frame_note = f"{len(frames)} frames extracted"

    if not frames:
        return False, "no frames extracted"

    content = build_content(frames, transcript)
    description = describe(client, args.model, args.max_tokens, content)
    if not description:
        return False, "empty description returned"

    description_path.write_text(description + "\n", encoding="utf-8")
    return True, f"{frame_note} -> {description_path}"


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

    anthropic = load_client()
    try:
        client = anthropic.Anthropic()
    except Exception as exc:  # noqa: BLE001
        raise SystemExit(f"Could not initialize the Anthropic client: {exc}")
    if not client.api_key and not client.auth_token:
        raise SystemExit(
            "No Anthropic credentials found. Set ANTHROPIC_API_KEY (or run `ant auth login`) before using this script."
        )

    described_count = 0
    skipped_count = 0
    error_count = 0

    for index, video_path in enumerate(videos, start=1):
        print(f"[{index}/{len(videos)}] Describing {video_path}")
        try:
            described, message = process_video(client, video_path, args)
            print(f"  {message}")
            if described:
                described_count += 1
            else:
                skipped_count += 1
        except anthropic.AuthenticationError:
            raise SystemExit(
                "Authentication failed. Set ANTHROPIC_API_KEY or run `ant auth login` before using this script."
            )
        except Exception as exc:  # noqa: BLE001
            error_count += 1
            print(f"  error: {exc}")

    print(
        f"Done. Described: {described_count} | Skipped: {skipped_count} | Errors: {error_count}"
    )
    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
