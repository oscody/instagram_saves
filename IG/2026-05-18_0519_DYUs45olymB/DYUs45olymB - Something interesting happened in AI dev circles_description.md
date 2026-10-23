---
shortcode: "DYUs45olymB"
url: "https://instagram.com/p/DYUs45olymB/"
type: "Carousel"
author: "thedevlife"
shared: "May 18, 2026, 05:19 AM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-15"
---

# Markdown vs HTML debate in AI dev circles

A six-slide carousel recaps the May 2026 debate over whether AI-generated output should be HTML instead of Markdown, covering Thariq Shihipar's post, Andrej Karpathy's comments, and Kurtis Redux's rebuttal. It ends with a call to follow the account and invites readers to share their own preference.

Written by claude-haiku-5-5.

## Source

* Link: thariqs.github.io/html-effectiveness

## Caption

Something interesting happened in AI dev circles this month.

On May 8, Thariq Shihipar on the Claude Code team at Anthropic shared that he's moved away from writing markdown files for most of his work and started using HTML instead. His reasoning: when AI generates the content, the things markdown is optimized for (easy to type, easy to edit by hand) matter less. HTML can offer richer layouts, interactivity, and visual hierarchy.

He shared a companion site with 9 examples where he thinks HTML works better dashboards, code reviews, SVG diagrams, presentations, collapsible explainers.

A few days later, Andrej Karpathy joined the conversation. He framed it as part of a longer evolution raw text to markdown to HTML to something more interactive down the line and suggested adding "structure your response as HTML" to prompts.

Not everyone agreed. Developer Kurtis Redux published a response arguing markdown still wins on readability, code review, and ecosystem compatibility.

Both sides make fair points. The conversation is still unfolding.

Curious where you land on this do you prefer markdown or HTML when working with AI tools? And has this changed how you're prompting? 👇
.
Follow @‌thedevlife for more content like this
.
.
.
.
.

#thedevlife AI ClaudeCode Anthropic Karpathy LLM WebDev DeveloperTools SoftwareEngineering TechNews AIagents

## Research

* Verdict: Partly valid. The companion site exists and matches the post's argument. It has 20 demos in 9 categories, not "9 examples" as the caption says. I didn't check the Karpathy and Kurtis Redux claims.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [The unreasonable effectiveness of HTML: examples (Thariq Shihipar) (thariqs.github.io)](https://thariqs.github.io/html-effectiveness): page, in the post, verified, high confidence. Opened it: it is the companion site with agent-made HTML examples (code review, SVG diagrams, decks, explainers) that the post describes.

### Key steps

1. Open the companion site and look at the demos by category: planning, code review, design, prototyping, diagrams, decks, research, reports and custom editing interfaces.
2. Ask your agent to produce a self-contained .html file instead of a .md file. For example, add 'structure your response as HTML' to the prompt, as Karpathy reportedly suggested.
3. Use HTML where markdown flattens the content: side-by-side option comparisons, annotated diffs or module maps, design previews, and long material that needs collapsible sections or tabs.
4. For throwaway editing tools such as a triage board or prompt tuner, add an export step that returns the result to the agent or to version control.

### Not found

I didn't find or verify Karpathy's comments or Kurtis Redux's rebuttal, and I didn't check the May 8 date. I also didn't open Thariq's original blog post.
