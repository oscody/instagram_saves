---
shortcode: "DWC_I1IDURZ"
url: "https://instagram.com/reel/DWC_I1IDURZ/"
type: "Reel"
author: "michellescomputer"
shared: "Mar 27, 2026, 04:17 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Harness engineering: why the environment matters more

A talking-head reel arguing that coding agents' results depend on their harness, the surrounding environment of tools, context storage and memory, more than on the model. It cites a Princeton study, OpenAI's three-engineer project and Anthropic's two-agent setup, and promises a later walkthrough on building your own harness.

Written by claude-haiku-5-5.

## What it teaches

1. Treat the harness (the tools an agent can call, how it stores context, how it compresses memory, and the rest of its environment) as the main lever for agent performance, not the model.
2. Add linters, feedback loops and observability tools so agents can check and correct their own work.
3. Split the work between two agents: one sets up the environment and the other builds the product.

## Caption

hop in babes, let’s go climbing

mwah 💋 

#build #aiengineering

## Research

* Verdict: Partly valid. Anthropic's two-agent harness is real and matches the reel. OpenAI's harness-engineering experiment is reported only by secondary sources, because I couldn't open OpenAI's post (403). I didn't find the Princeton study. "Harness matters more than the model" is a framing, not something these sources prove.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Effective harnesses for long-running agents (Anthropic Engineering) (anthropic.com)](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents): guide, found by search, verified, high confidence. Describes an initializer agent that sets up the environment and a coding agent that builds features, matching the reel's two-agent setup.
* [Agent Harness Engineering (Addy Osmani) (addyosmani.com)](https://addyosmani.com/blog/agent-harness-engineering/): guide, found by search, not opened, medium confidence. Search result covering the harness engineering concept; I did not open it.
* [OpenAI harness engineering post (guessed URL) (openai.com)](https://openai.com/index/harness-engineering/): page, found by search, not opened, low confidence. Secondary sources describe OpenAI's Codex experiment with about a million lines and no hand-written code. I guessed this URL and it returned 403, so I couldn't open it.

### Key steps

1. Run an initializer agent in the first session. It creates init.sh, a progress log file, an initial git commit, and a feature list for the whole project.
2. Keep the feature list in JSON, with every feature starting as failing. Agents change only the `passes` field, because the model is less likely to overwrite JSON than Markdown.
3. Run a coding agent in every later session. It works on one feature at a time.
4. At session start, the agent checks the working directory, reads the progress notes, git log and feature list, starts the dev server, and runs a basic end-to-end test.
5. Have the agent test like a human user, using browser automation. Without that prompt, agents often mark features done after only unit tests or curl checks.
6. At session end, the agent makes a descriptive commit and updates the progress notes, leaving the codebase clean for the next session.

### Not found

The Princeton study, OpenAI's original post (403 on a guessed URL), and the creator's promised build-your-own-harness walkthrough. I did not open the creator's profile. The two vault hits for "harness engineering" were search notes on other topics, and I did not read them.
