# w195 research: supervision r122, whole-suite expected red for proposals

Tools: `tools tests-of`, `untested` report "no map" (no coverage map); all test lists below are **by search**. `tools refs` worked (`acceptors` 1 production caller, `expect_red` 1 production caller, 0 tests).

Accepted scenario: `features/supervision.feature:813` Scenario Outline "when the whole suite is run <run>, a failing scenario whose requirement a capability-proposal that is <status> adds or changes is counted as <counted>", 10 rows. Requirement r122: a whole-suite check counts as expected a failing scenario whose requirement a capability-proposal that is neither `formulated` nor `withdrawn` adds or changes.

## 1. Why each scenario is red today

Command (`run`): `python3 -m pytest -q --tb=line -k "whole_suite_is_run" tests/scenarios/test_supervision.py` → 9 failed, 1 passed.

Failing rows, by first error (`run`):
- Undefined Given at line 817, `i1's capability-proposal p1 is <status>, its adds|changes naming thing#r2` (`approved`, `withdrawn`, `awaiting-answer`, `merged`): 6 rows: worktree/approved-changes-r2, worktree/withdrawn-changes-r2, merge/awaiting-answer-adds-r2, merge/merged-changes-r2, merge/withdrawn-adds-r2, merge/approved-changes-r3.
- Undefined Then at line 820, `the whole suite `work run` ran in the implementer's worktree before the implementer started counted "it waits" as <counted>`: 3 rows: worktree/drafted-adds-r2 (expected), worktree/formulated-adds-r2 (not expected), worktree/drafted-adds-r3 (not expected).
- Passed: merge/formulated-changes-r2 (not expected). It passes for the wrong reason: no work-item accepts `thing#r2` in that run, so today's rule counts every failure as not expected.

Missing in the step definitions:
- `tests/scenarios/supervision_proposal_steps.py`: Givens exist for `formulated` (line 21) and `drafted` with adds only (line 115). None for `approved`, `withdrawn`, `awaiting-answer`, `merged`, nor for a `changes` line.
- `tests/scenarios/supervision_tests_steps.py:134-142` `counted_as`: reads only the `stage == "merge"` suite record. No Then for the implementer's-worktree run (stage `implement`, written at `scripts/supervise_merge.py:97`).

Missing in the code (read, then confirmed by probe in section 2):
- `scripts/work_items.py:58-68` `acceptors()` reads only `kind: work-item` files, their `accepts:` and `status:`. Capability-proposals (`adds:`, `changes:`) are not read.
- `scripts/work_items.py:79-91` `expect_red()` marks xfail only for work-item acceptors whose status is not `green` or `withdrawn`. No proposal branch.

## 2. What the system answers today

Probe 1 (`run`): `python3 -m pytest -q -s -n 0 .shop/scratch/w195-1-research/probe_whole.py`. A consumer repo: w1 `ready` accepting `thing#r1`, the scenario "it waits" tagged `@r2` fails, a proposal p1 in `.shop/work/i1/`, command `python3 -m pytest -q -rfEx -p work_items --work-item w1 --whole-suite` with `PYTHONPATH` = this worktree's `scripts/`. Result (every case):

| case | today | r122 says |
|---|---|---|
| drafted, adds thing#r2 | FAILED (not expected) | expected |
| approved, changes thing#r2 | FAILED | expected |
| awaiting-answer, adds thing#r2 | FAILED | expected |
| merged, changes thing#r2 | FAILED | expected |
| formulated, adds thing#r2 | FAILED | not expected |
| withdrawn, changes thing#r2 | FAILED | not expected |
| drafted, adds thing#r3 | FAILED | not expected |
| drafted, adds other#r2 (other capability) | FAILED | not expected |
| drafted, adds and changes empty | FAILED | not expected |
| no proposal at all | FAILED | not expected |

The first run of this probe had a feature with no `Then` for "it waits", so every case passed. It was fixed and rerun; the table is the rerun.

