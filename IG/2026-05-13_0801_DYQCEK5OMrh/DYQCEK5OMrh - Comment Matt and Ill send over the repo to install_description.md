---
shortcode: "DYQCEK5OMrh"
url: "https://instagram.com/reel/DYQCEK5OMrh/"
type: "Reel"
author: "startscalr_sohum"
shared: "May 13, 2026, 08:01 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Matt Pocock's Claude Skills repo, by comment

The post names Matt Pocock's open-sourced Claude Skills repo and lists skills such as /grill-me, /tdd, /diagnose, /triage and /improve-codebase-architecture. Viewers are asked to comment "Matt" so the creator can send the repo.

Written by claude-haiku-5-5.

## Source

* How to get it: Comment "Matt" on the post; the creator says they will send the repo over

## Caption

Comment “Matt” and I’ll send over the repo to install into Claude Code 🤞🏼

This might be one of the most useful things released for Claude Code users this month.

Matt Pocock just open-sourced his personal Claude Skills repo — the exact workflows he uses for disciplined engineering inside Claude Code.

Not prompts. Actual reusable AI engineering systems.

The repo includes skills like:
• /grill-me
• /tdd
• /diagnose
• /triage
• /improve-codebase-architecture

Basically turning Claude from a chatbot into a real engineering partner.

The craziest part?
You install the entire thing with ONE command.

This is where AI coding is heading:
less prompting…
more reusable agent workflows.

And the devs learning this early are going to move insanely fast.

#ClaudeCode #ClaudeAI #Anthropic #AIEngineering #VibeCoding AITools CodingAI SoftwareEngineering TypeScript BuildInPublic OpenSource

## Research

* Verdict: Valid. The public repo mattpocock/skills exists and has the named skills. The "one command" install claim holds, and you don't need to comment to get it.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [mattpocock/skills (github.com)](https://github.com/mattpocock/skills): repo, in the vault, verified, high confidence. Opened it. It is Matt Pocock's MIT-licensed skills repo and lists grill-me, tdd, triage and improve-codebase-architecture. The debugging skill is named diagnosing-bugs there, not diagnose.

### Already in the vault

* Vault: `3. Resources/0. note idea draft/repo - mattpocock - skills.md`: Repo link, the X post and a LinkedIn post about the grill-me skill
* Vault: `ZAIHub/claude - Claude and Codex Skills Index.md`: Links to the repo note under the grill-me skill

### Key steps

1. In Claude Code, run: claude plugin install mattpocock-skills@claude-plugins-official
2. For other agents, run: npx skills@latest add mattpocock/skills -a <agent>. Leave out -a to pick the agent interactively.
3. Use only one install method per agent, or every skill is installed twice.
4. Once per repo, run /setup-matt-pocock-skills. It asks which issue tracker you use, your triage labels and where to save docs.
5. Run /grill-me before a change, /tdd while building, and /triage and /improve-codebase-architecture as needed.
6. The Claude Code plugin updates itself. The npx route needs npx skills@latest update.
