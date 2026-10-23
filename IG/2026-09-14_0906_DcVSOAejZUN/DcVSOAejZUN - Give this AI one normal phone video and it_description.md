---
shortcode: "DcVSOAejZUN"
url: "https://instagram.com/reel/DcVSOAejZUN/"
type: "Reel"
author: "githubsignals"
shared: "Sep 14, 2026, 09:06 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# 4DAnyone: one phone video to 4D character

A reel presenting the open-source 4DAnyone project, which turns one casual monocular phone video into multi-view videos that can feed 4D Gaussian Splatting reconstruction. On-screen, it scrolls through the project's GitHub README, including its installation and inference commands.

Written by claude-haiku-5-5.

## What it teaches

1. Clone the repo: git clone https://github.com/ant-research/4DAnyone.git, then cd 4DAnyone
2. Initialize the submodule: git submodule update --init third_party/GVHMR
3. Create the environment: conda create -n 4danyone python=3.11 -y, then conda activate 4danyone
4. Install dependencies: pip install -r requirements.txt
5. Optionally install FlashAttention-3 or SageAttention for faster inference
6. Models and examples download automatically on first use, or manually with python scripts/download_smplx.py, python scripts/download_model.py and python scripts/download_example.py
7. For inference, use the 'Generate target views' section of the README, which shows an example that generates 6 evenly spaced views around the subject

## Source

* Link: ant-research/4danyone

## Caption

Give this AI one normal phone video, and it predicts what the person looks like from angles the camera never captured. 

4DAnyone is the video generator that takes a single casual phone clip and turns it into a fully explorable four-dimensional character. You do not need a special camera rig or expensive studio setup to capture someone moving in three dimensions. This tool accepts one standard video of a person and predicts how they look from every possible angle, including views from above, behind, and around them. It handles the tricky work of matching the motion and lighting so the generated angles look consistent. Once you have those multiple views, you can feed them into standard reconstruction tools to build a realistic digital twin.

Open source: ant-research/4danyone

Follow for more open source project drops.

#4DGeneration #ComputerVision #GenerativeAI

## Research

* Verdict: Valid. The GitHub repo exists and its README matches the post's install steps and its multi-view generation claim. It outputs multi-view videos for 4DGS, not a finished 4D character, so the caption slightly overstates.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [ant-research/4DAnyone (github.com)](https://github.com/ant-research/4DAnyone): repo, in the post, verified, high confidence. README describes turning a monocular person video into multiview videos for 4DGS, with the same install commands as the post.

### Key steps

1. git clone https://github.com/ant-research/4DAnyone.git && cd 4DAnyone
2. git submodule update --init third_party/GVHMR
3. conda create -n 4danyone python=3.11 -y && conda activate 4danyone
4. pip install -r requirements.txt
5. Optional: install FlashAttention-3 or SageAttention for speed; it is enabled automatically.
6. Models and examples download on first run, or run scripts/download_smplx.py, download_model.py and download_example.py.
7. Run: python inference.py --video_path <video.mp4> --output_dir <out> --views_per_layer 6 (use 24 for dense 360° coverage). Run --help for all options.
8. Input tips: one person, full or upper body, a steady camera, 9:16 portrait, 1080p or higher, at least 121 frames. Expect about 22 GB peak GPU memory. Feed the output views into 4DGS reconstruction.
