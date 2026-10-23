---
shortcode: "DW4D0s6D0e4"
url: "https://instagram.com/p/DW4D0s6D0e4/"
type: "Carousel"
author: "okaashish"
shared: "Apr 18, 2026, 10:43 AM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Cutting Claude token usage with five habits

A carousel on why people run out of Claude tokens early, covering terse-output prompting, a code-structure repo, model choice by task, and converting PDFs before sharing them with Claude.

Written by claude-haiku-5-5.

## What it teaches

1. Keep inputs clean: remove extra words, avoid repeating context, and be specific, since every message carries past context.
2. Share only the key points or summaries of long material instead of full data, to get the same task done with fewer tokens.
3. Use a standing instruction to make Claude answer tersely: drop filler words and articles, give direct answers, use short sentences, run tools first, and skip narrating. The slide shows 127 tokens reduced to 32 for the same async answer.
4. Give Claude a structured map of a code project (the code-review-graph tool) so it reads the structure rather than every line of the codebase again and again.
5. Match the model to the task: Sonnet for code implementation, data analysis, general questions and document summaries; Opus for complex architecture decisions, critical bug diagnosis and nuanced writing; Haiku for quick answers, non-logical tasks and simple daily tasks.
6. Do not upload PDFs straight to Claude: upload the PDF to ChatGPT, ask it to strip filler and extract the core info as condensed plain text with key points, then paste that output into Claude.

## Source

* Link: github.com/tirth8205/code-review-graph
* How to get it: The full guide is sent by comment: comment "Claude" on the post

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
