"""Offline coverage, provenance, caching, and failure regression checks."""
import argparse
import contextlib
import copy
import io
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
            reduce_bytes=700000, timeout=5, dry_run=False, stage="all",
            model_merge=True)   # older flow; shared-topic tests below turn it off

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
    ids = [r["id"] for r in (data["sources"] if "sources" in data else data["source_titles"])]
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
            topics, manifest = bp.load_topics(self.output, records)
            self.assertEqual(topics["topics"][0]["sources"], ["abc"])
            saved = self.output / "groupings" / f"{manifest['grouping']}.json"
            self.assertEqual(json.loads(saved.read_text())["topics"], topics["topics"])
            self.args.stage = "playbook"
            bp.build(self.args)
            state = json.loads((self.output / "status.json").read_text())
            self.assertEqual(state["finished_grouping_batches"], 0)
            self.assertEqual(state["model_calls"], 2)
            self.assertTrue((self.output / "Instagram playbook.md").exists())
            self.args.dry_run = True
            report = io.StringIO()
            with contextlib.redirect_stdout(report):
                bp.build(self.args)
            self.assertIn("1 cached comparison calls, 0 uncached", report.getvalue())
            self.assertIn("one final cleanup call", report.getvalue())

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

    def test_playbook_call_limit_is_previewed_and_stops_before_model_use(self):
        records, _ = bp.inventory(self.source)
        self.output.mkdir()
        topics = [{"slug": slug, "name": name, "summary": name,
                   "use_cases": ["Review the source"], "sources": ["abc"]}
                  for slug, name in (("testing", "Testing"), ("review", "Review"))]
        bp.write_json(self.output / "topics.json",
                      {"source_fingerprint": bp.digest(records), "topics": topics})
        self.args.stage = "playbook"
        self.args.max_playbook_batches = 1
        self.args.dry_run = True
        report = io.StringIO()
        with patch.object(bp, "ROOT", self.root), contextlib.redirect_stdout(report):
            bp.build(self.args)
        self.assertIn("2 comparison calls", report.getvalue())
        self.assertIn("would stop before model calls", report.getvalue())
        self.assertFalse((self.output / "status.json").exists())
        self.args.dry_run = False
        with patch.object(bp, "ROOT", self.root), patch.object(
                bp.Model, "run", side_effect=AssertionError("model called")):
            with self.assertRaisesRegex(ValueError, "exceeding --max-playbook-batches 1"):
                bp.build(self.args)
        self.assertEqual(self.status()["batches"], 2)
        self.assertEqual(self.status()["finished_batches"], 0)

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

    # ---- Claude fallback -------------------------------------------------
    BRAIN = """
import json, pathlib, sys
def answer(prompt, schema):
    data = json.loads(prompt.split("INPUT DATA:\\n", 1)[1])
    grouping = "topics" in schema["properties"]
    if isinstance(data, dict):
        ids = [r["id"] for r in (data["sources"] if "sources" in data else data["source_titles"])]
    elif data and "entries" in data[0]:
        ids = sorted({sid for part in data for entry in part["entries"]
                      for sid in [entry["primary_source"], *entry["related_sources"]]})
    else:
        ids = [r["id"] for r in data]
    if grouping:
        return {"topics": [{"slug": "testing", "name": "Testing", "summary": "Testing methods.",
                            "use_cases": ["When checking software."], "sources": ids}]}
    return {"entries": [{"topic": "Testing", "title": "A method", "steps": ["Do a step."],
            "primary_source": ids[0], "related_sources": ids[1:], "evidence": "specific_instructions",
            "limitations": "Not tested.", "selection_reason": "Concrete steps."}],
            "contradictions": [], "excluded": []}
"""

    def fake_pair(self, codex="fail_limit", claude="ok"):
        """Fake codex and claude CLIs; each appends a line to its own call log."""
        for name, mode in (("codex", codex), ("claude", claude)):
            fake = self.root / f"fake-{name}"
            log = self.root / f"{name}.calls"
            body = self.BRAIN + f"""
pathlib.Path({str(log)!r}).open("a").write("call\\n")
mode = {mode!r}
prompt = sys.stdin.read()
if mode == "fail_limit":
    sys.stderr.write("You have hit your usage limit. Try again at 5pm.")
    sys.exit(1)
if mode == "fail":
    sys.stderr.write("boom")
    sys.exit(1)
if mode == "net_once" and not pathlib.Path({str(log)!r} + ".down").exists():
    pathlib.Path({str(log)!r} + ".down").write_text("down")
    print(json.dumps({{"is_error": True, "total_cost_usd": 0,
                      "result": "API Error: Can't reach the API server (EAI_AGAIN)"}}))
    sys.exit(1)
if mode == "bad":      # returns sources that do not exist
    result = {{"entries": [], "contradictions": [], "excluded": []}}
else:
    schema_arg = sys.argv[sys.argv.index("--output-schema") + 1] if "--output-schema" in sys.argv \\
        else sys.argv[sys.argv.index("--json-schema") + 1]
    schema = json.loads(pathlib.Path(schema_arg).read_text() if schema_arg.endswith(".json") else schema_arg)
    result = answer(prompt, schema)
if mode == "case":     # the model changes one ID's letter case
    result = json.loads(json.dumps(result).replace('"abc"', '"ABC"'))
if "--output-last-message" in sys.argv:
    pathlib.Path(sys.argv[sys.argv.index("--output-last-message") + 1]).write_text(json.dumps(result))
else:
    print(json.dumps({{"is_error": False, "structured_output": result, "total_cost_usd": 0.5}}))
"""
            fake.write_text("#!/usr/bin/env python3\n" + body)
            fake.chmod(0o700)
        self.args.codex = str(self.root / "fake-codex")
        self.args.claude = str(self.root / "fake-claude")
        self.args.fallback_model = "claude-fallback"
        self.args.fallback_effort = None
        self.args.no_fallback = False
        self.args.refresh_fallback = False

    def calls(self, name):
        log = self.root / f"{name}.calls"
        return len(log.read_text().splitlines()) if log.exists() else 0

    def status(self):
        return json.loads((self.output / "status.json").read_text())

    def test_codex_usage_limit_switches_to_claude_for_rest_of_run(self):
        self.fake_pair(codex="fail_limit")
        with patch.object(bp, "ROOT", self.root):
            bp.build(self.args)
        self.assertEqual(self.calls("codex"), 1)      # not retried once the limit is seen
        self.assertEqual(self.calls("claude"), 4)     # group, normalize, compare, cleanup
        status = self.status()
        self.assertEqual(status["status"], "complete")
        self.assertEqual(status["fallback_calls"], 4)
        self.assertEqual(status["fallback_cost_usd"], 2.0)
        self.assertIn("claude-fallback", (self.output / "Instagram playbook.md").read_text())
        producers = {json.loads(f.read_text())["model"] for f in self.output.glob(".cache/*/producer.json")}
        self.assertEqual(producers, {"claude-fallback"})

    def test_other_codex_failures_retry_codex_on_every_call(self):
        self.fake_pair(codex="fail")
        with patch.object(bp, "ROOT", self.root):
            bp.build(self.args)
        self.assertEqual(self.calls("codex"), self.calls("claude"))
        self.assertEqual(self.status()["status"], "complete")

    def test_invalid_codex_answer_falls_back_to_claude(self):
        self.fake_pair(codex="bad")
        with patch.object(bp, "ROOT", self.root):
            bp.build(self.args)
        self.assertGreater(self.calls("claude"), 0)
        self.assertEqual(self.status()["status"], "complete")

    def test_both_failing_stops_and_reports_both(self):
        self.fake_pair(codex="fail", claude="fail")
        with patch.object(bp, "ROOT", self.root):
            with self.assertRaisesRegex(RuntimeError, "also failed"):
                bp.build(self.args)
        self.assertEqual(self.status()["status"], "failed")

    def test_id_with_wrong_letter_case_is_corrected(self):
        self.fake_pair(codex="fail", claude="case")
        with patch.object(bp, "ROOT", self.root):
            bp.build(self.args)
        self.assertEqual(self.status()["status"], "complete")
        self.assertIn("Fixed source ID", (self.output / "build.log").read_text())
        self.assertIn("https://www.instagram.com/p/abc/",
                      (self.output / "Instagram playbook.md").read_text())

    def test_case_fix_needs_one_match_and_skips_non_id_fields(self):
        result = draft(["ABC"])
        result["entries"][0]["title"] = "ABC"
        self.assertEqual(bp.fix_source_ids(result, {"abc"}), [("ABC", "abc")])
        self.assertEqual(result["entries"][0]["primary_source"], "abc")
        self.assertEqual(result["entries"][0]["title"], "ABC")
        ambiguous = draft(["ABC"])
        self.assertEqual(bp.fix_source_ids(ambiguous, {"abc", "aBc"}), [])

    def test_garbled_id_is_restored_only_when_unambiguous(self):
        result = draft(["DaGIKtPki6B"])
        result["excluded"] = [{"source": "DWjQBJbmDBjQ", "reason": "Promo."}]
        expected = {"DaGIKtPki6B", "DWJUbQmDBjQ"}
        self.assertEqual(bp.fix_source_ids(result, expected), [("DWjQBJbmDBjQ", "DWJUbQmDBjQ")])
        bp.validate(result, expected)
        unrelated = draft(["DaGIKtPki6B"])
        unrelated["excluded"] = [{"source": "zzzzzzzzzzz", "reason": "Promo."}]
        self.assertEqual(bp.fix_source_ids(unrelated, expected), [])
        two_close = draft(["DaGIKtPki6B"])
        two_close["excluded"] = [{"source": "DWjQBJbmDBjQ", "reason": "Promo."}]
        self.assertEqual(bp.fix_source_ids(two_close, expected | {"DWJUbQmDBJQ"}), [])

    def test_network_failure_is_retried_then_continues(self):
        self.fake_pair(codex="fail", claude="net_once")
        with patch.object(bp, "ROOT", self.root), patch.object(bp, "NETWORK_RETRY_WAITS", (0, 0)):
            bp.build(self.args)
        self.assertEqual(self.status()["status"], "complete")
        self.assertEqual(self.calls("claude"), self.calls("codex") + 1)   # one retry
        self.assertIn("Network error", (self.output / "build.log").read_text())

    def test_other_claude_failures_are_not_retried(self):
        self.fake_pair(codex="fail", claude="fail")
        with patch.object(bp, "ROOT", self.root), patch.object(bp, "NETWORK_RETRY_WAITS", (0, 0)):
            with self.assertRaisesRegex(RuntimeError, "also failed"):
                bp.build(self.args)
        self.assertEqual(self.calls("claude"), 1)

    def test_no_fallback_stops_on_codex_failure(self):
        self.fake_pair(codex="fail")
        self.args.no_fallback = True
        with patch.object(bp, "ROOT", self.root):
            with self.assertRaisesRegex(RuntimeError, "Model call failed"):
                bp.build(self.args)
        self.assertEqual(self.calls("claude"), 0)

    def test_rerun_reuses_fallback_results_and_refresh_redoes_them_with_codex(self):
        self.fake_pair(codex="fail_limit")
        with patch.object(bp, "ROOT", self.root):
            bp.build(self.args)
            bp.build(self.args)
            self.assertEqual(self.status()["model_calls"], 0)     # all cached
            self.fake_pair(codex="ok", claude="fail")             # Codex is back
            self.args.refresh_fallback = True
            bp.build(self.args)
        self.assertEqual(self.status()["fallback_calls"], 0)
        producers = {json.loads(f.read_text())["model"] for f in self.output.glob(".cache/*/producer.json")}
        self.assertEqual(producers, {"fixture"})
        self.assertNotIn("fallback", (self.output / "Instagram playbook.md").read_text())

    # ---- shared topic list, grouping effort, switch log, cost cap -----------
    def second_note(self):
        folder = self.source / "2026-10-15_1400_def"
        folder.mkdir()
        (folder / "def_description.md").write_text(
            '---\nshortcode: "def"\nauthor: "other"\n---\n# Another technique\nMore.\n')
        records, _ = bp.inventory(self.source)
        self.args.shards = 1
        self.args.batch_bytes = max(len(bp.dump(r).encode()) for r in records) + 10  # one post per batch

    def test_merge_topics_joins_same_slug_or_name_and_keeps_every_source(self):
        one = {"topics": [{"slug": "editing", "name": "Video Editing", "summary": "First.",
                           "use_cases": ["Cut clips"], "sources": ["a"]}]}
        two = {"topics": [{"slug": "video-editing", "name": " video  editing", "summary": "Later.",
                           "use_cases": ["cut clips", "Add captions"], "sources": ["b", "a"]},
                          {"slug": "editing", "name": "Editing", "summary": "Same slug.",
                           "use_cases": [], "sources": ["c"]},
                          {"slug": "cooking", "name": "Cooking", "summary": "Food.",
                           "use_cases": ["Dinner"], "sources": ["d"]}]}
        merged = bp.merge_topics([one, two])
        self.assertEqual([t["slug"] for t in merged["topics"]], ["editing", "cooking"])
        editing = merged["topics"][0]
        self.assertEqual(editing["summary"], "First.")
        self.assertEqual(editing["sources"], ["a", "b", "c"])
        self.assertEqual(editing["use_cases"], ["Cut clips", "Add captions"])
        bp.validate_topics(merged, {"a", "b", "c", "d"})

    def test_batches_share_topic_list_and_merge_without_a_model_call(self):
        self.second_note()
        self.args.model_merge = False
        self.args.stage = "topics"
        self.fake_cli()
        with patch.object(bp, "ROOT", self.root):
            bp.build(self.args)
        state = json.loads((self.output / "status.json").read_text())
        self.assertEqual((state["status"], state["model_calls"]), ("topics_complete", 2))  # no merge call
        topics = json.loads((self.output / "topics.json").read_text())["topics"]
        self.assertEqual([(t["slug"], sorted(t["sources"])) for t in topics], [("testing", ["abc", "def"])])
        prompts = [p.read_text() for p in self.output.glob(".cache/*/prompt.txt")]
        later = [p for p in prompts if '"existing_topics": [{' in p]
        self.assertEqual(len(later), 1)
        self.assertIn('"name": "Testing"', later[0])

    def test_grouping_uses_its_own_effort_and_playbook_keeps_the_main_one(self):
        self.args.group_effort = "medium"
        self.fake_cli()
        seen = []
        original = bp.Model.call_codex

        def spy(model, job, prompt, raw, name, effort):
            seen.append(effort)
            return original(model, job, prompt, raw, name, effort)
        with patch.object(bp, "ROOT", self.root), patch.object(bp.Model, "call_codex", spy):
            bp.build(self.args)
        self.assertEqual(seen, ["medium", "medium", "xhigh", "xhigh"])  # group, merge, compare, cleanup

    def test_switch_to_claude_is_logged_with_reason_and_saved(self):
        self.fake_pair(codex="fail_limit")
        with patch.object(bp, "ROOT", self.root):
            bp.build(self.args)
        log = (self.output / "build.log").read_text()
        self.assertEqual(log.count("SWITCH:"), 1)           # once; later calls just say they use Claude
        self.assertIn("codex", log.lower())
        self.assertIn("claude-fallback", log)
        self.assertIn("fallback spend so far", log)
        events = self.status()["switch_events"]
        self.assertEqual((len(events), events[0]["to"]), (1, "claude-fallback"))
        self.assertIn("usage limit", events[0]["reason"])

    def test_fallback_cost_cap_stops_after_caching_and_rerun_resumes(self):
        self.fake_pair(codex="fail_limit")
        self.args.max_fallback_cost = 0.5                   # fake Claude charges 0.5 per call
        with patch.object(bp, "ROOT", self.root):
            with self.assertRaisesRegex(RuntimeError, "max-fallback-cost"):
                bp.build(self.args)
            self.assertEqual(self.calls("claude"), 1)
            self.assertEqual(len(list(self.output.glob(".cache/*/validated.json"))), 1)
            self.args.max_fallback_cost = 0
            bp.build(self.args)
        self.assertEqual(self.status()["status"], "complete")
        self.assertEqual(self.calls("claude"), 4)           # the first result was reused, not redone

    def test_claude_session_limit_message_is_recognised(self):
        error = RuntimeError("Fallback call failed (exit 1): You've hit your session limit \u00b7 resets 1:10am")
        self.assertTrue(bp.Model.claude_limit(error))
        self.assertFalse(bp.Model.claude_limit(RuntimeError("invalid JSON")))

    # ---- saved groupings, consolidation, split cleanup, running spend total ----
    def test_named_groupings_are_saved_listed_and_reused_by_the_playbook(self):
        self.fake_cli()
        self.args.stage = "topics"
        with patch.object(bp, "ROOT", self.root):
            self.args.grouping = "first"
            bp.build(self.args)
            self.args.grouping = "second"
            bp.build(self.args)
            self.assertEqual(json.loads((self.output / "topics.json").read_text())["grouping"], "second")
            self.args.list_groupings = True
            report = io.StringIO()
            with contextlib.redirect_stdout(report):
                bp.build(self.args)
            self.assertIn("first: 1 topics", report.getvalue())
            self.assertIn("second: 1 topics, 1 posts", report.getvalue())
            self.assertIn("[active]", report.getvalue())
            self.args.list_groupings = False
            self.args.stage, self.args.grouping = "playbook", "first"
            bp.build(self.args)
            self.assertEqual(self.status()["grouping"], "first")
            self.assertEqual(json.loads((self.output / "topics.json").read_text())["grouping"], "first")
            self.args.grouping = "missing"
            with self.assertRaisesRegex(ValueError, "No saved grouping 'missing'"):
                bp.build(self.args)

    def test_consolidation_absorbs_every_topic_and_keeps_all_sources(self):
        topics = {"topics": [{"slug": s, "name": s.title(), "summary": s, "use_cases": ["x"],
                              "sources": src} for s, src in
                             (("cuts", ["a"]), ("captions", ["b", "a"]), ("soup", ["c"]))]}
        result = {"topics": [
            {"slug": "video-editing", "name": "Video editing", "summary": "Editing.",
             "use_cases": ["Edit a reel"], "members": ["cuts", "captions"]},
            {"slug": "cooking", "name": "Cooking", "summary": "Food.",
             "use_cases": ["Dinner"], "members": ["soup"]}]}
        bp.validate_consolidation(result, {"cuts", "captions", "soup"})
        merged = bp.apply_consolidation(result, topics)
        self.assertEqual([t["sources"] for t in merged["topics"]], [["a", "b"], ["c"]])
        bp.validate_topics(merged, {"a", "b", "c"})
        lost = copy.deepcopy(result)
        lost["topics"][1]["members"] = []
        with self.assertRaises(ValueError):
            bp.validate_consolidation(lost, {"cuts", "captions", "soup"})
        twice = copy.deepcopy(result)
        twice["topics"][1]["members"] = ["soup", "cuts"]
        with self.assertRaisesRegex(ValueError, "repeated"):
            bp.validate_consolidation(twice, {"cuts", "captions", "soup"})

    def test_topic_stage_consolidates_down_to_max_topics(self):
        self.second_note()
        self.args.model_merge = False
        self.args.stage = "topics"
        self.args.max_topics = 1
        two = {"topics": [{"slug": "a", "name": "A", "summary": "A.", "use_cases": ["x"], "sources": ["abc"]},
                          {"slug": "b", "name": "B", "summary": "B.", "use_cases": ["y"], "sources": ["def"]}]}
        one = {"topics": [{"slug": "both", "name": "Both", "summary": "Both.", "use_cases": ["z"],
                           "members": ["a", "b"]}]}
        phases = []

        def fake_run(model, phase, payload, expected, *, grouping=False, schema=None, check=None):
            phases.append(phase)
            if schema is bp.CONSOLIDATE_SCHEMA:
                check(one, expected)
                return one
            return {"topics": [t for t in two["topics"] if set(t["sources"]) & expected]}
        with patch.object(bp, "ROOT", self.root), patch.object(bp.Model, "run", fake_run):
            bp.build(self.args)
        topics = json.loads((self.output / "topics.json").read_text())["topics"]
        self.assertEqual([(t["slug"], t["sources"]) for t in topics], [("both", ["abc", "def"])])
        self.assertEqual(self.status()["topics_before_consolidation"], 2)
        self.assertEqual(phases.count(bp.CONSOLIDATE_PHASE), 1)

    def test_cleanup_merges_in_parts_then_merges_the_parts(self):
        drafts = [draft([sid]) for sid in ("a", "b", "c", "d")]
        for i, d in enumerate(drafts):
            d["entries"][0]["title"] = f"Method {i}"
        budget = len(bp.dump(drafts[0]).encode()) * 2 + 10      # two drafts per part
        calls = []

        class Fake:
            def run(self, phase, payload, expected):
                calls.append((phase, len(payload), sorted(expected)))
                return draft(sorted(bp.draft_sources(payload)))

            def log(self, message):
                pass
        self.output.mkdir()
        state = {}
        result = bp.clean_up(Fake(), drafts, {"a", "b", "c", "d"}, budget, state, self.output)
        self.assertEqual([(p == bp.PARTIAL_PHASE, n, ids) for p, n, ids in calls],
                         [(True, 2, ["a", "b"]), (True, 2, ["c", "d"]), (False, 2, ["a", "b", "c", "d"])])
        self.assertEqual(sorted(bp.draft_sources([result])), ["a", "b", "c", "d"])
        self.assertEqual(state["phase"], "whole-library cleanup")
        calls.clear()       # drafts that never fit together go straight to the final call
        bp.clean_up(Fake(), drafts, {"a", "b", "c", "d"}, 10, state, self.output)
        self.assertEqual([(p == bp.FINAL_PHASE, n) for p, n, _ in calls], [(True, 4)])

    def test_parts_too_large_for_final_call_are_joined_in_code(self):
        drafts = [draft(["a"]), draft(["b", "c"]), draft(["a"])]   # third repeats the first
        drafts[1]["entries"][0]["title"] = "Another method"
        drafts[1]["excluded"] = [{"source": "a", "reason": "Covered elsewhere."}]
        drafts[2]["excluded"] = [{"source": "d", "reason": "No method."}]
        calls = []

        class Fake:
            args = argparse.Namespace(reduce_bytes=10)

            def run(self, *call):
                calls.append(call)

            def log(self, message):
                pass
        self.output.mkdir()
        state = {}
        result = bp.clean_up(Fake(), drafts, {"a", "b", "c", "d"}, 10, state, self.output)
        self.assertEqual(calls, [])
        self.assertEqual(state["phase"], "join cleaned parts")
        self.assertEqual(len(result["entries"]), 2)          # literal duplicate dropped
        self.assertEqual(result["excluded"], [{"source": "d", "reason": "No method."}])
        bp.validate(result, {"a", "b", "c", "d"})

    def test_fallback_cap_counts_spend_across_runs_until_reset(self):
        self.fake_pair(codex="fail_limit")
        self.args.max_fallback_cost = 1.0                   # fake Claude charges 0.5 per call
        with patch.object(bp, "ROOT", self.root):
            with self.assertRaisesRegex(RuntimeError, "max-fallback-cost"):
                bp.build(self.args)                         # two calls: $1.00
            self.assertEqual(self.calls("claude"), 2)
            with self.assertRaisesRegex(RuntimeError, "max-fallback-cost"):
                bp.build(self.args)                         # a new run starts at $1.00 and stops
            self.assertEqual(self.calls("claude"), 2)
            self.assertEqual(self.status()["fallback_cost_total_usd"], 1.0)
            self.args.reset_fallback_spend = True
            self.args.max_fallback_cost = 0
            bp.build(self.args)
        self.assertEqual(self.status()["status"], "complete")
        self.assertEqual(json.loads((self.output / "fallback_spend.json").read_text())["total_usd"], 1.0)


if __name__ == "__main__":
    unittest.main()
