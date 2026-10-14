---
shortcode: "DdUNm6sx_x1"
url: "https://instagram.com/reel/DdUNm6sx_x1/"
type: "Reel"
author: "angus.sewell"
shared: "Sep 16, 2026, 03:21 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Auditing job tasks against Anthropic's Economic Index

A prompt for an AI assistant to audit US computer programmer tasks against Anthropic's Economic Index automation and augmentation data, using the O*NET task list. The full prompt is only available by comment, and only the first of two prompt pages is shown on screen.

Written by claude-haiku-5-5.

## What it teaches

1. Download Anthropic's Economic Index dataset and read its data documentation, then download the AEI Claude csv for the release.
2. Filter to GLOBAL, May 2026, category_name=onet, hierarchy_level=0.
3. Pivot the automation and augmentation percentage columns by node_external_id (Task ID), then save the source and filtered files and cite dates and URLs.
4. Download the O*NET task statements and occupation data for 15-1251.00, listing every official task with its wording unchanged.
5. Join the O*NET tasks to the Anthropic data by Task ID, check uniqueness, and show unmatched tasks without forcing matches.
6. For each matched task, calculate automation share as A/(A+U), skipping zero denominators, and sort descending.
7. Read A>U as automation-leaning and U>A as augmentation-leaning, treating the results as usage patterns rather than job-loss probabilities or proof of AI performance.
8. Treat any explanations for missing cells as untested hypotheses.

## Source

* Link: https://huggingface.co/datasets/Anthropic/EconomicIndex
* How to get it: Full prompts are sent by comment: comment "audit"

## Caption

If you want the job audit prompts comment “audit” and I’ll send it your way

There is some real data to show this was an orchestrated PR campaign but that doesn’t mean they don’t genuinely believe the things they say. It’s like a weird SF culture at this point. Idk man I don’t live in SF but every person I know who does seems to be low key preparing for the apocalypse. 

#ai #buildwithai #vibecoding
