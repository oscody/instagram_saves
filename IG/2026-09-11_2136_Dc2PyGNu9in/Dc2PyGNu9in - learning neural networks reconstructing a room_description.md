---
shortcode: "Dc2PyGNu9in"
url: "https://instagram.com/reel/Dc2PyGNu9in/"
type: "Reel"
author: "yoiqino"
shared: "Sep 11, 2026, 09:36 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Reconstructing a room from phone images (pt. 5/7)

A reel explaining how a 3D clone of a room can be built from phone photos, using feature matching, Depth Anything V2 depth maps, and Gaussian splatting. It mentions VGGT as a possible upgrade and a phone with real depth sensing as a better option.

Written by claude-haiku-5-5.

## What it teaches

1. Take hundreds of phone photos of the room, including its most important features such as a bookshelf.
2. Run a feature extractor on the images to find the key features in each photo.
3. Match and align the features across photos to work out the phone position each photo was taken from (for example, two photos of a chair from opposite angles are about 180 degrees apart).
4. For each image, estimate a depth map of every object with Depth Anything V2.
5. Combine the images, their phone angles and depth maps, then paint colored splats sized by depth on screen to imitate 3D (Gaussian splatting).
6. To improve the result, try transformer models such as VGGT, or use a phone that gives actual depth values; the creator notes that their 8 GB laptop VRAM is too limited for the transformer option.

## Caption

learning neural networks - reconstructing a room with phone images (pt. 4/7)

day 12/131 learning to build cool tech

## Research

* Verdict: Partly valid. The pipeline in the reel (feature matching, camera poses, Depth Anything V2 depth maps, Gaussian splatting, VGGT as an upgrade) is a real, standard approach. The reel is an overview, not a single resource. I didn't find the creator's own code, and I didn't open the repos.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Depth Anything V2 (github.com)](https://github.com/DepthAnything/Depth-Anything-V2): repo, found by search, not opened, high confidence. Official repo for the depth model named in the reel; it appeared in search results but I didn't open it.
* [VGGT (facebookresearch) (github.com)](https://github.com/facebookresearch/vggt): repo, found by search, not opened, high confidence. Official repo for the transformer upgrade the reel mentions. It estimates camera poses and depth from images and exports to COLMAP for gsplat. I didn't open it.
* [VGGT-1B on Hugging Face (huggingface.co)](https://huggingface.co/facebook/VGGT-1B): tool, found by search, not opened, medium confidence. Model weights for VGGT, which are the usual way to run it.

### Not found

The creator's (yoiqino) own code or write-up for this series was not found, and I didn't search for it. Nothing in the vault matches.
