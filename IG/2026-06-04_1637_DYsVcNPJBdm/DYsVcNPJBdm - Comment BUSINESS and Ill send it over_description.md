---
shortcode: "DYsVcNPJBdm"
url: "https://instagram.com/reel/DYsVcNPJBdm/"
type: "Reel"
author: "wassimyounes_"
shared: "Jun 04, 2026, 04:37 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Anthropic's 31 small business skills, comment BUSINESS

The reel shows a file tree of 31 small business skills and 15 daily-use skills, each listed with a slash command such as /invoice-chase, plus a README excerpt titled "Knowledge Work Plugins." It ends with a call to comment "BUSINESS" to get the material.

Written by claude-haiku-5-5.

## Source

* How to get it: Comment "BUSINESS" on the post; the material is sent by DM

## Caption

Comment “BUSINESS” and I’ll send it over.

Anthropic dropped 31 small business skills. They got 382,000 downloads on day one.

Then someone mapped every single one into a 10-minute setup. Free.

Here’s what you’re handing your business:

- invoice-chase — automatically hunts down unpaid invoices
- close-month — closes your books at month-end like a bookkeeper
- tax-prep — organizes everything before tax season
- friday-brief — a weekly business summary, every Friday, automatic
- job-post-builder — writes and posts job listings
- contract-review — reads contracts and flags the risky clauses
- client-onboarding — runs your full new-client flow
- business-pulse — a live health check on your whole operation

That’s just the first pack. There’s a second one — 15 daily-use automations: morning-briefing, quick-research, email-drafter, slide-deck-builder, budget-dashboard, difficult-conversation-prep, and more.

Every one of these is a slash command. You type /invoice-chase and it runs.

This is the entire back office of a small business — finance, sales, HR, marketing, reporting — turned into commands you trigger in 10 seconds.

You don’t need to hire the team. You need the skill pack and 10 minutes.

Comment “BUSINESS” — full skill pack and setup guide in your DMs.

#SmallBusiness #ClaudeAI #AIAgents

## Research

* Verdict: Partly valid. The skills are real, public and free in Anthropic's knowledge-work-plugins repo, so there's no need to comment for a DM. The "31 skills" count and "382,000 downloads" are unconfirmed. The repo's small-business README lists about 44 skills, and it describes plain-language triggers rather than slash commands.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [anthropics/knowledge-work-plugins (small-business folder) (github.com)](https://github.com/anthropics/knowledge-work-plugins/tree/main/small-business): repo, found by search, verified, high confidence. Opened it. It holds invoice-chase, close-month, tax-prep, contract-review, job-post-builder and business-pulse, matching the reel's names.
* [invoice-chase skill page (third-party directory) (claudemarketplaces.com)](https://claudemarketplaces.com/skills/anthropics/knowledge-work-plugins/invoice-chase): page, found by search, not opened, medium confidence. Search result describing invoice-chase from the same repo. I did not open this page.

### Key steps

1. Run in Claude Code: claude plugin marketplace add anthropics/knowledge-work-plugins
2. Install a plugin with: claude plugin install <name>@knowledge-work-plugins. The exact small-business plugin name is unconfirmed, so check the repo's small-business README.
3. Or install a single skill: npx -y skills add anthropics/knowledge-work-plugins --skill invoice-chase --agent claude-code
4. In Cowork, install from claude.com/plugins.
5. Connect your tools, such as QuickBooks, Stripe and Gmail, which the finance skills use.
6. Trigger skills with plain requests such as "Pay the bills" or "Can I make payroll?". The smb-router skill sends each request to the matching skill.

### Not found

The 382,000 downloads figure is unverified. I did not open the MindStudio blog, which says 31 skills. The reel's slash-command names and the second pack of 15 daily-use skills were not confirmed. The "productivity" plugin may be that pack.
