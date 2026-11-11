---
shortcode: "Dd3rvh8sgln"
url: "https://instagram.com/reel/Dd3rvh8sgln/"
type: "Reel"
author: "rosamichael.digital"
shared: "Oct 01, 2026, 12:16 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Putting myself inside PS1 games with Blender

The creator shows himself placed inside PS1 levels such as Tekken 3 and Crash Bandicoot, with the footage filmed on a yellow-green screen. He asks viewers which PS1 game he should try next.

Written by claude-haiku-5-5.

## What it teaches

1. Rip a whole level from an original PS1 game using a special emulator.
2. Film yourself on a green screen.
3. Drop the footage into Blender so you appear inside the ripped level.

## Caption

Your favorite ps1 game?
I’m obsessed with the early 3D graphic and visuals.
Ps1 was ma first console ever. And it inspires me till today!

Now I found out you can rip whole levels from the original games thanks to the special emulator.

Tekken 3, Hercules and Crash were first.

Let me know what PS1 game I should try next.👇

## Research

* Verdict: Partly valid. The 'special emulator' is very likely scurest's DuckStation 3D-screenshot fork, which the same creator named in an earlier reel. The tool exists and does rip PS1 scenes into Blender, but it captures only the geometry in view at that moment, not the whole level file, and this reel never names it.
* Checked: 2026-11-10 by claude-opus-5-5

### Resources

* [scurest/duckstation-3D-Screenshot (github.com)](https://github.com/scurest/duckstation-3D-Screenshot): repo, in the vault, verified, medium confidence. The same creator's earlier reel DbqLB-zMoJR names 'duckstation with the 3D screenshot … on github', and this fork ('3D screenshots in DuckStation', topic model-ripper) is listed in the vault. In this reel, frame 5 shows a Blender object named 'shot_2026-09-23_22-22-42-394.001' with hash-named textures, which looks like an imported 3D capture.
* [VG Resource thread on ripping PS1 scenes with the DuckStation 3D screenshot build (vg-resource.com)](https://www.vg-resource.com/printthread.php?tid=36815): guide, found by search, not opened, low confidence. The search summary says it covers saving 3D screenshots to a screenshots_3d folder and cleaning up the capture in Blender. I didn't open it.

### Already in the vault

* Vault: `ZAIHub/ig repo to review.md`: Lists the scurest/duckstation-3D-Screenshot GitHub link twice, with no steps.
* Vault: `ZAIHub/Vault knowledge library/deadends/IG dead ends - other.md`: Logs this post (Dd3rvh8sgln) as a dead end, with the emulator not identified.

### Already in IG saves

* Same: Web: [Extracting PS1 3D models via 3D screenshot (instagram.com)](https://instagram.com/p/DbqLB-zMoJR/) (`DbqLB-zMoJR`). Same link: scurest/duckstation-3D-Screenshot.

### Key steps

1. Open github.com/scurest/duckstation-3D-Screenshot and switch to the feature/3d-screenshot branch.
2. Build it from source using upstream DuckStation's build instructions, since the fork has no releases.
3. Load the PS1 game with your own disc image and set Texture Mode to Full (as shown in the creator's earlier reel).
4. At the spot you want, take a 3D screenshot. It saves an .obj with textures to the screenshots_3D folder under DuckStation's screenshots folder.
5. Take several captures from different spots if you want more of the level, since each one only grabs the geometry in view.
6. Import the .obj files into Blender, line them up and delete stray geometry.
7. Film yourself against a green or yellow screen, key out the background, and put the footage on a plane in the Blender scene.
8. Render, then add a CRT/VHS look in compositing if you want.

### Not found

This reel never names the tool, and none of the 12 frames shows an emulator name, window title or URL. The link to the DuckStation fork comes from the same creator's earlier reel DbqLB-zMoJR. I didn't check the comments, and his Instagram bio (which links to rosamichael.com) doesn't mention the tool. The fork has no docs, so I couldn't confirm the .obj output or the 'shot_' file naming in the repo.
