---
shortcode: "DefIicBgCiv"
url: "https://instagram.com/reel/DefIicBgCiv/"
type: "Reel"
author: "claudeai"
shared: "Oct 14, 2026, 09:52 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-15"
---

# Trim outdated CLAUDE.md rules with /doctor

A short video says hard rules in a CLAUDE.md file add reasoning overhead that newer Claude models often don't need. It suggests running /doctor in a project to flag outdated rules, then trimming them.

Written by claude-haiku-5-5.

## What it teaches

1. Run /doctor in your project to get the rules in your CLAUDE.md flagged as outdated.
2. For each flagged rule, ask whether Claude really needs it or whether it is just an extra step of reasoning before the task.
3. Trim or delete the stale rules, since they take up space and use extra tokens.
4. Keep the preferences that are still worth having; Claude Code now automatically saves memories that are relevant to your work.

## Caption

Every hard rule in your CLAUDE.md file adds an extra step of reasoning before Claude Code starts a task. While older models needed that kind of guidance, the latest ones mostly don't.

Run /doctor in your project to flag outdated rules that are slowing things down and using extra tokens. Trimming them tends to improve Claude’s outputs.

## Research

* Verdict: Partly valid. /doctor is a real Claude Code command that checks CLAUDE.md and proposes fixes. The docs describe it as a duplicate and derivable-content check, plus a prompt-audit subcommand. I found no official statement that it flags rules newer models no longer need.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Claude Code commands reference (/doctor, alias /checkup) (code.claude.com)](https://code.claude.com/docs/en/commands): page, found by search, verified, high confidence. Opened it. It lists `/doctor [prompt-audit [path]]` as a setup checkup covering CLAUDE.md problems, with fixes applied after you confirm.
* [Claude Code Hub: /doctor full review (Spanish) (wmedia.es)](https://wmedia.es/es/tips/claude-code-doctor-revision-completa): guide, found by search, verified, medium confidence. Third-party page. It says /doctor flags CLAUDE.md rules that duplicate the committed file or that Claude can infer from the code (v2.1.205+).

### Key steps

1. In a Claude Code session in your project, run /doctor (alias /checkup).
2. Read the findings first. It reports before changing anything.
3. Review the flagged CLAUDE.md items: duplicated rules and content Claude can derive from the code.
4. Approve or reject each proposed fix. Each is shown as a diff before it is applied.
5. Optionally run /doctor prompt-audit [path] to audit your instructions (needs v2.1.283 or later).
6. Manually trim rules that older models needed but newer ones don't. /doctor won't judge that for you.

### Not found

I found no official Anthropic statement that /doctor flags rules as outdated for newer models, or that hard rules add reasoning overhead. The vault note listed only mentions the creator and has nothing on this topic.
