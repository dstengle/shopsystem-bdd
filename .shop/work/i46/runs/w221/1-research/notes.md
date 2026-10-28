# w221 research: design-model-check r122, r123, r124

Tools: `tools tests-of` answered "no map", so every test list here is `by search`. `tools refs` ran for PART_KINDS and STATUSES.

## 1. Why each scenario is red today

Command (run): `python3 -m pytest -q --work-item w221`. Result: 23 failed, 188 passed, 1 skipped.

- r122, "a glossary-proposal's list naming a term the glossary lacks...": 12 of 12 rows failed (run). Output tail cut the first errors, so the failing step is read, not seen. Read: no step matches "a <status> glossary-proposal whose <list> names term/<term>". The only matching step, `tests/scenarios/design_model_check_given.py:118`, accepts `capability-proposal` only. The remover steps ("no other glossary-proposal", "an approved ... glossary-proposal whose removes names term/shelf") have no step either. Code behind it: `scripts/model_work.py:153-175` reads term refs for capability-proposals only; `PART_KINDS` (`model_work.py:17`) lacks glossary-proposal; no set of terms removed by approved glossary-proposals.
- r123, "an initiative may be `done` when its glossary-proposal is approved": 1 row failed (run). Read: the Given "under it a glossary-proposal with status approved" has no step (`design_model_check_trace.py:114,119` take capability-proposal only). Code: `scripts/model.lp:57` closed() omits `approved`, so `v_d1` (`model.lp:243`) would still name the done initiative once the step exists.
- r124, "a malformed work directory or work file is a file problem": 10 of 18 rows failed (run). Each fails at `tests/scenarios/design_model_check_problems.py:103`, the else branch of `malformed_work`: `AssertionError: <case>` (run shows "initiative.md has no status" and "...capability-proposal and the status awaiting-answer"). Read, the 10 failing rows and what the code does:
  - "initiative.md has no status": no branch; code prints it (`model_work.py:106,212-219`).
  - "capability-proposal ... awaiting-answer": no branch; `STATUSES` (`model_work.py:11`) has it, so it passes once the branch exists.
  - "glossary-proposal ... drafted / formulated / approved" (3 rows): no branch. Code: glossary-proposal is not a PART_KIND (`model_work.py:17`), so `read_part` (`:137-138`) prints "needs an id and a kind" for the two does-not-print rows; no lifecycle in `STATUSES` (`:9-16`), so `formulated` is not printed.
  - five work-item rows (drafted, withdrawn, drafted-guarantees, green-retired, done-retired): no branch; `malformed_work` writes no work-item with `accepts`, though `tests/scenarios/conftest.py:118` `work_item()` does. Code already implements the rule (`model_work.py:194-200`).
  - Passing 8 rows: no initiative.md, initiative no id, priority high, date 16/10/2026, p1 no id, banana, p1 no status, capability-proposal built.

## 2. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/model_work.py:read_part, capability-proposal branch (153-175) | reads `term/` refs of capability-proposals; excuses `removes` of merged or formulated ones | r122: glossary-proposal lists read the same; removes excused by an approved glossary-proposal too | tests/scripts/test_model_glossary.py:56 (capability-proposal rows); r66 rows via subprocess | refs PART_KINDS; search `term/` |
| scripts/model_work.py:9-16 STATUSES | no glossary-proposal entry, so its status is unchecked | r124: drafted, awaiting-answer, approved, withdrawn (read, see question 3) | none | search `glossary-proposal` in tests |
| scripts/model_work.py:17 PART_KINDS, read_part:137-138 | refuses glossary-proposal as a part kind | r124: a part kind | none for glossary-proposal | search |
| scripts/model.lp:57 closed() | `approved` does not close a part (capability-proposal excluded by node check) | r123: approved closes a glossary-proposal | none | search `approved` in tests |
| scripts/model.lp:243 v_d1 and :273 v_d2 | done initiative needs closed parts; abandoned too | r123: approved glossary-proposal stops blocking done; drafted still blocks | design_model_check_trace.py done and abandoned rows, by search | search `closed` and v_d1 |
| scripts/model_facts.py:28 WORK_KINDS | PART_KINDS plus initiative and request; drives r121 id check (`:89`) | glossary-proposal ids become r121-checked once in PART_KINDS | none found for glossary-proposal (by search) | refs PART_KINDS |
| scripts/model_work.py:194-200 accepts | exempts guarantees capabilities and green-retired ids; withdrawn is closed | already matches r124; no change | design_model_check_problems.py r124 rows, red today (by search) | read |
| scripts/workqueue_done.py:13 and :34 CLOSED_PROPOSAL, _holds | counts capability-proposals only; a glossary-proposal never blocks queue done | r123 is model check's rule; queue rule not in scope (question 2) | tests/scripts/test_workqueue_done.py:18-28 (capability-proposal rows) | search `CLOSED_PROPOSAL` |
| scripts/supervise.py:264 exit status | exit 0 when statuses are green, withdrawn, formulated or merged | read in part: whether glossary-proposal statuses reach it is unknown | tests/scripts/test_supervise_show.py:36-37 | read in part |

