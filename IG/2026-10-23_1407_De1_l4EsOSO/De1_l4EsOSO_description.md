---
shortcode: "De1_l4EsOSO"
url: "https://instagram.com/reel/De1_l4EsOSO/"
type: "Reel"
author: "marc.kaz"
shared: "Oct 23, 2026, 02:07 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-01"
---

# Turn iPhone LiDAR room scans into Three.js rooms

The post promotes "3D Model Anything," a project that captures a room with an iPhone LiDAR app and uses an agent skill to build an editable Three.js scene, checking objects against the photos. The video shows the resulting 3D room in a dollhouse-style viewer, with the speaker pointing at it and at the repo link.

Written by claude-haiku-5-5.

## Source

* Link: https://github.com/wesbos/3d-model-anything

## Caption

3D Model Anything captures a room on an iPhone, then an agent skill builds the scene and checks every object against the photo from the exact spot it was taken.

Ships with:
• iPhone LiDAR app plus hundreds of photos
• scan-to-threejs skill for your agent
• Editable Three.js rooms, not a mesh dump
• Dollhouse, walk, and wireframe viewer
• MIT. 600 stars. Runs in the browser

The model has to match the photo or it gets rebuilt.

👉 https://github.com/wesbos/3d-model-anything

## Research

* Verdict: Valid. The repo exists and matches the post: an iPhone LiDAR capture app, a scan-to-threejs agent skill and a Three.js viewer. The repo says the app isn't on the App Store yet and it isn't a one-click converter.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [wesbos/3d-model-anything (github.com)](https://github.com/wesbos/3d-model-anything): repo, in the post, verified, high confidence. The opened repo describes an iPhone LiDAR capture app, a scan-to-threejs skill and an editable Three.js viewer. Code and skill are MIT. It currently shows about 2.9k stars, where the post says 600.

### Key steps

1. Viewer: use Node 22.12+, run `npm ci` then `npm run dev`, and open http://localhost:5188.
2. Capture: build the iPhone app in Xcode (no App Store release yet; needs a LiDAR iPhone or iPad). Scan the room and export through the share sheet.
3. Extract the export into `data/captures-in/<room>/`.
4. Open the repo in an agent that supports local skills and ask it to use scan-to-threejs on your export. It needs Python 3 and Pillow. Optional depth reconstruction needs NumPy and Open3D.
5. Add the finished room under `demos/<id>/` and register it in `demos/index.ts`.
6. Keep your own scans private; only the office demo is meant to be distributed.
