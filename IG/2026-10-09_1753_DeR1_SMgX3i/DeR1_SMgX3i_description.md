---
shortcode: "DeR1_SMgX3i"
url: "https://instagram.com/reel/DeR1_SMgX3i/"
type: "Reel"
author: "git.radar"
shared: "Oct 09, 2026, 05:53 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# LingBot-Map: 3D reconstruction from video

The reel promotes LingBot-Map, an open-source GitHub project that builds 3D maps from video as it is recorded, and scrolls through its README on screen. The caption notes 17,588 GitHub stars and an ECCV 2026 Best Paper Award candidate label.

Written by claude-haiku-5-5.

## What it teaches

1. Create the environment: conda create -n lingbot-map python=3.10 -y, then conda activate lingbot-map
2. Install PyTorch 2.8.0 with CUDA 12.8 (torchvision 0.23.0) using the index URL from the README; the README notes this version is recommended because the batch rendering pipeline needs its prebuilt wheels
3. Install the package from the repo folder with pip install -e .
4. Install FlashInfer (the README marks this as recommended)

## Source

* Link: https://github.com/Robbyant/lingbot-map

## Caption

[ECCV 2026 Best Paper Award Candidate] LingBot-Map: Geometric Context Transformer for Streaming 3D Reconstruction

🔗 https://github.com/Robbyant/lingbot-map
⭐ 17588 stars | 📈 +109 today
🔵 Python

#github #opensource #coding #developer #programming #softwareengineering #techtools #devtools #buildinpublic #python

## Research

* Verdict: Valid. The repo exists and matches the post: Apache-2.0, install steps as shown, and the repo title carries the "ECCV 2026 Best Paper Award Candidate" label. The label is a candidate nomination, not a win. Note the post says it builds maps "as it is recorded"; the repo does streaming reconstruction from frames or video and needs CUDA.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [LingBot-Map (Robbyant) (github.com)](https://github.com/Robbyant/lingbot-map): repo, in the post, verified, high confidence. README title, install steps (Python 3.10, PyTorch 2.8.0/CUDA 12.8, pip install -e ., FlashInfer) and star count of about 18k match the post.
* [LingBot-Map technical report (arxiv.org)](https://arxiv.org/abs/2604.14141): paper, found by search, not opened, medium confidence. The URL comes from the repo README as read by WebFetch. I did not open the paper itself.
* [LingBot-Map project page (technology.robbyant.com)](https://technology.robbyant.com/lingbot-map): page, found by search, not opened, medium confidence. The URL is listed in the repo README. I did not open it.

### Already in the vault

* Vault: `ZAIHub/ig repo to review.md`: Has the repo link, the one-line summary "video of a real place → 3D reconstruction", a ChatGPT research share link, and a note that it is not ready for Mac yet.

### Key steps

1. conda create -n lingbot-map python=3.10 -y && conda activate lingbot-map
2. Install PyTorch 2.8.0 and torchvision 0.23.0 for CUDA 12.8 (use the index URL from the README)
3. git clone the repo, then run pip install -e . in the repo folder
4. Optional: pip install flashinfer-python (from pypi.org). Without it, add --use_sdpa when running.
5. For the viewer: pip install -e ".[vis]"
6. Download the lingbot-map checkpoint from Hugging Face (robbyant/lingbot-map)
7. Run: python demo.py --model_path /path/to/lingbot-map.pt --image_folder example/courthouse --mask_sky, then open http://localhost:8080
8. For long sequences (over 3000 frames) add: --mode windowed --window_size 128 --overlap_keyframes 16 --keyframe_interval 2. For low GPU memory add: --offload_to_cpu --num_scale_frames 2.

### Not found

I did not open the arXiv paper or the project page. I could not confirm the ECCV award status beyond the repo's own "candidate" label.
