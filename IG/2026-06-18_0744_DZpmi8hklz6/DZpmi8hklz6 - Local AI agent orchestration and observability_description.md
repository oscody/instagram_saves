---
shortcode: "DZpmi8hklz6"
url: "https://instagram.com/p/DZpmi8hklz6/"
type: "Carousel"
author: "vyzual.ai"
shared: "Jun 18, 2026, 07:44 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-15"
---

# Five open-source local AI agent orchestration repos

A carousel listing five open-source repos for local AI agent work: agenttrace (session cost and health CLI), gbrain (cited answers from a knowledge graph), mission-control (self-hosted agent dashboard), skillclaw (cross-device skill sync proxy), and hermes-workspace (browser control plane for Hermes). Each slide gives a short description and a code snippet.

Written by claude-haiku-5-5.

## What it teaches

1. agenttrace: install with `go install github.com/luoyuctl/agenttrace@latest`, then run `agenttrace --doctor --fail-under-health 80` to get a terminal report or fail the CI pipeline when local agent run health is below 80.
2. gbrain: import `BrainEngine` from `@gbrain/core` and call `await BrainEngine.query("architecture")` to get answers cited from a local knowledge graph.
3. mission-control: start the dispatch with `OPENCLAW_GATEWAY_HOST=localhost pnpm run dispatch`.
4. skillclaw: `from skillclaw import EvolveProxy`, then create `EvolveProxy(target="http://localhost:11434")` to route LLM provider traffic through the local proxy.
5. hermes-workspace: set `HERMES_API_URL=http://gateway:8080` and `API_SERVER_ENABLED=true` in the environment section to connect to the Hermes gateway.

## Source

* Link: https://github.com/luoyuctl/agenttrace, https://github.com/garrytan/gbrain, https://github.com/builderz-labs/mission-control, https://github.com/AMAP-ML/SkillClaw, https://github.com/outsourc-e/hermes-workspace

## Caption

Local AI agent orchestration and observability infrastructure is maturing past the terminal window. Unmanaged local inference pipelines currently lack centralized control, costing developers severe latency gaps and fragmented session state.

→ agenttrace [Go] — agent session cost CLI tool
→ gbrain [TypeScript] — hybrid graph cited answer engine
→ mission-control [TypeScript] — self-hosted local agent dashboard
→ skillclaw [Python] — cross-device skill sync proxy
→ hermes-workspace [TypeScript] — browser-first agent control plane

Integrating these orchestration layers provides absolute local sovereignty over complex agent workflows. Owning the local infrastructure gives you a massive architectural advantage over developers who remain entirely dependent on opaque, third-party vendor interfaces.

Save this for your next sprint — which one are you integrating first?

👉 Follow @vyzual.ai for your clean daily dose of codebase audits, agentic workflows, and developer intelligence.

## Research

* Verdict: Partly valid. All five repos exist and match their descriptions. Several slide snippets don't match the READMEs: agenttrace is Rust, not Go; `@gbrain/core` and `EvolveProxy` aren't documented; `pnpm run dispatch` isn't documented. The "absolute local sovereignty" framing is hype.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [agenttrace (github.com)](https://github.com/luoyuctl/agenttrace): repo, in the post, verified, high confidence. Local TUI/CLI for auditing agent session cost and failures. It is Rust, not Go, so the `go install` line is wrong.
* [gbrain (github.com)](https://github.com/garrytan/gbrain): repo, in the vault, verified, high confidence. Garry Tan's agent memory layer with cited answers (`gbrain think`). It is not on npm, and `@gbrain/core` is not documented.
* [mission-control (github.com)](https://github.com/builderz-labs/mission-control): repo, in the post, verified, high confidence. Self-hosted alpha agent dashboard on SQLite. `pnpm run dispatch` isn't in the README, and `OPENCLAW_GATEWAY_HOST` appears only as a Docker troubleshooting tip.
* [SkillClaw (github.com)](https://github.com/AMAP-ML/SkillClaw): repo, in the post, verified, high confidence. Local client proxy plus an evolve server for sharing skills. No `EvolveProxy` class is documented; the CLI is `skillclaw`.
* [hermes-workspace (github.com)](https://github.com/outsourc-e/hermes-workspace): repo, in the post, verified, high confidence. Web UI for Hermes Agent. The README confirms `HERMES_API_URL` and `API_SERVER_ENABLED=true`, with the default gateway at 127.0.0.1:8642.

### Already in the vault

* Vault: `3. Resources/0. note idea draft/openclaw agent research.md`: Has the gbrain link, described as Garry's OpenClaw/Hermes agent brain.
* Vault: `ZAIHub/search - claudex-loop - similar ai agent workflows.md`: Lists this post as a related local agent tools roundup.
* Vault: `ZAIHub/search - skillspector - similar ai safety workflows.md`: Lists this post, citing agenttrace for watching agent behavior.

### Key steps

1. agenttrace: use the README install, not `go install`: `curl -fsSL https://raw.githubusercontent.com/luoyuctl/agenttrace/master/install.sh | sh`, or `brew install luoyuctl/tap/agenttrace`. Check with `agenttrace --version`.
2. gbrain: needs Bun 1.4+. Run `bun install -g github:garrytan/gbrain`, then `gbrain init --pglite --no-embedding`.
3. gbrain: run `gbrain doctor`, then `gbrain import <folder> --no-embed`. Query with `gbrain search "<phrase>"` or `gbrain think` for a cited answer.
4. mission-control: needs Node 22 and pnpm. Run `bash install.sh --local` or `pnpm install && pnpm dev`, then open localhost:3000/setup to create the admin account. Docker: `docker compose up`.
5. SkillClaw: clone the repo and run `bash scripts/install_skillclaw.sh`, then `skillclaw setup` and `skillclaw start --daemon`. Check the proxy at port 30000 `/healthz`, then point your agent at it.
6. hermes-workspace: set `API_SERVER_ENABLED=true` in `~/.hermes/.env` and run `hermes gateway run`. Clone the repo, run `pnpm install`, copy `.env.example` to `.env`, set `HERMES_API_URL=http://127.0.0.1:8642`, then run `pnpm dev`.

### Not found

I didn't check the `--fail-under-health 80` flag for agenttrace. The README only mentions `--doctor` under building from source.
