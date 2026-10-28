# Notes: w223 (supervision r162, r163)

Tools: `tools refs` and `tools size` ran. `tools tests-of` and `untested` have no map ("make one with tools map"), so test lists below are `by search`.

## 1. Why each scenario is red today

Command (run): `python3 -m pytest -q --work-item w223`. Result: 4 failed, 180 passed, 1 skipped.

All four accepted outlines fail at their first Given, an undefined step (`StepDefinitionNotFoundError`):
- `features/supervision.feature` line 1336, r163 "answers it" and "leaves it for the person" rows: `spec/index.md's Glossary holds the term "ledger"`. No step matches it (`tests/scenarios/` has only lowercase `glossary` steps in spec_integration and design_model_check).
- `features/supervision.feature` line 1354, r162 rows: same undefined Given (`spec/index.md's Glossary holds the term "ledger"`).

Steps after the first undefined one were not reached. By search, these are undefined too:
- r162 Given `i1's glossary-proposal g1 is awaiting-answer`: no step in `tests/scenarios/`.
- r162 Then `"<question>" was given to no session`: no step in `tests/scenarios/`.

Missing in code, not only in steps: `scripts/supervise_answers.py` `Answers.answers` (line 69-76) gives every open question to `ask`. No code reads glossary terms or glossary-proposal ids to skip a question.

## 2. Old assumptions

Places that assume every open question under a delegation goes to a session (`read`; callers by `tools refs`):

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_answers.py:Answers.answers (69-76) | calls `ask` for every open question, before the `left` check | skip a question naming a term or glossary-proposal, without calling `ask` (r162, r163) | `by search`: tests/scenarios/supervision_delegation_steps.py r77 steps; tests/scripts/test_supervise_answers.py (stub `ask`, no open question so `ask` not reached) | refs open_questions, read |
| scripts/supervise_answers.py:Answers.answers (74-78) | n-th answer goes to n-th bullet; after a gap, later answers dropped | a skipped question is a gap; later eligible questions have no bullet slot (see conflict below) | `by search`: r77 steps (no gap case) | read |
| scripts/supervise_answers.py:Answers.open_questions (59-60) | returns every question without an answer | unchanged; the move check at line 81 still needs `== []`, so a left question keeps the item `awaiting-answer` | `by search`: r77 scenarios | refs open_questions (3 refs: supervise.py local name, supervise_answers 72, 81) |
| scripts/supervise_answers.py:Answers.delegation (36-48) | reads the request's `delegation` | unchanged | `by search`: r77 scenarios | read |
| tests/scripts/test_supervise_answers.py:Stubbed | stubs `delegation`, `asking`, `held`, `ask`, `section`, `move`, `commit`, `uncommitted`, `push` | if the new filter is a method on `self`, the stub lacks it and fails with AttributeError; a module-level function avoids this | the one test there, `test_a_reviewers_item_...` | read |
| scripts/supervise_glossary.py:withheld (9-18) | terms of glossary-proposals not `approved` | not reusable as is for r162: a proposal's id and its approved terms must count too | `by search`: tests/scenarios/spec_integration_apply_steps.py | refs withheld (1 ref, supervise_brief 86) |
| scripts/supervise_brief.py:Briefs answer stage (43-44) | gives the answering session the question, the delegation, the files it names, nothing else | unchanged; a session now never sees a term question | `by search`: supervision_delegation_steps.py r77/r163 Thens | read |
| scripts/model_parse.py:glossary_entry (200), bullets (120) | read `- **term**: ...` bullets of a `## Glossary` section | reusable for term reading of spec/index.md (model_facts.py:149 does it) | `by search`: tests/scripts/test_model_glossary.py | read, refs |

## 3. Tests the requirements make impossible to keep

- `features/supervision.feature` r77 Outline at line 1302 (`@deprecated`, Deprecated for: the r163 outline text). Its questions name no glossary term and no proposal id, so it still passes after the change: kept. It is retired by w223's `## Retires` (r73). The w223 file has no `## Retires` section today; the planner should draft it (planner's call, two readings: list line 1302 only, or also line 1320 "Deprecated for: removal", which r73 does not name).
- `features/supervision.feature` r77 Outline examples: no term in them, so sound under the new rule (checked by reading their Given lines).
- `tests/scripts/test_supervise_answers.py::test_a_reviewers_item_with_every_question_answered_and_no_verdict_from_this_run_is_not_moved`: sound. It asserts no session, no move, no write; the question is answered already so `open_questions` is empty. Only the stub shape matters (row 5 above).
- No other test asserts that a glossary question goes to a session (searched `tests/` for `glossary`, `delegation`; hits are model and spec-integration glossary steps only, not supervision answers).

## 4. The file set

Production:
- `scripts/supervise_answers.py` (146 lines): before `ask`, skip each open question naming a glossary term or a glossary-proposal id; leave it open and mark `left`. Shown by read of lines 59-91.
- `scripts/supervise_glossary.py` (27 lines): add a reader of the initiative's glossary-proposal ids (any status) and their `adds/changes/removes` terms (`FIELDS`), and of spec/index.md's `## Glossary` terms. Shown by read; `withheld` is the model.
- `scripts/model_parse.py` (271 lines), read only, reusable `glossary_entry` and `bullets`; or write a local reader in supervise_glossary.py. Shown by refs.

Tests:
- `tests/scenarios/supervision_delegation_steps.py` (204 lines): add the Given `spec/index.md's Glossary holds the term "<term>"` (writes `## Glossary` bullet), the Given `i1's glossary-proposal g1 is awaiting-answer` (writes `.shop/work/i1/g1.md`, kind glossary-proposal), and the Then `"<question>" was given to no session` (no `delegation-answerer` start whose brief holds the question). Shown by grep for step text.
- `tests/scripts/test_supervise_answers.py` (56 lines): add a unit test of the filter; keep `Stubbed` working (new filter as a module function, or a stub method). Shown by read.
- `features/supervision.feature`: the w223 `## Retires` list is drafted, not edited here (r73).

Path, edited or not, with line counts (`wc -l`) and room under 300 (`tools size --limit 300` prints none over the limit):
- scripts/supervise.py: 293 lines, room 7 (Run class mixes in Answers, line 42; not edited).
- scripts/supervise_worker.py: 259, room 41 (the answering session's worker, not edited).
- scripts/supervise_brief.py: 216, room 84 (answer brief, not edited).
- scripts/model_parse.py: 271, room 29 (read only).
- scripts/model_facts.py: 287, room 13 (reads Glossary, not edited).
- scripts/supervise_answers.py: 146, room 154.
- scripts/supervise_glossary.py: 27, room 273.
- tests/scripts/test_supervise_answers.py: 56, room 244.
- tests/scenarios/supervision_delegation_steps.py: 204, room 96.
- tests/scenarios/test_supervision.py: 268, room 32 (step `(?P<name>\w+) is awaiting-answer` at line 147 exists).

Conflict, for the planner (both readings, not decided here): r163 says each eligible question goes to a session of its own, but `supervise_answers.py` line 74-78 and the n-th-bullet rule (`supervise_answers.py` implementation line of `## Answers` in spec) mean that a skipped question before an eligible one leaves no slot for the later answer. Reading A: skip such later questions' sessions too, stopping at the first left question. Reading B: give each eligible question its session and write its answer only if the bullet slot is free, else leave it with a question. No scenario covers a mixed case.

Matching of "names a term" is open: reading A, whole word, case-insensitive ("ledger" does not match "ledgers"); reading B, substring. The scenarios name only one term each, so both pass.
