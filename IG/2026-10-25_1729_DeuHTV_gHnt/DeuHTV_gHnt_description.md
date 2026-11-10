---
shortcode: "DeuHTV_gHnt"
url: "https://instagram.com/reel/DeuHTV_gHnt/"
type: "Reel"
author: "billy.coder"
shared: "Oct 25, 2026, 05:29 PM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-11-01"
---

# Open-source AR headset: 100° view for $350

A reel comparing the 52-degree field of view of the Army's HoloLens-based headset with an open-source AR headset that shows 100 degrees, using footage from Army tests and Anduril's EagleEye. It also lists the open headset's specs (two 1600 by 1440 screens at 120 fps, controller-free hand tracking) and says its files are public under GPL.

Written by claude-haiku-5-5.

## What it teaches

1. Print the headset shell.
2. Buy about $350 of parts.
3. Follow the assembly drawings.
4. Run the calibration software that comes with the headset.

## Source

* How to get it: Comment VISOR on the post to receive the material

## Caption

The Army paid $21.9 billion for a headset. Somebody gave away the plans for an open source AR headset that sees wider. Yours, for $350.

The Army's program started on Microsoft HoloLens, which shows a soldier 52 degrees, and now belongs to Anduril. The footage through the goggles here is from the Army's own tests and from Anduril's EagleEye, the headset built to replace it. The open one shows you 100 degrees, almost double. Two 1600 by 1440 screens at 120 frames a second, and it tracks your hands with no controllers and no account. You print the shell, buy about $350 of parts, and follow the assembly drawings. The calibration software comes with it.

GPL licensed, 1,823 stars, the mechanical files, the bill of materials, the schematic and the calibration software, all public.

Send this to whoever just bought a headset.

Comment VISOR and I'll send it.

. . .

open source ar glasses, military ar headset, how to make ar glasses, diy augmented reality glasses, homemade ar glasses, eagle eye military headset, diy ar glasses raspberry pi, hololens 2 field of view, ar headset vs vr headset, microsoft ar headset specs

#hololens #anduril #augmentedreality #militarytech #engineering

## Research

* Verdict: Partly valid. The headset is Leap Motion's Project North Star, which is open source and has a public repo with about 1.8k stars. The ">100°" FOV and 1600x1440 at 120 Hz specs match what outlets report. The "$350" cost, the license and the Army comparison were not verified, and the build guide is unfinished.
* Checked: 2026-11-10 by claude-sonnet-5-5

### Resources

* [Project North Star (leapmotion/ProjectNorthStar) (github.com)](https://github.com/leapmotion/ProjectNorthStar): repo, found by search, verified, high confidence. Opened it: Electronics, Mechanical and Software folders, about 1.8k stars, matching the post's 1,823 stars and its list of mechanical files, BOM, schematic and calibration software.
* [Project North Star mechanical folder (BOM and assembly PDF) (github.com)](https://github.com/leapmotion/ProjectNorthStar/tree/master/Mechanical): guide, found by search, verified, high confidence. Opened it: it holds the BOM TSV files, the assembly drawing PDF and printing notes.
* [Community build guide (GitBook) (project-north-star.gitbook.io)](https://project-north-star.gitbook.io): guide, in the post, not opened, low confidence. The repo README points to this host. I did not open it.

### Key steps

1. Open the repo's Mechanical folder and pick a version. Update 3.1 optics are recommended for a first build, since they halve print time and need no side supports.
2. Print the parts on an FDM printer. The author used PLA Pro, 0.25 mm layers, 2 perimeters and 15% infill, and recommends a bed of about 250x200 mm.
3. Order parts from the BOM TSV files (Release 3, Update 3.1 and the Calibration Stand).
4. Press heat-set inserts into the display trays (4 each) and the driver board mount (2).
5. Build each sub-assembly as shown in the assembly PDF. The guide says major sections are missing.
6. Build the calibration stand from its own BOM and drawing.
7. Install the software from the Software folder and run its calibration. The Electronics folder holds the schematics and driver board files.

### Not found

I could not confirm the $350 total cost. The BOM page gives no prices, and builds are generally reported to cost more. I did not verify the Army/HoloLens 52° comparison or the "$21.9 billion" figure. I could not confirm the license type from the repo page, and sources disagree between Apache 2.0 and GPL-3.0. The repo is from 2018-2019 and looks unmaintained, so it is not a new release. The post's "comment VISOR" gate is unnecessary because the repo is public.
