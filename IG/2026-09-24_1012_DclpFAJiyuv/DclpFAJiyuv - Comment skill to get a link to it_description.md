---
shortcode: "DclpFAJiyuv"
url: "https://instagram.com/reel/DclpFAJiyuv/"
type: "Reel"
author: "itstundeanthony"
shared: "Sep 24, 2026, 10:12 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Demo: Claude Watch repo for analyzing video

A demo of an open source repo called Claude Watch, which lets Claude watch a video from a pasted link and produce a report with a summary, a visuals table and key moments. The post shows a first run failing for a missing Whisper API key, then a rerun that completes.

Written by claude-haiku-5-5.

## What it teaches

1. Install the Claude Watch repo into Claude.
2. Paste a video link after the /watch command.
3. If the run stops asking for a Whisper API key, add your key and run it again.
4. When it finishes, open the generated report.md, which has a TL;DR, a visuals table and key moments.

## Source

* Link: Claude Watch
* How to get it: comment "skill" to get a link to it

## Caption

Comment “skill” to get a link to it 👇

#ai @duncanrogoff

## Research

* Verdict: Valid. The kalocis-ops/claude-watch repo exists and does what the reel shows: /watch on a URL, with a report and a Whisper key needed only when no captions exist. The vault note already lists this link, though it's tagged "similar but not the right one", and I couldn't confirm which repo the reel actually shows.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [claude-watch (kalocis-ops) (github.com)](https://github.com/kalocis-ops/claude-watch): repo, in the vault, verified, medium confidence. The page describes the /watch command, a report.md with a TL;DR and key moments, and a Whisper key needed only for videos without captions. It is a fork of bradautomates/claude-video, so the reel may show the original or another fork.

### Already in the vault

* Vault: `2. Areas/Botstack/Pi/pi todo/search video watch.md`: Lists this reel with the GitHub link kalocis-ops/claude-watch, alongside three similar watch-skill reels. The note calls them 'similar but not the right one'.

### Key steps

1. In Claude Code, run: /plugin marketplace add kalocis-ops/claude-watch
2. Run: /plugin install watch@claude-watch
3. On first run, the setup script checks for yt-dlp and ffmpeg. macOS installs them with Homebrew; on Linux and Windows it prints the commands to run.
4. Run: /watch <video url> <your question>. Use --start and --end to focus on a section.
5. Captions are used first and are free. If the video has no captions, set a Groq or OpenAI Whisper key, or pass --no-whisper to skip transcription.
6. Open the generated report.md. It has a TL;DR, key moments, and the transcript. It is also saved to the vault's raw/watched/ folder if WATCH_VAULT_DIR is set.
7. Alternative installs: on claude.ai, add watch.skill under Settings → Capabilities → Skills. Or clone the repo into ~/.claude/skills/watch.

### Not found

I couldn't confirm that the reel shows this exact fork. The "skill" comment link was not available, and I didn't check the original bradautomates/claude-video repo.
