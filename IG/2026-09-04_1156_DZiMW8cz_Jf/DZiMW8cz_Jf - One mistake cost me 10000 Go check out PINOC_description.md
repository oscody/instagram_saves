---
shortcode: "DZiMW8cz_Jf"
url: "https://instagram.com/reel/DZiMW8cz_Jf/"
type: "Reel"
author: "jerron_jacques"
shared: "Sep 04, 2026, 11:56 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Free video-to-mocap tool for game animation

A solo game developer describes spending $10,000 on a motion capture suit for his game, then says a free tool called P.I.N.O.C lets him turn an uploaded video into game-ready animation. He urges game developers and animators to try it.

Written by claude-haiku-5-5.

## What it teaches

1. Upload a video of the movement you want.
2. Export the resulting animation as FBX.
3. Add the FBX animation to your game.

## Caption

One mistake cost me $10,000! Go check out P.I.N.O.C @viggle_ai 

#Erased #GameDev #indiegames #MotionCapture #Animation

## Research

* Verdict: Partly valid. PINOC is a real Viggle tool that turns video into FBX/GLB animation. But the free tier is only 60 credits (about 60 seconds) and is non-commercial, so "free" is limited for game use.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Viggle PINOC (viggle.ai)](https://viggle.ai/pinoc): tool, found by search, verified, high confidence. Official page describes video-to-3D motion, FBX/GLB export on a 65-bone Mixamo-style rig, and 60 free credits.
* [Viggle docs: mocap quickstart (docs.viggle.ai)](https://docs.viggle.ai/v1/guides/quickstart-mocap.md): guide, found by search, not opened, medium confidence. Search result describes an API flow that uploads a motion video and downloads the FBX. I did not open it.

### Key steps

1. Open viggle.ai/pinoc and sign up. The free tier gives 60 credits with no card.
2. Upload a clip with one subject and clear movement, or type a text prompt. Motion costs 1 credit per second.
3. Preview the generated motion on a 3D character and keep the take you like.
4. Export as FBX (or GLB). The skeleton has 65 bones with Mixamo-style names.
5. Import the file into Unity, Unreal, Blender or Maya.
6. Free accounts are non-commercial only. Paid plans start at $12.99/month for 300 credits.

### Not found

The vault has no note on this post. Its grep hits for viggle/PINOC were in three ZAIHub files, which I did not read. One search result said FBX export was "coming soon" on the game-dev page, but the main PINOC page lists FBX. I did not open the API docs.
