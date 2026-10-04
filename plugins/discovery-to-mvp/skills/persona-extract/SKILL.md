---
name: persona-extract
description: Pulls one persona's evidence out of a merged interview transcript — pains with verbatim quotes and severity, workarounds, numbers, prompted vs unprompted signals, stated vs revealed gaps, what must not change, and conspicuous silences — every line tied to a turn ID. Use after transcripts are cleaned, when someone asks what a customer or stakeholder "really said", or before comparing personas.
---

# Persona extract (pipeline step 2)

A summary tells you what someone said. An extract tells you what you can rely on. The difference: it separates what came up on its own from what the interviewer put in their mouth, it separates the person's stated priorities from what their stories show, and it records what they never mentioned.

Run once per persona. If several interviews share a persona, run once over all of them and note which interview each line comes from.

## Inputs

- `out/01-merged-<CODE>.md` for this persona (required). If only raw transcripts exist, stop and suggest running `transcript-reconcile` first; quoting raw transcripts carries their attribution errors forward.
- `context/brief.md`, for what the team expected to hear.

## Process

Read the whole transcript once without writing. Then go through it turn by turn.

### 1. Who they are
Role, team size, how long they've been in the relationship, scale numbers (volumes, frequencies). Only what they said.

### 2. Mark every interviewer question as open or leading
A leading question names an answer ("Would a dashboard help with that?"). Any answer to a leading question is **prompted**. A pain the person raised before being asked about that topic is **unprompted**. Unprompted signals weigh more. List the leading questions you found; the PM needs to know.

### 3. Pains
For each pain:
- One-line description in plain words.
- The best verbatim quote and its turn ID. Add a second ID if they came back to it.
- **Prompted / unprompted.**
- **Severity 1–3**, scored from evidence, not tone:
  - 3 = they built a workaround, OR it cost money/time they can name, OR it happened and had a consequence (a launch missed, a fine, a complaint).
  - 2 = recurring and they can say how often, but no workaround or named cost.
  - 1 = mentioned once, no frequency, no consequence, or only in answer to a leading question.
- Evidence for the score in a few words ("keeps a private sheet since month two").

### 4. Workarounds
The strongest signal in discovery. Anything they built or do by hand to cope: a spreadsheet, DMing instead of using the thread, copy-pasting between tools, checking things nobody asked them to check. For each: what it is, how long they've done it, what it costs them, and the turn ID.

### 5. Numbers
Table of every number, count, frequency, duration or percentage they said, with the turn ID and the exact words. Keep their hedges ("maybe half, maybe less").

### 6. Stated vs revealed
Where what they **say** differs from what their **stories** show. Typical patterns:
- Says something is rare or fine, then describes it happening a lot ("the quality is good" vs "I just eat it, four hundred a month").
- Names one thing as the biggest problem, but most of the call is about another.
- Uses a solution word ("visibility", "a dashboard") whose meaning, from their stories, is something else.
- Says they're on top of something, then hedges ("mostly").

Each row: Stated (quote + ID) | Revealed (quote + ID) | Interpretation (labelled as such).

### 7. Their own "biggest problem"
Quote it in full with its ID. Then one line: does the rest of the interview support it, contradict it, or sharpen it?

### 8. Likes / must not change
What they explicitly value. Include warnings ("please don't replace Avi with a robot", "no new apps"). These become constraints in step 5.

### 9. Other people they mention
Anyone else in the loop (a partner who pays the invoices, a sous-chef who receives deliveries, a warehouse picker). Who they are, what they do in the workflow, how their input travels. Hidden relays matter.

### 10. Silences
Topics the brief expected, or that the workflow obviously includes, that this person never raised. For each: what was expected, and whether the interviewer asked (if asked and dodged, quote it). Only list silences that matter for the problem space; don't pad.

### 11. Their words
5 to 10 short verbatim phrases worth reusing in problem statements and product copy ("evidence folder", "a lottery every morning").

## Rules

- Every line from sections 3–9 and 11 has a turn ID. No ID, no line.
- Interpretations are allowed only inside fields labelled `Interpretation:`.
- No solutions. If one occurs to you, add it to a `Parked ideas` line at the end.
- Don't merge two different pains because they sound alike. "I can't find my old orders" and "my late change wasn't seen" are different problems with different fixes.

## Output: `out/02-extract-<CODE>.md`

```
# Extract — <Name>, <role>
Source: out/01-merged-<CODE>.md
## Who
## Leading questions in this interview
## Pains
| # | Pain | Quote [ID] | Prompted? | Severity | Evidence for severity |
## Workarounds
## Numbers
## Stated vs revealed
## Their biggest problem, in their words
## Must not change
## Other people in the loop
## Silences
## Their words
Parked ideas: ...
```

## Stop here: show the results and ask how to continue

This step always ends with a stop, including when it runs inside a full pipeline or the user said "run everything". Never start the next step, and never apply a decision, until the user answers.

1. **Show the results in the chat**, not only the file path: the top three pains with quote, turn ID and severity; the leading questions you found; the stated-vs-revealed rows; and the silences. Then say where the full file is.
2. **Ask the decisions below.** Give your recommended answer for each, clearly marked as a recommendation.
3. **Ask how to continue**, offering: Continue to step 3, `persona-collide` (or extract the next persona first) · redo this step with changes · edit the output together · stop here.

Then wait for the user.

### Decisions for you

- "Here's the one pain I scored highest and why. Does that match your read of the call?"
- If any leading questions were found: "These answers were prompted, so I've down-weighted them. Agree?"
