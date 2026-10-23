---
shortcode: "Dc8cexPGcVa"
url: "https://instagram.com/p/Dc8cexPGcVa/"
type: "Carousel"
author: "simplifyinai"
shared: "Sep 06, 2026, 01:49 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# GVHMR: free 3D motion capture from video

The post presents GVHMR, a research model that recovers 3D human motion from ordinary video, with screenshots of its README, demo stages (input video, image-aligned motion, gravity-aligned global motion, physics simulation), and a list of features and local setup needs. The link to the full list of resources is sent only after commenting.

Written by claude-haiku-5-5.

## Source

* How to get it: Comment "AI" on the post; the link and the full list of AI resources are sent via DM

## Caption

Comment “AI” to get the link and the full list of free AI resources.

this tool can turn any video into a full 3d motion capture. 100% free.

GVHMR is a research model, that recovers 3d human motion from ordinary video.

> handles moving, handheld footage
> built-in visual odometry estimates camera motion
> outputs full body motion data ready for animation or biomechanics work

local setup needs python, checkpoint downloads, and a gpu for real video processing.

100% free. open source.

## Research

* Verdict: Valid. GVHMR is a real open-source research repo (zju3dv, SIGGRAPH Asia 2024) that recovers world-grounded human motion from video. The post's claims match the README. The DM list is not needed.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [GVHMR (zju3dv) (github.com)](https://github.com/zju3dv/GVHMR): repo, in the vault, verified, high confidence. README describes world-grounded human motion recovery from video, with demo scripts and optional visual odometry, as in the post.

### Already in the vault

* Vault: `ZAIHub/ig repo to review.md`: GVHMR entry with repo link, a done item for forking it, and a note on an Apple-Silicon (MPS) fork
* Vault: `3. Resources/0. note idea draft/repo - gvhmr.md`: Draft note on the repo, including that it has no fingers or face tracking

### Key steps

1. Clone https://github.com/zju3dv/GVHMR and follow docs/INSTALL.md to set up the Python environment.
2. Download the checkpoints. The model is expected at inputs/checkpoints/gvhmr/gvhmr_siga24_release.ckpt.
3. Run a single video: python tools/demo/demo.py --video=docs/example_video/tennis.mp4 -s
4. Drop the -s flag for moving cameras. The camera is then estimated by visual odometry (DPVO). The README says SimpleVO is a newer option.
5. Run a folder of videos: python tools/demo/demo_folder.py -f inputs/demo/folder_in -d outputs/demo/folder_out -s
6. A GPU is needed for real video. Your vault mentions an Apple-Silicon (MPS) fork.

### Not found

The DM list of free AI resources was not checked. The license terms were not visible in the fetched page, so check the LICENSE file before commercial use, despite the post's "100% free".
