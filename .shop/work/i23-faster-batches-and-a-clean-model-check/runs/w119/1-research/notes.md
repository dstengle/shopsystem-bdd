# Research of w119 (supervision r63: blocked_by across initiatives)

No map: `tools map` has none, so `tests-of`/`untested` are unusable. Counts are `by search` (grep) or `run`. `tools refs` finds no method names (`supervise_pool.blocked`, `supervise.items`).

Accepted scenarios (features/supervision.feature, lines 664-670 and 673-679):
- S1 "no worker is started for a work-item whose blocked_by names a work-item that is not green"
  `tests/scenarios/test_supervision.py::test_no_worker_is_started_for_a_workitem_whose_blocked_by_names_a_workitem_that_is_not_green`
- S2 "a worker is started for a work-item whose blocked_by names a green work-item of another initiative"
  `tests/scenarios/test_supervision.py::test_a_worker_is_started_for_a_workitem_whose_blocked_by_names_a_green_workitem_of_another_initiative`

## 1. Why each scenario is red today

- S1: passes today. `python3 -m pytest -q <S1 node id>` (run): 1 passed. It must stay green.
- S2: fails at its first Given. `python3 -m pytest -q <S2 node id>` (run):
  `StepDefinitionNotFoundError: Given "i1's work-item w1 is drafted, its blocked_by naming w2"` (feature line 675).
  `blocked_item` (tests/scenarios/supervision_parallel_steps.py:23-28) matches only "..., its blocked_by naming X, and Y is Z" and writes Y into i1. S2 needs a Given with no second work-item in i1.
- S2, undefined by read (the run stops at the first undefined step; search of tests/scenarios):
  - feature line 676 "an initiative i2 under .shop/work/ whose work-item w2 is green": the only match is `with_items` (tests/scenarios/test_work_queue.py:66), and test_supervision.py does not import test_work_queue's steps. Read: undefined here.
  - feature line 679 "a worker was started for w1": no definition. `no worker was started for` (supervision_parallel_steps.py:122, supervision_faults_steps.py:29) is the negative; `the first worker started for {name} was ...` (supervision_then_workers.py:59) does not match. Read: undefined.
- In code: `Pool.choose` (scripts/supervise_pool.py:62) builds `statuses = dict(self.items())`, and `Run.items` (scripts/supervise.py:60-61) returns this initiative's work-items only. A blocker in i2 is never found, `Pool.blocked` (supervise_pool.py:46-50) returns True, and w1 is never started. Probe A1 confirms it (section 2).

## 2. What the system answers today

Probes (scratch directory only):
- `python3 -m pytest -q -s -n 0 .shop/scratch/1-research/probe_blocked.py` (run). Each case: its own repository, the stand-in claude, `work run i1`.
  - A1 S2's data (i1/w1 drafted, blocked_by [w2]; i2/w2 green; every worker DONE): exit 1, stdout `w1 drafted`, no worker started. S2 expects a start. Red reason confirmed.
  - A2 blocker not green across initiatives (i2/w2 awaiting-answer): exit 1, `w1 drafted`, no start. Correct today.
  - A3 blocker green in the same initiative (i1/w2 green): exit 0, `w1 green | w2 green`; w1's four stages and the branch reviewer started. Works today.
  - A4 blocker absent everywhere (blocked_by [w9]): exit 1, `w1 drafted`, no start, no message naming the missing blocker.
  - A5 id form `work-item/w2` with i2/w2 green: exit 1, `w1 drafted`, no start.
- `python3 -m pytest -q -s -n 0 .shop/scratch/1-research/probe_other.py` (run):
  - B1 i2/w2's file says green, i2's log.jsonl last transition is to done: `work show` prints `i1/w1 drafted | i2/w2 green` (rc 0); `work run i2` refuses, rc 1: `.shop/work/i2/w2.md gives its status as green, but log.jsonl's last transition of w2 is to done; it is not moved`; `work run i1` prints `w1 drafted`, rc 1 (w2 never read).
  - B2 i2/w2 with its status line removed: `work show` prints `i2/w2 None` (rc 0); `work run i1` prints `w1 drafted`, rc 1.
- Probe repositories: `.shop/scratch/1-research/probe_blocked_runs/` (cases named as above).

## 3. Old assumptions

