---
shortcode: "DVRu6GlDNHO"
url: "https://instagram.com/reel/DVRu6GlDNHO/"
type: "Reel"
author: "mikemeansbusiness_ai"
shared: "Mar 11, 2026, 07:40 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Five Claude Code repos to install

The reel recommends five GitHub repos for Claude Code: Claude Skills, Superpowers, 140+ subagents, Manus Planning, and a Prompt Generator. On-screen cards show install commands for the Skills, subagents, and Prompt Generator repos.

Written by claude-haiku-5-5.

## What it teaches

1. Install Claude Skills from github.com/anthropics/skills: run git clone https://github.com/anthropics/skills.git, then cd skills && cp -r . ~/.claude/skills/
2. Add Superpowers for automating the full software engineering lifecycle (requirements, design, testing, deployment) instead of prompting each step by hand
3. Add the 140+ subagents from github.com/VoltAgent/awesome-claude-code-subagents: run git clone https://github.com/VoltAgent/awesome-claude-code-subagents.git, then delegate each task to the specialist agent that fits it
4. Add Manus Planning so the agent keeps a persistent plan before each decision on multi-step builds
5. Install the Prompt Generator from github.com/huangserva/skill-prompt-generator: run git clone https://github.com/huangserva/skill-prompt-generator.git, then cd skill-prompt-generator && pip install -r requirements.txt
6. Use the Prompt Generator to read your codebase and write project-specific prompts, so each new Claude session starts with your stack and architecture

## Source

* Link: github.com/anthropics/skills, github.com/VoltAgent/awesome-claude-code-subagents, github.com/huangserva/skill-prompt-generator
* How to get it: The Superpowers and Manus Planning links are not shown on screen. The caption says to comment SKILLS to get them by DM, and to check the general tab in messages on the IG mobile app (links don't send via web).

## Caption

Stop using Claude Code without these 5 repos. You’re mass slower than everyone who has them.

Here’s the exact stack the top 1% of AI developers are installing right now:

1. Claude Skills (Anthropic’s official skill library)
2. Superpowers (full SWE lifecycle automation)
3. 140+ Subagents (specialized agents for every task)
4. Manus Planning (persistent context that doesn’t forget)
5. Prompt Generator (reads your entire codebase, writes your prompts)

The difference between “using Claude Code” and “using Claude Code properly” is about 10x productivity. These repos close that gap.

I installed all 5 in under 20 minutes. The subagents one alone changed how I build.

Comment SKILLS and I’ll DM you all 5 links plus a full library of everything else you need to 10x your AI coding setup.

Follow for more AI dev content that actually saves you time.

Save this. You’ll need it.

Make sure to check your “general” tab in messages on the IG mobile app. Link doesnt send via web app

.
.
.
#claudecode #aitools #aideveloper #claudeai #anthropic artificialintelligence codingtools devtools github programming softwaredeveloper techtools aiagents codeautomation 10xdeveloper aicoding techreels learntocode buildinpublic devlife codingskills aiproductivity claudeskills machinelearning futureofcoding

## Research

* Verdict: Partly valid. All five repos exist, but the Prompt Generator is an image-prompt tool (portraits, art, design, video), not a codebase-reading prompt writer as the reel says. The "top 1%" and "10x" claims are hype.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [anthropics/skills (github.com)](https://github.com/anthropics/skills): repo, in the post, verified, high confidence. Anthropic's official Agent Skills repo. Its README installs via /plugin marketplace add anthropics/skills, not by copying into ~/.claude/skills.
* [VoltAgent/awesome-claude-code-subagents (github.com)](https://github.com/VoltAgent/awesome-claude-code-subagents): repo, in the vault, not opened, high confidence. The vault note and the post both name it as a curated collection of Claude Code subagents. I did not open it myself.
* [huangserva/skill-prompt-generator (github.com)](https://github.com/huangserva/skill-prompt-generator): repo, in the post, verified, high confidence. The clone and pip install steps match the reel. The README describes AI image prompt generation built on Claude Skills, not reading your codebase.
* [obra/superpowers (github.com)](https://github.com/obra/superpowers): repo, found by search, not opened, medium confidence. Search results show a skills-based dev methodology plugin for Claude Code, which matches 'Superpowers'. The reel never shows its link, and I did not open the repo.
* [OthmanAdi/planning-with-files (github.com)](https://github.com/OthmanAdi/planning-with-files): repo, found by search, not opened, medium confidence. Search results describe a Manus-style persistent planning skill that keeps task_plan.md, findings.md and progress.md on disk. This is probably the 'Manus Planning' repo, but the reel doesn't name it.

### Already in the vault

* Vault: `3. Resources/0. note idea draft/article - 10 GitHub Repositories To Master Claude Code.md`: Lists VoltAgent/awesome-claude-code-subagents as a library of ready-made Claude Code subagent roles.

### Key steps

1. Skills: in Claude Code run /plugin marketplace add anthropics/skills, then /plugin install document-skills@anthropic-agent-skills (or example-skills@anthropic-agent-skills).
2. Subagents: git clone https://github.com/VoltAgent/awesome-claude-code-subagents.git, then copy the agent files you want into ~/.claude/agents/ (this step is my assumption and I did not check it against the README).
3. Superpowers: per search results, run /plugin install superpowers@claude-plugins-official, then use /superpowers:brainstorm, /superpowers:write-plan and /superpowers:execute-plan.
4. Manus-style planning: per search results, run npx skills add OthmanAdi/planning-with-files --skill planning-with-files -g. It keeps task_plan.md, findings.md and progress.md on disk.
5. Prompt Generator: git clone https://github.com/huangserva/skill-prompt-generator.git, cd into it, run pip install -r requirements.txt (Python 3.8+), then open Claude Code in that folder. It is for image prompts.

### Not found

The reel doesn't show the Superpowers and Manus Planning links. The creator sends them by DM after a SKILLS comment. I matched them to public repos by search, so they are likely but not certain. I did not open the VoltAgent, Superpowers or planning-with-files repos.
