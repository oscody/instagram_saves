---
shortcode: "DeSsCPAO771"
url: "https://instagram.com/reel/DeSsCPAO771/"
type: "Reel"
author: "lostandlucky"
shared: "Nov 01, 2026, 09:40 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-03"
---

# GPTs retired; replaced by skill folders

The speaker says OpenAI is retiring GPTs and that they are being replaced by "skills": folders of markdown files plus MCP connectors. A screenshot of OpenAI's help page on GPTs moving to GPT-5 appears, along with an "Anatomy of the Agora Skill Folder" diagram showing a skills/ folder with SKILL.md and references/ files.

Written by claude-haiku-5-5.

## What it teaches

1. Open a new folder on your desktop.
2. Write markdown files in plain English that say when and where to do something, i.e. how you want a task done.
3. Organize them as a skill folder: a skills/ collection holding a skill root folder with a SKILL.md entry point and supporting files such as references/ (the on-screen example lists doc-fetching.md and mcp-tools.md).
4. Optionally download existing markdown skill folders from GitHub repos for free instead of writing them yourself.

## Source

* Link: help.openai.com

## Caption

Just so you know, you can learn a lot more about this with all the links in my bio. I got YouTube videos, I got communities, I got all that good jazz. And I've been teaching this for so much longer than they were ever going to retire.

## Research

* Verdict: Partly valid. OpenAI's help center does describe retiring custom GPTs in favour of plugins (instructions, reference files, connected apps). The reel overstates it: the dates I found cover Enterprise and conflict across pages, and "just markdown files" leaves out the connectors and the custom actions that must be rebuilt.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [Custom GPT retirement and migration FAQ (OpenAI Help Center) (help.openai.com)](https://help.openai.com/en/articles/20001519): page, found by search, not opened, medium confidence. Search snippets say OpenAI plans to retire custom GPTs and move workflows to plugins. The page returned 403 when I opened it, so I only saw the snippets.

### Already in the vault

* Vault: `3. Resources/0. note idea draft/Apps in ChatGPT.md`: Only help.openai.com links on ChatGPT apps and connectors. Nothing on GPT retirement or skills.

### Already in IG saves

* Similar: Web: [Installing 890+ AI agent skills into a project (instagram.com)](https://instagram.com/p/DVFZWnPDA0A/) (`DVFZWnPDA0A`). Points to a free GitHub collection of SKILL.md skills (antigravity-awesome-skills), like the reel's tip to download skills from GitHub.
* Similar: Web: [Antigravity Awesome Skills: 978+ agent skills repo (instagram.com)](https://instagram.com/p/DbQ9SdYqoNk/) (`DbQ9SdYqoNk`). Same free SKILL.md skills repo (antigravity-awesome-skills).
* Similar: Web: [Claude Skills repo overview on GitHub (instagram.com)](https://instagram.com/p/DdZnbGqMfqO/) (`DdZnbGqMfqO`). Also covers skills as folders with a SKILL.md holding instructions and metadata.

### Key steps

1. Create a folder such as skills/<skill-name>/.
2. Add a SKILL.md as the entry point. Write plain-English instructions saying when to use the skill and how the task should be done.
3. Add supporting files in a references/ subfolder, such as doc-fetching.md or mcp-tools.md.
4. For outside tools, add an MCP connector. OpenAI says GPT custom actions don't migrate automatically and must be rebuilt with a supported connector or custom MCP server.
5. To migrate an existing GPT, follow the in-product notice. Per the FAQ, the original becomes read-only and the new plugin starts private.

### Not found

I couldn't open the OpenAI help page (403), so the retirement dates come from search snippets only. The "Agora Skill Folder" diagram has no public source that I could find. The screenshot in the reel shows an older GPT-to-GPT-5 transition page, not the plugin migration FAQ.
