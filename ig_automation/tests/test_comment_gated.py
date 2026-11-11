"""Offline tests for the comment limits and follow ups: no browser, no Instagram, no Telegram."""
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import comment_gated as cg
import dead_ends as de


class CommentRulesTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.saved = [(de, n, getattr(de, n)) for n in ("OUTPUT_DIR", "DEAD_ENDS_FILE", "LOCK_FILE")]
        self.saved += [(cg, n, getattr(cg, n)) for n in ("STATE_FILE", "PAUSED_FILE", "OTHER_STOPS", "send")]
        de.OUTPUT_DIR, de.DEAD_ENDS_FILE, de.LOCK_FILE = root, root / "dead_ends.json", root / "dead_ends.lock"
        cg.STATE_FILE, cg.PAUSED_FILE, cg.OTHER_STOPS = root / "state.json", root / "COMMENT_PAUSED", [root / "BLOCKED"]
        self.sent = []
        cg.send = lambda text: self.sent.append(text) or True
        self.noon = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)

    def tearDown(self):
        for module, name, value in self.saved:
            setattr(module, name, value)
        self.temp.cleanup()

    def comments(self, *minutes_ago):
        return {"comments": [{"at": (self.noon - timedelta(minutes=m)).isoformat(), "shortcode": "x"} for m in minutes_ago]}

    def test_hours_gap_and_daily_limit(self):
        self.assertIsNone(cg.why_not_now(self.comments(), self.noon))
        self.assertIn("hours", cg.why_not_now(self.comments(), self.noon.replace(hour=23)))
        self.assertIn("hours", cg.why_not_now(self.comments(), self.noon.replace(hour=3)))
        self.assertIn("minutes ago", cg.why_not_now(self.comments(30), self.noon))
        self.assertIn("limit", cg.why_not_now(self.comments(170, 150, 130, 100), self.noon))
        self.assertIn(cg.daily_limit("2026-11-10"), (2, 3))

    def test_pause_and_download_stops(self):
        cg.pause("test warning")
        self.assertIn("paused", cg.why_not_now(self.comments(), self.noon))
        self.assertIn("paused for", self.sent[0])
        cg.PAUSED_FILE.unlink()
        cg.OTHER_STOPS[0].write_text("{}")
        self.assertIn("BLOCKED", cg.why_not_now(self.comments(), self.noon))

    def entries(self):
        entries = []
        de.upsert(entries, "AAAAAAAA", "research", "comment_to_get", "gated", "r", keyword="ONE")
        de.upsert(entries, "BBBBBBBB", "research", "comment_to_get", "gated", "r", keyword="TWO", focus=True)
        de.upsert(entries, "CCCCCCCC", "research", "comment_to_get", "gated", "r")  # keyword unclear: needs you
        return entries

    def test_next_post_is_focus_first_and_needs_a_keyword(self):
        entries = self.entries()
        self.assertEqual(cg.next_post(entries)["shortcode"], "BBBBBBBB")
        self.assertIsNone(cg.next_post(entries, "CCCCCCCC"))

    def test_reminder_once_then_needs_you(self):
        entries = self.entries()
        entries[0].update(status="commented_waiting", commented_at=(self.noon - timedelta(days=4)).isoformat())
        de.save(entries)
        self.assertEqual(len(cg.follow_ups(self.noon)), 1)
        self.assertEqual(len(self.sent), 1)
        self.assertEqual(cg.follow_ups(self.noon), [])  # only one reminder
        cg.follow_ups(self.noon + timedelta(days=4))
        self.assertEqual(de.find(de.load(), "AAAAAAAA", "research")["status"], "needs_you")

    def test_dm_link_is_saved_and_cleaned(self):
        entries = self.entries()
        commented = self.noon - timedelta(hours=1)
        entries[0].update(status="commented_waiting", commented_at=commented.isoformat(), commented_as=cg.OWN_USERNAME,
                          author="Creator")
        de.save(entries)
        ms = int(commented.timestamp() * 1000)
        ask = [{"timestamp_ms": ms + 5000, "text": 'Want the guide? Follow me and reply "yes"', "url": "", "title": ""},
               {"timestamp_ms": ms - 9_000_000, "text": "old https://old.example.com/x", "url": "", "title": ""}]
        cg.check_dms(self.noon, read=lambda names: {"creator": ask})
        entry = de.find(de.load(), "AAAAAAAA", "research")
        self.assertEqual((entry["status"], entry["dm_checks"]), ("commented_waiting", 1))
        self.assertIn("reply", self.sent[-1])
        self.assertEqual(cg.check_dms(self.noon + timedelta(minutes=30), read=lambda names: self.fail("too soon")), [])
        link = ask + [{"timestamp_ms": ms + 90_000, "text": "Here you go https://site.example.com/guide?fbclid=abc&x=1.", "url": "", "title": ""}]
        cg.check_dms(self.noon + timedelta(hours=3), read=lambda names: {"creator": link})
        entry = de.find(de.load(), "AAAAAAAA", "research")
        self.assertEqual((entry["status"], entry["received_link"]), ("received", "https://site.example.com/guide?x=1"))
        self.assertEqual(len(self.sent), 2)  # one question, one "saved"

    def test_buttons_first_web_button_is_the_link(self):
        card = {"timestamp_ms": 2000, "text": "tap the first button below", "url": "", "loaded": True,
                "buttons": [{"title": "Claude Code", "url": "https://a.example.com/day-18?fbclid=z"},
                            {"title": "PLAYBOOKS", "url": "https://promo.example.com"}]}
        ask = {"timestamp_ms": 1000, "text": "Reply with your email", "url": "", "buttons": [], "loaded": True}
        verdict = cg.judge_dm([ask, card], 500)
        self.assertEqual(verdict["link"], "https://a.example.com/day-18")
        self.assertIn("[buttons: Claude Code, PLAYBOOKS]", verdict["text"])
        tap = {"timestamp_ms": 3000, "text": "Want it?", "url": "", "loaded": True, "buttons": [{"title": "Send me the link", "url": ""}]}
        self.assertIsNone(cg.judge_dm([tap], 500)["link"])
        self.assertEqual(cg.judge_dm([{"timestamp_ms": 9, "text": "", "url": "", "buttons": [], "loaded": False}], 0)["unread_cards"], 1)
        self.assertIsNone(cg.judge_dm([{"timestamp_ms": 9, "text": "follow https://instagram.com/x", "url": "", "buttons": []}], 0)["link"])

    def test_dm_check_skips_posts_you_commented_on_yourself(self):
        entries = self.entries()
        entries[0].update(status="commented_waiting", commented_at=(self.noon - timedelta(hours=1)).isoformat(), author="creator")
        de.save(entries)
        self.assertEqual(cg.dm_targets(de.load(), self.noon), [])


if __name__ == "__main__":
    unittest.main()
