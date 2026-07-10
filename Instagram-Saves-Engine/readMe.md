cd /Users/bogle/Dev/test-stuff/instagram_saves/Instagram-Saves-Engine
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

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

source .venv/bin/activate
python sync.py

A few practical notes:

- state.json will be created automatically after the first run.
- sync.log will contain runtime logs.
- config.json currently holds credential fields, so keep it local and out of version control.
- Python 3.10 or 3.11 is the safest choice here.

instagram-djboglemusic-2026-07-10-Rk6cAOgC/your_instagram_activity/messages/inbox/shemeirbogle_448720033191192/message_1.html