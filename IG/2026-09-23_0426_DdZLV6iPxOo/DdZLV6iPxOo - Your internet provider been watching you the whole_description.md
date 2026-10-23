---
shortcode: "DdZLV6iPxOo"
url: "https://instagram.com/reel/DdZLV6iPxOo/"
type: "Reel"
author: "raptechpcs_"
shared: "Sep 23, 2026, 04:26 AM"
transcribed_by: "faster-whisper base"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Redirect DNS away from your ISP on Windows

A reel claiming your internet provider sees every site you visit through DNS lookups, shown with a DNS diagram and a Windows network settings screen with manual DNS fields. The final frame promotes a PC optimizer tool.

Written by claude-haiku-5-5.

## What it teaches

1. Your device sends a DNS request before it reaches any website, and per the on-screen diagram that request goes to your ISP first.
2. On Windows, open Network & internet, select the connection's properties, and set the IP/DNS assignment to Manual.
3. Turn on IPv4 and enter 1.1.1.1 (shown on screen as "one dot one dot", named as Cloudflare in the audio) as the Preferred DNS.
4. Fill in the Alternate DNS field, and review the DNS over HTTPS options, which the screen shows set to Off.

## Source

* How to get it: Comment "Tool" for the free PC optimizer shown in the last frame

## Caption

Your internet provider been watching you the whole time and legally selling it. Here's how to take that data back#PrivacyTips #TechTips #PCOptimization #InternetSpeed #raptechpcs_

## Research

* Verdict: Partly valid. Changing Windows DNS to 1.1.1.1 is a real, documented setting, but it only hides lookups from your ISP's resolver. The ISP can still see the IP addresses you connect to, and with DoH off the lookups are unencrypted. The "legally selling it" line is overstated, and the post ends by promoting a PC optimizer tool offered via a comment.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [Cloudflare 1.1.1.1 setup guide (developers.cloudflare.com)](https://developers.cloudflare.com/1.1.1.1/): guide, found by search, not opened, medium confidence. Cloudflare's official documentation for its 1.1.1.1 resolver, which the reel names; I did not open it.

### Key steps

1. Open Settings > Network & internet and choose Wi-Fi or Ethernet, then the connection's properties.
2. Next to DNS server assignment, choose Edit and switch it to Manual.
3. Turn on IPv4.
4. Enter 1.1.1.1 as the Preferred DNS and 1.0.0.1 as the Alternate DNS (Cloudflare's secondary address).
5. Set DNS over HTTPS to On (automatic template) so lookups are encrypted, then Save.
6. Be aware that the ISP can still see the IP addresses you connect to. A VPN is needed to hide those.

### Not found

The "free PC optimizer" in the last frame is only given out after a comment. I did not look for it, and no public copy is known. I did not open the Cloudflare page, so its details come from general knowledge and are unverified.
