---
shortcode: "DdcPFEUFLOh"
url: "https://instagram.com/reel/DdcPFEUFLOh/"
type: "Reel"
author: "githubsignals"
shared: "Sep 22, 2026, 07:39 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# XGEN-JING: playable AI first-person worlds

The post presents Jing (XGEN-JING), an open-source interactive model that turns text and images into first-person video and audio that users can move through, turn in, and talk to characters in. Screens show the project's GitHub README with a navigation demo, a user prompt to release a lantern, and a character speaking in a medieval-style tavern.

Written by claude-haiku-5-5.

## Source

* Link: xgen-labs/xgen-jing

## Caption

This AI Model Generates Playable First-Person Worlds

Jing is the interactive model that lets you walk through AI-generated worlds as if you were actually there. It turns simple text and images into first-person video and audio, so you can move forward, turn, and talk to characters in real-time. This is not just a static video; it is a living experience where your actions change what you see and hear. It solves the problem of passive media by creating a playable, dynamic environment from a simple story prompt. The result is a fascinating glimpse into the future of immersive, personalized digital experiences.

Open source: xgen-labs/xgen-jing

Follow for more open source project drops.

#InteractiveAI #AIVideo #GameAI #GenerativeWorlds #AIResearch

## Research

* Verdict: Partly valid. The repo exists and matches, but it generates video offline from control inputs. It needs six H100 GPUs, so "real-time" play is overstated.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [xgen-labs/xgen-jing (github.com)](https://github.com/xgen-labs/xgen-jing): repo, in the post, verified, high confidence. README describes an egocentric interactive model built on MiniMax-H3 that makes first-person video and audio with navigation, object interaction and dialogue.

### Key steps

1. Use Python 3.12 with a compatible CUDA setup. The authors validated it on six H100 GPUs.
2. Clone the repo and run: python3 -m pip install -r requirements.txt
3. Install SGLang separately at the commit the README pins, plus the pinned Diffusers revision and CUDA wheels.
4. Weights download from Hugging Face on first use. Set HF_HOME to change the cache location.
5. Check the setup: python3 demo_bidirection.py check_config=true
6. Generate an example: bash demo.sh cases=examples/bakery_greeting.json. Output goes to examples/outputs/.
7. For custom cases, give each chunk a prompt, a repeat count and a control list. Keys: w/a/s/d move, i/k look up/down, j/l turn. Frames = 17*sum(repeat)+5.
8. Use the Prompt skills to turn a story plus reference images (up to 5) into a cases JSON.

### Not found

The causal model is listed as coming soon. I did not find a real-time interactive version.
