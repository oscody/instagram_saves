---
shortcode: "DddNPtGGayH"
url: "https://instagram.com/p/DddNPtGGayH/"
type: "Carousel"
author: "simplifyinai"
shared: "Sep 19, 2026, 08:25 AM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# EgoExoMoCap: free motion capture from smart glasses

The post presents EgoExoMoCap, a free, open-source tool that captures full-body motion from two or more people wearing smart glasses, with no cameras or markers. It explains the tool's core idea and shows its installation commands and method diagram.

Written by claude-haiku-5-5.

## What it teaches

1. Create a Python 3.10 environment: conda create -n egoexomocap python=3.10 -y
2. Activate it: conda activate egoexomocap
3. Install PyTorch matching your CUDA version first
4. Install the dependencies: pip install -r requirements.txt
5. How the method works: each person's glasses record their own point of view, and head and wrist tracking gives a rough starting pose
6. The model finds the same person in the other glasses' views and fuses the clearest views together, so accuracy holds when someone briefly leaves view

## Source

* How to get it: Comment "AI" on the post; the link is sent by DM

## Caption

Comment “AI” to get the link and the full list of free AI resources.

This tool can capture any motions without any cameras and markers.

It’s called EgoExoMoCap, and it can capture full-body motion from nothing but two or more people wearing smart glasses.

So this is how it works:
> each person’s glasses see their own pov
> head and wrist tracking gives a rough starting pose
> the model finds that same person inside the other glasses’ views and fuses the clearest ones together
> accuracy holds even when someone drops out of view for a while, since the other glasses cover the gap.

100% free & open-source.

## Research

* Verdict: Partly valid. EgoExoMoCap is a real open-source (MIT) research repo and the install commands match. But it is a research codebase for training and evaluating on datasets, not a ready-to-use capture tool. It also needs gated data and models, and the link needs no comment or DM.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [EgoExoMoCap code (eth-siplab) (github.com)](https://github.com/eth-siplab/EgoExoMoCap): repo, found by search, verified, high confidence. README has the exact conda python=3.10 env and the PyTorch-first, requirements.txt install from the post; MIT license.
* [EgoExoMoCap project page (siplab.org)](https://siplab.org/projects/EgoExoMoCap): page, found by search, verified, high confidence. Links to the GitHub code; paper from Meta Reality Labs and ETH Zürich.
* [EgoExoMoCap: Distributed Ego-Exo Human Motion Capture (arXiv 2607.15868) (arxiv.org)](https://arxiv.org/abs/2607.15868): paper, found by search, not opened, high confidence. Search result abstract matches the post's two-or-more smart-glasses wearers, head and wrist tracking, and DINOv3 features.

### Key steps

1. conda create -n egoexomocap python=3.10 -y && conda activate egoexomocap
2. Install PyTorch for your CUDA version from pytorch.org
3. pip install -r requirements.txt (dinov3, projectaria-tools, nymeria and human_body_prior build from source)
4. Register free at mano.is.tue.mpg.de and download the Extended SMPL+H model into third_party/body_models/smplh/
5. Download the four checkpoints from the README's Google Drive link into model_zoo/
6. Get the data: request Nymeria access, download EgoHumans, and fetch the ViTPose and DINOv3 checkpoints. Then run the data_prep/ scripts.
7. Evaluate: python main_test.py -opt options/test_nymeria_real_tracker_3pt.yaml
8. Multi-observer fusion: add --multi_observer --protocol splits/egohumans_multiobs_protocol.json to the egohumans test command

### Not found

The repo lists no live capture from your own glasses. It covers dataset training and evaluation only. The README doesn't say whether it supports your own recordings. I did not open the arXiv paper itself.
