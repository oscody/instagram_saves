#!/usr/bin/env python3
"""Describe downloaded posts on the Hailo-10H: on screen text, then a title and summary.

Runs one model at a time over every selected post (PaddleOCR, then the Qwen2.5 LLM), so each
model is loaded once. Image description (Qwen2-VL) was tried and dropped: on Instagram images it
described things that were not there. hailo-ollama holds the Hailo chip all day, so it is stopped for
the run and always started again at the end.
"""

import argparse
import fcntl
import json
import logging
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np

from download import DEFAULT_JSON, IG_DIR, post_dir, save, short_error
from export_chat_links import SENT_AT_FORMAT

# Hailo's standalone PaddleOCR example holds the OCR pre and post processing.
OCR_APP_DIR = Path.home() / "Work/hailo-apps/hailo_apps/python/standalone_apps/paddle_ocr"
sys.path.insert(0, str(OCR_APP_DIR))
from paddle_ocr_utils import (  # noqa: E402
    OcrCorrector,
    det_postprocess,
    ocr_eval_postprocess,
    resize_with_padding,
)

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger("ig_describe")

MODELS_DIR = Path("/usr/local/hailo/resources/models/hailo10h")
OCR_DET_HEF = MODELS_DIR / "ocr_det.hef"
OCR_REC_HEF = MODELS_DIR / "ocr.hef"
LLM_HEF = MODELS_DIR / "Qwen2.5-1.5B-Instruct.hef"
# Same lock the hailo-mcp server takes before each request, so it waits while describe runs.
HAILO_LOCK = Path(os.environ.get("XDG_RUNTIME_DIR", "/tmp")) / "hailo-mcp.lock"

FRAMES_PER_REEL = 3
OCR_MIN_CONFIDENCE = 0.6
LLM_SYSTEM = "You write short titles and summaries of Instagram posts."
LLM_MAX_TOKENS = 200
# The Hailo LLM context is about 2K tokens, so each input is cut to fit.
LLM_INPUT_LIMITS = {"caption": 1000, "transcript": 1800, "on screen text": 1000}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
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
    parser.add_argument("--limit", type=int, default=None, help="Describe at most N posts, newest first.")
    parser.add_argument("--retry-failed", action="store_true", help="Also try posts whose error field is set.")
    parser.add_argument(
        "--shortcode",
        action="append",
        help="Only consider this post. Can be given more than once.",
    )
    parser.add_argument(
        "--redo",
        action="store_true",
        help="Describe posts again even if they are already described (for example after a prompt change).",
    )
    parser.add_argument("--dry-run", action="store_true", help="List the posts that would be described, then stop.")
    return parser.parse_args()


# ---------------------------------------------------------------- selection and files


def base_of(record: dict) -> str:
    """The `<shortcode> - <title>` part shared by the post's files."""
    first = Path(record["files"][0]).stem
    return re.sub(r"_\d+$", "", first)


def transcript_text(record: dict, folder: Path) -> str:
    audio = next((name for name in record["files"] if name.endswith(".mp3")), None)
    if not audio:
        return ""
    path = folder / (Path(audio).stem + "_transcript.txt")
    return path.read_text(encoding="utf-8").strip() if path.exists() else ""


def needs_description(record: dict, retry_failed: bool, redo: bool) -> bool:
    if record.get("error") and not retry_failed:
        return False
    if not record.get("downloaded") or (record.get("described") and not redo):
        return False
    # Reels are described after they are transcribed, because the summary uses the transcript.
    has_audio = any(name.endswith(".mp3") for name in record.get("files") or [])
    return record.get("transcribed") or not has_audio


def video_duration(path: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def grab_frame(video: Path, seconds: float, out: Path) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{seconds:.2f}", "-i", str(video),
         "-frames:v", "1", "-q:v", "2", str(out)],
        check=True,
    )
    if not out.exists():
        raise RuntimeError(f"ffmpeg wrote no frame at {seconds:.1f}s")


def post_images(record: dict, folder: Path) -> list:
    """Images to read: 3 frames spread over a reel, or a photo's or carousel's own images.

    A video slide in a carousel gives one frame from its middle.
    """
    base = base_of(record)
    media = [folder / name for name in record["files"] if not name.endswith(".mp3")]
    if record.get("type") == "Reel":
        video = media[0]
        duration = video_duration(video)
        frames = []
        for n in range(1, FRAMES_PER_REEL + 1):
            out = folder / f"{base}_frame_{n}.jpg"
            grab_frame(video, duration * (2 * n - 1) / (2 * FRAMES_PER_REEL), out)
            frames.append(out)
        return frames
    images = []
    for path in media:
        if path.suffix == ".mp4":
            out = path.with_name(f"{path.stem}_frame.jpg")
            grab_frame(path, video_duration(path) / 2, out)
            images.append(out)
        else:
            images.append(path)
    return images


