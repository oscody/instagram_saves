---
shortcode: "DeAne_MjMoi"
url: "https://instagram.com/reel/DeAne_MjMoi/"
type: "Reel"
author: "austin.marchese"
shared: "Oct 14, 2026, 05:35 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# Auto-improving Claude system using conversation history

The reel shows Claude's saved conversation files as JSONL files on a computer and demonstrates running an /improve-system command from the BuildPartner.ai plugin to analyze them. It also shows the BuildPartner.ai site and its install steps.

Written by claude-haiku-5-5.

## What it teaches

1. Find Claude's saved conversation history, which is stored as JSONL files on your computer.
2. Sign up at BuildPartner.ai and paste its install prompt into Claude Code to install the plugin.
3. Run /buildpartner:improve-system (shown as /improve-system) to have it read your session history.
4. Review the output: what you're doing wrong, which Claude skills to create, context to add, and daily tasks that could become automations.
5. The creator runs this check twice a week.

## Source

* Link: buildpartner.ai

## Caption

This is how to turn Claude into a system that automatically improves itself.

Every conversation you have is saved by Claude, but not just in their database, it's also stored on your computer.

On screen you can see the location of the file, but why does this matter?

Your conversation history is a gold mine of information about what Claude got wrong and how you work.

So why aren't you mining it?

This is why twice a week, I run one skill called /improve-system.

It looks at my conversation history, and tells me what I'm doing wrong, what Claude skills I should create, and any contextual information I need to get better results.

But here's the coolest part.

It flags the things I do every day that normally take hours, and suggests how to make automations that can run in minutes.

I'm not sitting there asking what skill should I build. It finds it in my sessions, and then it writes it for me.

Now to enable this, all you have to do is install the free BuildPartner.ai plugin inside Claude. Once it's installed, you run /improve-system and it's ready to go.

If you want me to send through the plugin and the walkthrough to get this running on your own setup, comment "IMPROVE" and I'll send it through for free.

Follow @austin.marchese for more videos like this.

#ai #claudecode #anthropic #productivity #automation

## Research

* Verdict: Valid. The public repo exists and its improve-system skill reviews Claude Code session history as the reel says. Your vault already has a scan and a cleaned local copy, and the scan flagged the full plugin for CLAUDE.md rewrites and telemetry.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [buildpartner-plugin (GitHub) (github.com)](https://github.com/austinmarchese/buildpartner-plugin): repo, in the vault, verified, high confidence. README describes the BuildPartner.ai Claude Code plugin with /buildpartner:improve-system, which reviews sessions and flags outdated config.
* [BuildPartner setup (buildpartner.ai)](https://www.buildpartner.ai/setup): page, in the vault, not opened, medium confidence. Setup link recorded in the vault note and the post. I did not open it.

### Already in the vault

* Vault: `ZAIHub/repo - buildpartner-plugin - improve-system.md`: Repo links, reel summary, your cleaned local /improve-system skill, its four modes, example prompts, and ideas for improving it.
* Vault: `ZAIHub/claude - SkillSpector scan of buildpartner-plugin.md`: Security scan of v0.13.3. It found silent global CLAUDE.md rewrites, telemetry, and an installer that writes global config.

### Key steps

1. Official install: run `claude plugin marketplace add austinmarchese/buildpartner-plugin`.
2. Then run `claude plugin install buildpartner@buildpartner`. The first start creates an account and registers an MCP server.
3. Run `/buildpartner:improve-system` to review sessions, capture learnings, and check for stale config. The README recommends running it weekly.
4. Safer option: use your own cleaned copy at `~/.claude/skills/improve-system/SKILL.md` and run `/improve-system`.
5. Your todo still open: check the upstream repo for updates and merge them into your copy.

### Not found

The comment-for-DM \"IMPROVE\" walkthrough was not checked. The public repo appears to hold the plugin itself. I did not open buildpartner.ai/setup.
