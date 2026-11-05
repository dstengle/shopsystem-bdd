# Plan 4 of the workflow simplification: implementation report

This is the report of the one implementer agent that executed `plan-4-batches.md` on 2026-11-05. It used
superpowers:executing-plans, with one commit per task and no subagents.

All 10 tasks are done. The `batches` capability is built: all 13 of its requirements are out of `unbuilt:`, and each
one's scenario passes, each checked to fail for its own point first. Alongside: the backlog shows how far an
in-batch item's batch is along, `work depend --drop`, a request whose counter-proposals are settled closes, and the
skill `building-a-batch`. The commits are on `workflow-simplification`, from `d788ac99` to this report's commit. They
are not pushed, and no test or smoke run touched the real remote (a bare repository and the stand-in gh only). No
baseline got worse.

## Final state

| Check | Result |
|---|---|
| Suite (`python3 -m pytest -q`) | **1258 passed**, 1 skipped, **14 xfailed**, 132 subtests passed. The start was 1153 passed, 27 xfailed, 131 subtests. The 105 new passes are the 13 batches scenarios and 92 new script tests (batch plan 10, git and gh 10, pick 7, lines and unbuilt 3, start 8, tasks 17, review 11, close 7, backlog view and moves 7, counter-proposals 7, the skill 4, and the new skill's row of the description check 1). The new subtest is `test_agents.py`'s check over the new skill. The known flake `test_model_logic_on_the_live_spec_is_fast` is now a timing test and did not fail. |
| Timing run (`python3 -m pytest -m timing -n 0 -q`) | `1 passed, 1273 deselected` (1.7 s) |
| Unbuilt ids | `False 23 []`: batches is not in `spec_unbuilt.unbuilt()`, 23 ids remain (36 − 13), no problems |
| `model check` | 53 violations, 16 warnings, 19 unresolved references, 0 file problems (at its baseline) |
| `model logic` | `11 findings: 6 L5, 5 L6` (at its baseline, with the glossary's new transition) |
| `model lexicon --check` | 401 terms, 0 problems |
| `features generate --check` | exit 0. No feature file was touched. |
| `features vocab --check` | `every step has one handler` |
| `features bindings --unbound` | `every binding names a scenario` |
| `tools size --limit 300` | silent. `scripts/work` is at 213 (limit 216), `backlog_handlers.py` at 262 (limit 266), `work_queue_world.py` at 238 (limit 245). The largest new module is `batch_tasks.py`, 201. |
| `tools check` over the branch's Python files and `scripts/work` | ruff, vulture and import-linter clean |
| Smoke run (Task 10, Step 3, in bash) | `start` printed `batch-1 building: t1 b1 "Abandon a started initiative", t2 b2 "Abandon quietly"` and `b2 "Abandon quietly" renumbered: work-queue#g4 -> work-queue#g5, work-queue#r5 -> work-queue#r6`, in **0.23 s** (a warm parse cache). `work backlog` showed both rows `in batch-1 (building): 0 of 2 tasks done`. `resume` printed two `running in` lines. Both `done`s passed; `review` printed `https://github.com/ex/ctx/pull/1`; `merged` delivered b1 and b2, and `work backlog`'s `delivered (2)` table holds them. `git status --porcelain` is empty. `main`'s `work-queue.md` has r5 and r6, with `unbuilt: []`. The stand-in gh got one `pr create --draft --base main --head batch-1` and one `pr view`. |

## Commits

| Task | Commit | What was done | Verification |
|---|---|---|---|
| 1 | `d788ac99` | Created `batch_git.py` (`git`/`GitFailed` moved from `supervise_worker`, which imports them back; `delivery`, `scripts_env`, `locked`, `current_branch`, `trees_dir`, `add_tree`, `remove_tree`, `remote`, `push`), `batch_gh.py` (`create`, `state`, `close`), `batch_plan.py` (the batch file, round-tripping), `tests/scripts/stub_gh.py` (D20, executable), `batch_testing.py`, and the `batch_outside`/`batch_repo` fixtures. Three module-map rows. | The two test files failed first (no modules), then 20 passed (one test fixed: it read `delivery` of the repository it meant to be bare); with `test_supervision.py`, 100 passed. Suite: 1173 passed, 27 xfailed. |
| 2 | `ae63c4e7` | `backlog_lines.lay_onto`, `lay(..., others)`, `renumber` (D8); `readiness_bar.check`/`well_formed` take `others`; `spec_unbuilt.with_unbuilt`; `batch_pick.py` (D7). | The new tests failed first (no `batch_pick`, no `renumber`, no `with_unbuilt`), then passed; with the readiness tests, 51 passed. Suite: 1183 passed, 27 xfailed. |
| 3 | `5b841264` | `batch_start.py` (the batch branch and its worktree, the lines laid with ids into `unbuilt:` and the features generated, one commit citing each item; then the plan and items on the base; branch and worktree removed on a failure) and `batch_cli.py` (`start`, `status`, `--json`); `scripts/work` gained 2 lines. `batches_world.py`, `batches_handlers.py`; `local` chains (D23); `item_is` reads `strict_not` (D21); `test_batches.py` binds with `bind_all`. r1-r4 out of `unbuilt:`. | Script tests failed first (no `batch` command), then 8 passed. r1-r4 passed, r5-r13 xfailed. Mutations, each reverted: `start` not moving items failed r1 (`'ready'`); the alone check skipped failed r2 (`'ready'`); `blocked` ignored failed r3 (`'in-batch'`, exit 0); the status word dropped failed r4. Suite: 1195 passed, 23 xfailed. |
| 4 | `ea9d5dac` | `batch_tasks.py`: `resume` (D16), `done` (its seven checks, then the commit under the lock), `park` (D15), and `lines_commit`, `uncited`, `under_shop`, `run_tests`, `item_ids`; the three parsers; `batches_handlers_more.py` (resume, use, park, the question). r5, r6 out. | Script tests failed first, then 17 passed (two `done`s at once both landing; a lost worktree given back with its commit; each of six refusals naming its cause with nothing changed). Mutations: `resume` printing `Carry on?` failed r5 on `does not ask`; `park` setting the batch `abandoned` failed r6. Suite: 1214 passed, 21 xfailed. |
| 5 | `00e224cd` | `batch_review.py` (D11, the nine steps, the branches and the remote put back on a refusal) and the new `batch_merge.py` (Deviation 1); the review handlers. r7, r8, r11-r13 out. | Script tests failed first (no `review`), then 11 passed, the four Review Focus 3 causes included, with a rerun after `gh` publishing. Mutations: merging every task's branch failed r7 (the parked commit published); the title in place of the label failed r11; the task check skipped failed r12 (exit 0); `uncited` skipped failed r13. Suite: 1230 passed, 16 xfailed. |
| 6 | `ebba3a6e` | `batch_close.py` (`merged`, D13; `abandon`, D14); the glossary's `in-review` → `merged`: merge; the merge and abandon handlers; batches' `unbuilt: []`, its Implementation bullets and a `## Not yet`. | `model logic` and `lexicon` unchanged after the transition. Script tests failed first, then 7 passed; all 13 scenarios passed. Mutations: `merged` not delivering failed r9; `abandon` leaving items `in-batch` failed r10. Suite: 1239 passed, 14 xfailed, twice. |
| 7 | `2ec01065` | `backlog_view.progress` and the `waiting on` cell and `batch` JSON key (D26); `backlog_moves.undepend` and `--on | --drop` (D27); backlog's two `## Not yet` bullets gone. | The new tests failed first (4; the two usage-error rows passed already, as argparse refused `--drop`), then passed with the backlog scenarios: 130 passed. Suite: 1246 passed, 14 xfailed. |
| 8 | `f7c1ecbc` | `request_text.py` (the helpers made public, `countered`, `turned`); `workqueue_request.turn` calls `turned` and `refuse_upstream_part` is public; `intake_moves`' rewritten path writes `## Counter-proposals` and calls `turned`; `model_requests.SECTIONS` gains the section; the two tests' `_entries` renamed. | `test_request_counter.py` failed first (no section, the `awaiting-asker` literal), then 7 passed; the old turn, kept in the test, gives the same bytes on four requests without the section. Request, intake and `test_work_*` tests: 106 passed. Suite: 1253 passed, 14 xfailed; `model check` at baseline. |
| 9 | `bb0515e2` | `skills/building-a-batch/SKILL.md`, its test, the skills' command check over three skills, README's list, intake's `## Not yet` bullet (D25); `taking-in-a-request` step 2's sentence about plan 4 (Deviation 7). | The test failed first (no skill), then 4 passed; with the command check and `test_agents.py`, 27 passed. Suite: 1258 passed, 14 xfailed. |
| 10 | this report | The whole-plan verification, the smoke run, this report and its row in `.shop/records/README.md`; every box of the plan ticked. | See Final state. |

## Deviations from the plan

Each is a ruling, decided by the implementer; revisit.

1. **Two items of one capability always conflicted at review (a plan defect).** Under D6 every picked item's ids sit
   on one `unbuilt: [...]` line of the batch branch, and each task takes its own out, so two items of one capability
   change the same line differently. The plan's own smoke run would have failed at `review`. The new module
   `batch_merge.py` settles that conflict alone: when a conflicted file merges cleanly with its `unbuilt:` line set
   aside, the line is written with the ids still unbuilt on both sides. Any other conflict aborts the merge and is
   refused naming the item. Cost if wrong: a hand edit of `unbuilt:` on a branch is reconciled, not refused.
2. **`done` runs its checks and the tests outside the lock** (D17 said from first read to commit). Under the lock it
   reads the plan again and commits only if the task is still `running` and its branch is at the head that was
   tested; else it is refused, `changed while its tests ran; run it again`. Holding the lock through a suite would
   make every subagent's `done` wait for the others' tests. `review` holds the lock throughout, as planned.
3. **A failed review also puts the remote back.** After a push, a refusal by gh deletes the remote's branch (or
   force-pushes it back to where it was), so a rerun's new merge commits push cleanly. A worktree (or the worktrees
   directory) the review made again is removed on a refusal, so the base checkout stays byte-identical.
