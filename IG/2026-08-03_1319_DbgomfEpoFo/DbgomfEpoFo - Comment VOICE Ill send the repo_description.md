---
shortcode: "DbgomfEpoFo"
url: "https://instagram.com/reel/DbgomfEpoFo/"
type: "Reel"
author: "wassimyounes_"
shared: "Aug 03, 2026, 01:19 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# Free open-source voice agent pipeline from Hugging Face

The reel showcases Hugging Face's open-source, Apache 2.0 real-time speech-to-speech voice agent pipeline, which runs on your own GPU and can swap in local LLMs. It compares this to paid OpenAI Realtime, ElevenLabs and Google Cloud voice services.

Written by claude-haiku-5-5.

## Source

* How to get it: Comment "VOICE" on the post; the repo is sent by DM

## Caption

🟢 Comment “VOICE” — I’ll send the repo

Complete voice-agent pipeline. Free. Open source. Your GPU.

Hugging Face just released the entire real-time voice AI stack as Apache 2.0 — no OpenAI Realtime API fees, no ElevenLabs per-character billing, no Google Cloud per-minute pricing. Just a GPU and an internet connection.

- VAD → STT → LLM → TTS fully modular pipeline
- Every component is swappable (use local LLMs, your servers)
- OpenAI Realtime-compatible WebSocket API
- Already in production for thousands of robots

If you’re building voice agents, you’re not paying for the tech anymore.

🟢 Comment “VOICE” and I’ll DM you the repo

## Research

* Verdict: Valid. Hugging Face's speech-to-speech repo is Apache-2.0 and matches every claim in the post. The DM was not needed because the repo is public.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [huggingface/speech-to-speech (github.com)](https://github.com/huggingface/speech-to-speech): repo, found by search, verified, high confidence. README lists Apache-2.0, a modular VAD→STT→LLM→TTS pipeline, an OpenAI Realtime-compatible WebSocket and use in production for thousands of Reachy Mini robots.

### Already in the vault

* Vault: `ZAIHub/search - skillspector - similar ai safety workflows.md`: Links the post and creator only; no repo link.
* Vault: `2. Areas/VR Work/opensource/AI Inhabited Virtual Space - Implementation Plan.md`: Mentions speech-to-speech; I did not open it to check how.
* Vault: `4. Archives/AI/Ai learning - streaming.md`: Mentions speech-to-speech; I did not open it to check how.

### Key steps

1. Make a venv: python3 -m venv .venv && source .venv/bin/activate (Python 3.11 recommended, 3.11–3.14 supported).
2. On Ubuntu first run: sudo apt-get install libportaudio2 libsndfile1.
3. pip install speech-to-speech
4. Run speech-to-speech local. The first run downloads models (Silero VAD, Parakeet TDT, Qwen3.5-4B, Qwen3-TTS).
5. Wear headphones, or add --local_audio_block_mic_during_playback, so it doesn't hear itself.
6. For server only, run speech-to-speech serve and connect to ws://127.0.0.1:8765/v1/realtime.
7. Swap stages or point the LLM at llama.cpp, vLLM or a hosted provider using the CLI flags in the README.

### Not found

I did not check the post's price comparisons with OpenAI, ElevenLabs and Google. The README says the OpenAI Realtime API support is only a core subset, so the post's "compatible" claim is a bit generous. The default models are small, and the repo doesn't say what GPU you need.
