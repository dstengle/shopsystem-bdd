# Branch review of i60 (review 4)

**Verdict: DONE_WITH_CONCERNS.** w233 (supervision#r211), i60's only work-item, is still sound: it adds step definitions only and has no finding to fix now. But the whole suite now fails at the head, with 10 failures, and two findings are triaged fix now:

- **Finding 1 (new, Important, fix now): data lost.** i60's own capability-proposal i60-requests lost requests r65–r71 from its `adds`. Integrate round 25 rewrote the proposal's lists to `adds: [requests#r72]` and `removes: [requests#r69]`. r65–r71 are applied in `spec/` and formulated in `features/requests.feature`. Now no proposal and no work-item holds them, so:
  - their 10 scenario cases are no longer expected failures, and the whole suite fails;
  - no work-item will ever be drafted to deliver them.
- **Finding 2 (carried over, Important, fix now):** i54/w232's `work show <request>` leaves out lines that have no line outcome. It is still unfixed and is still w232's open question.

`tools check` still exits 1, on the same five ruff errors as review 3.

## Since review 3 (head `46d6b92a`)

The range has gained these commits:

- `215d9497`: branch review 3.
- `2d855982`: `work answer: requests`, the person's answer on r69, reading 1.
- `74578d67`, `d2c12bbb`, `e506e7ef`, `a9c27ae3`: workflow transitions and notes.
- `1fdab1cc`: i60-requests goes from `awaiting-answer` to `drafted`. This is integrate round 25, and it is where the lists were rewritten (Finding 1).
- `b2554e02`: i60-requests goes from `drafted` to `awaiting-answer`, at gate round 26.

None of them touches anything outside `.shop/`. The change outside `.shop/` is the same as in review 3.

## Range and work-items

- Range: `ae85edd3a2ce3488f4d930ac5814845eea5e6178..b2554e029ed0fe9e9cc4a6f837a6589b73023282`, on branch `main`.
- i60 (`started`, fulfils q39) holds:
  - work-item **w233**: `green`, under supervision, accepts supervision#r211, fileset `tests/scenarios/supervision_delegation_steps.py`.
    - Its transition commits are `6b7926df`, `864da987`, `4aa66cd4`, `129a247c`, `9b49a82a`, `de6a60b1` and `91d43216`.
    - Its only change is `4e206ec4` (steps only).
  - capability-proposal **i60-supervision**: `formulated`.
  - capability-proposal **i60-requests**: `awaiting-answer`.
    - It now reads `adds: [requests#r72]`, `changes: []` and `removes: [requests#r69]` (`.shop/work/i60/requests.md:8-10`).
    - Its open question is the r69→r72 swap from gate round 26 (`requests.md:26`).
- Every other commit in the range is marked `none` (Finding 3).

## Suite

`Suite: 1069 passed, 10 failed at b2554e02 in 34.63 s`

- The run also had 1 skipped, 16 xfailed, 6 xpassed and 56 subtests passed, and it exited 1.
- **All 10 failures are the requests r65–r71 `work delegate` scenarios.** These are r65 ×2, r66, r67, r68 ×3, r70 ×2 and r71.
  - In review 3 they were 10 of 26 xfails. Now they run and fail, because there are no steps yet:
    - `IndexError` at `tests/scenarios/requests_steps.py:63`;
    - `StepDefinitionNotFoundError` for "q1 holds no delegation" and for "q1 holds the delegation …".
  - xfails fell from 26 to 16. The difference is these 10 (Finding 1).
- **Parallel:** yes, `-n auto` (pytest-xdist).
- **In-process:** no. Step definitions run each script as a subprocess (`tests/scenarios/conftest.py:33-34`, verified). The suite is under 60 s, so this is no finding.
- **Dry-run against real mode:** the system has no dry-run mode of an operation of its own (review 2). No agreement test is owed.

## Checks

All runs are at `b2554e02`.

- **w233's check:** `w233.md` names no `check:` field. Its scenarios ran as `pytest -n auto -p work_items --work-item w233`: exit 0, `182 passed, 1 skipped, 56 subtests passed in 6.96s`. Both r211 examples (`[before]`, `[after]`) ran: the warnings name them.
- **Whole suite:** exit 1, with 10 failed (above).
- **tools check `== ruff ==`:** exit 1, with five errors:
  - `.shop/work/i60/runs/requests/23-formulate/splice.py:2:5`, `:3:5` and `:8:1`: SIM115, three times (Finding 5);
  - `tests/scenarios/test_supervision.py:14:1`: I001 (Finding 6);
  - `tests/scenarios/work_queue_list_steps.py:134:12`: RUF015 (Finding 6).
- **tools check `== vulture ==`:** clean.
- **tools check `== import-linter ==`:** "the project states no import contracts". No heading says `missing`.
- **tools size:** exit 0 and printed nothing.
- **features deprecated:** exit 0, 19 deprecated scenarios, as in review 3.
  - The r23 ×2 scenarios are deprecated for r62. The r62 outline is still xfail ("accepted by work-queue"), so it is not green.
  - r34 and r35 are "for: removal". Their work-item, w232, is `awaiting-answer`.
  - The `<reply>` delegation scenario says "for: r209 and r210", and the run says "no scenario has that title". This predates the range.
  - No deprecated scenario has a replacement whose work-item is `green`.
- **features bindings:** exit 0, "every binding names a scenario".

## Removed and weakened tests

What I searched the change for:

- deleted test or step functions;
- dropped Examples rows or parametrize cases;
- `assert`s removed or loosened;
- skip or xfail added;
- changed step patterns;
- scenarios removed from `features/`.

What I found:

- **`tests/scenarios/requests_flow_steps.py:99` `show_prints`** (i54/w232, `a5d6b59b`) is loosened. It used to assert the whole output and now asserts only the first line. w232's plan lists it under "Tests the decisions break" (review 2), so it is no finding.
- **`tests/scenarios/work_queue_list_steps.py:56` `prints_question`** (w232) moved to an anchored `parsers.re`. The assertion is unchanged, so it is not weakened.
- **`features/`:** r23 ×2, r34 and r35 were tagged `@deprecated` by formulate rounds. Nothing was removed.
- **w233 (`4e206ec4`)** removed and weakened nothing. The old Given keeps its pattern and writes the same files through `start_i1` and `write_q1`. Its plan's "Tests the decisions break" says "None" (`plan.md:26`), and that holds.
- **No xfail was added.** The opposite happened: 10 scenarios lost their expected-failure mark. That came from the proposal's lists, not from a test change (Finding 1).

## Allowances

- **w233's report**, `## Tests changed under an allowance`: "none". `4e206ec4` changes no `assert`, no expected value and no case, so the claim holds.
- **w232's report** (i54): "none". Its loosened test is in its plan's list.

## Cannot verify

None. Every check comes from a run at `b2554e02`.

## Findings

### 1. Important (fix now): i60-requests lost requests r65–r71, so the whole suite fails and no work-item will deliver them

- **Work-item:** none. This is i60's proposal i60-requests, rewritten by `work run`'s integrate round 25 in commit `1fdab1cc`.
- **Files:**
  - `.shop/work/i60/requests.md:8-10`: `adds: [requests#r72]`, `changes: []`, `removes: [requests#r69]`.
  - The mechanism: `scripts/supervise_change.py:59-72` `rewrite_lists`. Called from `write_proposals` at `:115`, it replaces the lists of the proposal the round was started for with the new change list alone.
- **What is wrong:** requests r65–r71 were applied (`186d4789`) and formulated (`9172f19e`). Formulate round 24 then formulated nothing and started integrate round 25 (r186). That round's change list held only the r69→r72 swap, so the proposal's earlier ids were dropped. As a result:
  - **The suite fails.** `scripts/work_items.py:73-87` (`proposals`) marks a scenario xfail only when an open proposal's `adds` or `changes` names its requirement. No work-item accepts r65–r71 either (`acceptors`, `:60-70`). So their 10 cases now run and fail.
  - **The ids are lost to delivery.** When i60-requests is formulated, `supervise_draft.py:87` drafts work-items from `adds` and `changes`, which now hold only r72. r65–r71 would stay in `spec/` and `features/` with no work-item and red scenarios.
- **Why it matters:** this is data lost, and a wrong state. The branch's head fails its whole suite.
- **The line gap:** supervision r187 keeps a proposal's held ids when a round started for *another* proposal names its capability. No line keeps them when the round re-integrates the proposal it was started for (r142, r148, r159, r186). The `rewrite_lists` docstring cites r114, which is retired.
- **Fix:**
  1. Restore `adds: [requests#r65, requests#r66, requests#r67, requests#r68, requests#r70, requests#r71, requests#r72]` and `removes: [requests#r69]` in `.shop/work/i60/requests.md`.
  2. Write a supervision line, through integrating-a-proposal: when an integrate round started for a capability-proposal ends, `work run` shall keep the ids the proposal already holds that `spec/` holds, adding the round's own ids.
  3. Then change `rewrite_lists` to keep those ids.
- **Reproduction:** the brief's whole-suite run shows 10 FAILED on r65–r71, where review 3's run at `46d6b92a` had them as xfail. Ledger lines 11-12 show the r186 path.
- **Test that would show it (not run):** an integrate round restarted under r186 for a proposal whose `adds` holds applied ids, giving a change list that names one other id. Assert that the proposal's `adds` still holds the earlier ids.

### 2. Important (fix now): `work show <request>` leaves out every line of a request that has no line outcome yet

- **Work-item:** w232 (i54), commit `a5d6b59b`. It is still w232's open question (`.shop/work/i54/w232.md:14`), and w232 is `awaiting-answer`. Fix it under w232 and do not draft it again in i60.
- **File:** `scripts/workqueue_list.py:85-88`. The `if outcome is not None:` test prints a line only when it has an outcome.
- **What is wrong:** work-queue r59 asks for the request's "lines with their line outcomes". An unsettled request is shown with fewer lines, or with none.
- **Fix:** print every line, with its outcome or `no outcome yet`.
- **Test that would show it (not run):** `work show q1` where line 2 has no outcome, asserting that line 2 is printed.

### 3. Minor (observation): the range holds commits of no i60 work-item, because i60's branch is `main`

- **Work-item:** none in i60.
- **Where:** every line of the brief's `## Commits` is marked `none` except w233's seven commits.
- **Commits that carry code:** `afc4aa72` (i54/w231, steps for r187) and `a5d6b59b` (i54/w232).
- **Commits that change `features/`:** formulate rounds only: `698c1d44`, `bb2caae9`, `fe960a7a`, `19c0bc4d` and `9172f19e`. None of them is a work-item commit.
- **Why it matters:** other initiatives' faults (Finding 2) hold up i60's review.
- **Fix:** give a branch review only the commits of the initiative's own nodes, or run each initiative on its own branch.

### 4. Minor (observation): r211's `after` example does not tell a live read from a read at the first `work run`

- **Work-item:** w233.
- **File:** `tests/scenarios/supervision_delegation_steps.py:32-40`.
- **What is wrong:** both commits land before `work run i1`. A copy of the delegation taken when the first `work run` starts would also pass.
- **What I verified:** the read is live today (`supervise_answers.py`, reviews 1-3). Nothing in the range touches it.
- **Fix:** add a scenario where the delegation is given between two `work run`s.
- **Test that would show it (not run):**
  1. Run `work run i1` with q1 undelegated and w1 awaiting-answer.
  2. Commit a delegation on q1.
  3. Run `work run i1` again, and assert that the question went to a delegation session.

### 5. Minor (observation): a formulate round's helper script stays tracked under i60's runs and fails `tools check`

- **Work-item:** none (i60-requests, formulate round 23).
- **File:** `.shop/work/i60/runs/requests/23-formulate/splice.py:2,3,8`, SIM115.
- **Fix:** exclude `.shop/` from ruff and vulture, or have `work run` leave a session's helper scripts out of a stage's kept files.
- **Reproduction:** the brief's `### tools check`, exit 1.

### 6. Minor (observation): two ruff errors older than the range, in files the range touched

- **The two errors:** `tests/scenarios/test_supervision.py:14` I001 (touched by `afc4aa72`) and `tests/scenarios/work_queue_list_steps.py:134:12` RUF015 (outside `a5d6b59b`'s hunk).
- **Fix:** run `ruff --fix` on the import block, and use `next(...)`.

### 7. Minor (observation): i60 cannot be done while i60-requests is awaiting-answer

- **Work-item:** none (i60-requests).
- **File:** `.shop/work/i60/requests.md:5,26`. Gate round 26 asks whether to swap r69 for r72.
- **What follows:** under supervision r213 and work-queue r62/r47, i60 stays `started`.
- **Fix:** answer it under the delegation (it is not a glossary question; reading A is recommended), after Finding 1's restore.

### 8. Minor (observation): `work show <request> --json` gives none of what r59 lists

- **Work-item:** w232 (i54).
- **File:** `scripts/workqueue_list.py:102`. The object is `{request, status, turn}` only.
- **Fix:** add the lines, outcomes, questions, answers and resolution, or write a line that limits the JSON form.
- **Test that would show it (not run):** `work show q1 --json` on the r59 fixture.

### 9. Minor (observation): 6 xpassed scenarios that the suite's output does not name

- **Work-item:** unknown, probably w232's r59–r61.
- **What is wrong:** the run uses `-rfEx` and the expected failures are not strict (`work_items.py:112`, `strict=False`).
- **Fix:** strict expected failures, or `-rX` in the whole-suite run.
- **Test that would show it (not run):** the whole-suite command with `-rX`.

## Shape

- **CLAUDE.md size limit:** met. `tools size` printed nothing.
- **Module map:**
  - `scripts/workqueue_list.py` (`request_parts`, `:79-94`): met.
  - `scripts/workqueue_request.py` (`sections`): met.
  - `tests/scenarios/supervision_merge_steps.py` and `supervision_delegation_steps.py:14-40`: met, one `<capability>_*_steps.py` module a concern.
  - `scripts/supervise_change.py` (the integrate round's change list into proposals): its row's concern holds. Its `rewrite_lists` docstring cites retired r114 (`:61`) (Finding 1).
- **Code no scenario reaches:** none found. `write_q1(None)` is reached by the `after` example.
- **Code no line asks for:** none in the range. w233 changes no production code. `request_parts` and `sections` serve work-queue r59.
- **Steps missing:** `work delegate` (r65–r71) has no steps, as expected while no work-item delivers it. Its scenarios must stay expected failures until one does (Finding 1).
- **Behaviour against Purpose:** nothing contradicts supervision's Purpose. The contradictions of lines are Finding 2 (r59) and Finding 1, a gap where no line keeps a proposal's ids.

## Coupling

- **pytest-bdd on pytest internals.** `pytest_bdd/compat.py:28` uses a nodeid and a baseid, and the run warns `PytestRemovedIn10Warning`. This breaks under pytest 10. Fix: pin `pytest<10`, or upgrade pytest-bdd.
- **Unregistered marks.** The tags `deprecated`, `r209`, `r210` and `r211` warn `PytestUnknownMarkWarning`, and they would break under `--strict-markers`. Fix: register them in the conftest.
- **git.** It is driven through its CLI only, on published behaviour. Stable.

## Observations

- F1: the brief's whole suite has 10 FAILED on `test_delegate_*` (r65–r71), where review 3 had 26 xfailed. `.shop/work/i60/requests.md:8` reads `adds: [requests#r72]`.
- F2: `workqueue_list.py:85-88`, `if outcome is not None`. Not run.
- F3: the brief's `## Commits`. All lines are `none` but w233's.
- F4: `supervision_delegation_steps.py:37-40`. Both commits come before `work run`. Not run.
- F5: the brief's `### tools check`, `splice.py` SIM115 ×3.
- F6: the brief's `### tools check`, I001 and RUF015.
- F7: `requests.md:5` `status: awaiting-answer`, and gate round 26's question at line 26.
- F8: `workqueue_list.py:102`. Not run.
- F9: the brief's "6 xpassed", with no XPASS line. Not run with `-rX`.
