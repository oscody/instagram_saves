---
shortcode: "DeTXC43OIpB"
url: "https://instagram.com/reel/DeTXC43OIpB/"
type: "Reel"
author: "wutronicai"
shared: "Oct 11, 2026, 05:50 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# lingbot-map: open-source 3D scene reconstruction from video

A creator showcases lingbot-map, a free open-source model that rebuilds a 3D room from a video. On-screen footage shows its point-cloud reconstruction as it renders, and the creator suggests uses like real estate tours.

Written by claude-haiku-5-5.

## Source

* Link: lingbot-map

## Caption

You want this library

## Research

* Verdict: Valid. LingBot-Map is a real, free, Apache-2.0 open-source model from Robbyant (Ant Group). It reconstructs 3D scenes from video. The "real estate tours" use is the creator's own suggestion, not something the repo claims.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [robbyant/lingbot-map (GitHub) (github.com)](https://github.com/robbyant/lingbot-map): repo, found by search, verified, high confidence. Opened the repo. It is a streaming 3D reconstruction model with a video demo script and an Apache-2.0 license.
* [LingBot-Map weights (Hugging Face) (huggingface.co)](https://huggingface.co/robbyant/lingbot-map): other, found by search, not opened, high confidence. Linked from the repo README. I did not open it.
* [LingBot-Map paper arXiv:2604.14141 (arxiv.org)](https://arxiv.org/abs/2604.14141): paper, found by search, not opened, medium confidence. The search summary gave the ID. I did not open it.

### Already in the vault

* Vault: `ZAIHub/ig repo to review.md`: Lists the GitHub repo link with the note 'give it a video of a real place → it reconstructs that place in 3D'.
* Vault: `ZAIHub/Vault knowledge library/claude - Instagram and vault correlation.md`: Mentions lingbot. I did not read the note.

### Key steps

1. Create the environment: conda create -n lingbot-map python=3.10 -y, then conda activate lingbot-map.
2. Install PyTorch: pip install torch==2.8.0 torchvision==0.23.0 --index-url https://download.pytorch.org/whl/cu128 (CUDA 12.8).
3. Clone the repo and run pip install -e . from its root.
4. Recommended: pip install flashinfer-python. If you skip it, add --use_sdpa when running the demo.
5. Optional, for the viewer: pip install -e ".[vis]".
6. Download the lingbot-map checkpoint from Hugging Face (robbyant/lingbot-map).
7. Run: python demo.py --model_path /path/to/lingbot-map.pt --video_path video.mp4 --fps 10 --mode windowed --window_size 128 --overlap_keyframes 16 --keyframe_interval 2.
8. Open http://localhost:8080 to view the point cloud.

### Not found

I did not check the Hugging Face page or the arXiv paper. Their links come from the repo README and search results. I also did not check the specific demo footage in the reel. The setup needs a CUDA GPU.
