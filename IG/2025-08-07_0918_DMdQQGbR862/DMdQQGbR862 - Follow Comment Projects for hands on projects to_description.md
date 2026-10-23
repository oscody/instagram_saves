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

## Research

* Verdict: Partly valid. The post is a short skit on system design with no single resource to find. The advice (confirm payment first, queue payments, unlock after success, use expiring per-user JWTs) is standard practice. The "Projects" material is only sent after a comment, and I found no public copy.
* Checked: 2026-10-23 by claude-sonnet-5-5

### Key steps

1. Take payment through the payment gateway and confirm it succeeded before showing any premium content.
2. Put payment requests on a message queue so they are stored durably and processed asynchronously, which protects against lost transactions at peak load.
3. Have the payment service consume from the queue and record the result.
4. Only after the payment succeeds, have the content service unlock the content.
5. Serve the content from S3 through links protected by a JWT that expires and is tied to one user, so links can't be shared.

### Not found

The "Projects" resource list is sent only after commenting on the reel. I did not search the web or the vault for it, and I found no public copy.
