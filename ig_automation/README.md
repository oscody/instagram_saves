# ig_automation

The Instagram pipeline: `export_chat_links.py` exports the links, `download.py` downloads the media, `transcribe.py` turns reel audio into text, `describe.py` reads on screen text on the Hailo-10H and writes a title, summary and note for each post (Claude, or Qwen2.5 on the Hailo when Claude is out of usage). `run_pipeline.py` runs the last three in batches until everything is done.

`export_chat_links.py` exports the posts and reels shared in one Instagram DM chat to a JSON file. Each later run adds only links it has not saved before.

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

* **Python environment:** the script uses the virtual environment of the sibling project, `../Instagram-Saves-Engine/.venv`, which already has the two packages it needs, `requests` and `yt-dlp`. There is no separate environment for this folder.
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
* `scan` records how far the script has read the chat. Do not edit it.

## How it works

1. **Log in:** loads the Instagram cookies from Firefox.
2. **Find the chat:** pages through your DM inbox until a thread's username or title matches.
3. **Read messages:** calls Instagram's private web API (the same kind of call `sync.py` makes) and reads 50 messages per page, newest to oldest. It pauses 1.5 to 3.5 seconds between pages and backs off when Instagram rate-limits.
4. **Pick out links:** keeps shared reels (`clip`), shared posts (`media_share`), IGTV shares (`felix_share`), newer share formats (`xma_*`), and Instagram URLs pasted into text messages. Other messages are skipped.
5. **Save:** writes the file after every page, so an interrupted run keeps its progress.

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

All three scripts get the folder from one helper, `post_dir()` in `download.py`. The date never changes, because the exporter never changes a saved post.

### How it works

* **Which posts:** newest first, every post with `downloaded: false` and `error: false`. A post marked `downloaded` whose files are missing from its folder is downloaded again.
* **Reels:** yt-dlp with the Firefox cookies (`--remux-video mp4`), then ffmpeg makes a 16 kHz mono `.mp3` for transcribing. yt-dlp is never self updated.
* **Photos and carousels:** no yt-dlp. The script asks Instagram's API for the post's media and saves the largest version of each image, or video slide, in slide order. A `/p/` link that turns out to be a video is handled like a reel. The record's `type` is corrected from the API.
* **After each post:** `files` lists the files written, `downloaded` becomes `true` and `error` becomes `false`, and `iambogle.json` is saved, so an interrupted run keeps its progress.
* **On failure:** `downloaded` stays `false` and `error` gets the reason, for example `HTTP 400 on /media/.../info/` for a deleted or private post. Later runs skip it unless you pass `--retry-failed`.
* **Pauses:** 5 to 12 seconds between posts, to avoid Instagram rate limits.

### Options

| Option | What it does |
| --- | --- |
| `--limit N` | Download at most N posts, the newest that still need it. Without it, every post that needs it is downloaded, which takes hours |
| `--retry-failed` | Also try posts whose `error` is set |
| `--shortcode CODE` | Only this post. Can be given more than once |
| `--dry-run` | List the posts that would be downloaded, with their file names, then stop |
| `--json PATH` | Export file to read and update. Default: `output/iambogle.json` |
| `--ig-dir DIR` | Folder for the post folders. Default: `../IG` |
| `--min-sleep`, `--max-sleep` | Pause between posts, in seconds. Default: 5 and 12 |

## Transcribe the reels: `transcribe.py`

`transcribe.py` turns the `.mp3` of each downloaded reel into text with faster-whisper on the CPU (`base` model, int8, the same settings as the first test on this Pi). Run it after `download.py`, never at the same time as another script.

```
cd /home/homepi/Work/ig/instagram_saves/ig_automation
../Instagram-Saves-Engine/.venv/bin/python transcribe.py --limit 3
```

The transcript goes next to the audio, as `<shortcode> - <title>_transcript.txt` in the post's folder.

### How it works

