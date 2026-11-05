---
shortcode: "DaAbZf9lYh2"
url: "https://instagram.com/p/DaAbZf9lYh2/"
type: "Carousel"
author: "power.ai"
shared: "Jul 01, 2026, 12:59 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-11-03"
---

# AI loops: goal-driven plan, execute, verify, repeat

A carousel explaining AI loops, where you give an AI a goal once and it plans, executes, verifies, and iterates until a stop condition is met. It includes a cost breakdown, a checklist for when loops are worth building, and a copy-paste self-checking prompt template.

Written by claude-haiku-5-5.

## What it teaches

1. Define a clear goal and a strict way to verify it (a test, metric, or rubric) before starting.
2. Run the cycle: Discover what needs doing, Plan how to do it, Execute the work, Verify against the goal, then Iterate by feeding the result back in and repeating.
3. Keep state/memory of what was already tried so each pass builds on the last instead of restarting from zero.
4. Set a stop condition with a hard iteration limit, so the loop does not run endlessly.
5. Only build a loop if the task repeats regularly, success can be judged automatically, and the agent can finish end to end without constant human help; otherwise a single well-structured prompt is better.
6. Track cost per accepted change rather than tokens or runs; if about half of outputs are rejected, the loop stops saving time.
7. Build order: get one manual run reliable, save it as a reusable skill/instructions, wrap it in a loop with a verification gate and stop condition, then schedule it.
8. Self-checking prompt template: write the task and strict success criteria, then each turn PLAN the single next step, DO the work, VERIFY by scoring each criterion 1-10 and listing weaknesses, and DECIDE: print FINAL if every criterion is 8+, otherwise ITERATING and fix the weakest point first.
9. Rules from the template: never call it done until every criterion is 8 or higher, each pass must fix the weakest score from the last verify, and make reasonable assumptions and note them instead of asking questions.
10. Coding example spec: each iteration runs the test suite, picks the highest-impact failure, makes the smallest fix, and re-runs tests, lint, and type checks; stop when verification passes or after 8 iterations, then summarize what changed and what still fails.

## Caption

🔄🤖 Most people still interact with AI as a single step process: they ask a question, read the output, fix what is wrong, then ask again.

That creates constant back and forth where every improvement depends on a new prompt. It works, but it keeps everything manual and limited by how much you can steer it in real time.

A loop changes the structure completely. Instead of treating AI as something you repeatedly prompt, you treat it as something that runs a process.

You give it a clear goal, then it moves through a cycle: it plans what needs to be done, executes the task, evaluates the result against the goal, identifies weaknesses, and then runs another pass to improve it.

This repeats until the output reaches an acceptable standard or a stopping condition is met.

The key difference is control. 

In the one-shot method, you are involved in every step. In a loop, you only define direction and constraints at the start, then step back while the system iterates internally.

This is why loop-based systems are becoming central in modern AI engineering, especially in agent-style workflows where models are expected to handle multi-step tasks without constant user input.

The structure itself is simple but powerful: define the objective, generate a plan, execute, critique, refine, and repeat.

When this cycle is stable, it reduces the need for constant human correction and allows more complex tasks to complete with less supervision.

Credits: @AnatoliKopadze on X

#ai #artificialintelligence #aitools #aihacks #chatgpt

## Research

* Verdict: Valid. The carousel summarizes Anatoli Kopadze's X article on AI loops. The advice is sound and matches the article's five-step cycle. I could only read a mirror of the article, not the original X post.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Loops explained: Claude, GPT, Mira and what actually works (Anatoli Kopadze, mirrored) (youmind.com)](https://youmind.com/landing/x-viral-articles/mastering-ai-loops-claude-mira): page, found by search, verified, medium confidence. Opened it. The author is @AnatoliKopadze, the date is 20 Jun 2026, and it lays out the same discover-plan-execute-verify-iterate cycle, the lint/tests check, and the iteration cap that the carousel shows.
* [mer.vin summary of the article (mer.vin)](https://mer.vin/2026/06/ai-agent-loops-explained-claude-goal-gpt-self-check-and-mira-telegram-skills/): page, found by search, not opened, low confidence. A search result describing the same article. I did not open it.

### Key steps

1. Define a clear goal and constraints once.
2. Cycle: Discover what needs doing, Plan, Execute, Verify against the goal, Iterate by feeding the result back in.
3. Coding loop: the goal is passing tests, clean lint and no type errors. Each pass runs the tests, picks the highest-impact failure, makes the smallest fix, then re-runs the checks.
4. Stop when verification passes or after 8 iterations.
5. Self-check prompt for Claude or ChatGPT: plan the next step, do it, score yourself 1-10 on each criterion, then decide. Print FINAL if every criterion scores 8 or more. Otherwise print ITERATING and fix the weakest point first. Don't ask questions; make assumptions and note them.
6. In Claude Code, /loop re-runs a prompt on an interval. /goal keeps a session running until a condition is true.
7. Keep state of what has been tried, and set a hard iteration limit to control cost.

### Not found

The original X article on x.com was not opened. Only an aggregator mirror was read. The vault has no related notes.
