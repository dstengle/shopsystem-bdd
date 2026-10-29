# Branch review of i60 (review 3)

**Verdict: DONE_WITH_CONCERNS.** i60's own work-item is sound. That is w233 (supervision#r211), which adds step definitions only and no production code. It has no Critical finding and nothing to fix now.

The review still goes to the person, for two reasons:

- **A fix-now finding in another initiative's code.** i60's branch is `main`, so `Base..HEAD` also holds other initiatives' code. One of those commits, i54/w232's `a5d6b59b`, gives a wrong answer for `work show <request>` (Finding 2). It was triaged fix now in review 2 and it is still unfixed at `46d6b92a`. It is already w232's own open question (`.shop/work/i54/w232.md:14`), so fix it under w232 in i54 and do not draft it again in i60.
- **`tools check` exits 1.** It now fails on five ruff errors:
  - three are new, in a helper script that i60's own formulate round left tracked under `.shop/` (Finding 4);
  - two predate this review (Finding 5).

## Since review 2 (head `40b081a4`)

The range has gained these commits:

- `45d99887`: branch review 2.
- `ceffd8cf`, `7895c544`, `f4f29679`, `c8a19c0e`, `46d6b92a`: workflow transitions and notes.
- `186d4789`: the spec commit adding requests r65–r71 (`work delegate`).
- `9172f19e`: the formulate round adding six scenarios for r65–r68, r70 and r71 to `features/requests.feature`.

The rest of the change outside `.shop/` is the same as in reviews 1 and 2.

## Range and work-items

- Range: `ae85edd3a2ce3488f4d930ac5814845eea5e6178..46d6b92a8f9043dd26bb8c4e8525ae22f31d3af8`, on branch `main`.
- i60 (`started`, fulfils q39) holds:
  - work-item **w233**: `green`, under supervision, accepts supervision#r211, fileset `tests/scenarios/supervision_delegation_steps.py`.
    - Its transition commits are `6b7926df`, `864da987`, `4aa66cd4`, `129a247c`, `9b49a82a`, `de6a60b1` and `91d43216`.
    - Its only change is `4e206ec4` (steps only).
  - capability-proposal **i60-supervision**: `formulated`, adds supervision#r211.
  - capability-proposal **i60-requests**: `awaiting-answer`, adds requests#r65–r71.
    - Apply round 22 applied it (`186d4789`).
    - Formulate round 23 (`9172f19e`) formulated six of the seven lines and asked one question, on r69.
- Every other commit in the range is marked `none` (Finding 1).

## Suite

`Suite: 1069 passed, 0 failed at 46d6b92a in 35.22 s`

- The run also had 1 skipped, 26 xfailed, 6 xpassed and 56 subtests passed, and it exited 0.
- The xfails rose from 16 in review 2 to 26. The 10 new ones are the new requests scenarios. Counting each Examples row, they are r65 ×2, r66, r67, r68 ×3, r70 ×2 and r71, each "accepted by requests, neither green nor withdrawn". That is as it should be: no work-item delivers them yet.
- **Parallel:** yes, `-n auto` (pytest-xdist).
- **In-process:** no. The step definitions run each script as a subprocess (`tests/scenarios/conftest.py:33-34`, verified in review 2). The suite is under 60 s, so this is no finding.
- **Dry-run against real mode:** the system has no dry-run mode of an operation of its own. The only `--dry-run` in `scripts/` is a `git push --dry-run` probe (review 2). No agreement test is owed.

## Checks

All runs are at `46d6b92a`.

