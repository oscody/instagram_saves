---
shortcode: "DaGIKtPki6B"
url: "https://instagram.com/p/DaGIKtPki6B/"
type: "Carousel"
author: "divyannshisharma"
shared: "Jul 02, 2026, 05:00 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-11-03"
---

# Claude Code skill to watch videos

An 18-slide carousel introducing a free Claude Code skill, /watch, which gives Claude frames and transcripts from a video. It covers installation, cost, and two use cases: breaking down viral hooks and analyzing one segment.

Written by claude-haiku-5-5.

## What it teaches

1. Copy the link of the video you want Claude to watch (the example is a 45-minute YouTube lecture).
2. In Claude Code, run /plugin marketplace add bradautomates/claude-video, then /plugin install watch@claude-video.
3. For Codex or other generic skills, run git clone https://github.com/bradautomates/claude-video.git ~/.codex/skills/watch. For claude.ai, download watch.skill from the README and add it under Settings → Capabilities → Skills.
4. Run /watch:watch followed by the video URL or file path, with an optional question.
5. To analyze only part of a video, add --start and --end times (the example uses --start 00:35 --end 01:38).
6. The skill pulls the video's captions when they exist. If a video has no captions, it transcribes the audio with Whisper, which needs an API key only in that case, according to the README.
7. For a viral video, paste its link and ask Claude to explain why the hook worked. Claude breaks it down by authority, pattern interrupt, visual and audio mismatch, and payoff.

## Source

* Link: https://github.com/bradautomates/claude-video
* How to get it: Caption asks readers to comment "SEND" for the link; the repo is also written on slides 8 and 9.

## Caption

Comment “SEND” I will send you the link!
.
.
.
.
#openclaw #ai #claude #aiagents

## Research

* Verdict: Valid. The public repo bradautomates/claude-video provides a /watch skill that pulls captions (or transcribes with Whisper) and extracts frames, as the post describes. The "comment SEND" gate isn't needed because the repo is public.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [bradautomates/claude-video (Watch skill) (github.com)](https://github.com/bradautomates/claude-video): repo, in the vault, verified, high confidence. README describes /watch downloading a video, extracting frames, using captions or Groq/Whisper transcription, matching the post.

### Already in the vault

* Vault: `2. Areas/Botstack/Pi/pi todo/search video watch.md`: Links this post and the GitHub repo bradautomates/claude-video, noting it uses Groq for transcription; also lists related reels.

### Key steps

1. In Claude Code run: /plugin marketplace add bradautomates/claude-video
2. Then run: /plugin install watch@claude-video
3. Make sure Python 3.10+, FFmpeg and the latest yt-dlp are installed (YouTube also needs a JS runtime like Deno).
4. Run /watch <video link or file> with an optional question.
5. Captions are used first. If there are none, set a transcription backend in ~/.config/watch/.env (whisperx locally, or groq/openai with an API key).
6. Adjust with --detail (transcript, efficient, balanced, token-burner), --start/--end, --timestamps, or --resolution 1024 for small on-screen text.

### Not found

I didn't find the creator's DM link. It isn't needed, since the repo is public.
