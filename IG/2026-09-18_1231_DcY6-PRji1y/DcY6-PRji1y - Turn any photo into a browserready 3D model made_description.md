---
shortcode: "DcY6-PRji1y"
url: "https://instagram.com/reel/DcY6-PRji1y/"
type: "Reel"
author: "gittrend.io"
shared: "Sep 18, 2026, 12:31 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# img2threejs: rebuild a reference image in Three.js

The post walks through the GitHub README for img2threejs, an open-source tool that rebuilds an object from one reference image as a code-only, animation-ready Three.js model. Its pipeline runs under Claude Code, Codex, or OpenCode.

Written by claude-haiku-5-5.

## What it teaches

1. Clone the img2threejs repo into your skills folder.
2. In Claude Code or Codex, attach one reference image of an object.
3. Ask the agent to rebuild the object from the image.
4. The pipeline runs a probe and suitability gate, then a pre-spec assessment of class, complexity and quality contract.
5. It authors an ObjectSculptSpec (components, materials, sockets); if the spec is too shallow, it loops back to authoring.
6. Once the spec passes strict-quality validation, it generates the Three.js factory for the current pass.
7. It renders the model in the browser, takes a screenshot, and repeats the staged pipeline until the render matches the reference.

## Source

* Link: github.com/hoainho/img2threejs

## Caption

Turn any photo into a browser-ready 3D model made entirely from code. More like this → gittrend.io

#opensource #3dmodeling #threejs #generative #aiagents #webgl #indiedev

## Research

* Verdict: Valid. The repo exists and matches the post: an agent skill that rebuilds an object from one image as code-only, animatable Three.js. Install is via npx, not a manual clone.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [hoainho/img2threejs (github.com)](https://github.com/hoainho/img2threejs): repo, in the post, verified, high confidence. README describes a single-image to procedural Three.js THREE.Group factory skill with a strict-quality spec gate and staged passes, for Claude Code, Codex and OpenCode.

### Already in the vault

* Vault: `ZAIHub/search - competition ideas by claude.md`: Lists img2threejs with AnyCreature as AI tools for generating Three.js models, e.g. custom Ludi pieces or alien types. No install steps.

### Key steps

1. Check you have Node.js 18+, Git, Python 3.10+ and a supported agent (Claude Code, Codex, OpenCode or Hermes).
2. Run: npx --yes img2threejs@latest install
3. Run: npx --yes img2threejs@latest doctor to verify.
4. Restart the agent.
5. In Claude Code, attach the image and run /img2threejs with a description of the target model.
6. The agent assesses the image, writes a spec, and passes it through the strict-quality gate.
7. It then builds in passes (blockout, structural, form, material, surface, lighting, interaction, optimization), checking each against a render of the reference.
8. For multi-session work, use forge/state.py init and forge/next.py --state to resume.

### Not found

I didn't check the quality of the output. The repo states that hidden sides are inferred from a single image.
