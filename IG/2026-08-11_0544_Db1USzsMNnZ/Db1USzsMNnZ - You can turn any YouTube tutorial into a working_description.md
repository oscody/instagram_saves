---
shortcode: "Db1USzsMNnZ"
url: "https://instagram.com/reel/Db1USzsMNnZ/"
type: "Reel"
author: "jens.heitmann"
shared: "Aug 11, 2026, 05:44 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# Build Claude Code agents from YouTube tutorials

A creator shows a three-part setup for turning a YouTube tutorial into a Claude Code agent: a video-watching skill for Claude, Gemini reading the same link through Google AI Studio, and a skill-creator step that writes the agent from a reconciled spec.

Written by claude-haiku-5-5.

## What it teaches

1. Install the bradautomates/claude-video skill so Claude can see the video's frames and transcript.
2. Get a free Gemini API key from Google AI Studio.
3. Send the same YouTube link to Gemini, which watches the video natively.
4. Reconcile both reads into one spec, labeling every line confirmed, single source, or conflict.
5. Check only the lines marked as conflicts.
6. Hand the finished spec to skill-creator, which writes the agent.

## Source

* Link: bradautomates/claude-video
* How to get it: Comment "YouTube" for the full step-by-step guide, which the creator says he will send directly.

## Caption

You can turn any YouTube tutorial into a working Claude Code agent by using this custom skill setup.

Install bradautomates/claude-video so Claude sees the frames and the transcript. Send the same link to Gemini from @googlegemini , which watches it natively. Reconcile both reads into one spec that labels every line confirmed, single source, or conflict. You only check the conflicts. Hand it to skill-creator and it writes the agent.

If you’re the human: share this reel to Claude Code and watch it build.

Comment “YouTube” for my full step-by-step guide.

#claudecode #claude #ai #aiagents #aitools

## Research

* Verdict: Valid. The bradautomates/claude-video repo exists and matches the post: it's a "watch" skill that gives Claude frames and a transcript, with an optional free Gemini key. The reconcile and skill-creator steps are the creator's own workflow, and the full guide is only sent by comment or DM.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [bradautomates/claude-video (Watch skill) (github.com)](https://github.com/bradautomates/claude-video): repo, in the vault, verified, high confidence. Repo turns a video URL or file into timestamped frames and a transcript for agents, and supports an optional Gemini API key from Google AI Studio, as the post describes.

### Already in the vault

* Vault: `2. Areas/Botstack/Pi/pi todo/search video watch.md`: Lists this reel and the bradautomates/claude-video GitHub link, along with related watch-skill reels.
* Vault: `2. Areas/Botstack/Pi/pi todo/repo - Instagram saves.md`: Test download of this reel (Db1USzsMNnZ) saved as reel.mp4 and audio.mp3.

### Key steps

1. In Claude Code, run: /plugin marketplace add bradautomates/claude-video
2. Then run: /plugin install watch@claude-video (other agents: npx skills add bradautomates/claude-video -g --skill watch)
3. Make sure Python 3.10+, FFmpeg and the latest yt-dlp are installed. YouTube also needs a JS runtime such as Deno.
4. Optional: put GEMINI_API_KEY (free from Google AI Studio) in ~/.config/watch/.env so Gemini handles the whole video.
5. For transcripts when captions are missing, use WhisperX locally or set GROQ_API_KEY or OPENAI_API_KEY.
6. Ask Claude: use the watch skill on <YouTube URL>. Options include --start, --end and --detail.
7. Per the post, have Claude reconcile the Claude and Gemini reads into a spec labeled confirmed, single source or conflict. Check only the conflicts.
8. Give the spec to skill-creator to write the agent.

### Not found

The creator's full step-by-step guide, which is sent only to people who comment "YouTube". No public copy was found. I didn't check the reconcile prompt wording.
