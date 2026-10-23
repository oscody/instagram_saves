---
shortcode: "DeR8ZyWxve0"
url: "https://instagram.com/reel/DeR8ZyWxve0/"
type: "Reel"
author: "joshuablatch"
shared: "Oct 11, 2026, 10:08 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# Cutting Claude token costs by offloading work to Mac

A creator shows a contact-sheet dashboard comparing Claude's token use for video editing before and after moving tasks to Mac tools. He says a video under two minutes went from about 50k tokens to about 3k.

Written by claude-haiku-5-5.

## What it teaches

1. Measure where Claude spends tokens first, such as which files and frames it reads.
2. Use Apple's built-in Vision tools on the Mac to read on-screen text, detect faces, and run green screen effects instead of having Claude process frames.
3. Use Spotlight on the Mac to locate folders so Claude does not have to search for them.
4. Transcribe audio locally with Whisper so Claude does not need to process the video for speech.
5. Build a single contact sheet of scene-change frames with ffmpeg and send Claude that sheet plus a hook image, instead of every frame.

## Source

* How to get it: The prompt is said to be in the comments, with no keyword given

## Caption

94% IN TOKEN SAVINGS. Prompt in the comments. Shoutout to @claudeai for being a baller. Shoutout to @apple for being a hustler.

Friends don’t let friends waste tokens.

#claude #claudecode #ai

## Research

* Verdict: Unresolved. The prompt is said to be in the comments, and I found no public copy. The 50k to 3k (94%) claim is plausible, because a contact sheet is far cheaper than many frames, but I couldn't verify the figures.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Key steps

1. Checked the vault for joshuablatch and 'contact sheet': no matches.
2. Ran one web search on the creator, the tools and the savings figure: no public copy of the prompt found.
3. Similar workflows exist (ButterCut, Brooke Lacey's Claude Code/FFmpeg/Whisper pipeline), but none are confirmed to be this creator's.

### Not found

The creator's prompt (in the Instagram comments) and the dashboard behind the 50k to 3k token figures. Check the comments on the reel directly.