def load_rgb(path: Path) -> np.ndarray:
    image = cv2.imread(str(path))
    if image is None:
        raise RuntimeError(f"Could not read image {path.name}")
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


# ---------------------------------------------------------------- Hailo device handling


def check_device() -> None:
    out = subprocess.run(["hailortcli", "fw-control", "identify"], capture_output=True, text=True)
    if "Device Architecture" not in out.stdout:
        raise RuntimeError(f"Hailo health check failed: {(out.stderr or out.stdout).strip()[:200]}")


def take_hailo_lock():
    fd = os.open(HAILO_LOCK, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        os.close(fd)
        raise RuntimeError("Another program is using the Hailo (hailo-mcp lock is held). Try again later.")
    return fd


def systemctl(action: str) -> None:
    subprocess.run(["sudo", "-n", "systemctl", action, "hailo-ollama"], check=True)


def pi_health() -> str:
    temp = subprocess.run(["vcgencmd", "measure_temp"], capture_output=True, text=True).stdout.strip()
    throttled = subprocess.run(["vcgencmd", "get_throttled"], capture_output=True, text=True).stdout.strip()
    return f"{temp.replace('temp=', 'Pi temp ')}, {throttled}"


# ---------------------------------------------------------------- stage 1: OCR


class HefRunner:
    """One HEF on the device, run one input at a time with float outputs."""

    def __init__(self, vdevice, hef: Path):
        from hailo_platform import FormatType

        self.model = vdevice.create_infer_model(str(hef))
        self.model.set_batch_size(1)
        for output in self.model.outputs:
            output.set_format_type(FormatType.FLOAT32)
        self._ctx = self.model.configure()
        self.configured = self._ctx.__enter__()
        self.input_shape = self.model.input().shape  # (height, width, channels)

    def run(self, image: np.ndarray) -> np.ndarray:
        output = self.model.output()
        bindings = self.configured.create_bindings(
            output_buffers={output.name: np.empty(output.shape, dtype=np.float32)}
        )
        bindings.input().set_buffer(np.ascontiguousarray(image))
        self.configured.run([bindings], 10000)
        return bindings.output().get_buffer()

    def release(self) -> None:
        self._ctx.__exit__(None, None, None)


def letterbox(image: np.ndarray, width: int, height: int) -> np.ndarray:
    """Resize keeping the aspect ratio and pad with grey, as the OCR example does."""
    h, w = image.shape[:2]
    scale = min(width / w, height / h)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_CUBIC)
    padded = np.full((height, width, 3), 114, dtype=np.uint8)
    x, y = (width - new_w) // 2, (height - new_h) // 2
    padded[y:y + new_h, x:x + new_w] = resized
    return padded


def read_text(det: HefRunner, rec: HefRunner, image: np.ndarray) -> list:
    """Lines of text found in one image, top to bottom."""
    det_h, det_w = det.input_shape[:2]
    heatmap = det.run(letterbox(image, det_w, det_h))
    crops, boxes = det_postprocess(heatmap, image, det_h, det_w)
    rec_h, rec_w = rec.input_shape[:2]
    lines = []
    for crop, box in zip(crops, boxes):
        if crop.size == 0:
            continue
        text, confidence = ocr_eval_postprocess(rec.run(resize_with_padding(crop, rec_h, rec_w)))[0]
        if text.strip() and confidence >= OCR_MIN_CONFIDENCE:
            lines.append((box[1], box[0], text.strip()))
    return [text for _, _, text in sorted(lines)]


def corrected_lines(corrector: OcrCorrector, lines: list) -> list:
    """Spell corrected copy for the LLM: splits run together words ("SCOTTLAUNCHED"), drops repeats."""
    seen, out = set(), []
    for line in lines:
        fixed = corrector.correct_text(line).replace("\ufeff", "").strip()
        if fixed and fixed not in seen:
            seen.add(fixed)
            out.append(fixed)
    return out


