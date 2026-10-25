# Branch review 8 of i32: Reviewers' answers and questions as the loop reads them

**Verdict: DONE_WITH_CONCERNS.**
- No finding of an i32 work-item is fix now, and none is Critical.
- Since branch review 7 (`620ec316`), none of i32's code, agent or test files has changed. The changes outside `.shop/` are i33's w192 (`64c62951`) and i31's w193 (`6b06211b`).
- The status is DONE_WITH_CONCERNS because two checks still cannot be verified. They are the same two as in reviews 1 to 7 (see Cannot verify).

## Range and work-items

- **Range:** `d3d3839d..7b81607b` (172 commits).
- **w189** (review#r31): `ee81efd0`, at `agents/bdd-branch-reviewer.md:74,76`.
- **w190** (supervision#r118, r119): `6622133a`, `31c86e3c`.
- **w191** (the fix of branch review 1): `32b5f1fa`.
- **Commits that belong to no i32 work-item:**
  - Carried from reviews 1 to 7: w185's `968344f4`, i33's rounds `af6357e1`, `f1a9ecd3` and `50addf01`, plus records and queue moves.
  - New since `620ec316` (17 commits):
    - `64c62951`: i33's w192 (work-queue r31, r32), in `scripts/workqueue.py`, `scripts/workqueue_done.py` and `tests/scenarios/work_queue_add_steps.py`.
    - `6b06211b`: i31's w193 (r114), in `agents/initiative-round.md`, `scripts/supervise_brief.py` and `tests/scenarios/supervision_formulate_steps.py`.
    - The rest touch `.shop/` only:
      - queue moves for w192, w193 and w194;
      - i34's start, its integrate round merge `c3ece9ea` and its notes;
      - branch review 7 of i32 (`0b6aba9f`) and branch review 2 of i31 (`2d5bb19a`);
      - i31's measurement and its move to done (`7088d12b`, `c3ae56d8`).

## Suite

`Suite: 905 passed, 8 failed at 7b81607b in 23.08 s`. The time is pytest's own figure. There were also 1 skipped and 56 subtests passed. The command was `python3 -m pytest -q -p no:cacheprovider --tb=line`.

- **Parallel:** yes, with `-n auto` from `pytest.ini`.
- **In-process:** no. The steps run `scripts/work` as a subprocess. The suite takes under 60 s, so this is no finding.
- **The 8 failures:** all belong to i33's w194 (`researched`, which accepts supervision r120, r121, r75 and r105). None is an i32 scenario.
  - @r121 ×4 (NEEDS_CONTEXT, DONE, PARTIAL, BLOCKED): StepDefinitionNotFound.
  - @r75, the row "w1 withdrawn and w2 withdrawn".
  - @r105 ×2.
  - @r120: StepDefinitionNotFound.
- **Since review 7:** there are 3 fewer failures (11 → 8). w192 made work-queue @r31 and @r32 pass.

## Checks

- **w189:** `pytest tests/scripts/test_agents.py tests/scripts/test_supervise_answers.py` gives 9 passed and 18 subtests passed. The plan's `measure` check on r31 cannot be verified (see Cannot verify).
- **w190:** `pytest -n 0 --work-item w190` gives 146 passed, 1 skipped and 56 subtests passed.
- **w191:** `pytest -n 0 --work-item w191` gives 146 passed, 1 skipped and 56 subtests passed. `test_supervise_answers.py` passes (it is within w189's 9).
- **`tools check --base d3d3839d`:**
  - **ruff:** 18 errors.
    - 12 are in committed run records under `.shop/work/i32/runs/` and `.shop/work/i33/runs/` (finding 3).
    - 2 are RUF100 at `tests/scripts/test_supervise_answers.py:9,10` (finding 2).
    - 3 are I001 at `tests/scenarios/test_supervision.py:14` and FURB167 at `tests/scripts/stub_claude.py:189,190` (finding 9).
    - 1 is new: I001 at `scripts/workqueue.py:248`. The line was already there, at :244, before w192. It now shows because w192 touched the file (finding 10).
  - **vulture:** clean.
  - **import-linter:** `missing`: "the project states no import contracts". I checked the module map myself (see Shape).
- **`tools size --limit 300`:** prints nothing.
- **`features deprecated`:** 8 deprecated scenarios, the same 8 as in review 7.
  - work-queue @r23: its replacement's work-item w192 is now `green`, but the old scenario is still there (finding 11).
  - supervision @r75, @r75-PARTIAL (now listed under @r121) and @r105: their work-item w194 is not green.
  - migration-tools @r15, supervision @r102, work-queue @r1 and @r9: carried from earlier reviews, not i32's.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real:** `work run` has no dry-run mode of any operation, so no agreement test applies.

## Removed and weakened tests

None in i32's work-items.

- **Searched:**
  - the removed lines of `git diff d3d3839d HEAD -- tests features`, as in reviews 1 to 7;
  - since review 7: the removed lines of `git diff 620ec316 HEAD -- tests features`, plus the added lines for `skip`, `xfail` and `parametrize`.
- **What I found since review 7:** one removed line, `from .supervision_world import log_lines`. It was replaced by an import that adds `starts` (w193). Nothing else was removed, skipped or loosened. w193 adds an assertion to `lists_written`, and w192 adds a new step.

## Allowances

- **i32:** none is claimed. The reports of w189 3-implement, w190 3- and 5-implement and w191 3-implement give none, and the commits agree.

## Cannot verify

- **review#r31 on a real batch.**
  - w189's plan names `measure` of a later initiative as the check.
  - i31's measurement (`7088d12b`) is now in the range, but it measures i31, not this reviewer's questions.
  - I checked the agent text instead (`agents/bdd-branch-reviewer.md:74,76`, unchanged), and this review follows it: `questions` is empty because nothing is fix now.
- **That a real `delegation-answerer` session gives `verdict`.**
  - `agents/delegation-answerer.md` is unchanged, so it still does not name `verdict`. Only the brief asks for it (`scripts/supervise_answers.py:17-18`).
  - Without it, the question is left for the person, which is safe.
  - This is i33's r120, whose scenario still has no step (w194).

## Findings

### 1. Minor, no work-item (`3e1cb8bb`), observation (carried): i31's status was edited by hand
- **Reproduction:** `git show 3e1cb8bb`.

### 2. Minor, w191, observation (carried): RUF100 in the new test
- **Where:** `tests/scripts/test_supervise_answers.py:9,10`.
- **Fix:** drop `E402` from the `noqa`.

### 3. Minor, no work-item, observation (carried): `tools check` lints committed run records
- **Where:** 12 ruff errors under `.shop/work/*/runs/`.
- **Fix:** exclude `.shop/` from `tools check`.

### 4. Minor, w191, observation (carried): an answered but unmoved reviewer's item waits with no question shown
- **Where:** `scripts/supervise_answers.py:85-88`, unchanged.
- **Reproduction:** review 2's probe.

### 5. Minor, w190, observation (carried): with several reviewer questions on one item, the last verdict wins
- **Where:** `scripts/supervise_answers.py:124`.

### 6. Important, no i32 work-item, observation (carried): other initiatives' work lands in i32's range
- **What:** since review 7, i33's w192 code and i31's w193 code are in the range, as are i34's start and i31's done.
- **Why it matters:** each of those commits starts i32's branch review again, which is how this is review 8.
- **Fix:** a line on how one initiative's branch review treats another's commits, through integrating-a-proposal.
- **Reproduction:** `git log --oneline 620ec316..HEAD -- scripts agents tests` lists `64c62951` and `6b06211b`.

### 9. Minor, w185 (i31), observation (carried): ruff hits in files w185 touched
- **Where:** `tests/scenarios/test_supervision.py:14` and `tests/scripts/stub_claude.py:189,190`.

### 10. Minor, w192 (i33), observation (new): a ruff hit that was already there, in a file w192 touched
- **Where:** `scripts/workqueue.py:248`, I001 on the local `import workqueue_done` in `moved_to`.
- **Origin:** the line is unchanged from :244 at `620ec316`.
- **Fix:** `ruff check --fix`, or a `noqa` with the reason the comment gives (a circular import).
- **Reproduction:** `tools check --base d3d3839d`.

### 11. Minor, w192 (i33), observation (new): the deprecated work-queue @r23 scenario stays while its replacement's work-item is green
- **Where:** `features/work-queue.feature:69-71`. w192 has no `## Retires`.
- **Why it matters:** the deprecated scenario still passes, so nothing is broken today. It stays as dead weight until some work-item retires it.
- **Fix:** i33 retires it, with `features retire`, in a work-item that lists it.
- **Reproduction:** `features deprecated` lists it, and `grep status .shop/work/i33/w192.md` gives `green`.

### Checked, no finding
- **i32's files since review 7:** unchanged. `git diff --stat 620ec316 HEAD` names none of `agents/bdd-branch-reviewer.md`, `scripts/supervise_answers.py`, `scripts/workqueue_answer.py`, `tests/scenarios/supervision_delegation_steps.py` or `tests/scripts/test_supervise_answers.py`.
- **Risk: w193's change to `supervise_brief.py` alters the reviewer's-question brief.** The `CHANGE_LIST` line is added only for `stage == "apply"`, and `findings_lines` is untouched. The w190 and w191 work-item runs pass.
- **Risk: w192's done condition (`"green" in statuses`, `workqueue_done.py:31`) changes when i32 can be done.** i32 has three green work-items, so the condition holds for it as before.
- **Code that no line asks for in i32:** none, as in review 7.

## Shape

- **Size, 300 lines:** met. `tools size` prints nothing.
- **Module map, i32's rows:** met and unchanged:
  - `supervise_answers.py`;
  - `workqueue_answer.py:31`;
  - `tests/scenarios/supervision_delegation_steps.py`;
  - `tests/scripts/test_supervise_answers.py`.
- **Unreached code or steps:** none. vulture is clean, and every binding names a scenario.
- **Observation (carried):** `asked_by_reviewer` is read three times for one question (`supervise_answers.py:82,106,121`). The refactor is complete when `grep -c asked_by_reviewer scripts/supervise_answers.py` gives 1.

## Coupling

- **Claude CLI / delegation-answerer:** r118 and r119 rely on a `verdict` result field that only the brief names. Naming it in `agents/delegation-answerer.md` (i33's r120) would make this stable.
- **`tests/scripts/stub_claude.py`:** mirrors the CLI's result JSON, so a change in the CLI's fields would show only on a real run.
- **pytest-bdd, ruff, vulture:** used through their public CLI or API only.

## Observations

- i31's status was hand-edited: `git show 3e1cb8bb` (finding 1).
- RUF100 at `test_supervise_answers.py:9,10`: `tools check --base d3d3839d` (finding 2).
- 12 ruff errors under `.shop/work/*/runs/`: `tools check` (finding 3).
- An answered but unmoved reviewer's item waits silently: review 2's probe gives rc 3 and `w1 awaiting-answer` (finding 4).
- The last verdict wins: `supervise_answers.py:124` (finding 5).
- Other initiatives' code is in i32's range: `git log --oneline 620ec316..HEAD -- scripts agents tests` lists `64c62951` and `6b06211b` (finding 6).
- I001 at `test_supervision.py:14` and FURB167 at `stub_claude.py:189,190`: `tools check` (finding 9).
- I001 at `scripts/workqueue.py:248`: `tools check` (finding 10).
- The deprecated @r23 remains with w192 green: `features deprecated` (finding 11).
- `agents/delegation-answerer.md` does not name `verdict` (Cannot verify; r120).
