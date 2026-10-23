---
shortcode: "DdJUHolm52S"
url: "https://instagram.com/p/DdJUHolm52S/"
type: "Carousel"
author: "simplifyinai"
shared: "Sep 11, 2026, 05:58 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Alibaba's ABot-Recon: open-source video-to-3D model

The post introduces ABot-Recon, an open-source 3D scene reconstruction model from Amap CV Lab (Alibaba) that works from a normal RGB video. It highlights a fixed 12-frame local window, lower peak memory, and a Hugging Face demo, with the full resource list gated behind a comment.

Written by claude-haiku-5-5.

## Source

* How to get it: Comment "AI" on the post; the link and resource list are sent by DM

## Caption

Comment “AI” to get the link and the full list of free AI resources.

Alibaba just open-sourced an AI that turns any video into a 3D scene, no depth sensor needed.

It’s called ABot-Recon, from Amap CV Lab (Alibaba).

Most streaming reconstruction systems keep growing their memory buffer as a video gets longer, so they slow down the longer they run. This one doesn’t.

→ Reconstructs scenes spanning 10,000+ frames using only a fixed 12-frame local window, so speed and memory stay flat no matter how long the video runs

→ Cuts peak memory use to roughly a third of comparable methods, making real-time reconstruction possible on regular consumer hardware

→ Only needs a normal RGB video, no depth sensor, no camera calibration

One thing to know: running it locally needs conda, PyTorch, and CUDA, but there’s a live Hugging Face demo if you just want to try it first.

100% Free. Open Source.

## Research

* Verdict: Partly valid. ABot-Recon is real, open source and has a public GitHub repo and HF demo, so no comment is needed. The "regular consumer hardware" claim is not backed up: the README only validates A100 and benchmarks on H100, and gives no minimum VRAM.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [ABot-Recon GitHub (github.com)](https://github.com/amap-cvlab/ABot-Recon): repo, found by search, verified, high confidence. Repo by Amap CV Lab describes the 12-frame streaming reconstruction from RGB video, with conda/PyTorch/CUDA install.
* [ABot-Recon Hugging Face demo (huggingface.co)](https://huggingface.co/spaces/acvlab/abot-recon-streaming-3d): tool, found by search, not opened, medium confidence. Linked from the repo README as the live demo; I did not open the Space itself.
* [ABot-Recon project page (amap-cvlab.github.io)](https://amap-cvlab.github.io/ABot-Recon-html): page, found by search, not opened, medium confidence. Linked from the repo README.
* [TechNode press release (technode.global)](https://technode.global/prnasia/alibabas-amap-introduces-abot-recon-reconstructing-10000-frame-scale-3d-scenes-from-just-12-frames-in-real-time/): page, found by search, not opened, medium confidence. Reports the 10,000-frame scale from a 12-frame window; these are company claims.

### Key steps

1. Try the Hugging Face Space first: huggingface.co/spaces/acvlab/abot-recon-streaming-3d
2. Run: conda create -n abot-recon python=3.11 -y && conda activate abot-recon
3. Run: pip install torch==2.5.1 torchvision==0.20.1 --index-url https://download.pytorch.org/whl/cu121
4. Clone the repo, then run: pip install -e .
5. Optional: install flashinfer-python and build cuRoPE for speed. PyTorch SDPA is the fallback.
6. Put frames in a folder with zero-padded names, then run: python demo.py --image-dir examples/images --output-dir outputs/demo --attention-backend auto --no-loop-closure
7. Or in Python: ABotRecon.from_pretrained('acvlab/ABot-Recon', device='cuda', loop_closure=False), then model.infer(images). The checkpoint downloads automatically.
8. Check MODEL_LICENSE.md before any commercial use. The weights may be non-commercial.

### Not found

The vault has no note on ABot-Recon. I did not open the HF Space. The 'about a third of the memory' claim was not checked against the paper. The README reports 6.71 GiB peak memory on KITTI-02 on an H100.
