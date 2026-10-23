---
shortcode: "Da6tDoqDeve"
url: "https://instagram.com/p/Da6tDoqDeve/"
type: "Carousel"
author: "technology"
shared: "Jul 19, 2026, 08:48 AM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Open-source tool turns phone videos into 3D worlds

The carousel presents a free, open-source tool that builds navigable 3D point clouds from ordinary phone videos on a home GPU, using ByteDance's Depth Anything 3. It includes screenshots of the depth-anything.cpp studio, a tweet from Richard Palethorpe showing reconstructions and noting rough, blocky results, and a GitHub pull request.

Written by claude-haiku-5-5.

## What it teaches

1. Record a video walking around a space with a phone.
2. The tool reads depth from each frame.
3. It stitches the frames into a 3D point cloud that you can move through.

## Source

* Link: mudler/depth-anything.cpp

## Caption

Someone has open sourced a powerful tool that transforms ordinary phone videos into interactive 3D worlds using local AI processing, with no cloud service or subscription required 📱🌍

The project combines ByteDance’s Depth Anything 3, depth-anything.cpp, and SLAM techniques to estimate depth from every video frame, track camera movement, and reconstruct a navigable 3D point cloud that runs on a home GPU. It is completely free and open source, although current results remain rough and voxel styled rather than fully realistic.

This approach could make 3D scene creation far more accessible for developers, creators, robotics, gaming, AR, and VR without expensive LiDAR hardware or paid software, while future improvements are expected to deliver cleaner and more detailed reconstructions.

Would you use your phone to build 3D worlds?

Sources: GitHub (mudler/depth-anything.cpp) · Hugging Face · ByteDance Seed

#ai #opensource #3d #tech #innovation

## Research

* Verdict: Valid. The repo exists and is MIT-licensed. Its merged PR #2 adds the video-to-point-cloud pipeline, voxel mode, VSLAM elements and a web studio. The "rough, voxel-styled" caveat matches. The README alone doesn't mention video or the studio, so you have to read the PR.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [mudler/depth-anything.cpp (github.com)](https://github.com/mudler/depth-anything.cpp): repo, in the post, verified, high confidence. C++/ggml port of ByteDance Depth Anything 3 with a CLI, point-cloud (PLY) export and Vulkan, CUDA and Metal backends.
* [PR #2: Demo server, Video, Voxels and elements of VSLAM (github.com)](https://github.com/mudler/depth-anything.cpp/pull/2): page, found by search, verified, high confidence. Merged Jul 27, 2026. Adds streaming video reconstruction, a WebGL studio server, voxel mode and loop closure, matching the post's screenshots.

### Key steps

1. Clone the repo: git clone --recursive https://github.com/mudler/depth-anything.cpp
2. Build with GPU support enabled: cmake -B build -DDA_BUILD_CLI=ON (add the CUDA, Metal or Vulkan flag), then cmake --build build -j
3. Download and convert a DA3 model to GGUF: python scripts/download_model.py --repo depth-anything/DA3-BASE --out models/DA3-BASE, then python scripts/convert_da3_to_gguf.py --model models/DA3-BASE --output models/depth-anything-base-f32.gguf
4. Quick test on one image: build/examples/cli/da3-cli reconstruct --model <gguf> --input photo.jpg --ply cloud.ply
5. For video, build and launch the demo server in the server/ directory from PR #2. Check that directory for the exact commands, since the README doesn't cover them.
6. To force a GPU, set DA_DEVICE, for example Vulkan1 or CUDA0.
7. Check the licenses. DA3 Small and Base are Apache-2.0. Large, Giant and Nested are CC BY-NC 4.0, so non-commercial only.

### Not found

I found no launch instructions for the video studio server. The PR page doesn't give them, and I didn't open the server/ directory. I didn't check the tweet or the Hugging Face link.
