---
shortcode: "Dcq4KBuJEMQ"
url: "https://instagram.com/reel/Dcq4KBuJEMQ/"
type: "Reel"
author: "100xengineers"
shared: "Aug 31, 2026, 07:38 AM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Scanning Claude skills for malicious code with SkillSpector

The post warns that Claude skills can hide malicious code and credits Nvidia's research on skills across AI agent marketplaces. It presents SkillSpector, an open-source Nvidia scanner that checks an agent skill before installation.

Written by claude-haiku-5-5.

## What it teaches

1. Point SkillSpector at a skill directory, a zip file, or the GitHub URL of a skill.
2. It runs a 71-pattern vulnerability test covering things like prompt injection, data exfiltration, and dangerous code calls.
3. It returns a risk score from 0 to 100; the video names 50 as the cutoff, with anything above 50 flagged.
4. Optionally run SkillSpector as an MCP server so an AI agent scans each new skill before installing it.

## Source

* How to get it: Comment "Skill" to receive the GitHub repo link (per the post)

## Caption

Comment "Skill" to get the GitHub Repo Link 🔗

Your Claude skills might have malicious code hidden inside them which can even hack your PC, and everyone should thank Nvidia for solving this.

So Nvidia did research over 42,000 skills across AI agent marketplaces and found 1 in every 4 agent skills you install could compromise your entire system.

And to tackle this, Nvidia built SkillSpector, which is an open-source scanner that checks any agent skill before you install it.

## On screen text

Research Background
F
be vulnerable
42,000
ZIP
crabracadabra
brand-guidelines.zip
file,
MCP
N
server,
