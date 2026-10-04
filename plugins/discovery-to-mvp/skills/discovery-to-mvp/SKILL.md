---
name: discovery-to-mvp
description: Takes the PM through the discovery pipeline one step at a time, from raw customer interview transcripts to a scoped v1, a prototype brief, a built prototype and an honest critique, showing the results of each step and stopping for the PM's decision before the next. Use when someone has interview or call transcripts and wants to get to an MVP, says "take these interviews to an MVP", "run the discovery pipeline", or wants to resume a pipeline already in progress.
---

# Discovery to MVP (orchestrator)

This skill chains eight step skills into one pipeline. Each step produces one file. Each file feeds the next. Between steps the PM makes a decision, and that decision is written down.

The pipeline exists because "summarize these interviews" is the easy 10%. The value is in the steps a summary skips: fixing who said what, separating what people stated from what their stories reveal, finding where two personas collide, writing a cut list you can defend, and prototyping only the riskiest piece.

## The steps

| # | Skill | Reads | Writes |
|---|-------|-------|--------|
| 0 | `interview-guide` (optional, before the calls) | `context/brief.md` | `out/00-interview-guide.md` |
| 1 | `transcript-reconcile` | `raw/*` | `out/01-merged-<CODE>.md` (one per call) |
| 2 | `persona-extract` | `out/01-*`, brief | `out/02-extract-<CODE>.md` (one per persona) |
| 3 | `persona-collide` | `out/02-*`, `out/01-*` | `out/03-collisions.md` |
| 4 | `problem-framing` | `out/03`, `out/02-*`, brief | `out/04-problem.md` |
| 5 | `mvp-scope-cutlist` | `out/04`, `out/03`, `out/02-*`, brief | `out/05-scope.md` |
| 6 | `prototype-brief` | `out/05`, `out/02-*`, `out/01-*` | `out/06-prototype-brief.md` |
| 7 | `prototype-build-critique` | `out/06`, `out/04`, `out/05` | `prototype/`, `out/07-critique.md` |

All steps also append to `out/decisions.md`.

## Folder layout

Expect (or create) this layout in the working project:

```
context/brief.md        # what we're exploring, who we talked to, glossary, constraints
raw/                    # original transcripts. READ-ONLY. Never edit, rename or delete.
out/                    # every pipeline output, numbered by step
out/decisions.md        # running log of decisions
prototype/              # the app built in step 7
```

If `context/brief.md` is missing, ask the user for: the problem space in two or three sentences, who was interviewed (name, role, which side of the relationship), known terms and product names (the glossary), and constraints (team, time, data you do or don't have). Write the brief before step 1. It is short; half a page is enough.

## How to run

1. **Find where we are.** List `out/`. The highest-numbered complete file tells you the last finished step. If the user asked for a specific step, start there, but check its inputs exist first. If an input is missing, say which step produces it and offer to run that step.
2. **Run one step.** Load the step's skill and follow it exactly. Each step skill has its own rules; they are stricter than this file and take precedence.
3. **Stop and show the results.** Every step ends the same way: show the step's key results in the chat (each step skill says what to show), ask its 1 to 3 decisions with your recommendation marked as such, and ask how to continue: next step, redo this step with changes, edit the output together, or stop. Then wait. **Never start the next step on your own**, even when the user asked to "run the whole pipeline". A request to run the pipeline means "take me through it", one step at a time.
4. **Log the decision.** Append to `out/decisions.md`:
   ```
   ## Step N: <step name> — <date>
   - Decision: <what was decided>
   - Made by: PM
   - Why: <one line, in the PM's words when they gave a reason>
   - Changed in the output: <what you edited as a result, or "nothing">
   ```
5. **Apply the decision** to the step's output file before moving on (for example, re-cut the scope after pushback). Then continue to the next step.

There is no unattended mode. If nobody is there to answer (a scheduled run, or the user stepped away), finish the current step, post its results and questions, and stop. The next step waits for a person. Never deploy anything without the user.

## Rules that hold across every step

- **Traceability.** Every claim about what a person said or experienced carries a turn ID from a merged transcript, like `[TAM-024]`. Step 1 creates these IDs. If a claim has no ID, it's an interpretation and must be labelled `Interpretation:`. If neither, delete it.
- **Raw stays raw.** Never edit files in `raw/`. Quotes get checked against `out/01-*` and, when in doubt, against `raw/`.
- **Verbatim means verbatim.** Quotes are copied from the merged transcript. Don't tidy grammar inside quote marks.
- **Hedges are data.** "I guess", "maybe half, maybe less", "mostly on top" carry meaning. Keep them in quotes and notice them.
- **No solutions before step 5.** Steps 1 to 4 describe people and problems. If a solution idea comes up early, park it in a `Parked ideas` line at the end of the file; step 5 picks them up.
- **The model proposes, the PM decides.** Each step ends with options and a recommendation, never a verdict, and the pipeline can't move until the PM answers. The decision log is the evidence of who decided.
- **Plain writing.** Outputs are read by people. Short sentences, concrete nouns, no filler ("leverage", "seamless", "robust", "it's important to note"). Numbers over adjectives.

## Running steps individually

Every step skill also works on its own. If the user invokes one directly, it checks for its own inputs and tells the user what's missing. This orchestrator is only needed for a full or resumed run.

## When the pipeline ends

After step 7, give the user three lines: the v1 in one sentence, the assumption the prototype tests, and the top issue from the critique. Then point to `out/decisions.md` as the record of what was decided and by whom.
