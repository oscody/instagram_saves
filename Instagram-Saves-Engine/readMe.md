# Instagram Saves Engine

## Setup

```
cd /Users/bogle/Dev/test-stuff/instagram_saves/Instagram-Saves-Engine
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Then configure the app:

1. Edit config.json.
2. Set these values:
   - ig_session_id
   - ig_csrftoken
   - ig_user_id
   - notion_token
   - notion_database_id

The Notion database also needs these properties with these names:

- Instagram Saves as Title
- URL as URL
- Type as Select
- Author as Text
- Status as Select
- Media ID as Text
- Saved as Date
- Caption as Text
- Collection as Select

Run it with:

```
source .venv/bin/activate
python sync.py
```

## Scripts

The pipeline runs in this order: `sync.py` → `download_media.py` → `transcribe_audio.py` → `describe_video.py`.

### sync.py

Fetches your saved posts from the Instagram API (using the session credentials in `config.json`) and writes one markdown note per post to `IG/Notes/`. Each note records the post's URL, author, caption, type, and collection. Progress is tracked in `state.json` so already-synced posts are skipped on later runs; logs go to `sync.log`.

### download_media.py

Reads the `- URL:` line from each markdown note in `IG/Notes/` and downloads the video with yt-dlp into a matching folder under `IG/Media/`, saved as `reel.mp4`. It then extracts the soundtrack to `audio.mp3` with ffmpeg. Folders that already have `audio.mp3` are skipped, and a random delay between downloads avoids rate limiting. Options: `--notes-dir`, `--media-dir`, `--firefox-profile` (for `--cookies-from-browser` when Instagram requires login).

### transcribe_audio.py

Runs faster-whisper over every `IG/Media/<post>/audio.mp3` and writes the transcript to `transcript.txt` in the same folder. Folders with an existing transcript are skipped. Options: `--media-dir`, `--model` (whisper size, default `small`), `--device`, `--compute-type`, `--language`.

### describe_video.py

Describes each `IG/Media/<post>/reel.mp4` with Claude vision. It extracts scene-change frames from the video (saved to a `frames/` subfolder and reused on later runs), sends them along with `transcript.txt` (if present) to the Claude API, and writes the result to `description.txt` in the same folder. Options: `--media-dir`, `--model` (default `claude-sonnet-5`), `--max-frames`, `--scene-threshold`, `--max-width`, `--max-tokens`.

### generate_frames.py

Frame-extraction tester — the same frame sampling as `describe_video.py` but with no API call. Writes scene-change frames from each `reel.mp4` into its `frames/` subfolder so you can inspect what would be sent to Claude. Options: `--media-dir`, `--max-frames`, `--scene-threshold`, `--max-width`.

## Practical notes

- state.json will be created automatically after the first run.
- sync.log will contain runtime logs.
- config.json currently holds credential fields, so keep it local and out of version control.
- Python 3.10 or 3.11 is the safest choice here.

## Reference

instagram-djboglemusic-2026-07-10-Rk6cAOgC/your_instagram_activity/messages/inbox/shemeirbogle_448720033191192/message_1.html

instagram-djboglemusic-2026-07-10-Rk6cAOgC/your_instagram_activity/saved/saved_collections.html

https://chatgpt.com/share/6a51204f-3d14-83ea-964b-d68fc6e99c7f

https://share.gemini.google/LmjC0JuaENig

https://chatgpt.com/share/6a512094-f4d8-83ea-9f81-e6d5f8d3de67
