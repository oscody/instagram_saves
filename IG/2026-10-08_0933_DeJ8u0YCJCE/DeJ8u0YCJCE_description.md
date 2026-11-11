---
shortcode: "DeJ8u0YCJCE"
url: "https://instagram.com/reel/DeJ8u0YCJCE/"
type: "Reel"
author: "fominyu"
shared: "Oct 08, 2026, 09:33 AM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# Local video mocap tool v0.6 demo

The reel announces version 0.6 of a video mocap tool that runs on your own PC without third-party services or uploads. Three screens show it tracking one or two characters in a shot, staying accurate during fast rotation, and tracking fingers, with Maya viewport footage.

Written by claude-haiku-5-5.

## What it teaches

1. Drag your video files into the tool.
2. Press solve.

## Caption

Hello fellas, I've been working video mocap that work directly from your my on your PC. No third-party services, no need to upload your videos somewhere else. Drag N Drop and press solve!
What it can do atm:
-using 1 or 2 camera views-static or handled;
-tracking 1 or 2+ plus characters;
-tracking fingers;
-tracking camera position;
It's 0.6 version atm.

Please, support me if you want to see more updates :)

#animation #maya #mocap

## Research

* Verdict: Valid. The tool is Motivox Capture by Yuriy Fomin (@fominyu). His LinkedIn describes it as a local, markerless video mocap tool inside Maya, and a later post says it is now in Early Access. The post's claims match those descriptions, but I couldn't read the price or version on the Gumroad pages.
* Checked: 2026-11-10 by claude-opus-5-5

### Resources

* [Motivox Capture (Gumroad product page) (motivox.gumroad.com)](https://motivox.gumroad.com/l/motivox_capture): product, found by search, not opened, high confidence. The creator's LinkedIn post announcing Motivox Capture Early Access links here through lnkd.in/eut5QwVZ, which I followed. Only the title 'Motivox Capture' loaded, so I couldn't check the contents.
* [Motivox Capture System Check (free) (motivox.gumroad.com)](https://motivox.gumroad.com/l/MotivoxCaptureSystemCheck): tool, found by search, not opened, medium confidence. The creator's LinkedIn links here through lnkd.in/enFhXpXi as a free check of whether your PC can run the tool. Only the page title loaded.
* [Yuriy Fomin LinkedIn (creator profile) (uk.linkedin.com)](https://uk.linkedin.com/in/yufo): page, found by search, verified, high confidence. I opened it. It lists instagram.com/fominyu as his website and has posts on a local markerless mocap tool working directly in Maya (WHAM/GVHMR solvers) and the Motivox Capture Early Access release.

### Already in the vault

* Vault: `ZAIHub/Vault knowledge library/IG dead ends - other.md`: Only this post's dead-end entry from the earlier pass. No link or steps.

### Already in IG saves

* Similar: Web: [Free video-to-mocap tool for game animation (instagram.com)](https://instagram.com/p/DZiMW8cz_Jf/) (`DZiMW8cz_Jf`). P.I.N.O.C is another tool that turns video into animation, but it is upload-based.
* Similar: Web: [GVHMR: free 3D motion capture from video (instagram.com)](https://instagram.com/p/Dc8cexPGcVa/) (`Dc8cexPGcVa`). GVHMR, one of the models Fomin said he uses, does free 3D mocap from video.
* Similar: Web: [Mixamo LLM Mocap: Turning Video Into 3D Animation (instagram.com)](https://instagram.com/p/DcNOMyTCXmO/) (`DcNOMyTCXmO`). mixamo-llm-mocap turns video into Mixamo rig animation with GVHMR, including two-person scenes.
* Similar: Web: [EasyMocap: free markerless 3D motion capture tool (instagram.com)](https://instagram.com/p/DcnIzp_GQ9d/) (`DcnIzp_GQ9d`). EasyMocap does markerless body, hand and face mocap from RGB video, with one or more cameras.
* Similar: Web: [Free open-source webcam motion capture tool: FreeMoCap (instagram.com)](https://instagram.com/p/DdyQEqMGb2U/) (`DdyQEqMGb2U`). FreeMoCap is an open-source tool that does markerless 3D mocap from webcams on your own machine.
* Similar: Web: [Motion2MixamoRig: Animate 3D Characters From Video (instagram.com)](https://instagram.com/p/DeaOQ2bD9Zl/) (`DeaOQ2bD9Zl`). Motion2MixamoRig animates 3D characters from video.
* Similar: Web: [RGB MoCap: open-source video-to-3D animation tool (instagram.com)](https://instagram.com/p/DfBOLz3ClL6/) (`DfBOLz3ClL6`). RGB MoCap is a Windows app that turns ordinary video into 3D animation with local AI.

### Key steps

1. Run the free Motivox Capture System Check (motivox.gumroad.com/l/MotivoxCaptureSystemCheck) to see if your PC can run it. It needs an NVIDIA GPU, and RTX 50-series cards are not yet supported.
2. Get Motivox Capture (Early Access) from motivox.gumroad.com/l/motivox_capture.
3. Record your shot with a phone, using 1 or 2 camera views. Static cameras work best; the creator says a moving camera lowers accuracy.
4. In Maya, drag the video files into the tool and press solve. Processing takes a few minutes, depending on clip length.
5. The result is a skeleton or body animation in Maya (UE5 Mannequin), with fingers and camera position tracked.

### Not found

The Gumroad pages only loaded their titles, so I couldn't confirm the price, version, install steps, or whether the tool is the same v0.6 build shown in the reel. None of the 12 frames shows a tool name.