Places that assume a work-item's statuses come from its own initiative, or that names are unique across initiatives (search of scripts/, read of the spec):

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_pool.py:Pool.choose, line 62 | `statuses = dict(self.items())`: this initiative's statuses, keyed by name | must hold every initiative's statuses, keyed by name (workqueue.items, workqueue.py:100, already reads every initiative) | S1 and S2 (test_supervision.py; S1 run, passes through it) | search (grep `items()`) |
| scripts/supervise_pool.py:Pool.blocked, lines 46-50 | looks each blocker up in the map given; reads the work-item's own file in self.dir | its logic can stay; only the map it is given changes | S1 (run); probes A1, A2, A4, A5 | read |
| scripts/supervise.py:Run.items, lines 60-61 | this initiative's (name, status) | must stay this initiative's: `choose` loops over it to pick what moves (supervise_pool.py:70), and `run` judges it (supervise.py:189, 196). Changing it would start other initiatives' work-items | every scenario that calls `work run` in test_supervision.py (by search: `items()` runs on every pull) | search |
| scripts/workqueue.py:items, line 100 (used by `work show` and supervise.py:61) | file status only, no log check | a blocker's status would be read without `agrees` (workqueue.py:169), which `check` runs for this initiative's items (supervise.py:72-73) | test_work_queue.py `work show` scenarios; probes B1, B2 | probe |
| spec/capabilities/migration-tools.md r26 and work-queue r12 | legacy names may be held by several initiatives; `work add` numbers ids `w<n>` above any initiative's highest, so ids are unique | a map keyed by name holds two statuses for one name; which counts is not given (see Questions) | none | search (spec text) |

## 4. Tests the requirements make impossible to keep

- By search: `grep -rln blocked tests/scenarios tests/scripts` finds blocked_by only in supervision_world.py (`item_text`), supervision_parallel_steps.py, the migration and model-check step modules, test_migrate_upgrade_ids.py and test_model_reading.py (migration and model, not `work run`). No test asserts that a blocker in another initiative keeps its work-item blocked. S1 is the only such assertion and it still holds (w2 is awaiting-answer, not green).
- By search: test_supervision.py scenarios with i2 (supervision_given.py:167-171, "another session commits .shop/work/i2/initiative.md"): i2 holds only an initiative.md (kind initiative, skipped by workqueue.items). Found sound: the new map would ignore it.
- Found sound: every other `work run` scenario uses one initiative, where the map of all initiatives equals this initiative's map.
- Nothing can no longer pass as it is.

## 5. A step the work-item skips

The new path reads a blocker's status from its file (workqueue.items) and not through `workqueue.agrees`. The existing way checks each of this initiative's work-items with `agrees` (supervise.py:63-73; workqueue.py:169-181), which refuses a file with no status (workqueue.py:173-174) or whose status differs from log.jsonl's last transition (workqueue.py:176-178). Effects only this step produces:
- Refusal "gives its status as X, but log.jsonl's last transition ... is to Y": run by B1 (`work run i2`, rc 1).
- Refusal "has no status in its frontmatter; it is not moved": read (workqueue.py:173-174); `work run i2` was not run on B2. B2 shows the status-less blocker is listed by `work show` as `None`.
- With a file-only read, `work run i1` would start w1 on w2 whose file says green while `work run i2` refuses w2 (B1). Read: this is the new path, not yet in the code.
Both readings for the plan: (a) read each blocker through `agrees`, and treat a refusal as not green (or as a refusal of i1); (b) read the file's status only, as r63 literally says ("names a work-item that is not `green`").

## 6. Defects

### D1: a blocked work-item gives no reason
Repro: `python3 -m pytest -q -s -n 0 .shop/scratch/1-research/probe_blocked.py`, case `blocker_absent` (run). `work run i1` with i1/w1 drafted, blocked_by [w9] and no w9 anywhere prints `w1 drafted` and exits 1. Nothing says w9 is missing or that w1 waits. The exit rule (r9, "otherwise") is met; the silence is the observation. Not judged here.

## 7. The file set

Changes needed:
- scripts/supervise_pool.py (141 lines; room 159): `Pool.choose` builds `statuses` from every initiative (workqueue.items), not `self.items()`. Read of line 62; probes A1, A2.
- tests/scenarios/supervision_parallel_steps.py (125 lines; room 175): new Given for "i1's work-item w1 is drafted, its blocked_by naming w2" (no w2 in i1), new Given "an initiative i2 under .shop/work/ whose work-item w2 is green", new Then "a worker was started for <name>". Read: feature lines 673-679; the undefined-step error (run).

Read, not edited (on the change's path):
- scripts/supervise.py (218 lines; room 82): `items()` must stay this initiative's; `check` and `run` read it.
- scripts/workqueue.py (262 lines; room 38): `items()` already reads every initiative. Not edited unless the plan reads blockers through `agrees` (section 5).
- scripts/supervise_worker.py (229 lines; room 71): the worker start `Workers.worker`, on the path of each started work-item.

Not edited: features/supervision.feature (scenarios present); tests/scenarios/test_supervision.py (242 lines; star imports pick up the new steps); tests/scenarios/supervision_given.py (250 lines); supervision_world.py (173 lines).

Size: `python3 <Scripts>/tools size --limit 300` printed nothing (no file over 300).

Brief's citation: it says statuses are "keyed by name (work-queue r12)". work-queue r12 is id numbering; the all-initiative reading is work-queue r3 (`work show`).

## Questions (also in result.json)
1. Names held by two initiatives (legacy names, migration-tools r26): which status counts for a blocker name? (a) the blocker in the work-item's own initiative first, then any other; or (b) refuse as ambiguous.
2. Should a blocker in another initiative be read through `agrees` (refusing a disagreeing file) or as its file's status only (section 5)?