* **Which posts:** newest first, every post with `downloaded: true`, `transcribed: false`, `error: false` and an `.mp3` in `files`. Photo and carousel posts have no audio, so they are skipped and keep `transcribed: false`.
* **No speech:** a reel with only music or silence gets an empty transcript and still `transcribed: true`, so it is not tried again every run. Music with lyrics comes out as the lyrics.
* **Trust the folder:** a post marked `transcribed` whose transcript file is gone is transcribed again. A post whose `.mp3` is gone gets `downloaded: false`, so the next `download.py` run fetches it again.
* **After each post:** `transcribed` becomes `true`, and `iambogle.json` is saved. The transcript is not added to `files`, which lists only downloaded media.
* **On failure:** `error` gets the reason, and later runs skip the post unless you pass `--retry-failed`.
* **Speed:** about 2 to 3 times faster than real time on the Pi 5 (54 seconds of audio in 20 seconds). The model loads once per run.
* **Cool down:** transcribing keeps all 4 CPU cores busy, and without a fan the Pi reaches 85 °C and throttles after about 4 minutes. So before each reel the script reads the CPU temperature (`/sys/class/thermal/thermal_zone0/temp`). At `--max-temp` (80 °C) or above it pauses, checking every 15 seconds, until the CPU is down to `--resume-temp` (70 °C). If a single pause reaches `--max-wait` (10 minutes) it carries on anyway, with a warning. Each reel's log line shows the CPU temperature, and the final line shows the total time and how much of it was cooling.

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
* `IG/<folder>/<base>_description.md`: a note with the title, summary, who wrote it, the caption, the transcript and the on screen text. Front matter: `shortcode`, `url`, `type`, `author` (the Instagram account), `shared`, `described_by`, `described_at`.
* In `iambogle.json`: `ai_title`, `summary`, `described_by` (the model, for example `claude-haiku-5-5` or `qwen2.5-1.5b-instruct (hailo)`), `described_at` (date), and `described: true`. `author` was already taken by the Instagram account, so the model goes in `described_by`.

Example (photo post `Db-54v5IBSj`):

* `ai_title`: "MacKenzie Scott's Fellowship Launches AI Solutions for Black Community Issues"
* `summary`: "The Marshall Heights Community Development Organization launched a dedicated AI fellowships for Black men focused on solving pressing community issues. ..."

### How it works

