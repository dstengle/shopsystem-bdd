# w117 research notes

Method: `tools tests-of` has no map (`tools: no map: make one with tools map`), so test lists are `by search`. `tools refs` ran on Python names only. Probes ran the worktree's `scripts/model` through its real entry point. Probe file: `.shop/scratch/w117-1-research/probe_w106.py`, run `python3 -m pytest -q -s -n 0 .shop/scratch/w117-1-research/probe_w106.py`. Its fixture puts the work-item directly under the initiative, so `v_b1` and `v_k3` print in every case; that is fixture noise, not studied.

Accepted: `features/design-model-check.feature:727` (Outline, 4 rows, `@r106`) and `:742` (`@r106`). Requirement `design-model-check#r106`, rule `v_w4`.

## 1. Why each scenario is red today

- **Outline, "a work-item with no accepts and no check is v_w4, unless it is withdrawn"** (`tests/scenarios/test_design_model_check.py`, 4 rows): run, `python3 -m pytest -q <4 node ids>`, **4 passed**. Green today; it must stay green.
- **"a work-item accepting a requirement no scenario names yet, with no check, is not v_w4"** (`test_a_workitem_accepting_a_requirement_no_scenario_names_yet_with_no_check_is_not_v_w4`): run, **red at the Given**, not at the Then. `KeyError: 'accepts thing#r2 and no check'` at `tests/scenarios/design_model_check_one_each.py:41` (`world.work_item(status=status, **FIELDS[fields])`). `FIELDS` (lines 32-34) has no key for that text. Missing: a `FIELDS` entry `{"accepts": "[thing#r2]", "check": None}`.
- Behind it, once the entry exists (read, and probe A `run`): `scripts/model_work.py:184-190` (`read_part`) writes an `accepts` fact only for scenarios found by `has_sc`. With no scenario naming `thing#r2`, `scripts/model.lp:64` (`has_accepts`) is false and `scripts/model.lp:235` (`v_w4`) prints w1. The Then "w1 is not printed under v_w4" would fail.

## 2. What the system answers today

Probe file `probe_w106.py`, run `python3 -m pytest -q -s -n 0 .shop/scratch/w117-1-research/probe_w106.py`, **8 passed** (each case printed). Repository per case under `.shop/scratch/w117-1-research/repos/<case>/`.

