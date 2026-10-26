# w201 research notes

Work-item w201 (i38, supervision), fixes branch review 2's findings. Accepts 20 requirements; the brief lists 64 accepted scenarios, all in `features/supervision.feature` and bound in `tests/scenarios/test_supervision.py`. Worktree HEAD `6941b590`. No `tools map` exists, so every count below is `by search` or `refs`, not `tests-of`.

## 1. Why each scenario is red today

None is red. Run: `python3 -m pytest -q -p no:warnings --tb=line -rfE tests/scenarios/test_supervision.py` (run). Result: 64 passed in 5.02 s. This is the whole file, not each node id one by one; it holds every accepted scenario (r4 x5, r31, r32 x2, r36, r37 x3, r45 x4, r61, r86, r87 x3, r88 x3, r89 x3, r90 x3, r115 x3, r128 x5, r129 x5, r130 x4, r131 x5, r132 x10, r133, r134).

Open gap, not an accepted scenario: the branch review's Important finding 1 (`.shop/work/i38/runs/branch-review/2/findings.md`, read) says a formulate round on a proposal whose `adds` names a guarantees capability's requirement can never reach `formulated`. No accepted scenario pins it; the r131/r132 formulate rows use `thing#r4`. A scenario for it would be red today (see section 2, probe P1).

## 2. What the system answers today

P1. `python3 -m pytest -q -s -p no:cacheprovider -n 0 .shop/scratch/w201-1-research/probe_guarantees.py` (run). The probe calls `supervise_outputs.unformulated(<worktree>, ids)` directly, not through `work run`.
- ids `planning#r1, review#r1, formulation#r1, supervision#r132, supervision#r3, supervision#r999, thing#r1-r3, term/x` gave `['planning#r1', 'review#r1', 'formulation#r1', 'supervision#r3', 'supervision#r999', 'thing#r1-r3']`.
- Guarantees ids (`planning`, `review`, `formulation`: `group: guarantees` in `spec/capabilities/*.md`) are lacking only for having no feature file.
- `supervision#r3` lacking is correct (its only scenario is deprecated). `thing#r1-r3` is lacking though ranges are a valid id form (read finding 2 of the review).
- Feature file missing for capability `nowhere`: `planning#r1` lacking (second test in the probe, same run).

P2. Wiring read, not run: `scripts/supervise_rounds.py:148-154`. A formulate round with no question calls `unformulated` on the proposal's `adds` and `changes`; a lacking id becomes a question via `supervise_outputs.question`, so the proposal goes to `awaiting-answer`. Each answer starts another formulate round (`supervise_rounds.py:60-61`, read), so the loop repeats.

P3. Nearest cases of the accepted formulate rows, read from `tests/scenarios/supervision_formulate_steps.py` (83 lines) and the r131/r132 outlines: the formulate check is reached only when a formulate round gives no question. No accepted scenario gives a question and no scenario together, or an empty `adds`. Not run.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/supervise_outputs.py:unformulated` | counts every id of a capability with no feature file as lacking | a guarantees capability has no scenarios (design-decision 0065, r56/r64/r65); the check must skip them, as `work_items.guarantees` does | none (no map; by search, no test names it) | search (`tools refs unformulated`: 1 caller) |
| `scripts/supervise_rounds.py:formulate branch (152-154)` | asks the lacking ids as one question | the caller is unchanged if `unformulated` skips guarantees ids | by search: the r131/r132 formulate rows in `tests/scenarios/test_supervision.py` | refs, read |
| `scripts/supervise_outputs.py:scenario_ids` | reads only `Scenario:` and `Scenario Outline:` and ignores ranges | a fix that reads tags through `features_gherkin` (review finding 2) changes what counts | none; by search | read (review finding 2) |
| `scripts/supervise_outputs.py:unformulated` (old scenario) | a changed requirement's old scenario counts | r132 "a scenario for each requirement ... changes": open case, review finding 4 | by search: `supervision_formulate_steps.py` | read |
| `scripts/work_items.py:guarantees` | reads `group: guarantees` | the reader the fix should reuse, not a place that assumes | by search: `tests/scenarios/supervision_tests_steps.py:165-173` (`steady` guarantees) | refs (1 test file) |

## 4. Tests the requirements make impossible to keep

No test asserts that a guarantees id is lacking. `grep -rn "guarantees" tests/scenarios/supervision_*.py` (by search) finds only `supervision_tests_steps.py` (a `steady` capability fixture for r56/r64/r65), which asserts the work-item test rules, not the formulate check. Verified sound by reading: the r131/r132 formulate tests use `thing`, which has a feature file. Result: none can no longer pass; but none covers the guarantees case, so a new scenario is needed to stop regression.

## 5. A step the work-item skips

None (read). The fix adds a skip in the check, not a path that leaves out a step. Probe P1 shows the check reads the feature file at HEAD, not the round's diff (review finding 4), which is the existing behaviour.

## 6. Defects

### D1. A formulate round on a guarantees requirement can never reach `formulated`
Reproduction:
- `python3 -m pytest -q -s -p no:cacheprovider -n 0 .shop/scratch/w201-1-research/probe_guarantees.py` (run).
- Came back: `unformulated: ['planning#r1', 'review#r1', 'formulation#r1', ...]`.
- Read: `supervise_rounds.py:150-154` turns that into a question, so the proposal goes to `awaiting-answer` (r83 says `formulated`).
- Source: `.shop/work/i38/runs/branch-review/2/findings.md` finding 1 (Important, fix now).

## 7. The file set

Production:
- `scripts/supervise_outputs.py` (62 lines; room 238): `unformulated` skips ids of `group: guarantees` capabilities (search: `tools refs unformulated`, read). Also the range and synonym gaps of review finding 2, if the plan takes them.
- `scripts/supervise_rounds.py` (198 lines; room 102): only if the plan changes the formulate branch (lines 148-154, read). Also ruff I001 at line 7 (review finding 3, read; `tools check --base 50a40103` reports it, run: not run here, carried from review).
- `scripts/work_items.py` (150 lines; room 150): read `guarantees` for reuse; change only if the plan moves the reader.

Tests:
- `tests/scenarios/test_supervision.py` (265 lines; room 35): the binding of new scenarios is `scenarios("supervision.feature")`, so new feature scenarios need no edit here unless new step imports are added (read).
- `tests/scenarios/supervision_formulate_steps.py` (83 lines; room 217): the formulate-round steps for a guarantees row (search).
- `tests/scenarios/supervision_session_faults_steps.py` (118 lines; room 182): `stage_gives` commits a scenario for the formulate row (review, read); a guarantees row would not commit one.
- `features/supervision.feature` (1626 lines, not Python; no line limit): a scenario for a guarantees requirement and an r132 row (read; finding 1's fix).

Modules on the change path with line count and room under 300:
- `scripts/supervise_outputs.py` 62 (238); `scripts/supervise_rounds.py` 198 (102); `scripts/work_items.py` 150 (150); `scripts/supervise_change.py` 88 (212, read: writes proposals, not on the formulate path); `tests/scenarios/test_supervision.py` 265 (35); `tests/scenarios/supervision_formulate_steps.py` 83 (217); `tests/scenarios/supervision_session_faults_steps.py` 118 (182).
- `tools size --limit 300` printed nothing (run): no tracked Python file is over the limit now.
