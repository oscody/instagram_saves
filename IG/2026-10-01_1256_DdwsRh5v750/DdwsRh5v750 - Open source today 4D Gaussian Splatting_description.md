---
shortcode: "DdwsRh5v750"
url: "https://instagram.com/reel/DdwsRh5v750/"
type: "Reel"
author: "index.opensource"
shared: "Oct 01, 2026, 12:56 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# 4D Gaussian Splatting open source research overview

An overview of 4D Gaussian Splatting, a research method that adds time to 3D Gaussian splatting so a scene can keep moving while the camera moves through it. It also points to the code and paper and flags the licensing terms to check before commercial use.

Written by claude-haiku-5-5.

## What it teaches

1. Video frames and calibrated cameras are the input.
2. The scene is represented as 3D Gaussians, which are soft colored 3D shapes.
3. A space-time feature grid adds the time dimension.
4. A small neural network predicts how each Gaussian deforms at each moment.
5. The result is new views of a moving scene from different camera positions.
6. It is a reconstruction method, not a one-click animation tool that turns a single image into motion.
7. Check each component's license before using it commercially: the root repository is Apache-2.0, but inherited Inria source files use non-commercial research terms, and the demo footage needs a separate rights check.

## Source

* Link: https://github.com/hustvl/4DGaussians

## Caption

Open source today: 4D Gaussian Splatting 📷
Gaussian splatting represents a 3D scene with many soft, colored 3D Gaussians. 4D-GS adds time, so the scene can keep moving while the camera moves through it.

① Video frames + calibrated cameras → ② 3D Gaussians → ③ space-time features → ④ predicted deformation at each moment → ⑤ new views of a moving scene

The researchers combined 3D Gaussians, 4D neural voxels, and a lightweight deformation network. They wanted one efficient representation for a dynamic scene instead of building a separate static 3D scene for every frame. The toy, cooking, and character clips here are the research team's published examples; we did not run the model locally.

가우시안 스플래팅으로 만든 공간에 시간축을 더한 연구입니다. 카메라가 자리를 옮기는 동안 장면 속 물체도 계속 움직이죠. 다중 시점으로 촬영한 움직임을 나중에 다른 시점에서 다시 보거나, 볼류메트릭 장면을 미리 시각화하는 작업을 상상해 볼 수 있어요. 다만 영상에서 보이는 결과는 원저자의 공개 데모이고, 한 장의 사진을 자동으로 애니메이션으로 바꾸는 도구는 아닙니다.

✳︎ Root repository: Apache-2.0 · inherited Inria files: non-commercial research terms · demo footage: separate rights check
📎 Code / 원본: https://github.com/hustvl/4DGaussians
📎 Paper & demos / 논문·데모: https://guanjunwu.github.io/4dgs/
Curated by @hyun2xyz
#OpenSource #4DGS #GaussianSplatting #Dynamic3D