def ocr_stage(vdevice, jobs: list) -> None:
    corrector = OcrCorrector(str(OCR_APP_DIR / "frequency_dictionary_en_82_765.txt"))
    det, rec = HefRunner(vdevice, OCR_DET_HEF), HefRunner(vdevice, OCR_REC_HEF)
    try:
        for job in jobs:
            if job.get("error"):
                continue
            try:
                seen, lines = set(), []
                for path in job["images"]:
                    for line in read_text(det, rec, load_rgb(path)):
                        if line.lower() not in seen:  # the same text shows on several frames
                            seen.add(line.lower())
                            lines.append(line)
                # The file keeps the raw text; the LLM gets the corrected copy.
                (job["dir"] / f"{job['base']}_ocr.txt").write_text("\n".join(lines) + "\n" if lines else "", encoding="utf-8")
                job["ocr"] = "\n".join(corrected_lines(corrector, lines))
                logger.info(f"  OCR {job['record']['shortcode']}: {len(lines)} lines")
            except Exception as exc:  # noqa: BLE001
                job["error"] = f"OCR: {short_error(exc)}"
                logger.warning(f"  ✗ {job['record']['shortcode']} {job['error']}")
    finally:
        rec.release()
        det.release()


def clean(text: str) -> str:
    return text.replace("<|im_end|>", "").strip()


# ---------------------------------------------------------------- stage 2: title and summary


TITLE_ASK = "Write one short title (at most 8 words) for this Instagram post. Reply with only the title."
# Telling it not to mention the user or the request made it worse: it echoed the instruction.
SUMMARY_ASK = "Summarize this Instagram post in 2 or 3 sentences. Reply with only the summary."


def llm_prompt(job: dict, ask: str) -> list:
    parts = {
        "caption": job["record"].get("caption", ""),
        "transcript": job["transcript"],
        "on screen text": job["ocr"],
    }
    body = "\n\n".join(
        f"{name.upper()}:\n{text.strip()[:LLM_INPUT_LIMITS[name]]}" for name, text in parts.items() if text.strip()
    )
    return [
        {"role": "system", "content": [{"type": "text", "text": LLM_SYSTEM}]},
        {"role": "user", "content": [{"type": "text", "text": f"{body}\n\n{ask}"}]},
    ]


def strip_markup(text: str, label: str) -> str:
    """Remove the markdown, quotes and "Title:" style labels the small model adds anyway."""
    text = re.sub(r"[*#`]", "", text)
    text = re.sub(rf"^\s*{label}s?\s*:\s*", "", text.strip(), flags=re.IGNORECASE)
    return text.strip().strip('"\'').strip()


def ask(llm, job: dict, question: str) -> str:
    answer = clean(llm.generate_all(
        prompt=llm_prompt(job, question), temperature=0.2, seed=42, max_generated_tokens=LLM_MAX_TOKENS
    ))
    llm.clear_context()
    return answer


def make_title(llm, job: dict) -> str:
    lines = [strip_markup(line, "title") for line in ask(llm, job, TITLE_ASK).splitlines()]
    # Skip intro lines such as "The title could be:", and keep the first title if it lists several.
    lines = [line for line in lines if line and not line.endswith(":")]
    title = re.sub(r"^\d+[.)]\s*", "", lines[0] if lines else "")
    if not title:
        raise RuntimeError("LLM gave an empty title")
    return strip_markup(title, "title")


def tidy_summary(text: str) -> str:
    """Clean the small model's summary: markup, talk about the task, repeats, run on text."""
    summary = " ".join(strip_markup(text, "summary").split())
    # It wraps its answer in talk about the task: "Sure, here's ...:",
    # "The summary of the Instagram post is:", "The user is asking for a summary ...".
    summary = re.sub(r"^(sure|here)[^:]{0,80}:\s*", "", summary, flags=re.IGNORECASE)
    summary = re.sub(r"[^.!?:]*\bsummar[^.!?:]*:\s*", "", summary, flags=re.IGNORECASE)
    sentences = [sentence.strip(' "\'') for sentence in re.findall(r"[^.!?]+[.!?]*", summary)]
    kept, seen = [], []
    for sentence in sentences:
        words = set(re.findall(r"\w+", sentence.lower()))
        if not words or re.search(r"summar", sentence, re.IGNORECASE):
            continue
        # It often ends by saying its first sentence again in other words.
        if any(len(words & other) / len(words | other) > 0.5 for other in seen):
            continue
        seen.append(words)
        kept.append(sentence)
    # It also runs on and copies its input; keep 3 sentences, without a cut off fragment at the end.
    kept = kept[:3]
    if len(kept) > 1 and not kept[-1].endswith((".", "!", "?")):
        kept.pop()
    return " ".join(kept)


