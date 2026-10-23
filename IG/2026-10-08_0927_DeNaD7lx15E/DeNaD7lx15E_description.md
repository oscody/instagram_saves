---
shortcode: "DeNaD7lx15E"
url: "https://instagram.com/reel/DeNaD7lx15E/"
type: "Reel"
author: "deonnahodges"
shared: "Oct 08, 2026, 09:27 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# Installing Impeccable to improve AI-generated websites

The reel recommends Impeccable, a free tool for making AI-generated websites less generic, and shows its install command on the project page. A screenshot of an article section about fixing existing sites appears at the end.

Written by claude-haiku-5-5.

## What it teaches

1. Open a terminal in your project folder and run `npx impeccable install`, then follow the prompts (the install page also lists Codex, Claude plugin and skills.sh options).
2. In Claude, type /impeccable and tell it what you want it to design.
3. To improve a site you already built, run Impeccable on that existing project instead of starting over.

## Research

* Verdict: Valid. Impeccable is a real, free, Apache 2.0 open-source design skill for AI coding tools. The README confirms the `npx impeccable install` command and the /impeccable usage the reel shows.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [pbakaus/impeccable (github.com)](https://github.com/pbakaus/impeccable): repo, found by search, verified, high confidence. README gives `npx impeccable install` and /impeccable commands, and has audit, critique and polish commands for existing projects.
* [Impeccable docs site (impeccable.style)](https://impeccable.style): page, found by search, not opened, medium confidence. The repo and search results name it as the official site, with a ZIP download and docs. I did not open it.

### Key steps

1. In your project root, run `npx impeccable install`. It detects your AI tools and asks for a project-local or global install.
2. In your AI tool, run `/impeccable init`. It inspects the project and writes PRODUCT.md.
3. Run commands as `/impeccable <command> <target>`, for example `/impeccable critique landing`, `/impeccable audit blog` or `/impeccable polish settings`.
4. For an existing site, run `/impeccable document` to generate DESIGN.md from your code. Then use audit, critique or polish on the pages you want to fix.
5. To scan code without an AI tool, run `npx impeccable detect src/`.
6. Update later with `npx impeccable update`.
7. Other installs: the Claude Code plugin (`/plugin marketplace add pbakaus/impeccable`) or `npx skills add pbakaus/impeccable`.

### Not found

I did not open the reel itself. I also did not open impeccable.style, so the command and rule counts are from the GitHub README only. Search results disagree on those counts.
