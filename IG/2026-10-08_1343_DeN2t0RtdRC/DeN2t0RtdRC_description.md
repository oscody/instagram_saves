---
shortcode: "DeN2t0RtdRC"
url: "https://instagram.com/reel/DeN2t0RtdRC/"
type: "Reel"
author: "index.opensource"
shared: "Oct 08, 2026, 01:43 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# SpaceshipGenerator: grows ships from a single box

The post introduces the open-source SpaceshipGenerator project, which builds spaceships procedurally from a single box and a seed word. It shows the generator's build steps, a code excerpt for random face extrusion, and the MIT license text.

Written by claude-haiku-5-5.

## What it teaches

1. Start from a single box.
2. Push the front and back faces outward repeatedly, tilting and resizing at each step.
3. Extrude a few random faces, with each extrusion smaller than the last (the code applies this only to faces with an aspect ratio of 4 or less, and only on a random chance).
4. Maybe scale the extruded faces.
5. Attach parts based on the direction each face points: engines at the back, antennas on top, turrets on the sides, glowing discs below.
6. Half the time, mirror one side of the ship onto the other.
7. Finish with a bevel and texture.
8. The same seed word always produces the same ship.
9. Under the MIT license, you may use, change, and share the code, but you must keep the copyright notice.
10. Ships made with the generator are CC BY, so credit the author.

## Source

* Link: SpaceshipGenerator

## On screen text

SpaceshipGenerator
Todays opensource project
grows them froma single box:
one ship, step by step
a few faces stick out
Thenaw randomfaces stik out
smaller each time.
br
591
get aspectatioface4
ontinue
59
in..
jace
# Maybe apply Some scaling
uniform(1.1,1.5)
ceceb,ce,,s
602
paceship_generator.py
paceshipenetorEN
Fle0140
da3yearsao
8 Lines (29 loc  1.69 KB
CodeBlame
he MT License MIT
ranted, f
free of charge
right
use it, change it,share i
keep the notice.
O.
camera, starsi ours
