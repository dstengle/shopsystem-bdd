# Research: design-model-check-3 (r110, work-item ids)

Accepted: `features/design-model-check.feature`: "a work-item not named w<n>.md, or two work-items with one id, is a file problem" (Scenario Outline, 4 rows, `@r110`).
Tool coverage: `tools refs` ran. `tools tests-of` and `untested` have no map ("no map: make one with tools map"); `tools map` runs the whole suite, so not made. Every test list below is `by search`.

## 1. Why each row is red today

Command, per row: `python3 -m pytest -q "tests/scenarios/test_design_model_check.py::test_a_workitem_not_named_wnmd_or_two_workitems_with_one_id_is_a_file_problem[<row>]"` (run, all four).
All four fail at the Given, before `model check` runs:
`AssertionError: <case>` at `tests/scenarios/design_model_check_problems.py:130`, in `malformed_record` (line 115). Its `if`/`elif` chain has no branch for the four case strings; its `else` asserts the one case "a decision and an observation have the same id".
- Missing in steps: branches for the four cases (work-items named `fix-login.md` and `w3.md`, in `i1` and `i2`).
- Missing in helpers: `tests/scenarios/conftest.py:118` `World.work_item` writes only `.shop/work/i1/<ident>.md` (no initiative argument, file name = id). Rows need a file name other than the id and a second initiative.
- Missing in code, `scripts/model_work.py:read_part` (lines 117-191): reads the id from frontmatter only; never compares the file stem with `w<n>`.
- Missing in code, `scripts/model_facts.py:node` (lines 45-49): reports only a kind clash; two work-items with one id register silently. No work-item id registry exists.
- Then steps: the outline's "Then it does not print a file problem" has no step. `design_model_check_problems.py:164` matches only "it does not print a file problem naming {named}". Read, not run. "it prints a file problem" (`design_model_check_problems.py:178`) asserts exactly one problem, so the printed case must give one entry.

## 2. What the system answers today

Probe: `python3 -m pytest -q -s -n0 .shop/scratch/design-model-check-3-2-research/probe_ids.py` (run; repositories built under the scratch dir; `scripts/model --root <repo> check [--json]`).
Every repo: one capability `thing` with `@r1`, one initiative `i1` (`source: []`), work-items with `under: thing`, `check: true`. Baseline shows "2 violations, 1 warning" in every case; not examined (likely from initiative kind, read).

| case (Given) | `check --json` file problems | exit | note |
|---|---|---|---|
| row 1: `i1/fix-login.md`, id `w3` | none | 1 | 2 violations only; should print a file problem |
| row 2: `i1/w3.md`, id `w3` | none | 1 | expected, correct |
| row 3: `i1/w3.md` and `i2/w3.md`, both id `w3` | none | 1 | `model facts` prints `node("work-item/ex.com/prod/ctx/w3", "work-item").` twice |
| row 4: `i1/w3.md` id `w3`, `i2/w4.md` id `w4` | none | 1 | expected, correct |
| nearest: `i1/fix-a.md` and `i1/fix-b.md`, both id `w3` | none | 1 | same initiative, duplicate silent |
| nearest: `i1/w4.md`, id `w3` | none | 1 | name and id disagree, silent |
| nearest: `i1/w3.md` id `w3`, `i2/w3.md` id `w3` withdrawn | none | 1 | duplicate with a withdrawn twin, silent |
| nearest: `i1/w3.md`, id bare `w3` | `id 'w3' is not work-item/ex.com/prod/ctx/<name>` | 1 | refused, by the id rule (`model_work`/`model_facts.check_id`) |
| nearest: `i1/w3.md`, no id | `needs an id and a kind among ...` | 1 | refused, existing rule |

Not run: the scenario's Then steps on the Outline rows (blocked at Given).

## 3. Old assumptions

