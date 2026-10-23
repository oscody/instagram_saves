---
shortcode: "DbYwiDIM6Gh"
url: "https://instagram.com/reel/DbYwiDIM6Gh/"
type: "Reel"
author: "marc.kaz"
shared: "Jul 30, 2026, 08:12 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# SNOWFLOW: WebGPU snow demo built with Claude

A reel showing SNOWFLOW, a browser WebGPU snow demo with deformable snow, waterbending terrain spells, and snow-surfing wakes. The speaker says the developer built it in nine hours using about four million Claude Opus 5 tokens, starting from a full technical design document.

Written by claude-haiku-5-5.

## Source

* Link: https://github.com/Noniv/snowflow_demo

## Caption

SNOWFLOW is a browser demo with persistent deformable snow, waterbending spells that reshape terrain, and snow-surfing with dynamic wakes.

Ships with:
• Custom snow shaders (subsurface scattering, glints, compression)
• 90 FPS targets, zero allocations in the render loop
• Cloth, particles, atmospheric lighting

The crazy part: it started with a full technical design document, not a vague prompt. Visual quality was the product.

👉 https://github.com/Noniv/snowflow_demo

## Research

* Verdict: Partly valid. The repo exists and matches the described features (deformable snow, spells, snow-surf wake). The README says nothing about the nine hours, four million Opus tokens or the design document, so those claims come only from the reel.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [snowflow_demo (Noniv) (github.com)](https://github.com/Noniv/snowflow_demo): repo, in the post, verified, high confidence. README describes WebGPU/Babylon.js snow with persistent deformation, SSS shading, Verlet cloth, five spells and a snow-surf wake.
* [SNOWFLOW live demo (snowflow-lilac.vercel.app)](https://snowflow-lilac.vercel.app/): page, in the post, not opened, medium confidence. The demo URL is listed in the repo README, which I opened. I did not open the demo page itself.

### Already in the vault

* Vault: `2. Areas/Botstack/Pi/pi todo/plan - ig_automation pipeline by claude.md`: Only lists the post's shortcode and a caption snippet. It doesn't cover the resource.

### Key steps

1. Use a WebGPU-capable desktop browser: Chrome or Edge 113+, Firefox 141+, or Safari 26+. There is no WebGL fallback.
2. Clone https://github.com/Noniv/snowflow_demo.
3. Run npm install.
4. Run npm run dev and open localhost:5173.
5. Press F1 or the backtick key to open the live sliders and performance overlay.
6. Or try the hosted demo at https://snowflow-lilac.vercel.app/.

### Not found

The README doesn't confirm the nine hours, the four million Claude Opus 5 tokens, or a published technical design document. I did not open the live demo page or check the repo's src/ folder for a design doc.
