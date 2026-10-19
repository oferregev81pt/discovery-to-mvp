# Discovery to MVP

A Claude plugin that takes you from raw customer interview transcripts to a scoped v1, a cut list you can defend, and a prototype someone can click.

Most "AI for discovery" advice stops at "paste your transcripts, get themes in three minutes." The themes are the easy part. The work that decides your MVP happens around them: fixing transcripts that put one person's words in another's mouth, separating what people say from what their stories show, finding where two personas want opposite things, and cutting features on the record. This plugin does that work in seven steps, adds two optional ones for presenting the work, and stops after each one so you make the call.

Built by [Ofer Regev](https://theaipmhub.com) for The AI PM Hub.

## The pipeline

| # | Skill | What it does | What you decide |
|---|-------|--------------|-----------------|
| 0 | `interview-guide` | Writes event-anchored interview questions per persona, before the calls | Who to talk to first |
| 1 | `transcript-reconcile` | Merges one or two auto-transcripts of the same call, fixes speaker labels and mangled terms, numbers every turn | Which merge notes are right |
| 2 | `persona-extract` | Pains with quotes and severity, workarounds, numbers, prompted vs unprompted, stated vs revealed, silences | Whether the top pain matches the call |
| 3 | `persona-collide` | Maps the workflow with an owner per step and finds where personas clash | Which side v1 favors |
| 4 | `problem-framing` | A problem statement under 80 words with no solution words, plus rejected framings | Which problem you solve |
| 5 | `mvp-scope-cutlist` | v1, what it won't do, and a cut list with a reason, a cost and a revisit trigger per cut | What you push back on |
| 6 | `prototype-brief` | Ranks assumptions and writes a build-ready brief for the riskiest one | Which assumption to test |
| 7 | `prototype-build-critique` | Builds the single flow, then reviews it as a skeptical head of product in a fresh context | What to fix before anyone sees it |
| 8 | `future-ideas` (optional) | A one-year position, a path from v1, and three to five bets nobody asked for, each tied to evidence | Which bet leads |
| 9 | `mvp-story-deck` (optional) | The whole process and the MVP as a slide deck: why, what we heard, what changed, the problem, v1, the test, what's next | Whether the titles tell the story |

`discovery-to-mvp` is the orchestrator. It runs the steps in order and keeps a decision log in `out/decisions.md`.

## It stops after every step

There is no autopilot. Even if you say "run the whole pipeline", each step:

1. Shows its key results in the chat, not just a file path.
2. Asks one to three decisions, with its recommendation marked as a recommendation.
3. Asks how to continue: next step, redo this step with changes, edit the output together, or stop.

Then it waits. Nothing moves until you answer, and every answer is logged with who made it.

## What changed in 1.1

Based on feedback from a product review of work built with this pipeline. The reviewer said the work started from screens instead of the why, that the customer's biggest complaint became a one-line field, that a premise ("customers trust us") wasn't tested against the call, and that the call tested ideas instead of digging into pain. Fixes:

- `interview-guide` starts from the business outcome, lists the team's beliefs and a question that would break each, bans "would this work for you" with rewrites, and adds an after-call self-check.
- `persona-extract` splits trust by object (person, process, output, reasoning), tags operational vs confidence pains, and flags a `Named top pain` that can't be scored below 2.
- `problem-framing` audits premises before drafting and adds a business case: one number, a chain with each link marked evidence or assumption, and the weakest link.
- `mvp-scope-cutlist` adds a business-link rule and a centrality check so the customer's biggest complaint can't shrink into a field without a written reason.
- New: `future-ideas` and `mvp-story-deck`.

## Rules every step follows

- **Turn IDs.** Every claim about what someone said cites a turn from the merged transcript, like `[TAM-024]`. No ID means it's labelled as an interpretation, or it's removed.
- **Raw stays raw.** Original transcripts are never edited, so any quote can be checked.
- **Hedges are data.** "Maybe one a week" is a finding. It doesn't get tidied away.
- **No solutions before step 5.** Ideas that come up early are parked, not built on.

## Install

### Claude Code

```
/plugin marketplace add oferregev81pt/discovery-to-mvp
/plugin install discovery-to-mvp@ai-pm-hub
```

Or from your shell:

```
claude plugin marketplace add oferregev81pt/discovery-to-mvp
claude plugin install discovery-to-mvp@ai-pm-hub
```

Skills then run as `/discovery-to-mvp:transcript-reconcile`, `/discovery-to-mvp:persona-collide`, and so on. You can also just ask: "run the discovery pipeline on these interviews."

### Claude.ai

Each folder under `plugins/discovery-to-mvp/skills/` is a standalone skill. Zip a folder and upload it as a custom skill in Claude's settings. Upload all eleven to run the full pipeline.

## Use it on your own interviews

Set up a folder like this:

```
context/brief.md   # the problem space, who you interviewed, a glossary, your constraints
raw/               # the original transcripts, as exported
```

The brief can be half a page. The glossary matters more than it looks: transcription tools mangle exactly the product names and acronyms you'd put in it. If the brief is missing, the pipeline asks for it before starting.

Outputs go to `out/`, numbered by step, and the prototype goes to `prototype/`.

Tip: if you can, record each call with two tools (your meeting tool's transcript plus a second recorder). One usually gets the speakers right and the other gets the words right. Step 1 merges them.

## Try it on the sample case

`examples/harvest-line/` is a fictional case you can run end to end. Harvest Line is a produce distributor. Tamar, a head chef, orders by WhatsApp voice note at midnight. Avi, her sales rep, types those orders into the warehouse system until 1 a.m. The brief from leadership asks for an ordering app.

It contains a short brief and three raw transcripts, messy on purpose: Tamar's call exists in two versions that disagree about who said what, and one of them cuts off mid-sentence. Copy the folder somewhere, open it in Claude Code with the plugin installed, and say "run the discovery pipeline."

## License

MIT
