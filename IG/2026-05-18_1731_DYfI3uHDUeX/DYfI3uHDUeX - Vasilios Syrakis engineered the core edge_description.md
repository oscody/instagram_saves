---
shortcode: "DYfI3uHDUeX"
url: "https://instagram.com/p/DYfI3uHDUeX/"
type: "Carousel"
author: "series"
shared: "May 18, 2026, 05:31 PM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Atlassian engineer's edge infrastructure: Envoy and sidecars

A news-style carousel reporting that Atlassian laid off senior engineer Vasilios Syrakis, who then posted a 38-minute YouTube video on the edge infrastructure he built there. It explains two technical terms from that video, Envoy and the sidecar pattern, in plain English.

Written by claude-haiku-5-5.

## What it teaches

1. Use Envoy, a free and open-source proxy, instead of enterprise load balancers: it is built to scale, handles the same traffic, and costs much less.
2. Use the sidecar pattern for shared concerns such as auth, logging and rate limits, instead of having each team build them separately.
3. Put the sidecar's pieces (service directory, server load balancer, circuit breaker and throttling, service routing) beside each service so one system covers everything.

## Caption

Vasilios Syrakis engineered the core edge infrastructure at software giant Atlassian before being laid off in a corporate pivot toward artificial intelligence.

Instead of posting a generic rant, the veteran systems engineer uploaded a masterclass detailing the precise architecture he built over eight years.

His blueprints showed how to route internet traffic cheaply for a corporation generating over 1.7 billion dollars in quarterly revenue.

True authority is built by letting your high level execution speak for itself, turning a sudden exit into an unshakeable professional monopoly.

Follow @series for more 🤝

## Research

* Verdict: Partly valid. The layoff and the ~38–40 minute video are backed by a transcript page and news write-ups. The carousel's generic Envoy and sidecar advice is a loose summary, and I could not open the YouTube video itself.
* Checked: 2026-10-22 by claude-sonnet-5-5

### Resources

* [I was laid off by Atlassian — transcript & summary (SozAI) (sozai.app)](https://sozai.app/transcript/laid-off-atlassian/index.md): page, found by search, verified, medium confidence. The transcript covers Envoy replacing licensed load balancers, sidecars for auth and rate limiting, and the Sovereign control plane. It does not give the YouTube link.
* [Atlassian laid him off after 8 years (Level Up Coding) (levelup.gitconnected.com)](https://levelup.gitconnected.com/atlassian-laid-him-off-after-8-years-he-responded-by-giving-away-everything-he-knew-46ff04017019): page, found by search, not opened, low confidence. A search result with the matching story. It is member-only and I did not open it.
* [Pplware article on the video (pplware.sapo.pt)](https://pplware.sapo.pt/software/engenheiro-despedido-da-atlassian-publica-video-a-revelar-tudo-o-que-construiu-na-empresa/): page, found by search, not opened, low confidence. A news write-up in search results about the laid-off engineer's video. I did not open it.

### Key steps

1. Envoy is an open-source proxy like Nginx. Its config reloads at runtime through an API, so it can replace licensed enterprise load balancers.
2. Run a control plane (he open-sourced one called Sovereign) that renders Envoy config from templates and pushes it to the proxies.
3. Run shared edge concerns (auth, authorization, rate limiting, logging) as sidecar services next to each Envoy proxy.
4. Provision proxies as code: CloudFormation, with AMIs built using Packer and Salt Stack.

### Not found

The YouTube video URL. Searches only returned secondary write-ups and a transcript page. The vault notes listed only matched the creator name "series" and have nothing relevant. I did not check the "1.7 billion dollars quarterly revenue" caption figure.
