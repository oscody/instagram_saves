---
shortcode: "DfLzaXBGdza"
url: "https://instagram.com/p/DfLzaXBGdza/"
type: "Carousel"
author: "simplifyinai"
shared: "Nov 01, 2026, 07:20 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-11-03"
---

# Qwen3.5-4B-3D-Coder: Three.js scenes from chat

Introduces Qwen3.5-4B-3D-Coder, a 4B model that generates interactive Three.js 3D scenes as HTML and JavaScript when given a text description in chat. The post shows a grid of example generated scenes and lists the release details: full FP16 weights, dataset, technical report, and Q4_K_M and Q8_0 GGUF versions.

Written by claude-haiku-5-5.

## What it teaches

1. Pick a version: full FP16 weights or the Q4_K_M or Q8_0 GGUF builds.
2. Set up the model with the Three.js system prompt and generation settings the post says are provided.
3. Describe the scene you want in the chat.
4. Take the HTML and JavaScript the model returns as the interactive 3D scene.
5. Use it through chat only; the model is not based on agent tools.

## Source

* Link: ccore/Qwen3.5-4B-3D-Coder

## Caption

simplifyinai Comment “AI” to get the link and the full list of free AI resources.

A 4B model can generate interactive 3D scenes with Three.js 🤯

It’s called Qwen3.5-4B-3D-Coder. Describe a scene in chat, and it generates the HTML and JavaScript.

- Full FP16 weights, dataset and technical report available
- Trained on 4,146 synthetic examples in about 60 hours
- Q4_K_M and Q8_0 GGUF versions available
- Runs through chat, without agent tools

Use the provided Three.js system prompt and generation settings to get started.

## Research

* Verdict: Partly valid. The model exists on Hugging Face and matches the post's details. The page calls it an early-preview, unofficial fine-tune with known bugs, and the post leaves that out.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [ccore/Qwen3.5-4B-3D-Coder (huggingface.co)](https://huggingface.co/ccore/Qwen3.5-4B-3D-Coder): tool, in the post, verified, high confidence. The post names this repo. The page lists FP16 safetensors, Q4_K_M and Q8_0 GGUF, 4,146 training examples, Apache-2.0 and a Three.js system prompt.

### Already in IG saves

* Similar: Web: [AnyCreature: text-to-3D creature generator from a JSON spec (instagram.com)](https://instagram.com/p/DcOYjLqtQAv/) (`DcOYjLqtQAv`). AnyCreature, which makes 3D models from a text prompt.
* Similar: Web: [Turning a 2D image into an animated 3D boxer (instagram.com)](https://instagram.com/p/Dctln3MO3Mg/) (`Dctln3MO3Mg`). img2threejs, an AI tool that generates Three.js models from an image.
* Similar: Web: [Mint Playground: open-source interactive 3D worlds in browser (instagram.com)](https://instagram.com/p/DerCSvSkbtn/) (`DerCSvSkbtn`). Mint Playground, open-source Three.js demos made with AI tools.

### Key steps

1. Pick a build: FP16 safetensors (load with Transformers), or the Q4_K_M or Q8_0 GGUF.
2. Run it locally with llama.cpp: `llama serve -hf ccore/Qwen3.5-4B-3D-Coder:Q4_K_M`. Or with Ollama: `ollama run hf.co/ccore/Qwen3.5-4B-3D-Coder:Q4_K_M`.
3. Use the system prompt from the model card: Three.js core ES module only, from cdnjs v0.160.0, no addons or legacy example imports, and camera controls written directly in the HTML.
4. Set temperature 0.6–0.8, top_p 0.90–0.95, top_k 20–40 and repeat penalty 1.0. In LM Studio, turn off multi-token prediction (MTP).
5. Describe the scene in chat, then save the returned HTML and open it in a browser.
6. If the scene breaks, ask the model to fix it or regenerate. The author says the usual bug is duplicate variable names.

### Not found

I did not open the dataset page (ccore/ThreeJs--Scenes) or the technical report. The Hugging Face page is the only source I checked. The post's "100% free" claim is not checked beyond the Apache-2.0 model license and MIT dataset license on that page.
