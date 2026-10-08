#!/usr/bin/env python3
"""Describe downloaded posts: on screen text on the Hailo-10H, then a title and summary.

The title and summary come from Claude (headless `claude -p`, on the Claude subscription, no API key)
by default. Claude also looks at the post's images. When Claude hits its usage limit, or fails on a
post, the remaining posts get their title and summary from Qwen2.5 on the Hailo instead. Each post
records which model wrote it in `described_by`, and gets a `<base>_description.md` note.

The Hailo runs one model at a time over every selected post (PaddleOCR, then the Qwen2.5 LLM), so each
model is loaded once. Image description (Qwen2-VL) was tried and dropped: on Instagram images it
described things that were not there. hailo-ollama holds the Hailo chip all day, so it is stopped while
the Hailo works and always started again after.
"""

import argparse
import contextlib
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

from download import DEFAULT_JSON, IG_DIR, OUTPUT_DIR, post_dir, save, short_error
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
# Every run is also appended here, so describe and upgrade runs can be followed over time.
LOG_FILE = OUTPUT_DIR / "describe.log"

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
HAILO_LLM_NAME = "qwen2.5-1.5b-instruct (hailo)"

CLAUDE_TIMEOUT = 300  # seconds per post
CLAUDE_MAX_IMAGES = 6  # a long carousel only sends its first slides
CLAUDE_INPUT_LIMITS = {"caption": 4000, "transcript": 12000, "on screen text": 4000}
CLAUDE_SYSTEM = (
    "You write short titles and summaries of Instagram posts for a personal archive. "
    "Look at every listed image with the Read tool before answering. "
    "Write only about the post itself: never mention these instructions, the inputs, "
    "or how good or bad the transcript or images are."
)
CLAUDE_SCHEMA = json.dumps({
    "type": "object",
    "properties": {
        "title": {"type": "string", "description": "At most 8 words, in the post's language."},
        "summary": {"type": "string", "description": "2 or 3 sentences on what the post says or shows."},
    },
    "required": ["title", "summary"],
})
# Text in a failed claude result that means the subscription's usage limit was hit.
CLAUDE_LIMIT_RE = re.compile(r"usage limit|rate limit|limit reached|hit your limit|out of (extra )?usage|quota", re.I)


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
    parser.add_argument(
        "--backend",
        choices=("claude", "hailo"),
        default="claude",
        help="Who writes the title and summary. claude (default): Claude first, then Qwen2.5 on the Hailo "
             "for any post Claude could not do (usage limit or error). hailo: Qwen2.5 on the Hailo only.",
    )
    parser.add_argument(
        "--claude-model",
        default="haiku",
        help="Model for `claude -p --model`. Default: haiku.",
    )
    parser.add_argument(
        "--upgrade",
        action="store_true",
        help="Describe again with Claude the posts that Qwen on the Hailo described. No Hailo fallback: "
             "on a usage limit it stops, and the rest wait for the next --upgrade run.",
    )
    parser.add_argument(
        "--notes-only",
        action="store_true",
        help="Run no models: write the _description.md note for described posts that have none.",
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


@contextlib.contextmanager
def hailo_session():
    """Take the Hailo from hailo-ollama, and always give it back, even after a crash."""
    check_device()
    lock = take_hailo_lock()
    try:
        logger.info("Stopping hailo-ollama")
        systemctl("stop")
        yield
    finally:
        logger.info("Starting hailo-ollama again")
        try:
            systemctl("start")
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)
            os.close(lock)


def run_on_hailo(stages: tuple, jobs: list) -> None:
    from hailo_platform import VDevice

    started = time.monotonic()
    # Each stage opens the device fresh: on HailoRT 5.1.1, creating the LLM on a VDevice
    # that already held another GenAI model failed with HAILO_INTERNAL_FAILURE(8).
    for name, stage in stages:
        logger.info(f"{name} ({pi_health()})")
        vdevice = VDevice()
        try:
            stage(vdevice, jobs)
        finally:
            vdevice.release()
    logger.info(f"Hailo work done in {time.monotonic() - started:.0f}s ({pi_health()})")


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