- **A** (scenario 2's Givens): capability `thing` with `- [r2]`, no feature file; w1 drafted, `accepts: [thing#r2]`, no check. `model check` exit 1. Prints `v_w4 a work-item has no acceptance and no check` for w1, and the file problem `accepts capability/ex.com/prod/ctx/thing#r2, which no scenario names yet`. `model facts` has no `accepts` fact for w1. **Wrong**: the Then expects no v_w4.
- **B** (outline row 1): no accepts, no check, drafted. `v_w4` printed for w1. Correct.
- **C** (row 2): same, withdrawn. `v_w4` not printed. Correct.
- **D** (row 3): `accepts: [thing#r1]`, named by scenario, no check. `v_w4` not printed; fact `accepts("work-item/ex.com/prod/ctx/w1", "features/thing.feature:it answers")`. The fact's second argument is a scenario title.
- **E** (nearest, capability in `guarantees`, r2 unnamed): `v_w4` printed; no file problem (the `exempt` branch of `model_work.py:192-194` suppresses only the file problem). Same defect as A.
- **F** (nearest, `accepts: [thing#r9]`, no such requirement): `v_w4` printed and the file problem printed. See defect D2.
- **G** (nearest, withdrawn, r2 unnamed): no `v_w4`, no file problem. Correct.
- **H** (nearest, r2 unnamed plus `check: true`): no `v_w4`; file problem printed; a `check` fact `"true"`. Correct.
- The scenario's own data empty: an empty `accepts: []` is row B. Two work-items of one name: not probed; `check_work_item_name` (`model_work.py:82-89`) is `read`, out of this requirement's path.
- Unit test `tests/scripts/test_model_withdrawn.py` (r27 file-problem test): run, **2 passed**.

## 3. Old assumptions

The old form: `accepts(W, S)` is a fact whose second argument is a scenario; `has_accepts` means "accepts a scenario". `tools refs` on `WorkReading.read_part`: 1 reference, production only (`model_work.py:125`). `tools refs has_accepts`: nothing (a Prolog name). Callers found by search (`grep accepts|has_accepts|v_w4` in `scripts/`).

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/model_work.py:read_part`, lines 184-190 | writes `accepts(W, S)` only for scenarios `has_sc` finds for the accepted requirement | an accepted requirement counts whether or not a scenario names it (r106); the fact's meaning (scenario or requirement) must be decided | Outline row `accepts thing#r1` (run, passes); probe D; by search | `tools refs`, then grep |
| `scripts/model_work.py:read_part`, line 195 | file problem `accepts X, which no scenario names yet` for non-withdrawn, non-guarantees, non-retired-green | stays: features `:309` and `test_model_withdrawn.py` r27 test pin it; so the gate `found` must not drive the problem's removal | `tests/scripts/test_model_withdrawn.py` (run, 2 passed); feature `:309` (read) | grep |
| `scripts/model.lp:64` `has_accepts(W) :- accepts(W,_)` | true only when a scenario-named `accepts` fact exists | must be true for an unnamed accepted requirement too, or the rule's input changes | Outline row `accepts thing#r1` (run) | grep |
| `scripts/model.lp:235` `v_w4` | fires when `has_accepts` and `has_check` both fail, not withdrawn | the rule text already matches r106; it is wrong only through `has_accepts` | Outline rows (run) | grep |
| `scripts/model.lp:24` `#defined accepts/2` | declares the relation; second argument read as a scenario id | a requirement-valued `accepts` changes what the second argument means, or a new relation avoids it | none (declaration) | grep |
| `scripts/model_facts.py` (prints facts, 275 lines) | prints `accepts` facts as they are | prints requirement-valued facts if the fact changes; no test asserts an `accepts(` line (by search) | none | grep `accepts` |

## 4. Tests the requirements make impossible to keep

`tools tests-of`: no map; **by search**. `grep accepts\(|has_accepts|v_w4` over `tests/`: only `tests/scenarios/design_model_check_one_each.py`. No unit test asserts an `accepts` fact, `has_accepts` or `v_w4` for an unnamed accepted requirement.

- Outline (4 rows, run, passing): all four still hold under the fix (row 3 is named; rows 1, 2 unchanged). None breaks.
- `tests/scripts/test_model_withdrawn.py` r27 test (run, passing): counts `accepts` problems only; the fix leaves line 195 in place, so it holds.
- Features `:309`, `:317`, `:325` (read, step names only: `design_model_check_problems.py:107-120`): assert the file problem or its absence. Hold under the fix.
- Reading to decide, not a break: feature `:309` pins "a work-item may accept only requirements a scenario already names" (file problem), while r106 `:742` pins "accepts counts whether or not a scenario names it" (no `v_w4`). Both hold if the file problem stays (exit 1) and only `v_w4` changes. The plan decides; both readings are in the spec.

## 5. A step the work-item skips

The existing way: an accepted requirement is looked up in the scenarios (`has_sc`, `model_work.py:188`) before anything else. Effects only that step produces:
- the `accepts` fact (`model_work.py:189-190`): only for named requirements. Probe D `run`: fact present; probe A `run`: absent.
- the file problem (`model_work.py:195`), a refusal: exit 1 for a drafted work-item. Probe A and F `run`.
- the exemption (`model_work.py:192-193`): suppresses only the file problem (guarantees, probe E `run`; green and retired `read`). It does not write the fact, so `v_w4` still prints in E.
- Withdrawn skips the problem (probe G `run`).

## 6. Defects

### D1: an accepting work-item with no check is `v_w4`
Reproduction: probe A (`repos/a`) and probe E (`repos/e`). `model check` prints `v_w4 a work-item has no acceptance and no check` for w1 whose `accepts` field is `[thing#r2]`. The file problem beside it says the scenario is missing; the `v_w4` label says there is no acceptance. Expected per r106: no `v_w4`.

### D2: an accepted requirement no capability has is `v_w4` too
Reproduction: probe F (`repos/f`), `accepts: [thing#r9]`, no check: `v_w4` printed and file problem `accepts capability/ex.com/prod/ctx/thing#r9, which no scenario names yet`. Same cause as D1; the file problem's wording does not fit a requirement no capability has.

## 7. The file set

Edited:
- `scripts/model_work.py` (214 lines, room 86): `read_part` writes `accepts` for each accepted requirement, named or not; keeps line 195 for r27. Found by refs and the grep above.
- `scripts/model.lp` (303 lines; not a tracked Python file, so the 300 limit does not apply; 3 lines over 300 as a count): `has_accepts`/`v_w4` if the `accepts` relation changes. Found by grep.
- `tests/scenarios/design_model_check_one_each.py` (47 lines, room 253): add the `FIELDS` key `accepts thing#r2 and no check`. Found by the KeyError (run).

Keep passing, not edited: `tests/scenarios/test_design_model_check.py` (the outline rows, run), `tests/scripts/test_model_withdrawn.py` (run), `tests/scenarios/design_model_check_problems.py` (steps 107-120, read), `features/design-model-check.feature:309-330` (read).

On the change's path, not edited (line counts by `wc -l`): `scripts/model` 137; `scripts/model_facts.py` 275 (room 25); `scripts/model_check.py` 139 (room 161, prints rows); `scripts/model_parse.py` 271 (room 29, `expand`, `as_list`). `tools size --limit 300` printed no file over the limit.

## Git state

`git status --porcelain` shows nothing. `.shop/scratch/` is ignored (`git status --porcelain --ignored .shop`). Probe repos are under `.shop/scratch/w117-1-research/`; the run directory is `.shop/scratch/1-research/`.
