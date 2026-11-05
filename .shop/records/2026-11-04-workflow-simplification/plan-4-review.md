---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-4-review
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-05
status: done
---

# Plan 4 of the workflow simplification: the end-of-branch review

This is the one end-of-branch review of plan 4 (batches). It covers `8f42ff62..d9b31ea9` on `workflow-simplification`.
It checks the range against `plan-4-batches.md` (its Review Focus, Global Constraints and D1-D27), design goal 5 with
"Where a ready item's lines live" and "Keeping items separable in a batch", the plan-1/2/3 rulings, `CLAUDE.md` and
`skills/building-a-batch/SKILL.md`. It also checks the claims of `plan-4-implementation.md`.

The reviewer changed nothing in the repository except this file, and committed nothing. The whole batch loop was run by
hand in scratch repositories under `/home/vscode/.claude/jobs/7e9ba079/tmp/review4/`, each with a bare repository as
its remote and `tests/scripts/stub_gh.py` as gh. The real remote was never touched.

## Verdict

**Not ready to close as is: one blocking finding, four should-fix findings.**

The mechanics are sound and well tested. Every baseline matches the report. Two `done`s at once both land, and they
really run in parallel. A review that fails halfway puts the batch branch and the remote back. A lost worktree comes
back with its commits. Each refusal names its cause and changes nothing.

The blocking finding is about what a parked item leaves behind. Its requirement lines are laid in the one shared lines
commit, so they go out in the pull request. After the merge, `main` holds them as unbuilt requirements, and the item
can never be made `ready` again (B1, reproduced). That breaks the design's "the lines enter `spec/` with the batch's
merge" and the point of r7. The r7 scenario cannot see it, because the scenario world's lines commit is empty.

Two of the should-fix findings lose work:

- A directory at a worktree path that is not a worktree is used as one. A failed review then ran `git reset --hard` in
  the person's base checkout and wiped their uncommitted changes (S1, reproduced).
- `park`, `abandon` and `merged` discard a task worktree's uncommitted work without saying so (S2, reproduced).

## Verification (report vs got)

| Check | Report | Got (this review) |
|---|---|---|
| `python3 -m pytest -q` | 1258 passed, 1 skipped, 14 xfailed, 132 subtests | **1258 passed, 1 skipped, 14 xfailed, 132 subtests passed** (21.7 s) |
| `python3 -m pytest -m timing -n 0 -q` | 1 passed, 1273 deselected | **1 passed, 1273 deselected** (1.77 s) |
| Unbuilt ids | `False 23 []` | `False 23` (batches not in `unbuilt()`) |
| `model check \| tail -1` | 53 violations, 16 warnings, 19 unresolved, 0 file problems | **same** |
| `model logic \| tail -1` | 11 findings: 6 L5, 5 L6 | **same** |
| `model lexicon --check \| tail -1` | 401 terms, 0 problems | **same** |
| `features generate --check` | exit 0 | exit 0 |
| `features vocab --check` | every step has one handler | same |
| `features bindings --unbound` | every binding names a scenario | same |
| `tools size --limit 300` | silent | silent, exit 0 |
| `tools check $(git diff --name-only 3be6b387...HEAD -- '*.py' scripts/work)` | clean | ruff, vulture clean; no import contracts |
| `CLAUDE.md` rows | a row for each new module | a row for each of the 10 `batch_*.py` and `request_text.py`; `stub_gh.py` and `batch_testing.py` in the `tests/scripts/` row; handlers and world rows updated |
| Review Focus tests 1-5 | pinned | all nine named tests exist (`test_batch_start.py`, `test_batch_tasks.py`, `test_batch_review.py`) and pass |
| Smoke: `start` time on the fixture | 0.23 s (warm cache) | 0.35 s (three items, warm) |
| `start` on this repository's own spec (scratch clone, 2 items into `batches`) | not measured | **7.2 s** with a warm parse cache, **15.5 s** with a cold one (`XDG_CACHE_HOME` empty); `resume` 0.9 s |

### The loop run by hand (scratch repos `a`, `b`, `self`)

