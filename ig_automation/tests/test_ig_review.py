"""Offline tests for the Telegram review loop: fake vault, fake Hermes send and history, temp files only."""
import importlib
import json
import os
import sqlite3
import sys
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

PLAYBOOK = """# Playbook

## Comedy

### A joke tip

1. Laugh.

**Evidence:** Opinion.

## Coding Agent Configuration and Workflows

### Tip one

1. Do the first thing.
2. Do the second thing.

**Evidence:** Specific instructions; not tested.

**Selected source:** [A](https://www.instagram.com/p/A/).

### Tip two

1. Other step.

**Evidence:** Tested.

## Contradictions

### Not a tip
"""

DIGEST = """---
name: d
---

### Coding agents

* **Worktrunk**: A CLI for worktrees.
\t* [ ] Would save
\t* Why you would care: parallel agents.
\t* Web: [max-sixty/worktrunk (github.com)](https://github.com/max-sixty/worktrunk)
\t* Found via GitHub

* **Other pick**: Something else.
\t* [ ] Would save
\t* Why you would care: reasons.
\t* Web: [x (example.com)](https://example.com/x)
"""

FOCUS = """### Focus 1: Coding

**Act on first** (in this order)

1. **Run doctor.** It cleans files.
   * **Status (2026-10-24):** Vault done.
2. **Read best practices.** Free page.

**Next after that**

* unlazy, a skill. Web: [u (github.com)](https://github.com/u)

### Interest profile

1. **Not an item.** No.
"""


class ReviewLoopTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        lib = root / "vault/ZAIHub/Vault knowledge library"
        (root / "vault/ZAIHub/Interest digest").mkdir(parents=True)
        lib.mkdir(parents=True)
        (root / "vault/ZAIHub/Interest digest/claude - interest digest 2026-11-10.md").write_text(DIGEST)
        (lib / "Focus topics - coding agents and agent skills by claude.md").write_text(FOCUS)
        (root / "playbook.md").write_text(PLAYBOOK)
        (root / "dead_ends.json").write_text(json.dumps([
            {"shortcode": "AAA", "stage": "research", "status": "needs_you", "focus": False, "title": "Old",
             "added_at": "2026-11-01", "list": "other", "url": "https://instagram.com/p/AAA/"},
            {"shortcode": "BBB", "stage": "research", "status": "needs_you", "focus": True, "title": "Focus one",
             "added_at": "2026-11-05", "list": "comment_to_get", "keyword": "GUIDE", "author": "someone"},
            {"shortcode": "CCC", "stage": "research", "status": "queued", "title": "Not mine"}]))
        self.sent = root / "sent.txt"
        fake = root / "hermes"
        fake.write_text(f"#!/bin/sh\ncat >> {self.sent}\necho '=====' >> {self.sent}\n")
        fake.chmod(0o755)
        self.db = root / "state.db"
        con = sqlite3.connect(self.db)
        con.execute("create table sessions (id text, source text, chat_id text)")
        con.execute("create table messages (session_id text, role text, content text, timestamp real, platform_message_id text)")
        con.execute("insert into sessions values ('s', 'telegram', '1')")
        con.commit()
        con.close()
        os.environ.update(IG_VAULT=str(root / "vault"), HERMES_SEND_BIN=str(fake), HERMES_STATE_DB=str(self.db),
                          HERMES_REVIEW_CHAT="1")
        import ig_review
        self.r = importlib.reload(ig_review)
        self.r.OUTPUT_DIR = root / "out"
        self.r.QUEUE_FILE = root / "out/review_queue.json"
        self.r.LOG_FILE = root / "out/review_log.json"
        self.r.LOCK_FILE = root / "out/review.lock"
        self.r.DEAD_ENDS_FILE = root / "dead_ends.json"
        self.r.PLAYBOOK_FILE = root / "playbook.md"
        self.r.SUMMARY_FILE = root / "out/review_summaries.json"
        self.r.simple_tip = lambda d: None
        self.r.simple_focus = lambda d: None  # no Claude call in tests: the short version is used
        self.lib = lib

    def tearDown(self):
        self.temp.cleanup()

    def reply(self, content, after=1.0):
        con = sqlite3.connect(self.db)
        con.execute("insert into messages values ('s', 'user', ?, ?, '9')", (content, self.r.now().timestamp() + after))
        con.commit()
        con.close()

    def queue(self):
        return json.loads(self.r.QUEUE_FILE.read_text())

    def test_playbook_sheet_order_and_reply(self):
        self.r.main(["send", "playbook"])
        sheet = (self.lib / "IG playbook review sheet by claude.md").read_text()
        self.assertLess(sheet.index("Tip one"), sheet.index("A joke tip"))  # coding agents first
        self.assertNotIn("Not a tip", sheet)
        self.assertTrue(self.sent.read_text().startswith("📘 P1 Playbook tip (1 of 3)\nTip one"))
        self.reply('[Replying to: "📘 P1 Playbook tip Tip one"]\n\ntry this weekend')
        self.r.main(["send", "playbook"])
        q = self.queue()["items"]
        self.assertEqual(q["playbook:Tip one"]["status"], "reviewed")
        self.assertIn("* [x] **Tip one** · try", (self.lib / "IG playbook review sheet by claude.md").read_text())
        self.assertIn("P2 Playbook tip (2 of 3)\nTip two", self.sent.read_text())

    def test_no_reply_comes_back_after_three_days(self):
        self.r.main(["send", "focus"])
        self.r.main(["send", "focus"])
        q = self.queue()
        f1 = q["items"]["focus:Run doctor"]
        self.assertEqual((f1["id"], f1["status"]), ("F1", "sent"))
        f1["sends"][-1]["at"] = self.r.stamp(self.r.now() - timedelta(days=3, minutes=1))
        self.r.save_json(self.r.QUEUE_FILE, q)
        self.r.main(["send", "focus"])
        self.assertIn("F1 Focus topic (again, sent 1 times before)", self.sent.read_text())
        log = json.loads(self.r.LOG_FILE.read_text())
        self.assertIn("no reply", [e["event"] for e in log])
        self.assertEqual(len(self.r.focus_items()), 3)

    def test_digest_save_ticks_note_and_vault_tick_counts(self):
        self.r.main(["send", "digest"])
        self.reply("save D1 please")
        self.r.main(["check"])
        note = (self.r.DIGEST_DIR / "claude - interest digest 2026-11-10.md").read_text()
        self.assertEqual(note.count("[x] Would save"), 1)
        self.assertLess(note.index("[x]"), note.index("Other pick"))
        self.r.main(["send", "digest"])  # D2
        Path(self.r.DIGEST_DIR / "claude - interest digest 2026-11-10.md").write_text(note.replace("[ ] Would save", "[x] Would save"))
        self.r.main(["check"])
        self.assertEqual(self.queue()["items"]["digest:https://example.com/x"]["status"], "reviewed")

    def test_deadends_focus_first_and_read_only(self):
        before = self.r.DEAD_ENDS_FILE.read_text()
        self.r.main(["send", "deadend"])
        self.assertIn("X1 Dead end, needs you\nFocus one by @someone", self.sent.read_text())
        self.assertEqual(before, self.r.DEAD_ENDS_FILE.read_text())

    def test_plain_message_without_id_is_ignored(self):
        self.r.main(["send", "focus"])
        self.reply("done with the laundry")
        self.reply("P1 is a parking spot")
        self.r.main(["check"])
        self.assertEqual(self.queue()["items"]["focus:Run doctor"]["status"], "sent")

    def test_reply_before_send_does_not_count(self):
        self.reply("reviewed F1", after=-100)
        self.r.main(["send", "focus"])
        self.r.main(["check"])
        self.assertEqual(self.queue()["items"]["focus:Run doctor"]["status"], "sent")


if __name__ == "__main__":
    unittest.main()
