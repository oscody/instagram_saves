---
shortcode: "Dc7ncLDmMIB"
url: "https://instagram.com/p/Dc7ncLDmMIB/"
type: "Carousel"
author: "datasciencebrain"
shared: "Sep 22, 2026, 08:02 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Repairing stale agent memories: a 20-file guide

A carousel promoting a written project guide for a memory agent that tracks when facts were true versus when they were believed, and detects and repairs stale facts. The slides show the guide's cover, table of contents, mental model, architecture diagram, and setup commands.

Written by claude-haiku-5-5.

## What it teaches

1. Store each memory as an interval with a belief attached, keeping valid time (when the fact was true) separate from transaction time (when the system believed it).
2. Never delete a memory. Close its validity window instead.
3. Classify every change as one of four operations: born (opens, no end), replaced (closes where its successor opens), ages (stays open, belief weakens, flagged), or ends (closes, nothing succeeds it).
4. Run two paths into one writer: an arrival path that extracts, classifies and applies policy when the user speaks, and a timed sweep that finds stale facts when nobody has said anything.
5. Make the repair module the only file that changes rows, so every rule and audit entry lives in one place.
6. Detect stale facts with SQL and file reads, so a sweep with no drift makes no model calls.
7. Send low-confidence repairs to a human review inbox instead of applying them automatically.
8. Build bottom-up, with config and clock first, then store, embed and recall, cache and LLM calls, extract, classify, policy and repair, detect, propose and sweep, graph nodes, and finally the demo, CLI and inbox.
9. Verify that the sqlite-vec extension loads before writing a schema around it.
10. Create the project with uv, add the listed dependencies, and put the Groq API key in a .env file as GROQ_API_KEY.
11. Inject a clock object so tests can run with a frozen time.
12. Write the success criterion for an ablation before running it, then measure which mechanisms actually changed answers.

## Source

* How to get it: The full guide PDF is shared only with Instagram subscribers via the subscribe button on the profile (paid membership). Not sent by comment or DM.

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
