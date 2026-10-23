---
shortcode: "DeAIlHrClCu"
url: "https://instagram.com/reel/DeAIlHrClCu/"
type: "Reel"
author: "billy.coder"
shared: "Oct 03, 2026, 12:16 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Open-source model turns house photos into floor plans

The reel shows a 3D reconstruction in which colored room outlines are drawn over point clouds, with the claim that a model turns photos of a building into a floor plan by solving all connected rooms together. The caption adds details about the license, weight size, notebook and paper venue.

Written by claude-haiku-5-5.

## Source

* How to get it: Comment SCAN on the post

## Caption

Matterport wants $6,000 for the camera and $69 a month to keep your tour online. Microsoft, ETH Zurich and Lund University gave away the model that turns ordinary photos of a house into a 3D floor plan. Apache licensed.

Photos of the building go in and a full 3D floor plan comes out. Most methods do one room, then the next, then try to stitch them together. This one solves every connected room at the same time, so the plan holds together instead of breaking at every doorway.

Apache 2.0, the trained weights are a 298MB download, and there is a notebook that runs on their sample scene. It is an ECCV 2026 paper, so the method was reviewed before it was released, and the repo sits at 165 stars.

Send this to whoever just got quoted $500 to scan a three bedroom house.

Comment SCAN and I'll send it over.
.
.
.
floor plan scanner app, floor plan scanner app free, how to 3d scan a building, how to 3d scan a house, 3d scan house interior, scan house to make floor plan, create a house plan from a scan, cost of 3d scanning a house, room layout estimation, floor plan ai app scan

#computervision #photogrammetry #3dscanning #opensourceproject #realestatetech

## Research

* Verdict: Partly valid. The resource is PolyLayout (ECCV 2026, Apache-2.0, 298 MiB weights, demo notebook), and it does optimize all rooms jointly. The post overstates it: it needs posed, undistorted images and sample datasets, not casual phone photos. It outputs Manhattan polygon layouts, not a finished 3D floor plan, and it isn't a Matterport replacement. The star count is now 195, not 165. The affiliations are unconfirmed.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [PolyLayout GitHub repo (github.com)](https://github.com/ghanning/PolyLayout): repo, found by search, verified, high confidence. Apache-2.0, ~298 MiB ScanNet++ checkpoint and demo notebook all match the caption.
* [PolyLayout: Multi-room Manhattan Layout Estimation (arXiv) (arxiv.org)](https://arxiv.org/abs/2608.03323): paper, found by search, verified, high confidence. Accepted at ECCV 2026. It optimizes all rooms jointly. Authors include Hanning, Pollefeys and Larsson, with Åström from Lund. Affiliations are not listed on the page.
* [PolyLayout project page (ghanning.github.io)](https://ghanning.github.io/PolyLayout): page, found by search, not opened, medium confidence. Linked from the arXiv page; not opened.

### Key steps

1. git clone https://github.com/ghanning/PolyLayout.git && cd PolyLayout
2. Create and activate a virtualenv: virtualenv venv && source venv/bin/activate
3. pip install -e . (use pip install -e .[extra] for the notebook)
4. Download the ScanNet++ fine-tuned checkpoint from the Google Drive link in the README
5. mkdir -p outputs/training && unzip polylayout_scannetpp_fine_tuned.zip -d outputs/training
6. Download the datasets (Aria Synthetic Environments, ScanNet++, 2D-3D-Semantics) into datasets/. Undistort the images, since only pinhole cameras are supported.
7. Open notebooks/demo_PolyLayout.ipynb, or run pixloc.run_PolyLayout --experiment polylayout_scannetpp_fine_tuned with a dataset config, --split and --output
8. Optionally add DeepLSD line segments to improve results

### Not found

The Microsoft and ETH Zurich affiliations are not shown on the arXiv page. The authors are consistent with ETH/Microsoft (Pollefeys) and Lund (Åström, Larsson, Hanning). No SCAN comment is needed because the repo is public. I did not open the project page.