def make_summary(llm, job: dict) -> str:
    summary = tidy_summary(ask(llm, job, SUMMARY_ASK))
    if not summary:
        raise RuntimeError("LLM gave an empty summary")
    return summary


def llm_stage(vdevice, jobs: list) -> None:
    from hailo_platform.genai import LLM

    llm = LLM(vdevice, str(LLM_HEF))
    try:
        for job in jobs:
            if job.get("error"):
                continue
            try:
                job["ai_title"] = make_title(llm, job)
                job["summary"] = make_summary(llm, job)
                logger.info(f"  LLM {job['record']['shortcode']}: {job['ai_title']}")
            except Exception as exc:  # noqa: BLE001
                llm.clear_context()
                job["error"] = f"LLM: {short_error(exc)}"
                logger.warning(f"  ✗ {job['record']['shortcode']} {job['error']}")
    finally:
        llm.release()


# ---------------------------------------------------------------- main


def write_results(jobs: list, data: dict, json_path: Path) -> tuple:
    done = failed = 0
    for job in jobs:
        record = job["record"]
        if job.get("error"):
            record["error"] = job["error"]
            failed += 1
            continue
        record["ai_title"] = job["ai_title"]
        record["summary"] = job["summary"]
        record["described"] = True
        record["error"] = False
        done += 1
    save(data, json_path)
    return done, failed


def main() -> int:
    args = parse_args()
    data = json.loads(args.json.read_text())
    records = sorted(
        data["links"],
        key=lambda r: datetime.strptime(r["sent_at"], SENT_AT_FORMAT),
        reverse=True,
    )
    if args.shortcode:
        records = [r for r in records if r["shortcode"] in args.shortcode]
    todo = [r for r in records if needs_description(r, args.retry_failed, args.redo)]
    if args.limit is not None:
        todo = todo[:args.limit]
    logger.info(f"{len(todo)} posts to describe")

    if args.dry_run:
        for record in todo:
            print(f"{record['sent_at']}  {record['type']:<8}  {record['shortcode']}")
        return 0
    if not todo:
        return 0

    # Frames and inputs first, on the CPU, before the Hailo is taken from hailo-ollama.
    jobs = []
    for record in todo:
        folder = post_dir(args.ig_dir, record)
        if not all((folder / name).exists() for name in record["files"]):
            record["downloaded"] = False  # download.py fetches it again
            logger.warning(f"  ✗ {record['shortcode']} downloaded files missing, marked for download again")
            continue
        job = {"record": record, "dir": folder, "ocr": ""}
        try:
            job["base"] = base_of(record)
            job["images"] = post_images(record, folder)
            job["transcript"] = transcript_text(record, folder)
        except Exception as exc:  # noqa: BLE001
            job["error"] = short_error(exc)
            logger.warning(f"  ✗ {record['shortcode']} {job['error']}")
        jobs.append(job)
    if not any(not job.get("error") for job in jobs):
        done, failed = write_results(jobs, data, args.json)
        logger.info(f"Done. Described: {done} | Failed: {failed}")
        return 1 if failed else 0

    check_device()
    lock = take_hailo_lock()
    started = time.monotonic()
    try:
        logger.info("Stopping hailo-ollama")
        systemctl("stop")
        from hailo_platform import VDevice

        # Each stage opens the device fresh: on HailoRT 5.1.1, creating the LLM on a VDevice
        # that already held another GenAI model failed with HAILO_INTERNAL_FAILURE(8).
        for name, stage in (("OCR", ocr_stage), ("Title and summary", llm_stage)):
            logger.info(f"{name} ({pi_health()})")
            vdevice = VDevice()
            try:
                stage(vdevice, jobs)
            finally:
                vdevice.release()
        logger.info(f"Hailo work done in {time.monotonic() - started:.0f}s ({pi_health()})")
    finally:
        logger.info("Starting hailo-ollama again")
        try:
            systemctl("start")
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)
            os.close(lock)

    done, failed = write_results(jobs, data, args.json)
    logger.info(f"Done. Described: {done} | Failed: {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("Interrupted; hailo-ollama was started again, no posts were marked described")
        sys.exit(130)