- **w233's check:** `w233.md` names no `check:` field. Its scenarios ran as `pytest -n auto -p work_items --work-item w233`: exit 0, `182 passed, 1 skipped, 56 subtests passed in 7.15s`. Both r211 examples (`[before]`, `[after]`) ran: the run's warnings name them.
- **tools check `== ruff ==`:** exit 1, with five errors:
  - `.shop/work/i60/runs/requests/23-formulate/splice.py:2:5`, `:3:5` and `:8:1`: SIM115, three times. These are new and are i60's own (Finding 4).
  - `tests/scenarios/test_supervision.py:14:1`: I001. This predates the range (Finding 5).
  - `tests/scenarios/work_queue_list_steps.py:134:12`: RUF015. This predates the range (Finding 5).
- **tools check `== vulture ==`:** clean.
- **tools check `== import-linter ==`:** "the project states no import contracts". No heading says `missing`.
- **tools size:** exit 0 and printed nothing. No tracked Python file is over 300 lines.
- **features deprecated:** exit 0, 19 deprecated scenarios.
  - The two r23 scenarios name the r62 outline. That outline is still xfail, so its replacement is not green.
  - r34 and r35 are "for: removal". w232 is the work-item that retires them, and it is awaiting-answer.
  - The `<reply>` delegation scenario says "for: r209 and r210", and the run says "no scenario has that title". This predates the range: no commit in the range touches it.
  - No deprecated scenario has a replacement whose work-item is `green`.
- **features bindings:** exit 0, "every binding names a scenario".

## Removed and weakened tests

What I searched the change for:

- deleted test or step functions;
- Examples rows or parametrize cases dropped;
- `assert`s removed or loosened;
- skip or xfail added;
- step patterns changed;
- scenarios removed from `features/`.

What I found:

- **`tests/scenarios/requests_flow_steps.py:99` `show_prints`** (i54/w232, `a5d6b59b`) is loosened.
  - It used to assert that the whole output of `work show <request>` was `q1 delivered asker`. It now asserts only the first line.
  - w232's plan lists it under "Tests the decisions break" (`.shop/work/i54/runs/w232/2-plan/plan.md:47`, per review 2), so it is no finding.
- **`tests/scenarios/work_queue_list_steps.py:56` `prints_question`** (w232) moved from `parsers.parse` to an anchored `parsers.re`. The assertion is unchanged, so it is not weakened.
- **`features/`:** r23 ×2, r34 and r35 were tagged `@deprecated` by formulate rounds. None was removed. `9172f19e` only adds scenarios.
- **w233 (`4e206ec4`)** removed and weakened nothing. The old Given `fulfils_with_delegation` keeps its pattern and writes the same files through `start_i1` and `write_q1`. Its plan's "Tests the decisions break" says "None" (plan.md:26), and that holds.

## Allowances

- **w233's report**, `## Tests changed under an allowance`: "none". `4e206ec4` changes no `assert`, no expected value and no case, so the claim holds.
- **w232's report** also says "none". Its only loosened test is in its plan's list, so no allowance is needed.

## Cannot verify

None. Every check comes from a run at `46d6b92a`.

## Findings

### 1. Minor (observation): the range holds commits of no i60 work-item, because i60's branch is `main`

- **Work-item:** none in i60. The commits belong to i54, i55, i61 and i62, to the q40 and q41 intake rounds, and to i60's own proposal rounds.
- **Where:** the brief's `## Commits`. Every line is marked `none` except brief lines 367–374, which are w233's.
- **Commits that carry code:**
  - `afc4aa72`: i54/w231, steps for r187.
  - `a5d6b59b`: i54/w232, `work show <request>`.
- **Commits that change `features/`:** each is a formulate-round commit, which is how the workflow itself adds scenarios (supervision r83 and r132):
  - `698c1d44`: i60's r211;
  - `bb2caae9`: r187;
  - `fe960a7a`: r59–r61 added, r34 and r35 deprecated;
  - `19c0bc4d`: r62 added, r23 deprecated;
  - `9172f19e`: i60's requests r65–r71.
- **Why this is not Critical:** no work-item commit changes `features/`.
- **What is wrong:** base-to-head does not separate i60's work from the work of the initiatives running alongside it.
- **Why it matters:** another initiative's faults (Findings 2 and 5) hold up i60's review.
- **Fix:** give a branch review only the commits of the initiative's own nodes, or run each initiative on its own branch.

