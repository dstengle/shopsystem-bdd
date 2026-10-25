# research of w194

Accepted: supervision#r120 (scenario "under a delegation, the session answering ... says whether ... change or accepts"), supervision#r121 (Outline "a kept branch review whose result gives <outcome> and no question ...", 4 rows).
Scripts used: worktree `scripts/` (conftest's SCRIPTS). `tools` has no map: `tests-of` says "no map", so every test list below is `by search`; `refs` reports 0 for `self.method` calls (it missed `self.lists_nothing`, `self.answer_brief`), so those are `by search`.
Shell env carries `--work-item w194` (PYTEST_ADDOPTS), so default collection keeps only the 5 accepted tests; the deprecated/other tests were run with `--whole-suite`.

## 1. Why each scenario is red today

- r121 Outline, all 4 rows (DONE, PARTIAL, BLOCKED, NEEDS_CONTEXT): `python3 -m pytest -q -rfEs "tests/scenarios/test_supervision.py::test_a_kept_branch_review_whose_result_gives_outcome_and_no_question_..._[<row>]"` (run). Fails at the Given: `StepDefinitionNotFoundError: every worker gives DONE, and the branch reviewer's result gives <row>, with no question`. Only defined step is `tests/scenarios/supervision_analysis_steps.py:37` ("gives PARTIAL, with no question and no finding", used by the deprecated r75 scenario). Missing: a parameterised Given for `<outcome>, with no question` setting `plan["bdd-branch-reviewer"] = {"status": <outcome>, "questions": []}`.
  - Code behind it, once the step exists (read): `scripts/supervise_analysis.py:19-26` `Analyses.lists_nothing` returns True only when `status == "DONE"` and `questions` is empty. So PARTIAL/BLOCKED/NEEDS_CONTEXT with no question give False: no `measure initiative`, which is the Then's failure (the deprecated PARTIAL test shows this path today, see §2). DONE row would pass once the step exists.
  - Called at `scripts/supervise.py:222` (`pull_through`), r75/r76 gate.
- r120 scenario (run): `StepDefinitionNotFoundError: Then "the brief of the session answering "Is the old reader kept?" asks it to give in its result whether its answer asks for a change or accepts w1 as it is"`. Missing: that Then. It belongs in `tests/scenarios/supervision_delegation_steps.py`, using its `given_to(repo, question)` helper (line 139) and asserting the brief names `verdict`, `change`, `accept`.
  - Code (run, function-level probe §2): `scripts/supervise_answers.py:127-143` `Answers.answer_brief` already appends the verdict ask (`VERDICT`, line 17) when the brief's `Reviewer` flag is set. No code change looks needed for r120; the red is the missing Then only.

## 2. What the system answers today

Probe file: `.shop/scratch/w194-1-research/probe_review_answers.py`, run `python3 -m pytest -q -s -n 0 .shop/scratch/w194-1-research/probe_review_answers.py`. The functions are called directly on files it writes; not through `work run`.

- `Analyses.lists_nothing(None, dir)` on `result.json` (run):
  - DONE, [] → True
  - PARTIAL, [] → False
  - BLOCKED, [] → False
  - NEEDS_CONTEXT, [] → False
  - PARTIAL, no questions key → False
  - DONE, no questions key → True
  - DONE, questions null → True
  - DONE, questions "" → True
  - DONE, one question → False
  - PARTIAL, one question → False
  - DONE, questions as one string "Is X kept?" → False
  - JSON list, not object → False
  - malformed JSON → False
  - no result.json → False
- `Answers.answer_brief` (run): reviewer question (Reviewer=yes) → brief contains "also give `verdict`, `change` when the answer asks for the work-item to be changed, `accept` when it takes the work-item as it is". Ordinary question → no verdict ask.
- `workqueue_answer.asked_by_reviewer` on a log whose last move is done→awaiting-answer (run) → True.
- Deprecated and measurement tests, through `work run` with the stub, `python3 -m pytest -q -n 0 -rfEs --whole-suite "<node id>"` (run), all 4 pass today:
  - `test_a_kept_branch_review_that_ended_partial_with_no_question_and_no_finding_does_not_list_nothing_to_fix_now_..._deprecated` (features/supervision.feature:1050): PARTIAL, no question → no `measure initiative`. This is the existing way for a non-DONE review.
  - `test_when_every_workitem_is_green_or_withdrawn_..._deprecated` (DONE, nothing to fix) → measured.
  - `test_an_initiative_with_no_workitem_is_not_measured` → not measured.
  - the outline row "w1 is green and w2 is withdrawn / is measured" → measured.
- Nearest cases the scenarios do not give, by reading the function (read): a review whose result.json is missing or not an object is treated as not listing nothing (the probe above shows False). This is the reading that keeps an unreadable review from the gate; r121 does not say it.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_analysis.py:Analyses.lists_nothing (lines 19-26) | True only for status DONE and empty `questions` | r121: status is ignored; only the absence of a question counts. The condition `status == "DONE"` must go | by search: DONE-with-nothing scenarios in test_supervision.py (the r121 DONE row; r75 deprecated DONE; analysis/record scenarios 1088-1103, 1439-1474 via `reviewer_lists_nothing`); the deprecated PARTIAL test (passes today) | grep "lists_nothing" (refs 0, method call); its docstring |
| scripts/supervise_analysis.py:Analyses.lists_nothing docstring (line 21) | says a review that ended any other way lists nothing "no more than one with findings" | states the old rule; rewrite with r121 | none (docstring) | read |
| scripts/supervise.py:Run.pull_through line 222 | calls lists_nothing; if True, analyse() then set_done() | call unchanged, but PARTIAL/BLOCKED/NEEDS_CONTEXT reviews without questions now reach analyse and set_done | by search: the same measurement scenarios; the deprecated PARTIAL test (fails after r121) | grep lists_nothing |
| scripts/supervise_done.py:set_done (r105/r109) | no review-status check of its own; relies on the gate upstream | a non-DONE review with no question now reaches it when the other r105 conditions hold | by search: the r105 deprecated "is set done" test (not run) | read: called only from supervise.py:224 |
| scripts/supervise_analysis.py:Analyses.analyse | runs measure, the analysis session, commits the record | reached now for non-DONE reviews | by search: supervision_analysis_steps.py scenarios | read |
| scripts/supervise_draft.py:Drafts.fix_work_item (58-81) | drafts a fix from `questions` only; no status check | consistent with r121 (a question still means fix), no change | by search: supervision_proposal_steps.py findings scenario | read |
| scripts/supervise_review.py:Reviews.branch_review (35-82) | writes a brief asking PARTIAL first; keeps the directory whatever the status | consistent with r121, no change | by search: supervision_review_steps.py | read |
| scripts/supervise_answers.py:Answers.answer_brief (127-143) and ask() (99-125) | reviewer questions carry a verdict ask and need a verdict | r120 already satisfied (run: probe above); no change | tests/scripts/test_supervise_answers.py::test_a_reviewers_item_..._no_verdict_... (run, passed); the r120 Then is undefined | grep VERDICT |

## 4. Tests the requirements make impossible to keep

`tools tests-of` has no map, so this list is `by search` (grep for "lists nothing", "PARTIAL", "gives PARTIAL" in features and tests).

- tests/scenarios/test_supervision.py::test_a_kept_branch_review_that_ended_partial_with_no_question_and_no_finding_does_not_list_nothing_to_fix_now_..._deprecated (feature line 1050; step supervision_analysis_steps.py:37-40): passes today (run). Asserts PARTIAL with no question is not measured. r121 makes it fail. Mechanism: lists_nothing's status check. Note: it is tagged `@r75 @deprecated`, so `supervise_draft.py` r73 Retires rule (matches `@r<n>` on requirements the work-item accepts: r120, r121) will NOT list it in w194's `## Retires`. Its own "Deprecated for" line names the r121 outline. The plan must choose: retire it by hand, or leave it failing. Both readings are open.
- Every other test that uses reviewer_lists_nothing (DONE) still passes under r121 (read; the DONE row of the r121 Outline is the same behaviour).
- Tests for r118/r119 reviewer answers (supervision_delegation_steps.py, tests/scripts/test_supervise_answers.py): read: unaffected by r120 (the brief already asks for a verdict; ask() unchanged). The test_supervise_answers unit test passed (run).
- No test asserts the absence of a verdict ask in a reviewer brief (grep "verdict" in tests: only test_supervise_answers.py and r120's Then, which is undefined).

## 5. A step the work-item skips

- r121 skips the DONE check that the gate makes today. Refusals/effects only that check produces (run, via the deprecated PARTIAL test, passes today): a non-DONE review with no question produces no `measure initiative`, no analysis session, no record, and no done. After r121, those effects appear for PARTIAL, BLOCKED and NEEDS_CONTEXT too (read: supervise.py:222-224). The existing non-DONE handling for workers (r5, r45: awaiting-answer or failed) has no counterpart for reviews (read: supervise_review.py has no outcome check).
- r120 skips no step: a reviewer session that gives no verdict is left for the person (read: supervise_answers.py:122-123; run via the unit test).

## 6. Defects

None shown by a probe. Probes run: §2 (lists_nothing, answer_brief, asked_by_reviewer) and the deprecated/measurement tests. No crash, no wrong landing found.

## 7. The file set

Production:
- scripts/supervise_analysis.py: drop the `status == "DONE"` condition from `lists_nothing` (r121); rewrite its docstring (line 19-21). Found by: grep lists_nothing; probe §2.

Tests:
- tests/scenarios/supervision_analysis_steps.py: add the parameterised Given "every worker gives DONE, and the branch reviewer's result gives <outcome>, with no question" for the four rows (r121). Found by: StepDefinitionNotFoundError run; file is 97 lines.
- tests/scenarios/supervision_delegation_steps.py: add the Then "the brief of the session answering "<q>" asks it to give in its result whether its answer asks for a change or accepts <w> as it is" (r120), using `given_to`; asserts the brief text. Found by: StepDefinitionNotFoundError run; file is 202 lines.
- The deprecated PARTIAL scenario (features/supervision.feature:1050 and its step at supervision_analysis_steps.py:37-40): must be retired by the plan or left failing; the step is needed only by it. Found by: run §4.

Not changed (checked): scripts/supervise_answers.py (already asks for the verdict; r120 needs no code), scripts/supervise.py (call site unchanged), scripts/supervise_done.py, scripts/supervise_review.py, scripts/supervise_draft.py, tests/scenarios/test_supervision.py (binds the feature; no change).

Modules on the change's path (line count from `wc -l`; room under 300, the CLAUDE.md limit):
- scripts/supervise_analysis.py: 80 lines, room 220 (edited)
- scripts/supervise.py: 271 lines, room 29 (on the path, line 222; not edited)
- scripts/supervise_done.py: 36 lines, room 264 (on the path, set_done; not edited)
- scripts/measure (entry), 97 lines; measure_write.py 41; measure_build.py 143 (run by analyse; not edited)
- scripts/supervise_review.py: 82 lines, room 218 (on the path; not edited)
- scripts/supervise_draft.py: 81 lines, room 219 (on the path; not edited)
- scripts/supervise_answers.py: 144 lines, room 156 (r120's brief; not edited)
- scripts/supervise_brief.py: 167 lines, room 133 (routes the answer brief; not edited)
- scripts/workqueue_answer.py: 77 lines, room 223 (asked_by_reviewer; not edited)
- scripts/supervise_worker.py: 251 lines, room 49 (worker session; not edited)
- tests/scenarios/supervision_analysis_steps.py: 97 lines, room 203 (edited)
- tests/scenarios/supervision_delegation_steps.py: 202 lines, room 98 (edited)
- tests/scenarios/test_supervision.py: 261 lines, room 39 (binds the feature; not edited)

Size check: `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` printed nothing (run; no tracked Python file over 300).
Scratch: `.shop/scratch/` is git-ignored (`git status --porcelain --ignored` shows `!!`), so `git status --porcelain` is clean.
