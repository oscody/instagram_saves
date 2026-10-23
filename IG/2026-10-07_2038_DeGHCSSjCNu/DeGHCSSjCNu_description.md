---
shortcode: "DeGHCSSjCNu"
url: "https://instagram.com/reel/DeGHCSSjCNu/"
type: "Reel"
author: "githubsignals"
shared: "Oct 07, 2026, 08:38 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# Procedural Blender buildings in the browser with Three.js

The post scrolls through the GitHub README of ProceduralBuildingsThreeJS, a web configurator that ports Blender geometry-nodes building generators to the browser. It shows the French, New York and Chinese building styles with their sliders, balcony options, lighting set and procedural city backdrop.

Written by claude-haiku-5-5.

## Source

* Link: github.com/achrefelouafi/proceduralbuildingsthreejs

## Research

* Verdict: Valid. The GitHub repo exists and its README matches the post: French, New York and Chinese building styles, lighting, a procedural city and a GUI. It is MIT licensed and has a live demo.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [ProceduralBuildingsThreeJS (github.com)](https://github.com/achrefelouafi/proceduralbuildingsthreejs): repo, in the post, verified, high confidence. README describes a web configurator for procedural buildings ported from Blender geometry nodes, with French, New York and Chinese styles.
* [Live demo (proceduralbuildings.chirostudio.xyz)](https://proceduralbuildings.chirostudio.xyz): product, in the post, not opened, medium confidence. The README lists this as the live demo. I did not open it.

### Already in the vault

* Vault: `2. Areas/VR Work/opensource/repo - LinearAbiltyCastingThreeJS.md`: A different repo by the same author (achrefelouafi), a Three.js ability casting engine. It does not cover this repo.

### Key steps

1. Install Git LFS first. The Blender source files are about 380 MB. If you already cloned the repo, run `git lfs pull`.
2. Clone the repo.
3. Run `npm install`.
4. Run `npm run dev` and open the local URL.
5. Pick French, New York or Chinese from the building menu in the GUI, then adjust the sliders.
6. Try the lighting moods (Golden Hour, Blue Hour, Neon Night), camera presets, and rain or snow.
7. Optional: run `npm run verify`, `verify:nyc` or `verify:cn` to compare the browser output with Blender's geometry.

### Not found

The vault has no note on this repo. I did not open the live demo.
