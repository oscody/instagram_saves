---
shortcode: "DWTw4T4EtjV"
url: "https://instagram.com/p/DWTw4T4EtjV/"
type: "Carousel"
author: "godofprompt"
shared: "Apr 06, 2026, 06:33 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Diagnose and fix Claude prompts with autoresearch

A six-slide carousel of copy-paste XML prompts for Claude, presented as Andrej Karpathy's autoresearch approach for finding why outputs fail and improving a skill through scored, one-change-at-a-time rounds. The slides cover diagnosis, building a yes/no scoring checklist, the improvement loop, turning the change log into rules, and applying the loop to any repeatable task.

Written by claude-haiku-5-5.

## What it teaches

1. Diagnose before fixing: paste your current Claude skill or prompt, run it against 5 different test inputs, and score each output.
2. Identify the common failure patterns (vague instructions, missing constraints, weak output format) and rank them by frequency and impact.
3. Write a specific root cause for each failure pattern and record a baseline score before making any changes.
4. Build a scoring checklist: describe what a great output looks like, then convert each vague preference into a specific yes/no question.
5. Keep the checklist to 3-6 questions, each checking one thing, with no ratings or scales.
6. Test each checklist question against 3 sample outputs and remove any question that gives different answers on the same output.
7. Run the improvement loop: score the skill against the checklist to set the baseline, then target the lowest-scoring checklist item.
8. Make one isolated change per round, re-run and re-score it, keep the change if the score improves, and revert it if not.
9. Repeat until the skill hits 90%+ three times in a row.
10. Log every change with the reason it was tried, including reverted ones, and keep the original skill untouched by saving the improved version separately.
11. Review the change log: identify which types of additions consistently improved scores and which types consistently hurt them.
12. Extract 5-10 universal rules from those patterns, each backed by an example from your own optimization history, and keep skill-specific rules separate.
13. For any repeatable task: define measurable success, build a 3-6 question yes/no checklist for it, design the iteration loop, run the first 3 rounds manually, then document the system so it can run without you.

## Source

* How to get it: comment CLAUDE

## Caption

30% of your AI outputs are failing silently. Andrej Karpathy’s approach shows how to eliminate that.
- - - -
👉 Follow @godofprompt if you want to:

- Stay posted with all the newest AI insights
- Optimize existing AI tools with a consistent prompt library

Comment “CLAUDE” to learn prompt engineering for free 🎁
