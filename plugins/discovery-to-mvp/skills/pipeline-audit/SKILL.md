---
name: pipeline-audit
description: Audits a finished or partly finished discovery pipeline end to end — do turn IDs resolve, are quotes verbatim, did the customer's top pain survive from the extract to the problem statement, scope and prototype, were contradicted premises dealt with, did every step stop and log a decision — and writes a pass/fail report with the step to redo for each failure. Use after the prototype critique or any time mid-pipeline, when someone asks "did we lose anything between steps", "validate the outputs", "check the pipeline" or before presenting the work.
---

# Pipeline audit (pipeline step 10)

Each step checks its own work a little (step 1 counts turns, step 4 runs six tests) and nothing checks the chain. Chains break at the seams: the customer's biggest complaint is a 3 in the extract, a footnote in the scope and absent from the prototype; a quote loses a hedge on its way into the deck; a premise is marked contradicted in step 4 and quietly built on in step 5. This step reads every output once, tests the links between them and reports what broke. It never fixes anything itself.

## Inputs

- Everything in `out/`, `out/decisions.md`, `context/brief.md`, `raw/` and `prototype/` if they exist.
- Run it in a fresh context when possible (a subagent or a new session) that did not produce the outputs. A step grading its own work gives a gentle grade. If a fresh context is not available, run it anyway and put `Not run in a fresh context.` at the top of `out/10-audit.md`.
- It works on a partial pipeline. A check whose inputs don't exist yet is `n/a`, not `fail`. List which steps were found.

## Rules

- **Read-only.** Write only `out/10-audit.md` and one entry in `out/decisions.md`. Never edit another output, even to fix a typo. A fix goes through the step that owns the file, so the PM sees it and the log records it.
- **Evidence for every verdict.** A `fail` names the file, the line or ID, and what was expected. A `pass` on a mechanical check says what was counted ("41 IDs, 41 resolve"). No "looks fine".
- **Three verdicts only:** `pass`, `fail`, `n/a`. If you cannot tell, that is `fail: cannot verify` with the reason. Do not round up.
- **Run the mechanical checks with commands** (grep, wc, diff), not by eye. Show the command output in the report, trimmed.
- **Severity:** `blocks` (a decision rests on a wrong or lost fact), `fix` (wrong but the decision survives), `note` (cosmetic). Anything in group C that fails is at least `fix`.

## Checks

### A. Integrity (mechanical)

1. **Raw is untouched.** If the folder is a git repo: `git status --short raw/` and `git log --oneline -- raw/` show no edits after import. Otherwise raw files must be older than every `out/01-*` file.
2. **Outputs exist and have their sections.** For each step found, the file exists and has every heading in that skill's output template. List missing headings.
3. **Turn IDs resolve.** Extract every `[ABC-123]` token from `out/02` to `out/09`. Each must exist as a turn in an `out/01-merged-*` file. List orphans.
4. **Quotes are verbatim.** For every quoted string next to a turn ID, normalize whitespace and quote marks and search the turn text for it. List mismatches, and say whether the difference is a dropped hedge, a tidied word, a splice of two turns or a wrong ID. A dropped hedge is `blocks`.
5. **Unlabelled claims.** In extract and collision tables, any cell that says what someone said or did with no ID and no `Interpretation:` label.
6. **Decision log is complete.** For each step found, `out/decisions.md` has an entry with a decision, `Made by: PM` and a date. Entries must appear in step order. A step N+1 output dated or logged before the step N decision is a stop-rule breach: `blocks`. Count the entries marked `PM (delegated` and list them in the report; they are not evidence that the PM decided.
7. **Outputs are current.** If an output is older than a file it reads from, or a logged decision says "changed in the output: X" and X is not in the file, it is stale.

### B. Rules the steps promised

8. **Problem statement:** under 80 words (count them), no banned words (platform, portal, dashboard, app, tool, feature, AI, automate, build, integrate, system, interface, page, view, bot), cites IDs.
9. **No solutions before step 5.** Steps 1 to 4 outputs contain no feature or product names outside `Parked ideas` lines and quotes.
10. **Cut list is real.** At least as long as the in-scope list. Every row has all five cells. "Revisit when" is a trigger, not a date. "What we lose" is not "nothing".
11. **Each in-scope capability** names a persona, evidence IDs, the workaround or relay it removes, and a link on the business chain.
12. **Severity follows the rules.** A pain with severity 1 or 2 has no named workaround, cost or consequence in its own evidence cell; a severity 3 has one. A pain raised only in answer to a leading question is not above 1. A `Named top pain` is at least 2.
13. **Plain writing.** Search all outputs for the stock words from step 7 of the critique (seamless, leverage, robust, empower, streamline, elevate, unlock, holistic, delve, crucial, game-changer) and for "not just X, but Y". List hits outside quotes.

