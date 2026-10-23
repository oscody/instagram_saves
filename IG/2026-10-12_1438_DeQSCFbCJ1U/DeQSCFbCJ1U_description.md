---
shortcode: "DeQSCFbCJ1U"
url: "https://instagram.com/reel/DeQSCFbCJ1U/"
type: "Reel"
author: "stridejosh.ai"
shared: "Oct 12, 2026, 02:38 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# Caustic Volume: browser water caustics demo

Shows Caustic Volume, a free browser water-caustics demo built on three.js, with its sandbox mode and excerpts from its README on downloading and running it.

Written by claude-haiku-5-5.

## What it teaches

1. Get the project from the repo: on the repository page, choose Code, then Download ZIP, and extract it.
2. Open lite/index.html in your browser. No package install or build command is needed; three.js loads from a CDN on the first connected visit.
3. If the browser works better with a local HTTP address, run python3 -m http.server from the extracted folder, then open http://localhost:8000 and navigate to Lite. On Windows, use the Python command if python3 isn't available. Keep the terminal open while using it and stop the server when finished.
4. Lite can switch to a CPU renderer when WebGL 2 or the library is unavailable.
5. Controls: on a computer, D produces a random ripple, Space pauses, and H hides the panel. Phone users can use the visible controls.
6. Use the sandbox only if you need it. It adds buoyant objects, creatures, ink, falling sand, multiple lamps and a laser, and expects more capable graphics hardware and WebGL 2. Start with its default Medium quality and change one feature at a time.
7. If it struggles, return to Lite, close other heavy tabs, and check whether hardware acceleration is enabled.

## Source

* Link: github.com/ScottieFox/caustic-volume
* How to get it: An extra free guide is offered by commenting RIPPLE; the repo link is public in the post.

## Caption

Comment RIPPLE and I'll send you my free guide: how to open the Lite simulator, control its light and waves, and run the one-file version locally.

This whole water tank, the waves, the rubber duck and the light dancing on the floor, is one free file running in your browser. No install, and under a thousand lines of code.

It's called Caustic Volume. Crank up the waves and the floor lights up like the bottom of a real pool. Switch to the lamp for a night scene. The bigger sandbox adds creatures, ink and even a laser.

The catch: the sandbox wants a strong graphics card, so start with Lite. Lite has a CPU fallback.

Repo: github.com/ScottieFox/caustic-volume

Follow for more AI.

#AI #OpenSource #ClaudeCode #AITools #Tech

## Research

* Verdict: Valid. The public GitHub repo matches the post: a three.js water-caustics demo with a Lite file of about 990 lines, a sandbox, and a CPU fallback. One control is wrong in the post: the README maps D to the duck and R to a random ripple.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [ScottieFox/caustic-volume (github.com)](https://github.com/ScottieFox/caustic-volume): repo, in the post, verified, high confidence. README describes Lite (about 990 lines), the sandbox with creatures, ink, sand, lamps and a laser, and the CPU fallback, as in the post.

### Already in the vault

* Vault: `ZAIHub/search - competition  ideas by codex.md`: Lists the post and repo as a desktop graphics reference for spatial light; says Quest XR performance was not established.

### Key steps

1. Download the ZIP from the repo (Code > Download ZIP) or clone it, then extract it.
2. Open lite/index.html in a browser. The first load needs internet to fetch three.js r186 from jsDelivr, and the browser caches it afterward.
3. Or run python3 -m http.server in the repo folder and open http://localhost:8000.
4. Lite controls: drag to orbit, scroll or pinch to zoom, click the water for a ripple. Keys: L toggles sun/lamp, D shows the duck, R makes a random ripple, Space pauses, H hides the panel. The post says D makes a ripple, but the README says R.
5. Add ?cpu to the URL to force the CPU renderer. Lite also switches to it on its own if WebGL 2 or three.js is unavailable.
6. Try sandbox/index.html only on a capable GPU. It needs WebGL 2 with EXT_color_buffer_float.

### Not found

The free RIPPLE guide is sent only after a comment, and I found no public copy. The repo README covers the same material.
