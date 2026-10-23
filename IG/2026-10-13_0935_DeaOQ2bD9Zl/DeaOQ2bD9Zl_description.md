---
shortcode: "DeaOQ2bD9Zl"
url: "https://instagram.com/reel/DeaOQ2bD9Zl/"
type: "Reel"
author: "githubsignals"
shared: "Oct 13, 2026, 09:35 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# Motion2MixamoRig: Animate 3D Characters From Video

A reel presenting the open-source Motion2MixamoRig tool, which transfers a person's movement from a video, or a pose from a still photo, onto an Adobe Mixamo-rigged 3D character. It shows the project's GitHub README and demo clips.

Written by claude-haiku-5-5.

## Source

* Link: maxliu22/motion2mixamorig

## Caption

Motion2MixamoRig: Animate 3D Characters From Video

Motion2MixamoRig is the motion capture tool that turns ordinary video clips into professional character animations without a motion lab. It watches a single person moving on camera and calculates their exact body pose frame by frame. The software then transfers those movements onto a three-dimensional character model you can download from Adobe Mixamo. This means you can make a digital robot or superhero dance by simply recording yourself on a phone. The tool even works with still photos to create static poses. It is a powerful way for independent creators to bring characters to life using just a camera and a computer.

Open source: maxliu22/motion2mixamorig

Follow for more open source project drops.

#3DAnimation #MotionCapture #Mixamo #IndieAnimation

## Research

* Verdict: Partly valid. The repo exists and does what the post says. The post leaves out that it is experimental, needs a free SMPL-X registration and a Mixamo character, and downloads about 5 GB of weights. SMPL-X is non-commercial by default.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [maxliu22/motion2mixamorig (github.com)](https://github.com/maxliu22/motion2mixamorig): repo, in the post, verified, high confidence. The README describes transferring video or still-photo pose onto a Mixamo-rigged character and exporting a .glb, as in the post.

### Key steps

1. Needs Python 3.11+ or Blender 4.2+, and ffmpeg is recommended.
2. Register to get SMPL-X (SMPLX_NEUTRAL.npz) and download a Mixamo FBX such as Y Bot with an Adobe account.
3. CLI: clone the repo, make a venv, then install numpy>=1.26, then chumpy==0.70 with --no-build-isolation, then pip install -e .
4. Put SMPLX_NEUTRAL.npz in assets/body_models/smplx/, the FBX in assets/mixamo/Y_Bot.fbx, and the clip in assets/video/.
5. Run `m2mr doctor` to check the setup, then `m2mr run`. Use --video, --image, --rig or --skeleton as needed.
6. Output goes to outputs/<timestamp>_<source>/ and includes a preview and a skinned .glb for Blender or Unity.
7. Blender route: install the release zip via Edit > Preferences > Get Extensions > Install from Disk. Then open the N-panel Motion2MixamoRig tab, click Install Runtime, pick the SMPL-X model, FBX and video, and click Generate Motion.
8. The clip must show exactly one person, head to toe. On CPU, a 30-second clip takes about 8–15 minutes.
