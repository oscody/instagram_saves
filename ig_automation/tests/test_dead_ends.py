"""Offline tests for dead end retries: no Claude, no network, temp files only."""
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import dead_ends as de


def unresolved(text="Could not find the repo anywhere.", cost=0.1):
    return {"verdict": "unresolved", "verdict_reason": text, "not_found": text, "ig_posts": [], "cost_usd": cost}


class RetryTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.saved = {n: getattr(de, n) for n in ("OUTPUT_DIR", "DEAD_ENDS_FILE", "LOCK_FILE", "RESEARCH_FILE", "IG_DIR")}
        de.OUTPUT_DIR = root
        de.DEAD_ENDS_FILE = root / "dead_ends.json"
        de.LOCK_FILE = root / "dead_ends.lock"
        de.RESEARCH_FILE = root / "research.json"
        de.IG_DIR = root / "IG"
        self.saved["post_text"] = de.post_text  # posts with plenty of speech, so "thin input" does not apply
        de.post_text = lambda code, record: {"caption": "", "transcript": "word " * 50, "screen": ""}
        self.results = {}
        self.entries = []

    def tearDown(self):
        for name, value in self.saved.items():
            setattr(de, name, value)
        self.temp.cleanup()

    def add(self, code, kind, reason, focus=False):
        self.results[code] = unresolved(reason)
        de.upsert(self.entries, code, "research", "other", kind, reason, focus=focus)
        de.save(self.entries)
        de.RESEARCH_FILE.write_text(json.dumps(self.results))

    def runner(self, new_result=None, code=0):
        """A stand-in for research.py: writes new_result, then updates the entry like research.py does."""
        calls = []

        def run(shortcode, kind):
            calls.append((shortcode, kind))
            if new_result is not None:
                self.results[shortcode] = new_result
                de.RESEARCH_FILE.write_text(json.dumps(self.results))
                with de.locked():
                    entries = de.load()
                    de.apply_research(entries, shortcode, new_result, {}, set())
                    de.save(entries)
            return code
        run.calls = calls
        return run

    def entry(self, code):
        return de.find(de.load(), code, "research")

    def make_due(self, code):
        entries = de.load()
        de.find(entries, code, "research")["next_retry"] = "2000-01-01"
        de.save(entries)

    def test_not_found_waits_then_retries_twice_then_closes(self):
        self.add("AAAAAAAA", "not_found", "Could not find the repo anywhere.")
        self.assertEqual(de.due(de.load()), [])  # first retry is RETRY_DAYS[0] days away
        self.make_due("AAAAAAAA")
        run = self.runner(unresolved("Still could not find the repo.", 0.2))
        self.assertEqual(de.retry_due(5, log=lambda m: None, run=run)["still_stuck"], 1)
        e = self.entry("AAAAAAAA")
        self.assertEqual((e["status"], len(e["attempts"])), ("retrying", 1))
        self.assertEqual(e["next_retry"], (datetime.now() + timedelta(days=de.RETRY_DAYS[1])).date().isoformat())
        self.make_due("AAAAAAAA")
        de.retry_due(5, log=lambda m: None, run=self.runner(unresolved("Nope, the repo is not out.", 0.3)))
        e = self.entry("AAAAAAAA")
        self.assertEqual((e["status"], e["next_retry"], len(e["attempts"])), ("closed", None, 2))
        self.assertEqual(de.due(de.load()), [])

    def test_retry_that_finds_it_resolves(self):
        self.add("BBBBBBBB", "not_found", "Could not find the repo anywhere.")
        self.make_due("BBBBBBBB")
        counts = de.retry_due(5, log=lambda m: None, run=self.runner({"verdict": "valid", "cost_usd": 0.2}))
        self.assertEqual(counts["resolved"], 1)
        self.assertEqual(self.entry("BBBBBBBB")["status"], "resolved")

    def test_second_look_runs_once_then_needs_you(self):
        self.add("CCCCCCCC", "unnamed", "The post never names the tool.")
        run = self.runner(unresolved("The post never names the tool, also not in the frames.", 0.5))
        de.retry_due(5, log=lambda m: None, run=run)
        self.assertEqual(run.calls, [("CCCCCCCC", "deep")])
        e = self.entry("CCCCCCCC")
        self.assertEqual((e["status"], e["next_retry"]), ("needs_you", None))
        self.assertEqual(de.due(de.load()), [])

    def test_usage_limit_and_lock_do_not_count(self):
        self.add("DDDDDDDD", "unnamed", "The post never names the tool.")
        self.assertTrue(de.retry_due(5, log=lambda m: None, run=self.runner(code=de.LIMIT_EXIT))["limited"])
        self.assertEqual(de.retry_due(5, log=lambda m: None, run=self.runner())["tried"], 0)  # nothing changed: lock held
        self.assertEqual(self.entry("DDDDDDDD")["attempts"], [])

    def test_crash_is_tried_again_before_it_counts(self):
        self.add("EEEEEEEE", "unnamed", "The post never names the tool.")
        for _ in range(de.MAX_RETRY_ERRORS):
            de.retry_due(5, log=lambda m: None, run=self.runner(code=1))
            self.assertEqual(self.entry("EEEEEEEE")["status"], "open")
        de.retry_due(5, log=lambda m: None, run=self.runner(code=1))
        self.assertEqual(self.entry("EEEEEEEE")["status"], "needs_you")

    def test_retry_that_shows_it_is_gated_moves_lists(self):
        self.add("FFFFFFFF", "not_found", "Could not find the repo anywhere.")
        self.make_due("FFFFFFFF")
        gated = unresolved("Only sent by DM after you comment on the post.")
        de.retry_due(5, log=lambda m: None, run=self.runner(gated))
        e = self.entry("FFFFFFFF")
        self.assertEqual((e["list"], e["status"], e["next_retry"]), ("comment_to_get", "needs_you", None))

    def test_focus_and_limit(self):
        self.add("GGGGGGGG", "unnamed", "The post never names the tool.")
        self.add("HHHHHHHH", "thin_input", "Almost no text.", focus=True)
        run = self.runner(unresolved("The post never names the tool, still.", 0.4))
        de.retry_due(1, log=lambda m: None, run=run)
        self.assertEqual(run.calls, [("HHHHHHHH", "deep")])

    def test_your_statuses_are_left_alone(self):
        self.add("IIIIIIII", "not_found", "Could not find the repo anywhere.")
        entries = de.load()
        de.find(entries, "IIIIIIII", "research").update(status="closed", next_retry="2000-01-01")
        de.save(entries)
        self.assertEqual(de.due(de.load()), [])


if __name__ == "__main__":
    unittest.main()
