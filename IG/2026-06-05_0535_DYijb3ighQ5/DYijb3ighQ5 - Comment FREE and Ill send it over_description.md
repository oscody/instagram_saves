---
shortcode: "DYijb3ighQ5"
url: "https://instagram.com/reel/DYijb3ighQ5/"
type: "Reel"
author: "wassimyounes_"
shared: "Jun 05, 2026, 05:35 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Spec Kit spec-driven workflow for AI coding

The creator presents GitHub's open-source Spec Kit, a toolkit for spec-driven development with AI coding agents, and lays out the stages it uses to turn an idea into code. The on-screen slides show the command sequence and the tool's compatibility with Claude Code, Cursor, Copilot, Codex and Gemini CLI.

Written by claude-haiku-5-5.

## What it teaches

1. Write the rules and standards first (/constitution).
2. Define what you want to build as a spec before any code is written (/specify).
3. Clarify doubts before starting (/clarify).
4. Plan the architecture from the spec (/plan).
5. Break the plan into ordered, atomic tasks (/tasks).
6. Implement the tasks one at a time and verify each output against the original spec (/implement).
7. Keep the agent from guessing or creatively reinterpreting requirements by working from the spec.

## Source

* Link: Spec Kit
* How to get it: Comment "FREE" to receive the GitHub link and starter guide by DM

## Caption

Comment “FREE” and I’ll send it over.
Why your AI builds keep breaking:
You’re vibe coding.
You opened Claude. You said “build me an app that does X.” You hit enter. The AI guessed. It built something. It half-worked. You patched it. You patched the patches. Now your app is a Jenga tower of glue code held together by hope.
Sound familiar? You’re not broken. You’re just doing it wrong.
GitHub just open-sourced the fix: Spec Kit. 103,000 stars and climbing.
It’s the toolkit for spec-driven development — meaning before Claude writes a single line of code, you define the spec. The AI generates a plan. The plan breaks into tasks. Tasks get executed. Every step is verified against the original spec.
You stop guessing. You stop patching. You start shipping.
What it actually does:
	•	Generates a full spec from a one-paragraph product idea
	•	Breaks the spec into a structured plan
	•	Creates atomic tasks Claude (or Cursor, Copilot, Codex) can execute one at a time
	•	Verifies every output against the original contract
	•	Stops AI from “creatively interpreting” your requirements
Works with: Claude Code, Cursor, Copilot, Codex — every major coding agent.
The difference between hobby vibe coders and founders who actually ship: a spec.
100% open source. MIT license. Free forever.
Comment “FREE” — GitHub link and the official starter guide in your DMs.
#ClaudeCode #VibeCoding #aiagents

## Research

* Verdict: Valid. Spec Kit is a real, MIT-licensed GitHub project for spec-driven development, and the public repo is free. The post's gating of the link behind a "FREE" comment is unnecessary, and its star count (103k) is now out of date.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [github/spec-kit (github.com)](https://github.com/github/spec-kit): repo, found by search, verified, high confidence. Opened the repo. It is an MIT toolkit with /constitution, /specify, /plan, /tasks and /implement commands, and it shows about 142k stars.

### Key steps

1. Install Python 3.11+ and uv.
2. Run: uv tool install specify-cli
3. Run: specify init my-project --integration <your agent> (e.g. copilot), then cd my-project.
4. In the agent chat, run /speckit-constitution once to set project rules.
5. For each feature, run /speckit-specify, then /speckit-plan, then /speckit-tasks.
6. Run /speckit-implement, then /speckit-converge. Repeat until it reports Converged, and review each result.
7. Optional: run specify extension add bug, or specify extension add assess, for bug-fix and idea-assessment flows.

### Not found

The DM "starter guide" was not found and may not be public. The repo's own docs cover the same ground. The post's /clarify step was not in the current README command list. Current commands are prefixed with speckit- and add /speckit-converge. I did not check which agents are supported. The README points to an integrations index for that.
