---
shortcode: "DWwq0ZxFWvI"
url: "https://instagram.com/reel/DWwq0ZxFWvI/"
type: "Reel"
author: "sabrina_ramonov"
shared: "Apr 17, 2026, 10:44 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# LLM knowledge base method from Andrej Karpathy

A woman presenter describes a method, attributed to Andrej Karpathy, for turning raw sources into an LLM-compiled markdown wiki. On-screen graphics show the flow from raw sources to the LLM compiler to the .md wiki, plus example queries.

Written by claude-haiku-5-5.

## What it teaches

1. Dump raw sources such as articles, papers and repos into a folder.
2. Have an LLM compile those sources into a markdown wiki with auto-generated summaries, backlinks and concepts.
3. Once the wiki reaches about 100+ articles (the graphic shows 400K words), query it like a search engine.
4. Ask queries such as 'find connections between X and Y', 'what data is inconsistent?' and 'summarize everything on Z'.
5. No fancy RAG setup is needed.
6. File every answer back into the wiki so the research compounds over time.

## Caption

LLM knowledge base method from Andrej Karpathy, co-founder of ChatGPT.

Stop asking your AI random questions. Build a knowledge base instead.

Dump raw sources into a folder... articles, papers, repos, whatever. Then your LLM compiles them into a markdown wiki. Summaries, backlinks, concepts, all auto-generated.

Once your wiki hits 100+ articles, query it like a search engine. "Find connections between X and Y." "What's inconsistent?" No fancy RAG needed.

The best part? Every answer gets filed back into the wiki. Your research compounds.

How are you organizing your AI knowledge? What's your setup?

#ai #chatgpt #learning #productivityhacks #technology

## Research

* Verdict: Valid. Karpathy's "LLM Wiki" gist exists and matches the post's method: raw sources, an LLM-maintained markdown wiki, and answers filed back in. The caption's "co-founder of ChatGPT" is wrong. Karpathy was an OpenAI co-founder, not a ChatGPT co-founder. The "100+ articles" threshold is not in the gist.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Karpathy – LLM Wiki gist (gist.github.com)](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f): guide, found by search, verified, medium confidence. The opened gist describes an LLM-maintained markdown wiki built from raw sources, with answers filed back in and no RAG. I guessed this URL from memory; a search for the gist returned only secondary write-ups.

### Already in the vault

* Vault: `ZAIHub/Karpathy’s autoresearch project.md`: A different Karpathy project (autoresearch), not the LLM wiki. Possibly related background only.
* Vault: `1. Projects/RohnSecondBrain/Task On my Plate.md`: Mentions the creator, sabrina_ramonov, but has nothing on this method.

### Key steps

1. Make a raw/ folder of immutable sources (articles, papers, repos). The LLM reads these but never edits them.
2. Add a schema file (CLAUDE.md or AGENTS.md) that defines the wiki's structure and conventions.
3. Ingest: have the LLM summarize each source and update the entity and concept pages, index.md and log.md.
4. Query: ask the LLM questions against the wiki, starting from index.md. Ask for citations.
5. File valuable answers back into the wiki as new pages.
6. Lint: periodically have the LLM check for contradictions, stale claims, orphan pages and missing cross-references.
7. Optionally, open the wiki in Obsidian as the viewer. Add a local search tool such as qmd once the wiki grows large.

### Not found

I did not read the last ~17k characters of the gist. I did not find a public source for the "100+ articles" threshold or the "400K words" figure.