The requirement makes a work-item's name its file stem as `w<n>` and its id unique. Places that assume otherwise or take the stem as the name:

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/model_work.py:read_part` | id from frontmatter; file stem never read | must compare stem with the id's `w<n>` (r110) | `by search`: `tests/scripts/test_model*.py` and `tests/scenarios/design_model_check_*` use `w1` names | `refs` (none: class only), search |
| `scripts/model_facts.py:node` | records ids; a second same-kind id overwrites silently | needs a cross-file id check (r110) | `none` for a duplicate work-item id (no test builds one) | search |
| `scripts/work_items.py:50,65` (`--work-item`, `work_items` plugin) | takes `path.stem` as the work-item name, glob `*/<name>.md` | consistent with r110: stem = id; no change needed unless names are not `w<n>` | `by search`: `tests/scripts/test_work_items.py` (2 `kind: work-item` files) | search |
| `scripts/workqueue.py:86` (`work` queue listing) | yields `path.stem` as the name | same as above; old names (e.g. `fix-login`) keep working for the queue but fail r110 | `by search`: `tests/scenarios/test_work_queue.py` | search |
| `tests/scenarios/design_model_check_problems.py:83`, `design_model_check_reading.py:51,81` | write `.shop/work/i1/p1.md` parts (kind capability-proposal, not work-item) | a check on every `.md` under `.shop/work/` would wrongly refuse parts; r110 is for work-items only | `by search` (read of `kind:`) | search |

Not an old assumption of this work-item: `scripts/migrate*` (0.24.0 "work-items named by ids") is another capability.

## 4. Tests the requirement makes impossible to keep

`by search` (no map). Searched `kind: work-item` in `tests/` (8 hits, 6 files) and every `model check` invocation in `tests/`.
- `tests/scenarios/test_work_queue.py`, `work_queue_*_steps.py`, `supervision_*`: write work-items named by name, not by `w<n>`; none runs `model check`. Keep.
- `tests/scripts/test_model*.py`, `tests/scenarios/design_model_check_*.py`: `World.work_item`/`work_item` default `w1` (file `w1.md`); pass. Keep.
- `tests/scenarios/migration_spec_steps.py:178`: `model check` on an old-layout repo (`work/`, not `.shop/work/`); not affected.
- Found impossible to keep: none. Verified by search; `tests-of` could not confirm.

## 5. A step the work-item skips

`read`: the existing way reads a work-item from frontmatter alone (`read_part`); the new check reads the path, which no step does today. No transaction, no signature involved. Refusals and effects only that step would produce: none; the check adds one file problem per bad work-item.

## 6. Defects

Reproduction for each: `python3 -m pytest -q -s -n0 .shop/scratch/design-model-check-3-2-research/probe_ids.py` (run), rows listed in part 2.
- D1: two work-items with one id across initiatives: `check` prints no file problem, exit 1 only for other rows; `facts` prints the node twice. (row 3)
- D2: work-item file `fix-login.md` with id `w3`: accepted, no file problem. (row 1)
- D3: work-item file `w4.md` with id `w3`: accepted, no file problem. (nearest)
- D4: same-initiative duplicate, `fix-a.md` and `fix-b.md` with id `w3`: accepted, no problem. (nearest)
Not judged: what the plan does about these.

## 7. The file set

Production:
- `scripts/model_work.py` (200 lines; room 100): `read_part` compares the stem with `w<n>` for work-items and registers ids across initiatives. Search: `read_part` above; `read_work` loop.
- `scripts/model_facts.py` (265 lines; room 35): `node`/a duplicate-id check, if the registry lives here. Search: `node`, lines 45-49.

Tests:
- `tests/scenarios/design_model_check_problems.py` (278 lines; room 22): `malformed_record` gets the four cases, with initiative `i2`. Search: lines 114-133.
- `tests/scenarios/conftest.py` (176 lines; room 124): `World.work_item` takes an initiative and a file name, or the step writes files directly. Search: line 118.
- A `Then` step for "it does not print a file problem" (bare form): `design_model_check_then.py` (215 lines; room 85) or `design_model_check_problems.py`. Search: line 164.

On the change's path, not edited:
- `scripts/model` (137 lines; room 163): entry point; no change. `wc -l`.
- `scripts/model_parse.py` (271 lines; room 29): `frontmatter`, `as_list`; no change.
- `scripts/model_check.py` (139 lines; room 161): prints problems generically; no change.
- `scripts/model.lp` (304 lines; not Python, outside the 300-line rule): no change; r110 is a file problem, not a rule.

Size: `tools size --limit 300` printed nothing (no tracked Python file over 300 lines).

## Scratch

`.shop/scratch/` is git-ignored (`git status --porcelain --ignored`).
