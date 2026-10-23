---
shortcode: "Dbp9VytG9-A"
url: "https://instagram.com/p/Dbp9VytG9-A/"
type: "Carousel"
author: "simplifyinai"
shared: "Aug 05, 2026, 11:55 AM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# LingBot-Map: open-source video to 3D scene tool

The post presents LingBot-Map, an open-source model from Robbyant that turns real video into a live 3D scene. It lists performance claims: about 20 fps at 518×378 on a single GPU, stable past 10,000 frames, support for drone, driving and indoor video, and a 13-minute, ~25,000-frame indoor walkthrough.

Written by claude-haiku-5-5.

## Source

* How to get it: Comment "AI" on the post; the link is sent by DM. The post also says it is for a free daily AI resource list.

## Caption

Comment “AI” to get the link and the full list of free AI resources.

This tool can turn any real video into a live 3D scene. 100% Open-source.

it’s called LingBot-Map, from Robbyant. 

the numbers back it up:

- ~20 fps at 518×378 on a single gpu
- holds steady past 10,000 frames
- handles drone, driving, and indoor video
- beats both streaming and offline methods on benchmarks

they even pushed a 13-minute, ~25,000-frame indoor walkthrough to prove it holds over long sequences.

## Research

* Verdict: Valid. The public repo exists and matches the post's claims: about 20 fps at 518×378, sequences over 10,000 frames, and the 25,000-frame walkthrough. The benchmark-beating claim is vendor-reported. The link needs no DM.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [robbyant/lingbot-map (GitHub) (github.com)](https://github.com/robbyant/lingbot-map): repo, found by search, verified, high confidence. README gives ~20 FPS at 518×378, 10k+ frames, a 25k-frame 13-minute indoor walkthrough, Apache-2.0.
* [LingBot-Map weights (Hugging Face) (huggingface.co)](https://huggingface.co/robbyant/lingbot-map): other, found by search, not opened, high confidence. Linked from the repo README as the official checkpoint location.
* [Business Wire launch announcement (secure.businesswire.com)](https://secure.businesswire.com/news/home/20260416714351/en/Ant-Groups-Robbyant-Unveils-LingBot-Map-A-Streaming-3D-Reconstruction-Model-for-Real-Time-Spatial-Understanding): page, found by search, not opened, medium confidence. Ant Group press release dated Apr 16, 2026 confirming Robbyant as the author.

### Already in the vault

* Vault: `ZAIHub/ig repo to review.md`: Already lists https://github.com/robbyant/lingbot-map at line 116.

### Key steps

1. Create the environment: conda create -n lingbot-map python=3.10 -y, then conda activate lingbot-map.
2. Install PyTorch 2.8.0 for CUDA 12.8: pip install torch==2.8.0 torchvision==0.23.0 --index-url https://download.pytorch.org/whl/cu128
3. Clone the repo and run pip install -e . (add ".[vis]" for the viewer). Optionally install flashinfer-python, or pass --use_sdpa without it.
4. Download the checkpoint from huggingface.co/robbyant/lingbot-map.
5. Run python demo.py --model_path /path/to/lingbot-map.pt --image_folder example/courthouse --mask_sky, then open http://localhost:8080.
6. For sequences over 3,000 frames, add --mode windowed. For the 25k-frame offline render, use demo_render/batch_demo.py. It needs the extra render install: ffmpeg, onnxruntime-gpu, Kaolin and CUDA extensions.

### Not found

I did not independently check the benchmark claim that it beats both streaming and offline methods. The README gives 6.42 m ATE on Oxford Spires, which is a vendor-reported figure. The demo takes an image folder, so video needs frame extraction first (not checked). An NVIDIA GPU with CUDA is needed.
