# ig_automation

The Instagram pipeline: `export_chat_links.py` exports the links, `download.py` downloads the media, `transcribe.py` turns reel audio into text, `describe.py` reads on screen text on the Hailo-10H and writes a title, summary and note for each post (Claude, or Qwen2.5 on the Hailo when Claude is out of usage). `run_pipeline.py` runs the exporter and the last three in batches until everything is done. `playback/play_saves.py` plays the downloaded posts on the Pi's screen and logs likes and skips (see [Watch the saves](#watch-the-saves-play_savespy-added-2026-10-14)).

`export_chat_links.py` exports the posts and reels shared in one Instagram DM chat to a JSON file. Each later run adds only links it has not saved before. It reads the chat through Instagram's Android app API. If that fails, it reads new messages through headless Firefox instead (`export_chat_browser.py`).

## Run it

```
cd /home/homepi/Work/ig/instagram_saves/ig_automation
../Instagram-Saves-Engine/.venv/bin/python export_chat_links.py
```

With no argument it exports the chat with `iambogle` (Shemeir Bogle). To export another chat, pass a username or the chat's title:

```
../Instagram-Saves-Engine/.venv/bin/python export_chat_links.py some_username
```

## Setup

* **Python environment:** the script uses the virtual environment of the sibling project, `../Instagram-Saves-Engine/.venv`, which already has the packages it needs: `requests`, `yt-dlp`, and `selenium` (4.50.0, installed 2026-10-08) for the browser fallback. There is no separate environment for this folder.
* **Browser fallback:** needs Firefox ESR at `/usr/bin/firefox-esr`. Selenium fetches the matching geckodriver by itself on first use.
* **No `.env` or `config.json`:** neither project uses a `.env` file, and this script needs no credentials file.
* **Login:** the script reads your Instagram login cookies straight from Firefox ESR, in the profile `~/.config/mozilla/firefox/413ffz8o.default-esr`. Stay logged into instagram.com in Firefox. If the session expires, log in again in Firefox and re-run.

## Output

The export is saved to `output/<chat>.json` in this folder. The default chat goes to:

```
/home/homepi/Work/ig/instagram_saves/ig_automation/output/iambogle.json
```

The file looks like this. Links are listed newest first:

```json
{
  "thread_id": "340282366841710301244258623737610278168",
  "thread_v2_id": "448720033191192",
  "thread_title": "Shemeir Bogle",
  "participants": ["iambogle"],
  "exported_at": "2026-10-06T13:17:23+00:00",
  "scan": {
    "newest_us": 1791257565907780,
    "oldest_us": 1787093838583748,
    "resume_cursor": "...",
    "history_complete": true
  },
  "link_count": 246,
  "links": [
    {
      "sent_at": "Oct 05, 2026, 11:32 PM",
      "item_type": "clip",
      "url": "https://instagram.com/reel/DeArCx4K4x6/",
      "shortcode": "DeArCx4K4x6",
      "type": "Reel",
      "author": "theolduniverseofficial",
      "caption": "follow along as we turn our book series into...",
      "downloaded": false,
      "transcribed": false,
      "described": false,
      "error": false,
      "files": []
    }
  ]
}
```

* `sent_at` is when the link was shared, in the Pi's local time.
* `item_type` is the kind of DM message the link came from (`clip`, `media_share` and so on).
* `type` is `Reel`, `Carousel`, `Post` or `Other`.
* URLs use the same format as `sync.py`, so they can feed the `download_media.py` pipeline.
* `shortcode` identifies the post. Every link is saved in the standard form, `https://instagram.com/reel/<shortcode>/` or `https://instagram.com/p/<shortcode>/`, even when it was pasted with `www.` or a `?igsh=` query string.
* `downloaded`, `transcribed`, `described`, `error` and `files` track the rest of the pipeline (download, transcribe, describe). New links start with `false`, `false`, `false`, `false` and `[]`. The later stages set them; this script only adds them and never changes them, so re-running it never loses pipeline progress. `error` is `false`, or the reason text when a stage failed.
* `transcribed_by` (added 2026-10-14) says which backend made the transcript: `groq whisper-large-v3-turbo` or `faster-whisper base`. Every transcript before that was made by faster-whisper `base` (the only model in the logs), so the 662 older posts were given `faster-whisper base` on 2026-10-14.
* `scan` records how far the script has read the chat. Do not edit it.

## How it works

1. **Log in:** loads the Instagram cookies from Firefox.
2. **Find the chat:** pages through your DM inbox until a thread's username or title matches.
3. **Read messages:** calls Instagram's private Android app API (`i.instagram.com/api/v1/direct_v2/...`) and reads 50 messages per page, newest to oldest. It pauses 1.5 to 3.5 seconds between pages and backs off when Instagram rate-limits.
4. **Pick out links:** keeps shared reels (`clip`), shared posts (`media_share`), IGTV shares (`felix_share`), newer share formats (`xma_*`), and Instagram URLs pasted into text messages. Other messages are skipped.
5. **Save:** writes the file after every page, so an interrupted run keeps its progress.

### Why the app API (changed 2026-10-08)

Until 2026-10-07 the script used the website's API (`www.instagram.com/api/v1`). Since then the website answers every `/direct_v2/` call with a 404 page that says "not logged in", even with a valid login: the website now loads DMs through a new GraphQL system. The Android app API still serves the same calls, so DM calls go there:

* `dm_api_get()` sends them to `i.instagram.com` with an app `User-Agent`, app ID `567067343352427`, and `Authorization: Bearer IGT:2:<base64 of ds_user_id and sessionid>`, built from the same Firefox cookies.
* `api_get()` and `HEADERS` still point at the website, because `download.py` uses them for `/media/<id>/info/`, which still works there.
* The app API returns shared posts as `xma_clip` and `xma_media_share`. They are read from `target_url`, so no parser change was needed.
* Instagram watches the app API more closely for scripts than the website, so keep runs small: a normal catch-up is one or two pages.

