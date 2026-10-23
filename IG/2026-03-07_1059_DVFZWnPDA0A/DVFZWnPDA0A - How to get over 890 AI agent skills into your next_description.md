---
shortcode: "DVFZWnPDA0A"
url: "https://instagram.com/reel/DVFZWnPDA0A/"
type: "Reel"
author: "bobbybuildsai"
shared: "Mar 07, 2026, 10:59 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Installing 890+ AI agent skills into a project

The reel walks through installing the Antigravity Awesome Skills GitHub collection of about 890 agentic skills into a project folder in Google Antigravity. It then shows where the skills appear and how to call one by name.

Written by claude-haiku-5-5.

## What it teaches

1. Open the Antigravity Awesome Skills repository on GitHub and go to its Installation tab.
2. Copy the option A npx install command.
3. In Google Antigravity, open your project folder and start a new terminal from the Terminal menu.
4. Paste the copied npx command into the terminal and let it finish running.
5. Find the installed skills in the my-skills/skills folder of the project.
6. To use a skill, call it by name in the Antigravity agent, for example frontend-slides.
7. Open the skill's SKILL.md file to read how it works and what it can do.

## Source

* Link: github.com/sickn33/antigravity-awesome-skills (Antigravity Awesome Skills)

## Caption

How to get over 890 AI agent skills into your next project. This is a no-brainer. You have to do this.

## Research

* Verdict: Partly valid. The repo exists and matches, but it has changed since the reel. It now holds about 2,600–2,700 skills (not 890) and has been rebranded and restructured, so the reel's install steps and my-skills/skills folder are probably outdated.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Antigravity Awesome Skills (now AAS Core / Agentic Awesome Skills) (github.com)](https://github.com/sickn33/antigravity-awesome-skills): repo, in the post, verified, high confidence. Opened the repo from the post link. It is a collection of SKILL.md agent skills with an npx/npm exec installer, now at V19.15.0 and MIT-licensed.

### Already in the vault

* Vault: `3. Resources/0. Daily/2026-02-15.md`: Same repo link with a one-line description (800+ agentic skills for Claude Code/Antigravity/Cursor). No install steps.
* Vault: `ZAIHub/claude - Claude and Codex Skills Index.md`: Index entry that points to the 2026-02-15 daily note.

### Key steps

1. Preview first. The README's current example install command is: npm exec --yes --ignore-scripts --package=agentic-awesome-skills@19.15.0 -- agentic-awesome-skills --release 19.15.0 --path .agents/skills --skills brainstorming,systematic-debugging --dry-run
2. Check the preview, then run the same command without --dry-run to install.
3. The install location comes from --path. The README also lists host flags such as --cursor, --gemini and --codex.
4. For Antigravity, the default target needs a selected set of skills, a filter, or an explicit --all.
5. Call a skill by name. In Antigravity CLI use /brainstorming <task>. In Cursor use @brainstorming <task>. In Gemini CLI use 'Use brainstorming to ...'.
6. Open a skill's SKILL.md to see what it does.
7. Treat bulk-installing thousands of skills with caution. Install only the ones you need and read their SKILL.md first.

### Not found

I read only the first 100,000 of 145,734 characters of the README. I did not see an explicit 'option A' label or the my-skills/skills folder, so I can't confirm the reel's exact steps still apply.