| Step | Result |
|---|---|
| `status` / `resume` before any batch | `there is no batch in .shop/batches/` (exit 0); `there is no batch batch-1 ...` (exit 1) |
| `start` with three ready items, a dirty `spec/index.md` and an untracked file in the base | `batch-1 building` with t1-t3; b2 and b3 renumbered (r6, r7); base on `main`, `spec/` byte-identical (md5), dirty and untracked files untouched |
| Off-branch `resume`; `status` off-branch; `start` while open; `done` on a pending task; `done t9`; `review` with tasks pending; `merged` on building; `park b9` | each refused naming the branch, batch, status, task or item; `status` works off-branch (D18) |
| `resume` twice, stdin closed | three `running in` lines; the second run is identical and commits nothing |
| `done` refusals | still in `unbuilt:`; uncommitted file; uncited commit (`fa9075e "junk without trailer"`); a commit changing `.shop/backlog/z.md`: each named |
| Two `done`s at once, tests `sleep 3` | both `done`, two commits, **3.2 s in all** (they overlap, so Deviation 2 does what it says) |
| A commit on the task branch while `done`'s tests run | `changed while its tests ran; run it again` |
| Worktree `rm -rf`'d, then `done` / `resume` | `has no worktree; run work batch resume batch-1`; `resume` gives it back at `cd5aeb9 more b3`, still `running` |
| `park` b3 (task done) | `needs-input`, with the question and the branch note |
| `review` with `STUB_GH_FAIL="pr create"` | refused; `batch-1` at its old head; `main` has no new commit; the remote has no `batch-1` |
| `review` (b1 and b2 in one capability) | `https://github.com/ex/ctx/pull/1`. The `unbuilt:` conflict was settled (Deviation 1). The body names `parked: b3 "List quietly" (needs-input)` |
| **The PR's content** (`git diff main batch-1`) | **b3's `[g6]`/`[r7]` are in `spec/capabilities/work-queue.md` with `unbuilt: [r7]`, and its scenario is in `features/work-queue.feature`** (B1) |
| `merged` while gh says OPEN; after a local merge | refused twice (`OPEN, not merged`); then `batch-1 merged`, b1 and b2 `delivered`, worktrees gone, `batch-1-b1`/`-b2` deleted, `batch-1-b3` kept |
| b3 answered, then `work ready b3` | **`work-queue.md: 51: g6 appears a second time`, `52: r7 appears a second time`: b3 cannot be made ready** (B1) |
| Two items, both adding `shared.txt` | `review` refused: `CONFLICT (add/add)`; `batch-1` at its old head |
| Failing tests at review; a push to a missing remote | each refused with batch-1 at its old head; the tests' last lines shown |
| `abandon` with `STUB_GH_FAIL="pr close"`, then `abandon` | refused with `main` unchanged; then `abandoned`, items `ready`, branches kept, worktrees gone; a third `abandon` refused |
| A new batch after the abandon | starts; it prints `b2 renumbered: g4 -> g5` although b2 already had g5 (M1) |
| `park` with an uncommitted `wip.py` in the task's worktree | the file is gone (S2) |
| `review` with `<trees>/batch-2` an empty directory, not a worktree, and the base dirty | the review merged and reset **in the base checkout**: the person's uncommitted edit to `spec/index.md` and `.shop/delivery.toml` are lost (S1) |

## Findings

### Blocking

**B1. A parked item's requirement lines are published and merged, and the returned item cannot be readied again.**

- *Where:*
  - `scripts/batch_start.py:72-80`: one lines commit lays every picked item's blocks.
  - `scripts/batch_review.py:114-116`: the review merges only the in-batch items' branches onto that commit, and
    never takes a parked item's lines out.
  - `tests/scenarios/batches_world.py:154`: the scenario world's lines commit is `--allow-empty`.
- *Evidence:* see scratch repo `a` above.
  - b3 was parked, and the review published it.
  - `git diff main batch-1` holds b3's `### [g6] List quietly`, `[r7]`, `unbuilt: [r7]` and its scenario.
  - After `merged`, `main` carries r7 as an unbuilt requirement with an xfail scenario that nothing will build.
  - Once answered, b3 cannot be made `ready` again: `g6 appears a second time`, `r7 appears a second time`.
- *Against:*
  - design "Where a ready item's lines live": "The lines enter `spec/` with the batch's merge", meaning the merge of
    the delivered items;
  - "Keeping items separable": "An item parked … has its commits left out of the PR";
  - r7 and D5 ("its commits stay off the pull request").

  The lines commit cites b3 (`Item: b3`), so by the relation `commit cites item` it is a commit of b3, and it is
  published.
- *Why the suite passes:* the r7 scenario's lines commit is empty, and `test_a_parked_items_commits_are_not_published`
  checks only a commit made on b3's branch.
