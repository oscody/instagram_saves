---
shortcode: "DXAYA7Gii95"
url: "https://instagram.com/reel/DXAYA7Gii95/"
type: "Reel"
author: "vee_daily19"
shared: "Apr 11, 2026, 10:32 PM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Engineer's Claude AI agent ranks 740+ job offers

A reel recounting an engineer in San Diego who built a Claude-based AI agent that scored 740+ job listings across 10 dimensions, such as role match and skills alignment, and then landed a head of applied AI role. It says the project was open-sourced on GitHub with 30,000+ stars and was discussed in a Reddit r/ClaudeAI post with 2,700+ upvotes.

Written by claude-haiku-5-5.

## Source

* How to get it: Comment "AI" to have the step-by-step article sent by DM

## Caption

An AI Engineer automated job search and landed an head of applied AI role! Follow and comment “AI” to get it for free
.
.
.
#ai #aiengineer #job

## Research

* Verdict: Partly valid. The repo is real and public, so the DM isn't needed. Its README matches the 740 listings and the Head of Applied AI role. The star count is now far above the reel's 30k, and the repo says the Claude agent only helps fill in applications. I didn't check the Reddit post.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [santifer/career-ops (github.com)](https://github.com/santifer/career-ops): repo, found by search, verified, high confidence. README says the author evaluated 740 listings, applied to 68, got 12 interviews and 1 offer, and landed a Head of Applied AI role. It also shows 76.6k stars.
* [Career-Ops: AI Job Search System That Scored 740+ Applications (themenonlab.blog)](https://themenonlab.blog/blog/career-ops-ai-job-search-claude-code-skill): page, found by search, not opened, medium confidence. Third-party write-up of the same project. I saw it in search results but didn't open it.

### Key steps

1. Run `npx @santifer/career-ops init`. It clones the latest release into ./career-ops and installs dependencies. You can also run `npm i -g @santifer/career-ops` and then `career-ops init`.
2. For a manual install, clone the repo, run `npm install`, then `npx playwright install chromium` (needed only for PDF generation).
3. Run `cd career-ops` and start your AI CLI there, such as `claude` or `codex`.
4. On first launch it walks you through setup by chat, including your CV.
5. Run `/career-ops {JD or URL}` to evaluate a job. This scores it, writes a report, makes a tailored PDF and adds a tracker entry.
6. Run `/career-ops scan` to find new offers on job portals.
7. Run `/career-ops pdf` for an ATS-optimized CV.
8. Run `/career-ops tracker` to see application status. It tailors the documents, but you press Submit yourself.

### Not found

I didn't find the r/ClaudeAI thread or confirm its 2,700+ upvotes. Sources disagree on the score scale (the reel says 10 dimensions, the README says 1-5) and on the evaluation and application counts (the Product Hunt listing says 631 and 68). I didn't open the "step-by-step article" sent by DM, but the repo README covers the same ground.
