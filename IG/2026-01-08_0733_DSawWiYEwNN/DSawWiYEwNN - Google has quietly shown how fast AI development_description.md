---
shortcode: "DSawWiYEwNN"
url: "https://instagram.com/p/DSawWiYEwNN/"
type: "Carousel"
author: "daytrading"
shared: "Jan 08, 2026, 07:33 AM"
described_by: "claude-haiku-5-5"
described_at: "2026-10-08"
---

# Google's guide to building a financial analyst assistant

The carousel promotes a Google Cloud video, titled "How to build a financial analyst assistant with Vertex AI Studio & Gemini in under 10 minutes," which shows building an assistant that turns earnings reports into an interactive tool. The caption describes the approach as guided prompting in Vertex AI Studio with Gemini 3.

Written by claude-haiku-5-5.

## What it teaches

1. Start from raw documents, such as dense earnings reports, and use guided prompting to turn them into structured outputs.
2. Build the app in Vertex AI Studio with Gemini 3 rather than through manual setup.
3. Iterate on prompts and evaluate the results.
4. Automate the steps so the tool is ready for real analytical workflows.

## Caption

Google has quietly shown how fast AI development is changing by demonstrating that a fully working financial analyst assistant can be built in minutes, turning dense earnings reports into something interactive and usable almost instantly. 📄🤖

The walkthrough focuses on reducing developer friction by letting users move from raw documents to structured outputs and applications through guided prompting rather than traditional manual setup or long development cycles.

By using Vertex AI Studio with Gemini 3, the process highlights how prompt iteration, evaluation, and automation can replace many steps that once required engineering teams, while still producing tools ready for real analytical workflows.

The release reflects how large platforms are shifting toward AI systems that anyone can assemble and scale, blurring the line between experimenting with models and deploying production software.

Follow us (👉@artificialintelligenceee) for everything latest from the AI world.

Source: Google

## Research

* Verdict: Valid. The Google Cloud video exists under that exact title, and a write-up of it matches the post's description. The caption's "Gemini 3" and "quietly shown" are embellishments I couldn't confirm.
* Checked: 2026-10-23 by claude-sonnet-5-5

### Resources

* [How to build a financial analyst assistant with Vertex AI Studio & Gemini in under 10 minutes (YouTube) (youtube.com)](https://www.youtube.com/watch?v=e8hehBcYU7E): video, found by search, verified, medium confidence. The page title matches the post exactly, but the channel and description didn't load, so I couldn't confirm it's Google Cloud's upload.
* [StartupHub summary of the video (startuphub.ai)](https://www.startuphub.ai/ai-news/ai-video/2025/googles-vertex-ai-studio-accelerating-ai-development-from-concept-to-production/): page, found by search, verified, medium confidence. Describes the same demo: a PDF earnings report turned into JSON and then a Sankey app in Vertex AI Studio.

### Key steps

1. Open Vertex AI Studio in Express Mode. It needs no Google Cloud account or credit card.
2. Give Gemini a PDF earnings report and ask it to extract revenue, cost of goods sold and operating expenses as structured JSON.
3. The first plain prompt gave a hard-to-parse list. Run the /prompt refine command, which adds an agent persona, explicit instructions and an example JSON format.
4. Generate an API key with one click.
5. Run the /build command with the refined prompt to generate a web app that shows the data as a Sankey diagram.
6. Move to a full Google Cloud project when ready for production. Your saved work carries over, and version history lets you revert changes.
7. Optionally chain steps and add tools such as Google Search, database lookups or custom APIs.
8. Share read-only links with people who don't use GCP.

### Not found

I couldn't confirm the video's channel, so I haven't verified it's Google Cloud's official upload. I also found no evidence that the demo uses Gemini 3. The vault note listed for this creator is unrelated (it's about paid trading groups).
