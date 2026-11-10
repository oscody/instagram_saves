---
shortcode: "DfUkfbjNjpx"
url: "https://instagram.com/reel/DfUkfbjNjpx/"
type: "Reel"
author: "opusjake"
shared: "Nov 05, 2026, 08:18 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-05"
---

# Seed Skill: 11 Claude skills for startup fundraising

The post promotes the Seed Skill, a free pack of 11 Claude skills that covers competitor research, investor matching, pitch materials and investor outreach. On screen it shows six named skills and a GitHub repo called seed-skill.

Written by claude-haiku-5-5.

## What it teaches

1. Install the skill in Claude by pasting the repo link and saying "install skill" (as stated in the transcript).
2. Run Competitor Scout first to research competitors and find their weak points.
3. Run Investor Finder to match investors to your business.
4. Use Business Planner, Market Sizer, and Pitch Deck Designer to build the business plan, market sizing, financial model, and pitch deck.
5. Use The Closer for outreach: personalized investor emails, follow-ups, and tracking conversations until an investor call is booked.
6. Keep the order: competitor research, investor matching, pitch materials, outreach. You still bring the idea, build the business, and attend the meetings.

## Source

* Link: seed-skill
* How to get it: Full setup is sent by comment; the caption says to comment SKILL (the transcript says "scale")

## Caption

Comment “SKILL” and I’ll send you the full setup 👇

Claude just killed bootstrapping.

It’s called the Seed Skill, and it brings 11 specialized AI skills together to help turn your startup idea into an investor pitch.

One researches your competitors and finds their weak points.

Another finds investors that match your business.

Others build your business plan, financial model and pitch deck so you’re ready for the conversation.

Then there’s the outreach: personalized investor emails, follow-ups and tracking conversations so you’re not managing your entire raise across a hundred tabs.

Competitor research → investor matching → pitch materials → outreach.

You still bring the idea, build the business and show up for the meetings. This handles a lot of the prep that slows founders down.

The skill pack is free. Save this for the startup idea you keep putting off.

#Claude #aitips #aitools #ai #claudeai

## Research

* Verdict: Partly valid. The free MIT repo exists with 11 skills matching the post. The claims are overstated: it doesn't raise money for you. Competitor Scout only mines App Store reviews, and The Closer sends emails only after you approve each batch.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [Jakeschincariol/seed-skill (github.com)](https://github.com/Jakeschincariol/seed-skill): repo, found by search, verified, high confidence. README lists 11 skills including Competitor Scout, Investor Finder, Business Planner, Pitch Deck Designer, The Closer and Market Sizer, with the 'install skill' paste method.

### Key steps

1. Paste https://github.com/Jakeschincariol/seed-skill into Claude and say 'install skill'. Or in Claude Code run /plugin marketplace add Jakeschincariol/seed-skill, then /plugin install seed-skill@seed-skill.
2. Or copy the folders for plain commands: cp -r seed-skill/seed-* ~/.claude/skills/
3. Requires Python 3.8+. For SEC investor searches, set sec_user_agent in seed/config.json or the SEC_USER_AGENT env var.
4. Optional: connect Gmail and Google Calendar in Claude and set their send tools to 'Needs approval'.
5. Story and numbers: /seed-scout, /seed-market, /seed-model, /seed-plan, /seed-deck.
6. The raise: /seed-investors, /seed-closer (sends nothing until you approve each batch), /seed-coach.
7. After a yes: /seed-terms and /seed-dataroom. Ongoing: /seed-updates. Outputs are saved in a seed/ folder.

### Not found

The creator's comment/DM setup was not checked. The repo is public, so it isn't needed.
