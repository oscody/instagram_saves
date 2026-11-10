---
shortcode: "DelSdCDmd2I"
url: "https://instagram.com/p/DelSdCDmd2I/"
type: "Carousel"
author: "simplifyinai"
shared: "Oct 29, 2026, 12:45 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-30"
---

# Claude Code as a job search assistant

The post promotes an open-source "AI Job Search" repo that runs on Claude Code and covers evaluating listings, tailoring a CV, drafting cover letters and preparing for interviews. The carousel also diagrams the repo's /setup, /scrape and /apply workflow.

Written by claude-haiku-5-5.

## What it teaches

1. Clone the repo and fill in your profile (/setup builds your profile files).
2. Use /scrape to search job portals; review the matches with fit ratings and pick one.
3. Run /apply <url> on the chosen job: Claude evaluates fit, scores it and gives a recommendation.
4. For a good fit, the framework drafts a tailored CV and cover letter (LaTeX).
5. A reviewer agent critiques the draft, you revise it, and you get the final output.
6. Use the repo's interview preparation for the next step after applying.

## Source

* Link: AI Job Search
* How to get it: Comment "AI" on the post; the link is sent via DM

## Caption

simplifyinai Comment “AI” to get the link and the full list of free AI resources.

Turn Claude Code into your job search assistant with this repo.

Clone it, fill in your profile, and let it help you:

- Evaluate job listings
- Tailor your CV
- Draft cover letters
- Prepare for interviews

Less repetitive work for every application.

## Research

* Verdict: Valid. The repo is MadsLorentzen/ai-job-search. It is MIT-licensed and has /setup, /scrape, /apply and /interview commands, as the post shows. The post says the link comes by DM, but the repo is public.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [AI Job Search (MadsLorentzen/ai-job-search) (github.com)](https://github.com/MadsLorentzen/ai-job-search): repo, found by search, verified, high confidence. The README matches the post: an MIT Claude Code framework with /setup, /scrape, /apply (draft, reviewer, LaTeX CV and cover letter) and /interview. The README's own clone command names a different owner, ai-job-search-dev/ai-job-search, so the repo may have moved or been renamed.

### Already in IG saves

* Similar: Web: [Career Ops: Claude Code job search tool (instagram.com)](https://instagram.com/p/DW5bfmLt4bS/) (`DW5bfmLt4bS`). Also recommends Career-Ops, a Claude Code job-search system.
* Similar: Web: [Engineer's Claude AI agent ranks 740+ job offers (instagram.com)](https://instagram.com/p/DXAYA7Gii95/) (`DXAYA7Gii95`). Career-Ops (santifer/career-ops), another Claude Code job-search repo that scores listings and tailors CVs.

### Key steps

1. Install the prerequisites: Claude Code (paid plan or API credits), Python 3.10+, Bun, and LaTeX with lualatex and xelatex. pypdf is optional, for the ATS parse check.
2. Fork and clone the repo. Keep your fork private, because /setup writes personal data into tracked files.
3. Run python3 tools/install_portal_clis.py to install the job portal CLIs.
4. Run claude in the repo, then /setup. It builds your profile from a documents/ folder, a pasted CV, or an interview.
5. Run /scrape to find postings that match your profile. /rank batch-scores the scraped jobs.
6. Run /apply <url or pasted job description>. It evaluates fit, drafts a CV and cover letter, has a reviewer agent critique them, revises, and compiles the PDFs.
7. Run /interview to get a prep pack for a scheduled interview, with an optional mock interview.
8. Read every cover letter before sending. Use /outcome to record results and draft follow-ups.

### Not found

The repo's README clone command names ai-job-search-dev/ai-job-search, not MadsLorentzen. I did not check whether the two are the same repo. I did not check the star count, which sources put at roughly 15k–19.5k.
