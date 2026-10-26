# notes: w198 research (i37, supervision)

Tools: `tools` present. No coverage map (`.shop/scratch/tools/coverage` absent), so `tests-of` and `untested` were not used; counts are `by search`. `refs` used for module-level names; methods (`self.x`) by Grep.

## 1. Why each scenario is red today

None is red. All 11 accepted test ids pass.
Run: `python3 -m pytest -q -rfEs --tb=short` on the 11 node ids of `tests/scenarios/test_supervision.py` → `11 passed` (run).

- r121 Outline, DONE / PARTIAL / BLOCKED / NEEDS_CONTEXT: 4 cases pass (run). Code: `scripts/supervise_analysis.py:lists_nothing` (19), called at `scripts/supervise.py:226`.
- r75 deprecated, "measure initiative is run": passes (run).
- r75 Outline, measured / not measured: 2 cases pass (run). Code: `supervise.py:226-227`, `supervise_analysis.py:analyse` (36).
- r105 deprecated, "is set done": passes (run).
- r105 Outline, is set done / is not set done: 2 cases pass (run). Code: `supervise_done.py:set_done` (27), `workqueue_done.py:_holds` (22, the "at least one green" test at 31).
- r120: passes (run). Code: `supervise_answers.py:VERDICT` (17-18), appended to the brief at 143 when reviewer. Its Then, `brief_asks_verdict`, is a substring check (read).

## 2. What the system answers today

Probes run through `scripts/work run i1` with the stand-in claude; repositories built under the scratch directory (`.shop/scratch/w198-1-research/`); checkout git status unchanged.

- P-A `python3 -m pytest -q -s -n 0 .shop/scratch/w198-1-research/probe_review.py::test_second_run_after_analysis_cut_short` (run).
  First run: review kept, `measure initiative` writes the measurement, the analysis session ends at its turn limit; stderr "cut short, so there is no analysis record"; exit 0; i1 `started`.
  Second run, same state: no worker starts, no measurement, no analysis; exit 0; i1 `started`.
- P-B `probe_review.py::test_review_question_given_as_one_string` (run). Review result `questions` = one string "Is the old reader kept?".
  Kept result.json holds the string; no fix work-item; no measurement; no record; exit 0; i1 `started`.
- P-C `probe_fix.py::test_review_question_naming_w1_as_a_list` (run). `questions` = ["w1 needs a fix: feature.txt is missing"].
  Killed by the 300 s timeout. Left behind: 198 `runs/branch-review/` directories, 198 drafted fix work-items, 197 of them `done`, each a review's fix. No bound on the loop.
- P-D `probe_fix.py::test_review_question_naming_w1_as_one_string` (run). Same question as one string.
  No fix drafted; no measurement; exit 0; i1 `started`.

Nearest cases, not probed (read):
- Review leaves no readable result: `lists_nothing` returns False; no measure, no done, exit 0 (`supervise_analysis.py` 23-26).
- Reviewer's question answered with no `verdict`: `supervise_answers.py:ask` returns None, the question is left for the person (121-124).
- Answer "accepts" by a reviewer session without a verdict: same as above.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| supervise.py:pull_through, 218-228 | `kept` is this run's review; `None` (no unread commit) skips measure and done | r75, r105: measure and done whenever the kept review lists nothing; a later run gets no measure or done | none for the `None` branch (by search: the three `a second time` scenarios, features lines 946, 959, 1252, not read) | read; probe P-A |
| supervise.py:pull_through, 220-225 | `while` over `fix_work_item` and `branch_review`, no bound | r74, r110: a fix is pulled and reviewed again; nothing bounds it | none (by search: the r74 and r110 scenarios, not read) | read; probe P-C |
| supervise_analysis.py:lists_nothing, 19-26 | a string `questions` is a question; missing or malformed result is "not nothing" | r121: no question means nothing to fix, whatever status | the 4 r121, 2 r75 and 2 r105 cases (by search: they reach it through `pull_through`) | read; probe P-B |
| supervise_draft.py:fix_work_item, 106-107 | returns False unless `questions` is a list | implementation note: a one-string `questions` is one question | none (by search: no test gives a branch review a one-string question) | read; probe P-D |
| supervise_answers.py:ask, 119-124 and VERDICT 17-18, 143 | a reviewer's answer needs `verdict`; without it the question stays for the person | r120: the session says change or accept; r119, r118 | r119 and r120 scenarios (by search, the delegation tests) | read |
| workqueue_answer.py:asked_by_reviewer, 24-28 and reviewer_status, 31-33 | a reviewer's question is one whose last move to awaiting-answer came from `done` | r118, r119: verdict moves the item to `ready` or `done` | r118, r119 scenarios (by search) | read |

