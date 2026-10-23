---
shortcode: "DbqLB-zMoJR"
url: "https://instagram.com/reel/DbqLB-zMoJR/"
type: "Reel"
author: "rosamichael.digital"
shared: "Sep 14, 2026, 08:04 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Extracting PS1 3D models via 3D screenshot

A reel showing a Gundam model being pulled from a PS1 game with DuckStation's 3D screenshot feature, then loaded into Blender and turned into a paper model. The caption says the special DuckStation build is on GitHub and that it works better than the Avocado emulator.

Written by claude-haiku-5-5.

## What it teaches

1. Get the special DuckStation build that includes the 3D screenshot feature (the caption says it is on GitHub and was flawless compared with Avocado PS1).
2. Run the PS1 game in DuckStation and take a 3D screenshot of the scene, with Texture Mode set to Full.
3. Find the saved .obj file in the screenshots_3D folder (the on-screen message shows the save path under DuckStation's screenshots folder).
4. Drag the last .obj file into Blender to see the model, including its position in the scene.
5. Convert the extracted model into a paper model (papercraft) so it can be printed and built.

## Caption

Turns out you can extract 3D models from almost any PS1 game using nothing more than a 3D screenshot.

In this reel, I’ll show you how it works and why it’s such a fun way to preserve and explore retro games.

Sou will need special version of duckstation with the 3D screenshot. You can find on github. Previously it worked only with Avocado ps1 emulator. But there was problems with vertices and textures. This duckstation version is flawless!

What’s the first PS1 game you’d rip a model from? 👇

#PS1 #PlayStation #RetroGaming #GameDev

## Research

* Verdict: Partly valid. A DuckStation fork for 3D screenshots exists on GitHub (scurest, topic "model-ripper"). Its page has no usage docs and no releases, so you'd have to build it, and I couldn't confirm the .obj output or the "flawless" claim.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [scurest/duckstation-3D-Screenshot (github.com)](https://github.com/scurest/duckstation-3D-Screenshot): repo, found by search, verified, medium confidence. Fork of stenzek/duckstation described as '3D screenshots in DuckStation', on the feature/3d-screenshot branch, topic model-ripper; README is only upstream's and the Releases section is empty.

### Already in the vault

* Vault: `ZAIHub/ig repo to review.md`: Lists the same scurest/duckstation-3D-Screenshot GitHub link (twice), with no steps.

### Key steps

1. Open the scurest/duckstation-3D-Screenshot repo and switch to the feature/3d-screenshot branch.
2. Build that branch from source, since the fork publishes no releases. Follow upstream DuckStation's build instructions.
3. Run the PS1 game and set Texture Mode to Full, as the reel shows.
4. Take a 3D screenshot. The reel says it saves a .obj file in the screenshots_3D folder under DuckStation's screenshots folder.
5. Drag the newest .obj into Blender to inspect the model and its textures.
6. Optionally unfold the model into a papercraft (the reel does this, but the tool isn't named).

### Not found

The reel itself wasn't watched. I couldn't confirm the .obj output, the screenshots_3D folder, the Texture Mode setting or the comparison with Avocado, because the fork's page has no usage docs. I also couldn't find prebuilt binaries or the papercraft tool used.