Probe 2 (`run`): `python3 -m pytest -q -s -n 0 .shop/scratch/w195-1-research/probe_skip.py`:
- `--work-item w9` (no such work-item), without `--whole-suite`: exit 3, last line `mainloop: caught unexpected SystemExit!` (the refusal is raised as SystemExit).
- `--work-item w9 --whole-suite`: exit 1, "1 failed, 1 xpassed". `it answers` (r1, of ready w1) is XPASS: w1 is "another work-item", so its requirement is expected.
- two proposals on `thing#r2`, p1 formulated adds, p2 drafted changes: exit 1, "it waits" FAILED. r122 says p2 makes it expected.

Read: `scripts/work_items.py:98-100` returns before `accepted()` for `--whole-suite`, so the name check, the guarantees rules and `pytest_sessionfinish` (line 123-131, returns early) are not run on the whole-suite path.

## 3. Old assumptions

Table: the rule "a failing scenario is expected only if a non-green, non-withdrawn work-item accepts its requirement".

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/work_items.py:acceptors | builds requirement → (work-item, status) from `kind: work-item` files only | must also read `kind: capability-proposal` `adds:`/`changes:` with status | by search: work run scenarios that reach a suite run (most of test_supervision.py); no map | refs, read |
| scripts/work_items.py:expect_red | xfail if an other work-item, status not green/withdrawn, accepts a tag | a second source: proposal not formulated/withdrawn; no exclusion of `name` for proposals | by search: supervision.feature:793 and :813 rows | refs, read |
| scripts/work_items.py:13-15 (docstring) | says "a work-item ... neither green nor withdrawn ... expected" | text must name proposals | none (text) | read |
| scripts/supervise_merge.py:17-19 (comment), 21 | names r43 only | text; TESTS dict unchanged | none (comment) | read |
| scripts/supervise_merge.py:Merge.suite_record:49-53 | takes expected names from XFAIL lines | no change: a proposal's xfail shows in `expected:` | by search: supervision_tests_steps counted_as | read |
| scripts/supervise_merge.py:Merge.claimed:96 | implement-stage run in the worktree from the claim-time head (`supervise_worker.py:143-152`) | the first r122 row set: proposal state at claim time | by search: r122 implementer's-worktree rows (no step yet) | read |
| scripts/supervise_merge.py:Merge.merge:126 | merge-stage run after rebase on the branch | the second r122 row set: proposal state at merge | by search: supervision.feature:793, :813 merge rows | read, run (probe 1) |
| tests/scenarios/supervision_tests_steps.py:counted_as:134 | reads stage `merge` only | needs stage `implement` too | by search: r43 and r122 outlines | read |
| model_work.py:11,16 (`SETTLED = {merged, formulated, withdrawn}`) | `merged` is a proposal status, settled for retired ids | r122 counts `merged` as not formulated/withdrawn, so expected: two readings, see Questions | by search: design-model-check features | read |
| supervise_rounds.py:19 (`AFTER`) | the work run's chain: drafted → awaiting-answer → approved → formulated | `merged` is never written by work run (grep over scripts/supervise*.py: none); the r122 `merged` row is a status the lifecycle does not produce | none in work run | read |
| agents/bdd-implementer.md:10 | "merges it only if they pass" | no change; the Suite record names expected | none (text) | read |
| README.md:74-79 | expected red for a work-item only | wording | none (text) | read |

## 4. Tests the requirements make impossible to keep

None found. By search: no test asserts a failing scenario is not expected while a non-formulated, non-withdrawn proposal names its requirement, except the r122 rows themselves. Checked:
- supervision.feature:793-810 (r43 outline, before merge): no proposal in its Givens, still passes.
- supervision.feature:104 (r43 merged), :484, :494, :504 (r56/r64/r65): no proposal, still pass.
- supervision.feature:536-545 (r26), :655-658 (r33): suite-fail with no proposal, still pass.
- tests/scripts/test_work_items.py (134 lines): none passes `--whole-suite` (search); all its cases unaffected.
- The `formulated` not-expected rows pass today and must still pass: formulated is excluded in r122.

