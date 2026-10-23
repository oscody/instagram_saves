---
shortcode: "DeHS3EQo0Os"
url: "https://instagram.com/reel/DeHS3EQo0Os/"
type: "Reel"
author: "peterandstewiecode"
shared: "Oct 05, 2026, 12:43 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# PewDiePie's Ajax local AI model news

A news-style reel about PewDiePie's Ajax, a fine-tuned Qwen3.5-9B model meant to run locally for browsing, email, and calendar tasks. It covers his claim that OpenAI deactivated his account over distillation, and his bet that everyday AI can run on smaller models on your own computer.

Written by claude-haiku-5-5.

## Source

* Link: Odysseus (GitHub)

## Caption

YouTuber PewDiePie's quest to take on Big Tech continues.

After building his own GPU setup and launching Odysseus, he has now unveiled Ajax, a fine-tuned Qwen3.5-9B model built to run locally and handle things like browsing, email and calendar tasks.

He also used Heretic to remove many refusal patterns, while saying he kept limits around harmful requests.

The biggest controversy came during training. PewDiePie says OpenAl banned him twice after he used outputs from its models to help train Ajax through distillation.

He mocked the rule, pointing out that major Al companies themselves trained on huge amounts of public web data.

Now he says Ajax v1 already works around 9 out of 10 times on the tasks he built it for, and he is already training the next version.

His bigger bet is that a lot of everyday Al may not need giant cloud models at all. It could run on smaller models, on your own computer, under your own control.

What are your thoughts?

Keywords
PewDiePie AI, Ajax AI, Ajax model, Odysseus AI, Qwen3.5-9B, local AI, local LLM, self hosted AI, AI assistant, open source AI, AI agents, AI news, OpenAI, AI distillation, private AI, offline AI, AI on PC

#PewDiePie #LocalAI #ArtificialIntelligence #AI #OpenSourceAI

## Research

* Verdict: Partly valid. The news matches press coverage: Ajax is a fine-tuned Qwen3.5-9B for Odysseus, and PewDiePie says OpenAI banned him. The OpenAI ban and the "9 of 10" figure come only from his own account. I found no public Ajax download, so only Odysseus can be used now.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Odysseus (PewDiePie) GitHub repo (github.com)](https://github.com/pewdiepie-archdaemon/odysseus): repo, found by search, verified, medium confidence. Opened it: a self-hosted AI workspace (chat, agents, email, calendar, local models) under AGPL-3.0-or-later. The page does not mention Ajax, and I did not confirm it is the repo the post's link points to.
* [PewDiePie Debuts Ajax, a Qwen 3.5 9B Agent for Odysseus Workspace (aiweekly.co)](https://aiweekly.co/alerts/pewdiepie-debuts-ajax-a-qwen-35-9b-agent-for-odysseus-workspace): page, found by search, not opened, medium confidence. Search result describing Ajax as a Qwen 3.5 9B fine-tune for Odysseus. I did not open it.
* [PewDiePie Says OpenAI Banned Him Twice While He Built Ajax (freepressjournal.in)](https://www.freepressjournal.in/tech/pewdiepie-says-openai-banned-him-twice-while-he-built-ajax-a-local-ai-model): page, found by search, not opened, medium confidence. Search result covering the OpenAI ban claim. I did not open it.

### Already in the vault

* Vault: `ZAIHub/search - skillspector - similar ai safety workflows.md`: Only lists this reel under 'Running AI locally'. It has no steps or resource.

### Key steps

1. Clone the Odysseus repo from GitHub and cd into it.
2. Copy .env.example to .env.
3. Run: docker compose up -d --build
4. Open http://localhost:7011. The first admin password is printed in the odysseus container logs.
5. For production, pin a specific image tag instead of :latest.
6. Ajax weights: as of early October reports, no public download, model card, or license had been confirmed. Check again before relying on it.

### Not found

I found no public Ajax weights, model card, or Hugging Face page. I found no official OpenAI statement on the bans. I did not open the news articles. The "9 out of 10" figure is PewDiePie's own claim.
