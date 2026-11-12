---
shortcode: "Dfm3zUdHNBs"
url: "https://instagram.com/reel/Dfm3zUdHNBs/"
type: "Reel"
author: null
shared: "Nov 11, 2026, 02:03 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-11"
---

# Claude skill that finds other skills

The speaker presents a Claude skill that searches a directory of about 700,000 skills, finds the best match for a task you describe, and can add it to your setup. He says it has passed 3 million installs and offers the full setup to anyone who comments "LIBRARY".

Written by claude-haiku-5-5.

## Source

* How to get it: Comment 'LIBRARY' on the post; the setup is sent by the account after the comment

## Caption

Comment ‘LIBRARY’ and I’ll send it over.

## Research

* Verdict: Valid. The skill is Vercel's public "find-skills" on skills.sh. It searches the skills directory and installs matches. Install count is now 4.3M, so the 3M claim holds. The "LIBRARY" comment gate is unnecessary because the install is public.
* Checked: 2026-11-11 by claude-sonnet-5-5

### Resources

* [find-skills (skills.sh page) (skills.sh)](https://skills.sh/vercel-labs/skills/find-skills): tool, found by search, verified, high confidence. Page describes finding and installing skills from the directory, matching the post's description, and lists 4.3M installs, above the 3M the post cites.
* [vercel-labs/skills (skills CLI repo) (github.com)](https://github.com/vercel-labs/skills): repo, in the vault, not opened, high confidence. A vault-adjacent saved-post note (DcgvcNGsEa1) records this repo as the verified home of the skills CLI and find-skills. I did not open it in this run.

### Already in IG saves

* Same: Web: [Top five most-installed Claude skills ranking (instagram.com)](https://instagram.com/p/DcgvcNGsEa1/) (`DcgvcNGsEa1`). Same link: vercel-labs/skills (skills CLI repo).
* Same: Web: [Five Claude plugins to upgrade your workflow (instagram.com)](https://instagram.com/p/DeNy_grv_AM/) (`DeNy_grv_AM`). Same link: vercel-labs/skills (skills CLI repo).
* Same: Web: [Find Skills: searching a million Claude skills (instagram.com)](https://instagram.com/p/DePtyBoAOPd/) (`DePtyBoAOPd`). Same link: vercel-labs/skills (skills CLI repo).
* Similar: Web: [Four boundaries to stop Claude overreaching (instagram.com)](https://instagram.com/p/Dc84Z0-iY5s/) (`Dc84Z0-iY5s`). Shows skills.sh listings for Claude Code skills, but the creator's file is sent by comment and was not identified.

### Key steps

1. Run: npx skills add https://github.com/vercel-labs/skills --skill find-skills
2. Restart Claude Code so it loads the skill.
3. Tell Claude what you want to do, for example "find a skill for writing content".
4. The skill checks the skills.sh leaderboard and runs npx skills find <query>.
5. It favors skills with 1K+ installs, reputable sources and good GitHub stars.
6. Install a match with npx skills add <owner/repo>.
7. Later, run npx skills check or npx skills update to keep skills current.

### Not found

Nothing in the post's own comment-only setup was seen. The public skill covers what the post describes. The "engineer at ForSale" is probably a mishearing of Vercel, since the on-screen text shows Vercel. I did not open the GitHub repo directly.
