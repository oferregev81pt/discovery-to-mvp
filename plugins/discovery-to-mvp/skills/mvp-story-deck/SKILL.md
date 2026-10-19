---
name: mvp-story-deck
description: Turns the whole discovery pipeline into a slide deck that tells the story in the order a decision-maker needs it — why it matters, what we heard, what we got wrong and changed, the problem, the v1 and its cut list, how it was tested, where it goes next and what's still open. Builds it as a slide deck with the host's slide tool. Use when the PM has to present, defend or hand over the MVP and the process behind it, or asks for "a deck", "slides" or "summarize the process and the MVP".
---

# MVP story deck (pipeline step 9, optional)

A deck that walks through the exercise ("here is what I built") loses to a deck that argues ("here is why it matters, what we learned, what we chose and what we'd do next"). This step builds the second kind from files that already exist, in a fixed order, with the reversals and the evidence visible. The output is a slide deck, not a markdown file.

## Inputs

- Everything in `out/` and `out/decisions.md`. Required at minimum: `out/04-problem.md`, `out/05-scope.md`. Without them, stop and name the missing step.
- `out/08-future-ideas.md` if it exists. If it doesn't, say so and recommend running `future-ideas` first, since a deck without direction is the gap this step exists to avoid. If the PM declines, the "where it goes" slide is built from the business case and the cut list's revisit triggers.
- `out/07-critique.md` and the prototype URL if deployed.
- `context/brief.md` for the audience and whether the calls were real or roleplayed.
- Ask once if missing: who will see this (a hiring panel, a leadership team, a client), how long they have, and whether the deck is presented live or read alone.

## Process

### 1. Write the outline first, in a file
`out/09-story-outline.md`: one line per slide with the **claim** the slide makes (a full sentence, not a topic), the evidence behind it with turn IDs, and the source file. Then stop and show it (see "Stop here"). Build slides only after the PM approves the outline.

### 2. The story, in this order
Use the slides below, merge or drop the ones that don't apply, never reorder them.

1. **Why this matters.** The business outcome and the number it should move, and who feels the pain today. From the business case in `out/04-problem.md`. This is the first content slide.
2. **Where this product goes.** The one-sentence position from `out/08-future-ideas.md`, and v1 as the first step. Put the destination before the details so the reader knows what the details are for.
3. **What we heard, and from whom.** The people, the number of conversations, and, in plain words, whether the calls were real or roleplayed. Evidence is stated at the strength it has. No prevalence claims from a few calls.
4. **What we got wrong, and what changed.** The reversals from `out/decisions.md` and the premise audit: what we believed, what the evidence said, what we did. At least one. A deck with no reversal tells the reader nobody tested anything.
5. **The problem.** The statement from `out/04-problem.md`, the customer's top pain in their own words, and the business-case chain with its weakest link marked.
6. **Where the sides collide, and what we chose.** The top one or two collisions and which side v1 favors.
7. **v1.** The one-sentence v1, the 3 to 6 capabilities, what v1 does not do. One slide for the cut list with the reason and the revisit trigger of the three cuts that cost the most.
8. **How we tested it.** The assumption, the test question, the prototype (link or screenshots) and the success and kill signals. If it hasn't been tested with a person, say what has been tested and what hasn't.
9. **What the critique found.** The top issues and what we fixed. Honesty about the weak parts is part of the argument.
10. **What we'd do next.** The lead bet from `out/08-future-ideas.md` with its cheapest test, and the next two cut-list items with their triggers.
11. **What's still open.** The unknowns, the risky premises, and the decision or help needed from the audience.

No more than 11 slides. Fewer is better. An appendix may hold the full cut list, the collisions table and the quotes.

### 3. Rules for every slide
- **Title is a claim.** "Chefs trust their rep, not the reasons behind substitutions" beats "Findings". Read only the titles: they should tell the story.
- **One idea per slide**, one visual (a table, a flow, a quote, a diagram). No bullet walls.
- **At most one quote per slide**, verbatim, with its turn ID in the speaker notes.
- **Every number has a source and a strength**: said, estimated, measured.
- **Show the weak link.** The weakest link in the chain, the thing the prototype can't tell us and the roleplay caveat appear on the slides where they apply, not only in the appendix.
- **Same rules as the critique.** No AI-sounding phrases (seamless, leverage, robust, empower, "not just X but Y"), no abstract nouns where a concrete example fits, no sentences that sound generated.
- **Speaker notes** carry the evidence IDs, the one-line reasoning behind the slide and the likely question with an answer.

### 4. Build the deck
Use the deck tool the host provides: a slide or deck type if the environment lists one, otherwise a PowerPoint skill. Don't write the deck as markdown or HTML pages and call it done. Use the PM's design system or brand colors if given. Check the result by opening it and reading each slide for overflow, empty placeholders and titles that don't read as claims. Some deck tools tell you not to verify unless asked; if yours does, don't open it unasked, and instead tell the PM plainly that the layout was not visually checked and offer to check it. Either way, check the content mechanically: every slide title appears in the outline, every number and quote on a slide is in the source files, and no slide has more than one quote. Report the link or file location. Don't share or send the deck anywhere without the PM's go-ahead.

## Output

`out/09-story-outline.md` and the slide deck (the link or file path goes at the top of the outline).

```
# Story outline — <project> — for <audience>, <minutes> min
Deck: <link or path>
| # | Claim (slide title) | Evidence [IDs] | Source file |
```

## Stop here: show the results and ask how to continue

This step always ends with a stop, including when it runs inside a full pipeline or the user said "run everything". Never start the next step, and never apply a decision, until the user answers. This step stops twice: after the outline, and after the deck.

1. **After the outline:** show the slide claims as a numbered list in the chat, not only the file path. Ask the decisions below. Wait. Don't build until the PM answers.
2. **After the deck:** show the link or path, the list of slide titles and any slide you are least sure about. Ask: redo with changes · edit together · done.

### Decisions for you

- "Reading only the titles, is this the story you'd tell? What's missing or out of order?"
- "Slide 4 shows <the reversal>. Do you want it in the main deck, or in the appendix?" (Recommend the main deck; it is the evidence that the process worked.)
- "Is the audience <X>? I'd cut <slide> if you have under 10 minutes."
