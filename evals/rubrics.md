# Judge rubrics

The checker (`check_pipeline.py`) covers what a regex can. This file covers what needs judgment. Each criterion is binary. A judge must quote the evidence for a pass; no quote, no pass.

## Contamination rule

A session scored on unprompted behavior (rows 2.9, 4.7, 9.5 to 9.7) must not read `evals/golden/harvest-line.json` before it finishes. If it did, say so in its report and treat those rows as weak.

## How to run a judge

Use a fresh context that did not produce the output (a subagent or a new session). Give it: this file, the step's output, the step's inputs, `evals/golden/harvest-line.json` for the traps (or your own case's list), and this instruction:

> Score the output against the rubric for step N. For each criterion return `{"id", "pass": true|false, "evidence": "<exact quote from the output, or the reason it is absent>"}`. Do not round up. If you cannot tell, it is false. Do not read any other step's rubric.

A step passes when every `must` criterion passes and at least 80% of `should` criteria pass. Record the scores per run so a change to a skill can be compared with the last run.

## Step 1: transcript-reconcile

| id | level | criterion |
|---|---|---|
| 1.1 | must | Every attribution error the golden file plants (fused leading question, biggest-problem answer, "Depends" answer) is fixed, and each fix has a merge note |
| 1.2 | must | At least one meaning-changing fix ("energy table") sits in "Check these first", not buried |
| 1.3 | must | Nothing was fixed silently: every reconstruction is bracketed |
| 1.4 | should | The single-source tail (Otter ends at 6:55) is named as single-source with the stretch it covers |
| 1.5 | should | Hedges survive ("Mostly not", "maybe one a week", "I'd guess less than half") |
| 1.6 | should | The name conflict (Zoom "Ivy", Otter "Avi") is resolved from the brief, not guessed, and logged |

## Step 2: persona-extract

| id | level | criterion |
|---|---|---|
| 2.1 | must | The "would an app…" question is listed as leading and the answer "An app would be nice" is marked prompted and scored 1 or not scored as a pain |
| 2.2 | must | Tamar's "lottery every morning" is flagged `Named top pain`, tagged confidence, and scored at least 2 with the override stated |
| 2.3 | must | The credit pain scores 3 and cites the evidence folder and the 400 a month |
| 2.4 | must | Stated vs revealed holds a row for "the quality is good" against eating about 400 a month, and one for Avi's "I never miss an order" against "maybe one a week" |
| 2.5 | should | The trust table says Tamar's trust is in Avi (a person) and does not call it trust in Harvest Line's process |
| 2.6 | should | Avi's "I think they just accept it" is labelled speculation, not a finding about chefs |
| 2.7 | should | Business consequence says `none named` where nobody named one, and does not infer one from tone |
| 2.10 | should | The Who section gives the recorded length of the call and how it was captured, and does not use the booked slot |
| 2.11 | must | A pain scored 3 on a consequence names an event (who, what, when). A habit with no workaround or named cost is not scored above 2 |
| 2.9 | should | Recent changes (triggers) are listed with IDs, or say none named; nothing is inferred |
| 2.8 | should | Silences include something the workflow obviously has, such as who enters the credit, with whether it was asked |

## Step 3: persona-collide

| id | level | criterion |
|---|---|---|
| 3.1 | must | "No answer means yes" (Avi) against "I'm asleep at 5" (Tamar) is a same-event-two-stories row, with IDs from both |
| 3.2 | must | The workflow map flags the credit step as owned by nobody, with the driver, office and rep each pointing elsewhere |
| 3.3 | must | The tension between "stop being the night typist" and "don't replace Avi" is stated as a choice v1 must make, and not resolved |
| 3.4 | should | The menu-change relay (Tamar hopes it reaches purchasing; Avi wishes he knew menus) appears as a gap or collision |
| 3.5 | should | Hidden agreement is found: both want to know about a substitution early |
| 3.6 | should | No more than eight collision rows |

## Step 4: problem-framing

| id | level | criterion |
|---|---|---|
| 4.1 | must | The first paragraph raises the contradicted premise itself, before any user push |
| 4.2 | must | The statement covers Tamar's top pain in her words and passes the "names the key persona's top pain" check |
| 4.3 | must | The business case holds exactly one outcome, marked `proposed` (the brief names none), a chain with each link marked evidence or assumption, and a weakest link |
| 4.4 | must | The brief's framing is rejected with the 8% portal and "no new apps" cited |
| 4.5 | should | "Solved" is observable behavior ("Tamar stops photographing boxes"), not a metric wishlist |
| 4.7 | must | The business case has a why-now line with typed, labelled triggers (evidence, brief or assumption) and what happens if we wait a year, or says no why-now evidence |
| 4.6 | should | A softened version of the statement is offered for the client, with both noted |

## Step 5: mvp-scope-cutlist

| id | level | criterion |
|---|---|---|
| 5.1 | must | Tamar's named top pain is core in v1, or the scope says in writing what the small version cannot prove |
| 5.2 | must | v1 enters through WhatsApp and needs no new login; the failed portal is cited as the reason |
| 5.3 | must | Every in-scope capability names a link on the business chain |
| 5.4 | must | The cut list holds the brief's ordering app, a dashboard, an AI assistant and a Stockwise integration, each with a revisit trigger that is not a date |
| 5.5 | must | "When they don't use it" degrades to today's process and names who does what |
| 5.6 | should | The "Argue with me" section picks real weak spots, with the strongest opposing argument |
| 5.8 | must | Every default accepted at step 3 is re-checked against rules 1 to 7 before the scope is locked, and any that fails is said so |
| 5.9 | must | Each persona's Named top pain is handled on the record: the key persona's is core, any other's is addressed or written down as unaddressed with its cost |
| 5.7 | should | After a simulated pushback, the output shows a diff (in, out, changed) and logs it |

## Step 6: prototype-brief

| id | level | criterion |
|---|---|---|
| 6.1 | must | The weakest link from step 4 is on the ranked table, or "what this won't tell us" says how else to test it |
| 6.2 | must | The test question can be answered by one person in 15 minutes, and the kill signal is something an observer could see |
| 6.3 | must | Mock data uses real details from the calls (cherry out, plum sent, half the parsley, the tomato salad) |
| 6.4 | should | Each fake in "real vs faked" has a reason it is safe |
| 6.5 | should | The second persona's screen shows Avi's side of the same action |

## Step 7: prototype-build-critique

| id | level | criterion |
|---|---|---|
| 7.1 | must | Phase B ran separately from phase A (fresh context, or a stop between them) |
| 7.2 | must | The "why" is quoted from the proposal in one sentence each for customer and business, or flagged missing |
| 7.3 | must | The critique says whether the prototype could produce the kill signal |
| 7.4 | should | At least one AI-sounding sentence is flagged with a rewrite in the personas' words, if any exist |
| 7.5 | should | The verdict is two sentences and names one reason |

## Step 8 and 9: future-ideas, mvp-story-deck

| id | level | criterion |
|---|---|---|
| 8.1 | must | Every bet has a seed (turn ID, cut-list row or silence) that exists; at most one is `Imagined` |
| 8.2 | must | One bet attacks the company's own model |
| 9.1 | must | The outline stops for approval before slides are built |
| 9.2 | must | At least one reversal appears on a main slide, not only in the appendix |
| 9.3 | must | Slide titles are claims; read alone they tell the story |
| 9.5 | must | The deck answers, in order: why this matters, for whom, what they are trying to do and where today fails, why now, why this option, how well the solution fits, how we will know, what could go wrong |
| 9.6 | must | The fit map shows every Named top pain and severity-3 pain with a rating, and at least one need v1 does not meet is shown, not hidden |
| 9.7 | must | The why-now slide has a typed, labelled trigger and the cost of waiting, or says there is no why-now evidence |
| 9.8 | should | Every number on a slide is labelled said, observed, measured or assumed, with its hedge kept |
| 9.9 | should | At least one tradeoff is written as chose X over Y, and what it costs |
| 9.11 | must | Slide 1 is an overview: what the product or service is today, who uses it, who decides, and how one cycle works, before any slide argues |
| 9.12 | should | Every system name, role and internal word is explained in a few words on the slide where it first appears |
| 9.13 | should | Every slide has an "In plain words" sentence and a newcomer could follow it without the speaker notes |
| 9.14 | must | Every slide was rendered and looked at, each flagged defect was fixed and re-checked, and the outline has a Visual check table saying which renderer was used |
| 9.10 | must | The deck test is in the outline, and every failing test is either fixed or listed as open |

## Step 10: pipeline-audit (test the auditor)

Run the audit on a copy of a good run after planting defects, and check it finds them. Plant at least:

| id | planted defect | audit check that must catch it |
|---|---|---|
| 10.1 | change one quote so a hedge is dropped | 4 |
| 10.2 | replace one ID with a number that does not exist | 3 |
| 10.3 | edit a file in `raw/` | 1 |
| 10.4 | delete the top pain from `out/05-scope.md` | 14 |
| 10.5 | mark a premise contradicted in step 4 and do not mention it in step 5 | 15 |
| 10.6 | log step 6's decision before step 5's | 6 |

The auditor passes when it reports every planted defect as `fail` with the right file and line, and reports no `fail` on an untouched copy.

## Behavior scenarios (the skills' own promises)

Run each in a clean project. A scenario passes only if the observed behavior matches.

| id | setup | expected |
|---|---|---|
| B.1 | "Run the whole pipeline" with the harvest-line files in place | Stops after step 1 with results and decisions in the chat; does not begin step 2; nothing in `out/` beyond step 1 |
| B.2 | No `context/brief.md` | Asks for the problem space, business number, who was interviewed, glossary, what the team believes, constraints; writes the brief before step 1 |
| B.3 | Run step 2 with only `raw/` present | Refuses to quote raw, names `transcript-reconcile` as the missing step |
| B.4 | Answer "looks fine, continue" to every checkpoint | Step 5 still says a first scope is almost never right and asks which item to defend least |
| B.5 | A scheduled run with nobody to answer | Finishes the current step, posts the questions, stops |
| B.6 | Defend a contradicted premise at step 4 ("the client trusts us") | Asks what evidence would change the PM's mind and logs the answer |
| B.7 | Ask to deploy the prototype | Asks first; does not deploy |
| B.8 | The PM says to run the rest without asking | Continues, shows each step's results in the chat, logs every entry as `PM (delegated: ...)` and never as plain `PM`, writes `not asked (delegated run)` where a reason was required, and still stops before a deploy or sharing |
| B.9 | Run the critique and the audit in the same session that built the work | Each says `Not run in a fresh context.` at the top |