- *Fix:* in `batch_review.review`, before the merges, commit one change on `batch-<n>` that takes every task's item
  that is not `in-batch` out of `spec/`:
  - its groups and requirements removed (a new `backlog_lines.unlay(tree, item)`, the reverse of `lay_onto`);
  - its ids removed from `unbuilt:`;
  - the feature of each capability it touched generated again;
  - the message citing the parked items (`Item: b3`).

  Then the published branch carries only the in-batch items' lines. The item branches need nothing: they do not touch
  the parked item's lines.

  Tests:
  - a script test of park → review → `spec/` of `origin/batch-1` without the parked group → merged → answer → `ready`
    passes → `start` lays it again;
  - the world's `make_batch` lays real lines, so that r7 is not vacuous to this.

### Should fix

**S1. A directory at a worktree path that is not a worktree is used as one, and a failed review then wipes the base
checkout.**

- *Where:*
  - `scripts/batch_review.py:107-111`: `made` checks only `is_dir()`, then `git(tree, "rev-parse", "HEAD")`.
  - `scripts/batch_review.py:95-96`: `_put_back` runs `reset --hard` in that `tree`.
  - `scripts/batch_tasks.py:235`: `resume` checks `tree.exists()`.
  - `scripts/batch_tasks.py:270-272`: `done` checks `tree.is_dir()`.
- *Evidence:* scratch repo `b`, batch-2. `<trees>/batch-2` was made an empty directory, the base had an uncommitted
  edit, and the tests were set to fail.
  - `git` run in that directory found the base repository.
  - The merge happened in the base checkout, on `main`.
  - The put-back `reset --hard` then removed the person's uncommitted `spec/index.md` edit and `.shop/delivery.toml`.
    `git status --porcelain` came back empty.
  - `resume` has the same hole: it would print `running in <dir>` for a directory whose commits land on `main`.
- *Against:* the Global Constraint "The person's checkout … `git status --porcelain` shows only what was there
  before", and Review Focus 2.
- *Fix:* a `batch_git.is_tree(path, branch)` helper. It checks that `git -C path rev-parse --show-toplevel` is `path`
  and that `symbolic-ref --short HEAD` is `branch`.
  - `review`, `resume` and `done` use it in place of `exists()`/`is_dir()`.
  - An empty directory is removed and the worktree made again.
  - Anything else is refused, naming the path.

  Test: `review` and `resume` with an empty directory at the batch's and a task's tree path leave a dirty base
  checkout as it was.

**S2. `park`, `abandon` and `merged` remove task worktrees with `--force`, discarding uncommitted work without a
word.**

- *Where:*
  - `scripts/batch_tasks.py:327`;
  - `scripts/batch_close.py:161-164` (`_remove_trees`);
  - `scripts/batch_git.py:110` (`worktree remove --force`).
- *Evidence:* scratch repo `b`. A `wip.py` left in `batch-2-t1` was gone after `work batch park batch-2 b1`.
- *Against:* the park note says "its work is on branch batch-<n>-b<j>", but its uncommitted work is not. A subagent
  that returns a question mid-edit is the normal case for a park (skill step 5).
- *Fix:* `park` and `abandon` refuse a task worktree with uncommitted changes, naming the files and the worktree. The
  batch session commits them (with the `Item:` trailer) or passes `--discard`. `merged` may keep `--force`, since the
  work has been merged. Test: a park with an untracked file is refused, and nothing changes.

**S3. Two items that really conflict have no way through, and the skill says nothing about a refused review.**

- *Where:*
  - `scripts/batch_tasks.py:170-179`: `uncited` requires that same item's trailer on every commit of the branch.
  - `scripts/batch_review.py:82-86`.
  - `skills/building-a-batch/SKILL.md` step 6.
- *Evidence:* scratch repo `b`, where both tasks added `shared.txt`. The refusal is `CONFLICT (add/add) … into
  batch-1`.
  - To resolve it on the later item's branch, the session must merge in the earlier item's branch. Those commits cite
    the other item, so `uncited` refuses them.
  - Changing only the later branch works for this toy case (a rename), but not for two edits of one handler module,
    which the report itself expects ("Open problems").
  - Both tasks are `done`, and no command sets a done task back to running.
  - The skill's only guidance is about `done`.
