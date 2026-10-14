---
shortcode: "DeMiEoaP-8i"
url: "https://instagram.com/reel/DeMiEoaP-8i/"
type: "Reel"
author: "index.opensource"
shared: "Oct 08, 2026, 09:35 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# VoxelSpace: Rebuilding Comanche's 1992 Terrain Trick

A reel introducing VoxelSpace, an MIT-licensed open-source project that rebuilds the voxel-space terrain technique from the 1992 game Comanche in under 20 lines. It shows the renderer drawing mountains as vertical coloured lines and the license terms.

Written by claude-haiku-5-5.

## What it teaches

1. Store the world as two images: a height map and a colour map with light and shadow already painted in.
2. Look out from the camera one horizontal line at a time.
3. On each line, pick one map point for every column of the screen (the on-screen example uses 800 points per line, a 90° view, and distance 800).
4. Project each point's height onto the screen and draw it as a vertical line in that point's colour.
5. Work from near to far and draw only the part of each vertical line that rises above what is already drawn.
6. Step farther points in larger increments so distant hills cost less to draw.
7. No polygons are needed, only vertical lines.
8. The code is MIT licensed: you may use, change, and sell it, as long as you keep the copyright and license notice.

## Source

* Link: s-macke/VoxelSpace
