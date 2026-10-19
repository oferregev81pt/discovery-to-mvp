---
name: future-ideas
description: Writes a point of view on where the product should go over the next year and brings ideas nobody asked for, each rooted in discovery evidence, the cut list or a conspicuous silence, with customer value, business value, what must be true and the cheapest test. Use after the prototype critique, when a PM needs to show strategic thinking beyond the MVP, or when someone asks "where does this go next", "what's the vision", or "what should we bring that they didn't ask for".
---

# Future ideas (pipeline step 8, optional)

A v1 answers the brief. A senior product person also says where the product is going and shows something the stakeholders didn't ask for. Without that, the work reads as a fix for today's process. This step turns the evidence into a position and a short list of bets, and keeps imagination tied to what people said, what they didn't say and what the cut list parked.

## Inputs

- `out/04-problem.md` (problem, business case), `out/05-scope.md` (v1, cut list with revisit triggers), `out/03-collisions.md` (including "Neither mentioned"), `out/02-extract-*.md` (silences, workarounds, "their words") and `out/07-critique.md`
- `context/brief.md` (business outcome, constraints, what the team believes)
- Every `Parked ideas` line from earlier outputs
- Optional: what the PM already knows about the company's strategy, competitors or data assets. Ask once if missing: "What does the company have that others don't (data, relationships, tech), and where does it want to be in a year?"

## Process

### 1. State the position
Write a paragraph, no more than 120 words, that opens with "In a year, this product is…" It names who it serves, what job it does for them and for the company, and why this company is the one to build it. It must be falsifiable: someone can disagree with it. Avoid the word "platform" unless the next clause says what it does.

Then one line: **v1 is the first step because** it proves X, which makes Y possible.

### 2. Draw the path
Three horizons, each a sentence or two and each tied to the cut list:
- **Now (v1):** the capability that proves the core assumption.
- **Next:** the 2 or 3 cut-list items whose revisit trigger v1 is designed to hit, in order, with the trigger.
- **Later:** what the product is when the triggers have been hit.

### 3. Find the seeds
Collect candidates from four places and write each with its source:
- **Cut list:** items cut for lack of supply or data. What would make them possible?
- **Silences and "neither mentioned":** things the workflow clearly includes that nobody raised. The best unrequested ideas live here.
- **Workarounds:** the shadow spreadsheets and relays that show a job nobody serves. What product would make them unnecessary?
- **The company side:** an asset the company has that the customer doesn't see (data across many customers, staff judgment, an internal engine, a library of past results). What would it look like if that were the product, not the service around it?

Add one candidate that **attacks the company's own model**: something that makes part of today's service unnecessary or cheaper to run, or changes who the customer is. If every idea protects the current model, the list is too safe.

### 4. Cut to three to five bets
For each bet:
- **Idea** in one sentence, and one line on why nobody asked for it.
- **Seed:** the evidence, with turn IDs, or the cut-list row or the silence it grows from. If there is no seed, it is a guess; label it `Imagined` and keep at most one.
- **Customer value** (one sentence) and **company value** (one sentence, tied to the business outcome in `out/04-problem.md`).
- **What must be true:** the two or three assumptions it rests on, typed as desirability, usability, feasibility or viability.
- **Cheapest test:** the smallest thing that would show it is worth building, doable in a few days (an interview, a fake door, a spreadsheet, one client, a pilot).
- **Kill signal.**
- **Risk of being wrong:** what we'd have spent.

Rank by value to the business times strength of the seed. Mark one **Lead with this**.

### 5. What to say out loud
Two lines the PM can use in a room: the vision in one sentence, and the first bet in one sentence with its cheapest test. Plain words. Include the evidence the idea grows from.

## Rules

- **Imagination needs a seed.** An idea with no turn ID, cut-list row or silence behind it is labelled `Imagined`, and there is at most one.
- **No feature lists.** A bet is a change in what the product is for, not a screen.
- **Don't promise what the company can't supply.** If an idea needs data or access the company doesn't have, say so in "what must be true". A real constraint belongs in the idea.
- **Say what v1 gave up.** If a bet reverses a cut, say the cut was right for v1 and name the trigger that changes it.
- **Plain writing.** No "platform", "ecosystem", "unlock", "seamless", "AI-powered" without a concrete mechanism after it.

## Output: `out/08-future-ideas.md`

```
# Where this goes
## Position (<n> words)
v1 is the first step because ...
## Path
| Horizon | What | Trigger / depends on |
## Bets
### 1. <name> — Lead with this
Idea / Why nobody asked / Seed [IDs] / Customer value / Company value / What must be true / Cheapest test / Kill signal / Risk
### 2. ...
## One bet that challenges our own model
## Say it in the room
```

## Stop here: show the results and ask how to continue

This step always ends with a stop, including when it runs inside a full pipeline or the user said "run everything". Never start the next step, and never apply a decision, until the user answers. The one exception is a delegated run, as the orchestrator defines it: show the results, log the delegated decision and continue.

1. **Show the results in the chat**, not only the file path: the position paragraph, the path table, the bets in one line each with their seeds, and the "say it in the room" lines. Then say where the full file is.
2. **Ask the decisions below.** Give your recommended answer for each, clearly marked as a recommendation.
3. **Ask how to continue**, offering: Continue to step 9, `mvp-story-deck` · redo this step with changes · edit the output together · stop here.

Then wait for the user.

### Decisions for you

- "Is this the position you'd defend? Where would you say it differently?" (If the PM can't say it in one sentence, the position isn't done.)
- "Which bet leads? I recommend <X> because <one line>."
- "Is there a bet on the list the company would never do? Keep it as a challenge, or drop it?"
- "Update the 'First step of' section of `out/05-scope.md` to match this position?" (Recommend yes: step 5 wrote it from the business case before this step existed.)
