"""Offline regression tests for mixed carousel media and transcript-aware notes."""
import copy
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from download import prepare_carousel_audio, download_post
from transcribe import needs_transcript, transcript_path
from describe import needs_description, transcript_text, write_note


class CarouselAudioTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        cls.folder = cls.root / "2026-10-15_1200_fixture"
        cls.folder.mkdir()
        for name, duration, frequency in [("fixture_2", 1, 440), ("fixture_10", 2, 880), ("silent", 1, None)]:
            cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "color=s=16x16:r=10"]
            if frequency:
                cmd += ["-f", "lavfi", "-i", f"sine=frequency={frequency}:sample_rate=16000"]
            cmd += ["-t", str(duration), "-c:v", "libx264", "-pix_fmt", "yuv420p"]
            if frequency:
                cmd += ["-c:a", "aac"]
            subprocess.run(cmd + [str(cls.folder / (name + ".mp4"))], check=True)
        cls.record = {"shortcode": "fixture", "type": "Carousel", "sent_at": "Oct 15, 2026, 12:00 PM",
                      "files": ["fixture_2.mp4", "silent.mp4", "fixture_10.mp4"],
                      "downloaded": True, "described": True, "transcribed": False}

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_audio_order_silent_slides_and_description_refresh(self):
        record = copy.deepcopy(self.record)
        self.assertTrue(prepare_carousel_audio(record, self.folder))
        self.assertEqual([s["file"] for s in record["carousel_audio_sources"]], ["fixture_2.mp4", "fixture_10.mp4"])
        offsets = record["carousel_audio_sources"]
        self.assertAlmostEqual(offsets[1]["start_seconds"], 1, delta=.15)
        self.assertAlmostEqual(offsets[1]["end_seconds"], 3, delta=.2)
        self.assertTrue(needs_transcript(record, self.root, False))
        self.assertFalse(needs_description(record, False, False))
        transcript_path(record, self.root).write_text("Speech from both video slides.")
        record["transcribed"] = True
        self.assertTrue(needs_description(record, False, False))
        self.assertEqual(transcript_text(record, self.folder), "Speech from both video slides.")
        snapshot = copy.deepcopy(record)
        self.assertFalse(prepare_carousel_audio(record, self.folder))
        self.assertEqual(record, snapshot)

    def test_silent_carousel_needs_no_transcript(self):
        record = {**self.record, "files": ["silent.mp4"]}
        self.assertFalse(prepare_carousel_audio(record, self.folder))
        self.assertFalse(needs_transcript(record, self.root, False))
        self.assertTrue(needs_description(record, False, True))

    def test_new_carousel_download_prepares_audio_automatically(self):
        record = copy.deepcopy(self.record)
        record["url"] = "https://instagram.com/p/fixture/"
        with patch("download.api_get", return_value={"items": [{"media_type": 8}]}), \
             patch("download.media_to_link", return_value={"type": "Carousel", "caption": ""}), \
             patch("download.download_images", return_value=list(record["files"])):
            download_post(record, self.root, {}, "unused")
        self.assertIn("fixture_carousel_audio.mp3", record["files"])
        self.assertTrue(record["downloaded"])
        self.assertFalse(record["described"])
        self.assertTrue(needs_transcript(record, self.root, False))

    def test_failed_probe_does_not_mark_audio_ready(self):
        record = {**self.record, "files": ["missing.mp4"]}
        snapshot = copy.deepcopy(record)
        with self.assertRaises(RuntimeError):
            prepare_carousel_audio(record, self.folder)
        self.assertEqual(record, snapshot)

    def test_markdown_contains_summary_not_raw_transcript(self):
        record = {**self.record, "ai_title": "Useful lesson", "summary": "A concise summary.",
                  "transcribed_by": "test", "described_by": "test"}
        note = write_note(record, self.folder, ["Apply the lesson."])
        body = note.read_text()
        self.assertIn("A concise summary.", body)
        self.assertIn("Apply the lesson.", body)
        self.assertNotIn("## Transcript", body)
        self.assertNotIn("Speech from both video slides.", body)


if __name__ == "__main__":
    unittest.main()
