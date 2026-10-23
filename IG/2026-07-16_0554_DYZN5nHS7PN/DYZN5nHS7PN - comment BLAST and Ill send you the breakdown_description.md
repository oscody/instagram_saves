---
shortcode: "DYZN5nHS7PN"
url: "https://instagram.com/reel/DYZN5nHS7PN/"
type: "Reel"
author: "nicnonac"
shared: "Jul 16, 2026, 05:54 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Image-blaster: photo to 3D world toolkit

A reel promoting an open-source Claude Code toolkit called image-blaster, which the speaker says turns a single image into an explorable 3D environment with meshes, physics, lighting and audio. On-screen clips show a cabin and a workshop rendered as 3D scenes with wireframe props.

Written by claude-haiku-5-5.

## Source

* Link: image-blaster
* How to get it: comment BLAST on the post; the breakdown and repo details are sent by DM

## Caption

comment "BLAST" and I'll send you the breakdown 👇

today an entire industry stopped making sense.

a guy posted a repo on github that turns any photo into an explorable 3d world. meshes with physics. background splats. ambient audio. everything.

an image goes in. a world comes out. five minutes.

the people who spent ten years learning blender have been staring at this in silence all day.

it's called image-blaster. neilsonnn published it as a claude code skillset that fans out across world labs marble for the room and hunyuan 3d via fal for the props, with elevenlabs sfx baked in for audio.

what it actually kills:

🧱 the greybox week. the splat is the blockout.

🪑 the prop pass. ten objects, glb meshes, around $1 in api calls.

🔊 the foley pass. ambient loop plus per-object physics sfx generated alongside the meshes.

📦 the quixel cart. every prop matches because every prop is sampled from the same source image.

the catch: it's a first-pass tool, not the shipping pipeline. you still bring in an artist for hero assets and anything that needs to be rigged.

Comment "BLAST" for the full breakdown 👇

#claudecode #gamedev #indiedev #3d #aiengineering devtools

## Research

* Verdict: Valid. The public GitHub repo neilsonnn/image-blaster exists and matches the post: Claude skills that turn one image into a splat environment, GLB props and SFX, using World Labs and fal. The "$1" and "five minutes" figures are the author's claims and I didn't test them.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [neilsonnn/image-blaster (github.com)](https://github.com/neilsonnn/image-blaster): repo, found by search, verified, high confidence. README describes an MIT image-to-world Claude skillset using World Labs, fal Hunyuan 3D and ElevenLabs SFX, with outputs of .spz splat, .glb/.obj meshes and .mp3 audio.

### Key steps

1. Install Claude Code (the `claude` CLI).
2. Get a World Labs API key (platform.worldlabs.ai) and a fal API key (fal.ai). ElevenLabs SFX is listed in the advanced section, so it may need its own key.
3. git clone https://github.com/neilsonnn/image-blaster && cd image-blaster
4. Run `claude` in the folder and give it your API keys.
5. Put your image in the input/ directory.
6. Tell Claude something like "blast it and confirm each step with me".
7. Collect the outputs: .spz splat, .glb/.obj props, .mp3 ambient and SFX.
8. Optional: tune Hunyuan settings (face count, PBR, generation type, polygon type). To edit the React viewer, remove /app from .claudeignore.

### Not found

The Korean forum listing's date (Aug 2026) was seen only in search results and not opened. I did not test the "$1 for ten props" cost claim.