The tests (all three options tried, and the long gap test) are written up in the vault note `2. Areas/Botstack/Pi/pi todo/ig export fix - DM api tests by claude`.

### Browser fallback: `export_chat_browser.py`

If the app API fails (any HTTP error, network error or unexpected answer), the exporter logs `App API export failed (...); falling back to reading the chat in Firefox` and reads the new messages through headless Firefox instead. `--browser` forces this route.

* It copies the Firefox profile to a temporary folder and runs Firefox ESR headless on the copy, so the real Firefox and its login are never touched. The copy is deleted at the end.
* It opens the inbox, clicks the chat by its `thread_title`, and reads Instagram's own in page data store (Relay): each `SlideMessage` record links to `content`, then `xma`, which holds `target_url` (the post URL) and `header_title_text` (the author). The posts on screen are cards without links, so the page HTML alone has no URLs.
* A page load holds the newest 20 messages. It then scrolls up with real mouse wheel steps (scrolling from JavaScript loads nothing), 20 older messages per step, until it reaches the newest message already scanned. If 4 steps in a row load nothing, it stops, keeps the links it found, and leaves `newest_us` alone so the next run reads the gap again.
* Each message is reshaped like an app API item, so the same `extract_links()` and `build_record()` handle it. Reels come in as `xma_clip`, posts as `xma_media_share`, often with no caption (see "Empty captions" in Troubleshooting).
* It needs `thread_v2_id` in the export file (the chat's id in the new DM system), which the first app API run saves.
* It only reads new messages. Older history (backfill) is only read through the app API.
* Speed: about 50 seconds to open the chat and scroll back 5 steps (100 messages).

### Runs after the first one

Each run has two phases:

* **Catch-up:** reads from the newest message down and stops at the first message it has already scanned. Once the history is complete, this is the only phase, and a run takes a few seconds.
* **Backfill:** until the whole chat has been read once, the script continues backward from `resume_cursor`, the point where the last run stopped.

Links already in the file are never changed or removed. A run only adds new ones, plus any missing status fields on older links. Each post is listed once, matched by shortcode: if a post was shared more than once, pasted as a link, or linked as both `/p/` and `/reel/`, the file keeps its newest share.

The first complete pass through a long chat can take 30 to 60 minutes. You can stop it with Ctrl-C at any time, and the next run picks up where it left off.

## Options

| Option | What it does |
| --- | --- |
| `chat` | Username or chat title to export. Default: `iambogle` |
| `--firefox-profile PATH` | Firefox profile to read the cookies from |
| `--output-dir DIR` | Where to write the JSON. Default: `output/` in this folder |
| `--max-pages N` | Stop after N pages (for testing). The next run continues from there |
| `--full` | Re-read the whole chat from the newest message. Saved links and their status are kept, so this only finds links a normal run missed |
| `--backfill-pages N` | Read all new messages, then at most N pages of older history. `0` reads no history (before 2026-10-08, `0` meant no limit). Without it, the backfill runs to the start of the chat. `run_pipeline.py` passes 50 |
| `--browser` | Read new messages through headless Firefox (`export_chat_browser.py`) instead of the app API. Happens on its own when the app API fails |

## Carousel audio (fixed 2026-10-15)

Carousel video slides now go through the audio pipeline too. After downloading a
carousel, `download.py` checks each video for an audio stream. It combines the
audio-bearing slides in their original slide order into
`<shortcode>_carousel_audio.mp3` (16 kHz mono). Silent slides are skipped. The
record's `carousel_audio_sources` retains the source video filenames and each
clip's start/end offset in the combined audio.

The existing transcription stage writes a separate
`<shortcode>_carousel_audio_transcript.txt`. Description generation waits for that
transcript and uses it along with the images, caption and OCR. **Raw transcripts
are not copied into Markdown notes**; notes continue to contain the title,
summary, takeaways, source information and caption.

`prepare_carousel_audio(record, folder)` also works on already downloaded media
without fetching Instagram again. Adding audio clears `transcribed` and
`described` so the following stages refresh the post. Existing notes remain on
disk until their replacements are ready. Existing combined audio is reused.

For a post whose audio was backfilled, refresh its note from saved OCR with:

```sh
../Instagram-Saves-Engine/.venv/bin/python describe.py --reuse-ocr --shortcode CODE
```

This uses Claude and the current transcript without taking the Hailo device. It
requires the saved OCR file and retains the old note if Claude fails or reaches
its limit. Use `--redo` too when intentionally refreshing a post still marked
described. The normal timer continues to use its existing OCR/Claude workflow.

The runner holds `output/pipeline.lock` for the whole batch. Maintenance that
writes the export file must hold the same exclusive `flock`; a scheduled run
skips when maintenance already holds it. Run only one standalone writing stage
at a time.

Offline regression checks:

```sh
../Instagram-Saves-Engine/.venv/bin/python -m unittest discover -s tests -p test_carousel_audio.py -v
```

## Daily status report

At the end of each pipeline run, `run_pipeline.py` refreshes `output/daily_status.md`. It reports total completed posts and those completed today, per-stage backlog, descriptions eligible for Claude upgrade, failed posts, the latest successful chat sync, chat history scan progress and the next scheduled timer window. It flags a logged out session, a failed latest export, and identical post errors affecting at least three posts. The sync attempt and success timestamps are stored in `output/pipeline_health.json`.

Every pipeline run appends a timestamped snapshot to `output/daily_status.md` and sends only that new snapshot to the configured Hermes home chat using `hermes send`. If delivery fails, the next run tries again with its newer snapshot. By default it uses `/home/homepi/.local/bin/hermes` and the `telegram` home target; override these with `HERMES_SEND_BIN` and `HERMES_STATUS_TARGET`. It records the latest delivery state in `pipeline_health.json`. `hermes send` uses its configured platform credentials and does not require the gateway process to be running.

The **last successful chat sync** is when the pipeline most recently finished reading the `iambogle` Instagram DM thread for shared post and reel links. It records a successful check even if there were no new links. It is separate from downloading or processing saved posts. `exported_at` in `iambogle.json` is used as a fallback until the pipeline records its first explicit sync result.

The next run window mirrors `~/.config/systemd/user/ig-pipeline.timer`: every two hours from 8 am through 10 pm, with up to 20 minutes of randomized delay. When a download-cap retry is scheduled sooner, the report shows that time instead. The report is generated locally in `output/` and appended once per pipeline run.

## Download the media: `download.py`

`download.py` reads `output/iambogle.json` and downloads each post's media into its own folder in `/home/homepi/Work/ig/instagram_saves/IG/`. Run the exporter first. Run one script at a time: they all write `iambogle.json`.

```
cd /home/homepi/Work/ig/instagram_saves/ig_automation
../Instagram-Saves-Engine/.venv/bin/python download.py --limit 3
```

### Where files go

One folder per post, named by when it was shared in the DM chat and its shortcode: `YYYY-MM-DD_HHMM_<shortcode>`, in 24 hour local time. The date comes first, so the folders sort in date order in any file browser. Files inside are named `<shortcode> - <title>`, where the title is the first line of the caption without hashtags, mentions, emoji or symbols, cut to about 50 characters. A post with no usable caption uses just the shortcode.

```
IG/
├── 2026-08-14_0748_Db-54v5IBSj/                        single photo
│   └── Db-54v5IBSj - Philanthropy in action looks like creating direct.jpg
├── 2026-10-04_2149_DeF0y--HLPy/                        carousel
│   ├── DeF0y--HLPy - Comment prompting and Ill send you the full guide_1.jpg
│   └── ... _2.jpg to _10.jpg, in slide order (video slides are .mp4)
└── 2026-10-05_2332_DeArCx4K4x6/                        reel
    ├── DeArCx4K4x6 - follow along as we turn our book series into an.mp4
    └── DeArCx4K4x6 - follow along as we turn our book series into an.mp3
```

**In git (since 2026-10-14):** only the notes (`IG/*/*_description.md`) are tracked in this repo, so changes to them can be seen and undone; media, transcripts and on screen text stay ignored (`.gitignore`). New notes from the timer show up in `git status` until they are committed. This repo is public on GitHub, so a push makes the notes public.

All three scripts get the folder from one helper, `post_dir()` in `download.py`. The date never changes, because the exporter never changes a saved post.

### How it works

* **Which posts:** newest first, every post with `downloaded: false` and `error: false`. A post marked `downloaded` whose files are missing from its folder is downloaded again.
* **Reels:** yt-dlp with the Firefox cookies and `--impersonate firefox` (needs `curl_cffi`, installed 2026-10-14, so the connection looks like Firefox and not a Python script), `--remux-video mp4`, then ffmpeg makes a 16 kHz mono `.mp3` for transcribing. yt-dlp is never self updated; update it with `pip install -U "yt-dlp[default,curl-cffi]"` in the venv.
* **Captions:** the share in the chat often has no caption. For reels yt-dlp writes an info file whose `description` is the real caption; for photos and carousels the media info has it. Either fills an empty `caption` (added 2026-10-14). The file names are chosen before that, so posts with no caption in the chat are still named by shortcode only.
* **Photos and carousels:** no yt-dlp. The script asks Instagram's API for the post's media and saves the largest version of each image, or video slide, in slide order. A `/p/` link that turns out to be a video is handled like a reel. The record's `type` is corrected from the API.
* **After each post:** `files` lists the files written, `downloaded` becomes `true` and `error` becomes `false`, and `iambogle.json` is saved, so an interrupted run keeps its progress.
* **On failure:** `downloaded` stays `false` and `error` gets the reason, for example `HTTP 400 on /media/.../info/` for a deleted or private post. Later runs skip it unless you pass `--retry-failed`. A failed post leaves no empty folder.
* **Stop on logout (added 2026-10-14):** an error that can mean Instagram sent the request to its login page or a challenge (`Exceeded 30 redirects`, `Failed to parse JSON`, login required, checkpoint, HTTP 401, 403 or 429) triggers one check of the session (a media info request that does not follow redirects). If the session is logged out, the post gets no error, the run stops with exit code 77, and `output/LOGGED_OUT` is written with the reason. No download (and no chat read by `run_pipeline.py`) starts while that file exists. To start again: log in to instagram.com in Firefox, close Firefox, run `tests/download_test.py`, then delete `output/LOGGED_OUT`. If the session is fine, only that post gets the error. Before this, the 2026-10-08 block failed about 960 posts over 5 hours.
* **Network drops:** an error like `Failed to resolve 'www.instagram.com'` leaves the post untouched (the next run tries it again) and waits up to 10 minutes for the network. If it does not come back, the run stops.
* **Pacing (added 2026-10-14):** 20 to 60 seconds between posts (was 5 to 12), at most `--daily-cap` posts (75) tried in any 24 hours across all runs, and none during `--quiet-hours` (11 pm to 8 am). Every try is logged in `output/download_attempts.json`, which the cap counts. At the cap the downloader records the first available slot in `output/download_cap_retry.json`. The pipeline schedules a one shot systemd retry for that slot when it is earlier than the next regular timer run; if the time falls in quiet hours, it moves the retry to the next allowed hour. The regular two hour timer remains a fallback. Instagram does not publish its limits, so these numbers are a cautious guess after the 2026-10-08 block.

### Options

| Option | What it does |
| --- | --- |
| `--limit N` | Download at most N posts, the newest that still need it. Without it, every post that needs it is downloaded, which takes hours |
| `--retry-failed` | Also try posts whose `error` is set |
| `--shortcode CODE` | Only this post. Can be given more than once |
| `--dry-run` | List the posts that would be downloaded, with their file names, then stop |
| `--json PATH` | Export file to read and update. Default: `output/iambogle.json` |
| `--ig-dir DIR` | Folder for the post folders. Default: `../IG` |
| `--min-sleep`, `--max-sleep` | Pause between posts, in seconds. Default: 20 and 60 |
| `--daily-cap N` | Most posts tried in any 24 hours, counting every run. `0` turns it off. Default: 75 |
| `--quiet-hours START-END` | Local hours with no downloads. Empty (`""`) turns it off. Default: `23-8` |

## Transcribe the reels: `transcribe.py`

`transcribe.py` turns the `.mp3` of each downloaded reel into text. Groq's hosted Whisper (`whisper-large-v3-turbo`) does it while the free quota lasts, and faster-whisper on the CPU (`base` model, int8) does the rest (added 2026-10-14). Run it after `download.py`, never at the same time as another script.

```
cd /home/homepi/Work/ig/instagram_saves/ig_automation
../Instagram-Saves-Engine/.venv/bin/python transcribe.py --limit 3
```

The transcript goes next to the audio, as `<shortcode> - <title>_transcript.txt` in the post's folder.

### How it works

* **Groq first (`--backend auto`, the default):** each reel goes to Groq, about 1 second per reel with no CPU heat. The key comes from `GROQ_API_KEY` or the `groq=` line in `ig_automation/.env`; with no key the CPU does everything.
  * Free quota: 2,000 requests a day (the `x-ratelimit-remaining-requests` header; the last line of each run shows what is left), plus limits on audio seconds per hour and per day.
  * A rate limit with a short `Retry-After` (60 seconds or less) is waited out. A longer one means the quota is used up, so the CPU does the rest of that run. The next run tries Groq again.
  * A reel over Groq's 25 MB upload limit, or a Groq error, goes to the CPU instead.
  * Each post records the backend in `transcribed_by` (`groq whisper-large-v3-turbo` or `faster-whisper base`).
  * Quality: on 5 reels Groq matched the local transcripts by 92 to 100% of words (`groq_transcribe_test.py`, 2026-10-08).
* **Which posts:** newest first, every post with `downloaded: true`, `transcribed: false`, `error: false` and an `.mp3` in `files`. Photos and silent videos are skipped and keep `transcribed: false`. Carousels with audio use the combined MP3 prepared by the download step.
* **No speech:** a reel with only music or silence gets an empty transcript and still `transcribed: true`, so it is not tried again every run. Music with lyrics comes out as the lyrics.
* **Trust the folder:** a post marked `transcribed` whose transcript file is gone is transcribed again. A post whose `.mp3` is gone gets `downloaded: false`, so the next `download.py` run fetches it again.
* **After each post:** `transcribed` becomes `true`, and `iambogle.json` is saved. The transcript is not added to `files`, which lists only downloaded media.
* **On failure:** `error` gets the reason, and later runs skip the post unless you pass `--retry-failed`.
* **Speed on the CPU:** about 2 to 3 times faster than real time on the Pi 5 (54 seconds of audio in 20 seconds). The model loads once per run, and only when the CPU is needed.
* **Cool down:** transcribing keeps all 4 CPU cores busy, and without a fan the Pi reaches 85 °C and throttles after about 4 minutes. So before each reel on the CPU the script reads the CPU temperature (`/sys/class/thermal/thermal_zone0/temp`). At `--max-temp` (80 °C) or above it pauses, checking every 15 seconds, until the CPU is down to `--resume-temp` (70 °C). If a single pause reaches `--max-wait` (10 minutes) it carries on anyway, with a warning. Each reel's log line shows the CPU temperature, and the final line shows the total time and how much of it was cooling.

Example from a 16 reel run (2026-10-07, no fan): 9.0 minutes in total, 3.5 of them cooling in 6 pauses of 15 to 75 seconds. The CPU peaked at 83.7 °C (it can pass 80 °C during a long reel, because the check happens between reels) and was not throttling at the end.

```
[7/16] Dc4wqcKgQNk (CPU 79.3C)
  ✓ 225 words, en, 68s of audio in 28s
  CPU at 80.4C, pausing until it is down to 70C
  cooled to 69.4C in 15s
[8/16] DeDMJ5_B2QR (CPU 69.4C)
...
Done. Transcribed: 16 | Failed: 0 | Time: 9.0 min, of which cooling 3.5 min in 6 pauses
```

### Options

| Option | What it does |
| --- | --- |
| `--limit N` | Transcribe at most N posts, newest first |
| `--retry-failed` | Also try posts whose `error` is set |
| `--shortcode CODE` | Only this post. Can be given more than once |
| `--dry-run` | List the posts that would be transcribed, then stop |
| `--backend auto\|groq\|cpu` | `auto`: Groq, then the CPU once the quota is used up. `groq`: Groq only, stop when the quota is used up. `cpu`: faster-whisper only. Default: `auto` |
| `--groq-model NAME` | `whisper-large-v3-turbo` (default) or `whisper-large-v3` |
| `--model NAME` | faster-whisper model. Default: `base`. `small` is more accurate and slower |
| `--language CODE` | Force a language, for example `en`. Default: detect it |
| `--max-temp C` | Pause before the next reel at or above this CPU temperature. Default: 80 |
| `--resume-temp C` | Continue once the CPU is down to this. Must be lower than `--max-temp`. Default: 70 |
| `--max-wait SECONDS` | Longest single pause; carries on after it even if still warm. Default: 600 |
| `--json PATH`, `--ig-dir DIR` | Same as `download.py` |

## Describe the posts: `describe.py`

`describe.py` reads the text in each post's images on the Hailo-10H (PaddleOCR), then writes a short title and summary from the caption, the transcript, that on screen text and the images. By default Claude writes them (headless `claude -p` on the Claude subscription login, no API key, model `haiku`). When Claude hits its usage limit, or fails on a post, the Qwen2.5 1.5B model on the Hailo writes the rest. Each post records which model wrote it. Run it after `download.py` and `transcribe.py`, one script at a time.

```
cd /home/homepi/Work/ig/instagram_saves/ig_automation
../Instagram-Saves-Engine/.venv/bin/python describe.py --limit 3
```

### What it writes

* `IG/<folder>/<base>_frame_1.jpg` to `_frame_3.jpg`: for reels, 3 frames spread evenly over the video. Photos and carousels use their own images (a carousel video slide gives one frame, `<slide>_frame.jpg`).
* `IG/<folder>/<base>_ocr.txt`: the raw text read from the frames or images, repeated lines removed.
* `IG/<folder>/<base>_description.md`: a note with the title, summary, who wrote it, **What it teaches** (numbered steps or rules) and **Source** (a link written in the post, and how to get the material, for example "comment AUDIT, sent by DM"), then the caption. The transcript and the on screen text are not in the note (left out since 2026-10-14; the OCR text was mostly broken fragments); they stay in `<audio>_transcript.txt` and `<base>_ocr.txt` in the same folder, and Claude still reads both. `strip_note_sections.py` removes the `## Transcript` and `## On screen text` sections from older notes (for example after restoring a backup): a dry run by default, `--apply` to change them, and it only removes a section whose text matches the post's own file exactly. On 2026-10-14 it removed the on screen text from 827 notes. The steps and source are only in the note, never in `iambogle.json`, and only Claude writes them (Qwen posts get them when upgraded). Front matter: `shortcode`, `url`, `type`, `author` (the Instagram account), `shared`, `transcribed_by` (posts with audio: `groq whisper-large-v3-turbo` or `faster-whisper base`, added 2026-10-14), `described_by`, `described_at`.
* In `iambogle.json`: `ai_title`, `summary`, `described_by` (the model, for example `claude-haiku-5-5` or `qwen2.5-1.5b-instruct (hailo)`), `described_at` (date), and `described: true`. `author` was already taken by the Instagram account, so the model goes in `described_by`.

Example note (reel `Dd2F41WFQgF`, Claude). Its title and summary are also in `iambogle.json`; the steps and source are only here:

```markdown
---
shortcode: "Dd2F41WFQgF"
url: "https://instagram.com/reel/Dd2F41WFQgF/"
type: "Reel"
author: "bashi_fuirkashi"
shared: "..."
described_by: "claude-haiku-5-5"
described_at: "2026-10-07"
---

# Side projects that impress employers

A tech creator argues that side projects nobody uses mostly help you learn but don't impress employers. ...

Written by claude-haiku-5-5.

## What it teaches

1. Build projects that have real users, not ones only you use.
2. Aim for production-level problems, since those show real engineering experience.
...

## Source

* How to get it: Comment IMPRESSIVE; the creator says he will send the link

## Caption
```

A post Qwen described (or one that teaches nothing) has no "What it teaches" section. Posts described before 2026-10-07 got their note from `--notes-only` and have an empty `described_at`.

### How it works

1. **Picks posts:** newest first, `downloaded: true`, `described: false`, `error: false`. Reels wait until they are transcribed. Posts whose files are missing get `downloaded: false` so `download.py` fetches them again.
2. **Frames first, on the CPU,** with ffmpeg, before touching the Hailo.
3. **Takes the Hailo:** checks the chip with `hailortcli fw-control identify`, takes the hailo-mcp lock (`$XDG_RUNTIME_DIR/hailo-mcp.lock`, so hailo-mcp requests wait), and stops hailo-ollama (`sudo -n systemctl stop hailo-ollama`, allowed without a password by `/etc/sudoers.d/hailo-ollama`).
4. **OCR stage:** every image of every post. The raw text goes to `_ocr.txt`. A spell corrected copy (Hailo's SymSpell corrector, which splits run together words like `SCOTTLAUNCHED`) goes to the LLM. hailo-ollama is started again right after.
5. **Claude stage** (default `--backend claude`): one `claude -p` run per post with `--safe-mode --strict-mcp-config` (no CLAUDE.md, hooks, plugins or MCP servers), only the `Read` tool (to open up to 6 of the post's images), and `--json-schema`, so the answer is always `{"title", "summary", "teaches", "source"}` and needs no cleaning. The prompt asks what the post actually teaches as steps or rules, with ads left out, and a source link only if it is written in the post (never invented, never the account name). About 9 seconds per post. If a post fails, it is left for the Hailo. If the usage limit is hit (exit with a "hit your limit" style message or HTTP 429), Claude stops and every remaining post goes to the Hailo.
6. **Hailo title and summary stage** (only for posts Claude did not do, or every post with `--backend hailo`): takes the Hailo again, then two short questions per post to Qwen2.5, one for the title and one for the summary. The small model does not follow format instructions well, so its answers are cleaned in code (`tidy_summary`): markdown and "Title:" labels removed, talk about the task removed ("Sure, here's a summary:", "The summary of the Instagram post is:", any sentence mentioning "summary"), sentences that repeat an earlier one dropped, at most 3 sentences, and no cut off fragment at the end. Telling it in the prompt not to mention the request made it worse (it repeated the instruction), so the prompt stays plain.
7. **Gives the Hailo back:** hailo-ollama is always started again and the lock released, even after an error or Ctrl+C.

Each post is saved to `iambogle.json`, and its note written, as soon as it is done, so an interrupted run keeps every finished post.

### Upgrading Qwen posts to Claude

```
../Instagram-Saves-Engine/.venv/bin/python describe.py --upgrade --limit 50
```

`run_pipeline.py` also runs it after each batch (see below), so you only need it by hand when the pipeline is not running. Each upgraded post gets Claude's title and summary, `described_by` and `described_at` change, and its note is rewritten. The Qwen text is replaced, but the log keeps the old title.

### Log

Describe logs to `output/pipeline.log`, the same file as the rest of the pipeline. Under `run_pipeline.py` its output already goes there. A run by hand is printed and also appended to `output/pipeline.log`, starting with `Run by hand, not by run_pipeline.py`, so every describe run is in one place:

* `=== describe.py (backend claude, ...)` or `(upgrade, ...)` starts each run
* `Claude <shortcode>: <title>` for each post Claude did, and `LLM <shortcode>: <title>` for each post the Hailo did
* `was (Qwen): <old title>` under each upgraded post
* `Claude usage limit reached (...); N posts left, ...` when the limit is hit
* The last line counts the results: posts per model for a normal run, or upgraded, not upgraded and posts still by Qwen for an upgrade

Check where things stand with `grep -E "=== describe|Done|limit|Run by hand" output/pipeline*.log`. Until 2026-10-08 describe also wrote its own `output/describe.log`; its hand runs from 2026-10-07 are now in `pipeline-2026-10-07-part2.log`.

Each model is loaded once per run, not once per post. Each stage opens the Hailo device fresh: on HailoRT 5.1.1, loading the LLM on a device handle that had already held another GenAI model failed with `HAILO_INTERNAL_FAILURE(8)`. The Pi temperature and throttle flag are logged at each stage.

**Speed with Claude:** about 6 seconds per post, plus about 1 second of OCR. It barely loads the Pi.

**Speed on the Hailo:** about 20 seconds per post (OCR takes about 1 second, the two LLM questions the rest), plus about 5 seconds to stop and start hailo-ollama. 20 posts took 6 to 7 minutes.

### Options

| Option | What it does |
| --- | --- |
| `--limit N` | Describe at most N posts, newest first |
| `--retry-failed` | Also try posts whose `error` is set |
| `--redo` | Describe posts again even if `described` is already `true` (after a prompt change) |
| `--shortcode CODE` | Only this post. Can be given more than once |
| `--backend claude\|hailo` | `claude` (default): Claude first, the Hailo for the rest. `hailo`: Qwen2.5 on the Hailo only |
| `--claude-model NAME` | Model for `claude -p --model`. Default `haiku` |
| `--upgrade` | Describe again with Claude the posts Qwen wrote (`described_by` is Qwen, or missing on older posts). Newest first, works with `--limit`. Uses the frames, transcript and `_ocr.txt` already on disk, so the Hailo and hailo-ollama are not touched. On a usage limit it stops; the rest stay Qwen until the next `--upgrade` run. A post Claude fails on keeps its Qwen text |
| `--notes-only` | Run no models. Write the `_description.md` note for described posts that have none (posts described before `described_by` existed get `qwen2.5-1.5b-instruct (hailo)`) |
| `--dry-run` | List the posts that would be described, then stop |
| `--json PATH`, `--ig-dir DIR` | Same as `download.py` |

### Setup it needs (done 2026-10-06)

* The engine venv sees system packages (`include-system-site-packages = true` in `../Instagram-Saves-Engine/.venv/pyvenv.cfg`), for HailoRT (`hailo_platform`) and OpenCV.
* `shapely`, `pyclipper` and `symspellpy` installed in that venv, for the OCR post processing.
* hailo-apps cloned at `~/Work/hailo-apps`: the OCR code and the spell dictionary are imported from `hailo_apps/python/standalone_apps/paddle_ocr`.
* Models in `/usr/local/hailo/resources/models/hailo10h/`: `ocr_det.hef`, `ocr.hef`, `Qwen2.5-1.5B-Instruct.hef`.
* The sudoers rule `/etc/sudoers.d/hailo-ollama`.
* For the Claude backend: Claude Code (`claude` on the `PATH`) logged in to the Claude subscription. Captions, transcripts and images are sent to Anthropic.

### Known limits

* **A post that teaches nothing** sometimes still gets a remark like "not instruction" at the end of its summary.
* **Only Claude sees the images.** The Hailo fallback works from text only.
* **No image description on the Hailo.** Qwen2-VL-2B on the Hailo was tried and dropped: on Instagram images it described things that were not there (for example "one person in a red shirt" for a slide showing four men and large text). It answers correctly on ordinary photos, but not on text heavy posts at its 336 x 336 input.
* **Images are skipped for now.** A CPU vision model (`qwen2.5vl:3b` in ollama) was also tested: excellent descriptions that read on screen text far better than the OCR, but about 3 minutes per image, and the Pi overheated and throttled. The tests and the recommended shape for a later optional image step are in the vault note `plan - ig_automation pipeline by claude`.
* **OCR is rough:** it often drops spaces and misreads small text. The spell corrector fixes most joined words but sometimes guesses wrong ("woan" becomes "loan").
* **Qwen2.5 sometimes invents details:** in one test run it made up song titles and cast names for an anime announcement. Treat summaries as a rough guide, not facts.
* **Transcription mistakes carry through:** "CLAUDE.md" heard as "Clod.MD" ends up in the title.
* **Qwen summaries are only as good as the text input:** posts with a long caption or clear speech get good summaries. A carousel whose slides are dense small text gets a weak one, mostly from the caption. Claude reads the slides itself, so this mostly affects Qwen posts until they are upgraded.
* **Links are often not in the post:** about 384 captions say "comment X and I'll send you..." or "link in bio", while only about 92 captions and 49 on screen texts contain a URL. The note then records how to get the material (the keyword), not a link. Claude is told never to invent one.

## Run everything: `run_pipeline.py`

`run_pipeline.py` runs `download.py`, `transcribe.py` and `describe.py` in batches until every post is done. describe runs with its defaults, so Claude writes the titles, summaries and notes, and the Hailo takes over when Claude is at its usage limit. Each batch takes the newest 100 posts that still need a stage through all three stages, one script after another (never at the same time). Finished posts appear early, and hailo-ollama is back between batches instead of being off for hours.

Start it with one command. It starts itself in the background, so it keeps running if the terminal closes, and prints its PID:

```
cd /home/homepi/Work/ig/instagram_saves/ig_automation
../Instagram-Saves-Engine/.venv/bin/python run_pipeline.py
```

Before it starts, it:

* refuses to start if another `run_pipeline.py` is already running, so two runs never write the export file at once
* checks that `output/iambogle.json` is valid JSON, and does not start if it is not
* moves the last run's `output/pipeline.log` to `output/pipeline-<date>-part<N>.log`, so a new run never overwrites an old log
* writes a warning at the top of the new log when the last run ended without its `Pipeline ran ...` finish line, which means it was cut off by a power cut or a kill (see the Pi shutdown on 2026-10-08). A log with no `=== Batch` line holds only `describe.py` runs by hand, so it gets no warning.
* logs the Pi temperature and throttle flags at the start and at each `=== Batch N ===` line

`--foreground` runs it in the terminal instead, with no log file and none of the log steps.

Each stage runs with `IG_PIPELINE=1` set, which tells `describe.py` its output already goes to the pipeline log, so it does not add a second copy.

* **Follow it:** `tail -f output/pipeline.log`. Each batch starts with a `Pending:` line counting what is left.
* **Stop cleanly** after the current batch: `touch output/STOP`. Stopping at once (`pkill -INT -f run_pipeline.py`) is also safe: every script saves after each post, and describe always starts hailo-ollama again. Since 2026-10-14 describe treats SIGTERM (a plain `kill` or `systemctl stop`) like Ctrl+C, so that is safe too.
* **It stops by itself** when nothing is left, or when a whole batch makes no progress (for example every download failing because the Instagram login expired).
* **Upgrades:** after describe, each batch also runs `describe.py --upgrade --limit 20`, so posts Qwen described slowly move to Claude. The posts Qwen still holds count as work left, so the runner keeps going until they are done too.
  * If Claude hit its usage limit during that batch's describe, the upgrade is skipped for that batch. Every batch tries again, so upgrades start again by themselves once the limit resets.
  * If only upgrades are left and Claude is at its limit, the batch makes no progress and the runner stops. Start it again later.
  * `describe.py` exits with code 75 when Claude hit its limit; that is how the runner knows.
  * The pipeline log shows `describe.py --limit 20 --upgrade finished ...`, `Upgrade skipped this batch: ...` or `Upgrade stopped: ...`, and the `Pending:` line counts `qwen` (posts still by Qwen). Details for each post are in the same log, under each `=== describe.py` line.
* **Options:** `--batch N` (posts per stage per batch, default 100), `--foreground`, `--max-batches N`, `--upgrade-batch N` (Qwen posts upgraded per batch, default 20, `0` turns upgrades off), `--export-every HOURS` (default 6).
* **Export:** each batch starts with `export_chat_links.py --backfill-pages 50`, so posts shared since the last batch go into that batch, and the older history comes in 50 pages per batch. Since 2026-10-14 it reads the chat only when the last export (`exported_at`) is at least `--export-every` hours old (6), because reading it every batch looked like a bot. `--no-export` turns it off. Nothing is read while `output/LOGGED_OUT` exists; the runner stops instead. A failed export does not stop the batch, but the log shows `EXPORT FAILED: no new posts from the chat this batch` with the error above it (added 2026-10-08, after the export failed quietly for a day).

## Watch the saves: `play_saves.py` (added 2026-10-14)

Plays the downloaded posts back to back on the Pi's screen with mpv. Both files are in `playback/`: `play_saves.py` and its mpv key script `saves_log.lua`. The watch log and playlist stay in `output/`. Reels play through, photos and carousel slides stay up 6 seconds. A carousel is one post: next and previous jump past all its slides.

```
../Instagram-Saves-Engine/.venv/bin/python playback/play_saves.py                     # unseen first, newest first
../Instagram-Saves-Engine/.venv/bin/python playback/play_saves.py --topic ai --type reel
../Instagram-Saves-Engine/.venv/bin/python playback/play_saves.py --dry-run --limit 20  # print the list only
../Instagram-Saves-Engine/.venv/bin/python playback/play_saves.py --report              # likes and skips per author and type
```

Options: `--order newest | oldest | random | liked-first | unseen-first`, `--topic WORD`, `--type reel | carousel | post`, `--author NAME`, `--limit N`, `--include-skipped` (posts skipped twice are left out otherwise), `--image-seconds N`.

Keys (from `saves_log.lua`): `l` like, `n` or `→` next post, `p` or `←` previous post, `Space` pause, `i` title and summary, `o` save the post's link to the log, `+` / `-` photo time, `q` quit.

* **Needs mpv:** `sudo apt install mpv`.
* **Over SSH** it sets `WAYLAND_DISPLAY=wayland-0`, so the video opens on the HDMI screen.
* **Log:** `output/watch_log.jsonl`, one line per post: `finished`, `partial` (moved on after half), `skip` (moved on before half), `quit` (closed mpv mid post, the post stays unseen), plus a `like` line when `l` is pressed and an `open` line for `o`.
* **Read only:** it never writes `iambogle.json` and never talks to Instagram. Likes stay on the Pi.
* Also writes `output/playlist.m3u`, `output/playlist_index.json` and a cache of video lengths, `output/video_durations.json`.

## Timer (added 2026-10-14)

A systemd user timer runs one short batch every 2 hours from 8 am to 10 pm, each up to 20 minutes late at random: `run_pipeline.py --batch 10 --max-batches 1`. With the daily cap that is about 75 downloads a day, so the backlog of about 1,300 posts takes about 18 days. Lingering is on, so it runs without a login.

* Units: `~/.config/systemd/user/ig-pipeline.timer` and `ig-pipeline.service` (`Type=forking`, because the runner starts itself in the background; `PATH` includes `~/.local/bin` for `claude`).
* Check: `systemctl --user list-timers ig-pipeline.timer`, and `tail -f output/pipeline.log`
* Pause: `systemctl --user disable --now ig-pipeline.timer`. `output/PAUSED` is an additional guard that makes any timer or manual pipeline invocation exit without work. To resume, remove `output/PAUSED` and run `systemctl --user enable --now ig-pipeline.timer`.
* Runs that finished today share `output/pipeline.log`; a log from an earlier day, or a run that was cut off, is still moved to `pipeline-<date>-part<N>.log`.
* A batch that downloads nothing because of the cap or the quiet hours logs `made no progress, stopping`. That is expected.

## Troubleshooting

For the manual, resumable knowledge synthesis script, see [Saved Instagram knowledge playbook](playbook/README.md).
Its output stays in `../knowledge_library/`, outside the vault. Run `python3 playbook/build_playbook.py --dry-run`
to inventory inputs. Run `python3 -u playbook/build_playbook.py --stage topics` first to save the topic library,
then `python3 -u playbook/build_playbook.py --stage playbook` to build from those groups with GPT-6 Astra.

* **A video plays with no sound:** the sound is in the `.mp4` (an AAC audio track, check with `ffprobe -v error -show_entries stream=codec_type,codec_name -of csv=p=0 FILE.mp4`). Instagram reels come down as VP9 video with AAC audio, an unusual mix: VS Code and Obsidian play VP9 but have no AAC support, so they show the picture with no sound. VLC plays them fine. The separate `.mp3` is a copy of the audio made on purpose for transcribe. Not fixed yet; options are to ask yt-dlp for H.264 (`-S vcodec:h264`, new downloads only) or convert the audio of existing videos to Opus in a `.webm`.
* **`No Instagram sessionid cookie in Firefox`:** log into instagram.com in Firefox ESR.
* **`HTTP 401` or `HTTP 403`:** the session expired. Log in again in Firefox.
* **`No DM thread found`:** check the username, or use the chat title exactly as Instagram shows it.
* **`HTTP 404 on /direct_v2/...` with a "not logged in" page:** this is not a login problem. It is what the website API answers for DMs since 2026-10-07 (see "Why the app API"). If the app API starts answering this way too, the exporter falls back to the browser.
* **`App API export failed (...); falling back to reading the chat in Firefox`:** the app API stopped working. New posts still come in through the browser, but older history does not. Check the error; if Instagram blocked the app API, consider making `--browser` the default.
* **Browser fallback: `No thread_v2_id in the export file yet`:** run the exporter once while the app API works, or add `"thread_v2_id"` to the file by hand (`448720033191192` for the iambogle chat).
* **Browser fallback: `Unable to locate element` on the chat title:** the chat is not in the first screen of the inbox, or its title changed. Open it once in Firefox so it moves up, or check `thread_title` in the export file.
* **Browser fallback: `Browser did not scroll back to the last scanned message`:** scrolling stopped loading older messages. The links it found are kept and the next run reads the gap again.
* **`describe.py`: `Another program is using the Hailo`:** hailo-mcp is in the middle of a request. Wait and run again.
* **`describe.py`: `sudo: a password is required`:** the sudoers rule `/etc/sudoers.d/hailo-ollama` is missing or wrong. Check it with `sudo -n -l`.
* **hailo-ollama not running after describe:** start it with `sudo systemctl start hailo-ollama`. describe always tries to, so check its log for the error.
* **Empty captions (found 2026-10-08):** shares in the new DM format (`xma_clip`, `xma_media_share`) often carry no caption, and 538 posts were saved with `null`. That crashed describe on 13 posts (`'NoneType' object has no attribute 'strip'`). Fixed: the exporter saves a missing caption as `""` and turns old `null` captions into `""` when it loads the file, and describe treats `null` as empty. The caption itself is still missing: for reels Instagram has it (yt-dlp returned it for all 3 checked), while the 2 photo posts checked really had none. Fetching it in `download.py` is a todo. The 13 failed posts were described again on 2026-10-14.
* **Many downloads fail with `Failed to resolve 'www.instagram.com'`:** the Pi lost its network (Wi-Fi dropped from about 16:45 to 16:50 on 2026-10-08 and 19 posts failed). The posts are fine. `download.py` skips posts with an error and the pipeline does not retry them, so run `download.py --retry-failed --shortcode ...` for them while the pipeline is stopped (two processes must never write `iambogle.json` at once).
* **A post keeps failing with `HTTP 400`:** it was deleted or made private. It stays in the file with its `error` set and is skipped.
* **`Message types with no links extracted`:** the chat contains a share format the script does not recognize yet. Those messages are skipped, so the script needs updating to handle them. Exception: `xma_clip` messages here are reels that were deleted ("Message unavailable", no URL), about 157 in the iambogle chat, so there is nothing to recover.
