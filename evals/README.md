# Evals

Three layers, cheapest first. Run them in this order.

| Layer | What it catches | Cost | How |
|---|---|---|---|
| 1. Checker | Broken IDs, doctored quotes, a problem statement over 80 words with "app" in it, a cut list shorter than the scope, decisions logged out of order, raw files edited, stock AI words | Seconds, no model | `python3 evals/check_pipeline.py <project> --golden evals/golden/harvest-line.json` |
| 2. Judge | What needs judgment: was the leading question flagged, did the top pain survive, is the cut reason honest | One fresh-context model call per step | `evals/rubrics.md` |
| 3. Audit | The same links, read by the shipped `pipeline-audit` skill | One model call | `/discovery-to-mvp:pipeline-audit` |

The checker implements the mechanical half of `pipeline-audit`, so the two should agree. If they disagree, one of them has a bug.

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

## What is and isn't verified

- The checker and its 18 tests run and pass.
- The golden assertions come from reading the raw transcripts. The `must_not_match` traps were confirmed to exist in the raw text. They have **not** yet been run against real pipeline output, so expect some patterns to need loosening on the first run.
- The rubrics have never been run.
- Known gap: `examples/harvest-line/context/brief.md` predates v1.1 and has no business outcome and no team beliefs, so check A8 fails on it. Add them before a baseline run, or the pipeline will stop and ask (which is scenario B.2).