### 2. Important (fix now): `work show <request>` leaves out every line of a request that has no line outcome yet

- **Work-item:** w232 (i54), commit `a5d6b59b`. It is already w232's open question (`.shop/work/i54/w232.md:14`), and w232 is `awaiting-answer`. Do not draft it again in i60.
- **File:** `scripts/workqueue_list.py:85-88` (`request_parts`). The `if outcome is not None:` test prints a line only when the line has an outcome. The diff at `46d6b92a` shows the code unchanged since review 2.
- **What is wrong:** work-queue r59 asks show to print the request's "lines with their line outcomes". A request whose lines are not all settled is shown with fewer lines, or with none. That is a wrong answer.
- **Fix:** print every line, with its outcome or a marker such as `no outcome yet`.
- **Test that would show it (not run):** `work show q1` where line 2 has no outcome, asserting that line 2 is printed.

### 3. Minor (observation): r211's `after` example does not tell a live read from a read at the first `work run`

- **Work-item:** w233.
- **File:** `tests/scenarios/supervision_delegation_steps.py:32-40`.
- **What is wrong:** both commits land before `work run i1`, the start first and then the delegation. A copy of the delegation taken when the first `work run` starts would also pass.
- **What I verified:** today the read is live. `supervise_answers.py` `Answers.delegation` re-reads the request on each call (reviews 1 and 2). Nothing in this range touches that file.
- **Why it matters:** a future cache of the delegation would not be caught.
- **Fix:** add a scenario where the delegation is given or changed between two `work run`s.
- **Test that would show it (not run):**
  1. Run `work run i1` with q1 undelegated and w1 awaiting-answer.
  2. Commit a delegation on q1.
  3. Run `work run i1` again, and assert that the question went to a delegation session in that second run.

### 4. Minor (observation): a formulate round's helper script stays tracked under i60's runs and fails `tools check`

