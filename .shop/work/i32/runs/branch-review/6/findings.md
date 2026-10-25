# Branch review 6 of i32: Reviewers' answers and questions as the loop reads them

**Verdict: DONE_WITH_CONCERNS.**
- No finding of an i32 work-item is triaged fix now, and none is Critical.
- Since branch review 5 (`507d361e`), no code, agent, test or spec file of i32 has changed: no file of w189, w190 or w191. The only i32 commit is `ac116922`, the record of review 5.
- Review 5's findings 7 and 8 (w185, i31) are fixed at HEAD by `968344f4`. w185 is `green`.
- The status is DONE_WITH_CONCERNS because two checks still cannot be verified. They are the same two as in reviews 1 to 5 (see Cannot verify).

## Range and work-items

- **Range:** `d3d3839d..05777a48`.
- **w189** (review#r31): `ee81efd0`, at `agents/bdd-branch-reviewer.md:74,76`.
- **w190** (supervision#r118, r119): `6622133a`, `31c86e3c`.
- **w191** (the fix of branch review 1): `32b5f1fa`.
- **Commits that belong to no i32 work-item:**
  - The ones carried from review 5.
  - New since then (48 commits in `507d361e..HEAD`):
    - **w185 (i31):** `968344f4`, between `507d361e` (claimed) and `7e17c47b` (done). It changes `scripts/supervise_change.py` and `scripts/supervise_rounds.py`.
    - **i33's apply and formulate rounds:**
      - `af6357e1` (spec), with `b0948f6f` merging it;
      - `f1a9ecd3` (`features/supervision.feature` and `features/work-queue.feature`), with `1b9fc196` merging it.
      - These come from rounds, not from work-items, so their `features/` change is no work-item's.
    - **Records and queue moves:**
      - i31's branch review 1 (`b0f5eef6`), w192's and w193's stage moves, and the `work answer` and `work note` commits;
      - the observation `6e562ea5`, request q11 (`48ed9d9d` to `98f9c35d`), and `ac116922`.
      - w192 and w193 have committed no code yet.

## Suite

`Suite: 902 passed, 10 failed at 05777a4 in 29.7 s` (pytest reports 29.06 s; also 1 skipped and 56 subtests passed). Command: `python3 -m pytest -q -p no:cacheprovider --tb=line`.

- **Parallel:** yes. `pytest.ini` sets `-n auto`, on 32 CPUs.
- **In-process:** no. The step definitions run `scripts/work` as a subprocess. The suite is under 60 s, so this is no finding.
- **The 10 failures** are all scenarios that i33's formulate round added in `f1a9ecd3`, which no green work-item implements yet:
  - supervision @r121, ×4 (DONE, PARTIAL, BLOCKED, NEEDS_CONTEXT): StepDefinitionNotFound.
  - supervision @r105, the new outline ×2: StepDefinitionNotFound.
  - supervision @r75, the new outline's "w1 is withdrawn and w2 is withdrawn" row: an AssertionError at `supervision_analysis_steps.py:65`, because a measurement is written. That is today's behaviour, against the changed r75.
  - work-queue @r32 ×2: StepDefinitionNotFound.
  - work-queue @r31: `assert 'done' == 'started'` at `test_work_queue.py:242`.
- None of the 10 is an i32 scenario. Under `--work-item w192`, w193's run records show the work-queue ones as xfail.

## Checks

- **w189:**
  - `pytest tests/scripts/test_agents.py tests/scripts/test_supervise_answers.py`: 9 passed, 18 subtests passed.
  - The kept-branch-review scenarios, run with `--whole-suite -n 0 -m "" tests/scenarios/test_supervision.py -k kept_branch_review`: 8 passed, 5 failed.
    - The 5 failures are i33's new r121 ×4 and r75 "withdrawn" row, the same ones as in the suite.
    - The 7 that passed in review 5 still pass. The 8th to pass is i33's new r75 "green" row.
  - The plan's `measure` check: cannot be verified (see Cannot verify).
- **w190:** `-n 0 --work-item w190` gives 146 passed, 1 skipped, 56 subtests passed.
- **w191:**
  - `-n 0 --work-item w191` gives 146 passed, 1 skipped, 56 subtests passed.
  - `test_supervise_answers.py` passed, within the 9 above.
- **`tools check --base d3d3839d`:**
  - **ruff:** 17 errors.
    - 5 are in `.shop/work/i32/runs/supervision/3-apply/apply.py` (finding 3, carried).
    - 7 are new, in i33's committed run records `.shop/work/i33/runs/supervision/7-apply/apply.py` and `8-formulate/splice.py` (finding 3, now wider).
    - 2 are RUF100 at `tests/scripts/test_supervise_answers.py:9,10` (finding 2, carried).
    - 3 are already-present lines in files w185 touched: I001 at `tests/scenarios/test_supervision.py:14`, and FURB167 at `tests/scripts/stub_claude.py:189,190` (finding 9, carried).
  - **vulture:** clean.
  - **import-linter:** "the project states no import contracts". I checked the module map myself (see Shape).
- **`tools size --limit 300`:** prints nothing and exits 0. No file is over the limit.
- **`features deprecated`:** 8 deprecated scenarios.
  - The 4 that were already deprecated: migration-tools @r15, supervision @r102, work-queue @r1 and @r9.
  - 4 that i33's formulate deprecated: supervision @r75 ×2 and @r105, and work-queue @r23.
  - None of them is an i32 work-item's. The replacements of i33's 4 belong to i33's work-items, none of which is `green`. So no deprecated scenario has a green replacement that should have retired it.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real:** `work run` has no dry-run mode of any operation, so no agreement test applies.

## Removed and weakened tests

None in i32's work-items.

- **Searched:** the removed lines of `git diff d3d3839d HEAD -- tests features`, for a deleted `def test_`, a removed or loosened assert, and `skip`, `xfail` or `parametrize` in the added lines.
- **`tests/`:** has no change since `507d361e`.
- **`features/`:** i33's formulate commit `f1a9ecd3` only adds scenarios and adds `@deprecated` with a "Deprecated for:" line. It removes no scenario.
- **Carried from review 5:** `re.M` → `re.MULTILINE` at `tests/scenarios/supervision_delegation_steps.py:171` is the same flag. w185's step widenings were checked in review 5, and none is a weakening.

## Allowances

- **i32:** none is claimed. The w189 3-implement, w190 3- and 5-implement and w191 3-implement reports each give none, and the commits agree.
- **w185:** its `setup` row was verified by i31's own reviews (`runs/w185/5-review` and i31 branch review 1), not by this review.

## Cannot verify

- **review#r31 on a real batch.**
  - w189's plan names `measure` of a later initiative as the check. The latest measurement in `.shop/records/measurements/` is still `2026-10-25-i30.md`.
  - I checked the agent text instead (`agents/bdd-branch-reviewer.md:74,76`), and this review follows it: `questions` is empty because nothing is fix now.
- **That a real `delegation-answerer` session gives `verdict`.**
  - `grep -c verdict agents/delegation-answerer.md` gives 0. Only the brief asks for it (`scripts/supervise_answers.py:17-18`).
  - Omitting it is safe: the question is left for the person.
  - i33 has now written this as supervision r120 (`spec/capabilities/supervision.md`, `af6357e1`). Its formulate returned r120 as a question, so it has no scenario yet.

## Findings

### 1. Minor, no work-item (`3e1cb8bb`), observation (carried): i31's status edited by hand on this branch
- **Where:** `.shop/work/i31/initiative.md:4`, changed outside `work`.
- **Reproduction:** `git show 3e1cb8bb`.

### 2. Minor, w191, observation (carried): RUF100 in the new test
- **Where:** `tests/scripts/test_supervise_answers.py:9,10`, an unused `noqa: E402`.
- **Fix:** drop `E402`.
- **Reproduction:** `tools check --base d3d3839d`.

### 3. Minor, no work-item (proposal rounds of i32 and i33), observation (carried, wider): `tools check` lints committed run records
- **Where:**
  - `.shop/work/i32/runs/supervision/3-apply/apply.py:3-13`: 5 errors;
  - `.shop/work/i33/runs/supervision/7-apply/apply.py:2-10` and `.shop/work/i33/runs/supervision/8-formulate/splice.py:1-33`: 7 errors.
- **Why it matters:** each new round's helper script adds noise to every branch review's ruff heading.
- **Fix:** exclude `.shop/` from `tools check`.
- **Reproduction:** `tools check --base d3d3839d` gives 12 errors under `.shop/`.

### 4. Minor, w191, observation (carried): an answered-but-unmoved reviewer's item waits with no question shown
- **Where:** `scripts/supervise_answers.py:85-88`.
- **What happens:** `work run` gives rc 3 and `w1 awaiting-answer`, and names no open question.
- **Reproduction:** review 2's probe. The code is unchanged since.

### 5. Minor, w190, observation (carried): with several reviewer questions on one item, the last verdict wins
- **Where:** `scripts/supervise_answers.py:124`.
- **Hardening:** move the item to `ready` if any verdict is `change`.

### 6. Important, no i32 work-item, observation (carried): other initiatives' work lands in i32's range
- **What:** this range now also holds:
  - w185's fix (`968344f4`);
  - i33's spec and feature rounds (`af6357e1`, `f1a9ecd3`).
- **Effect:** the suite at HEAD has 10 failures from i33's scenarios that are not implemented yet, and the ruff heading carries i33's run records.
- **Why it is an observation:** r95 shares the branch by design, and no line says how one initiative's branch review treats another's commits.
- **Fix:** a line for it, through integrating-a-proposal.
- **Reproduction:**
  - `git log --oneline 507d361e..HEAD -- scripts features spec` lists `968344f4`, `af6357e1`, `b0948f6f`, `f1a9ecd3` and `1b9fc196`;
  - the suite gives `10 failed`, all i33's (see Suite).

### 7. Was Important, w185 (i31): an apply round's list naming an unknown capability was dropped silently. Fixed.
- **Verified at HEAD:** `scripts/supervise_rounds.py:140-145` now calls `unknown(applied, …, runs=True)` before `rewrite_lists`. It keeps the round and raises `Refused` naming the capability (r107). I read this; I ran no probe.
- **Remaining, i31's:** an entry naming another known capability is still filtered out by `rewrite_lists` (`scripts/supervise_change.py:58-59`). i31 branch review 1 holds this as an observation.

### 8. Was Important, w185 (i31): a refused round stopped the others' rounds. Fixed.
- **Verified at HEAD:** `scripts/supervise_rounds.py:63-76`. `rounds()` catches `Refused`, adds the proposal to `left`, and lets `due(left)` go on. It raises the first fault once no round is due (r111, r115).

### 9. Minor, w185 (i31), observation (carried): ruff hits in files w185 touched
- **Where:** `tests/scenarios/test_supervision.py:14` (I001) and `tests/scripts/stub_claude.py:189,190` (FURB167). w185 did not change these lines.
- **Fix:** `ruff check --fix`.

### Checked, no finding
- **i32's code since review 5:** unchanged. `git diff --stat 507d361e HEAD -- agents scripts/supervise_answers.py scripts/workqueue_answer.py tests` is empty, so reviews 1 to 5's checks of w189, w190, w191 and decision 0069 stand.
- **i33's changed lines against i32's behaviour:** r121, r75, r105, r23, r31 and r32 do not touch r118, r119 or r31 (review), and r120 extends r118 and r119 without contradicting them.
  - Under r121, this result (DONE_WITH_CONCERNS with no question) will be taken as listing nothing to fix now, once i33 implements it.
  - Today's code still reads a non-DONE result as not done; that is i33's work-item.
- **Code that no line asks for in i32:** none. The `verdict` move serves r118, r119 and 0069, the no-move serves r77, and w189's text serves r31.

## Shape

- **Size, 300 lines:** met. `tools size` prints nothing.
- **Module map, i32's rows:** met, as in review 5:
  - `supervise_answers.py`: answers under a delegation;
  - `workqueue_answer.py:31` (`reviewer_status`), used by `supervise_answers.py:86`;
  - `tests/scenarios/supervision_delegation_steps.py`;
  - `tests/scripts/test_supervise_answers.py`.
- **The `supervise_change.py` row:** it still says "an integrate round's change list", but since `968344f4` the module also checks an apply round's list. This is w185's, and i31 branch review 1 named it.
- **Unreached code or steps:** none. vulture is clean, and every binding names a scenario.
- **Observation (carried):** `asked_by_reviewer` is read three times for one question (`supervise_answers.py:82,106,121`). The refactor is complete when `grep -c asked_by_reviewer scripts/supervise_answers.py` gives 1.

## Coupling

- **Claude CLI / delegation-answerer:** r118 and r119 rely on a `verdict` result field that only the brief names.
  - Without it, the question goes to the person, which is safe.
  - r120 (i33) now asks the session for it. Naming `verdict` in `agents/delegation-answerer.md` makes it stable.
- **`tests/scripts/stub_claude.py`:** mirrors the CLI's result JSON, so a change in the CLI's fields would show only on a real run.
- **pytest-bdd, ruff, vulture:** used through their public CLI or API only.

## Observations

- i31's status was hand-edited on this branch: `git show 3e1cb8bb` (finding 1).
- `tools check --base d3d3839d` gives RUF100 at `test_supervise_answers.py:9,10` (finding 2).
- `tools check` gives 12 ruff errors in committed run records under `.shop/work/i32/runs/` and `.shop/work/i33/runs/` (finding 3).
- An answered-but-unmoved reviewer's item waits silently, with rc 3 and `w1 awaiting-answer` (review 2's probe; finding 4).
- With several reviewer questions the last verdict wins, at `supervise_answers.py:124` (finding 5).
- Other initiatives' work is in i32's range: `git log --oneline 507d361e..HEAD -- scripts features spec` lists 5 commits, and the suite has 10 failures, all i33's (finding 6).
- `tools check` gives I001 at `test_supervision.py:14` and FURB167 at `stub_claude.py:189,190` (finding 9).
- `grep -c verdict agents/delegation-answerer.md` gives 0 (Cannot verify; r120).
