---
shortcode: "DfgbDr-lO4D"
url: "https://instagram.com/p/DfgbDr-lO4D/"
type: "Carousel"
author: "itsnextwork"
shared: "Nov 09, 2026, 03:34 AM"
described_by: "claude-haiku-5-5"
described_at: "2026-11-09"
---

# Claude Code use cases and free project guides

Shows five examples of things people built with Claude, including fixing slow Wi-Fi, a 3D jaw scan viewer, a TV system with a live apartment model, a pothole simulator, and a 3D anatomy figure generator. Each example is paired with a project title and the caption asks viewers to follow and comment "Build" to receive the list.

Written by claude-haiku-5-5.

## Source

* Link: nextwork.ai
* How to get it: Follow the account and comment "Build" to receive the list

## Caption

itsnextwork Follow & comment “Build” for a list of projects guides you can do! 

#claude

## Research

* Verdict: Partly valid. NextWork's project guides exist and match the on-screen titles, but the "free guide" claim is shaky: the Wi-Fi project says Claude Code needs a paid Claude plan. The "Build" comment list is a follow funnel, and the public project index already shows the guides.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [Fix Slow Wi-Fi with Claude Code (NextWork) (nextwork.ai)](https://nextwork.ai/projects/991c3210-71aa-4e2e-a745-ea9081d0533a): guide, found by search, verified, high confidence. Opened it. The title matches the slide, and it covers Claude Code measuring Wi-Fi speed and testing router changes. It needs a paid Claude plan, a Mac and router admin access.
* [Build a Private DICOM Explorer (nextwork.ai)](https://nextwork.ai/projects/4b262351-63f1-453e-afbf-985f9ba383b2): guide, found by search, not opened, medium confidence. Listed on the NextWork homepage. Its title matches the garbled slide text (the 'jaw scan viewer'), but I did not open the page.
* [Customize Your TV with Claude Code (nextwork.ai)](https://nextwork.ai/projects/d1f93300-eaec-401a-876c-d627e974a28b): guide, found by search, not opened, medium confidence. Listed on the homepage and matches the 'TV with no ads' slide. I did not open the page.
* [Rebuild a Street Problem in 3D (nextwork.ai)](https://nextwork.ai/projects/4017b92b-66b3-4ab4-86f8-116faad9dc7d): guide, found by search, not opened, medium confidence. Listed on the homepage and matches the pothole slide's 'Rebuild a Street Problem in 3D'. I did not open the page.
* [Generate Your First Anatomy Figure (nextwork.ai)](https://nextwork.ai/projects/fc800e5d-42ae-42cd-b1c5-0d1d875b6e0d): guide, found by search, not opened, medium confidence. Listed on the homepage and matches the anatomy slide title. I did not open the page.

### Already in IG saves

* Similar: Web: [Video Streaming System Design: CDN and Load Balancing (instagram.com)](https://instagram.com/p/DLwZJleCaHc/) (`DLwZJleCaHc`). Same creator and NextWork project platform, with a comment-keyword funnel.
* Similar: Web: [System design: pay-per-view content unlock flow (instagram.com)](https://instagram.com/p/DMdQQGbR862/) (`DMdQQGbR862`). Same creator (itsnextwork) with the same comment-to-get-projects funnel.
* Similar: Web: [Skit on exposed app data and access control (instagram.com)](https://instagram.com/p/DNPpuMlu9Y6/) (`DNPpuMlu9Y6`). Same creator and NextWork platform, with an 'I want in' comment funnel.

### Key steps

1. Open nextwork.ai and find the project by its title on the projects list.
2. For the Wi-Fi guide: you need a Mac (macOS 13+), Chrome, a paid Claude plan such as Pro, and your router admin password.
3. Install or update Claude Code, make a ~/wifi-fix folder, start a Manual-mode session and connect Claude in Chrome.
4. Build wifi-meter.zsh, which runs networkQuality and logs results to wifi-results.csv. Take a baseline reading.
5. Back up the router settings, then audit band, channel, width, radio mode and power. Write wifi-audit.md with up to 3 reversible changes.
6. Apply one change at a time and re-measure at the same spot. Keep it only if it clearly helps, otherwise restore the old value.
7. Write wifi-report.md with the baseline, final result and rollback values.

### Not found

The 'jaw scan viewer' slide has no clear matching title. The DICOM explorer is my best guess. I opened only the Wi-Fi project page. The other four are from the homepage listing. I did not confirm whether any of them are free. The comment-only 'Build' list was not checked, and the public project index seems to cover it.