## 3. Tests the requirements make impossible to keep

- The 23 red cases are the targets, not kept tests.
- Search for tests of old behaviour: `glossary-proposal` appears in tests only in design_model_check_problems.py (r124 rows) and spec_integration_apply_steps.py (not read; by search it writes proposals of the apply round). No test asserts a glossary-proposal is refused as a part or ignored by model check.
- Kept and sound (read): tests/scripts/test_model_glossary.py:56-63 (r66, capability-proposal term Store, unchanged by r122); tests/scripts/test_workqueue_done.py:18-28 (capability-proposal approved does not complete; the queue's rule is untouched); tests/scripts/test_model_reading.py:50-56 (status lifecycle of `failed`, unaffected).
- none for the other rules by search.

## 4. The file set

Production and tests the work-item must change:
- scripts/model_work.py: add glossary-proposal to STATUSES and PART_KINDS; term refs read for glossary-proposal; approved glossary-proposal removes excused (across parts, see question 1).
- scripts/model.lp: add `approved` to closed() at line 57 (r123). Not Python, so CLAUDE.md's limit does not apply; the file is 332 lines already.
- tests/scenarios/design_model_check_given.py: step for `a <status> glossary-proposal whose <list> names term/<term>` and the removes-remover steps (r122).
- tests/scenarios/design_model_check_trace.py: Given "under it a glossary-proposal with status approved" (r123).
- tests/scenarios/design_model_check_problems.py: malformed_work branches for the 10 red rows (r124).
- tests/scenarios/conftest.py: a glossary-proposal writer beside `proposal()` (`:145`) for the steps above.

Modules on the change's path, edited or not (`wc -l`, room to 300):
- scripts/model_work.py: 219 lines, room 81 (edited).
- scripts/model.lp: 332 lines, not Python (edited).
- scripts/model_facts.py: 287 lines, room 13 (not edited; WORK_KINDS picks up the change).
- scripts/model_parse.py: 271 lines, room 29 (not edited; reads glossary bullets and frontmatter lists).
- scripts/model: 139 lines, room 161 (not edited; the command entry).
- scripts/model_check.py: 139 lines, room 161 (not edited; prints the rows).
- scripts/model_report.py: 87 lines, room 213 (not edited).
- scripts/workqueue_done.py: 78 lines, room 222 (not edited; question 2).
- tests/scenarios/design_model_check_given.py: 244 lines, room 56 (edited).
- tests/scenarios/design_model_check_trace.py: 243 lines, room 57 (edited).
- tests/scenarios/design_model_check_problems.py: 270 lines, room 30 (edited; r124 branches may need ~20 lines, a split is near).
- tests/scenarios/conftest.py: 176 lines, room 124 (edited).
- tests/scenarios/design_model_check_then.py: 255 lines, room 45 (not edited; `term/<term> is ... unresolved` steps at :148 and :181 reuse).

## Questions for the plan (both readings)

1. r122's excuse: an approved glossary-proposal in any initiative of the context, or in the same initiative? The scenario has one initiative. The spec's "an approved glossary-proposal" is unscoped.
2. A drafted glossary-proposal under a done initiative: model check's v_d1 (`model.lp:243`) blocks it, while `workqueue_done.py` ignores it. r123 names only the approved case; the plan decides whether the queue should match.
3. The glossary-proposal lifecycle: read as drafted, awaiting-answer, approved, withdrawn (decision 0073 ledger; supervision r160 and r169 use awaiting-answer). The scenarios fix drafted, approved (not blocked) and formulated (a problem) only.