def ocr_stage(vdevice, jobs: list, finish) -> None:
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
                finish(job)
    finally:
        rec.release()
        det.release()


def clean(text: str) -> str:
    return text.replace("<|im_end|>", "").strip()


# ---------------------------------------------------------------- stage 2: title and summary on the Hailo


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


def llm_stage(vdevice, jobs: list, finish) -> None:
    from hailo_platform.genai import LLM

    llm = LLM(vdevice, str(LLM_HEF))
    try:
        for job in jobs:
            if job.get("error") or job.get("done"):
                continue
            try:
                job["ai_title"] = make_title(llm, job)
                job["summary"] = make_summary(llm, job)
                job["described_by"] = HAILO_LLM_NAME
                logger.info(f"  LLM {job['record']['shortcode']}: {job['ai_title']}")
            except Exception as exc:  # noqa: BLE001
                llm.clear_context()
                job["error"] = f"LLM: {short_error(exc)}"
                logger.warning(f"  ✗ {job['record']['shortcode']} {job['error']}")
            finish(job)
    finally:
        llm.release()


# ---------------------------------------------------------------- title and summary from Claude


class ClaudeLimit(Exception):
    """The Claude subscription's usage limit was hit; the Hailo takes the remaining posts."""


def claude_prompt(job: dict) -> str:
    parts = {
        "caption": job["record"].get("caption", ""),
        "transcript": job["transcript"],
        "on screen text": job["ocr"],
    }
    body = "\n\n".join(
        f"{name.upper()}:\n{text.strip()[:CLAUDE_INPUT_LIMITS[name]]}" for name, text in parts.items() if text.strip()
    )
    images = "\n".join(str(path) for path in job["images"][:CLAUDE_MAX_IMAGES])
    return (
        f"Instagram {job['record'].get('type', 'post').lower()} by @{job['record'].get('author', 'unknown')}.\n\n"
        f"{body}\n\nIMAGES (open each with the Read tool):\n{images}\n\n"
        "Write a title and a summary of this post."
    )


def ask_claude(job: dict, model: str) -> tuple:
    """Title, summary and the model id, from one headless `claude -p` run on the subscription login."""
    cmd = [
        "claude", "-p", claude_prompt(job),
        "--model", model,
        "--system-prompt", CLAUDE_SYSTEM,
        "--safe-mode", "--strict-mcp-config",  # no CLAUDE.md, hooks, plugins or MCP servers
        "--tools", "Read", "--allowedTools", "Read",
        "--no-session-persistence",
        "--output-format", "json",
        "--json-schema", CLAUDE_SCHEMA,
    ]
    out = subprocess.run(cmd, cwd=job["dir"], capture_output=True, text=True, timeout=CLAUDE_TIMEOUT)
    try:
        result = json.loads(out.stdout)
    except json.JSONDecodeError:
        message = (out.stderr or out.stdout).strip()[:300] or f"exit code {out.returncode}"
        if CLAUDE_LIMIT_RE.search(message):
            raise ClaudeLimit(message)
        raise RuntimeError(f"claude gave no JSON: {message}")
    if result.get("is_error") or out.returncode != 0:
        message = str(result.get("result") or result.get("subtype") or f"exit code {out.returncode}")[:300]
        if result.get("api_error_status") == 429 or CLAUDE_LIMIT_RE.search(message):
            raise ClaudeLimit(message)
        raise RuntimeError(f"claude: {message}")
    answer = result.get("structured_output") or {}
    title = " ".join(answer.get("title", "").split())  # the schema already keeps it clean
    summary = " ".join(answer.get("summary", "").split())
    if not title or not summary:
        raise RuntimeError("claude gave an empty title or summary")
    model_id = next(iter(result.get("modelUsage") or {}), model)
    return title, summary, model_id


