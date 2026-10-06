# ig_automation

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
      "caption": "follow along as we turn our book series into..."
    }
  ]
}
```

* `sent_at` is when the link was shared, in the Pi's local time.
* `item_type` is the kind of DM message the link came from (`clip`, `media_share` and so on).
* `type` is `Reel`, `Carousel`, `Post` or `Other`.
* URLs use the same format as `sync.py`, so they can feed the `download_media.py` pipeline.
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

Links already in the file are never changed or removed. A run only adds new ones. Each URL is listed once: if a post was shared more than once, the file keeps its newest share.

The first complete pass through a long chat can take 30 to 60 minutes. You can stop it with Ctrl-C at any time, and the next run picks up where it left off.

## Options

| Option | What it does |
| --- | --- |
| `chat` | Username or chat title to export. Default: `iambogle` |
| `--firefox-profile PATH` | Firefox profile to read the cookies from |
| `--output-dir DIR` | Where to write the JSON. Default: `output/` in this folder |
| `--max-pages N` | Stop after N pages (for testing). The next run continues from there |
| `--full` | Ignore the saved file and re-scan the whole chat from scratch |

## Troubleshooting

* **`No Instagram sessionid cookie in Firefox`:** log into instagram.com in Firefox ESR.
* **`HTTP 401` or `HTTP 403`:** the session expired. Log in again in Firefox.
* **`No DM thread found`:** check the username, or use the chat title exactly as Instagram shows it.
* **`Message types with no links extracted`:** the chat contains a share format the script does not recognize yet. Those messages are skipped, so the script needs updating to handle them.

## TODO

* **Normalize pasted links before checking for duplicates.** Shared posts and reels always get a URL like `https://instagram.com/reel/<shortcode>/`, but an Instagram link pasted into a text message is saved exactly as typed, for example `https://www.instagram.com/reel/<shortcode>/?igsh=...`. The two forms do not match, so the same post can be listed twice. Fix: before the duplicate check, reduce pasted links to the standard form (drop `www.` and the query string). Or check duplicates by shortcode instead of URL, which also catches the same post linked as both `/p/` and `/reel/`.
