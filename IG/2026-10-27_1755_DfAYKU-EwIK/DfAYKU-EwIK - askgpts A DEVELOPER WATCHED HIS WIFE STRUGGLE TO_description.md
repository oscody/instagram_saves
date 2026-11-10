---
shortcode: "DfAYKU-EwIK"
url: "https://instagram.com/p/DfAYKU-EwIK/"
type: "Carousel"
author: "askgpts"
shared: "Oct 27, 2026, 05:55 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-28"
---

# Dossier: free open-source AI job search tool

A carousel announcing Dossier, a free, open-source AI job search tool that a developer built for his wife, with a list of its features. It describes the tool's capabilities and points to the GitHub repo.

Written by claude-haiku-5-5.

## Source

* Link: AienTech/dossier
* How to get it: comment 'DOSSIER' on the post to get the official link sent by DM

## Caption

askgpts A DEVELOPER WATCHED HIS WIFE STRUGGLE TO FIND A JOB FOR NEARLY 10 MONTHS, SO HE BUILT AN AI TOOL THAT HELPED HER GET HIRED.

And now he's sharing the entire project for free.

Meet Dossier, a free, open-source AI job search assistant designed to simplify everything from finding job openings to creating personalized resumes and tracking applications.

Here's what makes Dossier worth checking out:

•AI-powered job search across LinkedIn, Indeed, and other job sources.
•Custom resumes tailored to individual job descriptions.
•Personalized cover letters generated from your actual experience.
•12 resume templates with customizable designs.
•Smart job matching based on your skills and qualifications.
•Application tracking from initial draft to job offer.
•Local AI support through Ollama and LM Studio for greater privacy.

The best part is that Dossier doesn't invent fake qualifications. It builds applications using the information in your professional profile.

It also supports self-hosting, giving you more control over your personal career data.

One developer's solution to his wife's job search is now a free AI tool that others can use to simplify their own hiring journey.

The software is open-source, although hosting and some AI services may have associated costs.

Comment "DOSSIER" to get the free GitHub project link in your DM.

Save this post for your next job search and follow @askgpts for more free AI tools, career resources, and productivity breakthroughs.

Source: GitHub | AienTech/dossier

#aitools #jobsearch #claudeai #opensource #artificialintelligence

{dossier ai, ai job search, free ai tools, ai resume builder, ai cover letter generator, job search automation, ai job assistant, job application tracker, resume optimization, linkedin jobs, indeed jobs, job hunting tips, ai career tools, open source ai, github projects, local ai models, ollama ai, ai productivity, interview preparation, future of work}

## Research

* Verdict: Valid. The AienTech/dossier repo exists and matches the post's features (12 themes, Ollama/LM Studio, tracking, profile-only drafts). The post's "comment to get the link" is unnecessary because the repo is public. The post omits that it is AGPL-3.0 and that job search needs a third-party API (JSearch, Adzuna or FreeHire).
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [AienTech/dossier (github.com)](https://github.com/AienTech/dossier): repo, in the post, verified, high confidence. The repo is a self-hosted job-search and resume builder with 12 themes, tailored resumes and cover letters, an application tracker, and Ollama/LM Studio support, as in the post.

### Already in IG saves

* Similar: Web: [Claude for a recruiter job search (instagram.com)](https://instagram.com/p/DWY-ysgFY-N/) (`DWY-ysgFY-N`). Also uses AI (Claude) to run a job search, but as a prompt workflow, not a self-hosted app.

### Key steps

1. Install Docker (with Compose) and have about 2 GB of free memory.
2. Download compose.production.yml from the repo.
3. Create a .env file with the database and secret values.
4. Hash your password with the repo's hash-password command and put the result in .env.
5. Run `docker compose up -d` and open http://localhost:3000.
6. For SQLite, set DATABASE_URL=file:/data/dossier.db and run the single container with a data volume.
7. In Settings → AI provider, choose Ollama or LM Studio for local use. You can also use an OpenAI-compatible API, Anthropic or Mistral.
8. Fill in your profile, then use Find jobs (JSearch, Adzuna or FreeHire). Paste a posting to get a draft resume and cover letter, then track the application.

### Not found

I did not check the repo's wiki, releases or star count. I did not check the post's claim that the developer built it for his wife.
