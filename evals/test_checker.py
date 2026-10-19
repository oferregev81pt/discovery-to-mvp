#!/usr/bin/env python3
"""Tests for check_pipeline.py: the good fixture passes, and each planted defect is caught.

    python3 evals/test_checker.py
"""
import shutil
import tempfile
import unittest
from pathlib import Path

import check_pipeline as cp

GOOD = Path(__file__).parent / "fixtures" / "good"


class Case(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.root = self.tmp / "p"
        shutil.copytree(GOOD, self.root)

    def tearDown(self):
        shutil.rmtree(self.tmp)

    def edit(self, rel, old, new):
        p = self.root / rel
        t = p.read_text()
        self.assertIn(old, t, f"fixture drifted: {old!r} not in {rel}")
        p.write_text(t.replace(old, new, 1))

    def status(self, prefix):
        res = cp.run(self.root, None)
        return next(r for r in res if r.check.startswith(prefix))


class TestGood(Case):
    def test_good_fixture_has_no_failures(self):
        self.assertEqual([r.check for r in cp.run(self.root, None) if r.status == "fail"], [])


class TestPlantedDefects(Case):
    def test_orphan_turn_id(self):
        self.edit("out/02-extract-ANN.md", "[ANN-004].", "[ANN-099].")
        self.assertEqual(self.status("A3").status, "fail")

    def test_dropped_hedge_in_quote(self):
        self.edit("out/02-extract-ANN.md", '"I call the depot every morning, maybe twice"',
                  '"I call the depot every morning"  "twice a day, every day of the week"')
        self.assertEqual(self.status("A4").status, "fail")

    def test_tidied_quote(self):
        self.edit("out/02-extract-ANN.md", "the tracking page says nothing useful",
                  "the tracking page is not helpful")
        self.assertEqual(self.status("A4").status, "fail")

    def test_quote_from_the_brief_is_allowed(self):
        self.edit("out/04-problem.md", "Customers trust our tracking.\n## Premise",
                  'The brief says "Toy Co ships parts by courier" [ANN-002].\n## Premise')
        self.assertEqual(self.status("A4").status, "pass")

    def test_missing_section(self):
        self.edit("out/05-scope.md", "## Centrality check", "## Something else")
        self.assertEqual(self.status("A2").status, "fail")

    def test_step_without_decision(self):
        p = self.root / "out" / "decisions.md"
        p.write_text(p.read_text().split("## Step 5")[0])
        self.assertEqual(self.status("A6").status, "fail")

    def test_decisions_out_of_order(self):
        p = self.root / "out" / "decisions.md"
        parts = p.read_text().split("## Step ")
        p.write_text("## Step ".join([parts[0], parts[2], parts[1]] + parts[3:]))
        self.assertEqual(self.status("A6").status, "fail")

    def test_a_rebuild_entry_may_come_after_later_steps(self):
        p = self.root / "out" / "decisions.md"
        p.write_text(p.read_text() + "## Step 4: problem-framing (rebuild) — 2026-01-05\n- Decision: redone\n- Made by: PM\n- Why: x\n- Changed in the output: y\n")
        self.assertEqual(self.status("A6").status, "pass")
        p.write_text(p.read_text() + "## Step 2: persona-extract — 2026-01-06\n- Decision: late\n- Made by: PM\n- Why: x\n- Changed in the output: y\n")
        self.assertEqual(self.status("A6").status, "fail")

    def test_decision_without_pm(self):
        self.edit("out/decisions.md", "- Made by: PM", "- Made by: model")
        self.assertEqual(self.status("A6").status, "fail")

    def test_banned_word_in_problem(self):
        self.edit("out/04-problem.md", "cannot tell where a parcel is",
                  "have no app that shows where a parcel is")
        self.assertEqual(self.status("B8").status, "fail")

    def test_problem_too_long(self):
        self.edit("out/04-problem.md", "Buyers phone", "word " * 80 + "Buyers phone")
        self.assertEqual(self.status("B8").status, "fail")

    def test_cut_list_shorter_than_scope(self):
        self.edit("out/05-scope.md",
                  "| Price view | expectation | not on the chain | buyers cannot compare cost | when 3 buyers ask unprompted |\n", "")
        self.edit("out/05-scope.md", "| Live map |", "| Live map |")  # still 1 cut vs 1 in: ok
        self.assertEqual(self.status("B10").status, "pass")
        self.edit("out/05-scope.md", "| Late message | Ann | [ANN-002] | daily call | fewer calls |\n",
                  "| Late message | Ann | [ANN-002] | daily call | fewer calls |\n"
                  "| Second | Ann | [ANN-002] | call | fewer calls |\n")
        self.assertEqual(self.status("B10").status, "fail")

    def test_revisit_is_a_date(self):
        self.edit("out/05-scope.md", "when vans report position", "in Q3 2026")
        self.assertEqual(self.status("B10").status, "fail")

    def test_revisit_words_that_only_look_like_months_are_fine(self):
        self.edit("out/05-scope.md", "when vans report position", "when a decision on marketing data is made, and may 3 buyers ask")
        self.assertEqual(self.status("B10").status, "pass")

    def test_revisit_in_a_month_name_fails(self):
        self.edit("out/05-scope.md", "when vans report position", "in October")
        self.assertEqual(self.status("B10").status, "fail")

    def test_what_we_lose_is_nothing(self):
        self.edit("out/05-scope.md", "buyers who want a map will be disappointed", "nothing")
        self.assertEqual(self.status("B10").status, "fail")

    def test_stock_word(self):
        self.edit("out/05-scope.md", "Buyers get a message", "Buyers get a seamless message")
        self.assertEqual(self.status("B13").status, "fail")

    def test_stock_word_inside_quote_is_allowed(self):
        self.edit("out/05-scope.md", "Cut the map?", 'Ann said "this is a robust answer to the question" [ANN-002]')
        self.assertEqual(self.status("B13").status, "pass")

    def test_short_quote_does_not_shift_pairing(self):
        self.edit("out/02-extract-ANN.md", "| 1 | Calls depot daily |", '| 1 | Calls the "daily" depot |')
        self.assertEqual(self.status("A4").status, "pass")

    def test_missing_why_now(self):
        self.edit("out/04-problem.md", "Why now: peak season starts next month, brief. If we wait a year: the calls double again.\n", "")
        self.assertEqual(self.status("B14").status, "fail")

    def test_why_now_without_label_or_cost_of_waiting(self):
        self.edit("out/04-problem.md", "Why now: peak season starts next month, brief. If we wait a year: the calls double again.",
                  "Why now: peak season starts next month.")
        r = self.status("B14")
        self.assertEqual(r.status, "fail")
        self.assertEqual(len(r.items), 2)

    def test_deck_test_missing(self):
        self.edit("out/09-story-outline.md", "## Deck test", "## Something else")
        self.assertEqual(self.status("B15").status, "fail")

    def test_failed_deck_test_must_be_listed_open(self):
        self.edit("out/09-story-outline.md", "| T4 | Why now | pass | ok |", "| T4 | Why now | fail | no trigger |")
        self.assertEqual(self.status("B15").status, "fail")
        self.edit("out/09-story-outline.md", "None.", "T4: no why-now evidence; slide 2 says so.")
        self.assertEqual(self.status("B15").status, "pass")

    def test_more_than_twelve_slides(self):
        extra = "".join(f"| {i} | Q | claim | said | [ANN-002] | x |\n" for i in range(3, 14))
        self.edit("out/09-story-outline.md", "\n## Deck test", extra + "\n## Deck test")
        self.assertEqual(self.status("B15").status, "fail")

    def test_extract_without_recent_changes_section(self):
        self.edit("out/02-extract-ANN.md", "## Recent changes (triggers)", "## Something else")
        self.assertEqual(self.status("A2").status, "fail")

    def test_raw_edit_detected(self):
        cp.main.__globals__["sys"].argv = ["x", str(self.root), "--snapshot-raw"]
        self.assertEqual(cp.main(), 0)
        self.assertEqual(self.status("A1").status, "pass")
        (self.root / "raw" / "call.txt").write_text("tidied")
        self.assertEqual(self.status("A1").status, "fail")

    def test_brief_missing_outcome_and_beliefs(self):
        (self.root / "context" / "brief.md").write_text("# Brief\nToy Co ships parts.\n")
        r = self.status("A8")
        self.assertEqual(r.status, "fail")
        self.assertEqual(len(r.items), 2)


class TestGolden(Case):
    def test_trail_and_assertions(self):
        golden = {
            "assertions": [
                {"id": "t1", "file": "out/01-merged-*.md", "scope": "turns", "kind": "must_not_match",
                 "pattern": "tracking pages", "why": "x"},
                {"id": "t2", "file": "out/01-merged-*.md", "scope": "turns", "kind": "must_match",
                 "pattern": r"^\[INT-003\].*late", "why": "x"},
                {"id": "t3", "file": "out/01-merged-*.md", "scope": "turns", "kind": "must_match",
                 "pattern": r"^\[ANN-003\]", "why": "x"},
            ],
            "trails": [{"name": "top pain", "pattern": "where (a|the) parcel",
                        "files": ["out/02-extract-*.md", "out/04-problem.md", "out/05-scope.md", "out/06-prototype-brief.md"]}],
        }
        res = {r.check: r for r in cp.golden_checks(self.root, golden)}
        self.assertEqual(res["G t1"].status, "pass")
        self.assertEqual(res["G t2"].status, "pass")
        self.assertEqual(res["G t3"].status, "fail")
        # 06 does not exist yet: trail is judged on the files that do
        self.assertEqual(res["C trail: top pain"].status, "fail")  # 02 lacks the phrase
        self.edit("out/02-extract-ANN.md", "Calls depot daily", "Cannot tell where a parcel is")
        res = {r.check: r for r in cp.golden_checks(self.root, golden)}
        self.assertEqual(res["C trail: top pain"].status, "pass")


if __name__ == "__main__":
    unittest.main(verbosity=1)
