---
shortcode: "Dd18lXRDfrY"
url: "https://instagram.com/reel/Dd18lXRDfrY/"
type: "Reel"
author: "githubsignals"
shared: "Sep 30, 2026, 08:18 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Aha 3D: indoor video to Blender scene

A reel promoting Aha 3D, an open-source tool that turns an ordinary indoor video into an editable 3D scene in Blender, with people's motion placed into the room. The on-screen GitHub README shows the demo office, the requirements and the quick-start setup commands.

Written by claude-haiku-5-5.

## What it teaches

1. Requirements: a Linux workstation (Ubuntu or WSL2) with an NVIDIA GPU (24 GB class recommended), Python 3.11, Blender 5.2 for scene assembly and Blender 4.5 for skinning.
2. Clone and install the core environment: run git clone https://github.com/KevinXu02/aha-3d.git && cd aha-3d, export KIMODO_ENV="${KIMODO_ENV:-$PWD/.venv}", preview with bash tools/setup_core.sh --plan, then run bash tools/setup_core.sh.
3. Point the project at your Blender builds and model checkpoints: run source kimodo_blender/env.sh in every new shell, then run python tools/configure_runtime.py with --blender pointing to Blender 5.x, --skin-blender pointing to Blender 4.5, and the --kimodo and --checkpoint values.
4. Check the setup.

## Source

* Link: kevinxu02/aha-3d

## Caption

This tool can turn a normal indoor video into an editable 3D scene. 

Aha 3D takes a standard indoor video and turns it into a fully editable three-dimensional scene in Blender, which is honestly the kind of magic you expect from a sci-fi movie but actually works. The coolest part is that it doesn't just show you a static picture; it figures out where the people are moving and places them right back into the room. It then tweaks their feet so they land naturally on the floor and interact with objects without floating or sinking through tables. This is super useful for anyone who needs realistic motion capture data without expensive sensors or motion capture suits.

Open source: kevinxu02/aha-3d

Follow for more open source project drops.

#3DReconstruction #Blender3D #MotionCapture #AITools

## Research

* Verdict: Valid. The repo KevinXu02/aha-3d exists and does what the post says: it turns an indoor video into an editable Blender scene with people's motion placed in it. The README's current quick start differs from the reel's (a setup.sh installer with levels instead of setup_core.sh).
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [AHa-3D (KevinXu02/aha-3d) (github.com)](https://github.com/KevinXu02/aha-3d): repo, in the post, verified, high confidence. README describes rebuilding a room from indoor video, estimating people's motion and placing it in a Blender scene, with Linux/NVIDIA/Python 3.11/Blender requirements.

### Key steps

1. Use a Linux workstation (Ubuntu or WSL2) with an NVIDIA GPU and Python 3.11, plus Blender (and Blender 4.5 for skinning).
2. Clone https://github.com/KevinXu02/aha-3d and run `bash tools/setup.sh`. Add `--plan` to preview. Choose a level: static, human or robotics (`--level ...`).
3. Finish the level's setup: static needs Pi3X/SAM3 checkpoints and Blender; human adds PMPose, GVHMR and skinning; robotics adds Kimodo, G1 and text models.
4. Put your video under `references/`, run `bash tools/indoor intake`, then follow the scene workflow doc.
5. Verify with `python kimodo_blender/check_runtime.py --model g1` (G1 motion) and `python -m unittest discover -s tests -v`.

### Not found

I didn't check the post's claims about foot placement or object interaction against the repo, and I didn't look for the Blender 5.2 version or the configure_runtime.py steps shown in the reel. The README I fetched may be a newer version than the one in the reel.