### C. The chain (does it survive the handoffs)

14. **Top pain, end to end.** Take each persona's `Named top pain` from the extracts and trace each one. Mark where it appears, with the form it takes: problem statement (in their words?), scope (core, small or later), prototype brief (tested, or listed under "won't tell us"), critique (mentioned?), deck. A gap anywhere is `fail`. If it shrank, check that the scope's centrality check says so in writing and the PM decided it in the log.
15. **Premises.** Every `contradicted` or `untested` premise in step 4 shows up in step 5 as dropped, or kept and tested. If kept, `out/decisions.md` holds the evidence that would change the PM's mind.
16. **Collisions.** The top three tensions in step 3 each appear in step 5 under "Collisions decided" with a side chosen, or in the log as deliberately avoided.
17. **Weakest link.** The weakest link of the business case in step 4 is on the ranked assumptions in step 6, or step 6 says what else would test it. The deck and critique name it.
18. **Assumptions.** Every assumption in step 5 is on the step 6 ranked table. The one chosen has a test question, a success threshold and a kill signal that an observer could actually see.
19. **Prototype matches the brief.** If `prototype/` exists: `src/data/mock.json` holds the "bite" values the brief specified; the entry point matches the adoption plan; the screens are no more than the brief's; `NOTES.md` holds what was left out; the README copies the test script. Run the build or dev server and walk the flow if you can. Say if you could not.
20. **Critique to action.** Each top issue in step 7 is fixed in the files it points to, or logged as accepted. List the open ones.
21. **Future ideas have seeds.** Each bet in step 8 cites a turn ID, a cut-list row or a silence that exists. At most one is `Imagined`.
22. **Deck traces.** Every slide claim in `out/09-story-outline.md` points to a file and ID that exist and say it. At least one reversal appears. The weakest link is on the slide where it applies. Nothing on a slide is stronger than its evidence ("clients trust us" from one call).
23. **Deck answers why, why now and fit.** `out/09-story-outline.md` holds the deck test with results. Read the slide titles alone: they answer why this matters, for whom, why now, why this option, whether it fits, how we will know, and what could go wrong. Slide 1 names exactly one business number. The why-now slide has a typed, labelled trigger, or says `no why-now evidence`. Every Named top pain and every severity-3 pain is on the fit map with a rating, and unmet needs are shown. At most 12 slides. Re-read the source file for each number on a slide and compare it, with its hedge.

## Output: `out/10-audit.md`

```
# Pipeline audit — <project> — <date>
<If not run in a fresh context, one line saying so.>
Steps found: 0 1 2 ... / Steps missing: ...
## Verdict
One sentence: safe to present | safe with fixes | not safe, and the single biggest reason.
## Scorecard
| Group | pass | fail | n/a |
## Failures (blocks first)
| # | Check | Severity | Where | Expected | Found | Redo step |
## Top pain trail
| Stage | Appears as | OK? |
## Passed checks
| # | Check | What was counted |
## Could not verify
```

Keep the failures table to what matters: a PM reads the first ten rows and stops. Group repeat offenders ("11 quotes lost hedges, in 02-extract-TAM, rows 3, 4, 9...") instead of listing each.

## Stop here: show the results and ask how to continue

This step always ends with a stop, including when it runs inside a full pipeline or the user said "run everything". Never redo a step on your own, and never edit another output. In a delegated run, as the orchestrator defines it, show the results, log the delegated decision and continue.

1. **Show the results in the chat**, not only the file path: the verdict, the scorecard, the top pain trail and the failures that block. Then say where the full file is.
2. **Ask the decisions below.** Give your recommended answer for each, clearly marked as a recommendation.
3. **Ask how to continue**, offering: redo the earliest failing step with the findings · fix specific items together · accept the failures and log why · stop here.

Then wait for the user. Log the answer in `out/decisions.md`. If a step is redone, every later output that read from it is stale: say which, and offer to re-run the audit afterwards.

### Decisions for you

- "These failures block a decision. Redo from step <N>, the earliest broken link?" (Recommend the earliest, since later steps inherit its errors.)
- "These I'd accept as they are. Agree, and should I log the reason?"
- "Present with the known gaps, or fix first?" (Recommend fix first if any check in group C failed.)
