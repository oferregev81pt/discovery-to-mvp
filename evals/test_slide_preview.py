#!/usr/bin/env python3
"""Tests for the slide preview script in mvp-story-deck.

    python3 evals/test_slide_preview.py
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "plugins/discovery-to-mvp/skills/mvp-story-deck/slide_preview.py"


class TestPreview(unittest.TestCase):
    def test_builds_a_page_in_deck_order_without_speaker_notes(self):
        with tempfile.TemporaryDirectory() as d:
            deck, out = Path(d) / "deck", Path(d) / "out"
            (deck / "project" / "slides").mkdir(parents=True)
            (deck / "project" / "deck.json").write_text(json.dumps({"order": ["b", "a"]}))
            (deck / "project" / "slides" / "a.html").write_text('<section id="a" style="padding:128px"><h2>First A</h2><aside>secret notes</aside></section>')
            (deck / "project" / "slides" / "b.html").write_text('<section id="b" style="padding:128px"><h2>First B</h2></section>')
            r = subprocess.run([sys.executable, str(SCRIPT), str(deck), str(out)], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            page = (out / "preview.html").read_text()
            self.assertLess(page.index("First B"), page.index("First A"))
            self.assertNotIn("secret notes", page)
            self.assertIn("margin:0", page)  # the deck format ignores margin, so the preview resets it

    def test_rejects_a_bad_slide_id(self):
        with tempfile.TemporaryDirectory() as d:
            deck = Path(d) / "deck"
            (deck / "project").mkdir(parents=True)
            (deck / "project" / "deck.json").write_text(json.dumps({"order": ["../evil"]}))
            r = subprocess.run([sys.executable, str(SCRIPT), str(deck), str(Path(d) / "out")], capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=1)
