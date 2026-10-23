---
shortcode: "DdIc2jHAZp9"
url: "https://instagram.com/reel/DdIc2jHAZp9/"
type: "Reel"
author: "githubsignals"
shared: "Sep 11, 2026, 11:02 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# sprite-gen: one drawing to game sprites

The post shows the README of the open-source sprite-gen project, which turns one character drawing into game-ready sprite atlases or transparent motion loops. It describes the tool's pipeline on screen with a demo of a knight, a wolf, and a slime.

Written by claude-haiku-5-5.

## What it teaches

1. Start with one base image of the character.
2. Ask for sprites or an image; the agent checks access, asks only for missing provider or motion choices, runs the pipeline, and delivers the files.
3. The tool drives generation row by row and locks the character's identity.
4. It strips the chroma background to real alpha transparency.
5. It extracts each pose as a clean transparent frame.
6. It bakes a runtime atlas with a machine-readable manifest.json frame_layout, or you can give the same still to a video model to get a seamless transparent loop per motion state.
7. Optionally use the curation webview to compare, reject, nudge, and watch the loop live before baking.
8. Save your choices once to reuse them as sprite and image defaults; a one-off request does not overwrite them.

## Source

* Link: aldegad/sprite-gen

## Caption

Give this tool one character image, and it turns it into usable animated game sprites. 

Transform a single static drawing into polished, game-ready character sprites that actually work in your engine. Traditional AI image generation often produces messy sheets with shifting faces and backgrounds that are impossible to remove cleanly, leaving developers with unusable files. This tool fixes that by taking one base image and processing it step by step to lock the character’s identity and strip away the background into true transparency. The most surprising feature is its ability to turn that still image into seamless, animated motion loops, giving your character a living idle state without needing to animate every frame by hand.

Open source: aldegad/sprite-gen

Follow for more open source project drops.

#GameDev #IndieDev #PixelArt #SpriteAnimation #AIArt

## Research

* Verdict: Valid. The aldegad/sprite-gen repo exists and matches the post. It turns one base image into transparent sprite atlases with a manifest, or into video-based transparent loops, and it has a curation webview and saved defaults.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [aldegad/sprite-gen (github.com)](https://github.com/aldegad/sprite-gen): repo, in the post, verified, high confidence. The README describes the atlas-rows and video-to-loop pipelines, manifest.json frame layout, curation webview and saved defaults, all as shown in the post.

### Key steps

1. Create a Python 3.11+ virtualenv and run `pip install -e .` in the cloned repo; run `sprite-gen --help` to see the commands.
2. Or install it as a Codex/Claude skill with the repo's install-skill-from-github.py script.
3. Choose a provider: codex or grok use existing subscription logins, while openai needs OPENAI_API_KEY and bills per call.
4. Atlas flow: run `prepare`, then `gen-set`, `extract` and `compose-atlas`. This produces sprite-sheet-alpha.png and manifest.json.
5. Optionally run `sprite-gen curation --run-dir <run>` to compare, reject and nudge frames and preview loops before baking.
6. Loop flow: animate the still with a video model, then cut it into transparent GIF, WebP or strip loops. This needs ffmpeg and img2webp.
7. Save defaults once with `sprite-gen defaults save ...`, for example `--codex-unavailable grok|openai`. One-off requests don't overwrite them.

### Not found

The vault has no notes on this tool. I did not check the demo images (knight, wolf, slime) or the output quality.
