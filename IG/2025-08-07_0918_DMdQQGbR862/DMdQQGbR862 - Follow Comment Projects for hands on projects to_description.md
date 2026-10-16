---
shortcode: "DMdQQGbR862"
url: "https://instagram.com/reel/DMdQQGbR862/"
type: "Reel"
author: "itsnextwork"
shared: "Aug 07, 2025, 09:18 AM"
transcribed_by: "groq whisper-large-v3-turbo"
described_by: "claude-haiku-5-5"
described_at: "2026-10-15"
---

# System design: pay-per-view content unlock flow

A skit in which a colleague is quizzed on designing a pay-per-view content system, with architecture diagrams showing the payment gateway, message queue, payment service, content service and S3 storage. It ends with a remark about hands-on projects and a LinkedIn post.

Written by claude-haiku-5-5.

## What it teaches

1. Confirm payment before showing any premium content, because viewers cannot be made to unsee it.
2. Send payment requests through a message queue so they are stored safely and processed asynchronously, which keeps transactions from being lost during peak hours. The diagram flow is user, payment gateway, message queue, payment service, content service, S3 storage.
3. Unlock the content only after the payment succeeds.
4. Use JSON Web Tokens with an expiration that are tied to a specific user, so access links cannot be shared with friends.

## Source

* How to get it: Caption says to follow and comment 'Projects' for hands-on projects to add to your resume

## Caption

Follow & Comment "Projects" for hands on projects to add to your resume 🤪

Thanks to our lead engineer for the research for this video...

#systemsdesign #softwareengineer