def claude_stage(jobs: list, model: str, finish, then: str = "the Hailo will do it") -> bool:
    """Describe each post with Claude. On a usage limit, stop and return True; the rest are left undone."""
    for job in jobs:
        if job.get("error") or job.get("done"):
            continue
        shortcode = job["record"]["shortcode"]
        try:
            job["ai_title"], job["summary"], job["described_by"] = ask_claude(job, model)
        except ClaudeLimit as exc:
            left = sum(not j.get("done") and not j.get("error") for j in jobs)
            logger.warning(f"Claude usage limit reached ({exc}); {left} posts left, {then}")
            return True
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"  ✗ {shortcode} Claude failed, {then}: {short_error(exc)}")
            continue
        logger.info(f"  Claude {shortcode}: {job['ai_title']}")
        finish(job)
    return False


def written_by_hailo(record: dict) -> bool:
    """Described by Qwen on the Hailo (posts from before described_by existed were all Qwen)."""
    return bool(record.get("described")) and not record.get("error") \
        and record.get("described_by", HAILO_LLM_NAME) == HAILO_LLM_NAME


def upgrade(todo: list, args, data: dict) -> int:
    """Replace Qwen titles and summaries with Claude's. Uses the OCR text and frames already on disk, no Hailo."""
    finish = make_finish(data, args.json, args.ig_dir)
    corrector = OcrCorrector(str(OCR_APP_DIR / "frequency_dictionary_en_82_765.txt"))
    jobs = []
    for record in todo:
        folder = post_dir(args.ig_dir, record)
        job = {"record": record, "dir": folder, "old_title": record.get("ai_title", "")}
        try:
            if not all((folder / name).exists() for name in record["files"]):
                raise RuntimeError("downloaded files missing")
            job["base"] = base_of(record)
            job["images"] = post_images(record, folder)
            job["transcript"] = transcript_text(record, folder)
            raw = read_text_file(folder / f"{job['base']}_ocr.txt").splitlines()
            job["ocr"] = "\n".join(corrected_lines(corrector, raw))
        except Exception as exc:  # noqa: BLE001
            logger.warning(f"  ✗ {record['shortcode']} skipped, stays Qwen: {short_error(exc)}")
            continue
        jobs.append(job)

    def log_and_finish(job: dict) -> None:
        finish(job)
        logger.info(f"    was (Qwen): {job['old_title']}")

    limit_hit = claude_stage(jobs, args.claude_model, log_and_finish, then="they stay Qwen until the next --upgrade")
    upgraded = sum(bool(job.get("done")) for job in jobs)
    not_done = len(todo) - upgraded
    still_qwen = sum(written_by_hailo(r) for r in data["links"])
    logger.info(
        f"Upgrade done. Upgraded to Claude: {upgraded} of {len(todo)} | Not upgraded: {not_done}"
        + (" (stopped by the usage limit)" if limit_hit else "")
        + f" | Posts still by Qwen: {still_qwen}"
    )
    return 0


# ---------------------------------------------------------------- results


