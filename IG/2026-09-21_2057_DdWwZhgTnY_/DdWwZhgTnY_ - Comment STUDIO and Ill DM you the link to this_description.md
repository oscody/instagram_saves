---
shortcode: "DdWwZhgTnY_"
url: "https://instagram.com/reel/DdWwZhgTnY_/"
type: "Reel"
author: "buildwithneej"
shared: "Sep 21, 2026, 08:57 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Free Claude-driven video studio repo: OpenMontage

A reel promoting OpenMontage, a free GitHub repo that lets an AI coding assistant turn a plain-language brief into a finished video through staged steps with approval gates. Viewers are told to comment STUDIO to receive the repo link by DM.

Written by claude-haiku-5-5.

## Source

* Link: OpenMontage
* How to get it: Comment "STUDIO" on the post and the link is sent by DM

## Caption

Comment “STUDIO” and I’ll DM you the link to this repo.

There is a GitHub repo that turns Claude into a full video production studio, and it is free.

OpenMontage makes your AI coding assistant the director. You type a plain-language brief, and the agent runs the whole pipeline: research, proposal, script, scene plan, assets, edit, compose, then hands you one finished MP4. It works with Claude Code, Cursor, Copilot, Windsurf and Codex. Zero API keys required for a real video: Piper narration runs offline, footage comes from Archive.org, NASA, Wikimedia, Pexels and Pixabay, and Remotion, HyperFrames and FFmpeg do the composition and subtitles. Every creative stage has an approval gate, and the checkpoint writer refuses to mark a gated stage complete without your recorded yes. It also reviews its own render before you see it: ffprobe checks, frame pulls for black frames, audio level checks, subtitle presence. 12 production pipelines cover animated explainers, documentary montages, talking heads, screen demos, podcast repurposing and dubbing. I ran the install and the zero-key demo on my own machine on Sep 14: clean setup, four videos rendered, no errors.

59,493 stars and 7,485 forks as of Sep 16, up from 13.7K stars in June. Number one repository of the day on GitHub Trending.

The catch, in full: the license is AGPL-3.0, so anyone modifying and redistributing it as a service has obligations. The showcase videos in the README were made with paid models like Veo and Kling, and the free tier is the simpler Remotion path, so the zero-key output looks nothing like the trailers. 325 open issues, expect rough edges. And only install from the real repo, because copycat installers using this name have shipped malware twice.

#claude #claudecode #github #opensource #openclaw

## Research

* Verdict: Valid. The public repo exists, is AGPL-3.0, and matches the post's features and assistant list. It needs no comment or DM. The star count is higher now than the post's figure, which is plausible growth.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [calesthio/OpenMontage (github.com)](https://github.com/calesthio/OpenMontage): repo, found by search, verified, high confidence. Opened the repo. It lists AGPL-3.0, 12 pipelines in the About text, a zero-key demo using Piper, and support for Claude Code, Cursor, Copilot, Codex and Windsurf.

### Key steps

1. Install Python 3.10+, FFmpeg, Node.js 18+ and an AI coding assistant such as Claude Code.
2. git clone https://github.com/calesthio/OpenMontage.git
3. cd OpenMontage
4. make setup (the README also gives manual pip, npm and piper-tts steps, and PowerShell commands for Windows)
5. make demo to render the zero-key demo videos (Piper narration and free stock sources)
6. Open the folder in your assistant and give it a plain-language video brief.
7. Approve each gated stage as the agent runs it.
8. Add paid API keys in .env only if you want paid-model output like the README trailers.

### Not found

I did not check the creator's claims of a Sep 14 demo run, the malware copycats, or the 325 open issues. The README's pipeline table lists 11 pipelines, not the 12 in the About text.
