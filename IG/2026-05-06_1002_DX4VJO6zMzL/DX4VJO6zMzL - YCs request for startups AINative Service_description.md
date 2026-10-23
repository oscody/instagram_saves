---
shortcode: "DX4VJO6zMzL"
url: "https://instagram.com/reel/DX4VJO6zMzL/"
type: "Reel"
author: "tpadumke"
shared: "May 06, 2026, 10:02 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# AI-native service company job-listing workflow

A creator pitches selling finished work as an AI-native service company, shown with a Claude Code prompt on screen for building a client capabilities PDF. The caption and voiceover say the full prompts are sent to people who comment.

Written by claude-haiku-5-5.

## What it teaches

1. Install the JobSpy MCP server (github.com/borgius/jobspy-mcp-server) so Claude can reach Indeed, LinkedIn and Google Jobs.
2. Connect Claude to the MCP and have it pull job listings.
3. Have Claude check the job descriptions and score each listing by how automatable its tasks are.
4. Have Claude generate a proposal PDF with four pages: a cover with the company name and a one-line outcome promise; every listed task reframed as an outcome; how it works (turnaround times, weekly reporting, your approval flow); and a sample output (one follow-up email and one categorized receipt log), matched to the client's industry.
5. Send the proposal to the client.
6. Once the client onboards, set up the infrastructure once.
7. Set up agents for the repetitive tasks and Claude routines connected to the client's Gmail, so incoming client emails are handled by the agents while you approve and send.

## Source

* Link: github.com/borgius/jobspy-mcp-server
* How to get it: Full prompts are sent by comment: comment "job"

## Caption

YC’s #2 request for startups: AI-Native Service Companies.
Stop selling software. Sell the finished work.
The loop: → JobSpy MCP pulls listings from Indeed, LinkedIn, Google Jobs → Claude scores them by how automatable they are → Claude writes the proposal, you send it → Client onboards, you set up the Gmail routine once → Agents handle the repetitive tasks, you approve and hit send
20 clients × $400/mo = $8k MRR. Ten hours a week.
Comment job — I’ll send all the prompts.

## Research

* Verdict: Partly valid. The JobSpy MCP server is real and does pull listings from Indeed, LinkedIn and Google Jobs. The proposal prompts are only sent by comment, and the "20 clients × $400/mo in ten hours a week" income figure is an unsupported pitch.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [jobspy-mcp-server (github.com)](https://github.com/borgius/jobspy-mcp-server): repo, in the post, verified, high confidence. README describes an MCP server with a search_jobs tool covering Indeed, LinkedIn, Google and other job sites, for use with Claude.

### Already in the vault

* Vault: `ZAIHub/search - skillspector - similar ai safety workflows.md`: Only lists another reel by the same creator (free-claude-code proxy). It does not cover this post.

### Key steps

1. Clone the repo and run `npm install`.
2. Set up JobSpy in `../jobSpy`: run `pip install -r requirements.txt` and make `run.sh` executable.
3. Add a `jobspy` entry to `claude_desktop_config.json` that runs `node` on `src/index.js`.
4. Ask Claude to call `search_jobs` with `site_names`, `search_term`, `location` and `results_wanted`. Set `linkedin_fetch_description` to true if you need full LinkedIn descriptions.
5. Ask Claude to score each listing by how automatable its tasks are, then generate the 4-page proposal PDF (cover, tasks as outcomes, how it works, sample output).

### Not found

The creator's full prompts (the capabilities PDF prompt and the scoring prompt) are only sent to people who comment "job". I found no public copy. The server needs a separate JobSpy install, and the README does not link it.
