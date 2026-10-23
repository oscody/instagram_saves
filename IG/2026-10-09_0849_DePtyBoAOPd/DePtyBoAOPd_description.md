---
shortcode: "DePtyBoAOPd"
url: "https://instagram.com/reel/DePtyBoAOPd/"
type: "Reel"
author: "jackroberts___"
shared: "Oct 09, 2026, 08:49 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-14"
---

# Find Skills: searching a million Claude skills

The reel introduces Find Skills, a tool from vercel-labs/skills that searches a library of over a million Claude skills by task and installs the best matches, with a ranked list of popular skills on screen. The post is gated behind a comment keyword.

Written by claude-haiku-5-5.

## What it teaches

1. Describe what you are working on, such as editing videos or writing emails.
2. Find Skills picks the best-matching skills from the library.
3. Find Skills installs the chosen skills for you.
4. Skim each skill before it runs.
5. Run a skill through ChatGPT and Claude to check that it is safe before installing it.

## Source

* Link: vercel-labs/skills
* How to get it: comment FINDER

## Caption

Comment "FINDER" and I'll send you the skill.

Most people install skills one at a time.

Then they stop looking.

There are over a million out there.

Nobody can search that by hand.

Find Skills does the searching for you.

Tell it what you're working on.

Editing videos. Writing emails.

It picks the best matches.

Then it installs them for you.

Skim each one before it runs.

Like a librarian who fetches the book.

And puts it on your desk.

It's the number one skill on the site.

Install this one first.

Let it find the rest.

#claude #claudeskills #findskills #aitools #productivity

## Research

* Verdict: Valid. The find-skills skill is in vercel-labs/skills and does what the post says. It sits at #1 on skills.sh. The "million skills" figure is not confirmed: the page's 1.46M "All Time" number may count installs rather than skills.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [vercel-labs/skills (CLI, includes skills/find-skills) (github.com)](https://github.com/vercel-labs/skills): repo, in the post, verified, high confidence. Public MIT repo with the `npx skills` CLI and a skills/find-skills folder.
* [find-skills SKILL.md (github.com)](https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md): page, found by search, verified, high confidence. The skill finds skills by task and installs them on request.
* [skills.sh leaderboard (skills.sh)](https://skills.sh): page, found by search, verified, medium confidence. find-skills is #1 with about 4.0M installs. The page doesn't state a total number of skills.

### Key steps

1. Check that Node.js is version 22.20 or later.
2. Install the skill: `npx skills add vercel-labs/skills --skill find-skills -g`. I did not run this; the repo README doesn't spell out this exact command, so check it against `npx skills --help`.
3. Ask your agent for a task, for example "is there a skill for editing videos?".
4. The skill checks the skills.sh leaderboard, then runs `npx skills find <keywords>` if nothing fits.
5. It vets results by install count, source reputation and GitHub stars, then shows the options and install commands.
6. Read each skill's SKILL.md before approving the install.
7. Install the one you want with `npx skills add <owner/repo@skill>`.
8. Manage installed skills with `npx skills list`, `check`, `update` and `remove`.

### Not found

The comment keyword FINDER is not needed, because the repo is public. I could not confirm the "over a million skills" figure.
