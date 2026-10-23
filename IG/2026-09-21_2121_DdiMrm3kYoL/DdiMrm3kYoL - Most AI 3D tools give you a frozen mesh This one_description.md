---
shortcode: "DdiMrm3kYoL"
url: "https://instagram.com/reel/DdiMrm3kYoL/"
type: "Reel"
author: "githubsignals"
shared: "Sep 21, 2026, 09:21 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# WorldSculpt: turning video into editable 3D scenes

The reel presents WorldSculpt, a research tool that builds compositional 3D meshes of cluttered scenes with hundreds of objects from regular camera footage. The on-screen GitHub README shows its authors, news items, a TL;DR list and a pipeline diagram.

Written by claude-haiku-5-5.

## Source

* Link: alayalab/worldsculpt

## Caption

Most AI 3D tools give you a frozen mesh. This one gives you the actual code behind the model. 

WorldSculpt is the research tool that turns messy video footage into detailed, editable three-dimensional worlds. It takes regular camera clips and figures out the precise shape and position of every single object in the scene, even when things are overlapping. This is huge because it means you can build realistic digital environments for games or movies without manually modeling each item from scratch. The system handles hundreds of objects at once, creating a structured mesh that you can actually interact with. It’s like having a magic 3D scanner that understands complex, cluttered rooms.

Open source: alayalab/worldsculpt

Follow for more open source project drops.

#3DDesign #CreativeCoding #GenerativeAI #AICoding #Procedural3D

## Research

* Verdict: Partly valid. The repo is real and matches the reel. But it needs RGB images with instance masks and 3D boxes as input, not plain video. The "actual code behind the model" and "editable" lines are loose: inference code and checkpoints are released, with no training code mentioned.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [alayalab/worldsculpt (github.com)](https://github.com/alayalab/worldsculpt): repo, in the post, verified, high confidence. README describes the official WorldSculpt implementation (compositional meshes of scenes with hundreds of objects), from Alaya Lab, with a TL;DR list, as shown in the reel.

### Key steps

1. Set up the base environment by following the TRELLIS.2 install guide.
2. Install the extra dependencies: natten==0.21.0 built for your GPU, the utils3d wheel, the listed pip packages, and setuptools<81.
3. Download checkpoints from Hugging Face: AlayaLab/WorldSculpt and TencentARC/Pixal3D.
4. Download the UE-MeshyScene and Marble demo datasets and extract the tar archives.
5. Set the env vars INPUT_ROOT, OUTPUT_ROOT, CKPT_ROOT, SAMPLER, step counts, RENDER, FACE_BUDGET and GPU.
6. Run ./inference.sh <scene_name>.

### Not found

I did not check the arXiv paper (2609.05416) or the Hugging Face pages. I did not test the install.
