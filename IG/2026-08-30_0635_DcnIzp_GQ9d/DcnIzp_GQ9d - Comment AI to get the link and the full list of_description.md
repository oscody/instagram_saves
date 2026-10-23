---
shortcode: "DcnIzp_GQ9d"
url: "https://instagram.com/p/DcnIzp_GQ9d/"
type: "Carousel"
author: "simplifyinai"
shared: "Aug 30, 2026, 06:35 AM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# EasyMocap: free markerless 3D motion capture tool

The post introduces EasyMocap, an open-source toolbox from Zhejiang University that estimates 3D body, hand, and face pose from regular RGB video, including YouTube footage. It shows a figure skating clip alongside the tool's README and feature list.

Written by claude-haiku-5-5.

## Source

* Link: EasyMocap
* How to get it: Comment 'AI' on the post; the full list of free AI resources is sent via DM

## Caption

Comment “AI” to get the link and the full list of free AI resources.

Motion capture used to need marker suits and a studio. This tool just needs a YouTube video.

It’s called EasyMocap, built by Zhejiang University’s 3D vision lab.

A handful of well-known 3D human research projects, HumanNeRF, Neural Body, KeypointNeRF, all lean on this same toolbox underneath.

→ Estimates full 3D body, hand, and face pose straight from regular RGB video, no marker suits or specialized rigs

→ Works even on footage pulled straight from YouTube

→ Fits the same SMPL body models researchers already use, so results plug into existing pipelines

One thing to know: last major release was 2021, and it depends on SMPL models that carry their own non-commercial academic license, worth checking before using this beyond research.

Open Source.

## Research

* Verdict: Partly valid. EasyMocap is real and public on GitHub, and it supports fitting SMPL to a single internet video. The post leaves out that its best results need multiple calibrated cameras. The repo's last dated update is Nov 2022, not 2021 as the post says.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [EasyMocap (zju3dv) (github.com)](https://github.com/zju3dv/EasyMocap): repo, found by search, verified, high confidence. Opened it: the repo from Zhejiang University's zju3dv group does markerless mocap with SMPL, SMPL-X and MANO from RGB video, including single internet video.
* [EasyMocap quickstart (github.com)](https://github.com/zju3dv/EasyMocap/blob/master/doc/quickstart.md): guide, found by search, verified, high confidence. Opened it: it has the install prerequisite and demo commands. It covers multi-view data, not the single-video demo.

### Already in the vault

* Vault: `ZAIHub/ig repo to review.md`: Holds the bare GitHub link https://github.com/zju3dv/EasyMocap in a list of repos to review. It has no steps.

### Key steps

1. Install EasyMocap by following the installation doc in the repo. You also need to download the SMPL models separately, and they carry a non-commercial license.
2. Put your videos in a data folder. For multi-view, add a videos/ folder plus intri.yml and extri.yml camera files.
3. Extract frames and keypoints: python3 scripts/preprocess/extract_video.py ${data} --handface. Add --openpose <path> when running on your own data.
4. Run the multi-view SMPL fit: python3 apps/demo/mv1p.py ${data} --out ${data}/output/smpl --vis_det --vis_repro --undis --vis_smpl.
5. For SMPL-X with hands and face, add --body bodyhandface --model smplx --gender male.
6. For a single YouTube-style video, use the repo's 'Internet video' docs. The quickstart doesn't cover that demo, and the Colab notebook linked from the README may help.

### Not found

The post's DM list of free AI resources was not checked. The repo's license name and the single-video commands weren't shown in the pages I opened. The 'last major release 2021' claim doesn't match the README, whose newest dated entry is 11/03/2022.
