---
shortcode: "DW1UByySWwJ"
url: "https://instagram.com/reel/DW1UByySWwJ/"
type: "Reel"
author: "heystevetan"
shared: "May 11, 2026, 01:54 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Mirofish: simulate decisions with AI agents before committing

A video presenting Mirofish, an open-source tool that spawns thousands of AI agents with different backgrounds and opinions into a simulation to show how people might react to a decision. It also shows GitHub star growth and a short product walkthrough.

Written by claude-haiku-5-5.

## What it teaches

1. Describe the decision or scenario you want to test, such as a price change or a campaign.
2. Run it through an AI agent simulation to see how different people might react before spending money.
3. Use the simulated reactions to inform the decision before you commit to it.

## Source

* Link: 666ghj/mirofish
* How to get it: comment "simulate" to get the link

## Caption

Black Mirror predicted this in 2017. A 20-year-old just built it for real and gave it away for free.

Mirofish spawns thousands of AI agents with different backgrounds and opinions into a live simulation. They react, argue, and change each other’s minds like real humans.

Will customers leave if I raise prices? Will this campaign blow up in my face? You get the answer before you spend a dollar.

Built in ten days. 33,000 GitHub stars. $4M in funding within 24 hours. And it’s completely free.

Stop guessing. Start simulating.

Comment “simulate” and I’ll send you the link.

## Research

* Verdict: Partly valid. MiroFish is a real, free, open-source (AGPL-3.0) multi-agent simulation tool, but the hype is unverified. Simulated reactions are predictions, not "answers", and it needs paid LLM and Zep API keys. I did not check the "20-year-old", "10 days", "$4M" or "Black Mirror" claims.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [666ghj/MiroFish (github.com)](https://github.com/666ghj/MiroFish): repo, in the post, verified, high confidence. The repo is a swarm-intelligence engine that simulates agents with distinct personalities to predict outcomes. It shows 81.3k stars, which is consistent with the post's 33k figure from earlier in its growth.

### Key steps

1. Install Node.js 18+, Python 3.11-3.12 and uv.
2. Clone the repo and copy .env.example to .env.
3. Add an OpenAI-compatible LLM API key (README suggests qwen-plus) and a Zep Cloud API key to .env.
4. Run `npm run setup:all`.
5. Run `npm run dev`.
6. Open the frontend at localhost:3000 (the API runs on 5001).
7. Upload seed material (news, a policy draft or a scenario) and run the simulation.
8. Docker alternative: `docker compose up -d`.

### Not found

Did not verify the post's claims about the founder's age, the 10-day build, the $4M funding or Black Mirror. Simulation accuracy was not checked. The comment-for-link gate is unnecessary because the repo is public.
