---
shortcode: "Deav1B_ANwB"
url: "https://instagram.com/reel/Deav1B_ANwB/"
type: "Reel"
author: "index.opensource"
shared: "Oct 13, 2026, 01:11 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# COLMAP recovers camera positions and 3D points

A reel introducing COLMAP, an open-source tool that recovers camera positions and 3D points from overlapping photos. It uses 96 frames of a drone clip of Chapultepec Castle, yielding 69,316 sparse 3D points, and ends by asking which place viewers would record as a point cloud.

Written by claude-haiku-5-5.

## What it teaches

1. Find features: detect distinctive spots in every image.
2. Match features: match those spots across overlapping views, keeping only matches that fit one camera motion.
3. Estimate cameras and triangulate points: start from two frames, work out the camera motion, triangulate the first points, then add one frame at a time.
4. Refine the reconstruction: bundle adjustment adjusts all cameras and points together until they agree with every frame.

## Source

* Link: https://github.com/colmap/colmap/tree/c4a3b308bddf391b4e7c62e835720f83c13aea8b

## Caption

COLMAP — recovering camera positions and 3D points from overlapping images.

① Find features → ② match them across views → ③ estimate cameras and triangulate points → ④ refine the reconstruction.

This run used 96 frames from a drone clip and recovered 69,316 sparse 3D points. We used its camera positions for our own 3D-object compositing and point-cloud fly-through effects.

What place would you record as a point cloud?

COLMAP은 겹치는 사진에서 카메라 위치와 3D 점을 함께 찾습니다.

① 특징점 찾기 → ② 사진끼리 매칭하기 → ③ 카메라 위치와 점 계산하기 → ④ 전체 결과 다듬기.

이번 실행은 드론 영상의 96개 프레임에서 희소 3D 점 69,316개를 찾았습니다. 계산된 카메라 위치를 활용해 저희가 3D 물체 합성과 점구름 비행 효과를 더했습니다.

어떤 장소를 점구름으로 기록해 보고 싶으세요?

📎 COLMAP · Johannes Schönberger et al. · © ETH Zurich and UNC Chapel Hill · new BSD
https://github.com/colmap/colmap/tree/c4a3b308bddf391b4e7c62e835720f83c13aea8b
https://github.com/colmap/colmap/blob/c4a3b308bddf391b4e7c62e835720f83c13aea8b/COPYING.txt
Drone video: ProtoplasmaKid · CC0 · Wikimedia Commons
https://commons.wikimedia.org/wiki/File:Sobrevuelo_Castillo_de_Chapultepec.webm

Curated by @hyun2xyz

#OpenSource #COLMAP #Photogrammetry #CreativeCoding

## Research

* Verdict: Valid. COLMAP is a real, well-known open-source SfM/MVS tool under the new BSD license, and the post's four-stage description matches how it works. The 96-frame and 69,316-point figures come from the creator's own run, and I did not check them.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [COLMAP (GitHub) (github.com)](https://github.com/colmap/colmap): repo, in the post, verified, high confidence. The repo page describes a Structure-from-Motion and Multi-View Stereo pipeline under the new BSD license, as the post credits. The post links a specific commit of this repo.
* [Sobrevuelo Castillo de Chapultepec (drone video, ProtoplasmaKid, CC0) (commons.wikimedia.org)](https://commons.wikimedia.org/wiki/File:Sobrevuelo_Castillo_de_Chapultepec.webm): video, in the post, not opened, medium confidence. The post credits this as the source of its drone footage. I did not open it.

### Key steps

1. Install COLMAP: Windows prebuilt binaries from GitHub releases, `conda install colmap` (conda-forge), Docker, or build from source (see colmap.github.io/install.html).
2. For Python use, install the `pycolmap` bindings from PyPI (`pycolmap-cuda12` for CUDA).
3. Extract frames from a video, or collect overlapping photos, into one folder.
4. Open the GUI, or use the CLI automatic reconstructor, and point it at the image folder. This runs feature extraction, matching, incremental mapping and bundle adjustment.
5. Inspect the sparse model's camera poses and 3D points, then export them to use in compositing or point-cloud effects.

### Not found

I did not open the specific commit link or the Wikimedia video. I did not check the CLI command names in the docs. I could not check the 96-frame and 69,316-point figures.
