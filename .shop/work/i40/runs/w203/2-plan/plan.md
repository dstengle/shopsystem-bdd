# Plan of w203: spec-integration#r45

## 1. What goes green

- **spec-integration#r45**: "When a round of the kind `integrate` is given answers that ask for lines the request's accepted lines do not, `initiative-round` shall draft those lines under the capabilities the answers name."
  - Scenario (features/spec-integration.feature, @r45): "a round of the kind integrate given answers that ask for a line the request's accepted lines do not drafts that line under the capability the answers name".
  - Red today: `StepDefinitionNotFoundError` at its first Given ("a request whose accepted lines ask that the customer sees the status of an order"). None of its six steps has a definition (notes §1). Even with steps, nothing tells the round that an answer's extra lines are to be drafted. The integrate brief gives the accepted lines, the drafted ids and the change-list form, but nothing about answers beyond the accepted lines. The agent's and the skill's integrate text name the answers only "from round 2" and require every line to quote the note (notes §1, §3).
- Retired scenarios: none. The work-item has no Retires section and no Rulings.

## 2. Where the change lands

- `scripts/supervise_brief.py`: the integrate brief gains one fixed sentence, next to the change-list sentence. It says that where an answer asks for lines the request's accepted lines do not, the round drafts those lines under the capabilities the answer names. The sentence is given when the brief carries answers (decision D2).
- `agents/initiative-round.md`: the `integrate` bullet's input names the person's answers in any round, not only from round 2. It says that lines an answer asks for beyond the accepted lines are drafted under the capabilities the answer names, and that each such line quotes the answer (D3).
- `skills/integrating-a-proposal/SKILL.md`: step 2's rule that every line quotes the note sentence it comes from also accepts a quote of the answer it comes from. Step 1 names answers as an input alongside the note (D3).
- `tests/scenarios/spec_integration_steps.py`: the six r45 steps, in the existing module (107 lines, room 193), with the current When reused or shared (D4, D5).

Changes from the researcher's set:
- Removed: `scripts/workqueue_request.py`. No reader of a request's `## Answers` is added (D1).
- Removed: `tests/scenarios/test_spec_integration.py`. It already imports everything in `spec_integration_steps.py`, and no new steps module is made (D5).
- Added: `agents/initiative-round.md` and `skills/integrating-a-proposal/SKILL.md`. r45's actor is `initiative-round`, and today its text would remove an answer's line as unquoted (r2) (D3).

## 3. Decisions

- **D1: the answers an integrate round is given come by the existing path.** That path is the initiative's own `## Questions` and `## Answers`, which `answer_lines` already writes into every brief of the initiative, including the integrate brief (notes §2, probe 2). No reader of the request's `## Answers` is added, and `integrate_lines` keeps its request reading through `accepted_lines` unchanged. This also keeps the `due` gate and the UTF-8 refusal the notes' §5 warns about.
  - Rests on: supervision r57, under which a brief carries its own work-item's answers; for an integrate round that work-item is the initiative. And on r45, which is conditional on the round being given answers but does not say where the answers come from. Giving them is supervision's work. q18's line 2 (the capability-proposal's questions and answers given to an integrate round) is a separate supervision line, not this work-item's.
  - The researcher read r45 as needing the request's `## Answers`. No requirement says a request's answers go to a round; under requests they are the asker's exchange with the upstream.
- **D2: the brief's r45 sentence is given only when the integrate brief carries answers.** A round given no answers gets the brief it gets today. This follows how the r44 sentence (`REQUEST_LINES`) is given only when an upstream is named.
  - Rests on: spec-integration r45, whose condition is "is given answers".
- **D3: a line drafted from an answer quotes the answer, and the round keeps it.** It is not removed and asked as a question for lacking a note quote. The agent and skill text say so, and that the line goes under the capability the answer names, a new capability included.
  - Rests on: spec-integration r45 (draft those lines), and r2 (a line that quotes no sentence of its source is a question), read with r4 (an answer drafted as a further round).
- **D4: what the Then checks.** Because the round is the stub, the drafting alone would pass without any change (notes §1, harness caveat). So the Then checks three things:
  - (a) the integrate brief carries the answer, naming notifications, and the r45 sentence;
  - (b) the kept drafts under the integrate stage directory's `drafts/round-*/spec/capabilities/notifications.md` hold the shipping line. The stub's plan must write under `round-1`, because a change list naming a capability absent from `spec/` is refused unless its drafts are under `round-*` (r107; notes §2, probe 3);
  - (c) `work run` wrote the drafted `notifications` capability-proposal from the change list (supervision r92).
  - Rests on: spec-integration r45, supervision r57, r92 and r107.
- **D5: the Givens.**
  - The request Given writes q1 with one accepted line, the customer sees the status of an order, and i1 `fulfils: q1`, as the r44 Given does.
  - "none of those lines asks ..." asserts that no accepted line mentions shipping.
  - The answer Givens write i1's `initiative.md` `## Questions` with one question and `## Answers` with the answer that the customer is told when an order ships, naming notifications.
  - The When either reuses `run_integrate` under a second step text or shares its body.
  - Rests on: D1.

## 4. Tests the decisions break

None. I checked this against the notes' §4, which was verified by reading:
- `supervision_rounds_steps.py` `integrate_started` (lines 212-217) asserts that line 1 and line 3 are in the brief and line 2 is not. Its initiative has no answers, so under D2 its brief is unchanged.
- `supervision_integrate_steps.py` `integrate_given_ids` reads only the `Ids drafted elsewhere` line.
- The r44 Thens in `spec_integration_steps.py` read flat drafts and the brief's upstream and glossary words. Neither D2 nor D5 touches them.
- No test asserts an integrate brief's answer lines. The notes found no match for "Answers the person gave" anywhere in tests/.
- The agent and skill text are run by no test.

## 5. Open cases

- An answer that asks for a line the accepted lines already ask: is it drafted once, or given as a question?
- An answer that names no capability.
- An answer that names more than one capability.
- An answer that names an existing capability rather than a new one.
- An `## Answers` bullet with no matching `## Questions` bullet. `answer_lines` pairs them by position and drops the extra.
- The research found a defect outside r45 (notes §6, defect 1): an integrate round's result `questions` are kept only in its result.json and never written where the person sees them. This plan does not fix it. The implementer names it; it is not chosen here.
