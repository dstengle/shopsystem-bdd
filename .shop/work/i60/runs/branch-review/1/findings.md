# Branch review of i60

**Verdict: DONE_WITH_CONCERNS.** i60's own work (w233, supervision#r211) is sound: no Critical finding and nothing to fix now in i60. But i60's branch is `main`, so the range `Base..HEAD` also holds other initiatives' work. One of their commits, i54/w232's `a5d6b59b`, gives a wrong answer that is already held open as w232's own fix-now. It is triaged fix now here and goes to the person, to be fixed under w232 and not drafted again in i60. `tools check` fails on two ruff errors, both in other initiatives' commits.

## Range and work-items

- Range: `ae85edd3a2ce3488f4d930ac5814845eea5e6178..91d43216bef3d0fba6f0d6ffddc3e1ddcb56b669`, on the branch `main`.
- i60 (started, fulfils q39) holds:
  - work-item **w233** (green, under supervision, accepts supervision#r211, fileset `tests/scenarios/supervision_delegation_steps.py`). Its commits are `6b7926df`, `864da987`, `4aa66cd4`, `129a247c`, `9b49a82a` and `de6a60b1`, `91d43216` (transitions), and `4e206ec4` (its only code commit, steps only).
  - capability-proposal **i60-supervision** (formulated, adds supervision#r211).
  - capability-proposal **i60-requests** (**awaiting-answer**, adds requests#r59–r63, the `work delegate` lines).
- Every other commit in the range belongs to no i60 work-item. See Finding 1.

## Suite

`Suite: 1069 passed, 0 failed at 91d43216 in 33.99 s`. The run also had 1 skipped, 16 xfailed, 6 xpassed and 56 subtests passed. The 16 xfails are the requests scenarios held by w212 and the work-queue r62 outline "accepted by work-queue".

- It runs in parallel: `-n auto`, pytest-xdist.
- The step definitions do not drive the entry point in-process. `tests/scenarios/conftest.py:27-33` runs each script as `subprocess` `[sys.executable, SCRIPTS/<script>, ...]`.
- The suite is under 60 s, so this is no finding.
- Dry-run against real mode: the system has no dry-run mode of an operation of its own. The only `--dry-run` in `scripts/` is `git push --dry-run` (`supervise_faults.py:71`, `supervise_review.py:55`), a probe of git and not a mode of the system's own. So no agreement test is owed.

## Checks

All the runs below are at `91d43216`.

- **w233's check:** w233's file names no `check:` field. Its scenarios ran as `pytest -p work_items --work-item w233`: exit 0, 182 passed, 1 skipped, 56 subtests passed in 7.10 s.
- **tools check `== ruff ==`:** **2 errors**, exit 1.
  - `tests/scenarios/test_supervision.py:14:1` I001 (import block unsorted).
  - `tests/scenarios/work_queue_list_steps.py:134:12` RUF015.
  - See Finding 4.
- **tools check `== vulture ==`:** clean.
- **tools check `== import-linter ==`:** "the project states no import contracts".
- **tools size:** exit 0 and printed nothing. No tracked Python file is over 300 lines.
- **features deprecated:** exit 0, 19 deprecated scenarios.
  - One of them (`under a delegation, each question of the initiative ... <reply>`, "for: r209 and r210") names a replacement with "no scenario has that title". This predates the range: no commit in it touches that scenario.
  - The two r23 scenarios, deprecated in this range, name the r62 outline. That outline is xfail "accepted by work-queue", so its work-item is not green yet.
  - None of the deprecated scenarios has a replacement whose work-item is green.
- **features bindings:** exit 0, "every binding names a scenario".

## Removed and weakened tests

I searched the change for:

- deleted test or step functions;
- parametrize cases or Examples rows dropped;
- `assert`s removed or loosened;
- skip or xfail added;
- step patterns changed;
- scenarios removed from `features/`.

What I found:

- `tests/scenarios/requests_flow_steps.py:99` `show_prints` (w232, i54, commit `a5d6b59b`) is **loosened**. It used to assert that the whole output of `work show <request>` is `q1 delivered asker`. It now asserts only the first line. It proved that show prints a request's status and turn and nothing else. w232's plan lists it under its tests the decisions break (`.shop/work/i54/runs/w232/2-plan/plan.md:47`), because r59 makes the output run to several lines. It is listed, so this is no finding.
- `tests/scenarios/work_queue_list_steps.py:56` `prints_question` (w232) changed from `parsers.parse` to an anchored `parsers.re`. Its assertion is unchanged. The step now leaves the longer `... and the answer "..."` form to the new step. This is not weakened.
- `features/work-queue.feature` deprecated r23 ×2 and r34/r35 (formulate-round commits `fe960a7a` and `19c0bc4d`). They are tagged `@deprecated` and none was removed. Their deprecations name r62, or removal.
- w233 (`4e206ec4`) removed and weakened nothing. The old Given `fulfils_with_delegation` keeps its pattern, and it writes the same files through the new helpers `start_i1` and `write_q1`. Its plan's "Tests the decisions break" is "None", and that holds.

## Allowances

- w233's report, `## Tests changed under an allowance`: "none". `4e206ec4` changes no `assert`, no expected value and no case, so the report holds.
- w232's allowances are i54's to verify. Its report is outside my brief's reading.

## Cannot verify

None. Every check is given by a run at `91d43216`. w233 names no check of its own.

## Findings

### 1. Minor (observation): the range holds about 150 commits of no i60 work-item, because i60's branch is `main`
- **Work-item:** none in i60. The commits are i54's, i55's, i61's and i62's, and they include intake rounds of q40 and q41.
- **Where:** brief `## Commits`, every line marked `none`. The ones carrying code are `afc4aa72` (i54/w231, steps for r187) and `a5d6b59b` (i54/w232, `work show <request>`). The ones changing `features/` are formulate-round commits:
  - `698c1d44`: i60's r211 scenario;
  - `bb2caae9`: r187;
  - `fe960a7a`: r59–r61, with r34 and r35 deprecated;
  - `19c0bc4d`: r62, with r23 deprecated.
  No work-item commit changes `features/`, so no Critical.
- **What is wrong:** the base-to-head range does not separate i60's work from that of the initiatives running alongside it. A review of i60 so reads, and is held by, other initiatives' code (Findings 2 and 4).
- **Why it matters:** a fault in another initiative's code fails i60's review, and the same finding can be drafted twice.
- **Fix:** give the branch review only the commits of the initiative's own nodes, or run each initiative on its own branch.
- **Reproduction:** brief lines 201–352, each marked `none`. Only lines 353–360 are w233's.

### 2. Important (fix now): `work show <request>` leaves out every line of a request that has no line outcome yet
- **Work-item:** w232 (i54), commit `a5d6b59b`. It is already w232's open fix-now: `.shop/work/i54/w232.md:14`, and w232 is awaiting-answer.
- **File:** `scripts/workqueue_list.py:85-88` (`request_parts`): `if outcome is not None:` prints a line only when it has an outcome.
- **What is wrong:** work-queue r59 asks show to print "its lines with their line outcomes". A request still in the upstream's turn, with some or all lines unsettled, shows fewer lines or none. This is a wrong answer.
- **Why it matters:** the person or the asker reading `work show q<n>` cannot see what was asked until the upstream has answered each line.
- **Fix:** print every line, with its outcome or a marker such as `no outcome yet`. Do this under w232 in i54, not as a new i60 work-item.
- **Test that would show it (not run):** a scenario of `work show q1` where line 2 has no outcome, asserting that line 2 is printed.

### 3. Minor (observation): r211's `after` example does not tell a live read from a read at the first `work run`
- **Work-item:** w233.
- **File:** `tests/scenarios/supervision_delegation_steps.py:32-40` (`fulfils_with_delegation_given`).
- **What is wrong:** both commits, initiative.md and then the delegation, land before `work run i1`. A copy taken at the start of the first `work run` would pass the example as well. The production read is live today: I verified with one focused look that `supervise_answers.py` `Answers.delegation` re-reads the request on each call (also in w233's review).
- **Why it matters:** a future cache of the delegation would not be caught.
- **Fix:** a scenario where the delegation is given or changed between two `work run`s. The plan and the report name this as their open case.
- **Test that would show it (not run):** run `work run i1` with q1 undelegated and w1 awaiting-answer. Then commit a delegation on q1 and run `work run i1` again. Assert that the question was given to a delegation session in the second run.

### 4. Minor (observation): `tools check` fails on two ruff errors in files the branch touched
- **Work-items:** w231 (i54, `afc4aa72`) for `tests/scenarios/test_supervision.py:14` I001, caused by the added `from .supervision_merge_steps import *`. w232 (i54, `a5d6b59b`) for `tests/scenarios/work_queue_list_steps.py:134:12` RUF015.
- **What is wrong:** the import block is unsorted, and a single-element slice is used where `next(...)` belongs.
- **Why it matters:** `tools check` exits 1 for every branch built on `main` until they are fixed.
- **Fix:** `ruff --fix` for I001, and `next(...)` at line 134.
- **Reproduction:** brief, `### tools check`, exit code 1, the two lines above.

### 5. Minor (observation): i60 holds the capability-proposal i60-requests awaiting-answer
- **Work-item:** none (proposal i60-requests).
- **File:** `.shop/work/i60/requests.md`: status `awaiting-answer`, with five open questions on requests#r59–r63 (`work delegate`). One has been answered.
- **What is wrong:** under supervision r213 and work-queue r62/r47, i60 cannot be `done` while this proposal is neither formulated nor withdrawn, although w233 is green. Until `work delegate` exists, delegations are reworded by hand (`9b453fd2`).
- **Fix:** answer or withdraw the proposal. This is the person's call under the delegation.

### 6. Minor (observation): `work show <request> --json` gives none of what r59 lists
- **Work-item:** w232 (i54).
- **File:** `scripts/workqueue_list.py:100-102`: the `--json` branch prints only `{request, status, turn}`, as w232's plan decided (D4).
- **What is wrong:** work-queue r38 says `--json` prints show's result as one JSON object. Read with r59, the result holds the lines, outcomes, questions, answers and resolution.
- **Fix:** add those fields to the JSON object, or write a line saying the JSON form gives only status and turn.
- **Test that would show it (not run):** `work show q1 --json` on the r59 fixture, asserting the lines and the resolution are present.

## Shape

- **CLAUDE.md size limit:** met. `tools size` printed nothing. `supervision_delegation_steps.py` has 258 lines (w233's review).
- **Module map:**
  - `scripts/workqueue_list.py` ("`work list` and `work show <target>`"): `request_parts` (`:79-94`) is show's request output. Met.
  - `scripts/workqueue_request.py` ("the requests of a context"): `sections` (`:32-37`) reads a request's parts. Met.
  - `tests/scenarios/` ("one `<capability>_*_steps.py` module a concern"): the new `supervision_merge_steps.py` (r187) and the extended `supervision_delegation_steps.py:14-40` (r211). Met.
- **Code no scenario reaches:** none found. The old `fulfils_with_delegation` Given is still reached by the r78, r210 and glossary scenarios and by `supervision_session_faults_steps.py`. The default `delegation=None` of `write_q1` is reached by the `after` example.
- **Code no line asks for:** none. w233 changes no production code. `request_parts` and `sections` serve work-queue r59.

## Coupling

- **pytest-bdd on pytest internals.** The suite prints `PytestRemovedIn10Warning` from `pytest_bdd/compat.py:28`: pytest-bdd calls pytest's private `_fixturemanager._register_fixture` with a nodeid, and `FixtureDef` with a baseid. These are not part of pytest's public API, and they break under pytest 10. Fix: pin `pytest<10`, or upgrade pytest-bdd to a release that passes `node`.
- **Unregistered marks.** pytest-bdd turns each Gherkin tag into `pytest.mark.<tag>` (`@deprecated`, `@r209`, `@r210`, `@r211`), and the run prints `PytestUnknownMarkWarning`. This would break under `--strict-markers`. Fix: register the tags as markers in the conftest's `pytest_configure`.
- **git.** The steps drive `git` through `subprocess` (`supervision_world.py:54`) only through its CLI. They rely on nothing beyond what it publishes.

## Observations

- F1: reproduction is the brief's `## Commits`, lines 201–352, all marked `none`, on branch `main`.
- F3: reproduction is in `supervision_delegation_steps.py:37-40`. Both commits come before `When the person runs work run i1`. The test is not run.
- F4: reproduction is the brief's `tools check`, exit 1, `test_supervision.py:14:1 I001` and `work_queue_list_steps.py:134:12 RUF015`.
- F5: reproduction is `.shop/work/i60/requests.md`, line 5, `status: awaiting-answer`.
- F6: reproduction is `workqueue_list.py:100-102`, where the JSON object is `{"request", "status", "turn"}` only. The test is not run.
