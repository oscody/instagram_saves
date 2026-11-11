"""Offline tests for check_comments.py: no Instagram, no GitHub, temp files only."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_comments as cc
import dead_ends


def entry(**kw):
    e = {"shortcode": "AAAAAAAAAAA", "stage": "research", "list": "comment_to_get", "type": "gated",
         "status": "needs_you", "author": "maker", "title": "A Claude skill that updates your other skills",
         "history": [], "added_at": "2026-11-01"}
    e.update(kw)
    return e


def fake_github(repos, user_type="User"):
    def fetch(url):
        if url.endswith("/repos?per_page=100&sort=updated"):
            return repos
        if url.endswith("/users/maker"):
            return {"type": user_type, "html_url": "https://github.com/maker"}
        return None
    return fetch


class GitHubTest(unittest.TestCase):
    def test_strong_match(self):
        gh = cc.check_github(entry(), fake_github([
            {"name": "skills-lab", "description": "Portable Claude skills", "html_url": "https://github.com/maker/skills-lab"},
            {"name": "dotfiles", "description": "", "html_url": "https://github.com/maker/dotfiles"}]))
        self.assertEqual(gh["strong"][0][1], "https://github.com/maker/skills-lab")
        self.assertEqual(cc.judge(entry(), None, gh)["status"], "received")

    def test_weak_match_is_only_a_hint(self):
        gh = cc.check_github(entry(), fake_github([
            {"name": "skills-notes", "description": "", "html_url": "https://github.com/maker/a"},
            {"name": "other", "description": "", "html_url": "https://github.com/maker/b"}]))
        v = cc.judge(entry(), None, gh)
        self.assertIsNone(v["status"])
        self.assertIn("https://github.com/maker/a", v["hints"])

    def test_no_user(self):
        gh = cc.check_github(entry(author="nobody.here"), lambda url: None)
        self.assertEqual(gh, {"user": None, "strong": [], "weak": []})


class JudgeTest(unittest.TestCase):
    def ig(self, texts, links=(), bio_links=()):
        return {"gone": False, "texts": texts, "post_links": list(links), "bio": "", "bio_links": list(bio_links)}

    def test_caption_and_header_are_not_comments(self):
        cap = "Per usual if you want the prompts comment connect and I will send em your way " * 3
        old = cc.saved_caption
        cc.saved_caption = lambda e: cap
        try:
            ig = self.ig(["maker\nOriginal audio\nFollow", "maker\n \n4w\n" + cap])
            self.assertEqual(cc.creator_comments(entry(), ig), [])
            v = cc.judge(entry(), ig, {"strong": [], "weak": []})
            self.assertEqual((v["status"], v["keyword"]), ("queued", "connect"))
        finally:
            cc.saved_caption = old

    def test_long_creator_comment_is_received(self):
        ig = self.ig(["maker\n \n4w\nPrompt in the comments.", "maker\n \n4w\nPROMPT:\n" + "Do this. " * 40])
        v = cc.judge(entry(), ig, {"strong": [], "weak": []})
        self.assertEqual((v["status"], v["source"]), ("received", "the creator's own comment"))
        self.assertTrue(v["text"].startswith("PROMPT:"))

    def test_link_in_creator_comment(self):
        ig = self.ig(["maker\n \n4w\ncaption", "maker\n \n4w\nGet it here https://example.com/guide?utm_source=ig"])
        v = cc.judge(entry(), ig, {"strong": [], "weak": []})
        self.assertEqual((v["status"], v["link"]), ("received", "https://example.com/guide"))

    def test_instagram_menu_links_are_ignored(self):
        ig = self.ig(["maker\n \n4w\ncaption"], links=["https://www.threads.com/@maker"])
        self.assertIsNone(cc.judge(entry(), ig, {"strong": [], "weak": []})["status"])

    def test_keyword_in_comment_queues(self):
        ig = self.ig(["maker\n \n4w\ncaption", "maker\n \n4w\nComment GUIDE and I'll send it"])
        v = cc.judge(entry(), ig, {"strong": [], "weak": []})
        self.assertEqual((v["status"], v["keyword"]), ("queued", "GUIDE"))

    def test_bio_link_only_for_link_in_bio_posts(self):
        ig = self.ig(["maker\n \n4w\ncaption"], bio_links=["https://l.instagram.com/?u=https%3A%2F%2Flinktr.ee%2Fmaker"])
        self.assertIsNone(cc.judge(entry(), ig, {"strong": [], "weak": []})["status"])
        v = cc.judge(entry(type="link_in_bio", list="other", status="open"), ig, {"strong": [], "weak": []})
        self.assertEqual((v["status"], v["link"]), ("received", "https://linktr.ee/maker"))


class TargetsTest(unittest.TestCase):
    def test_which_posts(self):
        entries = [entry(shortcode="A"), entry(shortcode="B", status="queued"),
                   entry(shortcode="C", status="open", type="link_in_bio", list="other"),
                   entry(shortcode="D", history=[{"event": "comments checked (GitHub and Instagram): nothing found"}]),
                   entry(shortcode="E", author=None), entry(shortcode="F", focus=True, added_at="2026-11-09")]
        self.assertEqual([e["shortcode"] for e in cc.targets(entries)], ["F", "A", "C"])
        self.assertIn("D", [e["shortcode"] for e in cc.targets(entries, again=True)])

    def test_apply_saves_comment(self):
        with tempfile.TemporaryDirectory() as tmp:
            old = dead_ends.IG_DIR
            dead_ends.IG_DIR = Path(tmp)
            try:
                (Path(tmp) / "2026-01-01_0000_AAAAAAAAAAA").mkdir()
                e = entry()
                note = cc.apply(e, {"status": "received", "text": "PROMPT: x" * 30, "link": None,
                                    "source": "the creator's own comment", "hints": []}, {"gone": False}, {})
                self.assertEqual(e["status"], "received")
                self.assertIn("comments checked", note)
                self.assertTrue((Path(tmp) / "2026-01-01_0000_AAAAAAAAAAA/AAAAAAAAAAA_creator_comment.txt").exists())
            finally:
                dead_ends.IG_DIR = old


if __name__ == "__main__":
    unittest.main()
