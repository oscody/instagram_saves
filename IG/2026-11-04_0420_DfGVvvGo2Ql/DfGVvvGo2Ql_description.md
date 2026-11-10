---
shortcode: "DfGVvvGo2Ql"
url: "https://instagram.com/reel/DfGVvvGo2Ql/"
type: "Reel"
author: "zchangd"
shared: "Nov 04, 2026, 04:20 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-04"
---

# Reverse API Engineered repo promo via comment

The creator promotes a GitHub project called Reverse API Engineered, which he says turns websites into APIs so you can scrape without paid scraping tools or APIs. The on-screen shots show its README tagline "Turn websites into APIs" and the repo's file list.

Written by claude-haiku-5-5.

## Source

* Link: Reverse API Engineered
* How to get it: Comment "repo" on the post; the link is sent by DM

## Caption

comment “repo” for the repo link sent to your dms

## Research

* Verdict: Partly valid. The repo is real and free (MIT) and matches the on-screen tagline. It doesn't replace all APIs or scraping tools, though. It needs an AI model/API key, and bot-protected sites like LinkedIn and Instagram may block capture.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [Reverse API Engineer (kalil0321) (github.com)](https://github.com/kalil0321/reverse-api-engineer): repo, found by search, verified, high confidence. README tagline 'Turn websites into APIs', command 'rae', and v0.14.0 all match the on-screen text.

### Already in IG saves

* Same: Web: [Turning websites into agent APIs via reverse engineering (instagram.com)](https://instagram.com/p/DeON0MOB5oi/) (`DeON0MOB5oi`). Same link: Reverse API Engineer (kalil0321).

### Key steps

1. Install: `uv tool install reverse-api-engineer` (or `pip install reverse-api-engineer`).
2. For manual mode: `uv tool install "reverse-api-engineer[manual]"`, then `playwright install chromium`.
3. Run `reverse-api-engineer` and describe the site and your goal.
4. Pick a mode with Shift+Tab: manual (you browse), agent (AI browses), engineer (regenerate from a HAR), collector (gather JSON/CSV).
5. Traffic is captured to a HAR file, and your configured model writes a typed client (Python, TypeScript, Go and others).
6. Find the output in `./scripts/<name>/` and review the code before running it.
7. Optional: `npx skills add kalil0321/reverse-api-engineer` to add it as a coding-agent skill.

### Not found

Nothing missing. The creator's DM link wasn't needed because the repo is public.
