---
shortcode: "DdIc2jHAZp9"
url: "https://instagram.com/reel/DdIc2jHAZp9/"
type: "Reel"
author: "githubsignals"
shared: "Sep 11, 2026, 11:02 AM"
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

## On screen text

github.omaldegadspriegen
C
sprite-gen
motion loops.
SPRITEGEN
NESTILAWHOLESPRITEST
one base image
row byrow.locks the character's
drives genera
ne-readable
Start with a request
@GithubSignals
curation view is optiong
arate sprite and
aveyour
ubegaspre
ogithub.oaldeedpriger
README
Apache-2.0 license
Security
tion lo
PRITEGEN
ONESTILAWHOLESPRITESET.
, poses that
thafw
verlap and
anifest.json.fram
e
Eu inelinec n
github.omaldegadspriteg
RIEHE
whose facechanges every fram
Cute demo, useless asset.
Ine atawhamachnereadabe
ean transparen rame and bakes
efaults.
Four pipelines, one CLI
tegenherp prints this
