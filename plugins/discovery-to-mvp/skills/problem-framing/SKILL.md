---
name: problem-framing
description: Turns discovery evidence into a solution-free problem statement under 80 words, compares it with how the original brief framed the problem, offers rejected alternative framings with reasons, and defines what "solved" would look like per persona. Use after synthesizing interviews and before scoping, or when someone asks "what problem are we actually solving" or suspects the brief asked for the wrong thing.
---

# Problem framing (pipeline step 4)

Briefs usually arrive with a solution baked in ("customers keep complaining about mistakes, should we build an ordering app?"). The interviews often say the problem is somewhere else. This step writes down the problem the evidence supports, shows how it differs from the brief, and forces a choice between framings before anyone scopes features.

## Inputs

- `out/03-collisions.md` (required)
- `out/02-extract-*.md` (required)
- `context/brief.md` (required, for the original framing)
- The PM's answers at the step 3 checkpoint, from `out/decisions.md`

## Process

### 1. Restate the brief's framing
In one or two sentences, what problem did the brief assume, and what solution did it imply? Quote the brief.

### 2. Draft three candidate framings
- **The brief's framing**, stated as fairly as possible.
- **The evidence framing**: built from the highest-severity pains, the top collisions and the workflow gaps in step 3.
- **A narrower or broader framing**: one level down (a single step of the workflow) or one level up (the whole relationship).

### 3. Write the chosen-by-default problem statement
Default to the evidence framing unless the evidence is thin. The statement:
- Is **under 80 words**.
- Says **who** (both personas if it's a seam problem), **what's broken**, **what it costs** (time, money, a missed outcome, trust), and cites **turn IDs** for the evidence.
- Contains **no solution words**. Banned: platform, portal, dashboard, app, tool, feature, AI, automate, build, integrate, system, interface, page, view, bot. If one slips in, rewrite.
- Uses the personas' own words where they're sharper than yours (from the "Their words" section of each extract).

### 4. Test it
Run each check and write pass/fail with a line of reasoning:
- **Evidence:** every claim traces to an ID.
- **Both sides:** if it's a seam problem, both personas would recognize it.
- **Not a feature in disguise:** you can name at least two different solutions that would solve it.
- **Explains the workarounds:** the shadow spreadsheets, DMs and relays from step 2 make sense if this problem is true.
- **Explains the silences:** the things nobody mentioned are consistent with it.

### 5. Reject the alternatives, in writing
For each of the other two framings: why it's tempting and why you'd reject it (or keep it as a fallback). Cite evidence. "The brief's framing would produce an ordering app; the vendor already built a web portal that 8% of customers used [AVI-031], and the customer asked for no new apps [TAM-036]."

### 6. What "solved" looks like
For each persona, 2 to 3 observable changes in behavior if the problem were gone. Observable means you could watch it happen: "Tamar stops screenshotting every order", "Avi spends his evenings selling instead of retyping voice notes." Not metrics wishlists, not feelings.

### 7. Non-goals
Problems that are real but not this one, so step 5 doesn't scope them in by accident.

## Output: `out/04-problem.md`

```
# Problem
## The brief said
## Problem statement (<n> words)
## Checks
| Check | Pass/fail | Why |
## Framings considered
| Framing | Why it's tempting | Why rejected / kept as fallback |
## What solved looks like
### <Persona A>
### <Persona B>
## Non-goals
Parked ideas: ...
```

## Stop here: show the results and ask how to continue

This step always ends with a stop, including when it runs inside a full pipeline or the user said "run everything". Never start the next step, and never apply a decision, until the user answers.

1. **Show the results in the chat**, not only the file path: the brief's framing, the proposed problem statement with its word count, the checks table, and each rejected framing in one line. Then say where the full file is.
2. **Ask the decisions below.** Give your recommended answer for each, clearly marked as a recommendation.
3. **Ask how to continue**, offering: Continue to step 5, `mvp-scope-cutlist` · redo this step with changes · edit the output together · stop here.

Then wait for the user.

### Decisions for you

- "Which framing do we scope against? I recommend <X> because <one line>." This is the most consequential decision in the pipeline; don't let it pass as a formality.
- "Anything in the problem statement you'd say differently to the client's face?" (If the PM would soften it for the client, the softened version often hides the real problem; note both.)
