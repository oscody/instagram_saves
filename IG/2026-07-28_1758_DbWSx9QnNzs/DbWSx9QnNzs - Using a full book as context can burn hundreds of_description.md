---
shortcode: "DbWSx9QnNzs"
url: "https://instagram.com/p/DbWSx9QnNzs/"
type: "Carousel"
author: "godofprompt"
shared: "Jul 28, 2026, 05:58 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-07"
---

# Turn any book into a Claude skill

The post introduces book-to-skill, an open-source tool that converts a book into a Claude skill that loads one chapter at a time instead of the whole book, cutting token use. It shows the files the tool generates and its three-step workflow, based on a README screenshot.

Written by claude-haiku-5-5.

## What it teaches

1. Run book-to-skill on a book file, folder, or glob, for example: /book-to-skill ./my-book.pdf
2. The tool distills the book into a skill with frameworks, decision rules, anti-patterns, and per-chapter files, structured rather than summarized
3. The generated skill contains a SKILL.md with main concepts and a full index, a separate file per chapter, a glossary of key terms and where they appear, and a document of every technique, pattern, and algorithm in the book
4. Ask the agent to consult the skill by name, for example: /my-book replication, and it reads the relevant chapter and answers from the real content
5. Chapters load only when needed, so with many books installed Claude spends tokens only on the chapter being asked about

## Source

* Link: book-to-skill
* How to get it: comment "Github" on the post and the author will send the link

## Caption

Using a full book as context can burn hundreds of thousands of tokens before you even ask a question.

Someone built an open-source tool to fix that. It’s called book-to-skill, and it turns any book into a skill Claude can consult chapter by chapter. It generates a SKILL.md with the main concepts and index, a separate file per chapter, a glossary, a document of every technique and pattern in the book, and a quick-reference guide.

The best part: chapters only load when you actually need them. Install 20 books, and Claude only spends tokens on the one chapter you’re asking about. A 400-page book can run 200,000+ tokens loaded in full. This way, every answer comes straight from the book’s own content, and hallucinations drop hard.

Completely free and open-source.

Comment “Github” and I’ll send you the link.

Full guide’s in my bio. Go check it out.

## Research

* Verdict: Valid. The public repo virgiliojr94/book-to-skill exists, is MIT-licensed, and generates the files the post describes, loading chapters on demand. The "hallucinations drop hard" line is the author's claim and I did not test it.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [virgiliojr94/book-to-skill (github.com)](https://github.com/virgiliojr94/book-to-skill): repo, found by search, verified, high confidence. README describes /book-to-skill, SKILL.md plus index, per-chapter files, glossary, patterns and cheatsheet, with chapters loaded on demand.
* [alirezarezvani/claude-skills book-to-skill (Tessl listing) (tessl.io)](https://tessl.io/registry/skills/github/alirezarezvani/claude-skills/book-to-skill): page, found by search, not opened, low confidence. A similarly named skill with a similar pipeline. I did not open it, so it may not be the one in the post.

### Already in the vault

* Vault: `2. Areas/Botstack/Pi/pi todo/plan - ig_automation pipeline by claude.md`: Only mentions this post as a test case for the describe pipeline fallback. It does not hold the resource.

### Key steps

1. Install: npx skills add virgiliojr94/book-to-skill (or clone it into ~/.claude/skills/book-to-skill).
2. Run python3 scripts/extract.py --check to see which extractors you have (pdftotext, docling). Scanned PDFs need OCR first, for example ocrmypdf.
3. Convert a book: /book-to-skill <path|folder|glob> [skill-name].
4. The output goes to ~/.agents/skills/<slug>/. It holds SKILL.md (about 4k tokens), chapters/chNN-*.md, glossary.md, patterns.md and cheatsheet.md.
5. Query it with /<slug> <topic>. The agent reads only the relevant chapter.
6. Chapter detection works best when the book has explicit "Chapter N" headings. Keep skills made from third-party books private.

### Not found

I did not check the post's claim that a 400-page book runs 200k+ tokens, or that hallucinations drop. Neither is measured in the README that I saw.
