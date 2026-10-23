---
shortcode: "DeOuSexvQGu"
url: "https://instagram.com/reel/DeOuSexvQGu/"
type: "Reel"
author: "devilco.nitin"
shared: "Oct 08, 2026, 09:28 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# DreamX-World: interactive world model from Alibaba

A reel introducing DreamX-World, an Alibaba research model that renders explorable worlds from text prompts, trained on Unreal Engine data, gameplay footage and real road video. It says the 5-billion-parameter weights are on Hugging Face and offers the repo link to anyone who comments "dream".

Written by claude-haiku-5-5.

## Source

* How to get it: Comment "dream" on the post and the creator will send the repo link

## Research

* Verdict: Valid. DreamX-World is a real, public Apache-2.0 repo from Alibaba's AMAP-ML team. Its README matches the post's training data and 5B weights on Hugging Face. The link is public, so you don't need to comment "dream".
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [AMAP-ML/DreamX-World (GitHub) (github.com)](https://github.com/AMAP-ML/DreamX-World): repo, found by search, verified, high confidence. README describes an interactive world model trained on Unreal Engine, gameplay and real-world video, with 5B weights on Hugging Face.
* [DreamX-World-5B (Hugging Face) (huggingface.co)](https://huggingface.co/GD-ML/DreamX-World-5B): tool, found by search, not opened, medium confidence. Linked from the GitHub README as the autoregressive long-horizon 5B checkpoint; I did not open the page itself.
* [DreamX-World-5B-Cam (Hugging Face) (huggingface.co)](https://huggingface.co/GD-ML/DreamX-World-5B-Cam): tool, found by search, not opened, medium confidence. Linked from the README as the 5-second bidirectional camera-control checkpoint; I did not open the page itself.

### Key steps

1. Clone https://github.com/AMAP-ML/DreamX-World and run pip install -r requirements.txt.
2. Download the base Wan2.2-TI2V-5B checkpoint from the Wan-AI org on Hugging Face.
3. Download DreamX-World-5B (long-horizon, autoregressive) and/or DreamX-World-5B-Cam (5-second, camera control) from the GD-ML org on Hugging Face.
4. Follow inference_README.md in the repo.
5. Run inference_dreamx_5b.sh for the standard model, or inference_ar_forcing.sh for the autoregressive path.
6. Expect heavy hardware: one source reports 16 FPS on eight RTX 5090 GPUs.

### Not found

I did not open the Hugging Face model pages directly. I did not check the reel's claim of "real road video" beyond the README's "real-world videos". Search results disagree on release dates (May vs June 2026).
