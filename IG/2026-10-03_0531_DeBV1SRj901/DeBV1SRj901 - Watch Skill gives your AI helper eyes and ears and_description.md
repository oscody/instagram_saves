---
shortcode: "DeBV1SRj901"
url: "https://instagram.com/reel/DeBV1SRj901/"
type: "Reel"
author: "gittrend.io"
shared: "Oct 03, 2026, 05:31 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Watch Skill gives AI eyes, ears and proof

A reel promoting Watch Skill, a tool that turns video, audio and screen recordings into timestamped evidence an AI agent can cite. It says a separate process checks results, so the answer is not just the AI's word.

Written by claude-haiku-5-5.

## Source

* Link: github.com/oxbshw/watch-skill
* How to get it: The repo URL appears on screen in the reel. The reel also offers to send the repo link if you comment 'watch'.

## Caption

Watch Skill gives your AI helper eyes and ears, and lets something other than the AI check the work. Every answer points to a moment you can open. More like this → gittrend.io

#ai #agents #opensource #github #mcp #video #python #devtools

## Research

* Verdict: Valid. The repo exists and matches the reel. It turns video, audio and screen activity into timestamped frames, transcripts and OCR, and a separate Core process issues the verdicts. The benchmark numbers are the project's own and haven't been independently reproduced.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [oxbshw/watch-skill (github.com)](https://github.com/oxbshw/watch-skill): repo, in the post, verified, high confidence. README tagline is 'Give AI agents eyes, ears, and verifiable results.' It has timestamped perception and verdicts from a separate Core, matching the reel.
* [gittrend.io (gittrend.io)](https://gittrend.io): page, in the post, not opened, medium confidence. The caption names it as the creator's site. I did not open it.

### Already in the vault

* Vault: `2. Areas/Botstack/Pi/pi todo/search video watch.md`: Lists this reel and the repo link. The note says it was similar to, but not, the post the user was looking for. It points to bradautomates/claude-video, which uses Groq for transcription.

### Key steps

1. Install the engine: pip install 'watch-skill[standard]'. Add the [ocr], [whisper] or [loop] extras if you need them. A bare install can't extract frames.
2. Check the setup: watch-skill doctor
3. Index a source: watch-skill watch <video-url-or-file>
4. Query it: watch-skill ask <id> "what changed at 3:12?"
5. Run it as an MCP server for agents: watch-skill serve (stdio, 39 tools).
6. Optional, for the DeepWatch workspace: npm install -g @deepwatch/cli, then deepwatch doctor, deepwatch setup, and deepwatch web --workspace ./my-project. It needs Node ^22.19 or >=24, and Python 3.11–3.13 for the engine.
7. A model provider is needed only for chat and critique. Local Watch tools and the Library work without one.

### Not found

I did not open gittrend.io. I did not independently check the benchmark claims (89.7% vs 27.9% groundedness), which are self-reported.
