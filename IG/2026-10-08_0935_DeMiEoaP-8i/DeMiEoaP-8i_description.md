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

## Research

* Verdict: Valid. The s-macke/VoxelSpace repo exists, is MIT licensed, and matches the post's description of the Comanche terrain technique in under 20 lines. One caveat: the Comanche height and colour maps are excluded from the MIT licence.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [s-macke/VoxelSpace (github.com)](https://github.com/s-macke/VoxelSpace): repo, in the post, verified, high confidence. README describes terrain rendering from Comanche (1992) in under 20 lines, with height and colour maps, MIT licence, and vertical-line drawing.

### Key steps

1. Open the repo and try the web demo to see the terrain render.
2. Keep two maps: a height map and a colour map with the shading already baked in (1024x1024, one byte each).
3. Clear the screen, then go through the depth steps from back to front (painter's algorithm).
4. At each depth, find the map line at that distance, allowing for field of view, and split it into one segment per screen column.
5. For each segment, read the height and colour from the maps.
6. Project the height to a screen y-position and draw a vertical line in that colour.
7. To speed it up, draw front to back with a y-buffer so you only draw what rises above the previous line, and use coarser steps at distance.
8. Check the licence: the code is MIT, but the Comanche maps are not covered by it, and the technique may be patented in some countries.

### Not found

The vault note that mentions this post only covers a caption-download fix, not the resource. The exact line count of the shipped code wasn't checked.
