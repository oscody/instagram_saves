I read all six scripts, the README, config, state and logs. Short answer: the overall design is good, but a few structural choices will cause trouble as you scale from 10 media folders to ~1,700.

What's already right

- Separate stages that each skip finished work. Every stage checks whether its output file exists (audio.mp3, transcript.txt, description.txt) and skips if so. That makes reruns safe and cheap, and you can re-run a single stage with --overwrite.
- Transcription runs locally with faster-whisper, and Claude only sees sampled frames plus the transcript, not the video. Both choices keep costs low.
- Reading your data export (sync_export.py) is the safer way in. It gets you 1,703 shares with no session cookies and no account risk. sync.py calls Instagram's private API with your sessionid, which can get the account flagged.

What I'd change, most important first

1. Media folders are named after the note title, not the post's shortcode. download_media.py:120 builds the folder path from the note's filename, and that filename comes from the first line of the caption.
   - If you rename or re-sync a note, its media downloads again and the old folder is left orphaned.
   - When a title is already taken, the note gets a -<media_id> suffix instead, so the naming isn't consistent.
   - Fix: name folders Media/<shortcode>/ and put Media Folder: or the shortcode in the note. This matters most with 1,700 notes.
2. There are two ingestion paths that don't line up.
   - sync.py writes to IG/, sync_export.py writes to IG_export/, and the three later stages all default to IG/. So the 201 export notes need --notes-dir/--media-dir passed on every stage, and IG_export/Media is currently empty.
   - sanitize_filename, build_note_title and load_state/save_state are copied between the two scripts. Their state files also can't see each other: one tracks by pk, the other by id= (or shortcode), so the same reel can end up in both trees.
   - Fix: pick one output root, share a small common.py, and deduplicate on shortcode.
3. update_ytdlp() runs on every download run. When self-update isn't available, it force-reinstalls yt-dlp from GitHub master via pip (download_media.py:85). That's slow, it needs the network every time, and it pulls unpinned code on each run. Make it an opt-in --update-ytdlp flag.
4. Photo and carousel posts count as errors. /p/ posts have no video, so yt-dlp fails and they're counted as errors. Either skip them (sync_export.py --reels-only exists but is off by default) or add an image path that downloads the images and describes them with Claude directly. Carousels are probably worth describing.
5. Frame sampling favours the start of the video. -frames:v max_frames keeps the first 10 scene changes (describe_video.py:128), so a fast-cut reel never shows Claude its ending. Extract all scene-change frames, then pick 10 spread evenly across the video.
6. Only reel.mp4 is picked up downstream. download_media accepts .webm, .mkv and .mov, but find_videos only globs reel.mp4. Other formats get audio and a transcript but never a description. Add -f mp4 or --remux-video mp4 to the yt-dlp call.
7. Bulk descriptions should go through the Message Batches API. You'll be running ~1,700 non-urgent requests, and batches cost 50% less. Also consider asking Claude for structured output (a JSON summary plus topics/tags/category) instead of a free-text paragraph. That's what makes a saves collection searchable later, and you can write it back into the note's frontmatter.

Smaller issues

- In sync.py, Saved At is the time the sync ran (utcnow()), not when you saved the post. The collection lookup loop (sync.py:218) does nothing, so every post gets "Saved".
- The README doesn't match the code:
  - It documents Notion setup, but nothing uses Notion.
  - It says --max-width, but the flag is --frame-width.
  - It says Python 3.10/3.11, but your venv is 3.13.
  - The transcribe --model help text says "Default: base", but the default is small.
- All paths are hardcoded to /Users/bogle/.... Resolve them relative to the script or read them from config.json.
- export/state_export.json and sync_export.log are committed, while the root .gitignore excludes the equivalents for sync.py. config.json has never been committed, which is good.
- Notes are written as a list of - Key: value lines, which download_media then reads back with a regex. YAML frontmatter would do the same job and also work with Obsidian and Dataview.

If you only fix two things, make them #1 (shortcode-named folders) and #2 (one output root with shared code). Those are what will hurt once you process all 1,700 posts. I can make those changes if you want.
