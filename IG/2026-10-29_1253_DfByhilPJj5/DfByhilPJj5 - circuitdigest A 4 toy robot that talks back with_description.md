---
shortcode: "DfByhilPJj5"
url: "https://instagram.com/p/DfByhilPJj5/"
type: "Post"
author: "circuit_digest"
shared: "Oct 29, 2026, 12:53 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-30"
---

# Toy robot turned AI companion with 0.8B model

A maker turned a $4 Silverlit line-follower toy into a talking robot by mounting an old Android phone on it as its face and voice. A tiny fine-tuned 0.8B model handles simple movement commands in about 200 ms, and harder questions go to a larger chat model.

Written by claude-haiku-5-5.

## Source

* Link: https://circuitdigest.com/news/a-maker-turned-a-4-toy-robot-into-an-ai-companion-for-a-kid-and-a-tiny-0-8b-model-makes-it-stop-in-200-ms

## Caption

circuit_digest A $4 toy robot that talks back, with AI reflexes 🤖⚡

Maker Asten (beasaltfish) took a cheap Silverlit line-follower, soldered four wires to its motor and steering drivers, and put an old Android phone on top as its face, ears and voice.

🔹 An FT232H board lets the phone drive the toy over WebUSB
🔹 A tiny fine-tuned 0.8B model turns "stop" or "turn left" into a move in about 200 ms
🔹 Anything harder goes to a bigger chat model, so it can answer a kid's homework questions too

The code, dataset and model are all open sources. Next up: an ESP32-S3 body, because the phone tips the robot over when it reverses 😅

Read the full story:
https://circuitdigest.com/news/a-maker-turned-a-4-toy-robot-into-an-ai-companion-for-a-kid-and-a-tiny-0-8b-model-makes-it-stop-in-200-ms
Link in bio 🔗

#CircuitDigest #Robotics #AI #EdgeAI #LLM

## Research

* Verdict: Valid. The article and the open-source repo both exist and match the post's details: Silverlit toy, FT232H over WebUSB, Qwen3.5-0.8B reflex model, and the dataset and model on Hugging Face.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [beasaltfish/bot-reborn (github.com)](https://github.com/beasaltfish/bot-reborn): repo, in the post, verified, high confidence. The article names the repo; the opened README covers the phone body, toy car wiring, reflex model and ESP32 body.
* [CircuitDigest article (circuitdigest.com)](https://circuitdigest.com/news/a-maker-turned-a-4-toy-robot-into-an-ai-companion-for-a-kid-and-a-tiny-0-8b-model-makes-it-stop-in-200-ms): page, in the post, verified, high confidence. Link from the post; the content matches the caption.
* [robot-simple-commands dataset (huggingface.co)](https://huggingface.co/datasets/beasaltfish/robot-simple-commands): other, found by search, not opened, medium confidence. Linked in the repo README; I did not open the page itself.
* [robot-simple-commands-qwen3.5-0.8b model (huggingface.co)](https://huggingface.co/beasaltfish/robot-simple-commands-qwen3.5-0.8b): other, found by search, not opened, medium confidence. Linked in the repo README as the reflex model; I did not open the page itself.

### Key steps

1. Wire the toy: cut the PCB trace to the controller and solder four wires to the two motor driver chips' inputs. Never connect straight to the coil, or the FT232H pin can burn out. See docs/hardware.md (watch the D6/D7 warning).
2. Connect the wires to an FT232H USB-to-GPIO board and plug it into the Android phone.
3. On a computer on the same Wi-Fi, clone the repo and run `npm install`.
4. Run `server/models/fetch.sh` once to download the wake-word and VAD models.
5. Run `npm start`. In the admin page, create a character, choose the body type, and set a provider and API key for each layer (ears, mind, voice, optional reflex).
6. Enable the Chrome flag for insecure origins so USB and the mic work on the admin address.
7. Scan the character's QR code with the phone, which becomes the face, mic and speaker.
8. Optional: add the fine-tuned reflex model (beasaltfish/robot-simple-commands-qwen3.5-0.8b) for fast stop/turn commands. Test without hardware first using the 'Dry run' body or http://localhost:8787/sim/.

### Not found

I did not open the Hugging Face pages themselves. The article gave no URLs for them, so I took the links from the GitHub README.
