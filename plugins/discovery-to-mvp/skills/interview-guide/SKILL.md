---
name: interview-guide
description: Writes a discovery interview guide before customer or stakeholder calls — learning goals, the riskiest assumption behind each, and event-anchored questions per persona, plus recording setup that makes later synthesis reliable. Use when someone is about to run discovery interviews, asks "what should I ask them", or wants to prep calls with clients, users or internal teams.
---

# Interview guide (pipeline step 0)

Good synthesis starts before the call. Most bad discovery data comes from hypothetical questions ("would you use…"), leading questions ("would a dashboard help?"), and pitching. This skill writes a guide that avoids those and sets up the recording so step 1 has something to reconcile.

## Inputs

- `context/brief.md`: the problem space, who will be interviewed, what the team already believes. If it's missing, ask for these three things in one message.
- Optional: an existing solution idea the team is attached to. Ask for it explicitly. It's better to know the bias than to have it leak into the questions.

## Process

1. **List what we need to learn.** Write 4 to 6 learning goals. Each is a question about the world, not about a feature. Good: "How does a client know a request was seen?" Bad: "Do clients want a status page?"
2. **Name the assumption behind each goal** and how bad it is if wrong (high / medium / low). Order goals by that.
3. **Map goals to personas.** For each persona, mark which goals they can actually speak to. A client can't tell you how production schedules work; an account manager can't tell you what the client does on Sunday.
4. **Write questions per persona, 6 to 8 each.** Rules:
   - Anchor in a specific recent event: "Walk me through the last time…", "Tell me about last night's order."
   - Ask about behavior and workarounds: "What did you do then?", "Where do you keep track of that?"
   - Ask for numbers when they'd naturally exist: how often, how many, how long.
   - One "what do you like / what must not change" question. People protect things you'd otherwise break.
   - One "what's the biggest problem, if you had to pick one" question, late in the call, after they've told stories. Compare their answer to their stories in step 2.
   - Close with "What should I have asked and didn't?"
5. **Write probes** the interviewer can use anywhere: "What happened next?", "How did you know?", "What did you do instead?", "Can you show me?", "How often?"
6. **List what not to ask** for this specific project, including the leading version of the team's favorite solution (e.g. "Would a dashboard help?"). Explain that if it slips out, the answer must be marked as prompted in step 2.
7. **Listen-for list.** Things worth noting live: workarounds people built themselves (spreadsheets, DMs, screenshots), emotional words, numbers, things they say twice, things they hedge.
8. **Recording setup.** Recommend:
   - Record with two transcription sources if possible (e.g. the meeting tool's transcript plus a second recorder). One usually gets speaker labels right and the other gets wording right; step 1 merges them.
   - Write the glossary (product names, internal tool names, acronyms) into the brief before the call; transcription tools mangle exactly these.
   - Note the interviewer's name as it will appear in the transcript.

## Output: `out/00-interview-guide.md`

```
# Interview guide — <project>
## Learning goals (ordered by risk)
| # | Goal | Assumption behind it | Risk if wrong | Personas who can answer |
## Questions — <Persona A>
1. ...
## Questions — <Persona B>
## Probes
## Don't ask
## Listen for
## Recording setup
```

Keep it to two pages. An interviewer has to be able to glance at it mid-call.

## Stop here: show the results and ask how to continue

This step always ends with a stop, including when it runs inside a full pipeline or the user said "run everything". Never start the next step, and never apply a decision, until the user answers.

1. **Show the results in the chat**, not only the file path: the learning goals table and the first three questions for each persona. Then say where the full file is.
2. **Ask the decisions below.** Give your recommended answer for each, clearly marked as a recommendation.
3. **Ask how to continue**, offering: Continue to step 1, `transcript-reconcile` (once the calls are recorded) · redo this step with changes · edit the output together · stop here.

Then wait for the user.

### Decisions for you

End with:
- "Which persona do you talk to first?" (Recommend the one closest to the money or the pain; the second call can then probe what the first revealed.)
- "Is there a solution the team is already attached to? I've put its leading question on the don't-ask list; tell me if I named the wrong one."
