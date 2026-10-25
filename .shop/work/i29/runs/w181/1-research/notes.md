# w181 research notes

Method: `tools map` has no map, so `tests-of` and `untested` could not run: tests are found by search. `tools refs` misses calls through `self.` and module attributes (0 refs for `becomes`, `write_proposals`, `analyse`, though each is called): counts for those are by search. Scenario runs use node ids from `--collect-only`. The shell's PYTEST_ADDOPTS carries `--work-item w181`, so a selection with no accepted scenario is refused (`scripts/work_items.py:109`), and `-p no:work_items` is refused as an argument.

## 1. Why each accepted scenario is red today

Command for each: `python3 -m pytest -q -p no:warnings --tb=short <node id>`. pytest-bdd stops at the first undefined step, so later steps are listed by search only.

- r107, "a change list naming a capability ... gives no capability-proposal ... exits with an error naming it" (`tests/scenarios/test_supervision.py::test_a_change_list_naming_...`). Run: `StepDefinitionNotFoundError` on Given "spec/capabilities/ holds no capability nowhere" (feature line 1319). By search, no step matches the integrate Given at line 1320 (`supervision_integrate_steps.py:41,56` require "on thing"), nor the Thens at 1323-1325. Code: `supervise_change.py:write_proposals` (38-52) and `supervise_change.py:entries` (13-32) check no capability exists; `supervise_rounds.py:run_round` (96-109) passes the entries on. Nothing raises for an unknown capability.
- r108, Outline "the <kind> round ... is given the path of the kept drafts" (two examples: gate, apply). Run both: `StepDefinitionNotFoundError` on Given "p1 was written from the change list of i1's integrate round, whose drafts are kept at .shop/work/i1/runs/i1/2-integrate/drafts/round-1/" (line 1331). By search: the gate Given "i1's capability-proposal p1 is drafted" exists (`supervision_rounds_steps.py:27`). The apply Given (awaiting-answer with ## Questions and ## Answers) has no exact match (`supervision_given.py:247` and `supervision_all_steps.py:90` differ). Missing in code: `supervise_brief.py:brief` (21-71) gives gate and apply rounds no drafts path. Only `integrate_lines` (73-86) writes "Drafts path:".
- r106, "once the measurement and analysis record are written, they are committed" (line 1343). Run: `StepDefinitionNotFoundError` on Then "the initiative branch has a commit of i1's measurement and i1's analysis record" (line 1348). By search: no step for "nothing under .shop/records/ is left uncommitted" (line 1349; `supervision_rounds_steps.py:154` is for `.shop/work/`). Missing in code: `supervise_analysis.py:analyse` (36-74) copies the record to `.shop/records/<date>-<i>-analysis.md` with no `git add` or commit. `supervise.py:pull_through` (202-213) calls `analyse()` and nothing commits. `supervise.py:commit` (98-109) is used for work-item moves only.
- r105, "... is set done" (line 1352). Run: `StepDefinitionNotFoundError` on Given "i1 is started and its work-items w1 is green and w2 is withdrawn" (line 1354). The near match `supervision_proposal_steps.py:37` says "i1's work-items w1 is green, part of the capability-proposal p1, and w2 is withdrawn". By search, the q2 Given (`work_queue_start_steps.py:22` takes only "q1") and the Then "i1 is done" have no step. Missing in code: `supervise.py:pull_through` never calls `workqueue_done.becomes` or `mark` for done. `workqueue_done._holds` (22-38) counts work-items and requests only, not the branch review or the analysis record.
- r109, "an initiative set done is committed" (line 1361). Run: same first undefined Given as r105. By search, the Then "the initiative branch has a commit of i1 with its status done" has no step. Missing in code: `workqueue_done.mark` (51-56) writes the file only. The command path commits it (`workqueue.py:242-252` `moved_to` adds initiative.md to the commit). The run path does not.

## 2. What the system answers today

Probe file: `.shop/scratch/w181-1-research/probe_supervision.py`, run with `python3 -m pytest -q -s -n 0 -p no:warnings .shop/scratch/w181-1-research/probe_supervision.py`. It calls the functions directly in a scratch repo with `spec/index.md`; it does not drive `work run`, because the scenario harness builds that repository. Treat these as function-level `run`.

- P1 `entries({"changes":[{"capability":"nowhere","adds":["nowhere#r1"],...}]})` gave `[{'capability': 'nowhere', ...}]`. `Changes.write_proposals` in a scratch `.shop/work/i1` wrote `.shop/work/i1/nowhere.md`, `status: drafted`, with `spec/capabilities` absent. No error. Nearest case not run: a capability held only in the round's drafts (read: `kept_drafts` globs `runs/*-integrate/drafts/round-*/spec/capabilities/*.md`, `supervise_drafts.py:16-19`).
- P2 `workqueue_done._holds(root, i1, "initiative/<ctx>/i1", {})` with w1 green, w2 withdrawn, q2 delivered (asker internal), no branch review and no analysis record: returned `True`. With w2 overridden to started: `False`. So the condition for done lacks the branch-review and analysis conditions of r105. Read: with no work-items it returns `False` (empty `statuses`); with a request not delivered it returns `False`.
- Nearest case not probed: the request kept but its asker external (read: `_holds` ignores it, `mine` is False).

## 3. Old assumptions

`becomes`, `_holds` and `mark` are shared by the command path and the request path, so changing them changes both.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_done.py:_holds (22-38) | done condition: work-items green/withdrawn and requests delivered | r105 adds branch review and analysis for `work run` only. Widening it also changes the command path (work-queue r23) | by search: tests/scenarios/test_work_queue.py and work_queue_*_steps.py (not run, see notes below) | refs (`becomes`), read |
| scripts/workqueue_done.py:becomes (41-48) | done flag for a move | callers: workqueue.py:245 (moved_to, command moves), workqueue_request.py:174 (resolve delivered). Unchanged unless `_holds` changes | by search: as above | refs found 0 callers, search found 2 |
| scripts/workqueue.py:moved_to (242-252) | commits initiative.md with a done move | the run path does not use it; r109 needs the same commit | by search | refs |
| scripts/workqueue_request.py:174-179 | resolve sets request delivered, then done | unchanged | by search | search |
| scripts/supervise.py:pull_through (202-213) | after lists_nothing: analyse(), no done | r105: set done after analysis is committed; r106: commit | none | read |
| scripts/supervise_analysis.py:analyse (68-70) | copies record into .shop/records, no git | r106: commit with the measurement | by search: tests/scenarios/supervision_analysis_steps.py (analysis_there, analysis_not_there) | read |
| scripts/supervise_change.py:write_proposals (38-52) | writes one drafted proposal per entry, no check | r107: refuse a capability neither spec/capabilities nor the drafts have | none verified (no map); by search: supervision_integrate_steps.py | read, run (P1) |
| scripts/supervise_change.py:write_proposals body (48-50) | "The drafts of this proposal are in <stage dir>" | r108: drafts path is the integrate round's drafts/round-N, not its stage dir | none | read |
| scripts/supervise_brief.py:brief gate/apply (40-46) | gate asks by adds/changes/removes; apply has none of its own | r108: give gate and apply the drafts path | none verified | read |
| scripts/supervise_brief.py:brief read list (31-32) | reads runs/<proposal> dirs only | the integrate stage dir is not in it; r108 needs it | none verified | read |
| scripts/supervise_rounds.py:start_initiative (118-123) | mark to started | unchanged | by search | read |

## 4. Tests the requirements make impossible to keep

No map, so no `tests-of` list. Found by search and not run; the one run is marked.

- tests/scenarios/test_work_queue.py, Outlines and scenarios named "...sets the initiative to done" (features/work-queue.feature:57, :75): their initiative is done with no branch review or analysis record. Widening `_holds` for r105 would make them fail unless the run-only condition is a separate function. Not run: the shell's PYTEST_ADDOPTS `--work-item w181` refuses a selection with none of its scenarios. Verdict: at risk if `_holds` changes; sound today by read only.
- features/supervision.feature:1173 names `other#r1 on other`. Whether `other` is held by spec or drafts in its Givens is not verified. Under r107 it must be. Verdict: unverified.
- Scenarios whose integrate change lists name `thing` (features :1159, :1183): `thing` is held in spec or drafts in their Givens (`supervision_integrate_steps.py:63`, `:137`). By read, sound.
- No test asserts the old uncommitted-record state or "no done after run": none found by search of `records` and `done` in tests/scenarios (the `i1 is done` search had only design-model-check and migration hits).

## 5. A step the work-item skips

- The commit of the measurement and record (r106). The existing way is `supervise.py:commit` (98-109): `git add`, `git commit`, then `push()` (r38). `analyse()` skips all three. Effects only that step produces: a commit under `GitFailed` refusal (`supervise_worker.git`), a push, and the log reset (`unlogged`, `own`). Read.
- The set-done commit (r109). The existing way is `workqueue.moved_to` (242-252), through `committed` with initiative.md in the rels. The run path skips the commit and the push. Effects: no push of the done state (r38). Read.
- Check that the run path's done is taken after the analysis record is committed: the new step must read the commit, not the file. Read.

## 6. Defects

- Today a change list that names a missing capability gets a `drafted` proposal with no error (P1). Reproduce: `python3 -m pytest -q -s -n 0 -p no:warnings .shop/scratch/w181-1-research/probe_supervision.py::test_r107_unknown_capability_gets_a_proposal`. This is the behaviour r107 forbids. I do not judge the plan.
- The analysis record lands in `.shop/records/` uncommitted, and the start-of-run check looks only at `.shop/work/` (`supervise.py:check`, 72-90). So an uncommitted record survives a run without a refusal. Read.

## 7. The file set

Production files (scripts/):
- supervise_change.py (52 lines, room 248): check each name against spec/capabilities and the round's drafts; r107 error naming it. Found by read and P1.
- supervise_rounds.py (134, room 166): `run_round` raises Refused naming the capability (r107) before the write and keeps the status (r86-88). Read.
- supervise_brief.py (162, room 138): drafts path for gate and apply (r108); read list adds the integrate stage dir. Read.
- supervise_analysis.py (74, room 226): commit the measurement and the record (r106). Read.
- supervise.py (260, room 40): after analyse, the done transition and its commit (r105, r109). Tight: a helper module may be needed. Read.
- workqueue_done.py (67, room 233): a run-path done condition (branch review, analysis record) kept apart from `_holds` (r105). Read, P2.
- Read only, not edited unless `_holds` changes: workqueue.py (290, room 10), workqueue_request.py (181, room 119), supervise_drafts.py (room unknown: not counted), supervise_worker.py (247, room 53), supervise_draft.py (81, room 219).

Test files (tests/scenarios/, step definitions are missing):
- supervision_integrate_steps.py (190, room 110): steps for r107 and r108's drafts Givens. Found by search.
- supervision_analysis_steps.py (83, room 217): r106 and r105 steps (commit Then, "i1 is done"). Found by search.
- supervision_proposal_steps.py (116, room 184): r108 gate/apply Givens. Found by search.
- supervision_given.py (259, room 41): apply Given (r108 awaiting-answer) if it fits. Found by search.
- test_supervision.py (259, room 41): the bindings; no change expected. Found by read.
- A new steps module if these pass 300 lines.

Modules on the path, not edited: scripts/supervise_all.py (83), scripts/supervise_review.py (82), scripts/workqueue.py (290), scripts/workqueue_request.py (181). `tools size --limit 300` printed nothing: no tracked Python file is over the limit.

Git state at the end: `git status --porcelain` empty (scratch and stage dir ignored).
