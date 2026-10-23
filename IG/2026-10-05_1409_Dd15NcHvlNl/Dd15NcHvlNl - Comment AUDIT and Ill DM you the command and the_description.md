---
shortcode: "Dd15NcHvlNl"
url: "https://instagram.com/reel/Dd15NcHvlNl/"
type: "Reel"
author: "nocodealex"
shared: "Oct 05, 2026, 02:09 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Clean up CLAUDE.md for Opus 5.5

A reel claims that old instructions in CLAUDE.md written for earlier Claude models make Opus 5.5 slower and less accurate. It says a "prompt audit" command can scan the file, propose cuts, and change nothing until approved.

Written by claude-haiku-5-5.

## What it teaches

1. Check your CLAUDE.md for instructions written for older Claude models, since Opus 5.5 follows instructions more literally.
2. Remove 'double-check your work' style rituals.
3. Remove instructions written in ALL CAPS.
4. Remove step-by-step scripts for tasks the model already knows how to do.
5. Run the prompt audit in Claude Code so it scans CLAUDE.md, skills and prompts and writes a report and proposed diff.
6. Review the proposed diff and approve each cut before any change is made.

## Source

* How to get it: Comment AUDIT; the command and guide are sent by DM

## Caption

Comment “AUDIT” and I’ll DM you the command and the guide: how to clean up your CLAUDE.md so Opus 5.5 gets smarter and cheaper. Follow so the DM lands 📩

👇 Why your CLAUDE.md is holding Opus 5.5 back

1. Old rules, new model. Most CLAUDE.md files are full of instructions written for older Claude models. Opus 5.5 follows instructions more literally, so those leftovers slow it down and make its answers worse.

2. One command fixes it. Anthropic’s own Claude API skill has a prompt audit built in. Run it in Claude Code and it scans your CLAUDE.md, skills and prompts.

3. It hunts three habits. “Double-check your work” rituals, instructions shouting in ALL CAPS, and step-by-step scripts for things the model already knows how to do.

4. You approve every cut. It writes a report and a proposed diff first. Nothing changes until you say yes.

5. It pays off. One developer found about 70 fixes across his skills, CLAUDE.md and AGENTS.md. When Anthropic tested it, costs dropped around 9% and accuracy went up about 2 points on the same model.

Comment “AUDIT” and I’ll send you the exact command and the full guide. #claudeai #claude #claudetips #claudecode

## Research

* Verdict: Partly valid. The command is public and matches the post: `/claude-api prompt-audit` in Anthropic's claude-api skill. The 9% cost and 2-point accuracy figures could not be confirmed. The skill also applies edits only if you explicitly ask, rather than asking you to approve each cut.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [anthropics/skills claude-api SKILL.md (prompt-audit) (github.com)](https://github.com/anthropics/skills/blob/main/skills/claude-api/SKILL.md): repo, found by search, verified, high confidence. Opened it. It documents /claude-api prompt-audit, which scans CLAUDE.md, skills and prompts for dated patterns and outputs a report and proposed diff.
* [Lance Martin post announcing the prompt-audit command (x.com)](https://x.com/RLanceMartin/status/2095170001175199771): page, found by search, not opened, medium confidence. The search snippet shows the command and the anti-pattern list (verification rituals and others). The page itself returned HTTP 402, so it was not opened.
* [Claude API skill - Claude Platform Docs (platform.claude.com)](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/claude-api-skill): guide, found by search, not opened, medium confidence. Official docs page for the claude-api skill. It appeared in search results and was not opened.

### Key steps

1. Install the skill: `npx skills add https://github.com/anthropics/skills --skill claude-api`, or use the plugin marketplace. Restart Claude Code.
2. In your project, run `/claude-api prompt-audit`.
3. It sets scope and target model without asking, then inventories CLAUDE.md, rules, commands, skills, subagents and prompts.
4. It scans for dated patterns using the tables in shared/prompt-audit.md, and it has a keep list of things not to delete.
5. Read the report. Each finding has file:line, the pattern, why it is obsolete, and a confidence level.
6. Review the proposed diff. The skill applies edits only if you explicitly ask, so say so only for the cuts you accept.

### Not found

The 9% cost drop and +2 accuracy points claim was not found in the skill page (its last ~14k characters were not read). The creator's DM guide was not found. The command itself is public, so the DM is not needed. The X post returned 402.
