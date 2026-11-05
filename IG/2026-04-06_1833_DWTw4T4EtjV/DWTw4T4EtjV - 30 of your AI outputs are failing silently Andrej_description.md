---
shortcode: "DWTw4T4EtjV"
url: "https://instagram.com/p/DWTw4T4EtjV/"
type: "Carousel"
author: "godofprompt"
shared: "Apr 06, 2026, 06:33 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-11-03"
---

# Diagnosing and improving Claude prompts with scoring loops

A five-slide carousel with prompt templates, each with steps and rules, for finding why a Claude prompt gives inconsistent results, building a yes/no scoring checklist, and improving the prompt one change at a time. It is framed as Andrej Karpathy's approach, and the last slide is a comment-for-guide offer.

Written by claude-haiku-5-5.

## What it teaches

1. 1. Find why prompts fail: paste your current skill or prompt, run it against 5 different test inputs and score each output, identify common failure patterns (vague instructions, missing constraints, weak output format), rank failures by frequency and impact, and give a plain-language diagnosis before suggesting fixes. Rules: diagnose before fixing, make every failure pattern specific, rank by how often failures appear rather than how obvious they are, and establish a baseline score before any changes.
2. 2. Build a scoring checklist: state what a great output looks like and feels like, convert each vague preference into a specific yes/no question, test each question against 3 sample outputs to check it scores consistently, and remove any question that gives different answers on the same output. Rules: every question is yes or no with no ratings or scales, use 3 to 6 questions maximum, each question checks one thing with no compound questions, and vague questions like 'is it good quality?' are not allowed.
3. 3. Run the autoresearch loop: ask for the skill prompt and scoring checklist, establish a baseline score, identify the lowest-scoring checklist item as the first target, make one specific change to address it, re-run and re-score, keep the change if the score improves and revert it if not, and repeat until the skill hits 90%+ three times in a row. Rules: one change per round, log every change with the reason it was tried, document reverted changes as well as kept ones, and keep the original skill untouched while saving the improved version separately.
4. 4. Turn the changelog into rules: from the log of kept changes, find which types of additions consistently improved scores, and from the reverted changes, find which types consistently hurt outputs. Extract 5 to 10 universal rules from these patterns, build a short personal prompt-writing guide to check before writing any new skill, and flag which rules are skill-specific versus universally applicable. Rules: rules must come from evidence in the changelog, each rule needs a specific example from the optimization history, and the guide must be usable in under 2 minutes.
5. 5. Apply autoresearch to any repeatable task: choose a repeatable task (one-off tasks cannot be autoresearched), define what success looks like as measurable outcomes, build a 3 to 6 question yes/no scoring checklist for that task, design the iteration loop (what changes, what gets tested, what gets scored), run the first 3 rounds manually to establish the pattern, and document the system so it can run without you. Rules: the scoring checklist stays consistent across every iteration, changes are isolated with one variable at a time, and the system must be documented so anyone or any agent can run it.

## Source

* How to get it: Comment "CLAUDE" on the post to receive the free AI guide mentioned on the last slide

## Caption

30% of your AI outputs are failing silently. Andrej Karpathy’s approach shows how to eliminate that.
- - - -
👉 Follow @godofprompt if you want to:

- Stay posted with all the newest AI insights
- Optimize existing AI tools with a consistent prompt library

Comment “CLAUDE” to learn prompt engineering for free 🎁

## Research

* Verdict: Partly valid. Karpathy's autoresearch is real, and the keep-or-revert loop idea carries over. But the repo is for LLM training experiments, not Claude prompts. The XML prompts are the creator's own adaptation and are only sent after a comment. The "30% failing silently" figure has no source.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [karpathy/autoresearch (github.com)](https://github.com/karpathy/autoresearch): repo, found by search, verified, high confidence. Opened it: an agent changes one file, runs a fixed test, keeps the change if the score improves and discards it if not. This is the loop the post borrows.

### Key steps

1. Paste your current skill or prompt and run it on 5 different test inputs. Score each output and note the failure patterns.
2. Write 3-6 yes/no checklist questions, each checking one thing. Test them on 3 sample outputs and drop any that give different answers on the same output.
3. Score the skill against the checklist to set a baseline, then target the lowest-scoring item.
4. Make one change per round and re-score. Keep it if the score rises, revert it if not, and log every change with its reason.
5. Stop when the skill scores 90%+ three times in a row. Save the improved version separately from the original.
6. Turn the change log into 5-10 general rules, each backed by an example from your own history.

### Not found

The full XML prompts from the carousel are sent only after commenting "CLAUDE" on the post, and I found no public copy. The "30% of outputs fail silently" claim has no source.
