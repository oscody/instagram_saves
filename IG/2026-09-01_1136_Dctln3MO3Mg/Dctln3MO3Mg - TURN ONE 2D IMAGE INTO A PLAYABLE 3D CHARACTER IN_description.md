---
shortcode: "Dctln3MO3Mg"
url: "https://instagram.com/reel/Dctln3MO3Mg/"
type: "Reel"
author: "marc.kaz"
shared: "Sep 01, 2026, 11:36 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Turning a 2D image into an animated 3D boxer

The reel showcases a browser tool that reconstructs a 2D image as a rigged 3D character with boxing animations such as jab, hook, ring walk and defeat, plus explode-part and physics effects. The creator talks over the demo and calls it a fun way to animate a picture.

Written by claude-haiku-5-5.

## Source

* Link: https://github.com/img2threejs/img2threejs

## Caption

🚨 TURN ONE 2D IMAGE INTO A PLAYABLE 3D CHARACTER IN THE BROWSER

img2threejs reconstructs, rigs, animates, and drops the result into a Three.js scene as pure TypeScript.

Ships with:
• Image → 3D reconstruction → rig → animation loops
• Physics VFX and 360° orbit
• No Blender. No traditional 3D pipeline
• Output is inspectable Three.js + TypeScript code

Image in. Interactive WebGL out.

👉 https://github.com/img2threejs/img2threejs

Who’s turning photos into 3D scenes today? Drop a 🔥

## Research

* Verdict: Partly valid. The repo exists and makes Three.js TypeScript models from a reference image. It runs as an AI-agent skill, not a standalone browser tool. The README lists auto rigging and skin weights as planned, so "image → rig → animation" is overstated.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [img2threejs (github.com)](https://github.com/img2threejs/img2threejs): repo, in the post, verified, high confidence. The README describes a code-only, procedural, animation-ready Three.js model rebuilt from a reference image. It is Apache-2.0 with a character track.

### Already in the vault

* Vault: `ZAIHub/ig repo to review.md`: Has the repo link, marked done on 2026-09-19. It includes a one-line summary and a ChatGPT research link. It also lists related tools: kimodo.cpp, GVHMR, mixamo-llm-mocap and WorldClaw.

### Key steps

1. Install Node.js 18 or newer, Git and Python 3.10 or newer.
2. Run: npx --yes img2threejs@latest install
3. Run: npx --yes img2threejs@latest doctor to check the setup.
4. Hermes users also symlink the skill into their profile, as described in the README.
5. Restart your agent (e.g. Claude Code).
6. Attach a reference image and run /img2threejs with your request.
7. Optionally install plugins such as `character` through the img2 harness. It rigs and animates from a GLB skeleton.

### Not found

I did not find the exact reel demo (boxer with jab, hook and defeat animations) in the repo. I did not confirm the "in the browser" claim, since the README describes an agent-skill workflow.
