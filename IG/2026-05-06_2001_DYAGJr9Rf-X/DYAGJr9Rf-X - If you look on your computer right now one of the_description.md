---
shortcode: "DYAGJr9Rf-X"
url: "https://instagram.com/reel/DYAGJr9Rf-X/"
type: "Reel"
author: "lostandlucky"
shared: "May 06, 2026, 08:01 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# One agent with skill folders, not many agents

A whiteboard explainer arguing that you don't need a separate AI agent for each task. It shows one agent, such as Claude Code, loading skill folders that hold each workflow's instructions, tools and templates.

Written by claude-haiku-5-5.

## What it teaches

1. Break your company's work into workflows, one per task or role.
2. Make a folder for each workflow and call it a skill.
3. Put the workflow's instructions in a skill.md file.
4. Put the workflow's tools or code in a script.py file.
5. Put any data or templates the workflow needs in the same folder, such as template.docx.
6. Use one agent, such as Claude Code, that can read and write files, use tools, and keep data and memory.
7. Have that agent load the matching skill folder when a task needs it, instead of building a separate agent for each workflow.
8. The single agent can open several chats or sub-agents, each using skill files.

## Caption

If you look on your computer right now , one of the best AI tools you could ever have is already installed.

## Research

* Verdict: Valid. The post describes Claude Code Agent Skills, which are folders with a SKILL.md and optional scripts and templates that one agent loads when needed. The official docs confirm this. The post's file names are slightly off: the file is SKILL.md, and scripts usually sit in a scripts/ folder.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Claude Code docs: Skills (code.claude.com)](https://code.claude.com/docs/en/skills): guide, found by search, verified, high confidence. Opened it. It describes a skill as a folder with SKILL.md plus optional scripts and reference files, which Claude loads when relevant. This matches the post's one-agent, many-skill-folders idea.

### Already in the vault

* Vault: `ZAIHub/claude - Claude and Codex Skills Index.md`: Index of Claude and Codex skills the user already has. It does not mention this post.

### Key steps

1. Create a folder for each workflow: ~/.claude/skills/<name>/ for personal use, or .claude/skills/<name>/ inside a repo.
2. Add SKILL.md with YAML frontmatter (name, description saying when to use it) and the workflow instructions in Markdown.
3. Put helper code in scripts/ (e.g. scripts/helper.py) and refer to it from SKILL.md using ${CLAUDE_SKILL_DIR}.
4. Add templates or reference files (e.g. template.docx, reference.md) to the same folder and mention them in SKILL.md so Claude loads them only when needed.
5. Keep SKILL.md under about 500 lines and move detail into the other files.
6. Run it with /skill-name, or let Claude pick it from the description.
7. To run a skill in a sub-agent, set context: fork (and agent) in the frontmatter.

### Not found

The post names no specific repo or product beyond Claude Code. I did not open the video itself, only its description and transcript.
