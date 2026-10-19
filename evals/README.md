# Evals

Three layers, cheapest first. Run them in this order.

| Layer | What it catches | Cost | How |
|---|---|---|---|
| 1. Checker | Broken IDs, doctored quotes, a problem statement over 80 words with "app" in it, a cut list shorter than the scope, decisions logged out of order, raw files edited, stock AI words | Seconds, no model | `python3 evals/check_pipeline.py <project> --golden evals/golden/harvest-line.json` |
| 2. Judge | What needs judgment: was the leading question flagged, did the top pain survive, is the cut reason honest | One fresh-context model call per step | `evals/rubrics.md` |
| 3. Audit | The same links, read by the shipped `pipeline-audit` skill | One model call | `/discovery-to-mvp:pipeline-audit` |

The checker implements the mechanical half of `pipeline-audit`, so the two should agree. If they disagree, one of them has a bug.

## Keep the golden file away from the run

`golden/harvest-line.json` names the triggers and traps the run is expected to find (Avi's summer, Tamar's spring menu, "energy table"). A session that reads it before the run can't show it found them unprompted. For any run scored on rubric rows about unprompted behavior (2.9, 4.7 and the like), the session that runs the pipeline must not read the golden file or `rubrics.md`'s answers until it has finished. Run the checker with `--golden` afterwards, from outside that session.

## Run it on the sample case

```bash
cp -r examples/harvest-line /tmp/hl-run && cd /tmp/hl-run
python3 <repo>/evals/check_pipeline.py . --snapshot-raw     # hash raw/ before the run
# ... run the pipeline one step at a time in Claude Code, answering each checkpoint ...
python3 <repo>/evals/check_pipeline.py . --golden <repo>/evals/golden/harvest-line.json
```

Steps that have not run yet show as `n/a`, so the checker can be run after every step. Calls are assumed real; the evals do not check for a real-or-roleplayed flag.

## Test the checker itself

```bash
python3 evals/test_checker.py
```

Starts from `fixtures/good` (must pass), plants one defect at a time, and asserts the right check fails.

## Run records stay on the machine that made them

Outputs, decision logs, prototypes and decks from a run (`evals/runs/`) and the written reports (`evals/results/`) are not committed: both folders are in `.gitignore`. A run log is evidence about one session, not part of the plugin. `evals/test_repo_clean.py` fails if run logs or run outputs are tracked anywhere except the synthetic fixtures. Keep a report somewhere else if you want to share it.

## What is and isn't verified

- The checker and its tests run and pass: `python3 evals/test_checker.py`, `python3 evals/test_slide_preview.py`, `python3 evals/test_repo_clean.py`.
- The golden assertions come from reading the raw transcripts. The `must_not_match` traps were confirmed to exist in the raw text, and planted regressions were each caught.
- Runs of the skills on the sample case were judged in the session that produced them, and the first runs had no v1.0 baseline. Treat any rubric score from a self-run as generous.
- Not covered: the audit against planted defects (rubric 10), the pushback loop (5.7), a case with more than two personas or a real why-now.
