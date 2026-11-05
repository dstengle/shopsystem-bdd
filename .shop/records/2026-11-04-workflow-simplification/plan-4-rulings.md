---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-4-rulings
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-05
status: done
---

# Plan 4 of the workflow simplification: rulings on the review, and what was done with each finding

`plan-4-review.md` asked the person two questions, and two of its findings left a choice open. The person was not
available. Each ruling below was **ruled by the main session without the person, 2026-11-05; revisit.** The fixes are
on branch `workflow-simplification` after `f3f8cf50` (the review): `91221299` (the scripts and tests) and `c819cce3`
(the skill).

## Rulings

| # | Question | Ruling (main session, without the person, 2026-11-05; revisit) | What was done |
|---|---|---|---|
| Q1 | A parked item's kept branch is never used again | Accept a fresh branch for a returned item. `building-a-batch` tells the subagent to cherry-pick from the old branch that the item's notes name. | `c819cce3`: in step 4, a returning item's subagent cherry-picks what still applies from `batch-<n>-b<j>` (named in its `## Notes`), keeping each commit's `Item:` line. |
| Q2 | May a branch carry a merge of an earlier in-batch item's branch? | Yes. `uncited` accepts commits that cite an earlier in-batch item of the same batch. A parked item's commits stay refused. | `91221299`: `batch_tasks.citable` gives the task's own item and each `in-batch` item of an earlier task in plan order. `done` and `review` check against it. Tests: `test_done_takes_a_merge_of_an_earlier_in_batch_items_branch`, `test_done_refuses_a_merge_of_a_parked_items_branch`. |
| S4 | Rewrite bdd-red-green, or a brief of the batch's own | Leave `bdd-red-green` as it is, since it serves `work run` until plan 9. Give the batch subagent its own short brief in `building-a-batch` step 4. | `c819cce3`: see S4 below. |
| S2 | What `park` and `abandon` do with uncommitted work | Refuse while a task worktree has uncommitted changes, unless `--discard`. | `91221299`: see S2 below. |

## The findings

