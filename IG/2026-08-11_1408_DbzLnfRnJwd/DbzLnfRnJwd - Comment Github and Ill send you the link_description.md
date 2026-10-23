---
shortcode: "DbzLnfRnJwd"
url: "https://instagram.com/p/DbzLnfRnJwd/"
type: "Carousel"
author: "godofprompt"
shared: "Aug 11, 2026, 02:08 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Codex Router: run DeepSeek, GLM, Qwen in Codex

The post introduces Codex Router, a local router that adds external models such as DeepSeek, Kimi, GLM, Qwen and Anthropic to Codex's model picker so Codex can delegate work to them as subagents. It shows the agent prompt used to install it from GitHub.

Written by claude-haiku-5-5.

## What it teaches

1. Install codex-router from the GitHub repository given in the post (github.com/duolahypercho/codex-router).
2. Have the agent follow the repo's AGENTS.md, keeping your existing Codex models, profiles, settings and ChatGPT login.
3. Choose which provider authentication to use yourself, and only migrate recognized older versions.
4. Run the Codex doctor check.
5. Restart the final app yourself; the agent leaves that step to you and never asks you to paste a token or API key into chat.
6. In Codex's model picker, toggle "subagent models" on for the models you want; they then appear beside the built-in models and Codex can delegate to them as subagents.

## Source

* Link: github.com/duolahypercho/codex-router

## Caption

Comment “Github” and I’ll send you the link.

Someone figured out how to run DeepSeek, GLM, and Qwen as subagents inside Codex, right alongside GPT.

It’s called Codex Router. It’s a local router that merges external models, DeepSeek, Kimi, GLM, Qwen, Anthropic, and more, straight into Codex’s native model picker, so they show up right next to the built-in models and Codex can delegate work to them as subagents.

Setup: install codex-router from GitHub, toggle “subagent models” to enable the ones you want, and that’s it, they’re live.

## Research

* Verdict: Valid. The repo exists and matches the post: it's a local router that adds external models (Kimi, DeepSeek, Anthropic, Z.ai/GLM, Qwen) to Codex and has a subagent-model toggle. The caption's "that's it" skips the install and restart steps.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [duolahypercho/codex-router (github.com)](https://github.com/duolahypercho/codex-router): repo, in the post, verified, high confidence. The README describes an external-model router for Codex with providers like DeepSeek, Kimi, Anthropic, Z.ai and Qwen, per-model subagent toggles, and an AGENTS.md install prompt.

### Already in the vault

* Vault: `ZAIHub/search - skillspector - similar ai safety workflows.md`: Lists Codex Router (@godofprompt) as a proxy-type tool that sits between the agent and your code, and says to run SkillSpector on it first.

### Key steps

1. macOS/Linux: run the repo's install.sh with `--target codex --guided --with-tray`. On Windows, run install.ps1 with `-Target codex -Guided -WithTray`.
2. Alternative, CLI only: `brew tap duolahypercho/codex-router`, then `brew install codex-router`, then `codex-router setup --guided`.
3. Or tell a Codex agent to follow the repo's AGENTS.md to install it.
4. Add provider credentials (API key or OAuth) for the providers you want. They stay on your machine.
5. Run `./bin/model-router codex doctor` and fix any FAIL line.
6. In the Control Center or tray Settings tab, turn on the models you want as subagents and in the picker.
7. Fully quit and reopen Codex, start a new task, and pick a routed model.

### Not found

I didn't read the last ~54k characters of the README or the contents of AGENTS.md. I didn't security-audit the code, and it routes your API keys, so check it first (your vault note suggests SkillSpector).
