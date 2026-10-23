---
shortcode: "DcmuyLFJtCp"
url: "https://instagram.com/reel/DcmuyLFJtCp/"
type: "Reel"
author: "tomcrawshaw.ai"
shared: "Oct 09, 2026, 04:24 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# ICM method: structuring context for AI agents

A talking-head reel explaining why adding more context to AI agents fails, and how the ICM (interpretable context methodology) structures a file system so each workflow stage gets the context it needs.

Written by claude-haiku-5-5.

## What it teaches

1. Number the workflow folders so their order shows the stage of the work (e.g. intake, drafting, review).
2. Keep the root file (such as CLAUDE.md) small as a router that lists the folders and what each one is for, not a full business encyclopedia.
3. Give every working folder a context file that states four things: inputs, process, outputs, and the human check.
4. Separate the factory (skills, templates, process rules) from the product (drafts, records, deliverables).
5. Have the agent load only the context for the stage it is working on, not everything every time.
6. On one repeating workflow, run an inventory-only audit: no moving, renaming or deleting files. Classify each part as complete, partial or empty, and show what the workflow would need under ICM.
7. Decide what to change only after seeing the audit results, then check the stage's contract, loaded context and human check when output is wrong.

## Source

* How to get it: Comment "ICM" on the post; the full article is sent by DM

## Caption

Everything you've been told about context is wrong, and this is why the ICM method is so valuable. If you want the full article on the entire ICM method and how to implement it in your business, just comment "ICM" below and I'll send it to your DMs.

## Research

* Verdict: Valid. ICM is a real, public method (GitHub repo and arXiv paper) that matches the reel's description. The creator's full article is only sent by DM, but the original source is public.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Interpretable Context Methodology (RinDig) (github.com)](https://github.com/RinDig/Interpretable-Context-Methodology): repo, found by search, verified, high confidence. README describes numbered stage folders, a small CLAUDE.md router, per-stage CONTEXT.md with inputs, process and outputs, and layered context loading, as in the reel.
* [Model Workspace Protocol: Folder Structure as Agent Architecture (Van Clief, 2026) (arxiv.org)](https://arxiv.org/abs/2603.16021): paper, found by search, not opened, medium confidence. The paper is cited in the repo README, and the search results list it as the ICM paper. I did not open the paper itself.

### Key steps

1. Clone the RinDig/Interpretable-Context-Methodology repo.
2. cd into a workspace, e.g. workspaces/script-to-animation (or workspace-builder to generate your own).
3. Open Claude Code there and type `setup`; answer the onboarding questions in one pass.
4. Give the agent a topic and run the numbered stages in order.
5. Review and edit each stage's output/ files before the next stage runs.
6. For your own workflow: keep CLAUDE.md as a short router, and give each stage folder a CONTEXT.md covering inputs, process, outputs and the human check.

### Not found

The creator's (tomcrawshaw.ai) DM-only article was not found publicly. The reel's audit steps (inventory-only, complete/partial/empty) are probably from that article and were not checked against the repo.
