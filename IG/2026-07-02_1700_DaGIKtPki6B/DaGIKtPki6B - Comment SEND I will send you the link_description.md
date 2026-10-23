---
shortcode: "DaGIKtPki6B"
url: "https://instagram.com/p/DaGIKtPki6B/"
type: "Carousel"
author: "divyannshisharma"
shared: "Jul 02, 2026, 05:00 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Claude Code watches any video via /watch

A six-slide carousel showing how to let Claude Code analyze a video by pulling both its transcript and screenshots, using a free skill. It walks through the example of a 45-minute Y Combinator lecture and a use case for breaking down viral hooks.

Written by claude-haiku-5-5.

## What it teaches

1. Install the free video skill in Claude Code by adding its marketplace and entering the marketplace source.
2. Find the video you want and copy its link (the example is a 45-minute Y Combinator lecture on YouTube).
3. In Claude Code, type /watch followed by the video link, and optionally a question.
4. The skill takes the transcript from the video's captions, or transcribes the audio if there are no captions.
5. The skill also captures screenshots from the video so Claude can see on-screen graphs, charts and text, and can reference moments at specific timestamps.
6. To analyze a viral hook, ask Claude to explain the hook frame by frame, checking for elements such as authority, pattern interrupt, visual-audio mismatch, payoff and zooming in on one moment.

## Source

* How to get it: Comment "SEND" on the post to receive the link

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
