---
shortcode: "DYdWoL8gASP"
url: "https://instagram.com/reel/DYdWoL8gASP/"
type: "Reel"
author: "wassimyounes_"
shared: "Jun 05, 2026, 05:35 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Streambert: open-source streaming app promo reel

The reel promotes Streambert, a free open-source cross-platform desktop app for streaming and downloading movies, TV shows and anime, and shows its GitHub README on screen. The GitHub link and install instructions are offered only through a comment-to-receive keyword.

Written by claude-haiku-5-5.

## Source

* How to get it: Comment "STREAM" and the GitHub link and install instructions are sent by DM

## Caption

Comment “STREAM” and I’ll send it over.
One open-source developer just out-shipped Netflix, Hulu, Disney, and HBO. With a free desktop app.
Streambert is what happens when a solo dev gets fed up with subscription fatigue, region locks, and tracker pixels — and decides to build the alternative.
What it actually does:
	•	Streams movies, TV, and anime across one unified library
	•	Multithreaded downloads — faster than your browser can pull
	•	Subtitle manager built in
	•	Library mode tracks what you’ve watched and queues what’s next
	•	Trending tab so you discover new stuff every day
	•	Customizable UI
	•	100% open source under GPL-3.0
	•	Zero ads. Zero trackers. Forever.
Cross-platform Electron app. Runs on Mac, Windows, and Linux. One install. No subscriptions. No login walls. No “this content isn’t available in your region.”
The streaming wars built six apps with half the catalog each, 4 minutes of pre-roll ads, and an algorithm designed to keep you scrolling instead of watching.
Streambert is the opposite philosophy: one tool, your library, your machine.
Comment “STREAM” — GitHub link and install instructions in your DMs.
#OpenSource #StreamingApp #IndieDev

## Research

* Verdict: Partly valid. Streambert is a real GPL-3.0 Electron app with the listed features, and its repo is public, so you don't need the DM. The post overstates it: it isn't a Netflix replacement, it streams from third-party providers, and it has had critical CVEs.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Streambert (truelockmc/streambert) (github.com)](https://github.com/truelockmc/streambert): repo, found by search, verified, high confidence. README lists streaming of movies, TV and anime, multithreaded downloads, subtitles, library, trending, UI customization, GPL-3.0, and builds for Mac, Windows and Linux.

### Key steps

1. Open github.com/truelockmc/streambert and download the latest release (2.5.0 or later, because earlier versions have critical CVEs).
2. Windows: run the Setup .exe. macOS: open the universal .dmg and drag the app to Applications. Linux: use the .deb, .pacman or .AppImage. Arch users can install the AUR package streambert-bin.
3. Get a free TMDB API Read Access Token and paste it when the app asks on first launch.
4. For downloads, also install ffmpeg and the separate vid-dl-cli-only program.
5. To build from source, install Node 22.12 or later, run npm install, then npm run dist:linux, dist:win or dist:mac.

### Not found

The DM contents were not checked, but the public GitHub README already has the link and install steps. The "zero trackers, forever" claim is only partly supported: the README says its tracker and ad blocking is imperfect and that the streaming sources may still collect data.