1. **Picks posts:** newest first, `downloaded: true`, `described: false`, `error: false`. Reels wait until they are transcribed. Posts whose files are missing get `downloaded: false` so `download.py` fetches them again.
2. **Frames first, on the CPU,** with ffmpeg, before touching the Hailo.
3. **Takes the Hailo:** checks the chip with `hailortcli fw-control identify`, takes the hailo-mcp lock (`$XDG_RUNTIME_DIR/hailo-mcp.lock`, so hailo-mcp requests wait), and stops hailo-ollama (`sudo -n systemctl stop hailo-ollama`, allowed without a password by `/etc/sudoers.d/hailo-ollama`).
4. **OCR stage:** every image of every post. The raw text goes to `_ocr.txt`. A spell corrected copy (Hailo's SymSpell corrector, which splits run together words like `SCOTTLAUNCHED`) goes to the LLM. hailo-ollama is started again right after.
5. **Claude stage** (default `--backend claude`): one `claude -p` run per post with `--safe-mode --strict-mcp-config` (no CLAUDE.md, hooks, plugins or MCP servers), only the `Read` tool (to open up to 6 of the post's images), and `--json-schema`, so the answer is always `{"title", "summary"}` and needs no cleaning. About 6 seconds per post. If a post fails, it is left for the Hailo. If the usage limit is hit (exit with a "hit your limit" style message or HTTP 429), Claude stops and every remaining post goes to the Hailo.
6. **Hailo title and summary stage** (only for posts Claude did not do, or every post with `--backend hailo`): takes the Hailo again, then two short questions per post to Qwen2.5, one for the title and one for the summary. The small model does not follow format instructions well, so its answers are cleaned in code (`tidy_summary`): markdown and "Title:" labels removed, talk about the task removed ("Sure, here's a summary:", "The summary of the Instagram post is:", any sentence mentioning "summary"), sentences that repeat an earlier one dropped, at most 3 sentences, and no cut off fragment at the end. Telling it in the prompt not to mention the request made it worse (it repeated the instruction), so the prompt stays plain.
7. **Gives the Hailo back:** hailo-ollama is always started again and the lock released, even after an error or Ctrl+C.

Each post is saved to `iambogle.json`, and its note written, as soon as it is done, so an interrupted run keeps every finished post.

### Upgrading Qwen posts to Claude

```
../Instagram-Saves-Engine/.venv/bin/python describe.py --upgrade --limit 50
```

`run_pipeline.py` also runs it after each batch (see below), so you only need it by hand when the pipeline is not running. Each upgraded post gets Claude's title and summary, `described_by` and `described_at` change, and its note is rewritten. The Qwen text is replaced, but the log keeps the old title.

### Log

Every run is printed and also appended to `output/describe.log`, so you can follow runs over time:

* `=== describe.py (backend claude, ...)` or `(upgrade, ...)` starts each run
* `Claude <shortcode>: <title>` for each post Claude did, and `LLM <shortcode>: <title>` for each post the Hailo did
* `was (Qwen): <old title>` under each upgraded post
* `Claude usage limit reached (...); N posts left, ...` when the limit is hit
* The last line counts the results: posts per model for a normal run, or upgraded, not upgraded and posts still by Qwen for an upgrade

Check where things stand with `grep -E "===|Done|limit" output/describe.log`.

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

* **Only Claude sees the images.** The Hailo fallback works from text only.
* **No image description on the Hailo.** Qwen2-VL-2B on the Hailo was tried and dropped: on Instagram images it described things that were not there (for example "one person in a red shirt" for a slide showing four men and large text). It answers correctly on ordinary photos, but not on text heavy posts at its 336 x 336 input.
* **Images are skipped for now.** A CPU vision model (`qwen2.5vl:3b` in ollama) was also tested: excellent descriptions that read on screen text far better than the OCR, but about 3 minutes per image, and the Pi overheated and throttled. The tests and the recommended shape for a later optional image step are in the vault note `plan - ig_automation pipeline by claude`.
* **OCR is rough:** it often drops spaces and misreads small text. The spell corrector fixes most joined words but sometimes guesses wrong ("woan" becomes "loan").
* **Qwen2.5 sometimes invents details:** in one test run it made up song titles and cast names for an anime announcement. Treat summaries as a rough guide, not facts.
* **Transcription mistakes carry through:** "CLAUDE.md" heard as "Clod.MD" ends up in the title.
* **Summaries are only as good as the input:** posts with a long caption or clear speech get good summaries. A carousel whose slides are dense small text gets a weak one, mostly from the caption.

## Run everything: `run_pipeline.py`

`run_pipeline.py` runs `download.py`, `transcribe.py` and `describe.py` in batches until every post is done. Each batch takes the newest 100 posts that still need a stage through all three stages, one script after another (never at the same time). Finished posts appear early, and hailo-ollama is back between batches instead of being off for hours.

Start it detached, so it keeps running if the terminal closes:

```
cd /home/homepi/Work/ig/instagram_saves/ig_automation
setsid nohup ../Instagram-Saves-Engine/.venv/bin/python run_pipeline.py --batch 100 > output/pipeline.log 2>&1 < /dev/null &
```

* **Follow it:** `tail -f output/pipeline.log`. Each batch starts with a `Pending:` line counting what is left.
* **Stop cleanly** after the current batch: `touch output/STOP`. Stopping at once (`pkill -INT -f run_pipeline.py`) is also safe: every script saves after each post, and describe always starts hailo-ollama again.
* **It stops by itself** when nothing is left, or when a whole batch makes no progress (for example every download failing because the Instagram login expired).
* **Upgrades:** after describe, each batch also runs `describe.py --upgrade --limit 20`, so posts Qwen described slowly move to Claude. The posts Qwen still holds count as work left, so the runner keeps going until they are done too.
  * If Claude hit its usage limit during that batch's describe, the upgrade is skipped for that batch. Every batch tries again, so upgrades start again by themselves once the limit resets.
  * If only upgrades are left and Claude is at its limit, the batch makes no progress and the runner stops. Start it again later.
  * `describe.py` exits with code 75 when Claude hit its limit; that is how the runner knows.
  * The pipeline log shows `describe.py --limit 20 --upgrade finished ...`, `Upgrade skipped this batch: ...` or `Upgrade stopped: ...`, and the `Pending:` line counts `qwen` (posts still by Qwen). Details for each post are in `output/describe.log`.
* **Options:** `--batch N` (posts per stage per batch, default 100), `--max-batches N`, `--upgrade-batch N` (Qwen posts upgraded per batch, default 20, `0` turns upgrades off).
* Run the exporter first if you want newer posts included; the runner does not export.

## Troubleshooting

* **`No Instagram sessionid cookie in Firefox`:** log into instagram.com in Firefox ESR.
* **`HTTP 401` or `HTTP 403`:** the session expired. Log in again in Firefox.
* **`No DM thread found`:** check the username, or use the chat title exactly as Instagram shows it.
* **`describe.py`: `Another program is using the Hailo`:** hailo-mcp is in the middle of a request. Wait and run again.
* **`describe.py`: `sudo: a password is required`:** the sudoers rule `/etc/sudoers.d/hailo-ollama` is missing or wrong. Check it with `sudo -n -l`.
* **hailo-ollama not running after describe:** start it with `sudo systemctl start hailo-ollama`. describe always tries to, so check its log for the error.
* **A post keeps failing with `HTTP 400`:** it was deleted or made private. It stays in the file with its `error` set and is skipped.
* **`Message types with no links extracted`:** the chat contains a share format the script does not recognize yet. Those messages are skipped, so the script needs updating to handle them.
