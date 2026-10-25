# Branch review 7 of i32: Reviewers' answers and questions as the loop reads them

**Verdict: DONE_WITH_CONCERNS.**
- No finding of an i32 work-item is triaged fix now, and none is Critical.
- Since branch review 6 (`05777a48`), no code, agent or test file has changed. The one change outside `.shop/` is i33's formulate round `50addf01`, which adds the supervision @r120 scenario.
- The status is DONE_WITH_CONCERNS because two checks still cannot be verified. They are the same two as in reviews 1 to 6 (see Cannot verify).

## Range and work-items

- **Range:** `d3d3839d..620ec316` (155 commits).
- **w189** (review#r31): `ee81efd0`, at `agents/bdd-branch-reviewer.md:74,76`.
- **w190** (supervision#r118, r119): `6622133a`, `31c86e3c`.
- **w191** (the fix of branch review 1): `32b5f1fa`.
- **Commits that belong to no i32 work-item:**
  - The ones carried from reviews 1 to 6. These are w185's `968344f4`, i33's rounds `af6357e1` and `f1a9ecd3`, records and queue moves.
  - New since `05777a48` (20 commits):
    - `50addf01` (`features/supervision.feature` +9, the @r120 scenario) and its merge `44616413`. This is i33's formulate round 9, not a work-item.
    - The rest touch `.shop/` only:
      - w192, w193 and w194's queue moves and answers;
      - `13e91f83`, `6e17f0de` and `59ca81e1`, hand edits to i33's work-item and proposal files under the person's delegation;
      - i34's start (`c7f6d2f7`, `c3b67a4a`);
      - branch review 6's record (`fc077bf1`).

## Suite

`Suite: 902 passed, 11 failed at 620ec31 in 34.8 s`. pytest reports 34.43 s; there were also 1 skipped and 56 subtests passed. The command was `python3 -m pytest -q -p no:cacheprovider --tb=line`.

- **Parallel:** yes, with `-n auto` from `pytest.ini`.
- **In-process:** no. The steps run `scripts/work` as a subprocess. The suite is under 60 s, so this is no finding.
- **The 11 failures:** all are i33's, from scenarios that no green work-item implements yet.
  - 10 are the same as in review 6:
    - supervision @r121 ×4;
    - @r105 outline ×2;
    - the @r75 "withdrawn" row;
    - work-queue @r32 ×2;
    - work-queue @r31.
  - 1 is new: supervision @r120. It fails with StepDefinitionNotFoundError on its Then, "the brief of the session answering … asks it to give in its result whether its answer asks for a change or accepts w1 as it is".
  - i33's w194 (`researched`) accepts r120. None of the 11 is an i32 scenario.

## Checks

- **w189:**
  - `pytest tests/scripts/test_agents.py tests/scripts/test_supervise_answers.py`: 9 passed, 18 subtests passed.
  - The plan's `measure` check on r31: cannot be verified (see Cannot verify).
- **w190:** `pytest -n 0 --work-item w190`: 146 passed, 1 skipped, 56 subtests passed.
  - The reviewer's-question scenarios (`--whole-suite -n 0 -m "" -k reviewer`): 11 passed, 1 failed. The failure is i33's @r120. The @r118 and @r119 scenarios pass.
- **w191:**
  - `pytest -n 0 --work-item w191`: 146 passed, 1 skipped, 56 subtests passed.
  - `test_supervise_answers.py`: passed (within the 9 above).
- **`tools check --base d3d3839d`:**
  - **ruff:** 17 errors, the same 17 as in review 6.
    - 12 are in committed run records under `.shop/work/i32/runs/` and `.shop/work/i33/runs/` (finding 3).
    - 2 are RUF100 at `tests/scripts/test_supervise_answers.py:9,10` (finding 2).
    - 3 are I001 at `tests/scenarios/test_supervision.py:14` and FURB167 at `tests/scripts/stub_claude.py:189,190` (finding 9).
  - **vulture:** clean.
  - **import-linter:** `missing`: "the project states no import contracts". I checked the module map myself (see Shape).
- **`tools size --limit 300`:** prints nothing and exits 0.
- **`features deprecated`:** 8 deprecated scenarios, the same 8 as in review 6:
  - migration-tools @r15;
  - supervision @r75 (its replacement is @r75), @r75 PARTIAL (now listed with its replacement @r121), @r102 and @r105;
  - work-queue @r1, @r9 and @r23.
  - None is an i32 work-item's. The replacements of i33's four belong to w192 and w194, neither of which is `green`.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real:** `work run` has no dry-run mode of any operation, so no agreement test applies.

## Removed and weakened tests

None in i32's work-items.

- **Searched:**
  - the removed lines of `git diff d3d3839d HEAD -- tests features`;
  - the added lines of `tests/` for `skip`, `xfail` and `parametrize`. There were none.
- **What the removed lines are:**
  - `re.M` → `re.MULTILINE` at `tests/scenarios/supervision_delegation_steps.py:171` (w191) is the same flag.
  - The others are:
    - the `@r75`, `@r105` and `@r23` tag lines that i33's formulate rewrote to `@deprecated` with a "Deprecated for:" line;
    - w185's (i31) retirement of the deprecated @r83 scenario, with its binding. Review 5 verified this.
- **Since review 6:** `features/` gains only the @r120 scenario, and `tests/` is unchanged.

## Allowances

- **i32:** none is claimed. The w189 3-implement, w190 3- and 5-implement and w191 3-implement reports give none, and the commits agree.

## Cannot verify

- **review#r31 on a real batch.**
  - w189's plan names `measure` of a later initiative as the check. The latest measurement in `.shop/records/measurements/` is still `2026-10-25-i30.md`.
  - I checked the agent text instead (`agents/bdd-branch-reviewer.md:74,76`), and this review follows it: `questions` is empty because nothing is fix now.
- **That a real `delegation-answerer` session gives `verdict`.**
  - `grep -c verdict agents/delegation-answerer.md` gives 0. Only the brief asks for it (`scripts/supervise_answers.py:17-18`).
  - Without it, the question is left for the person, which is safe.
  - This is now i33's r120. Its scenario was formulated in `50addf01` and has no step yet; w194 accepts it.

## Findings

### 1. Minor, no work-item (`3e1cb8bb`), observation (carried): i31's status edited by hand
- **Where:** `.shop/work/i31/initiative.md:4`.
- **Reproduction:** `git show 3e1cb8bb`.

### 2. Minor, w191, observation (carried): RUF100 in the new test
- **Where:** `tests/scripts/test_supervise_answers.py:9,10`, an unused `noqa: E402`.
- **Fix:** drop `E402`.
- **Reproduction:** `tools check --base d3d3839d`.

### 3. Minor, no work-item (proposal rounds of i32 and i33), observation (carried): `tools check` lints committed run records
- **Where:** 12 ruff errors under `.shop/work/*/runs/`.
- **Why it matters:** each round's helper script adds noise to every branch review's ruff heading.
- **Fix:** exclude `.shop/` from `tools check`.
- **Reproduction:** `tools check --base d3d3839d`.

### 4. Minor, w191, observation (carried): an answered-but-unmoved reviewer's item waits with no question shown
- **Where:** `scripts/supervise_answers.py:85-88`.
- **What happens:** rc 3 and `w1 awaiting-answer`, with no open question named.
- **Reproduction:** review 2's probe. The code is unchanged since.

### 5. Minor, w190, observation (carried): with several reviewer questions on one item, the last verdict wins
- **Where:** `scripts/supervise_answers.py:124`.
- **Hardening:** move the item to `ready` if any verdict is `change`.

### 6. Important, no i32 work-item, observation (carried, wider): other initiatives' work lands in i32's range
- **What:** since review 6, i33's `50addf01` adds @r120, and with it an 11th failure in the suite at HEAD. The commits of i34's start are in the range too.
- **Why it is an observation:** r95 shares the branch by design, and no line says how one initiative's branch review treats another's commits.
- **Fix:** a line for it, through integrating-a-proposal.
- **Reproduction:**
  - `git log --oneline 05777a48..HEAD -- features` lists `50addf01`;
  - the suite gives `11 failed`, all of them i33's.

### 7 and 8. w185 (i31): fixed, as verified in review 6
- `scripts/supervise_rounds.py` is unchanged since.

### 9. Minor, w185 (i31), observation (carried): ruff hits in files w185 touched
- **Where:** `tests/scenarios/test_supervision.py:14` (I001) and `tests/scripts/stub_claude.py:189,190` (FURB167).
- **Fix:** `ruff check --fix`.

### Checked, no finding
- **i32's code:** unchanged since review 5. `git diff --stat 05777a48 HEAD -- agents scripts tests` is empty, so the earlier checks of w189, w190, w191 and decision 0069 stand.
- **i33's new r120 scenario against i32's behaviour:** it asks that a reviewer's-question brief ask for the verdict. `scripts/supervise_answers.py:17-18,139` already appends that text when `Reviewer` is given, so r120 extends r118 and r119 without contradicting them. Only its step is missing, and that step is w194's.
- **Code that no line asks for in i32:** none. The `verdict` move serves r118, r119 and 0069, the no-move serves r77, and w189's text serves r31.

## Shape

- **Size, 300 lines:** met. `tools size` prints nothing.
- **Module map, i32's rows:** met, as in reviews 5 and 6:
  - `supervise_answers.py`: answers under a delegation;
  - `workqueue_answer.py:31` (`reviewer_status`);
  - `tests/scenarios/supervision_delegation_steps.py`;
  - `tests/scripts/test_supervise_answers.py`.
- **Unreached code or steps:** none. vulture is clean, and every binding names a scenario.
- **Observation (carried):** `asked_by_reviewer` is read three times for one question (`supervise_answers.py:82,106,121`). The refactor is complete when `grep -c asked_by_reviewer scripts/supervise_answers.py` gives 1.

## Coupling

- **Claude CLI / delegation-answerer:** r118 and r119 rely on a `verdict` result field that only the brief names.
  - Without it, the question is left for the person, which is safe.
  - Naming `verdict` in `agents/delegation-answerer.md` (r120, i33) makes it stable.
- **`tests/scripts/stub_claude.py`:** mirrors the CLI's result JSON, so a change in the CLI's fields would show only on a real run.
- **pytest-bdd, ruff, vulture:** used through their public CLI or API only.

## Observations

- i31's status was hand-edited: `git show 3e1cb8bb` (finding 1).
- `tools check --base d3d3839d` gives RUF100 at `test_supervise_answers.py:9,10` (finding 2).
- `tools check` gives 12 ruff errors under `.shop/work/*/runs/` (finding 3).
- An answered-but-unmoved reviewer's item waits silently, with rc 3 and `w1 awaiting-answer` (review 2's probe; finding 4).
- With several reviewer questions the last verdict wins, at `supervise_answers.py:124` (finding 5).
- Other initiatives' work is in i32's range: the suite gives `11 failed`, all i33's, @r120 among them since `50addf01` (finding 6).
- `tools check` gives I001 at `test_supervision.py:14` and FURB167 at `stub_claude.py:189,190` (finding 9).
- `grep -c verdict agents/delegation-answerer.md` gives 0 (Cannot verify; r120).