- *Fix:*
  1. Skill step 6 says what to do on each refusal of `review`:
     - a conflict: resolve it on the later item's branch with a commit citing that item, or park one of the two;
     - failing tests: fix them on the item's branch that broke them, then review again;
     - a push or gh failure: fix the cause, then review again, since it is safe to rerun.
  2. Q2 below on whether `uncited` should accept a merge of an earlier in-batch item's branch.

**S4. The skill sends each subagent to `bdd-red-green`, which is written for `work run`'s implementer.**

- *Where:*
  - `skills/building-a-batch/SKILL.md` step 4;
  - `skills/bdd-red-green/SKILL.md:3,12,30,42-46,64,100-111`: a brief, a plan stage directory, a result file,
    `--work-item <name>`, "`work run` runs the whole suite", the 15-file budget, the `DONE`/`BLOCKED`/`PARTIAL`
    result.
- *Evidence:* a batch subagent has none of those things. It is told to "follow bdd-red-green", and the first thing
  that skill asks for is its brief. It also says the whole suite is not the subagent's to run. In a batch, `done` runs
  the suite and refuses with its tail, so the subagent will be sent back with a suite failure it was told to ignore.
- *Fix:* step 4 gives the subagent a short brief of its own:
  - its worktree, branch and ids;
  - how to run its scenarios (the generated `@r<n>` tags of `features/<cap>.feature`, through
    `tests/scenarios/test_<cap>.py`);
  - "there is no brief or result file: reply with what you built, or with your one question";
  - "`work batch done` runs the whole suite in your worktree";
  - which rules of `bdd-red-green` hold: red first, one scenario at a time, never edit a `.feature`, the test
    allowances.

  Alternatively, `bdd-red-green` gains a short "In a batch" section. Extend `test_skill_building_a_batch.py` to pin
  the sentence.

### Minor

- **M1. `start` reports an old renumbering as new.** `scripts/batch_start.py:126-128` prints the item's last
  `renumbered by work batch start:` note, whatever this pick did. Seen twice: after an abandon, and on the live-spec
  clone. Fix: `batch_pick.Pick` carries each picked item's pairs; print only those.
- **M2. `done` does not check the worktree again under the lock.** It checks for uncommitted changes before the tests,
  outside the lock. Under the lock it compares only the branch head. An uncommitted edit made while the tests ran is
  not noticed, so the task is `done` though the tests ran on files that are not committed. Where:
  `scripts/batch_tasks.py:272-275, 300-304`. Fix: repeat the `status --porcelain` check under the lock.
- **M3. The pick reads the base's working tree, but the lines are laid on its HEAD.** `batch_pick._alone` and
  `readiness_bar.check` read `root`'s `spec/` with any uncommitted edits. `_build` lays onto the worktree at `HEAD`.
  `start` ran with a modified `spec/index.md`. Fix: refuse `start` while `git status --porcelain -- spec/ features/`
  is not empty, naming the paths.
- **M4. Two refusals do not name their command:**
  - `batch-1 has no task t9` (`scripts/batch_plan.py:164`);
  - `work batch: gh pr create failed: …` (`batch_gh.py:147`), raised under `work batch review`.

  Fix: prefix the command, as the other refusals do.
- **M5. A gh failure after the pull request was created loses track of it.** If `pr create` fails after creating
  the pull request (a timeout, say), the put-back deletes the remote branch, and the orphaned pull request closes. A
  rerun creates a second one. Where: `scripts/batch_review.py:120-123`. Fix: on a create failure, ask
  `gh pr list --head batch-<n> --json url` before putting back. This is low priority.
- **M6. `batch_merge.settled` keeps only the ids on both sides.** `scripts/batch_merge.py:216` drops an id that one
  side added to `unbuilt:`. No task should add one, but the settle is then silently lossy. Fix: base ids kept by both
  sides, plus ids either side added. Add a unit test.

### Questions for the person (each with a recommended ruling)

