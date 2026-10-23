---
shortcode: "DeG7TqAmdt3"
url: "https://instagram.com/p/DeG7TqAmdt3/"
type: "Carousel"
author: "simplifyinai"
shared: "Oct 07, 2026, 08:41 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# NVIDIA Lyra 2.0 turns images into 3D worlds

The post announces NVIDIA's open-source Lyra 2.0, which turns a single image into a walkable 3D world that a robot can be dropped into for simulation. The model is said to be on Hugging Face and the UI code on GitHub.

Written by claude-haiku-5-5.

## Source

* How to get it: Comment "AI" on the post; the link and the full list of free AI resources are sent by DM

## Caption

simplifyinai Comment “AI” to get the link and the full list of free AI resources.

Nvidia has just released a tool to turn any image into an explorable 3D world

And they made it 100% open source 🔥

- Model available on Hugging Face
- UI code available on GitHub

Lyra 2.0 creates a world you can walk through, turn around in, and even drop a robot into for simulation.

## Research

* Verdict: Valid. NVIDIA's Lyra 2.0 is real, with code on GitHub and weights on Hugging Face. The DM link is not needed because both are public. Licensing is unclear: code is Apache 2.0, but the weights' license needs checking.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [nv-tlabs/lyra (GitHub) (github.com)](https://github.com/nv-tlabs/lyra): repo, found by search, verified, high confidence. Official NVIDIA repo with Lyra 2.0 code, and a GUI released 2026-07-20.
* [nvidia/Lyra-2.0 (Hugging Face) (huggingface.co)](https://huggingface.co/nvidia/Lyra-2.0): other, found by search, not opened, high confidence. Model weights page linked from the GitHub README; I did not open it myself.
* [Lyra 2 project page (research.nvidia.com)](https://research.nvidia.com/labs/sil/projects/lyra2/): page, found by search, not opened, medium confidence. Linked from the repo README; I did not open it. The paper is arXiv 2604.13036.

### Key steps

1. Clone https://github.com/nv-tlabs/lyra and open the Lyra-2 directory for setup.
2. Download the weights from huggingface.co/nvidia/Lyra-2.0.
3. Check the model license on Hugging Face before any commercial use. Reports conflict on whether the weights are research-only.
4. For the UI, follow Lyra-2/gui/README.md.
5. Give it a single image. It generates a camera-controlled walkthrough video, then reconstructs 3D Gaussian splats and a mesh.
6. The robot simulation step is not documented in the pages I opened. Look in the repo or the paper.

### Not found

The Hugging Face model page and the project page were not opened. The repo's setup commands were not shown on the main README. The robot-simulation claim was not confirmed. The DM'd "free AI resources" list was not checked. The vault's "Lyra" notes are about an unrelated prompt.
