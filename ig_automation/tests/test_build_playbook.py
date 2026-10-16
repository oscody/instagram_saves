"""Offline coverage, provenance, caching, and failure regression checks."""
import argparse
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_playbook as bp


def draft(ids):
    return {"entries": [{"topic": "Testing", "title": "A supported method",
                         "steps": ["Use the supplied procedure."], "primary_source": ids[0],
                         "related_sources": ids[1:], "evidence": "specific_instructions",
                         "limitations": "Not independently tested.",
                         "selection_reason": "This source supplies the concrete procedure."}],
            "contradictions": [], "excluded": []}


class PlaybookTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "IG"
        self.output = self.root / "knowledge_library"
        folder = self.source / "2026-10-15_1200_abc"
        folder.mkdir(parents=True)
        (folder / "abc_description.md").write_text(
            '---\nshortcode: "abc"\nauthor: "person"\n---\n# A useful technique\nInstructions.\n')
        (folder / "abc_carousel_audio_transcript.txt").write_text("RAW AUDIO SENTINEL")
        (folder / "abc_ocr.txt").write_text("RAW OCR SENTINEL")
        (self.source / "2026-10-15_1300_missing").mkdir()
        self.args = argparse.Namespace(source=self.source, output=self.output, model="fixture",
            effort="xhigh", codex="unused", shards=1, batch_bytes=240000,
            reduce_bytes=700000, timeout=5, dry_run=False, stage="all")

    def test_inventory_includes_carousel_audio_and_reports_missing_notes(self):
        records, missing = bp.inventory(self.source)
        self.assertEqual(len(missing), 1)
        self.assertEqual({e["text"] for e in records[0]["evidence"]},
                         {"RAW AUDIO SENTINEL", "RAW OCR SENTINEL"})

    def test_missing_unknown_and_conflicting_provenance_rejected(self):
        for result in [draft(["wrong"]), draft(["abc"])]:
            with self.assertRaises(ValueError):
                bp.validate(result, {"abc", "other"})
        result = draft(["abc"])
        result["excluded"] = [{"source": "abc", "reason": "Duplicate."}]
        with self.assertRaises(ValueError):
            bp.validate(result, {"abc"})
        result = draft(["abc"])
        result["contradictions"] = [{"topic": "Conflict", "claim_a": "A", "claim_b": "B",
                                      "sources_a": ["abc"], "sources_b": ["unknown"],
                                      "assessment": "Unresolved"}]
        with self.assertRaises(ValueError):
            bp.validate(result, {"abc"})

    def test_readable_output_links_sources_without_raw_evidence(self):
        records, missing = bp.inventory(self.source)
        body, index = bp.render(draft(["abc"]), records, missing, self.output, "fixture", "xhigh", "today")
        self.assertNotIn("RAW AUDIO SENTINEL", body + index)
        self.assertNotIn("RAW OCR SENTINEL", body + index)
        self.assertIn("https://www.instagram.com/p/abc/", body)
        self.assertIn("../IG/", index)
        self.assertIn("missing", index)

    def test_stable_shards_and_evidence_changes_affect_cache_identity(self):
        records, _ = bp.inventory(self.source)
        before = bp.digest(records)
        changed = copy.deepcopy(records)
        changed[0]["evidence"][0]["text"] += " new finding"
        self.assertNotEqual(before, bp.digest(changed))
        expanded = records + [{**records[0], "id": "new"}]
        old_group = next(g for g in bp.batches(records) if records[0] in g)
        new_group = next(g for g in bp.batches(expanded) if records[0] in g)
        self.assertIn(old_group[0], new_group)

    def test_failure_preserves_last_good_playbook(self):
        self.output.mkdir()
        playbook = self.output / "Instagram playbook.md"
        playbook.write_text("Previous good result")
        with patch.object(bp, "ROOT", self.root), patch.object(bp.Model, "run", side_effect=RuntimeError("quota")):
            with self.assertRaises(RuntimeError):
                bp.build(self.args)
        self.assertEqual(playbook.read_text(), "Previous good result")
        self.assertEqual(json.loads((self.output / "status.json").read_text())["status"], "failed")

    def fake_cli(self):
        fake = self.root / "fake-codex"
        fake.write_text('''#!/usr/bin/env python3
import json, pathlib, sys
prompt = sys.stdin.read()
data = json.loads(prompt.split("INPUT DATA:\\n", 1)[1])
schema = json.loads(pathlib.Path(sys.argv[sys.argv.index("--output-schema")+1]).read_text())
grouping = "topics" in schema["properties"]
if isinstance(data, dict):
    ids = [r["id"] for r in data["source_titles"]]
elif data and "entries" in data[0]:
    ids = sorted({sid for part in data for entry in part["entries"]
                  for sid in [entry["primary_source"], *entry["related_sources"]]})
else:
    ids = [r["id"] for r in data]
if grouping:
    result = {"topics": [{"slug": "testing", "name": "Testing", "summary": "Testing methods.",
                         "use_cases": ["When checking software."], "sources": ids}]}
else:
    # Ordering requirement: a topic library must exist BEFORE any cleanup call.
    assert (pathlib.Path.cwd().parents[1] / "Topic index.md").exists()
    result = {"entries": [{"topic": "Testing", "title": "A method", "steps": ["Do a step."],
"primary_source": ids[0], "related_sources": ids[1:], "evidence": "specific_instructions",
"limitations": "Not tested.", "selection_reason": "Concrete steps."}],
"contradictions": [], "excluded": []}
pathlib.Path(sys.argv[sys.argv.index("--output-last-message")+1]).write_text(json.dumps(result))
''')
        fake.chmod(0o700)
        self.args.codex = str(fake)

    def test_fake_cli_end_to_end_resume_and_changed_input(self):
        self.fake_cli()
        with patch.object(bp, "ROOT", self.root):
            bp.build(self.args)
            bp.build(self.args)
            status = json.loads((self.output / "status.json").read_text())
            self.assertEqual((status["model_calls"], status["cache_hits"]), (0, 4))
            transcript = next(self.source.glob("*/*_transcript.txt"))
            transcript.write_text("Updated evidence")
            bp.build(self.args)
            status = json.loads((self.output / "status.json").read_text())
            self.assertEqual((status["model_calls"], status["cache_hits"]), (2, 2))
        self.assertEqual(len((self.output / "runs.jsonl").read_text().splitlines()), 3)

    def test_single_batch_gets_cleanup_and_prompt_changes_invalidate_cache(self):
        self.fake_cli()
        with patch.object(bp, "ROOT", self.root):
            bp.build(self.args)
            status = json.loads((self.output / "status.json").read_text())
            self.assertEqual(status["model_calls"], 4)
            prompts = [p.read_text() for p in (self.output / ".cache").glob("*/prompt.txt")]
            self.assertTrue(any("Produce ONE final playbook" in p for p in prompts))
            self.assertEqual(sum(bp.PROMPT_FILE.read_text().strip() in p for p in prompts), 2)
            self.assertEqual(sum(bp.GROUP_PROMPT_FILE.read_text().strip() in p for p in prompts), 2)
            changed = self.root / "changed_prompt.md"
            changed.write_text(bp.PROMPT_FILE.read_text() + "\nState any remaining evidence gaps.\n")
            with patch.object(bp, "PROMPT_FILE", changed):
                bp.build(self.args)
            updated = json.loads((self.output / "status.json").read_text())
            self.assertEqual((updated["model_calls"], updated["cache_hits"]), (2, 2))
            self.assertNotEqual(status["cleanup_prompt_hash"], updated["cleanup_prompt_hash"])

    def test_cleanup_preserves_conflicts_and_rejects_literal_duplicates(self):
        original = draft(["abc", "def"])
        original["contradictions"] = [{"topic": "Timing", "claim_a": "Before", "claim_b": "After",
                                      "sources_a": ["abc"], "sources_b": ["def"],
                                      "assessment": "Conflicting conditions need checking."}]
        result = copy.deepcopy(original)
        bp.validate_cleanup(result, [original])
        # Side order may change during synthesis without losing the conflict.
        result["contradictions"][0].update(sources_a=["def"], sources_b=["abc"])
        bp.validate_cleanup(result, [original])
        result["contradictions"] = []
        with self.assertRaisesRegex(ValueError, "lost a contradiction"):
            bp.validate_cleanup(result, [original])
        result = copy.deepcopy(original)
        result["entries"].append(copy.deepcopy(result["entries"][0]))
        result["entries"][1]["topic"] = "Different topic name"
        with self.assertRaisesRegex(ValueError, "duplicate entry"):
            bp.validate_cleanup(result, [original])

    def test_final_synthesis_merges_across_batches_and_resumes(self):
        self.fake_cli()
        folder = self.source / "2026-10-15_1400_def"
        folder.mkdir()
        (folder / "def_description.md").write_text('---\nshortcode: "def"\n---\n# Similar advice\nMore steps.')
        records, _ = bp.inventory(self.source)
        self.args.batch_bytes = max(len(bp.dump(r).encode()) for r in records) + 1
        with patch.object(bp, "ROOT", self.root):
            bp.build(self.args)
            state = json.loads((self.output / "status.json").read_text())
            self.assertEqual((state["batches"], state["model_calls"]), (2, 6))
            result = json.loads((self.output / "playbook.json").read_text())
            self.assertEqual(len(result["entries"]), 1)
            bp.validate(result, {"abc", "def"})
            bp.build(self.args)
            state = json.loads((self.output / "status.json").read_text())
            self.assertEqual((state["model_calls"], state["cache_hits"]), (0, 6))

    def test_topics_only_then_playbook_uses_saved_grouping(self):
        self.fake_cli()
        self.args.stage = "topics"
        with patch.object(bp, "ROOT", self.root):
            bp.build(self.args)
            self.assertFalse((self.output / "Instagram playbook.md").exists())
            state = json.loads((self.output / "status.json").read_text())
            self.assertEqual((state["status"], state["model_calls"]), ("topics_complete", 2))
            note = self.output / "topics/testing/Sources.md"
            text = note.read_text()
            self.assertIn("When checking software", text)
            self.assertIn("../../../IG/", text)
            self.assertNotIn("RAW AUDIO SENTINEL", text)
            records, _ = bp.inventory(self.source)
            self.assertEqual(bp.load_topics(self.output, records)["topics"][0]["sources"], ["abc"])
            self.args.stage = "playbook"
            bp.build(self.args)
            state = json.loads((self.output / "status.json").read_text())
            self.assertEqual(state["finished_grouping_batches"], 0)
            self.assertEqual(state["model_calls"], 2)
            self.assertTrue((self.output / "Instagram playbook.md").exists())

    def test_playbook_requires_current_topic_grouping(self):
        self.fake_cli()
        self.args.stage = "playbook"
        with patch.object(bp, "ROOT", self.root):
            with self.assertRaisesRegex(ValueError, "Group sources first"):
                bp.build(self.args)
            self.args.stage = "topics"
            bp.build(self.args)
            next(self.source.glob("*/*_ocr.txt")).write_text("New knowledge")
            self.args.stage = "playbook"
            with self.assertRaisesRegex(ValueError, "grouping is stale"):
                bp.build(self.args)
            self.assertFalse((self.output / "Instagram playbook.md").exists())

    def test_grouping_rejects_lost_sources_and_unsafe_paths_but_allows_cross_topic_posts(self):
        topic = {"slug": "testing", "name": "Testing", "summary": "Software tests.",
                 "use_cases": ["Check software"], "sources": ["abc"]}
        grouped = {"topics": [topic]}
        with self.assertRaisesRegex(ValueError, "coverage"):
            bp.validate_topics(grouped, {"abc", "def"})
        topic["slug"] = "../escape"
        with self.assertRaisesRegex(ValueError, "slug"):
            bp.validate_topics(grouped, {"abc"})
        topic["slug"] = "testing"
        grouped["topics"].append({**topic, "slug": "automation", "name": "Automation"})
        bp.validate_topics(grouped, {"abc"})

    def test_dry_run_has_no_writes_and_vault_destination_rejected(self):
        self.args.dry_run = True
        with patch.object(bp, "ROOT", self.root):
            bp.build(self.args)
            self.assertFalse(self.output.exists())
            self.args.output = self.root.parent / "vault"
            with self.assertRaises(ValueError):
                bp.build(self.args)


if __name__ == "__main__":
    unittest.main()
