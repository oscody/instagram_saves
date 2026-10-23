---
shortcode: "DeULCAPk8SW"
url: "https://instagram.com/reel/DeULCAPk8SW/"
type: "Reel"
author: "aiproductlabs"
shared: "Oct 12, 2026, 01:29 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# SpatialLM1.1: open-source 3D scene understanding model

Announces SpatialLM1.1, an open-source 0.5B-parameter model that identifies walls, doors, windows, furniture and other objects in 3D point clouds from monocular video, RGB-D or LiDAR, and supports user-defined object categories. The screenshots show a living room with labeled 3D boxes for TV, sofa, curtain, plants, and similar objects.

Written by claude-haiku-5-5.

## Source

* How to get it: Comment on the post; the post says 'Comment for the link' and gives no specific keyword.

## Caption

The open-source project can process 3D point clouds reconstructed from monocular video, RGB-D images, or LiDAR and identify walls, doors, windows, furniture, and other objects in 3D.
Its lightweight 0.5B-parameter model can be used for applications such as robot navigation, embodied AI, indoor mapping, spatial understanding, and 3D scene reconstruction. SpatialLM1.1 also supports user-defined object categories, letting developers choose which types of objects they want the model to detect.
Comment for the GitHub link.
#SpatialLM #OpenSource #ArtificialIntelligence #AI #SpatialAI #ComputerVision #Robotics #3DMapping #3DReconstruction #EmbodiedAI #MachineLearning #PointCloud #AutonomousRobots #GitHub #Developers

## Research

* Verdict: Valid. The public GitHub repo exists and confirms the post's claims: a 0.5B Qwen-based model, 1.1 release and user-specified categories. The post's "comment for link" gate is unnecessary.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [manycore-research/SpatialLM (github.com)](https://github.com/manycore-research/SpatialLM): repo, found by search, verified, high confidence. README lists SpatialLM1.1-Qwen-0.5B, the Sonata encoder, user-specified categories, and walls, doors, windows and boxes output.

### Already in the vault

* Vault: `ZAIHub/search - competition ideas by claude.md`: Lists this post as 3D scene understanding research. It judges it not needed for the entry, since Quest WebXR already gives planes and meshes. It has no repo link or steps.

### Key steps

1. Create a Python 3.11 conda env. Install the CUDA 12.4 toolkit and sparsehash through conda.
2. Clone the repo, install Poetry, and run `poetry install`.
3. For 1.1, build the Sonata dependency with `poe install-sonata`. This compiles flash-attn and is slow.
4. Prepare a PLY point cloud with z up. Example clouds come from MASt3R-SLAM video reconstructions, and the SpatialLM-Testset has samples.
5. Run `inference.py` with the point cloud path, an output path, and the model, e.g. SpatialLM1.1-Qwen-0.5B from Hugging Face.
6. For custom categories, use `--detect_type object` with `--category`. There are 59 furniture categories.
7. Run `visualize.py` to convert the layout text output to Rerun format.
8. Weights are CC-BY-NC-4.0, so they are non-commercial.

### Not found

Nothing was missing. I didn't check the paper or the Hugging Face model cards. The repo needs an NVIDIA CUDA GPU, which is a limit for Pi or Quest use.
