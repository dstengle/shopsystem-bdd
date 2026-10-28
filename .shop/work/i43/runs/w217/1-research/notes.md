# research of w217 (supervision r154-r157)

Tools: plugin 0.28.1 `tools` (refs, size, check); `tools tests-of` has no map ("no map: make one with tools map"), so every test count below is `by search`.

## 1. Why each scenario is red today

None is red. Command, run once: `python3 -m pytest -q --work-item w217 -rfEx`.
Result (run): 187 passed, 1 skipped, 56 subtests passed, 0 failed.
`--work-item` keeps the scenarios tagged r154-r157 and every non-scenario test (r55), so the 187 includes unit tests.
Step definitions exist for all four (tests/scenarios/supervision_branch_steps.py:79-183).

The defect that w217 fixes is not covered by these scenarios (read):
- findings of branch review 1 (`.shop/work/i43/runs/branch-review/1/findings.md`), finding 1: r156 gives `none` for commits that `work answer`, `work withdraw`, `work retry` and `work add` make.
- `gives_work_items` (supervision_branch_steps.py:144) builds only `work: <name> ` subjects, so the gap passes unseen.

## 2. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_review_read.py:ReviewRead.commits_text, TRANSITION (line 11) | owner is the `work: <name> <a> -> <b>` subject, else `none` | r156: `work answer/withdraw/retry: <name> ...` and `work add: <i>/<name> drafted` belong to <name> | tests/scripts/test_supervise_review_read.py:test_a_proposals_transition_commit_belongs_to_no_work_item (by search); r156 steps via `work run` (by search) | refs TRANSITION (1 production ref); grep of scripts/ for `work answer:`, `work withdraw:`, `work retry:`, `work add:` (workqueue.py:105,217,242; workqueue_answer.py:74,76) |
| scripts/measure_build.py:81 and :88 (`work: <name> .*-> .*`, skip `work: ` subjects) | measure reads a work-item's transitions by the `work: ` subject | not changed by r154-r157; same subject assumption, and finding 1 proposes one shared pattern | none (by search: tests/scripts/test_measure_runs.py has no transition subject) | grep of scripts/ for `work: ` |
| agents/bdd-branch-reviewer.md:16 (`Read:` list) | names each implementer's `report.md` and `result.json`; no `findings.md` | r157: plan.md, report.md, findings.md per stage (read_text, supervise_review_read.py:61-63) | none (by search: tests/scripts/test_agents.py asserts no such text) | grep of agents/ for `result.json` |
| agents/bdd-branch-reviewer.md:25 | "A commit that belongs to no work-item is a finding", no exception for `work`'s own commits | r156 gives `none` for proposal rounds, `work note`, `work answer: <proposal>`, request and start commits | none (by search: test_agents.py) | grep of agents/ for "belongs to no work-item"; finding 4 (41 of 59 commits `none`) |

Outside the table, not w217's requirements: scripts/supervise_review.py:71-72 tells the reviewer to "run every command" (finding 2). That contradicts r32, which w217 does not accept.

## 3. Tests the requirements make impossible to keep

None. Method: `tests-of` has no map; searched tests/ by name for the functions in part 2 and for the r154-r157 steps (by search).
- tests/scripts/test_supervise_review_read.py:test_a_proposals_transition_commit_belongs_to_no_work_item (lines 25-33): read. Its commits are `work: supervision approved -> awaiting-answer` (name not an item, so `none`) and `work: w1 ready -> claimed`. Both still give their expected owners under the widened pattern. Sound.
- tests/scenarios/supervision_branch_steps.py r156 steps (lines 134-165): read. Their `work:` and `notes.txt` lines are unchanged by the fix. Sound.
- r154 and r155 steps (lines 79-131) and r157 steps (168-183): read. Their code (branch_runs, read_text) is not changed. Sound.
- tests/scripts/test_work_items_worker.py:28-33 (`test_the_branch_review_runs_the_whole_suite`): by search, runs the plugin's whole-suite gate; unaffected.
Not run: no test of the fixed pattern exists yet; the fix's unit cases would be new.

## 4. The file set

Production:
- scripts/supervise_review_read.py: widen TRANSITION (line 11) to `work answer/withdraw/retry` and `work add: <i>/<name> drafted`, keep the owner check at line 42. Shown by refs TRANSITION and the grep in part 2.

Tests:
- tests/scripts/test_supervise_review_read.py: add cases: `work answer: w1 awaiting-answer -> ready`, `work withdraw: w1 ready -> withdrawn`, `work retry: w1 failed -> ready`, `work add: i1/w1 drafted`, each expecting `w1`. Shown by read of the file and of workqueue.py:105,217,242.

Not in the file set, with readings:
- features/supervision.feature: a scenario row for these commits would change a formulated scenario and needs a formulate round first (requests-only-propose). Reading A (recommended): unit cases only, inside this file set. Reading B: a scenario row, through a spec round first.
- scripts/measure_build.py: shared subject pattern (finding 1). Not required by r156; out of this file set.
- agents/bdd-branch-reviewer.md:25 exception (finding 4): not fix-now in the findings file; out of this file set.

Modules on the change's path, with lines and room under the 300 limit (CLAUDE.md gives it; `tools size --limit 300` printed nothing, so no file is over):
- scripts/supervise_review_read.py: 64 lines, room 236 (edited).
- tests/scripts/test_supervise_review_read.py: 33 lines, room 267 (edited).
- scripts/supervise_review.py: 99 lines, room 201 (calls commits_text, line 77; not edited).
- scripts/supervise_branch_runs.py: 51 lines, room 249 (provides `indented`; not edited).
- scripts/workqueue.py: 294 lines, room 6 (writes the subjects; not edited; any change here has 6 lines).
- scripts/workqueue_answer.py: 77 lines, room 223 (writes `work answer:` subjects; not edited).
- scripts/measure_build.py: 143 lines, room 157 (not edited).
- tests/scenarios/supervision_branch_steps.py: 183 lines, room 117 (not edited).
- agents/bdd-branch-reviewer.md: 77 lines (markdown; no line limit applies).
