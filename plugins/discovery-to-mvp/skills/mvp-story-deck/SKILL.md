---
name: mvp-story-deck
description: Turns the whole discovery pipeline into a slide deck that argues for the MVP the way a product decision-maker reads it — why this problem and for whom, why now, how the solution fits the needs one by one and where it does not, why this option and not the obvious alternatives, how we will know it worked, and what could go wrong. Runs a deck test on the outline before anything is built, then builds the deck with the host's slide tool. Use when the PM has to present, defend or hand over the MVP and the process behind it, or asks for "a deck", "slides", "the story" or "why should we build this".
---

# MVP story deck (pipeline step 9, optional)

A deck that walks through the exercise ("here is what I did") loses to a deck that argues ("here is why this matters, why now, how the solution meets what people need, and how we will know"). This step builds the second kind, in a fixed order, from files that already exist, and tests the outline against product-sense rules before building. The output is a slide deck, not a markdown file.

The order follows one rule from product work: **customer and user first.** The deck never describes the solution before it has said who it is for, what they are trying to do, and where today fails them.

## Inputs

- Everything in `out/` and `out/decisions.md`. Required at minimum: `out/04-problem.md`, `out/05-scope.md`. Without them, stop and name the missing step.
- `out/02-extract-*.md` for the needs, the pains and the recent changes (triggers). `out/03-collisions.md` for the tradeoffs.
- `out/08-future-ideas.md` if it exists. If not, say so and recommend running `future-ideas` first; if the PM declines, the "why now" and "why us" lines come from the business case and the cut list's revisit triggers.
- `out/07-critique.md` and the prototype link if built or deployed.
- `context/brief.md` for the audience and the team's stated why now.
- Ask once if missing: who will see this (a hiring panel, a leadership team, a client), how long they have, and whether it is presented live or read alone.

## The questions the deck must answer

A decision-maker asks these in this order. Each gets one slide (two at most). The slide's title is the answer, as a full claim.

| # | Question | Source | The slide must contain | If the pipeline lacks it |
|---|---|---|---|---|
| 1 | **Why does this matter?** | `04` business case, `02` | Who is hurt, what it costs them in their own terms, and the one business number it should move, each with a strength label | Say "not yet known" and what would measure it. Never fill it in |
| 2 | **Who is it for?** | `02`, `03`, brief | Users (who use it) and customers (who pay or decide), and which one v1 serves first and why | Name the missing side as a risk |
| 3 | **What are they trying to do, and where does today fail them?** | `02`, `03` | A table: need, how it is served today, where it breaks, evidence ID. Include each persona's Named top pain | |
| 4 | **What did we hear, and how much does it prove?** | `02`, brief | Who, how many conversations, how long, real or roleplayed; strength of each claim. No prevalence from a few calls | |
| 5 | **What did we get wrong?** | `04` premise audit, `decisions.md` | The reversals: what we believed, what the evidence said, what we did. At least one | If there is none, say nobody tested a premise |
| 6 | **Why now?** | `04` business case (why now), `02` triggers, brief | One to three triggers, each typed (customers changed, our situation changed, what is possible changed, cost of waiting) and labelled `evidence [ID]`, `brief` or `assumption`. What happens if we wait a year | `no why-now evidence`: say so on the slide, and say that this argues for a cheap test before a build |
| 7 | **Why this option and not the obvious alternatives?** | `04` framings, `05` cut list, `08` | The brief's solution, the current workaround and one real alternative, each with why not. If `08` exists, one line on why this company is the one to do it | |
| 8 | **How well does the solution fit the needs?** | `05`, `02` | The fit map: each need from slide 3, the v1 capability that meets it, and a fit rating (fits, partly, does not) with the reason. Needs v1 leaves unmet are shown, with why | |
| 9 | **What is v1, and what is it not?** | `05` | The one-sentence v1, the 3 to 6 capabilities, what v1 does not do, and the cut list for the three cuts that cost the most, with their revisit triggers | |
| 10 | **What did we trade off?** | `03`, `05` collisions decided | One or two choices written as "we chose X over Y because Z, and we lose W" | |
| 11 | **How will we know it worked?** | `05` adoption plan, `06` | The business signal tied to the number on slide 1, the leading indicator, the riskiest assumption, the test and its kill signal, and what the prototype cannot show | |
| 12 | **What could go wrong, and what do we need?** | `07`, `04`, `05` | The top critique issues and which were fixed, the open unknowns, the next cheapest test, and the decision or help needed | |

No more than 12 slides. An appendix may hold the full cut list, the collisions table, the premise audit and the quotes. If two questions share one slide, say so in the outline. Never reorder.

## Process

