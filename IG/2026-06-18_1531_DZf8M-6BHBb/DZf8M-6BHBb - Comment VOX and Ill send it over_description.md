---
shortcode: "DZf8M-6BHBb"
url: "https://instagram.com/reel/DZf8M-6BHBb/"
type: "Reel"
author: "wassimyounes_"
shared: "Jun 18, 2026, 03:31 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# VoxCPM2: free open-source voice AI tool

The reel promotes VoxCPM2, a free, open-source text-to-speech model that its creator calls the #1 trending repo on GitHub, and lists its features: voice design from a text description, 30 languages, local use on an RTX 4090, Apache-2.0 licensing, and voice cloning. The on-screen README shows the project title and Apache-2.0 license.

Written by claude-haiku-5-5.

## Source

* Link: VoxCPM2
* How to get it: comment "VOX" to receive the repo and live demo by DM

## Caption

Comment “VOX” and I’ll send it over. 👇

The #1 trending repo on GitHub right now is a free, open-source voice AI that generates a studio-quality voice from a single text description. 🎙️

It’s VoxCPM2 — a text-to-speech model from the team behind MiniCPM. Type what you want it to say, and it speaks it in a natural, expressive voice across 30 languages. Why creators are jumping on it:

🎨 Design a brand-new voice from words alone — set the gender, age, tone, and emotion, no reference audio needed
🌍 30 languages out of the box, in crisp 48kHz studio quality
⚡ Runs faster than real-time on a single RTX 4090 — locally, no cloud, no per-character bill
🆓 Fully open-source (Apache-2.0) and free for commercial use — voiceovers, dubbing, characters, all yours
🎛️ It can also clone a voice from a short clip — meant for your own voice, since the project bans impersonation and fraud

Premium AI voices used to mean a monthly bill. This one’s free, runs on your own machine, and it’s yours to keep.

Comment “VOX” — the repo + the live demo, in your DMs. 👇

#VoiceAI #TextToSpeech #OpenSourceAI

## Research

* Verdict: Partly valid. VoxCPM2 is real, public and matches the listed features (Apache-2.0, 30 languages, voice design, cloning). The "#1 trending" claim isn't backed by the README, and the "runs on a 4090" claim needs a caveat. The DM gate is unnecessary.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [OpenBMB/VoxCPM (VoxCPM2) (github.com)](https://github.com/OpenBMB/VoxCPM): repo, found by search, verified, high confidence. README describes VoxCPM2, a 2B MiniCPM-4-based TTS model with Apache-2.0 license, 30 languages, 48kHz, voice design and cloning.
* [VoxCPM live demo (Hugging Face Space) (huggingface.co)](https://huggingface.co/spaces/OpenBMB/VoxCPM-Demo): tool, found by search, not opened, medium confidence. Link given in the repo README as the Live Playground; I did not open the Space itself.
* [VoxCPM2 model weights (huggingface.co)](https://huggingface.co/openbmb/VoxCPM2): page, found by search, not opened, medium confidence. Appeared in search results as the official model page; I did not open it.

### Key steps

1. Install: pip install voxcpm (Python 3.10–3.12, PyTorch ≥2.5, CUDA ≥12.0).
2. Voice design: put a description in parentheses before the text, e.g. "(A young woman, gentle and sweet voice)Hello, welcome to VoxCPM2!" No reference audio is needed.
3. Controllable cloning: pass reference_wav_path with a short clip of your own voice. You can add a style description in parentheses.
4. Ultimate cloning: pass prompt_wav_path plus prompt_text (the exact transcript of the clip).
5. Try it without installing in the Hugging Face demo Space.
6. The repo also supports SFT/LoRA fine-tuning and a CLI.

### Not found

I found no source for the "#1 trending repo on GitHub" claim for VoxCPM2. The README cites #1 GitHub Trending only for the earlier VoxCPM1.5. I did not open the demo Space or the HF model page.
