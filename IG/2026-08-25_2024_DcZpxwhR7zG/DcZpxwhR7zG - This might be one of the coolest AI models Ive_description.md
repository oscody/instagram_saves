---
shortcode: "DcZpxwhR7zG"
url: "https://instagram.com/reel/DcZpxwhR7zG/"
type: "Reel"
author: "mr.eflow"
shared: "Aug 25, 2026, 08:24 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Tencent WorldClaw: AI generates editable 3D worlds

A streamer reacts to Tencent's WorldClaw model, which generates a full 3D world from a prompt with each object (trees, buildings, carts, lamp posts) as a separate editable asset. The reel shows desert and valley example worlds with depth, normal, and instance renders, and notes the model is not yet available to try.

Written by claude-haiku-5-5.

## Caption

This might be one of the coolest AI models I’ve seen all year.

Tencent’s new WorldClaw model can generate an entire editable 3D world from a prompt — not just the environment, but every individual object inside it.

Trees, buildings, carts, lamp posts, terrain, they’re all generated as separate 3D assets you can actually work with.

Under the hood, it combines image generation, segmentation, and Tencent’s Hunyuan 2D-to-3D tech to turn a generated scene into a full collection of 3D objects.

And the use cases could get really interesting.

You could imagine generating game environments in minutes, building virtual worlds for simulations, or even creating environments where robots can train before they ever enter the real world.

Unfortunately we can’t actually play with this model yet, but this is absolutely one I’m keeping an eye on.

#ai #ainews #aimodel #genai #3dart

## Research

* Verdict: Valid. WorldClaw is a real Tencent Hunyuan paper and the repo matches the post's description of editable separate assets. As the post says, no code or weights are out yet.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [WorldClaw: Agentic 3D Open-World Generation at Scale (arXiv 2608.05248) (arxiv.org)](https://arxiv.org/abs/2608.05248): paper, found by search, verified, high confidence. Abstract describes text-to-3D worlds built from planning agents, terrain, and editable textured meshes placed on terrain.
* [Hunyuan3D-WorldClaw GitHub (github.com)](https://github.com/Tencent-Hunyuan/Hunyuan3D-WorldClaw): repo, in the vault, verified, high confidence. Official Tencent-Hunyuan repo with the same title. It holds only a README and assets, with no code or weights.
* [WorldClaw project page (tencent-hunyuan.github.io)](https://tencent-hunyuan.github.io/Hunyuan3D-WorldClaw/): page, found by search, not opened, medium confidence. Linked from the GitHub README. I did not open it.

### Already in the vault

* Vault: `ZAIHub/ig repo to review.md`: Has the GitHub repo link, marked '3D Open-world Generation not released', and a ChatGPT research link on WorldClaw alternatives.

### Not found

No released code, weights or demo. The project page was not opened. The arXiv page does not list a code link.