4. **The merge When is `local("WhenHappens", "pull request")`**, not a registry handler `("WhenHappens", "merge")`:
   that one took supervision's `work run merges the work-item branch` from supervision's fallback and failed
   `test_a_merged_workitem_branch_is_deleted`.
5. **The `ThenExitsErr` task and commit locals came in Task 3**, not Task 5: r12 passed vacuously (XPASS strict)
   through the registry's ``ThenExitsErr `work` ``, since argparse's exit 2 named nothing. With the locals, r12
   xfailed until `review` existed.
6. **Renumbering against `spec/` comes before the alone check.** An item is checked alone with its ids moved past
   its capability's only (on a copy), so an item whose ids a delivered batch took is not returned for the collision.
   Cost if wrong: an item with a real duplicate-id problem is renumbered, not returned.
7. **Files outside a task's list:** Task 7 rewrote backlog's Implementation sentence that the same-batch exception
   "waits for plan 4" (the pick makes it); Task 9 rewrote `taking-in-a-request`'s sentence that a counter-proposed
   request stays `awaiting-asker` (Task 8 made it false); Task 7 also gave `work show --json` the `batch` key.
8. **Smaller choices:** the scenario world's `$SHOPSYSTEM_WORK_GH` is `<python> stub_gh.py` (`batch_gh` shell-splits
   the variable), not a `bin/gh` script; `start`'s refusals read `batch-1 is building; one batch is open at a time`
   and `the checkout is on a detached HEAD`; `start` silences `features generate`'s skipped-group stderr (the bar
   names them); the renumber note lists groups too (`work-queue#g4 -> work-queue#g5, work-queue#r5 -> work-queue#r6`)
   and a returned item's note is `returned by work batch start: <reasons>`; `park` takes an in-batch item whatever
   its task's status; `merged` commits first, then removes worktrees and deletes merged item branches (`git branch
   -d`, failures ignored); the batch progress shows for an `in-batch` item only; the stand-in gh records a failed
   call with `"failed": true` and counts only the creates that did not fail; the old turn is a Python function in
   `test_request_counter.py` (ruff's S102 refuses `exec`).

## D1-D27

| # | Kept or changed |
|---|---|
| D1 | Kept: every commit on `workflow-simplification`, none pushed. |
| D2 | Kept: `work batch` starts no session; `building-a-batch` is the batch session's instructions. |
| D3 | Kept: one task an item, `t<k>` in pick order, branch `batch-<n>-b<j>`, worktree `batch-<n>-t<k>`. |
| D4 | Kept: `.shop/batches/<n>/plan.md` in the given format, committed on the base only; `done` and `review` refuse a branch that changes `.shop/backlog/` or `.shop/batches/`. |
| D5 | Kept. Item branches are merged only by `review`, `--no-ff`, in plan order; a parked item's never. |
| D6 | Kept, with `batch_merge` (Deviation 1) for the `unbuilt:` line it makes two items share. |
| D7 | Kept, with the spec renumber before the alone check (Deviation 6). |
| D8 | Kept: `renumber`, with the note naming groups as well. |
| D9 | Kept. |
| D10 | Kept: the `Item: b<j>` trailer, read with `%(trailers:key=Item)`. |
| D11 | Kept, with the remote put back on a failure (Deviation 3). |
| D12 | Kept: `[batch] tests`, default `python3 -m pytest -q -p work_items`, the last 20 lines on a failure. |
| D13 | Kept: the glossary transition, `model logic` and `lexicon` unchanged. |
| D14 | Kept. |
| D15 | Kept. |
| D16 | Kept. |
| D17 | Changed for `done` (Deviation 2); kept for the other commands. |
| D18 | Kept: every batch command but `status` refuses another branch; `start` a detached HEAD. |
| D19 | Kept: `[batch] worktrees`, else `.shop/worktrees/`, with a `.gitignore` of `*`. |
| D20 | Kept, with failed calls recorded and not counted. |
| D21 | Kept: the world's own `i92`; `strict_not` set by the `start` handler; `batch_is` asserts exit 0 on a negated Then too. |
| D22 | Kept: tasks `done` unless a Given says otherwise, `pending` under `resume`. |
| D23 | Kept. |
| D24 | Kept. |
| D25 | Kept: `request_text`'s public names, `refuse_upstream_part`; M9 kept; no intake session; no rewording command. |
| D26 | Kept, for `in-batch` items (and `work show --json`). |
| D27 | Kept. |

## Open problems for plan 5 and later

- **The end-of-branch review has not run.** The plan gives it to a separate reviewer, writing `plan-4-review.md` and
  reading `8f42ff62..HEAD` against the plan's Review Focus.
- **The scenarios' batches are built by hand** (`batches_world.make_batch`): an empty lines commit and one commit for
  each item. They test the commands' contracts, not `start`'s output feeding `review`; the script tests and the
  smoke run cover the whole loop.
- **`batch_merge` settles only the `unbuilt:` line.** Two items that each add a group at the end of one capability's
  `## Behaviour` are laid together by `start` in one commit, so they do not conflict; but two items whose tasks both
  edit the same feature file or handler module will conflict at review, and that is refused (by design: the batch
  session resolves it on one item's branch, or parks one).
- **`done`'s tests are not re-run after review's merges per item**; `review` runs the suite once, on the merged
  branch.
- **`start`'s time on the live spec has not been measured.** On the fixture it is 0.23 s with a warm cache; each
  picked item costs two bar checks (alone and laid with the picked).
- **The fix loop (plan 5)** sets a reviewed batch back to `building`; `review` then pushes only. Nothing sets
  `building` from `in-review` yet, and `awaiting-merge` is never written.
- **Not yet** (batches' `## Not yet`): tasks finer than an item, a task `failed` by a command, the delivered item's
  request resolved at the merge, a session `work` starts itself.

## Files

- Created: `scripts/batch_git.py`, `scripts/batch_gh.py`, `scripts/batch_plan.py`, `scripts/batch_pick.py`,
  `scripts/batch_start.py`, `scripts/batch_cli.py`, `scripts/batch_tasks.py`, `scripts/batch_review.py`,
  `scripts/batch_merge.py`, `scripts/batch_close.py`, `scripts/request_text.py`, `skills/building-a-batch/SKILL.md`,
  `tests/scripts/stub_gh.py`, `tests/scripts/batch_testing.py`, `tests/scripts/test_batch_plan.py`,
  `tests/scripts/test_batch_git.py`, `tests/scripts/test_batch_pick.py`, `tests/scripts/test_batch_start.py`,
  `tests/scripts/test_batch_tasks.py`, `tests/scripts/test_batch_review.py`, `tests/scripts/test_batch_close.py`,
  `tests/scripts/test_request_counter.py`, `tests/scripts/test_skill_building_a_batch.py`,
  `tests/scenarios/batches_world.py`, `tests/scenarios/batches_handlers.py`, `tests/scenarios/batches_handlers_more.py`.
- Modified: `scripts/work`, `scripts/supervise_worker.py`, `scripts/backlog_lines.py`, `scripts/backlog_view.py`,
  `scripts/backlog_moves.py`, `scripts/backlog_cli.py`, `scripts/readiness_bar.py`, `scripts/spec_unbuilt.py`,
  `scripts/workqueue_request.py`, `scripts/intake_moves.py`, `scripts/model_requests.py`, `tests/scripts/conftest.py`,
  `tests/scripts/test_backlog_lines.py`, `tests/scripts/test_spec_unbuilt.py`, `tests/scripts/test_backlog_view.py`,
  `tests/scripts/test_backlog_moves.py`, `tests/scripts/test_intake_outcome.py`,
  `tests/scripts/test_skill_shaping_items.py`, `tests/scenarios/work_queue_world.py`,
  `tests/scenarios/backlog_handlers.py`, `tests/scenarios/intake_handlers.py`, `tests/scenarios/test_batches.py`,
  `skills/taking-in-a-request/SKILL.md`, `spec/capabilities/batches.md`, `spec/capabilities/backlog.md`,
  `spec/capabilities/requests.md`, `spec/capabilities/intake.md`, `spec/index.md` (one transition), `README.md`,
  `CLAUDE.md`, `.shop/records/README.md`, `plan-4-batches.md` (boxes ticked).
