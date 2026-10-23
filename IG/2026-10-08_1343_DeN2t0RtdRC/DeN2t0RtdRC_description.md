---
shortcode: "DeN2t0RtdRC"
url: "https://instagram.com/reel/DeN2t0RtdRC/"
type: "Reel"
author: "index.opensource"
shared: "Oct 08, 2026, 01:43 PM"
transcribed_by: "faster-whisper base"
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

## Research

* Verdict: Valid. SpaceshipGenerator is a real MIT-licensed Blender add-on by Michael Davies, and it makes seeded, reproducible ships. I couldn't confirm the "ships are CC BY" claim from the repo page.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [a1studmuffin/SpaceshipGenerator (github.com)](https://github.com/a1studmuffin/SpaceshipGenerator): repo, found by search, verified, high confidence. Blender script that builds ships procedurally from a seed, MIT licensed, with seed reproducibility as in the post.

### Key steps

1. Install Blender 2.80 or later.
2. Download the newest add_mesh_SpaceshipGenerator.zip from the repo's Releases.
3. In Blender: Edit > Preferences > Add-ons > Install, and pick the zip.
4. Enable "Add Mesh: Spaceship Generator".
5. Add a ship with Add > Mesh > Spaceship in the 3D View.
6. Adjust settings in the Spaceship panel at the bottom-left of the viewport.
7. For a repeatable ship in the script, call generate_spaceship('yourseed').
8. The script deletes existing objects named Spaceship* by default. Comment out reset_scene() to stop that.

### Not found

The repo page says nothing about CC BY for generated ships (point 10 of the post). Only the MIT license is named there. I did not check the other repo files.