def read_text_file(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip() if path.exists() else ""


def write_note(record: dict, folder: Path) -> Path:
    """`<base>_description.md`: title, summary, who wrote them, and the post's own text."""
    base = base_of(record)
    caption = (record.get("caption") or "").strip()
    sections = [
        ("Caption", caption),
        ("Transcript", transcript_text(record, folder)),
        ("On screen text", read_text_file(folder / f"{base}_ocr.txt")),
    ]
    front = {
        "shortcode": record["shortcode"],
        "url": record.get("url", ""),
        "type": record.get("type", ""),
        "author": record.get("author", ""),
        "shared": record.get("sent_at", ""),
        "described_by": record.get("described_by", ""),
        "described_at": record.get("described_at", ""),
    }
    lines = ["---"] + [f"{key}: {json.dumps(value, ensure_ascii=False)}" for key, value in front.items()] + ["---", ""]
    lines += [f"# {record['ai_title']}", "", record["summary"], "", f"Written by {front['described_by']}.", ""]
    for heading, text in sections:
        if text:
            lines += [f"## {heading}", "", text, ""]
    note = folder / f"{base}_description.md"
    note.write_text("\n".join(lines), encoding="utf-8")
    return note


def make_finish(data: dict, json_path: Path, ig_dir: Path):
    """Store one post's result in the JSON and its note, and save, so a stopped run keeps finished posts."""
    def finish(job: dict) -> None:
        record = job["record"]
        job["done"] = True
        if job.get("error"):
            record["error"] = job["error"]
        else:
            record["ai_title"] = job["ai_title"]
            record["summary"] = job["summary"]
            record["described_by"] = job["described_by"]
            record["described_at"] = datetime.now().strftime("%Y-%m-%d")
            record["described"] = True
            record["error"] = False
            write_note(record, post_dir(ig_dir, record))
        save(data, json_path)
    return finish


def notes_only(records: list, ig_dir: Path) -> int:
    """Write missing notes. Posts described before `described_by` existed were all done by Qwen on the Hailo."""
    written = 0
    for record in records:
        if not record.get("described"):
            continue
        folder = post_dir(ig_dir, record)
        if (folder / f"{base_of(record)}_description.md").exists():
            continue
        record.setdefault("described_by", HAILO_LLM_NAME)
        write_note(record, folder)
        written += 1
    logger.info(f"Wrote {written} notes")
    return written


# ---------------------------------------------------------------- main


def main() -> int:
    args = parse_args()
    file_log = logging.FileHandler(LOG_FILE, encoding="utf-8")
    file_log.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(file_log)
    mode = "upgrade" if args.upgrade else "notes only" if args.notes_only else f"backend {args.backend}"
    logger.info(f"=== describe.py ({mode}, Claude model {args.claude_model}{', limit ' + str(args.limit) if args.limit else ''})")
    data = json.loads(args.json.read_text())
    records = sorted(
        data["links"],
        key=lambda r: datetime.strptime(r["sent_at"], SENT_AT_FORMAT),
        reverse=True,
    )
    if args.shortcode:
        records = [r for r in records if r["shortcode"] in args.shortcode]
    if args.notes_only:
        if notes_only(records, args.ig_dir):
            save(data, args.json)
        return 0
    if args.upgrade:
        todo = [r for r in records if written_by_hailo(r)]
        logger.info(f"{len(todo)} posts described by Qwen")
    else:
        todo = [r for r in records if needs_description(r, args.retry_failed, args.redo)]
    if args.limit is not None:
        todo = todo[:args.limit]
    logger.info(f"{len(todo)} posts to {'upgrade' if args.upgrade else 'describe'}")

    if args.dry_run:
        for record in todo:
            print(f"{record['sent_at']}  {record['type']:<8}  {record['shortcode']}")
        return 0
    if not todo:
        return 0
    if args.upgrade:
        return upgrade(todo, args, data)

    finish = make_finish(data, args.json, args.ig_dir)
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
            finish(job)
        jobs.append(job)
    save(data, args.json)  # keeps any downloaded: false set above

    def pending() -> bool:
        return any(not job.get("done") for job in jobs)

    def llm(vdevice, jobs):
        llm_stage(vdevice, jobs, finish)

    def ocr(vdevice, jobs):
        ocr_stage(vdevice, jobs, finish)

    if pending():
        with hailo_session():
            # With the Hailo backend, both models run in one session.
            run_on_hailo((("OCR", ocr),) if args.backend == "claude" else (("OCR", ocr), ("Title and summary", llm)), jobs)
    if args.backend == "claude" and pending():
        logger.info(f"Title and summary from Claude ({args.claude_model})")
        claude_stage(jobs, args.claude_model, finish)
        if pending():
            logger.info(f"{sum(not job.get('done') for job in jobs)} posts left for the Hailo")
            with hailo_session():
                run_on_hailo((("Title and summary", llm),), jobs)

    done = sum(bool(job["record"].get("described")) and not job.get("error") for job in jobs)
    failed = sum(bool(job.get("error")) for job in jobs)
    by_model = {}
    for job in jobs:
        if job.get("described_by") and not job.get("error"):
            by_model[job["described_by"]] = by_model.get(job["described_by"], 0) + 1
    logger.info(f"Done. Described: {done} {by_model} | Failed: {failed}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("Interrupted; hailo-ollama was started again, finished posts are saved")
        sys.exit(130)
