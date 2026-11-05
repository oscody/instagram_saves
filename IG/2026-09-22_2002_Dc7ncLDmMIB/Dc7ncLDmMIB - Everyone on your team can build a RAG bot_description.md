---
shortcode: "Dc7ncLDmMIB"
url: "https://instagram.com/p/Dc7ncLDmMIB/"
type: "Carousel"
author: "datasciencebrain"
shared: "Sep 22, 2026, 08:02 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-11-03"
---

# Repairing stale memories in a RAG agent

A carousel that presents a project for an agent whose stored facts go stale over time, using two time axes, closed validity windows, zero-model-call detectors and a human review gate, built on free Groq models and SQLite. The visible slides cover the mental model, architecture, config and early modules; the rest of the guide is behind a subscriber paywall.

Written by claude-haiku-5-5.

## What it teaches

1. Store each memory as an interval with a belief attached, not as an overwritable value.
2. Track two time axes: valid time (when the fact was true in the world) and transaction time (when the system believed it).
3. Never delete a memory; when a fact is replaced, close its validity window exactly where its successor opens.
4. Close an ended fact with no successor, and keep an aging fact open while weakening its confidence and flagging it.
5. Use one far-future sentinel date instead of NULL for open intervals, so the vector index can filter with simple comparisons.
6. Route every write through a single module, with arrival events from user messages and a timer-driven sweep for silent decay.
7. Read the time only in one clock module and inject a frozen clock, so staleness over months can be tested in one session.
8. Give each kind of fact its own half-life (for example 3650 days for stable, 180 for slow, 30 for fast) and use the same threshold for the flag and the sweep.
9. Apply repairs automatically only above a high confidence threshold, require a higher bar for retiring rows than for adding them, and always send stable facts to a human.
10. Keep detectors free of model calls by using SQL and a single file read, so an always-on sweep costs nothing.
11. Use a larger completion-token budget for reasoning models, since low limits leave no room for the JSON output.
12. Write the success criterion of an ablation before the run, and report mechanisms that show no effect.

## Source

* How to get it: Full guide is a paid PDF for Instagram subscribers, accessed via the subscribe button on the profile

## Caption

Everyone on your team can build a RAG bot.

Almost nobody can answer this:

"What happens to that memory in six months?"

That question is the gap between a demo and a system. And it is the one interviewers reach for when they want to find out if you have actually shipped something.

I built the answer as a full project.

→ Two time axes - when a fact was TRUE vs when you BELIEVED it
→ Nothing is ever deleted, only closed
→ Four detectors that find stale facts with zero model calls
→ A human gate for repairs the agent shouldn't make alone
→ An ablation with a criterion written down BEFORE the run

And the honest part most write-ups skip: two of my own mechanisms came back null. Keeping history changed no answer on the present. I published that instead of hiding it.

Free Groq. No credit card. 20 files.

A PDF Version of the complete Guide is shared with our Exclusive Instagram Subscribers 👑. Get access to it with 1000+ other FREE Resources for just Rs.45 per month❗️. Click subscribe button in profile to access it now!

Follow @datasciencebrain for daily AI notes 📝,tips ⚙️ and interview Q&A 🎯

.
.
.
.
.
.
[dataanalytics, artificialintelligence, deeplearning, bigdata, agenticai, aiagents, statistics, dataanalysis, datavisualization, analytics, datascientist, neuralnetworks, 100daysofcode, llms, datasciencebootcamp, ai]

#genai #aiengineer #datascience #pythonforai #aicareers

## Research

* Verdict: Promo. The 20-file guide is only available through a paid Instagram subscription (Rs.45 per month), and I found no public copy. The design ideas it describes (bitemporal memory, never deleting rows, a human review gate) are sound and well known, but I couldn't check the author's ablation claims.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Not found

No public repo or copy of the guide turned up. The one vault match, a ZAIHub note on API logging, isn't related. I did not check the author's null-result claims, because the guide is paywalled.
