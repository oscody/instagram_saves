---
shortcode: "Dfb2FEKm_YB"
url: "https://instagram.com/p/Dfb2FEKm_YB/"
type: "Carousel"
author: "simplifyinai"
shared: "Nov 07, 2026, 09:44 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-09"
---

# ABot-Recon: Alibaba free 3D reconstruction model

The post announces ABot-Recon, an open-source streaming 3D reconstruction model from Amap CV Lab, and lists its claims: 10,000+ frames with a 12-frame window, peak memory at one third of comparable methods, and only a normal RGB video as input. It shows three city-map examples (Beijing 3rd Ring Road, Beijing Wangjing, Wuhan University) with video length and frame counts.

Written by claude-haiku-5-5.

## Source

* How to get it: Comment "AI" on the post; the link is sent by DM

## Caption

simplifyinai Comment “AI” to get the link and the full list of free AI resources.

This alibaba model turns any image into ready-to-use 3d assets. 100% free.

It's called ABot-Recon, from Amap CV Lab 

Most streaming reconstruction systems keep growing their memory buffer as a video gets longer, so they slow down the longer they run. This one doesn't.

→ Reconstructs 10,000+ frames using a 12-frame window
→ Cuts peak memory use to 1/3 of comparable methods
→ Only needs a normal RGB video

100% free & open-source.

## Research

* Verdict: Partly valid. ABot-Recon is real and open source, and the repo is public, so no comment or DM is needed. The caption's "turns any image into 3D assets" is wrong: it reconstructs scenes from RGB video, and the weights have a separate license.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [ABot-Recon GitHub repo (github.com)](https://github.com/amap-cvlab/ABot-Recon): repo, found by search, verified, high confidence. README matches the post: Apache-2.0 code, 12-frame local context, Amap CV Lab, paper and online demo links.
* [Paper: Revisiting Local Context for Long-Horizon Streaming 3D Reconstruction (arXiv 2608.27529) (arxiv.org)](https://arxiv.org/abs/2608.27529): paper, found by search, not opened, medium confidence. The arXiv ID comes from search results and the repo README. I did not open the paper.
* [ABot-Recon project page (amap-cvlab.github.io)](https://amap-cvlab.github.io/ABot-Recon-html): page, found by search, not opened, medium confidence. Search results and the repo README name this project page. I did not open it.

### Already in IG saves

* Same: Web: [Alibaba's ABot-Recon: open-source video-to-3D model (instagram.com)](https://instagram.com/p/DdJUHolm52S/) (`DdJUHolm52S`). Same link: ABot-Recon GitHub repo.

### Key steps

1. Create a conda env with Python 3.11 on Linux. The README validates CUDA 12.1 on an A100.
2. Install torch 2.5.1 and torchvision 0.20.1 from the cu121 index.
3. Clone https://github.com/amap-cvlab/ABot-Recon and run pip install -e .
4. Extract video frames into a folder with zero-padded names (000001.jpg), because frames are sorted by name.
5. Run demo.py with --image-dir, --output-dir, --attention-backend auto and --no-loop-closure.
6. Or use the Python API: ABotRecon.from_pretrained(...) then model.infer(images).
7. The weights download automatically from Hugging Face (acvlab/ABot-Recon) or ModelScope. For offline use, put them at checkpoints/abot_recon.safetensors.
8. Check MODEL_LICENSE.md before any commercial use. Press coverage says the weights are non-commercial.

### Not found

I did not open the arXiv paper or the project page. I did not read MODEL_LICENSE.md, so the weights' license terms are unconfirmed. No minimum GPU memory is stated. The README validates A100 and benchmarks on H100.