| # | What was done |
|---|---|
| B1 | Fixed in `91221299`. Before the merges, `work batch review` makes one commit on `batch-<n>` that takes every parked item's lines out of `spec/`. Its groups and term bullets go (`backlog_lines.unlay`), its ids leave `unbuilt:` (`spec_unbuilt.without_unbuilt`), and each feature it touched is generated again (`batch_start.unlay_lines`). The commit is `batch-<n>: the requirement lines of <items> taken out` and cites them. A rerun makes no second commit. The scenario world's `make_batch` now makes a real lines commit (`batch_start.lay_lines`), and each item branch takes its ids out of `unbuilt:`. r7's `does not publish the commit` also checks that the item's groups are not in the published spec. With the take-out disabled, r7 and the new end-to-end test fail. That test is `test_a_parked_item_is_published_without_its_lines_and_laid_again`: park → review (`origin/batch-1` without b2's group, id or scenario) → merge → `merged` → `work answer` → `work ready` → `work batch start` lays it on `batch-2`. |
| S1 | Fixed in `91221299`. `batch_git.is_tree(path, branch)` checks that `git -C path rev-parse --show-toplevel` is the path and that HEAD is the branch. `tree_for` makes the worktree when it is not there: an empty directory is replaced, and anything else is refused, naming the path. `review` and `resume` use `tree_for`; `done` refuses `has no worktree at <path>`. `remove_tree` removes only a worktree or an empty directory. Tests (`test_batch_trees.py`): an empty directory at the batch's tree with a dirty base and failing tests leaves the base as it was; a non-empty one is refused; `resume` makes a task's tree in an empty directory; `done` refuses one. |
| S2 | Fixed as ruled in `91221299`. `work batch park … [--discard]` and `work batch abandon … [--discard]` refuse with `<cmd>: t<k> b<j> "<title>" has uncommitted changes in <tree>: <files>; commit them on <branch> with Item: b<j>, or pass --discard`. `merged` keeps removing with `--force`, since the work has been merged. Tests: `test_park_refuses_uncommitted_work`, `test_abandon_refuses_uncommitted_work`. |
| S3 | Fixed in `c819cce3`, with Q2. Step 6 says what to do on each refusal of `review`. On a conflict, the later item's subagent merges the earlier item's branch and resolves it in a commit citing its own item, or one of the two is parked. When the tests fail, the item that broke them is fixed on its branch. On a push or gh failure, the cause is fixed and the review is run again. |
| S4 | Fixed as ruled in `c819cce3`. Step 4's brief gives the worktree, the branch and the item file. It gives the ids, with `python3 -m pytest -q tests/scenarios/test_<cap>.py -m r<n>` to run their scenarios. It names the rules of `bdd-red-green` that hold: one scenario at a time, red first, never edit a `.feature`, and setup-only changes to existing tests. It says: "There is no brief or result file … `work batch done` runs the whole suite in your worktree". `test_skill_building_a_batch.py` pins each of these. |
| M1 | Fixed in `91221299`. `batch_pick.Pick` has `renumbered`, which holds this pick's pairs by item, and `said` prints only those. Test: `test_start_prints_only_the_renumbering_it_made` (start, abandon, start). |
| M2 | Fixed in `91221299`. Under the lock, `done` also requires the worktree to be the task's and to have no uncommitted changes. Test: `test_done_refuses_an_edit_made_while_its_tests_ran`. |
| M3 | Fixed in `91221299`. `start` refuses while `git status --porcelain -- spec features` is not empty, naming the paths. Test: `test_start_refuses_uncommitted_spec_or_features`. |
| M4 | Fixed in `91221299`. `batch_plan.task`, `batch_gh` and `batch_git.push` take the command: `work batch done: batch-1 has no task t9`, and `work batch review: gh pr create failed: …`. |
| M5 | Fixed in `91221299`. When `gh pr create` fails, `batch_gh.create` asks `gh pr list --head <branch> --json url`. If an open pull request is there, the review keeps it and does not put the branch back. The stand-in gh gained `pr list` (open creates of that head) and `$STUB_GH_LATE`, which makes a call do its work and then fail. Test: `test_a_pull_request_created_by_a_failing_gh_is_kept`, which fails with the lookup removed. |
| M6 | Fixed in `91221299`. The settle keeps the base's ids that both sides kept, then each id that either side added. Test: `test_batch_merge.py`. |

## Verification after the fixes

| Check | Result |
|---|---|
| `python3 -m pytest -q` | 1277 passed, 1 skipped, 14 xfailed, 132 subtests passed (was 1258; the 19 new tests). The ceiling report lists two old tests over 10 s under load (`test_supervision`'s flaky-scenario test, `test_e2e_codified`). It reports only. |
| `python3 -m pytest -m timing -n 0 -q` | 1 passed, 1292 deselected |
| `model check` / `logic` / `lexicon --check` | 53 violations, 16 warnings, 19 unresolved, 0 file problems / 11 findings: 6 L5, 5 L6 / 401 terms, 0 problems (all at baseline) |
| `features generate --check`, `vocab --check`, `bindings --unbound` | exit 0, every step has one handler, every binding names a scenario |
| `tools size --limit 300`; `tools check` over the changed Python | silent; ruff and vulture clean |
| Smoke loop (`/home/vscode/.claude/jobs/7e9ba079/tmp/fix4/`, bare remote, stand-in gh) | Below. |

The smoke loop gave these results:

- A dirty `spec/index.md` refused `start`.
- `start` took three items (0.36 s); b2 and b3 were renumbered.
- `park b3` was refused for a `wip.py`, then parked with `--discard`.
- Both `done`s passed.
- `review` ran with an empty directory at `batch-1`'s tree and a dirty base. It made the worktree there, and the base kept only its own edit. It published `pull/1`, whose spec has b1's and b2's groups, `unbuilt: []`, and no b3.
- `merged` delivered b1 and b2. `main` has no r7. b3 was answered and readied.
- `start` laid b3 again as g6/r7 on `batch-2`, with no renumbering printed.
- `abandon` was refused for a `wip.py`, then passed with `--discard`.
- The base's `git status --porcelain` was empty.