## 5. A step the work-item skips

`--whole-suite` skips `accepted()` (read: `work_items.py:98-100`, `pytest_sessionfinish` early return at :128). Effects only the scenario path produces (run, probe 2 and test_work_items.py): the refusal of an unknown work-item (exit 3), the refusal of a run whose scenarios no work-item accepts (r56, test_work_items.py:67-69), deselection for a guarantees-only work-item (r64), and exit 0 for a guarantees-only run left empty (r65). The whole-suite path produces none of these; the r122 check adds no step to them. Consequence (run, probe 2): an unknown name still runs the whole suite.

Second, read: the implement-stage run uses the claim-time head, the merge-stage run the rebased head (supervise_merge.py:96, :121, :126). This is the difference the two row sets test, not a missing step.

## 6. Defects

D1 (run): `--work-item <unknown>` on the scenario path is refused with exit 3 and `mainloop: caught unexpected SystemExit!`. Reproduction: `python3 -m pytest -q -s -n 0 .shop/scratch/w195-1-research/probe_skip.py` (line `UNKNOWN w9, scenario path`). Not judged.

D2 (run, a reading of r43 and r122): `--whole-suite --work-item <unknown>` runs and expects w1's scenarios (xpass) instead of refusing. Reproduction: probe_skip.py line `UNKNOWN w9, whole-suite`. Whether this is a defect depends on the spec's reading of an unknown name. Not judged.

## 7. The file set

Must change:
- `scripts/work_items.py`: `acceptors` and `expect_red` read `kind: capability-proposal` `adds:`/`changes:` with status not formulated/withdrawn; docstring. 131 lines, room 169. Found by refs and read.
- `tests/scenarios/supervision_proposal_steps.py`: one Given `i1's capability-proposal p1 is <status>, its adds|changes naming <id>` for approved, withdrawn, awaiting-answer, merged. 153 lines, room 147. Found by run (undefined step, line 817).
- `tests/scenarios/supervision_tests_steps.py`: a Then for the implementer's-worktree run (stage `implement`), shared with `counted_as`. 208 lines, room 92. Found by run (undefined step, line 820).

Optional (text or unit cases):
- `scripts/supervise_merge.py`: comment lines 17-19 name r122. 135 lines, room 165.
- `tests/scripts/test_work_items.py`: unit cases for proposal statuses under `--whole-suite` (none today). 134 lines, room 166.
- `README.md:74-79`: wording. Not a Python file.
- `tests/scenarios/test_supervision.py` (261 lines, room 39): only if the new Givens go in a new module (imports at lines 25-42).

On the change's path, not edited:
- `scripts/supervise.py`: 271 lines, room 29 (`Run` mixing in `Merge`).
- `scripts/supervise_worker.py`: 251 lines, room 49 (`worktree()` at 143-157).
- `tests/scenarios/supervision_world.py`: 173 lines, room 127 (helpers the steps use).
- `tests/scenarios/conftest.py`: 176 lines, room 124 (`full`, `cap`).

Size: `tools size --limit 300` (run) printed nothing; no tracked Python file is over 300.

## Questions

1. `merged`: r122 counts a `merged` proposal's adds or changes as expected (the outline row). `model_work.py` treats `merged` as settled, and work run never writes it. Reading A: keep the r122 wording and the outline row. Reading B: drop `merged` from the r122 set.
2. D2: should `--whole-suite` with an unknown work-item refuse as the scenario path does? Reading A: yes, as r56 does for the scenario path. Reading B: no, the whole-suite check does not need the work-item.
3. Scope: r122 names no initiative, so a proposal in any `.shop/work/<initiative>/` counts. Reading A: any initiative (as r43 does for work-items). Reading B: the initiative of the work-item only.

Git: `git status --porcelain` is empty before and after; `.shop/scratch/` is ignored by the repository, so the scratch directory is not listed.
