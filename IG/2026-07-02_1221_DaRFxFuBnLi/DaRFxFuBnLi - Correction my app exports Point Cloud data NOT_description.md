---
shortcode: "DaRFxFuBnLi"
url: "https://instagram.com/reel/DaRFxFuBnLi/"
type: "Reel"
author: "donalleniii"
shared: "Jul 02, 2026, 12:21 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Correction: Lingbot Studio exports point clouds, not splats

The creator corrects an earlier claim: their Mac app exports point cloud data rather than Gaussian splats, and they have open sourced it. Screen captures show the Lingbot Studio interface with its "Save Point Cloud" and "Save Splat" buttons, and a point cloud imported into Blender.

Written by claude-haiku-5-5.

## What it teaches

1. Import your footage into the app
2. Generate the scene locally on a MacBook Pro instead of using the cloud
3. Save the result as a PLY file
4. Bring the PLY into 3D tools such as Blender or After Effects

## Source

* Link: https://github.com/donalleniii/lingbot-desktop-mac

## Caption

⚠️Correction: my app exports Point Cloud data NOT Gaussian Splats 

Open sourced it 💕 https://github.com/donalleniii/lingbot-desktop-mac

## Research

* Verdict: Valid. The repo exists and says the app exports a point cloud PLY. Its splat-format PLY is only converted from that point cloud, so the correction holds.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [lingbot-desktop-mac (github.com)](https://github.com/donalleniii/lingbot-desktop-mac): repo, in the post, verified, high confidence. The README describes a local Apple Silicon Mac app for Lingbot-Map with point cloud and splat-format PLY export, matching the post.
* [lingbot-map (upstream model) (github.com)](https://github.com/robbyant/lingbot-map): repo, in the vault, not opened, medium confidence. The vault note 'ig repo to review' lists it. The desktop app wraps Lingbot-Map, but I did not open this link.

### Already in the vault

* Vault: `ZAIHub/ig repo to review.md`: Lists the upstream robbyant/lingbot-map repo, not the Mac app.

### Key steps

1. Requirements: Apple Silicon Mac, Homebrew with ffmpeg, Python 3.10 (uv recommended), and about 4.6 GB of disk for the model checkpoint.
2. Install with the one-line curl installer in the README, or manually: clone the repo, create a Python 3.10 venv, install the pinned dependencies, clone Lingbot-Map at the pinned commit, apply the patch, and download the checkpoint and check its sha256.
3. Run ./launch.command, which opens http://localhost:8000.
4. Drop in a video and check the time estimate. Then click Create 3D Scene.
5. Explore the result in the viewer. Use Save Point Cloud for a PLY, or Save Splat for a splat-format PLY.
6. Import the PLY into Blender or After Effects.
7. Tips: move the camera through the scene and avoid pure rotations in place. Processing runs at about 0.3 to 1 frame per second.
8. Check the model weights licence before commercial use. The README says the lineage includes VGGT, which is non-commercial.

### Not found

I did not open the upstream lingbot-map repo or test the app.
