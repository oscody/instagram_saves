---
shortcode: "DeUTTa3thQ4"
url: "https://instagram.com/reel/DeUTTa3thQ4/"
type: "Reel"
author: "thevibefounder"
shared: "Oct 11, 2026, 09:43 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# Claudex Loop: Claude and Codex Working Together

A creator describes Claudex Loop, a free open-source skill that links Claude Code and Codex, and explains how the two models split planning, challenging, building and reviewing code. The post's on-screen text reads "open source" and "mistakes."

Written by claude-haiku-5-5.

## What it teaches

1. Have Fable 5.1 (as named in the post) create the plan.
2. Have GPT-6 Astra (as named in the post) challenge the plan before any code is written.
3. Have Claude fix the plan based on that challenge.
4. Have Astra build the fixed plan.
5. Have Claude review the code against the original requirements.
6. Keep the planning and review in one loop instead of copying work between two AI chats.

## Source

* Link: Claudex Loop (GitHub repo)
* How to get it: Comment "split" to receive the skill and setup, as stated in the post

## Research

* Verdict: Valid. The public MIT-licensed repo exists and matches the post's plan, challenge, build, inspect workflow. You don't need to comment "split" to get it. The model names in the post (Fable 5.1, GPT-6 Astra) are the creator's labels and I didn't check them.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [claudex-loop (chaseai-yt) (github.com)](https://github.com/chaseai-yt/claudex-loop): repo, in the vault, verified, high confidence. The repo describes a four-phase plan-hardening workflow in which one provider reviews the plan and the other builds and inspects. It ships the skills claudex-loop, claudex-route, codex-build and codex-review.

### Already in the vault

* Vault: `ZAIHub/repo - claudex-loop.md`: Repo link, manual install commands, skill list, copyable Claude Code prompt, and a record of the Pi install.
* Vault: `ZAIHub/claude - SkillSpector scan of Claudex Loop 2026-10-11.md`: Security scan of the repo. It flagged the legacy/ skills, which the vault install does not copy.
* Vault: `ZAIHub/search - claudex-loop - similar ai agent workflows.md`: Similar agent workflows.

### Key steps

1. Prerequisites: install and sign in to both the Claude Code and Codex CLIs, and have Python 3.10+.
2. Plugin install in Claude Code: run `/plugin marketplace add chaseai-yt/claudex-loop`, then `/plugin install claudex-loop@claudex-loop`.
3. Manual install: clone the repo, then copy the whole `skills/` folder into `~/.agents/skills/` and `~/.claude/skills/`. Copying a single skill is not enough, because the compatibility commands share a runtime.
4. Open new Claude Code and Codex sessions so they load the skills.
5. Run it: use `/claudex-loop:claudex-loop` (plugin), `/claudex-loop` (manual install) or `$claudex-loop` (Codex).
6. Example prompt: "Plan and implement [task]. builder=codex. Have Codex review the plan and build it, then a fresh Claude session inspects the changes."
7. Options: `builder=claude|codex`, a round cap (default 5) and `PROOF_CMD` for verification. Commits and pushes need your separate approval.

### Not found

I did not check the post's model names (Fable 5.1, GPT-6 Astra). The repo is provider-agnostic. I found no separate resource behind the "split" comment trigger.
