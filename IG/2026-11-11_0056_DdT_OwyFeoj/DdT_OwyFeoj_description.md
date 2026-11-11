---
shortcode: "DdT_OwyFeoj"
url: "https://instagram.com/reel/DdT_OwyFeoj/"
type: "Reel"
author: null
shared: "Nov 11, 2026, 12:56 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-11"
---

# Five free tools to make Claude design better

The creator names five free tools for improving Claude's design and front-end work, showing a generic-looking landing page, a code-and-form editor, and a 3D motorcycle model. Each tool is described briefly in the spoken narration.

Written by claude-haiku-5-5.

## What it teaches

1. Taste: gives Claude explicit design rules so its websites look less generic
2. Impeccable: improves front-end designs using its own design system and provides a live editor to change designs in the browser
3. Playwright CLI: lets Claude run multiple browsers, test a website automatically, and take screenshots to check it works and looks right
4. Awesome Design: gives Claude design systems based on real websites, covering typography, spacing, buttons, and layouts
5. A fifth tool (spoken as 'Image23JS'): Claude recreates an object from an image, such as a bike, as an interactive 3D model using code

## Source

* How to get it: Comment 'FRONTEND' on the post to receive the full list

## Caption

Comment 'FRONTEND' and I'll send it over.

## Research

* Verdict: Valid. All five tools exist as free, public GitHub projects, so the claim holds. The full list is only sent by comment, but the public repos can be found without it. "Image23JS" is img2threejs.
* Checked: 2026-11-11 by claude-sonnet-5-5

### Resources

* [Taste Skill (Leonxlnx/taste-skill) (github.com)](https://github.com/Leonxlnx/taste-skill): repo, in the vault, verified, medium confidence. An earlier saved post's note verified it as an anti-generic-AI-UI frontend skill; search listings agree. I did not open it this time.
* [Impeccable (pbakaus/impeccable) (github.com)](https://github.com/pbakaus/impeccable): repo, found by search, verified, high confidence. An earlier saved post's note verified this free design skill, which has a live-editing mode and design commands; it matches the post's description.
* [Playwright CLI (microsoft/playwright-cli) (github.com)](https://github.com/microsoft/playwright-cli): repo, found by search, verified, high confidence. Opened it: a CLI for coding agents with named sessions, screenshots and browser control, as the post describes.
* [Awesome DESIGN.md (VoltAgent) (github.com)](https://github.com/VoltAgent/awesome-design-md): repo, in the vault, not opened, medium confidence. An earlier saved post's note treated it as the likely "Awesome Design": design-system files from real brands. I did not open it this time.
* [img2threejs (hoainho/img2threejs) (raw.githubusercontent.com)](https://raw.githubusercontent.com/hoainho/img2threejs/master/SKILL.md): repo, found by search, not opened, medium confidence. A search result describes a Claude skill that turns an object image into procedural Three.js code, which fits "Image23JS". This is the raw SKILL.md link; I did not open it.

### Already in IG saves

* Same: Web: [Five Claude Code plugins for better website design (instagram.com)](https://instagram.com/p/DcWQCQdN28T/) (`DcWQCQdN28T`). Same link: Taste Skill (Leonxlnx/taste-skill).
* Same: Web: [Installing Impeccable to improve AI-generated websites (instagram.com)](https://instagram.com/p/DeNaD7lx15E/) (`DeNaD7lx15E`). Same link: Impeccable (pbakaus/impeccable).

### Key steps

1. Taste: in Claude Code run `/plugin marketplace add Leonxlnx/taste-skill`, then `/plugin install taste-skill@taste-skill`.
2. Impeccable: run `npx impeccable install` in your project, then `/impeccable init` and commands like `/impeccable critique <target>`.
3. Playwright CLI: run `npm install -g @playwright/cli@latest`, then `playwright-cli install --skills`.
4. Playwright CLI use: `playwright-cli open <url>`, `snapshot`, `click`, `screenshot`. Use `-s=name` for separate sessions.
5. Awesome DESIGN.md: copy a brand's DESIGN.md from the repo into your project and tell Claude to follow it.
6. img2threejs: install the skill from the repo (the SKILL.md can be copied into your skills folder), then run `/img2threejs Rebuild this object as a Three.js model` with an image.

### Not found

I didn't open the Taste, Awesome DESIGN.md or img2threejs repos in this session. The exact img2threejs install command is unconfirmed. The creator's own full list is only sent via a "FRONTEND" comment.