- **Work-item:** none (i60's proposal i60-requests, formulate round 23).
- **File:** `.shop/work/i60/runs/requests/23-formulate/splice.py:2,3,8`. The three ruff errors are `open()` without a context manager.
- **What is wrong:** the session's scratch script, which splices the draft into `features/requests.feature`, was kept with the stage directory. Ruff now lints it as project code.
- **What it refers to:** it names `.shop/scratch/23-formulate/...`, a path that no longer exists once the scratch is gone.
- **Why it matters:** `tools check` fails on workflow records, not on code, and that holds every later review on `main`.
- **Fix:** exclude `.shop/` from ruff (and from vulture), or have `work run` leave a session's helper scripts out of what it keeps of a stage.
- **Reproduction:** the brief's `### tools check` shows exit 1 with the three SIM115 lines on `splice.py`.

### 5. Minor (observation): two ruff errors older than the range, in files the range touched

- **The two errors:**
  - `tests/scenarios/test_supervision.py:14` I001. The file was touched by i54/w231 (`afc4aa72`). The disorder is at lines 27-28 and 41-42, not at the added line 36 (review 2).
  - `tests/scenarios/work_queue_list_steps.py:134:12` RUF015. The file was touched by i54/w232 (`a5d6b59b`). Line 134 lies outside the change's hunk, which covers new lines 53-117.
- **Fix:** run `ruff --fix` on the import block, and use `next(...)` at line 134.

### 6. Minor (observation): i60 cannot be done while i60-requests is awaiting-answer

- **Work-item:** none (proposal i60-requests).
- **File:** `.shop/work/i60/requests.md:5` says `status: awaiting-answer`. The open question is r69's (line 25), from formulate round 23.
- **Why it stays open:** r69 is a session's behaviour and has no scenario. The question asks where the date goes: inside the delegation text, or beside it.
- **What follows:** under supervision r213 and work-queue r62/r47, i60 stays `started` even though w233 is green. The requests r65–r71 lines still have no work-item, so their scenarios stay xfail.
- **Fix:** answer the r69 question under the delegation. It is not a glossary question, and the delegation answers with the recommended reading, which the question does not yet mark. Or ask the person.

### 7. Minor (observation): `work show <request> --json` gives none of what r59 lists

- **Work-item:** w232 (i54).
- **File:** `scripts/workqueue_list.py:102`. The JSON object is `{request, status, turn}` only.
- **What is wrong:** r38, read with r59, implies that the JSON form holds the lines, outcomes, questions, answers and resolution.
- **Fix:** add those fields, or write a line saying that the JSON form gives the status and turn only.
- **Test that would show it (not run):** `work show q1 --json` on the r59 fixture, asserting the lines and the resolution.

### 8. Minor (observation): 6 xpassed scenarios that the suite's output does not name

- **Work-item:** unknown. They are probably w232's r59–r61 scenarios, whose code is on `main` while w232 is not green.
- **What is wrong:** the run uses `-rfEx`, so it names xfails but not xpasses, and the expected failures are not strict.
- **Fix:** make the `work_items` plugin's expected failures strict, or report X in the whole-suite run.
- **Test that would show it (not run):** the whole-suite command with `-rX`.

## Shape

- **CLAUDE.md size limit:** met. `tools size` printed nothing.
- **Module map:**
  - `scripts/workqueue_list.py` (`request_parts`, `:79-94`): met.
  - `scripts/workqueue_request.py` (`sections`, `:32-37`): met.
  - `tests/scenarios/supervision_merge_steps.py` and `supervision_delegation_steps.py:14-40`: met, one `<capability>_*_steps.py` module a concern.
  - `9172f19e` adds scenarios only. No steps exist for `work delegate` yet, which is expected while no work-item delivers r65–r71.
- **Code no scenario reaches:** none found. The old `fulfils_with_delegation` is still reached by the r78 and r210 scenarios and the glossary scenarios. `write_q1(delegation=None)` is reached by the `after` example.
- **Code no line asks for:** none. w233 changes no production code. `request_parts` and `sections` serve work-queue r59.
- **Behaviour against Purpose:** nothing contradicts supervision's Purpose. The one contradiction of a line is Finding 2 (r59).

## Coupling

- **pytest-bdd on pytest internals.** `pytest_bdd/compat.py:28` calls `_register_fixture` with a nodeid and builds a `FixtureDef` with a baseid. The run warns `PytestRemovedIn10Warning`, so both break under pytest 10. Fix: pin `pytest<10`, or move to a pytest-bdd release that passes a node.
- **Unregistered marks.** The Gherkin tags `deprecated`, `r209`, `r210` and `r211` become pytest marks, and the run warns `PytestUnknownMarkWarning`. They would break under `--strict-markers`. Fix: register them in the conftest.
- **git.** It is driven through its CLI only, on published behaviour. Stable.

## Observations

- F1: the brief's `## Commits`. Every line but 367–374 is `none`, on branch `main`.
- F3: `supervision_delegation_steps.py:37-40`. Both commits come before `When the person runs work run i1`. Not run.
- F4: the brief's `### tools check`, exit 1, with `splice.py:2:5`, `:3:5` and `:8:1` SIM115.
- F5: the brief's `### tools check`, with `test_supervision.py:14:1 I001` and `work_queue_list_steps.py:134:12 RUF015`.
- F6: `.shop/work/i60/requests.md:5`, `status: awaiting-answer`. Ledger line 10: "formulate requests round 1: ... 1 question (r69)".
- F7: `workqueue_list.py:102`, `{"request", "status", "turn"}` only. Not run.
- F8: the brief's whole-suite run says "6 xpassed", and its summary has no XPASS line. Not run with `-rX`.
