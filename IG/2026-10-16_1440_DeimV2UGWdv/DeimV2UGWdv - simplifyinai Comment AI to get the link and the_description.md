---
shortcode: "DeimV2UGWdv"
url: "https://instagram.com/p/DeimV2UGWdv/"
type: "Carousel"
author: "simplifyinai"
shared: "Oct 16, 2026, 02:40 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-16"
---

# NVIDIA SANA: open-source world model on one GPU

The post presents NVIDIA's SANA, a 2.6B open-source world model that turns an image, a text prompt, and a camera trajectory into a controllable world on a single GPU such as an RTX 5090 or H100. Screenshots of the SANA README and demo clips show examples of generated scenes.

Written by claude-haiku-5-5.

## Source

* How to get it: Comment "AI" on the post; the link is sent by DM

## Caption

simplifyinai Comment “AI” to get the link and the full list of free AI resources.

Nvidia has a 2.6B open-source world model 🔥

Turn an image, a text prompt, and a camera trajectory into a controllable world.

All on a single GPU.

- Code available on GitHub
- Paper on arXiv
- Useful for embodied AI, robotics research, and simulations

Runs on GPUs like an RTX 5090 or H100, making world-model experiments possible without a multi-GPU setup.

## Research

* Verdict: Valid. The post's SANA is NVIDIA's SANA-WM, a 2.6B open-source world model with public code, paper and weights. The one-GPU claim holds, but only with quantization on a 32 GB RTX 5090.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [NVlabs/Sana (GitHub, includes SANA-WM) (github.com)](https://github.com/NVlabs/Sana): repo, found by search, verified, high confidence. README describes SANA-WM as a 2.6B controllable world model with 720p one-minute video and 6-DoF camera control, Apache-2.0.
* [SANA-WM paper (arXiv 2605.15178) (arxiv.org)](https://arxiv.org/abs/2605.15178): paper, found by search, not opened, high confidence. Linked from the repo README; the paper link was not opened itself.
* [SANA-WM docs (nvlabs.github.io)](https://nvlabs.github.io/Sana/docs/sana_wm/): guide, found by search, verified, high confidence. Gives install, weights, inference commands and VRAM table.
* [SANA-WM weights (bidirectional) (huggingface.co)](https://huggingface.co/Efficient-Large-Model/SANA-WM_bidirectional): other, found by search, not opened, medium confidence. Linked from the official docs; the Hugging Face page was not opened.
* [SANA-WM project page (nvlabs.github.io)](https://nvlabs.github.io/Sana/WM/): page, found by search, not opened, medium confidence. Linked from the repo README; not opened.

### Key steps

1. Clone https://github.com/NVlabs/Sana and run `bash ./environment_setup.sh sana`, then `conda activate sana`.
2. Weights download automatically on first run from Hugging Face (Efficient-Large-Model/SANA-WM_bidirectional, about 96 GB in total including the refiner and its text encoder).
3. Run the bidirectional model: `python inference_video_scripts/wm/inference_sana_wm.py --image asset/sana_wm/demo_0.png --prompt asset/sana_wm/demo_0.txt --action "w-100,dw-60,w-100,aw-60" --num_frames 321 --output_dir results/sana_wm_demo`.
4. For a custom camera path, pass a `.npy` pose file with `--camera` (optionally `--intrinsics`) instead of `--action`. The two options can't be combined.
5. For lower VRAM, add `--offload_vae --offload_refiner`.
6. For streaming, use `inference_sana_wm_streaming.py`. Add `--stage1_precision fp4 --refiner_precision fp4` to fit a 32 GB RTX 5090 (about 29 GB peak, Blackwell only). fp8 needs about 35 GB (H100 or Blackwell) and bf16 about 47 GB.

### Not found

The post's own link is sent only by DM after commenting. A public copy was found on the official GitHub. I didn't open the Hugging Face weights page or the arXiv page directly. The vault has no note on SANA.
