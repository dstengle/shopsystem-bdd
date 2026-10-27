# w203 research notes: spec-integration r45

Tools: plugin scripts at `/home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts`. `tools size --limit 300` ran (no file over 300). `tools tests-of` and `untested` refused: "no map" (I did not make one). `tools refs workqueue_request.accepted_lines` returned 0, but two production calls exist (supervise_brief.py:110, supervise_rounds.py:43, by search): refs did not follow the attribute call. Test lists below are `by search`.

Probes: `.shop/scratch/w203-1-research/probe_r45.py`, `probe_integrate_questions.py`. Run with `python3 -m pytest -q -s -n 0 <path>` (`-n 0` because the project's addopts start xdist and swallow prints). Probe repos are under the scratch directory, built with the scenario helpers (`repository`, `run_integrate`, `rounds`).

Stray file: `probe_r45.py` was first written into the run directory by mistake. My shell cannot delete it. It is ignored by git (`.shop/`) and `work run` removes it with the worktree.

## 1. Why each scenario is red today

Scenario: `features/spec-integration.feature` @r45, "a round of the kind integrate given answers that ask for a line the request's accepted lines do not drafts that line under the capability the answers name".

- Command: `python3 -m pytest -q "tests/scenarios/test_spec_integration.py::test_a_round_of_the_kind_integrate_given_answers_that_ask_for_a_line_the_requests_accepted_lines_do_not_drafts_that_line_under_the_capability_the_answers_name"`. Result: `StepDefinitionNotFoundError` on line 20, `Given "a request whose accepted lines ask that the customer sees the status of an order"` (run).
- Undefined steps by search, not yet reached (the first undefined step stops the run): the Given "none of those lines asks that the customer is told when an order ships", the Given "an answer that asks that the customer is told when an order ships", the Given "that answer names the capability notifications", the When "work run starts a round of the kind integrate given that request and that answer", the Then "the round drafts, under notifications, a line that the customer is told when an order ships" (by search: no definition in tests/).
- Missing in step definitions: all five. `tests/scenarios/spec_integration_steps.py` has the r44 steps only. `run_integrate` (line 60) runs `work run i1` with the stub, and reads its plan; a new When can reuse it.
- Missing in code: `scripts/supervise_brief.py:integrate_lines` (line 103) gives the request's accepted lines (`workqueue_request.accepted_lines`) and the ids, but not the request's `## Questions` and `## Answers`. So an answer on the request never reaches the integrate round (see section 2, probe 1).
- Code that does give answers, for an initiative: `supervise_brief.py:answer_lines` (line 133) reads the initiative's own `## Questions`/`## Answers` (`supervise.py:held`, `name == initiative` → `initiative.md`). Nothing in the round flow writes those for an integrate round (see section 6, defect 1).
- Harness caveat for the Then: the stub writes only the plan's `write` path; the Then can pass whether or not the brief carried the answer. The Then should check the brief's answer line too, or the Given should be checked by the brief.

## 2. What the system answers today

Probe 1 (`probe_r45.py::test_request_answer_round_path`), run: request q1 accepted line 1 "The customer sees the status of an order.", `## Answers` 1 "The customer is told when an order ships, under notifications.", initiative i1 `fulfils: q1`, plan writes `notifications.md` under `drafts/round-1/` and a change list adds `notifications#r1`.
- Result: returncode 0. Brief (`work run` started one integrate round): `Request: q1`, `Accepted lines of the request:`, `- 1. The customer sees the status of an order.`, `Ids drafted elsewhere ...: none`. No answer line. The kept drafts hold `notifications.md`; `notifications.md` proposal written.
- The answer does not reach the round. The round drafts what the stub's plan says, so the scenario's "drafts under notifications" passes only through the stub.

Probe 2 (`test_initiative_answer_round_path`), run: same, but the answer is in i1's `initiative.md` `## Questions` and `## Answers`.
- Brief shows `Answers the person gave, each with the question it answers:` / `- Question: line 1: ...` / `  Answer: The customer is told when an order ships, under notifications.` So the existing initiative-answer path already carries an answer to an integrate round (read: `answer_lines` runs for every stage).

Probe 3 (`test_request_answer_no_round_path`), run: the same as probe 1 but the plan's drafts path is `drafts/spec/capabilities/notifications.md` (no `round-1`). Result: returncode 1, `its change list names notifications, which neither spec/capabilities/ nor its drafts have`. `supervise_change.py:unknown` (line 43) counts only `drafts/round-*/spec/capabilities/*.md`. The r44 scenario's stub writes flat drafts, which is harmless there only because `thing` exists in `spec/` (read). A new-capability Then must glob under `round-*`.

Nearest cases not run (read): request with an answer numbered 2 and only question 1: the existing code gives no answer line at all, so there is no pairing to test today. Request with no `## Questions`: the brief gets only accepted lines (as probe 1 minus the answer).

## 3. Old assumptions

Requirement r45 adds a second source of answers for an integrate round (the request's `## Answers`), next to the initiative's own `## Questions`/`## Answers`.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_brief.py:integrate_lines (103) | gives the round the request's accepted lines and the drafted ids only | must also give the request's answers, paired with its questions by number (r21: answer n answers question n) | by search: tests/scenarios/supervision_rounds_steps.py:212 (`integrate_started`, asserts lines 1 and 3 in brief, line 2 not); tests/scenarios/supervision_integrate_steps.py:186 (`integrate_given_ids`, reads the `Ids drafted elsewhere` line) | read; probe 1 |
| scripts/supervise_brief.py:answer_lines (133) | answers come from the work-item's own `## Questions`/`## Answers`, for `name == initiative` read from initiative.md | stays for initiative answers; the request's answers come from a second reader | none: by search no test asserts an `Answers the person gave` line | read; probe 2 |
| scripts/workqueue_request.py:accepted_lines (32) | reads `## Lines` and `## Outcomes` only | a new reader of `## Questions`/`## Answers` sits beside it | by search: none directly; reached only through `work run` scenarios (supervision_rounds_steps.py:212) | read |
| scripts/supervise_rounds.py:due (35-46) | calls accepted_lines as the gate: a request the queue lacks gives no round | the new answer read must come after this gate, or the same `Refused` must hold | by search: tests/scenarios/supervision.feature:1022 scenario (a request not held gives no round) | read |
| scripts/supervise_rounds.py:run_round (128, 145, 149) | `questions` of an integrate result are not used; `asked` is set for gate, apply, formulate only | not changed by r45 (see defect 1) | none (no integrate round scenario asserts questions) | read; section 6 probe |
| agents/initiative-round.md:27 and skills/integrating-a-proposal/SKILL.md:23 | the integrate input is "the note's path, or from round 2 the person's answers" | the request's answers are an input the text does not name | none (prompt text, not run by tests) | read |

## 4. Tests the requirement makes impossible to keep

`tools tests-of` has no map, so this list is `by search`. I read the integrate-brief assertions:
- tests/scenarios/supervision_rounds_steps.py:212-217 (`integrate_started`): asserts `Line 1 text.` and `Line 3 text.` in the brief and `Line 2 text.` not in it. Still passes with request answers, provided no answer contains `Line 2 text.`. Verified by read only.
- tests/scenarios/supervision_integrate_steps.py:186-193 (`integrate_given_ids`): checks the `Ids drafted elsewhere` line. Unaffected.
- tests/scenarios/spec_integration_steps.py:88-107 (r44 Thens): read `DRAFTS` flat under `drafts/spec/capabilities/thing.md`, and the brief for `BILLING` and `glossary`. Unaffected by r45.
- No test asserts that an integrate brief has no answer line (search for `Answers the person gave` and `Accepted lines of the request` in tests/: no match for the first; only the scenario steps above for the second).
Conclusion: none of the existing tests can no longer pass. I did not run the whole suite.

## 5. A step the work-item skips

The new path reads a request's answers. The existing way reads the request through `workqueue_request.accepted_lines` (via `due`), which:
- refuses a request the queue does not hold (`path_of`: "there is no request ..."); `due` turns that into no round (read; `supervise_rounds.py:42-46`; existing scenario supervision.feature:1022);
- refuses a request file that is not UTF-8 (`workqueue.read`, lines 50-55: "is not UTF-8 text") (read);
- drops lines whose outcome is not `accepted` (read).
A new answers reader that does not go through the same gate would give a round answers for a request `due` has refused. Effects only the existing step produces: the refusal and the UTF-8 refusal. Neither shown by a probe here; both read.

## 6. Defects

### Defect 1: an integrate round's question is kept only in result.json

Reproduction (`probe_integrate_questions.py::test_integrate_question_is_kept`, run):
- Request q1 with accepted line 1, empty `## Questions`/`## Answers`; i1 proposed, fulfils q1.
- The stub's integrate result gives `changes` (adds notifications#r1) and `questions: ["Should the customer be told by e-mail or by SMS?"]`.
- Result: returncode 0; one integrate round; `notifications` proposal written; `initiative.md` now `status: started` with no `## Questions` section. The question appears only inside the kept `runs/i1/1-integrate/result.json`.
- Read: `supervise_rounds.py:128` and `:145-149` use `questions` for gate, apply and formulate only. Spec r1 of spec-integration says every open question of a note is shown to the person; this path shows none.

### Defect candidate 2: none proven
A flat-draft change list is refused (probe 3). That is the r107 behaviour, not a defect.

## 7. The file set

Edited:
- `scripts/supervise_brief.py` (190 lines; room 110): `integrate_lines` also gives the request's `## Answers`, each paired with its `## Questions` line. Found by probe 1 and read of lines 103-114.
- `scripts/workqueue_request.py` (186; room 114): a reader of a request's question/answer pairs beside `accepted_lines` (lines 27-37, `_entries`). Found by read of `asked_here` (40-54), which already reads Questions and Answers.
- `tests/scenarios/spec_integration_steps.py` (107; room 193), or a new module `tests/scenarios/spec_integration_answers_steps.py`: the five undefined steps; the Then must check the brief's answer line and drafts under `round-*`. Found by section 1.
- `tests/scenarios/test_spec_integration.py` (8): only if a new steps module is used, import it. Found by read.

Modules on the change's path, edited or not:
- `scripts/work` 171 (room 129): entry point, not edited.
- `scripts/workqueue.py` 294 (room 6): `read` and `committed`, not edited.
- `scripts/supervise.py` 284 (room 16): `held`, `section`, not edited.
- `scripts/supervise_rounds.py` 198 (room 102): `due`, `run_round`, not edited.
- `scripts/supervise_drafts.py` 32 (room 268): the `Ids drafted elsewhere` line, not edited.
- `scripts/supervise_change.py` 88 (room 212): `unknown` (round-n drafts), not edited.
- `tests/scenarios/supervision_rounds_steps.py` 272 (room 28): `rounds` helper, not edited.
- `tests/scenarios/supervision_world.py` 173, `tests/scenarios/supervision_given.py` 259 (room 41), `tests/scripts/stub_claude.py` 281 (room 19): helpers the scenario's stub and repository use, not edited.
- `tests/scenarios/supervision_integrate_steps.py` 201 (room 99): integrate helpers, not edited.

Not in the file set: `agents/initiative-round.md` and `skills/integrating-a-proposal/SKILL.md` describe the integrate input; no test runs them. Not needed for r45's scenario.
