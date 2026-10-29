# Branch review of i60 (review 2)

**Verdict: DONE_WITH_CONCERNS.** i60's own work is sound. That is w233 (supervision#r211, a step definition only, no production code): it has no Critical finding and nothing to fix now. But i60's branch is `main`, so `Base..HEAD` also holds other initiatives' code. One of their commits, i54/w232's `a5d6b59b`, gives a wrong answer for `work show <request>`. That is triaged fix now and goes to the person. It is already w232's own open question, so fix it under w232 and do not draft it again in i60. `tools check` exits 1 on two ruff errors. Both are in files the range touched, but both predate it.

Since branch review 1 (head `91d43216`), the range has gained only workflow commits under `.shop/` (`ff632c3a`..`40b081a4`: the i60-requests proposal's answer, apply, integrate and gate rounds, and ledger notes). The change outside `.shop/` is the same as in review 1.

## Range and work-items

- Range: `ae85edd3a2ce3488f4d930ac5814845eea5e6178..40b081a4e82d1f2370e922bfdff1b0a9e6383381`, on branch `main`.
- i60 (started, fulfils q39) holds:
  - work-item **w233** (green, under supervision, accepts supervision#r211, fileset `tests/scenarios/supervision_delegation_steps.py`). Its commits are `6b7926df`, `864da987`, `4aa66cd4`, `129a247c`, `9b49a82a`, `de6a60b1` and `91d43216` (the transitions) and `4e206ec4` (its only change, steps only).
  - capability-proposal **i60-supervision**: formulated, adds supervision#r211.
  - capability-proposal **i60-requests**: **awaiting-answer**, adds requests#r65–r71 (`work delegate`), with one gate question still open.
- Every other commit in the range is marked `none` (Finding 1).

## Suite

`Suite: 1069 passed, 0 failed at 40b081a4 in 33.34 s`. The run also had 1 skipped, 16 xfailed, 6 xpassed and 56 subtests passed, and it exited 0.

- **Parallel:** yes, `-n auto` (pytest-xdist).
- **In-process:** no. `tests/scenarios/conftest.py:33-34` runs each script as `subprocess.run([sys.executable, SCRIPTS/<script>, ...])`. The suite is under 60 s, so this is no finding.
- **Dry-run against real mode:** the system has no dry-run mode of an operation of its own. The only `--dry-run` in `scripts/` is `git push --dry-run`, used as a probe of git (`supervise_review.py:55`, `supervise_faults.py:71`). So no agreement test is owed.

## Checks

All runs are at `40b081a4`.

- **w233's check:** `w233.md` names no `check:` field. Its scenarios ran as `pytest -n auto -p work_items --work-item w233`: exit 0, `182 passed, 1 skipped, 56 subtests passed in 6.88s`. Both r211 examples (`[before]`, `[after]`) ran: the warnings name them.
- **tools check `== ruff ==`:** exit 1, two errors (Finding 4):
  - `tests/scenarios/test_supervision.py:14:1` I001;
  - `tests/scenarios/work_queue_list_steps.py:134:12` RUF015.
- **tools check `== vulture ==`:** clean.
- **tools check `== import-linter ==`:** "the project states no import contracts". No heading says `missing`.
- **tools size:** exit 0 and printed nothing. No tracked Python file is over 300 lines.
- **features deprecated:** exit 0, 19 deprecated scenarios.
  - The two r23 scenarios (deprecated in this range by `19c0bc4d`) name the r62 outline. That outline is still xfail ("accepted by work-queue, neither green nor withdrawn"), so its replacement is not green.
  - r34 and r35 (deprecated by `fe960a7a`) are "for: removal". w232 retires them and is awaiting-answer, not green.
  - `under a delegation, each question of the initiative ... <reply>` names "for: r209 and r210", and the run says "no scenario has that title". This predates the range: no commit in it touches that scenario.
  - No deprecated scenario has a replacement whose work-item is green.
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

- `tests/scenarios/requests_flow_steps.py:99` `show_prints` (i54/w232, `a5d6b59b`) is **loosened**. It used to assert that the whole output of `work show <request>` is `q1 delivered asker`, which proved that show prints a request's status and turn and nothing more. It now asserts only the first line. w232's plan lists it under "Tests the decisions break" (`.shop/work/i54/runs/w232/2-plan/plan.md:47`), so it is no finding.
- `tests/scenarios/work_queue_list_steps.py:56` `prints_question` (w232) moved from `parsers.parse` to an anchored `parsers.re`. Its assertion is unchanged; the longer `... and the answer "..."` form goes to the new step. It is not weakened.
- `features/work-queue.feature`: r23 ×2, r34 and r35 were tagged `@deprecated` by formulate rounds. None was removed.
- w233 (`4e206ec4`) removed and weakened nothing. The old Given `fulfils_with_delegation` (`supervision_delegation_steps.py:14-19`) keeps its anchored pattern and writes the same files through `start_i1` and `write_q1`. Its plan's "Tests the decisions break" is "None", and that holds.

## Allowances

- w233's report, `## Tests changed under an allowance`: "none". `4e206ec4` changes no `assert`, no expected value and no case. It holds.
- w232's report also says "none". Its only loosened test is in its plan's list, so no allowance is needed.

## Cannot verify

None. Every check comes from a run at `40b081a4`.

## Findings

### 1. Minor (observation): the range holds about 150 commits of no i60 work-item, because i60's branch is `main`
- **Work-item:** none in i60. The commits belong to i54, i55, i61 and i62, plus the q40 and q41 intake rounds.
- **Where:** brief `## Commits`, every line marked `none`.
  - The ones carrying code: `afc4aa72` (i54/w231, steps for r187) and `a5d6b59b` (i54/w232, `work show <request>`).
  - The ones changing `features/` are formulate-round commits, the workflow's own sanctioned way to add scenarios (supervision r83/r132): `698c1d44` (i60's r211), `bb2caae9` (r187), `fe960a7a` (r59–r61, r34 and r35 deprecated) and `19c0bc4d` (r62, r23 deprecated).
  - No work-item commit changes `features/`, so this is not Critical.
- **What is wrong:** base-to-head does not separate i60's work from that of the initiatives running alongside it.
- **Why it matters:** another initiative's fault (Findings 2, 4 and 6) holds i60's review, and the same finding can be drafted twice.
- **Fix:** give a branch review only the commits of the initiative's own nodes, or run each initiative on its own branch.
- **Reproduction:** brief lines 201–352 and 361–372 are all `none`. Only lines 353–360 are w233's.

### 2. Important (fix now): `work show <request>` leaves out every line of a request that has no line outcome yet
- **Work-item:** w232 (i54), commit `a5d6b59b`. It is already w232's open question (`.shop/work/i54/w232.md:14`), and w232 is awaiting-answer.
- **File:** `scripts/workqueue_list.py:86-88` (`request_parts`): `if outcome is not None:` prints a line only when it has an outcome.
- **What is wrong:** work-queue r59 asks show to print the request's "lines with their line outcomes". A request in the upstream's turn whose lines are not all settled shows fewer lines, or none. That is a wrong answer.
- **Why it matters:** whoever reads `work show q<n>` cannot see what was asked until every line has an outcome.
- **Fix:** print every line, with its outcome or a marker such as `no outcome yet`. Do this under w232 in i54, not as a new i60 work-item.
- **Test that would show it (not run):** `work show q1` where line 2 has no outcome, asserting that line 2 is printed.

### 3. Minor (observation): r211's `after` example does not tell a live read from a read at the first `work run`
- **Work-item:** w233.
- **File:** `tests/scenarios/supervision_delegation_steps.py:32-40` (`fulfils_with_delegation_given`).
- **What is wrong:** both commits, the start and then the delegation, land before `work run i1`. A copy of the delegation taken when the first `work run` starts would pass as well.
- **What I verified:** the read is live today. `supervise_answers.py` `Answers.delegation` re-reads the request on each call, as found in w233's review and branch review 1.
- **Why it matters:** a future cache of the delegation would not be caught.
- **Fix:** a scenario where the delegation is given or changed between two `work run`s. The plan and the report already name this as their open case.
- **Test that would show it (not run):**
  1. `work run i1` with q1 undelegated and w1 awaiting-answer.
  2. Commit a delegation on q1.
  3. `work run i1` again, and assert that the question went to a delegation session in that second run.

### 4. Minor (observation): `tools check` fails on two ruff errors, both older than the range, in files the range touched
- **Files and work-items:**
  - `tests/scenarios/test_supervision.py:14` I001 (touched by i54/w231, `afc4aa72`). The disorder is at lines 27-28 (`branch_steps` before `answers_steps`) and 41-42 (`review_steps` before `reintegrate_steps`), not at the added line 36 (`supervision_merge_steps`, which sorts correctly). This corrects review 1, which put the error on line 36.
  - `tests/scenarios/work_queue_list_steps.py:134:12` RUF015 (touched by i54/w232, `a5d6b59b`). Line 134 lies outside the change's hunk (new lines 53-117), so it predates the range.
- **Why it matters:** `tools check` exits 1 for every review on `main` until they are fixed.
- **Fix:** sort the import block (`ruff --fix`), and use `next(i for i in ... )` at line 134.
- **Reproduction:** brief `### tools check`: exit 1, with the two lines above.

### 5. Minor (observation): i60 cannot be done while its capability-proposal i60-requests is awaiting-answer
- **Work-item:** none (proposal i60-requests).
- **File:** `.shop/work/i60/requests.md:5`, `status: awaiting-answer`. Gate round 20 left one question open (whether r16 and r55 reach `work delegate`).
- **What is wrong:** under supervision r213 and work-queue r62/r47, i60 stays started even though w233 is green.
- **Fix:** answer the question under the delegation (it is not a glossary question), or withdraw the proposal.

### 6. Minor (observation): `work show <request> --json` gives none of what r59 lists
- **Work-item:** w232 (i54).
- **File:** `scripts/workqueue_list.py:102`: the JSON object is `{request, status, turn}` only.
- **What is wrong:** r38 read with r59 implies that the JSON form holds the lines, outcomes, questions, answers and resolution.
- **Fix:** add those fields, or write a line saying the JSON form gives status and turn only.
- **Test that would show it (not run):** `work show q1 --json` on the r59 fixture, asserting the lines and the resolution.

### 7. Minor (observation): 6 xpassed scenarios, not named in the suite's output
- **Work-item:** unknown. They are probably w232's r59–r61 scenarios, whose code is on `main` while w232 is not green.
- **What is wrong:** the run is `-rfEx`, so it names xfails but not xpasses. A scenario expected to fail that passes goes unreported, and the expected failures are not strict.
- **Fix:** make the `work_items` plugin's expected failures strict, or report X in the whole-suite run.
- **Test that would show it (not run):** the whole-suite command with `-rX`, naming the 6.

## Shape

- **CLAUDE.md size limit:** met. `tools size` printed nothing. `supervision_delegation_steps.py` has 258 lines.
- **Module map:**
  - `scripts/workqueue_list.py` ("`work list` and `work show <target>`"): `request_parts` (`:79-94`) is show's output for a request. Met.
  - `scripts/workqueue_request.py` ("the requests of a context"): `sections` (`:32-37`) reads a request's parts. Met.
  - `tests/scenarios/` ("one `<capability>_*_steps.py` module a concern"): `supervision_merge_steps.py` (r187, new) and `supervision_delegation_steps.py:14-40` (r211). Met.
- **Code no scenario reaches:** none found.
  - The old `fulfils_with_delegation` is reached by the r78, r210 and glossary scenarios and by `supervision_session_faults_steps.py`.
  - `write_q1`'s `delegation=None` is reached by the `after` example.
- **Code no line asks for:** none. w233 changes no production code. `request_parts` and `sections` serve work-queue r59.
- **Behaviour against Purpose:** nothing contradicts supervision's Purpose. The one contradiction of a line is Finding 2 (r59).

## Coupling

- **pytest-bdd on pytest internals.** `pytest_bdd/compat.py:28` calls `_fixturemanager._register_fixture` with a nodeid, and `FixtureDef` with a baseid. Neither is public pytest API: the run warns `PytestRemovedIn10Warning`, and both break under pytest 10. Fix: pin `pytest<10`, or move to a pytest-bdd release that passes `node`.
- **Unregistered marks.** Gherkin tags become `pytest.mark.<tag>` (`deprecated`, `r209`, `r210`, `r211`), and the run warns `PytestUnknownMarkWarning`. They would break under `--strict-markers`. Fix: register them in the conftest's `pytest_configure`.
- **git.** It is driven only through its CLI (`subprocess`), on published behaviour. Stable.

## Observations

- F1: brief `## Commits`. Every line but 353–360 is `none`, on branch `main`.
- F3: `supervision_delegation_steps.py:37-40`. Both commits come before `When the person runs work run i1`. Not run.
- F4: brief `### tools check`, exit 1: `test_supervision.py:14:1 I001` and `work_queue_list_steps.py:134:12 RUF015`.
- F5: `.shop/work/i60/requests.md:5`, `status: awaiting-answer`. Ledger line 8: "gate round 20: 1 question".
- F6: `workqueue_list.py:102`, where the JSON object is `{"request", "status", "turn"}` only. Not run.
- F7: brief, whole suite, "6 xpassed", with no XPASS line in the summary. Not run with `-rX`.
