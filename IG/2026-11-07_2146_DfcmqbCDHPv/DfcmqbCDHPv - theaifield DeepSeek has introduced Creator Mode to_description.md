---
shortcode: "DfcmqbCDHPv"
url: "https://instagram.com/p/DfcmqbCDHPv/"
type: "Carousel"
author: "theaifield"
shared: "Nov 07, 2026, 09:46 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-09"
---

# DeepSeek Harness Creator Mode builds plugins from chat

The carousel announces DeepSeek's Creator Mode in its open-source Harness agent, where users describe a tool or interface change in plain English and the agent writes, installs, and tests a plugin. It shows demos including a Pomodoro timer built in about five minutes, a sandbox game, a 3D Transformer visualizer, and a pixel-art style switcher.

Written by claude-haiku-5-5.

## Caption

theaifield 🤯🚨DeepSeek has introduced Creator Mode to DeepSeek Harness, its open-source AI agent application designed to compete with tools like Claude Code. In this mode, users can request custom tools or interface changes in plain English; the agent then writes, installs, and tests the corresponding plugins.

Demonstrations include a Pomodoro timer (built and verified in roughly five minutes), a video editor, a sandbox-style game, and a 3D visualization of how large language models process information. One plugin can even restyle the entire app, with options such as a pixel-art theme. DeepSeek has released the prompts for seven of its demo plugins in English and Chinese so others can recreate or adapt them.

Harness, which follows an “everything is a plugin” architecture, has surpassed 270,000 GitHub stars. It runs on Apple silicon Macs and 64-bit Windows (and via a local web interface), supports models from other providers including Claude, and remains in developer preview. Users are advised to begin in a test environment due to ongoing rapid changes.

➡️ Want to stay ahead in the world of AI? Grab your coffee, relax, and let our newsletter deliver the biggest updates straight to your inbox.

## Research

* Verdict: Valid. DeepSeek Harness is a real MIT-licensed open-source repo with about 278k stars, and press coverage confirms Creator Mode and the seven demo prompts. Some demos were refined over several rounds, so one prompt may not reproduce them exactly.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [deepseek-ai/deepseek-harness (GitHub) (github.com)](https://github.com/deepseek-ai/deepseek-harness): repo, found by search, verified, high confidence. Opened it: MIT license, about 278k stars, and npm and source install steps. The page doesn't mention Creator Mode.
* [DeepSeek releases Creator Mode (Implicator) (implicator.ai)](https://www.implicator.ai/deepseek-releases-creator-mode-allows-deepseek-harness-users/): page, found by search, verified, high confidence. Opened it: it describes Creator Mode and lists the seven demo plugin prompts (3D landmarks, Transformer game, theme switcher, poster tool, video editor, paper reader, usage stats).
* [DeepSeek Harness developer preview page (deepseek.com)](https://deepseek.com/harness/en/): page, found by search, not opened, medium confidence. Official page that appeared in search results; it calls Harness a developer preview. I didn't open it.

### Key steps

1. Install Node.js, then run `npx @deepseek-ai/dsh web`. The web UI opens at http://127.0.0.1:3080. Add `--no-open` to stop it opening a browser.
2. Or build from source: clone the repo, then run `pnpm install`, `pnpm run build` and `pnpm dsh web`.
3. Start in a test environment, because the project is a developer preview and changes quickly.
4. Copy one of DeepSeek's published demo prompts (English or Chinese) into Harness and select the Creator Mode option.
5. Let the agent write, install and test the plugin. Refine it over a few more messages, because some demos took several rounds.
6. Community plugins can be shared on GitHub under the `dsh-plugin` topic.

### Not found

I didn't find the official page that hosts the seven demo prompts, and the GitHub README says nothing about Creator Mode. The platform claims (Apple silicon Macs, 64-bit Windows) and the Claude model support are unchecked. No vault note covers the resource, and no other saved post covers it.
