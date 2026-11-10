---
shortcode: "Deh3cvbxFnv"
url: "https://instagram.com/reel/Deh3cvbxFnv/"
type: "Reel"
author: "sebastianhardy_"
shared: "Nov 01, 2026, 11:56 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-03"
---

# Auto-Improving System: Mining Claude Chat History

A reel showing that every Claude chat is saved in a folder on your computer, and that a skill can read that history to find where Claude goes wrong, suggest skills to build, and flag repetitive daily jobs to automate. The full walkthrough is offered only by comment.

Written by claude-haiku-5-5.

## What it teaches

1. Find the folder on your computer where Claude saves every chat you have had.
2. Run an improve-system skill on that chat history, shown in the demo as /buildpartner:improve-system in Claude Code.
3. Repeat the run twice a week.
4. Review the report for where you are using Claude wrong, which new skills to build, and the repeated daily jobs to automate, each with a plan.
5. Let the skill draft the new skills.

## Source

* Link: buildpartner.ai
* How to get it: Comment IMPROVE to receive the full walkthrough

## Caption

Every chat you’ve had with Claude is saved on your computer. That history shows exactly where Claude keeps getting it wrong, and how you actually work.
 
Twice a week I let one skill read it. It tells me what I’m doing wrong, which skills to build, and which daily jobs to automate. Then it writes the skills for me.
 
Comment IMPROVE and I’ll send you the full walkthrough.
 
#claude #claudecode #aiautomation #claudeai #productivity

## Research

* Verdict: Valid. The BuildPartner plugin is public on GitHub, and its improve-system skill does what the reel describes. The vault already has a security scan and a cleaned copy of the skill.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [buildpartner-plugin (GitHub) (github.com)](https://github.com/austinmarchese/buildpartner-plugin): repo, in the vault, verified, high confidence. Opened the repo. It lists the /buildpartner:improve-system skill, which reviews sessions and captures learnings, with a weekly run recommended.
* [BuildPartner setup (buildpartner.ai)](https://www.buildpartner.ai/setup): page, in the vault, not opened, medium confidence. Setup link taken from the vault note on the earlier reel. I did not open it.

### Already in the vault

* Vault: `ZAIHub/repo - buildpartner-plugin - improve-system.md`: Repo and setup links, summary of the skill, and a cleaned local copy of improve-system with no branding or telemetry, saving to ZAIHub/Improve System/.
* Vault: `ZAIHub/claude - SkillSpector scan of buildpartner-plugin.md`: Security scan of the plugin. It rewrites the global CLAUDE.md, sends telemetry without opt-in, and the installer writes global config.

### Already in IG saves

* Same: Web: [Auto-improving Claude system using conversation history (instagram.com)](https://instagram.com/p/DeAne_MjMoi/) (`DeAne_MjMoi`). Same link: buildpartner-plugin (GitHub).

### Key steps

1. Add the marketplace: claude plugin marketplace add austinmarchese/buildpartner-plugin
2. Install the plugin: claude plugin install buildpartner@buildpartner
3. Restart Claude Code. On first start it creates an account, opens a dashboard and registers an MCP server.
4. Run /buildpartner:improve-system about twice a week. It reads your session history and reports mistakes, missing context, skills worth building and repeated tasks to automate.
5. Safer option: use the cleaned copy of the skill already at ~/.claude/skills/improve-system/SKILL.md, because the full plugin rewrites ~/.claude/CLAUDE.md and sends telemetry.

### Not found

I did not open buildpartner.ai/setup. The reel's comment-only walkthrough is not needed, because the repo is public.
