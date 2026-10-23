---
shortcode: "Db5t4WOjF4Q"
url: "https://instagram.com/p/Db5t4WOjF4Q/"
type: "Carousel"
author: "activeprogrammer"
shared: "Aug 12, 2026, 09:23 AM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Open-source elemental VFX playground in Three.js

The carousel shows an open-source browser VFX playground built with Three.js, with six elemental abilities (frost lance, storm lance, cinder fall, nova beam, voltaic snare, glacial crown) rendered in real time. A flaming meteor-style fire ability is shown on a dark plain, with the playground's control panel and ability bar on screen.

Written by claude-haiku-5-5.

## Source

* Link: https://github.com/achrefelouafi/LinearAbiltyCastingThreeJS

## Caption

A developer built an open-source elemental VFX playground that runs directly in your browser using Three.js. ⚡🔥❄️

It includes six fully customizable abilities—and everything is generated in real time.

No textures.
No sprite sheets.
No baked meshes.

Just hand-written GLSL shaders and GPU-simulated particles showing what modern browser graphics can do.

Explore the source code:
https://github.com/achrefelouafi/LinearAbiltyCastingThreeJS

Which ability would you try first: fire, ice, or lightning? 👇

Credit: chirovisuals on X

Follow @activeprogrammer for more programming and tech discoveries.

#threejs #webgl #javascript #programming #opensource

## Research

* Verdict: Partly valid. The repo exists and matches the post: six abilities, hand-written GLSL, GPU particles and a live editor. The "no textures, no baked meshes" claim is slightly overstated, because it bundles a character FBX with textures and an HDR probe. The README license text is ambiguous (MIT in the sidebar, "as-is" in the README).
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [LinearAbiltyCastingThreeJS (Elemental Sandbox) (github.com)](https://github.com/achrefelouafi/LinearAbiltyCastingThreeJS): repo, in the post, verified, high confidence. README lists the same six abilities (Frost Lance, Storm Lance, Cinder Fall, Nova Beam, Voltaic Snare, Glacial Crown) built with Three.js, GLSL and GPU particles.
* [LinearAbilityCastingIWSDK (VR port) (github.com)](https://github.com/oscody/LinearAbilityCastingIWSDK): repo, in the vault, not opened, medium confidence. Linked in the user's vault note as an Immersive Web SDK version; I did not open it.

### Already in the vault

* Vault: `2. Areas/VR Work/opensource/repo - LinearAbiltyCastingThreeJS.md`: Repo link and the IWSDK port link, with a local bench URL.
* Vault: `ZAIHub/ig repo to review.md`: Repo link and local clone path /Users/bogle/Dev/VR/open_source/LinearAbiltyCastingThreeJS.
* Vault: `ZAIHub/search - competition ideas by claude.md`: Lists this post as a source of VFX ideas for turrets and alien deaths in RTSVR.

### Key steps

1. Clone the repo and run npm install.
2. Run npm run dev and open the URL Vite prints (default http://127.0.0.1:5173).
3. Cast abilities with Q/E/R/F/V/X or keys 1-6. Aim with the mouse and left click to fire.
4. Press G to open the lil-gui editor (about 938 sliders). Presets save to localStorage.
5. Press P to pause while editing.
6. Run npm run build and npm run preview for a production build.
7. Check the licenses before reuse: the bundled character FBX and HDR probe keep their own licenses.

### Not found

I did not open the IWSDK port repo. I did not check the original X post by chirovisuals.
