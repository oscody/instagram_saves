---
shortcode: "DaOHSKmsoBC"
url: "https://instagram.com/reel/DaOHSKmsoBC/"
type: "Reel"
author: "speedy_devv"
shared: "Jul 01, 2026, 07:07 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# KittenTTS: free 25MB CPU text-to-speech model

The post promotes KittenTTS, an open-source text-to-speech model under 25 MB that runs on a CPU without a GPU or cloud API, and lists its features. The caption and on-screen text give the GitHub repo and say a separate voice cloning link is available by comment.

Written by claude-haiku-5-5.

## Source

* Link: github.com/KittenML/KittenTTS
* How to get it: The voice cloning link is not in the post; it is sent only when you comment 'TEXT'.

## Caption

COMMENT ‘TEXT’ to get the link PLUS a voice cloning link as well

ElevenLabs bills you per character. KittenTTS is a full text-to-speech model under 25MB that runs on your CPU for free. 

Go to github.com/KittenML/KittenTTS

It is smaller than a single photo and needs no GPU, so you can ship voices in an app or a script without ever calling a paid cloud API.

> a complete TTS model under 25 MB
> CPU-only, no GPU, fast enough for real time
> open source, generate speech offline
> no per-character cloud bill

Save this if you need voices on a budget.

## Research

* Verdict: Partly valid. KittenTTS is real, open source and runs on CPU, but only the int8 nano V0.8 model is 25 MB. The new flagship KittenTTS 2 is about 506–947 MiB. Voice cloning is now in the repo's KittenTTS 2, so the comment-gated link isn't needed.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [KittenML/KittenTTS (github.com)](https://github.com/KittenML/KittenTTS): repo, in the post, verified, high confidence. Repo opened. It lists the V0.8 ONNX models (nano int8 at 25 MB, CPU-only), Apache-2.0 code, and voice cloning in KittenTTS 2.

### Key steps

1. Requires Python 3.9+. Run: pip install kittenml
2. For the small 25 MB CPU model, use the V0.8 kitten-tts-nano int8 model listed in the repo (check the README for its exact model ID).
3. For the flagship, load it with m = KittenTTS("KittenML/kitten-tts-2"). It is about 506 MiB with weights="emb4" or 947 MiB by default.
4. Generate audio with m.generate(text, voice=...), then save it with soundfile at m.sample_rate. generate_to_file and generate_stream also exist.
5. For voice cloning (KittenTTS 2 only), pass reference=<5–30 s clip of one speaker> instead of voice=. reference_text is optional, and Whisper transcribes the clip if it is omitted.
6. Check the license: the code is Apache-2.0, but the KittenTTS 2 weights use the Stellon Labs Community License.

### Not found

The separate voice cloning link sent by comment 'TEXT' was not seen. The repo documents cloning itself. I did not check the V0.8 nano model's exact Hugging Face ID.
