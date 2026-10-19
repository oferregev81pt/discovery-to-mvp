#!/usr/bin/env python3
"""Fails if run logs or run outputs are tracked in git.

    python3 evals/test_repo_clean.py

Run records (out/ folders, decision logs, prototypes and decks from a run, reports) belong
on the machine that made them. The synthetic fixtures under evals/fixtures are allowed.
"""
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORBIDDEN = [
    r"(^|/)evals/runs/", r"(^|/)evals/results/", r"\.raw-manifest\.json$",
    r"(^|/)decisions\.md$", r"(^|/)out/\d\d-[^/]+\.md$", r"(^|/)node_modules/", r"(^|/)dist/",
]
LEAKS = [r"/private/tmp/claude", r"scratch-2026", r"local_[0-9a-f]{8}-[0-9a-f]{4}", r"worktrees/[a-z]+-[a-z]+-[0-9a-f]{6}"]


def tracked() -> list[str]:
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return [x for x in out.splitlines() if x]


class TestRepoClean(unittest.TestCase):
    def test_no_run_logs_are_tracked(self):
        bad = [f for f in tracked() if not f.startswith("evals/fixtures/") and any(re.search(p, f) for p in FORBIDDEN)]
        self.assertEqual(bad, [], f"run logs or outputs are tracked: {bad[:5]}")

    def test_no_session_paths_or_ids_in_tracked_text(self):
        bad = []
        for f in tracked():
            if f == "evals/test_repo_clean.py":
                continue
            try:
                text = (ROOT / f).read_text(encoding="utf-8")
            except (UnicodeDecodeError, FileNotFoundError):
                continue
            for p in LEAKS:
                if re.search(p, text):
                    bad.append(f"{f}: {p}")
        self.assertEqual(bad, [], f"session paths or ids found: {bad[:5]}")


if __name__ == "__main__":
    unittest.main(verbosity=1)
