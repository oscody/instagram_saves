---
shortcode: "DfBOLz3ClL6"
url: "https://instagram.com/reel/DfBOLz3ClL6/"
type: "Reel"
author: "githubsignals"
shared: "Oct 28, 2026, 12:22 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-28"
---

# RGB MoCap: open-source video-to-3D animation tool

Presents RGB MoCap, a native Windows app that uses local AI to turn standard video into editable 3D character animation. Screenshots show the app's interface, sample motion-capture clips, and character retargeting.

Written by claude-haiku-5-5.

## Source

* Link: toyxyz/toyxyz_rgbmocap

## Caption

RGB MoCap: Video to 3D Animation

Turn any standard video into clean, editable 3D character animation right on your own Windows machine. This tool uses local AI to track movement from plain footage, then lets you fix sliding feet and retarget that motion onto any game character model. You can export the final result as standard animation files for game engines or anime software without ever sending your data to a cloud server. It is a powerful, offline way to create high-quality motion capture data using just a computer and a camera. If you want to animate characters without expensive studio equipment, this project is your new creative toolkit.

Open source: toyxyz/toyxyz_rgbmocap

Follow for more open source project drops.

#MotionCapture #3DAnimation #CharacterAnimation #IndieGameDev

## Research

* Verdict: Valid. The repo exists and matches the post: a native Windows app that runs video mocap locally, reduces foot sliding, retargets to characters and exports FBX/BVH. The post leaves out the heavy requirements: an NVIDIA GPU and about 78 GB of disk.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [toyxyz/toyxyz_rgbmocap (RGB MoCap) (github.com)](https://github.com/toyxyz/toyxyz_rgbmocap): repo, in the post, verified, high confidence. Opened the repo. It is a native Windows video mocap app with local AI, foot-sliding reduction, retargeting to Mixamo/VRM/PMX, and MIT-licensed code.

### Key steps

1. You need 64-bit Windows, an NVIDIA GPU with a current driver, OpenGL 4.3, and about 78 GB free disk.
2. Install Git for Windows and clone the repo.
3. Run install.cmd to set up the base runtimes.
4. Run RGBMoCap.cmd and keep the console window open.
5. Open Model Manager and prepare the model files. Some need account registration or a manual download.
6. Optionally run Setup_MAMMA.cmd, Setup_PromptHMR.cmd, Setup_GEMX.cmd or Setup_SAM31.cmd for extra models.
7. Use File > Open Video, optionally Find person, then click Reconstruct 3D.
8. Fix foot and palm sliding, retarget to a Mixamo FBX, VRM or PMX character, then export FBX, BVH or VMD. Run update.cmd to update.
