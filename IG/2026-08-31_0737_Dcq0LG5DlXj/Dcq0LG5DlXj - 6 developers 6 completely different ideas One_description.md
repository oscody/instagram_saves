---
shortcode: "Dcq0LG5DlXj"
url: "https://instagram.com/p/Dcq0LG5DlXj/"
type: "Carousel"
author: "activeprogrammer"
shared: "Aug 31, 2026, 07:37 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-15"
---

# Six Developer Projects Making the Internet Creative Again

A carousel showcasing six creative developer projects: a portfolio whose airplane window controls dark mode, ThreeUI's free Three.js components, a bouquet that becomes a scannable QR code, Claude designing its own personal website, a tool that syncs a real iPhone with a 3D model, and a soccer game with no referees.

Written by claude-haiku-5-5.

## What it teaches

1. To use ThreeUI components: copy the prompt or source code for a component.
2. Give the copied prompt or source to an AI coding agent.
3. Customize the theme, lighting, motion, and layout of the component.

## Caption

6 developers. 6 completely different ideas. One reminder: the internet can still be incredibly creative. 🤯

From an airplane window that controls a website’s dark mode ✈️ to a bouquet that becomes a QR code 🌸, developers are experimenting with what websites and software can actually feel like.

There’s also a library of 160+ creative 3D components, Claude designing its own personal website, a live 3D iPhone demo, and even a soccer game with no referees. 💀⚽

Not every project needs to solve a billion-dollar problem.

Sometimes building something weird, beautiful, or fun is enough to inspire thousands of other developers.

Which project would you try first? 👀👇

Follow @activeprogrammer for more creative developer projects, AI, and programming.

Credits:
✈️ Mikey Barton
🎨 Meng To
🌸 Ann Nguyen
🤖 Kevin Ngo
📱 yyyole (source post; original project attribution unclear)
⚽ Repotted

#developer #webdevelopment #threejs #opensource #ai

## Research

* Verdict: Valid. The ThreeUI repo by Meng To exists and matches the post's claim of a free Three.js component library (about 160 free browse results). The other five projects are only credited in the post, and I did not check them.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [ThreeUI Community (MengTo/threeui) (github.com)](https://github.com/MengTo/threeui): repo, found by search, verified, high confidence. The repo opened. It is an MIT-licensed open-source Three.js component catalog by Meng To, with 164 free browse results, which fits the post's "160+".
* [ThreeUI on 21st.dev (21st.dev)](https://21st.dev/@mengto/library/threeui): page, found by search, not opened, medium confidence. It appeared in search results as a listing of the ThreeUI library. I did not open it.

### Already in the vault

* Vault: `ZAIHub/search - competition ideas by claude.md`: Mentions other activeprogrammer posts (Elemental VFX playground in Three.js). It does not cover this post or ThreeUI.

### Key steps

1. Run `npm install @designcodeio/threeui`.
2. Import a component and the stylesheet: `import { AtTheHorizon } from "@designcodeio/threeui"; import "@designcodeio/threeui/style.css";`.
3. For a smaller bundle, import from a subpath such as `@designcodeio/threeui/components/AtTheHorizon`.
4. Some components render full HTML documents. Copy the files from `node_modules/@designcodeio/threeui/lib-dist/assets/` into your public folder, or override the `sourceUrl` or `assetBaseUrl` props.
5. To browse locally, clone the repo and run `npm install` and then `npm run dev`.
6. Alternatively, copy a component's prompt or source from threeui.com and give it to your AI coding agent.

### Not found

I did not check the other five projects: Mikey Barton's airplane-window portfolio, Ann Nguyen's QR bouquet, Kevin Ngo's Claude-designed site, yyyole's iPhone 3D sync, and Repotted's soccer game. The post marks the yyyole attribution as unclear. I did not check the Pro-tier claims (MCP and skills).
