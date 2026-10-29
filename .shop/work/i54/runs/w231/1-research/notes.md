# w231 research: supervision r187

Tools: `tools refs` ran (merge_lists). `tools tests-of` had no map (`tools map` not made), so test lists are `by search`.

## 1. Why the scenario is red today

Command (`run`): `python3 -m pytest -q --work-item w231 -rfEx`
Result (`run`): 1 failed, 180 passed, 1 skipped (182 items; non-scenario tests kept, r55).
Failure (`run`): `StepDefinitionNotFoundError` on Given line 1523: "i1's capability-proposal p2, for other, is awaiting-answer, its adds naming other#r1, its changes naming other#r2 and its removes naming nothing". Lines 1521-1522 pass; later steps not reached.

Undefined or non-matching after it (`read`, not reached by the run):
- Given line 1525 "the integrate round for p1 gives DONE ... adds other#r6, changes other#r3 and removes other#r5 on other": `tests/scenarios/supervision_reintegrate_steps.py:56-57` matches only `... on thing$`; `entry()` in `supervision_formulate_steps.py:35` keeps one capability per phrase.
- Then line 1528 "p2's adds name ... and its removes name ...": no definition. `supervision_formulate_steps.py:87` matches only p1 and "removes name nothing".

Code behind it (`read`): `scripts/supervise_change.py` `Changes.write_proposals` (94-140) already merges a non-own held proposal via `merge_lists` (82-92), added by commit e4e61321 (branch-review fix). The scenario never reaches it, so this is unrun. Expected result for p2 (`read`): adds other#r1, other#r6; changes other#r2, other#r3; removes other#r5.

## 2. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_change.py:Changes.rewrite_lists | replaces a proposal's adds, changes, removes wholesale | called only for the round's own proposal (line 115); other held proposals merged | none traced | read |
| scripts/supervise_change.py:Changes.write_proposals (held branch) | rewrote every held proposal of the capability | merges ids into a non-own proposal (line 111-114), keeps its drafts path | tests/scripts/test_supervise_change.py:26, :44, :56 (by search, not run) | read; git show e4e61321 |
| scripts/supervise_rounds.py:Rounds integrate branch (line 206) | calls write_proposals without the round's proposal | passes `own=name` so the round's own proposal is rewritten | none traced | read |
| scripts/supervise_rounds.py (formulate, lines 189-193) | reads a proposal's adds and changes to ask scenarios | merged ids from another capability make p2's formulate round owe scenarios | none traced | read |
| scripts/supervise_draft.py:Drafts.draft_proposals (line 87) | one work-item for each adds or changes of a formulated proposal | merged ids of another capability land in p2's work-items | none traced | read |
| scripts/work_items.py (proposals, lines 73-83) | reads adds and changes of proposals for expected-failure marks (r122) | merged ids count as expected-to-fail for p2 | none traced | read |
| scripts/model_report.py:60-72; scripts/model.lp:185-191 | model facts per requirement id, not per capability | no change needed | none | read |

## 3. Tests the requirement makes impossible to keep

None found by search. The old wholesale rewrite of a non-own held proposal was replaced by e4e61321, whose unit tests in tests/scripts/test_supervise_change.py (26, 44, 56) assert the merge. Searched the step modules for p1/p2 integrate and apply steps; the only merge scenario is the red r187 one. Not checked: the r142/r148 scenarios in `supervision_reintegrate_steps.py`, which drive the own-proposal rewrite.

## 4. The file set

Files to change:
- tests/scenarios/supervision_merge_steps.py (new, about 60-80 lines): Given p2 awaiting-answer with `argues: [other]` and its lists; Given the integrate round for p1 with a change list on thing and on other, split per capability; Then p2's lists name the ids. Needs no module-map row (`tests/scenarios/` covers `<capability>_*_steps.py`). The alternative is `supervision_reintegrate_steps.py` (175 lines, room 125).

No production change expected: `scripts/supervise_change.py` already implements r187 (see 1). Confirm with one run once the steps exist.

Modules on the path, with lines (`wc -l`) and room to 300:
- scripts/supervise_change.py: 140, room 160
- scripts/supervise_rounds.py: 275, room 25
- scripts/supervise.py: 295, room 5
- scripts/supervise_draft.py: 122, room 178
- scripts/supervise_outputs.py: 103, room 197
- scripts/work_items.py: 164, room 136
- scripts/workqueue.py: 294, room 6 (`frontmatter` re-exported from model_parse)
- scripts/model_parse.py: 271, room 29
- tests/scripts/test_supervise_change.py: 63, room 237
- tests/scenarios/supervision_formulate_steps.py: 96, room 204 (`entry()` helper; its p1-only Then stays)
- tests/scenarios/supervision_reintegrate_steps.py: 175, room 125
- tests/scenarios/supervision_integrate_steps.py: 252, room 48 (defines "every other round ends")
- tests/scenarios/test_supervision.py: 268, room 32 (binds the scenario)

`tools size --limit 300` printed no file over the limit (`run`).
