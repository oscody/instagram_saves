#!/usr/bin/env python3
"""Transcribe downloaded audio with faster-whisper and save transcripts to each media folder."""

import argparse
import sys
from pathlib import Path


IG_ROOT = Path("/Users/bogle/Dev/test-stuff/instagram_saves/IG")
DEFAULT_MEDIA_DIR = IG_ROOT / "Media"
AUDIO_FILENAME = "audio.mp3"
TRANSCRIPT_FILENAME = "transcript.txt"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcribe audio.mp3 files with faster-whisper and write transcript.txt alongside them."
    )
    parser.add_argument(
        "--media-dir",
        type=Path,
        default=DEFAULT_MEDIA_DIR,
        help=f"Directory containing media folders. Default: {DEFAULT_MEDIA_DIR}",
    )
    parser.add_argument(
        "--model",
        default="base",
        help="faster-whisper model size (tiny, base, small, medium, large-v3, ...). Default: base",
    )
    parser.add_argument(
        "--device",
        default="auto",
        help="Device for inference (auto, cpu, cuda). Default: auto",
    )
    parser.add_argument(
        "--compute-type",
        default="int8",
        help="Compute type (int8, int8_float16, float16, float32). Default: int8",
    )
    parser.add_argument(
        "--language",
        default=None,
        help="Force a language code (e.g. en). Default: auto-detect.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Re-transcribe even if a transcript already exists.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional maximum number of audio files to process.",
    )
    return parser.parse_args()


def find_audio_files(media_dir: Path) -> list[Path]:
    return sorted(
        path for path in media_dir.rglob(AUDIO_FILENAME) if path.is_file()
    )


def load_model(model: str, device: str, compute_type: str):
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise SystemExit(
            "faster-whisper is not installed. Install it with: pip install faster-whisper"
        ) from exc
    print(f"Loading model '{model}' (device={device}, compute_type={compute_type})...")
    return WhisperModel(model, device=device, compute_type=compute_type)


def transcribe(model, audio_path: Path, language: str | None) -> tuple[str, str]:
    segments, info = model.transcribe(str(audio_path), language=language)
    text = "".join(segment.text for segment in segments).strip()
    return text, info.language


def process_audio(
    model,
    audio_path: Path,
    language: str | None,
    overwrite: bool,
) -> tuple[bool, str]:
    transcript_path = audio_path.with_name(TRANSCRIPT_FILENAME)
    if transcript_path.exists() and not overwrite:
        return False, "transcript already exists"

    text, detected_language = transcribe(model, audio_path, language)
    if not text:
        return False, "no speech detected"

    transcript_path.write_text(text + "\n", encoding="utf-8")
    return True, f"[{detected_language}] {transcript_path}"


def main() -> int:
    args = parse_args()
    if not args.media_dir.exists():
        raise SystemExit(f"Media directory does not exist: {args.media_dir}")

    audio_files = find_audio_files(args.media_dir)
    if args.limit is not None:
        audio_files = audio_files[: args.limit]

    if not audio_files:
        print(f"No {AUDIO_FILENAME} files found under {args.media_dir}")
        return 0

    model = load_model(args.model, args.device, args.compute_type)

    transcribed_count = 0
    skipped_count = 0
    error_count = 0

    for index, audio_path in enumerate(audio_files, start=1):
        print(f"[{index}/{len(audio_files)}] Transcribing {audio_path}")
        try:
            transcribed, message = process_audio(
                model=model,
                audio_path=audio_path,
                language=args.language,
                overwrite=args.overwrite,
            )
            print(f"  {message}")
            if transcribed:
                transcribed_count += 1
            else:
                skipped_count += 1
        except Exception as exc:  # noqa: BLE001
            error_count += 1
            print(f"  error: {exc}")

    print(
        f"Done. Transcribed: {transcribed_count} | Skipped: {skipped_count} | Errors: {error_count}"
    )
    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
