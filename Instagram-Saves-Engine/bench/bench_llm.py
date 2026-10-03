#!/usr/bin/env python3
"""Benchmark hailo-ollama models: cold load, generation speed, long prompt prefill, and a tagging task."""

import fcntl
import json
import os
import re
import time
from pathlib import Path

import requests

URL = "http://localhost:8000/api/chat"
LOCK_PATH = Path(os.environ.get("XDG_RUNTIME_DIR", "/tmp")) / "hailo-mcp.lock"
IG = Path.home() / "Work/ig/instagram_saves/IG"
MODELS = ["llama3.2:3b", "qwen2.5-instruct:1.5b"]  # end on qwen, the hailo-mcp default
TAGS = ["ai", "coding", "nyc-events", "dating", "relationships", "music", "career",
        "finance", "fitness", "food", "humor", "other"]
OUT = Path(__file__).with_name("bench_llm_results.json")


def chat(model, prompt, num_predict, system=None):
    """Stream one request. Returns text, seconds to first token, total seconds, output tokens."""
    messages = ([{"role": "system", "content": system}] if system else []) + [
        {"role": "user", "content": prompt}]
    body = {"model": model, "messages": messages, "stream": True,
            "options": {"num_predict": num_predict, "temperature": 0}}
    start = time.monotonic()
    first = None
    chunks, text, eval_count = 0, "", None
    with requests.post(URL, json=body, stream=True, timeout=600) as r:
        r.raise_for_status()
        for line in r.iter_lines():
            if not line:
                continue
            data = json.loads(line)
            piece = (data.get("message") or {}).get("content", "")
            if piece:
                if first is None:
                    first = time.monotonic() - start
                chunks += 1
                text += piece
            if data.get("done"):
                eval_count = data.get("eval_count")
    total = time.monotonic() - start
    tokens = eval_count or chunks
    gen_time = total - (first or total)
    return {"text": text, "ttft_s": round(first or total, 2), "total_s": round(total, 2),
            "tokens": tokens, "tok_per_s": round((tokens - 1) / gen_time, 2) if gen_time > 0 else None}


def note_input(note, transcript=None):
    caption = ""
    if note:
        body = note.read_text(encoding="utf-8")
        caption = body.split("## Caption", 1)[-1].strip()[:800]
    words = transcript.read_text(encoding="utf-8").strip()[:1500] if transcript and transcript.exists() else ""
    return f"Caption:\n{caption or '(none)'}\n\nTranscript:\n{words or '(none)'}"


def main():
    items = {
        "claude code reel (transcript only)": note_input(None, IG / "Media/test/test-reel-1/transcript.txt"),
        "healthy relationship (caption only)": note_input(IG / "Notes/1. What does a healthy relationship look like to you.md"),
        "NYC things to do (caption + song lyrics)": note_input(
            IG / "Notes/Things to Do August 29th Events in NYC.md",
            IG / "Media/Things to Do August 29th Events in NYC/transcript.txt"),
        "NYC this week (photo post, caption)": note_input(IG / "Notes/🗽 NYC THIS WEEK 🎉.md"),
    }
    tag_system = ("You label saved Instagram posts. Reply with only JSON: "
                  '{"title": "<short title, max 8 words>", "tags": [<1 to 3 tags>], "summary": "<one sentence>"}. '
                  f"Tags must come from this list only: {', '.join(TAGS)}. "
                  "Ignore song lyrics in the transcript; they are background music.")
    long_text = (IG / "Media/test/test-reel-1/transcript.txt").read_text(encoding="utf-8").strip()

    fd = os.open(LOCK_PATH, os.O_CREAT | os.O_RDWR, 0o600)
    print("waiting for hailo lock...")
    fcntl.flock(fd, fcntl.LOCK_EX)
    results = {}
    try:
        for model in MODELS:
            print(f"\n===== {model} =====")
            res = results[model] = {}
            res["cold"] = chat(model, "Say hi in three words.", 10)
            print(f"cold (model load) total {res['cold']['total_s']}s")

            res["speed"] = []
            for i in range(3):
                r = chat(model, "Write about 150 words explaining what a Raspberry Pi is.", 200)
                res["speed"].append(r)
                print(f"speed run {i + 1}: ttft {r['ttft_s']}s, {r['tokens']} tokens, {r['tok_per_s']} tok/s")

            res["long_prompt"] = {}
            for reps in (1, 2, 3, 5):
                prompt = ("\n\n".join([long_text] * reps)) + "\n\nSummarize the text above in one sentence."
                words = len(prompt.split())
                try:
                    r = chat(model, prompt, 60)
                except requests.RequestException as e:
                    res["long_prompt"][words] = {"error": str(e)[:120]}
                    print(f"prompt {words} words: FAILED ({type(e).__name__})")
                    break
                res["long_prompt"][words] = r
                print(f"prompt {words} words: ttft {r['ttft_s']}s, total {r['total_s']}s -> {r['text'][:120]!r}")

            res["tagging"] = {}
            for name, prompt in items.items():
                r = chat(model, prompt, 150, system=tag_system)
                m = re.search(r"\{.*\}", r["text"], re.S)
                try:
                    parsed = json.loads(m.group(0)) if m else None
                except json.JSONDecodeError:
                    parsed = None
                bad = [t for t in (parsed or {}).get("tags", []) if t not in TAGS] if parsed else None
                r.update(valid_json=parsed is not None, off_list_tags=bad)
                res["tagging"][name] = r
                print(f"tag [{name}] {r['total_s']}s json={parsed is not None} off_list={bad}")
                print(f"  -> {r['text'].strip()[:300]!r}")
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        os.close(fd)
        OUT.write_text(json.dumps(results, indent=2))
        print(f"\nsaved {OUT}")


if __name__ == "__main__":
    main()