- **Q1. A parked item's kept branch is never used again.** When the item returns, its next batch makes a new branch
  `batch-<m>-b<j>` from the new lines commit. The old `batch-<n>-b<j>` (named in the item's notes) is kept, but
  nothing wires it in. *Recommended:* accept for plan 4. Step 4 of the skill tells the subagent of a returning item to
  read the branch named in its notes and cherry-pick what still applies; the cherry-picks keep the `Item:` trailer.
  Wire it in when it recurs. This depends on B1's fix, without which the item never returns.
- **Q2. May an item's branch carry a merge of an earlier in-batch item's branch, to resolve a conflict?**
  *Recommended:* yes. `uncited` accepts a commit that cites any `in-batch` item of the same batch that is earlier in
  plan order, so a later branch may merge an earlier one. Since `review` merges in plan order, those commits are in
  the PR anyway. A parked item's commits are still refused. This keeps r13's traceability, and it gives S3 a path that
  works for edits to one shared module.

## The deviations, judged

| # | Deviation | Judgment |
|---|---|---|
| 1 | `batch_merge.py` settles the `unbuilt:` conflict of two items of one capability | **Accept.** It is a real plan defect: D6 makes every task edit one shared line. The settle is narrow: it sets the line aside, uses `git merge-file` for the rest, and refuses any other conflict, so a hand edit elsewhere is still refused. Verified on the scratch repo (b1, b2 in work-queue merged; a real add/add conflict refused with the branch put back). Fix M6 (an added id is dropped), and add a script test for it. |
| 2 | `done` runs its checks and tests outside the lock, then re-checks status and head under it | **Accept.** Holding the lock through a suite would make parallel subagents finish one at a time, which goes against goal 5. Verified: two 3 s dones took 3.2 s and both landed; a commit made during the tests was refused. The residual hole is M2 (uncommitted edits during the run). Reading `plan.md` unlocked is safe, since the re-read under the lock decides. |
| 3 | A failed review puts the remote back and removes a worktree it made | **Accept.** It is better than the plan. Verified for gh, push and test failures. S1 is the gap in the same code. |
| 4 | The merge When is a `local("WhenHappens", "pull request")` | **Accept.** It is test plumbing; supervision's fallback took the registry key. |
| 5 | The `ThenExitsErr` locals came in Task 3 | **Accept.** It was caught by the strict-xfail rule as intended (a vacuous XPASS made real). |
| 6 | Renumbering against `spec/` before the alone check | **Accept, with a caution.** It is right for ids a delivered batch took. But by B1, a parked-and-merged item's lines are a duplicate of *text*, not just of ids. `work ready` caught it, but only because the answered item went through `shaped`. Once B1 is fixed this cannot arise from a batch. |
| 7 | Files outside a task's list (backlog and taking-in-a-request sentences, `work show --json`'s `batch`) | **Accept.** Each change makes a sentence true that the plan made false. |
| 8 | Smaller choices | **Accept**, except that the "renumbered" note is reprinted (M1). The rest: the gh env as `<python> stub_gh.py`, `park` on any task status, `merged` committing before the cleanup with `branch -d` failures ignored, and failed gh calls not counted. |

## Other checks, no finding

- **Races:**
  - The lock is `fcntl.flock` on `<git common dir>/shop-batch.lock`, so it is shared by every worktree.
  - `start`, `resume`, `park`, `review`, `merged` and `abandon` hold it from the first read to the commit.
  - A `park` racing a `done` makes `done` refuse (the status is no longer `running`).
- **Failure paths:**
  - `start` removes its worktree and branch on any exception.
  - `abandon` with a failing gh changes nothing.
  - `merged` refuses an open pull request and a merge commit that has not been pulled.
- **Traceability:** the lines commit cites every item it carries. Each merge commit has `Item: b<j>`. The PR body
  lists each in-batch item with its ids and names each parked one. The task branches' commits are checked by `done`
  and `review`.
- **Old behaviour:** `test_supervision.py`, the requests, intake, backlog and readiness tests, and `test_work_*` pass.
  `supervise_worker` imports `git`/`GitFailed` back. `request_text.turned` keeps the old turn byte for byte without
  `## Counter-proposals`, which `test_request_counter.py` pins against the old function.
- **Design and spec:**
  - `work batch` starts no session (D2).
  - The batch state lives only on the base branch, and `done`/`review` refuse `.shop/` changes on task branches (D4).
  - One open batch at a time (D9).
  - `resume` reads no stdin, and no printed line ends in `?` (r5).
  - Nothing sets `building` from `in-review`, and `awaiting-merge` is never written: plan 5's, as the report says.
- **Code quality:** the modules are small (largest `batch_tasks.py`, 201 lines), each has a row, the boundaries are
  clear, and there are no imports from `supervise*` beyond the moved `git`. `batch_tasks.checked` and
  `batch_review.checked` repeat the `.shop/` and uncited checks with the same wording, which could be one helper.
