# Research of w236 (supervision#r218)

Tools: no map (`tools tests-of` and `refs` answer "no map" / 0 refs for method calls); counts below are by search and by read.

## 1. Why each scenario is red today

Accepted scenario: features/supervision.feature:2021 (r218, put-back of an uncommitted `.shop/work/` change, less another initiative's path).

Command, run once: `python3 -m pytest -q --work-item w236`
Result: 1 failed, 180 passed, 1 skipped, 56 subtests passed (run).

- Failure (run): `StepDefinitionNotFoundError` for the Given at features/supervision.feature:2025: "every round ends and every worker gives DONE, and while i1's researcher works another session changes .shop/work/i1/initiative.md and a session of i2 changes .shop/work/i2/initiative.md, both ... without committing them". Steps at 2023 and 2024 matched.
- Missing step definition (run, and read): the Given. The existing `another_session_changes` (tests/scenarios/supervision_faults_steps.py:42) covers i1's path only; `every round ends` (supervision_rounds_steps.py:122) does not carry the "while ... works" clause.
- Missing step definition (search, not reached by the run): the Then "nothing recorded of w1 names .shop/work/i2/initiative.md". No match in tests/ by search.
- Behaviour behind the Given (read): scripts/supervise_faults.py `Faults.checkout_changes` (104-125) skips only `run.own` run directories and log lines of the group. It does not skip `.shop/work/i2/initiative.md`, so i2's change is put back and listed as changed. It is then called by scripts/supervise_worker.py `Run.worker` (189), which raises one Fault naming every changed path (197-199). Expected, by read: w1's Faults names i2's path too, failing the last Then.
- Group: scripts/supervise.py:65 sets `self.group`; the comment says supervise_all shares it (supervise_all.py not read).

## 2. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_faults.py:Faults.checkout_changes (104-125) | puts back every `.shop/work/` path differing from HEAD, except own run dirs and log tails of the group | must skip each path under `.shop/work/<initiative>/` of another group initiative (r214, r218) | none by search beyond the scenario steps (no map) | read; grep `checkout_changes` |
| scripts/supervise_worker.py:Run.worker (169-199) | calls checkout_changes after each worker ends; raises Fault naming all changed paths | Fault must name only this initiative's paths (r218) | scenario steps, supervision_faults_steps.py:42 and supervision_given.py:158,167 (by search) | read; grep `checkout_changes` |
| scripts/supervise_answers.py:AnswerRound.ask (109-120) | answer sessions run through worker(), so they get checkout_changes too; its own `changed` is the worktree diff | inherits the exclusion through worker(); no change of its own | none by search | read |
| scripts/supervise_answers.py:uncommitted (94-98) | item's file, runs and log differ from HEAD | checks only the item's own path, never another initiative's; unaffected | none by search | read |
| scripts/supervise.py:Run.check (86-93) | refuses to start over loose `.shop/work/` changes (r46) | r218 is about change while a worker runs; start refusal unchanged | none by search | read |
| scripts/supervise_rounds.py:keep_round (266-275) | commits round directory and log; docstring says "nothing uncommitted under .shop/work/" | path-level, unaffected; docstring is loose once other initiatives write there | none by search | read |
| scripts/supervise_intake.py (37, 111) | r46 start check, "nothing uncommitted under .shop/work/" | unaffected (start-up, not during a worker) | none by search | grep |
| scripts/supervise_merge.py (56-65, 117-124) | the work-item branch's changes under .shop/work/ | a worktree/branch concern (r4, r6), not the main checkout | none by search | grep |

## 3. Tests the requirement makes impossible to keep

None. By search over tests/ for "put back", "uncommitted", "own checkout", "changed in the repository" and the other initiative's path: no test asserts that another initiative's uncommitted path is put back. Checked and sound:
- features/supervision.feature:570 (r28, `@deprecated`, retired): asserts only i1's path. It still passes under r218.
- tests/scenarios/supervision_given.py:167 and test_supervision.py:158: i2 changes are committed, so kept under r218 and r214.
- supervision_faults_steps.py:42: i1 path only; still put back.
- features/supervision.feature:2002 and :2011 (r215, r216): not accepted by w236; they describe the same exclusion and will need the same change.

## 4. The file set

- scripts/supervise_faults.py (190 lines; room 110): checkout_changes skips each other group initiative's `.shop/work/<initiative>/` path. Read (104-125).
- scripts/supervise_worker.py (259; room 41): the Fault names only the changed paths left; check the message. Read (169-199).
- scripts/supervise.py (295; room 5): only if the group's initiative names must be passed; avoid editing. Read (58-66).
- tests/scenarios/supervision_faults_steps.py (188; room 112): add the Given for i1's and i2's uncommitted changes in one session, and the Then "nothing recorded of <name> names <path>". Read (42-46, 103-112).
- Path modules, edited or not: supervise.py 295, supervise_worker.py 259, supervise_faults.py 190, supervise_answers.py 147, supervise_rounds.py 275, supervise_merge.py 138 (wc -l, run below). Room is the 300-line limit (no limit line in CLAUDE.md beyond the 300 it names).
- CLAUDE.md: the limit is 300 lines; `tools size --limit 300` run showed no file over it (run).
