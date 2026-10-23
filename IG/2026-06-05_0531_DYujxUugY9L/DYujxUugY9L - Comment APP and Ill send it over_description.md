---
shortcode: "DYujxUugY9L"
url: "https://instagram.com/reel/DYujxUugY9L/"
type: "Reel"
author: "wassimyounes_"
shared: "Jun 05, 2026, 05:31 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# OpenWA: free self-hosted WhatsApp API gateway

A promotion for OpenWA, a free, open-source, self-hosted WhatsApp API gateway built on NestJS, with a list of things it can be used for. The on-screen text and caption ask viewers to comment "APP" to get the material.

Written by claude-haiku-5-5.

## Source

* How to get it: Comment "APP" on the post; the GitHub repo and setup details are sent by DM

## Caption

Comment “APP” and I’ll send it over.

Free WhatsApp API gateway. Open source. Self-hosted. No per-message fees.

If you’ve ever tried to automate WhatsApp for your business, you know the problem: the official WhatsApp Business API is expensive, slow to approve, and locks you into per-message pricing. OpenWA fixes all of it.

OpenWA is a free, open-source WhatsApp API gateway that gives you full control over your messaging infrastructure — no vendor lock-in, no hidden paywalls, no licensing fees.

What you can build with the OpenWA WhatsApp API:

- A WhatsApp chatbot that answers customers 24/7
- Automated order confirmations and appointment reminders
- WhatsApp broadcasts to your opted-in subscriber list
- An AI WhatsApp agent connected to your CRM
- Multiple WhatsApp numbers running on one instance

The stack: built on NestJS and TypeScript, Docker-ready, multi-session, 100% MIT licensed. Spin up your own WhatsApp API server in minutes.

Businesses pay messaging platforms thousands a month for WhatsApp automation. OpenWA does it self-hosted, for free.

If you build WhatsApp bots, automations, or messaging tools, this is the WhatsApp API gateway you’ve been looking for.

Comment “APP” — GitHub repo and full setup guide in your DMs.

#WhatsAppAPI #WhatsAppAutomation #OpenSource

## Research

* Verdict: Partly valid. OpenWA is a real, MIT-licensed, self-hosted NestJS gateway, and it is public, so no DM is needed. The post leaves out that it is unofficial (whatsapp-web.js/Baileys), carries a real ban risk, and is not a replacement for the official Business API in high-stakes use.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [rmyndharis/OpenWA (github.com)](https://github.com/rmyndharis/OpenWA): repo, found by search, verified, high confidence. README confirms MIT license, NestJS/TypeScript, Docker, multi-session, and a dashboard, matching the post's stack list.

### Key steps

1. Clone the repo: git clone https://github.com/rmyndharis/OpenWA.git && cd OpenWA
2. Start it with Docker: docker compose -f docker-compose.dev.yml up -d
3. Get the admin API key: docker exec openwa-api cat /app/data/.api-key
4. Open the dashboard and API on port 2785. Swagger is at /api/docs, and in production only if ENABLE_SWAGGER=true.
5. Create a session and scan the QR code with a dedicated WhatsApp number, not your main one.
6. Choose the engine with ENGINE_TYPE: whatsapp-web.js (default, about 300–500 MB RAM per session) or Baileys (about 30–80 MB).
7. Set up webhooks, and pace your sends (SEND_PACING_ENABLED), message only opted-in recipients, and warm up new numbers to lower the ban risk.

### Not found

The creator's DM content was not checked. The public repo covers the same material.
