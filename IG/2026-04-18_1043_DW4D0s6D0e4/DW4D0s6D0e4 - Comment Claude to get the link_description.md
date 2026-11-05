---
shortcode: "DW4D0s6D0e4"
url: "https://instagram.com/p/DW4D0s6D0e4/"
type: "Carousel"
author: "okaashish"
shared: "Apr 18, 2026, 10:43 AM"
described_by: "claude-haiku-5-5"
described_at: "2026-11-03"
---

# 7 Hacks to Cut Claude Token Usage

The carousel lists seven hacks for using fewer Claude tokens, covering shorter prompts, a code-mapping repo, model choice, PDF handling, session timing, compact summaries and peak hours. It ends with an offer for a fuller guide sent by comment.

Written by claude-haiku-5-5.

## What it teaches

1. Give cleaner, shorter inputs: remove extra words, avoid repeating context, and be specific.
2. Share only the important parts of data, such as summaries or key points, instead of the full data.
3. Caveman method: tell Claude to remove filler words (no 'the', 'is', 'am', 'are'), give direct answers in short 3-6 word sentences, run tools first, show the result, then stop without narrating.
4. For code projects, use a code-review-graph tool so Claude sees a structured map of the code instead of re-reading the whole codebase.
5. Match the model to the task: Sonnet for code implementation, data analysis, general questions and document summaries; Opus for complex architecture decisions, critical bug diagnosis and nuanced writing; Haiku for quick answers, non-logical tasks and simple daily tasks.
6. Don't upload PDFs directly to Claude: upload the PDF to ChatGPT, prompt it to remove filler and extract the core info as condensed plain text with key points, copy the output and paste it into Claude.
7. Session timing: your 5-hour window starts with your first message, so send a basic message (e.g. 'hey') 2-3 hours before you need Claude to start the window early.
8. Compact skill: create a skill so that saying 'COMPACT' summarizes the conversation into 5-7 bullet points with critical context, decisions and code snippets, formatted for pasting into a new chat.
9. Avoid peak hours, which burn tokens faster: weekdays 5am-11am PT (1pm-7pm GMT). Prefer weekends, weekday evenings, and late night or early morning.

## Source

* Link: github.com/tirth8205/code-review-graph
* How to get it: Comment "Claude" on the post to get the full guide

## Caption

Comment “Claude” to get the link.

Most people run out of tokens early because of how they use Claude, not how much they use it. 

Every message carries past context, so longer chats slowly become expensive.

A simple shift helps: give cleaner inputs. 

Remove extra words, avoid repeating context, and be specific. 

This reduces how much Claude has to process each time.

Also, Claude doesn’t need your full data every time. 

If you share only the important parts (like summaries or key points), it performs the same task with fewer tokens.

Model choice also matters. Using a heavier model for simple tasks increases token usage without adding real value.

Think of it like this: the clearer and shorter your input, the less work Claude has to do. And the longer your session lasts.

I have shared a lot more in the guide. Comment "Claude" and I'll share it with you.

#claude #ai #tokens #aitools #hacks

(Claude, Claude code, Claude skills, token limit, hacks, ai tools)

## Research

* Verdict: Partly valid. The repo is real and matches the post, and the general token-saving habits are sensible. The tool's own README says its big reduction figures are best-case, and small edits can cost more tokens with it. The "guide" is only sent by comment, and I found no public copy.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [code-review-graph (github.com)](https://github.com/tirth8205/code-review-graph): repo, in the post, verified, high confidence. A local Tree-sitter code graph served over MCP so AI assistants read only the affected files, as slide 4 describes.

### Key steps

1. Install it: pip install code-review-graph (needs Python 3.10+; pipx also works).
2. Run code-review-graph install to add the MCP server entry to your detected AI coding tools (use --platform to pick one).
3. In the project, run code-review-graph build, then restart your editor.
4. Ask the assistant to build or use the code review graph for the project.
5. Keep the graph current with update, watch mode or the hooks. Use status or detect-changes --brief to check it.

### Not found

The creator's full guide, which is sent only after commenting "Claude". I found no public copy. I did not check the other claims (the 127→32 token example, the model-choice advice and the ChatGPT PDF step).