### 1. Write the outline, with the deck test, in a file
`out/09-story-outline.md`: one row per slide with the question it answers, the **claim** (a full sentence), its strength, the evidence IDs and the source file. Re-read the source files for every number and every quote; do not work from memory. Then run the deck test below, write its results in the same file, and show both (see "Stop here"). Build slides only after the PM approves the outline.

### 2. The deck test
Run every row. A fail is fixed in the outline, or kept and written in the "open" list on slide 12.

| # | Test | Pass when |
|---|---|---|
| T1 | Titles alone | Reading only the slide titles in order, a stranger could answer: why, for whom, why now, why this option, does it fit, how will we know, what could go wrong |
| T2 | Customer first | No slide describes the solution before slides 1 to 3 have named the user, the need and where today fails |
| T3 | Why | Slide 1 names who is hurt, what it costs, and exactly one business number, each with a strength label |
| T4 | Why now | Slide 6 has at least one typed trigger with a label and the cost of waiting a year, or states `no why-now evidence` and the plan changes |
| T5 | Fit | Every Named top pain and every severity-3 pain appears on the fit map with a rating, and every unmet need is shown |
| T6 | Alternatives | The brief's solution, the current workaround and one real alternative each have a reason they lost |
| T7 | Tradeoff | At least one choice is written with what it costs |
| T8 | Validation | One business signal, one kill signal, the riskiest assumption, and what the prototype cannot show |
| T9 | Strength | Every number is labelled said, observed, measured or assumed; no claim about how many people behave a way from a few calls; hedges kept ("maybe", "like") |
| T10 | Traceability | Every claim has a turn ID or is labelled an assumption; each number matches its source file today |
| T11 | Writing | No stock AI vocabulary, no "not just X but Y", no abstract noun where an example fits |

### 3. Rules for every slide
- **Title is a claim.** "Clients trust the PG, not the reasoning behind the builds" beats "Findings". Read only the titles: they should tell the story.
- **One idea per slide**, one visual (a table, a flow, a quote, a diagram). No bullet walls.
- **At most one quote per slide**, verbatim, with its turn ID in the speaker notes. Keep the hedge inside the quote.
- **Every number has a source and a strength**: said, observed, measured, assumed. A figure a person said is not a measurement; the slide says "said".
- **Show the weak link.** The weakest link in the business-case chain, the thing the prototype cannot tell us, and the roleplay caveat (if any) appear on the slide they apply to, not only in the appendix.
- **Show the gaps in the fit.** A deck where every need is met is not credible. A need v1 does not meet is shown with the reason.
- **Same rules as the critique.** No AI-sounding phrases (seamless, leverage, robust, empower, "not just X but Y"), no abstract nouns where a concrete example fits.
- **Speaker notes** carry the evidence IDs, the one-line reasoning behind the slide, the strength, and the likely question with an answer.

### 4. Build the deck
Use the deck tool the host provides: a slide or deck type if the environment lists one, otherwise a PowerPoint skill. Don't write the deck as markdown or HTML pages and call it done. Use the PM's design system or brand colors if given. Then open the result and read each slide for overflow, empty placeholders and titles that don't read as claims, unless the host's deck tool says not to verify; if it does, say that the slides were not checked. Report the link or file location. Don't share or send the deck anywhere without the PM's go-ahead.

## Output

`out/09-story-outline.md` and the slide deck (the link or file path goes at the top of the outline).

```
# Story outline — <project> — for <audience>, <minutes> min
Deck: <link or path>
| # | Question | Claim (slide title) | Strength | Evidence [IDs] | Source file |
## Deck test
| # | Test | Pass/fail | Why |
## Open
The tests that still fail and where the deck says so.
```

## Stop here: show the results and ask how to continue

This step always ends with a stop, including when it runs inside a full pipeline or the user said "run everything". It stops twice: after the outline, and after the deck. (If the PM has told the session to run without asking, finish the outline and deck, log the approval as delegated, and say that the outline stop was waived.)

1. **After the outline:** show the slide claims as a numbered list in the chat, with the deck-test results, not only the file path. Ask the decisions below. Wait. Don't build until the PM answers.
2. **After the deck:** show the link or path, the list of slide titles and any slide you are least sure about. Ask: redo with changes · edit together · done.

### Decisions for you

- "Reading only the titles, is this the story you'd tell? What's missing or out of order?"
- "Slide 6 says <why now, or that there is no evidence>. Is that the real reason now? If you know a trigger the calls didn't show, tell me and I'll label it as yours."
- "Slide 8 shows <n> needs v1 does not meet. Are you comfortable saying that out loud?"
- "Slide 5 shows <the reversal>. Main deck or appendix?" (Recommend the main deck; it is the evidence that the process worked.)
- "Is the audience <X>? I'd cut <slide> if you have under 10 minutes."