## 4. Tests the requirements make impossible to keep

None of the 11 accepted tests can fail on the requirements: each passes today (section 1). The work-item's retirements remove two accepted deprecated tests; both pass today and go with their scenarios (intended, not a break):
- `tests/scenarios/test_supervision.py::test_when_every_workitem_..._deprecated`
- `tests/scenarios/test_supervision.py::test_an_initiative_whose_workitems_are_green_or_withdrawn_..._deprecated`

Other retired scenarios (not accepted here, not run): `features/migration-tools.feature:311` (@r15), `features/work-queue.feature:5, 69, 280` (@r1, @r23, @r9), `features/supervision.feature:1411` (@r102). Their generated tests go with them (by search).

Sound (read): `tests/scenarios/test_supervision.py` (scenarios generated from the feature file, so removal drops the test without a code edit); `tests/scenarios/supervision_done_steps.py`, `supervision_analysis_steps.py`, `supervision_delegation_steps.py`: their steps are shared with live scenarios (`i1 is done`, the r105 Outline; the `measure initiative` Then, the r75 Outline), so nothing becomes unused. `tests/scripts/test_bound.py` checks every scenario of the bound feature files has exactly one test; removing a scenario with its test keeps it green (read).

## 5. A step the work-item skips

None. The work-item adds no path; it removes scenarios.

## 6. Defects

### D1: a branch review's fix loop has no bound (P-C)
Reproduce: `python3 -m pytest -q -s -n 0 .shop/scratch/w198-1-research/probe_fix.py::test_review_question_naming_w1_as_a_list`.
Came back: `TimeoutExpired` after 300 s. Left behind 198 review directories and 198 fix work-items, each `done` in the log but for one; the stand-in reviewer always names w1.

### D2: a one-string `questions` naming a work-item is dropped (P-D; P-B)
Reproduce: `probe_fix.py::test_review_question_naming_w1_as_one_string`. Same repository, the question as a list (D1) drafts fixes; as one string: no fix, no measure, no record; exit 0; i1 `started`. The implementation note says a one-string `questions` is read as one question.

### D3: a cut-short analysis is never retried (P-A)
Reproduce: `probe_review.py::test_second_run_after_analysis_cut_short`. After the first run's analysis turned out cut short, the second run starts no analysis and no measure; i1 stays `started`, exit 0. The review is kept, lists nothing and w1 is green, so r75 and r105 are met.

## 7. The file set

Python: none to change. `tools size --limit 300` prints no file over 300 (run), so no split is forced.

- `features/supervision.feature` (1563 lines): remove the deprecated r75 (line 1089), r102 (1411), r105 (1485) scenarios. Found by `grep @deprecated features/`.
- `features/migration-tools.feature` (584 lines): remove the deprecated r15 scenario (line 311). Same grep.
- `features/work-queue.feature` (480 lines): remove the deprecated r1 (line 5), r23 (69), r9 (280) scenarios. Same grep.

Modules on the change's path (edited or not):
- `scripts/features_edit.py`: 131 lines, room 169 under 300. The `retire` command lives in the `features` command (`scripts/features*.py`); I did not read its retire code, so "the path" is not verified beyond that.
- `tests/scenarios/test_supervision.py`: 262 lines, room 38. Not edited; its scenarios come from the feature file.
- `tests/scripts/test_bound.py`: not edited; under 300 (no output from `tools size`).

The deprecated scenarios of the file set are the ones `features retire` removes; the work-item's `Retires` section names them.
