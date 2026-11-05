---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-4
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-05
status: draft
---

# Plan 4: Batches — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the `batches` capability, so that all 13 of its requirements are built: `work batch start` picks
ready, unblocked, passing items in rank order and lays their lines on a batch branch; each item is one task, built in
its own worktree; `work batch resume`, `done` and `park` carry the batch on from any session; `work batch review`
publishes the pull request; `work batch merged` and `abandon` close it. Each id leaves `unbuilt:` in the same commit
that makes its scenario pass. Alongside: the backlog shows how far a batch is along, `work depend --drop`, and a
request whose counter-proposal is settled can close (the plan-3 leftovers).

**Architecture:**
- **`work` keeps the state; the session orchestrates (D2).** `work batch` writes the plan, makes the worktrees and
  branches, runs the checks, pushes and calls `gh`. It starts no `claude -p`. The batch session, a Claude Code session
  following the new skill `building-a-batch`, dispatches one subagent for each running task, in parallel, the way
  superpowers' subagent-driven development does. So the suite tests every mechanic with git alone, a bare repository
  as the remote and a stand-in `gh`, with no network and no stand-in claude.
- **New modules behind `scripts/work`** (each ≤ 300 lines):
  - `batch_git.py`: git plumbing. `git` and `GitFailed` move here from `supervise_worker.py`, which imports them
    back. It also holds the lock, the worktrees and the push.
  - `batch_gh.py`: the `gh` calls.
  - `batch_plan.py`: the file `.shop/batches/<n>/plan.md`.
  - `batch_pick.py`: the pick.
  - `batch_start.py`: `work batch start`.
  - `batch_tasks.py`: `resume`, `done`, `park`, and the checks they share with the review.
  - `batch_review.py`: `work batch review`.
  - `batch_close.py`: `merged`, `abandon`.
  - `batch_cli.py`: the parsers and `status`.
  - `request_text.py`: the request text helpers, split out of `workqueue_request.py` (plan-3 M12).
- **Reused from plans 2-3:**
  - `backlog_items` (items, labels, commits) and `backlog_view.ordered` (rank).
  - `readiness_bar.check`, given `others` so it can lay a batch's items together.
  - `backlog_lines`, which gains `renumber` and `lay_onto`.
  - `spec_unbuilt` (strict xfail), which gains a writer.
  - `features_generate.generate`.
- **Reused from `supervise_*`:**
  - `git`/`GitFailed`, which are moved.
  - The patterns, rewritten small: a worktree under `.shop/worktrees/` with a self-ignoring directory, the
    branch-upstream-else-`origin` remote, and running the suite in the worktree before a merge.
  - Plan 9 deletes `supervise*.py`, `stub_claude.py` and the agents; nothing in this plan imports them.

**Tech Stack:** Python 3.11 (standard library: `tomllib`, `fcntl`, `subprocess`), git (worktrees, a bare remote in
tests), pytest, pytest-bdd and xdist, GF 3.12 with pgf and clingo (the bar). `gh` only through `$SHOPSYSTEM_WORK_GH`;
the suite uses `tests/scripts/stub_gh.py`.

**Spec:**
- Read first: `spec/capabilities/batches.md` (its 13 lines are the acceptance tests).
- The glossary entries of `spec/index.md` it uses: `batch`, `batch plan`, `task`, `pull request`, the statuses of
  item, batch and task with their transitions, `blocked`, `passing`, `pick`, `park`, `publish`, and the relations
  `item in batch`, `task of batch`, `pull request of batch`, `question on item`.
- `spec/capabilities/pr-review.md` (plan 5 builds it; this plan publishes the pull request it reviews).
- `.shop/records/2026-11-04-workflow-simplification/design.md` goal 5, with "Keeping items separable in a batch" and
  "Where a ready item's lines live".
- Read beside them:
  - `roadmap.md` (plan 4's row);
  - `plan-1-rulings.md` (the generator's dropped preconditions in r7, r8; M3: r5's weak "does not ask");
  - `plan-2-rulings.md` (Q1: `--drop` for plan 4; Q2: a negated Then);
  - `plan-3-rulings.md` "For plan 4", and `plan-3-implementation.md` "Open problems".

## Global Constraints

- **Branch:** `workflow-simplification`, from `3be6b387` or later (the main session's ruling: every plan on this one
  branch). No new branch, no push.
- **Shell rule (the person's):** never combine `cp` and `rm` in one command. They need the person's approval together.
  Run them as separate commands, or leave scratch directories under `/home/vscode/.claude/jobs/7e9ba079/tmp`.
  Keep shell variables few.
- **File size:** every tracked Python file stays at 300 lines or fewer (`python3 scripts/tools size --limit 300`).
  - `scripts/work` is at 211 lines and may grow by at most 5.
  - `tests/scenarios/backlog_handlers.py` is at 261 and may grow by at most 5.
  - `tests/scenarios/work_queue_world.py` is at 235 and may grow by at most 10.
- **Module map:** each new module gets a row in `CLAUDE.md`'s module map, in the task that creates it.
  - The new scenario modules join the `<capability>_handlers*.py` and `<capability>_world.py` rows.
  - `stub_gh.py` is named in the `tests/scripts/` row.
- **Strict xfail:** `spec_unbuilt.mark` is `strict=True`.
  - A task removes an id from `batches.md`'s `unbuilt:` in the same commit that makes its scenario pass, never
    before.
  - An `XPASS(strict)` a task does not name is read. If it tests its point, its id goes in that commit and the
    report says so. If it passes vacuously, the handler is fixed.
- **Spec lines:** no requirement line is edited or added.
  - In `batches.md` a task changes only `unbuilt:`, `## Implementation, may change` and a new `## Not yet`.
  - In `backlog.md`, `intake.md` and `requests.md`, only those prose sections.
  - In `spec/index.md`, only the one transition D13 adds (it was never merged; plan-1 ruling P10).
  - A line found wrong is reported, not changed.
- **No network:** no test reaches a network.
  - Pushes go to a bare repository on disk.
  - `gh` is `$SHOPSYSTEM_WORK_GH`, set to the stand-in by every fixture and world that runs a publishing command.
  - The script fixture also sets `GH_TOKEN=` and `GIT_TERMINAL_PROMPT=0`.
- **The person's checkout:** no batch command switches the branch of `--root`, or writes outside:
  - `.shop/backlog/`, `.shop/batches/` and the worktrees directory;
  - `.git` (refs, worktree admin, the lock);
  - the batch's own worktrees.

  `spec/` and `features/` of the base branch are never written. The lines enter `spec/` on the batch branch.
- **Refusals:** a refused command raises `workqueue.Refused`, and `scripts/work` prints `work: <message>` and exits 1.
  The base checkout is left byte-identical and the U3 check holds. What a refusal undoes on the batch branch is named
  in its task.
- **Names next to ids:** an item is named by `backlog_items.label`, a batch as `batch-<n>`, a task as
  `t<k> <item label>`, and a commit as `<short sha> "<subject>"` (design goal 10).
- **Old behaviour kept:**
  - `work outcome`, `turn` and `request` on a request with no `## Counter-proposals` behave byte for byte as before.
  - `test_requests.py`, `test_intake.py`, `test_backlog.py`, `test_readiness.py`, `test_supervision.py` and the
    `tests/scripts/test_work_*.py`, `test_backlog_*.py` and `test_intake_*.py` tests pass. Their only changes are
    the imports Task 8 renames.
- **Baselines** (measured at `3be6b387`). Every task keeps them, and none may get worse:
  - `python3 -m pytest -q`: `1153 passed, 1 skipped, 27 xfailed, 131 subtests passed`. Each built scenario moves from
    xfailed to passed, ending at `14 xfailed` with no failures.
  - `python3 -m pytest -m timing -n 0 -q`: `1 passed, 1181 deselected` (the deselected count grows with the suite).
  - Unbuilt ids (`spec_unbuilt.unbuilt`): 36, with no problems; at the end 23.
  - `python3 scripts/model check | tail -1`: `53 violations, 16 warnings, 19 unresolved references, 0 file problems`.
  - `python3 scripts/model logic | tail -1`: `11 findings: 6 L5, 5 L6`.
  - `python3 scripts/model lexicon --check | tail -1`: `401 terms, 0 problems`.
  - `python3 scripts/features generate --check`: exit 0. No feature file is regenerated by hand or edited.
  - `python3 scripts/features vocab --check | tail -1`: `every step has one handler`.
  - `python3 scripts/features bindings --unbound`: `every binding names a scenario`.
  - `python3 scripts/tools size --limit 300`: silent, exit 0.
- **Smoke steps** run `work` through a shell function, which bash and zsh both run:
  `r=$PWD; W() { python3 "$r/scripts/work" --root "$d" "$@"; }`.

## Decisions (decided by the planner; revisit)

The person was unavailable and asked not to be blocked. Each decision below was **decided by the planner, 2026-11-05;
revisit.**

| # | Decision |
|---|---|
| D1 | **Branch.** Built and committed on `workflow-simplification`, as the main session ruled. |
| D2 | **The session orchestrates; `work` keeps state.** `work batch` starts no `claude -p`. The skill `building-a-batch` is the batch session's instructions: `start`, then loop on `resume`, dispatching one subagent for each running task in parallel (each in its task's worktree), then `done` or `park` for each from the base checkout, then `review`. Why: design goal 5 asks for superpowers' execution model; it keeps no stage machinery; the suite needs no stand-in claude. Plan-3 D14's intake session started by `work backlog` stays unbuilt: the skill takes requests in first (D25). |
| D3 | **One task for each item.** Tasks are `t1`, `t2`, … in pick order. Task `t<k>` of item `b<j>` builds on the branch `batch-<n>-b<j>`, in the worktree `<trees>/batch-<n>-t<k>`. Finer tasks are the session's own, as subagents inside a task. Not yet: tasks finer than an item. |
| D4 | **One file holds the batch and its plan.** `.shop/batches/<n>/plan.md` (format below). The batch's state is committed on the **base branch** only (the branch `start` ran on). The batch and item branches never change `.shop/backlog/` or `.shop/batches/`: `done` and `review` refuse a branch that does, naming the paths. So the pull request's merge never conflicts with the batch's own records. |
| D5 | **Branches.** `batch-<n>` is made at the base's HEAD before `start` commits (`forked_from`). On it, one commit lays the lines. Each item branch starts at that commit. Item branches are merged into `batch-<n>` only by `review`, in plan order, `--no-ff`. A parked item's branch is never merged, so its commits stay off the pull request (r7). |
| D6 | **The lines enter `spec/` on the batch branch, at `start`.** Every picked item's blocks are laid with `backlog_lines.lay_onto`, its requirement ids are appended to the capability's `unbuilt:`, `features generate` runs for each capability laid, and one commit is made. A task is done when its item's ids have left `unbuilt:` and the tests pass in its worktree: the repository's own strict-xfail practice. The item file keeps its `## Requirements`. |
| D7 | **The pick.** Ready items are taken in rank order (`backlog_view.ordered`'s `ready` table), up to `batch_size`, a top-level key of `.shop/delivery.toml` (default 4).<br>- An item is blocked unless each dependency is `delivered` or picked earlier in this pick. The pick loops until it picks nothing more, so a dependency ranked lower is still picked first (the same-batch exception).<br>- Each candidate is checked alone (`readiness_bar.check`). One that fails goes back to `shaped`, its reasons under `## Notes` (r2).<br>- One that passes is renumbered (D8), then checked laid over the items picked before it. One that fails then is left out and stays `ready`, its reasons printed.<br>- With no `ready` item at all, `start` is refused. With ready items and none picked, the returns are committed, `no batch started` is printed and it exits 0. |
| D8 | **Id collisions.** `backlog_lines.renumber` gives an item's group and requirement ids new ones wherever they collide with its capability in `spec/` (groups, requirements, `retired:`) or with an item picked before it. The next free number is taken in file order, and the item gains a `## Notes` line `renumbered by work batch start: work-queue#r5 -> work-queue#r6`. This closes plan-3 D3. |
| D9 | **One open batch at a time** (`building`, `in-review` or `awaiting-merge`). `start` refuses while one is open, naming it. |
| D10 | **Citation.** A commit cites an item when its message has the line `Item: b<j>` (a git trailer). `done` and `review` refuse a commit on an item's branch since its start that does not cite it (r13), naming `<short sha> "<subject>"`. The lines commit and the merge commits cite every item they carry. |
| D11 | **Publishing.** `review` pushes `batch-<n>` with `git push -u <remote> batch-<n>`. The remote is the base's upstream remote, else `origin`. Then `gh pr create --draft --base <base> --head batch-<n> --title <title> --body <body>`, its URL kept as `pull_request`. The body cites each `in-batch` item as `- b<j> "<title>": <ids>` and names each parked one as `parked: b<j> "<title>" (needs-input)`. A batch that already has a `pull_request` (plan 5's fix loop) is pushed only. `gh` is `$SHOPSYSTEM_WORK_GH`, else `gh`. |
| D12 | **Tests.** A task's `done` and the `review` run `.shop/delivery.toml`'s `[batch] tests` (default `python3 -m pytest -q -p work_items`) in the worktree, with the plugin's scripts on `PYTHONPATH`. A failure is refused with the last 20 lines of the output. |
| D13 | **The merge** is recorded by `work batch merged <batch>`. `gh pr view` must give `MERGED`, and its merge commit must be in the base's HEAD history; otherwise it is refused, naming `git pull`. It takes a batch that is `in-review` or `awaiting-merge`: the glossary gains `in-review` → `merged`: merge (the person may merge before plan 5's review clears it; measured: `model logic` and `lexicon` unchanged). It sets every `in-batch` item `delivered` and the batch `merged`, removes the batch's worktrees, and deletes the merged item branches with `git branch -d`. |
| D14 | **Abandon** takes a `building` or `in-review` batch. It closes its pull request with `gh pr close` when it has one, refusing (nothing changed) if gh fails. Its `in-batch` items go to `ready`, its worktrees are removed and its branches are kept. |
| D15 | **Park:** `work batch park <batch> <item> --question TEXT`.<br>- The item goes from `in-batch` to `needs-input`, with `## Question` TEXT and the note `parked from batch-<n>; its work is on branch batch-<n>-b<j>`.<br>- Its task goes back to `pending` and its worktree is removed; the branch is kept.<br>- `review` leaves out every task whose item is not `in-batch`.<br>- The returned item goes to a later batch. |
| D16 | **Resume:** `work batch resume <batch>` reads the plan.<br>- Each `pending` task of an `in-batch` item gets its worktree (its branch made from the lines commit if missing) and becomes `running`.<br>- Each `running` task whose worktree is missing gets it back on its branch.<br>- It commits the plan when it changed and prints one line for each task. A running task's line names its worktree, its branch, its requirement ids, and the two commands that end it.<br>- It reads no stdin, and no line it prints ends in `?`. |
| D17 | **Locking.** Every batch command that commits holds an exclusive `fcntl.flock` on `<git common dir>/shop-batch.lock` from its first read to its commit, so parallel `done` calls from several subagents' results land one after another. |
| D18 | **The base branch.** `plan.md` keeps `base:`. Every batch command but `status` refuses when `--root`'s current branch is not the base: `work batch: batch-1 is built from main; run it on main, not <branch>`. A detached HEAD is refused by `start`. |
| D19 | **Worktrees.** They go in `.shop/delivery.toml`'s `[batch] worktrees` (relative to the root, or absolute), else `.shop/worktrees/`. The directory gets a `.gitignore` of `*` so the base checkout stays clean. |
| D20 | **The `gh` stand-in** is `tests/scripts/stub_gh.py`. It appends `{"argv": [...]}` to `$STUB_GH_CALLS`. For `pr create` it prints `https://github.com/ex/ctx/pull/<k>` (k counts creates). For `pr view <url> --json state,mergeCommit` it prints the entry for `<url>` in the JSON file `$STUB_GH_STATE`, else `{"state": "OPEN", "mergeCommit": null}`. For `pr close` it prints nothing. When `$STUB_GH_FAIL` equals `<sub> <sub2>` (`pr create`), that call exits 1 with `stand-in gh: refused`. |
| D21 | **The "is not" rule for batches** (plan-2 Q2 held a negated Then only to "the command exists"). A negated Then after a batch command requires exit 0. Under `work batch start` the world always adds its own ready, passing item (`i92`, line `SECOND` as `work-queue#r5`, so renumbering runs in every start scenario), so a batch starts. `backlog_handlers.item_is` asserts exit 0 when `context["strict_not"]` is set. |
| D22 | **The generator's dropped preconditions** (plan-1 rulings S2). r8's `every task of the batch is done` gives no Given, so the world's tasks are `done` unless a Given says otherwise, except under `work batch resume`, where they are `pending` so that resume has work. r7's commit is in its precondition already. |
| D23 | **`work_queue_world.local` chains.** A second registration of one (template, kind) key tries the new handler first and the earlier one when it returns False. Then batches can claim `ThenPrints item` and `ThenR question` beside the backlog's without replacing them. |
| D24 | **A counter-proposed request closes without a new line.** Measured on a copy of `spec/`: a controlled-language `countered` condition, used negated in a replacement of requests r20, gives two L1s (r21/r27 and r22/r27), because the solver follows a definition only where it is positive. So:<br>- `work outcome … rewritten --line` also writes `<n>. <m>` under a new request section `## Counter-proposals` (n the rewritten line, m its counter-proposal; `model_requests.SECTIONS` gains it).<br>- `request_text.turned(text)` reads every line listed there as no longer proposed (its counter-proposal is), so r20-r22 hold as written.<br>- A request without the section is unchanged.<br>- The turn rule is written once, in `turned`; `intake_moves.outcome` calls it (plan-3 "doubled turn rule").<br>- requests' `## Implementation, may change` says it, and intake's `## Not yet` bullet goes. |
| D25 | **Plan-3 leftovers.**<br>- M12: `request_text.py` holds the request text helpers as public names (`entries`, `with_entries`, `with_field`, `field`, `numbered`, `turned`, `SETTLED`), and `workqueue_request._refuse_upstream_part` becomes `refuse_upstream_part`.<br>- M9 (`_LineParser`'s class swap) is kept. It still works on 3.11; the alternatives change every subcommand's parsing, and plan 9 rewrites `scripts/work`'s parser when the old commands go.<br>- The intake session start (plan-3 D14) is not built (D2). `building-a-batch`'s first step takes in each request in the upstream's turn with `taking-in-a-request`.<br>- The rewording command (plan-3 S3) stays out. |
| D26 | **Batch progress in the backlog** (design goal 2).<br>- In the `in-batch` table, an item's `waiting on` cell gains `in batch-1 (building): 1 of 2 tasks done` (its batch is `batch_plan.of_item`).<br>- `--json` gives `batch: {"name", "status", "tasks_done", "tasks"}` only for an item in a batch, so every other row is as before.<br>- backlog's `## Not yet` bullet goes. |
| D27 | **`work depend B --drop A`** removes A from B's `depends_on` (a missing A included) and commits. It prints `b2 "…" no longer depends on b1 "…"` (or `b1 (missing)`). A dependency B lacks is refused. `--on` and `--drop` are mutually exclusive, and one is required. backlog's `## Not yet` bullet goes. |

**`plan.md`** (`batch_plan.render` writes exactly this; `parse` refuses any other shape as `<rel>: <field> ...`):

```
---
id: batch/ex.com/prod/ctx/batch-1
kind: batch
status: building
base: main
forked_from: 3be6b387e1c0ffee…
branch: batch-1
pull_request:
---

# batch-1

## Tasks

| task | item | status | branch |
|---|---|---|---|
| t1 | b3 | pending | batch-1-b3 |

## Plan

One task for each item: each builds its item's requirement lines, whose generated scenarios are its acceptance tests.
```

`## Plan` is free text, kept byte for byte (the session's notes).

## Review Focus

These are the input classes the spec implies but no generated scenario exercises, most likely to bite first. Each has
its test in the task named.

1. **Parallel subagents finishing together.** Two `work batch done` runs on two tasks at once should both land: two
   commits on the base branch, both tasks `done`, and no `index.lock` failure.
   Pinned in Task 4: `test_two_dones_at_once_both_land`.
2. **The person's checkout.** `start`, `resume` and `review` must leave the base checkout alone:
   - the current branch stays the same;
   - an uncommitted change elsewhere stays uncommitted;
   - `spec/` and `features/` of the base branch stay byte-identical;
   - `git status --porcelain` shows only what was there before.

   Pinned in Task 3 (`test_start_leaves_the_checkout_and_spec_alone`) and Task 5 (`test_review_leaves_the_checkout_alone`).
3. **A review that fails halfway.** A merge conflict between two items, a failing suite after the merges, a refused
   push, or a failing `gh pr create` should leave things as they were:
   - the batch stays `building`;
   - `batch-<n>` is at its head from before;
   - the base branch has no new commit.

   A rerun after the cause is fixed should publish.
   Pinned in Task 5: `test_a_failed_review_leaves_the_batch_building`, parametrised over the four causes.
4. **The wrong place or the wrong time:**
   - a batch command run from another branch;
   - `start` while a batch is open;
   - `resume`, `done` or `park` on a batch that is not `building`;
   - `done` on a task that is not `running`;
   - `park` on an item that is not in the batch.

   Each is refused, naming the branch, batch, status, task or item, with nothing changed.
   Pinned in Task 3 (`test_start_refuses_while_a_batch_is_open`, `test_start_refuses_a_detached_head`) and Task 4
   (`test_batch_commands_refuse_off_the_base_branch`, `test_moves_refuse_the_wrong_status`).
5. **A session that died mid-task.** The next session's `resume` should give the same branch, with the commits made
   so far, a worktree again if it was deleted, and the task still `running` (not reset to `pending`, not given a new
   branch).
   Pinned in Task 4: `test_resume_recreates_a_lost_worktree_with_its_commits`.

---

### Task 1: The plumbing — git, `gh` and the batch file

Builds no requirement. Every later task stands on it.

**Files:**
- Create: `scripts/batch_git.py`, `scripts/batch_gh.py`, `scripts/batch_plan.py`, `tests/scripts/stub_gh.py`,
  `tests/scripts/batch_testing.py`
- Modify:
  - `scripts/supervise_worker.py`: `GitFailed` and `git` deleted, and `from batch_git import GitFailed, git` in their
    place. Every `from supervise_worker import git` elsewhere keeps working.
  - `tests/scripts/conftest.py`: the fixture `batch_repo`.
  - `CLAUDE.md`: three rows, and `stub_gh.py` in the `tests/scripts/` row.
- Test: `tests/scripts/test_batch_plan.py`, `tests/scripts/test_batch_git.py`

**Interfaces:**
- Produces, in `batch_git.py`:
  - `class GitFailed(Refused)` and `git(root, *args) -> CompletedProcess`, moved verbatim.
  - `delivery(root) -> dict`: `.shop/delivery.toml` read with `tomllib`, `{}` when it is missing.
  - `scripts_env() -> dict`: `os.environ` with the plugin's `scripts/` last on `PYTHONPATH`.
  - `locked(root)`: a context manager (D17).
  - `current_branch(root) -> str | None`: None on a detached HEAD.
  - `trees_dir(root) -> Path`: D19, made with its `.gitignore`.
  - `add_tree(root, path, branch, start=None) -> Path`: an existing branch is checked out; otherwise
    `-b branch path start`.
  - `remove_tree(root, path) -> None`: `git worktree remove --force`, then `git worktree prune`. A missing path is no
    error.
  - `remote(root, branch) -> str`: `branch.<branch>.remote`, else `origin`.
  - `push(root, remote, branch) -> None`: refused as `work batch: the push of <branch> to <remote> failed: <git's
    reason>`.
- Produces, in `batch_gh.py`:
  - `GH = "SHOPSYSTEM_WORK_GH"`
  - `create(root, base, head, title, body) -> str`: the URL, the last line of stdout.
  - `state(root, url) -> tuple[str, str | None]`: (state, merge commit oid).
  - `close(root, url) -> None`.
  - A non-zero gh is refused as `work batch: gh <sub> <sub2> failed: <first line of its stderr>`.
- Produces, in `batch_plan.py`:
  - `BATCHES = Path(".shop/batches")`; `STATUSES = ("building", "in-review", "awaiting-merge", "merged",
    "abandoned")`; `OPEN = STATUSES[:3]`; `TASK_STATUSES = ("pending", "running", "done", "failed")`.
  - `@dataclass Task: task, item, status, branch`
  - `@dataclass Batch: name, ident, status, base, forked_from, branch, pull_request, tasks: list[Task], plan: str`
  - `is_batch(name) -> bool` (`batch-[1-9]\d*`).
  - `rel_of(name) -> str`: `.shop/batches/<n>/plan.md`.
  - `parse(text, rel) -> Batch` and `render(batch) -> str`, which round-trip.
  - `names(root)`, `batches(root)`, `find(root, name)`: find is refused as `there is no batch batch-9 in
    .shop/batches/`.
  - `open_batch(root) -> Batch | None`; `next_name(root) -> str`.
  - `task(batch, tid) -> Task`: refused as `batch-1 has no task t9`.
  - `of_item(root, item_name) -> Batch | None`: the highest-numbered batch whose tasks name the item.
  - `on_base(root, batch) -> None` (D18).
  - `commit(root, batch, items, message) -> None`: `plan.md` and each item's file written (`backlog_items.render`)
    and committed by `workqueue.committed`. The caller holds `locked`.
- Produces, in `tests/scripts/batch_testing.py` (beside `backlog_testing.py`):
  - `gh_env(where) -> dict`: the stand-in's env, with `STUB_GH_CALLS` and `STUB_GH_STATE` under `where`.
  - `gh_calls(where) -> list[list[str]]`.
  - `ready_item(repo, name, title, text)`: a `ready` item file with one line in `work-queue` g4/r5, committed.
  - `commit_on(repo, branch, path, text, message)`: in a throwaway worktree.
- `batch_repo` (conftest): `ready_repo` plus a bare repository beside it as `origin` (`main` pushed), plus
  `.shop/delivery.toml` holding `[batch]` with `tests = "python3 -c pass"`. With `monkeypatch`, it sets
  `SHOPSYSTEM_WORK_GH` to a script running `stub_gh.py`, and `GH_TOKEN=`, `GIT_TERMINAL_PROMPT=0`.

- [x] **Step 1: Write the failing tests.**
  - `test_batch_plan.py`:
    - `test_render_round_trips`: a Batch with two tasks and a two-line `## Plan`; `parse(render(b), rel) == b`, and
      the text equals the format above for the one-task case.
    - `test_malformed_plans_are_refused`: parametrised over a wrong `kind`, a status not in `STATUSES`, a task status
      not in `TASK_STATUSES`, a task row with three cells, a task id twice, and no `# ` heading. Each is refused
      naming `rel` and the field.
    - `test_next_name_open_batch_and_of_item`: with `batch-1` merged and `batch-2` building, `next_name` is
      `batch-3`, `open_batch` is `batch-2`, `of_item(root, "b3")` is the batch naming b3, and it is None for an item
      in no batch.
    - `test_a_file_not_named_by_number_is_refused`: `.shop/batches/x/plan.md` is refused by `names`.
    - `test_on_base_refuses_another_branch`: the message names the base and the current branch.
  - `test_batch_git.py`:
    - `test_git_still_imports_from_supervise_worker`: `supervise_worker.git is batch_git.git`.
    - `test_trees_dir_is_ignored`: after `trees_dir` and `add_tree`, `git status --porcelain` of the root is empty.
    - `test_add_tree_on_an_existing_branch_keeps_its_commits`, and `test_remove_tree_of_a_missing_path_is_quiet`.
    - `test_push_goes_to_the_bare_remote`: after `push`, `git ls-remote origin batch-1` gives the branch's head.
      `test_a_refused_push_names_git`: a remote path that does not exist is refused naming the branch and the
      remote.
    - `test_locked_serialises`: two processes each hold `locked` for 0.3 s and append their start and end times to a
      file; the two intervals do not overlap.
    - `test_gh_create_state_close_through_the_stand_in`: `create` returns `…/pull/1`; the calls file holds
      `["pr", "create", "--draft", "--base", "main", "--head", "batch-1", "--title", …]`; `state` gives `("OPEN",
      None)`, then after writing the state file `("MERGED", "abc")`; with `STUB_GH_FAIL="pr create"` it is refused
      naming `gh pr create`.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_batch_plan.py tests/scripts/test_batch_git.py -q`
  Expected: FAIL; the modules do not exist.

- [x] **Step 3: Implement the three modules and `stub_gh.py`, then move `git`/`GitFailed`.** `stub_gh.py` follows
  D20 and its docstring says so.

- [x] **Step 4: Run them, and the suite's supervision tests (the move).**
  Run: `python3 -m pytest tests/scripts/test_batch_plan.py tests/scripts/test_batch_git.py tests/scenarios/test_supervision.py -q | tail -1`
  Expected: all pass.

- [x] **Step 5: The baselines.**
  Run: `python3 -m pytest -q | tail -1; python3 scripts/tools size --limit 300; python3 scripts/tools check scripts/batch_git.py scripts/batch_gh.py scripts/batch_plan.py scripts/supervise_worker.py tests/scripts/stub_gh.py tests/scripts/batch_testing.py tests/scripts/test_batch_plan.py tests/scripts/test_batch_git.py tests/scripts/conftest.py`
  Expected: `27 xfailed`, no failures, passed = 1153 + the new tests; `size` silent; `check` clean.

- [x] **Step 6: Commit.**
  ```bash
  git add scripts/batch_git.py scripts/batch_gh.py scripts/batch_plan.py scripts/supervise_worker.py tests/scripts/stub_gh.py \
    tests/scripts/batch_testing.py tests/scripts/test_batch_plan.py tests/scripts/test_batch_git.py tests/scripts/conftest.py CLAUDE.md
  git commit -m "batches: git and gh plumbing, the batch file .shop/batches/<n>/plan.md, a stand-in gh"
  ```

### Task 2: The pick — rank, blocked, the bar again, renumbering

Builds no requirement on its own. Task 3's `start` is a commit around it.

**Files:**
- Create: `scripts/batch_pick.py`
- Modify:
  - `scripts/backlog_lines.py`: `lay_onto` and `renumber`. `lay` gains `others`.
  - `scripts/readiness_bar.py`: `check` and `well_formed` gain `others`.
  - `scripts/spec_unbuilt.py`: `with_unbuilt`.
  - `CLAUDE.md`: a row for `batch_pick.py`; the `spec_unbuilt` mention, if the map has one.
- Test: `tests/scripts/test_batch_pick.py`; additions to `tests/scripts/test_backlog_lines.py` and
  `tests/scripts/test_spec_unbuilt.py`.

**Interfaces:**
- Consumes: Task 1's `delivery`; `backlog_view.ordered`, `backlog_items.items`, `readiness_bar.check`.
- Produces:
  - `backlog_lines.lay_onto(into, item) -> list[str]`: lay's body without the copy, writing into `into/spec`.
  - `backlog_lines.lay(root, item, into, others=())`: copy, then `lay_onto` each of `others`, then `item`.
  - `backlog_lines.renumber(root, item, taken) -> list[tuple[str, str]]` (D8). `taken` is `{capability: set of ids}`
    and is updated in place; the item's `## Requirements` is rewritten; the result is the
    `("work-queue#r5", "work-queue#r6")` pairs, including groups as `work-queue#g4`.
  - `readiness_bar.check(root, item, others=())`: the item's own ids are the only `mine`.
  - `spec_unbuilt.with_unbuilt(text, ids) -> str`: a capability file's text with `ids` appended to `unbuilt:`, once
    each, in the order given. The key is written after `retired:` when missing.
  - `batch_pick.SIZE = 4`
  - `batch_pick.Pick = namedtuple("Pick", "picked returned left_out")`: `picked` holds Items in pick order;
    `returned` and `left_out` hold `(Item, reasons)`.
  - `batch_pick.pick(root, size=None) -> Pick`: D7, writing nothing. Returned items have `status="shaped"` and the
    note set on the Item; picked ones keep `ready`, and Task 3 moves them.

- [x] **Step 1: Write the failing tests.** Use `ready_repo`, `ABANDON` as the passing line, `SECOND` (``When the person
  runs `work abandon` on an initiative that is `started`, `work` shall exit successfully.``, measured to pass alone
  and together with `ABANDON`), and `FROBNICATE`.
  - `test_with_unbuilt_appends_and_inserts`: on a file with `unbuilt: [r1]`, `[r5]` gives `unbuilt: [r1, r5]`. On a
    file with no key, the key comes after `retired:`, and `spec_unbuilt.unbuilt` then reads it.
  - `test_renumber_moves_past_spec_and_taken`: an item with g4/r5. With `taken = {}`, nothing changes and `[]` is
    returned. With `taken = {"work-queue": {"g4", "r5"}}`, it gives g5/r6, the pairs, and `taken` holding both sets.
    With the fixture's `work-queue.md` given an `r6` and `retired: [r7]`, it gives r8.
  - `test_lay_with_others_lays_both`: the copy's `work-queue.md` has g4 and g5, and `root/spec` is unchanged.
  - `test_pick_takes_ready_items_in_rank_order_up_to_the_size`: five ready, passing items rated so their ranks are
    b3, b1, b5, b2, b4. `batch_size = 3` in delivery.toml gives picked `[b3, b1, b5]`, renumbered so their r ids
    differ.
  - `test_pick_returns_an_item_that_no_longer_passes`: b1 `FROBNICATE` is in `returned`, `status == "shaped"`, with a
    `## Notes` line naming `work batch start` and `frobnicate`; b2 is picked.
  - `test_a_blocked_item_is_not_picked`: b2 depends on an `idea` b9 and is in neither list; it stays `ready`.
  - `test_a_dependency_in_the_same_pick_does_not_block`: b1 (rank 1) depends on b2 (rank 2), both ready, giving
    picked `[b2, b1]`.
  - `test_a_dependency_fills_the_size_first`: the same with `batch_size = 1` gives picked `[b2]`. b1 is blocked in
    the first pass and the size is reached, so b1 stays `ready`, in no list.
  - `test_an_item_that_clashes_with_one_picked_is_left_out`: b1 `ABANDON`; b2 `CLASH` (``When the person runs `work
    abandon` on an initiative that is `started`, `work` shall set its status to `done`.``). The planner measured
    that `CLASH` passes alone and gives `L1 work-queue#r5 and #r6 clash` laid with `ABANDON`. b2 is in `left_out`
    with that `L1` reason and stays `ready`.
  - `test_pick_writes_nothing`: the tree and HEAD are unchanged.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_batch_pick.py tests/scripts/test_backlog_lines.py tests/scripts/test_spec_unbuilt.py -q`
  Expected: FAIL; `batch_pick` does not exist.

- [x] **Step 3: Implement.** The pick loops over the `ready` table until a pass picks nothing new. Each item is
  checked alone once, and laid with the picked once.

- [x] **Step 4: Run them and the readiness tests.**
  Run: `python3 -m pytest tests/scripts/test_batch_pick.py tests/scripts/test_backlog_lines.py tests/scripts/test_spec_unbuilt.py tests/scripts/test_readiness_bar.py tests/scenarios/test_readiness.py -q | tail -1`
  Expected: all pass.

- [x] **Step 5: The baselines.** The Task 1 command, with this task's files.
  Expected: `27 xfailed`, no failures; `size` silent; `check` clean.

- [x] **Step 6: Commit.**
  ```bash
  git add scripts/batch_pick.py scripts/backlog_lines.py scripts/readiness_bar.py scripts/spec_unbuilt.py \
    tests/scripts/test_batch_pick.py tests/scripts/test_backlog_lines.py tests/scripts/test_spec_unbuilt.py CLAUDE.md
  git commit -m "batches: the pick, ready items in rank order with the bar checked again together and ids renumbered"
  ```

### Task 3: `work batch start` and `work batch status`

Builds `batches#r1`-`r4`.

**Files:**
- Create:
  - `scripts/batch_start.py`, `scripts/batch_cli.py`
  - `tests/scenarios/batches_world.py`, `tests/scenarios/batches_handlers.py`
- Modify:
  - `scripts/work`: `import batch_cli`, `batch_cli.add_parsers(sub)` and `**batch_cli.COMMANDS`.
  - `tests/scenarios/work_queue_world.py`: `local` chains (D23).
  - `tests/scenarios/backlog_handlers.py`: `item_is` reads `strict_not` (D21).
  - `tests/scenarios/test_batches.py`: `bind_all(globals(), ROOT)` before `scenarios(...)`; the docstring names its
    handlers.
  - `spec/capabilities/batches.md`: `unbuilt: [r5, …, r13]`; `## Implementation, may change` gains the plan's
    format, branches (D5) and `batch_size`.
  - `CLAUDE.md`: rows for `batch_start.py` and `batch_cli.py`; `batches` in the handlers and world rows.
- Test: `tests/scripts/test_batch_start.py`

**Interfaces:**
- Consumes: Tasks 1-2.
- Produces:
  - `batch_start.start(root) -> tuple[Batch | None, Pick]`. Under `locked`:
    1. refuse a detached HEAD and an open batch (D9);
    2. `pick`;
    3. with picks: `batch-<n>` at HEAD, its worktree, the lines laid with ids into `unbuilt:` and `features generate`
       run, committed there as `batch-<n>: the requirement lines of <labels>` with one `Item:` line for each;
    4. then on the base, one commit of `plan.md` (tasks `pending`), the picked items `in-batch`, the renumbered and
       returned items: `work batch start: batch-<n> <labels>`.

    Without picks but with returns, only the returns are committed: `work batch start: no batch; <labels> -> shaped`.
    A failure after step 3 began removes the worktree and deletes the new branch before it re-raises.
  - `batch_cli.add_parsers(sub)`: the `batch` parser and its subparsers `start`, `status [batch] [--json]`, `resume
    batch`, `done batch task`, `park batch item --question TEXT`, `review batch`, `merged batch`, `abandon batch`.
    The ones later tasks build are added there.
  - `batch_cli.COMMANDS = {"batch": cmd_batch}`.
  - `batch_cli.status_text(root, batch) -> str`, which prints:
    - `batch-1 building, base main, pull request -`;
    - `plan: .shop/batches/1/plan.md`;
    - one `  <label> <status>` line for each item of its tasks;
    - one `  t<k> <label>: <status>, branch <branch>` line for each task.
  - `batch_cli.as_json(root, batch) -> dict`: `{"batch": {name, status, base, pull_request, plan, items: [{id, title,
    status}], tasks: [{task, item, status, branch}]}}`.
  - `start` prints:
    - `batch-1 building: t1 b1 "…", t2 b92 "…"`;
    - one line for each item returned (`<label> -> shaped: <first reason>`) or left out (`<label> left out: <first
      reason>`);
    - each renumbering.
- **The scenario world** (`batches_world.py`, loaded by path as `shop_batches_world`):
  - `outside(step) -> Path`: a directory beside `step.repo`, holding the bare remote, the stand-in `bin/gh` and its
    files.
  - `env(step) -> dict`: Task 1's `gh_env`.
  - `prepare(step)`: once, `codify`, `.shop/delivery.toml`, `init`, and the remote with `main` pushed.
  - `own_item(step)`: D21's `i92`.
  - `make_batch(step, name, status, items, tasks)`: writes `plan.md` by hand in the format above. It makes `batch-1`
    from `main` with a lines commit, and one branch for each item, each with one commit `Item: b<j>` adding
    `src/b<j>.txt`. `context["commits"]` maps a scenario's `c<k>` to its sha, and `context["batches"]` maps `b1` to
    `batch-1`.
  - `ensure_batch(step)`: before a When that is not `start`, every batch, task, commit and pull request the scenario
    names is built:
    - D22's task defaults;
    - the world's own in-batch item (with a cited commit and a `done` task) when no item the scenario names is
      `in-batch` (r7's parked item, r8's and r12's batches with no item);
    - an item given `in-batch` with no batch put in the batch `b1`;
    - a pull request making the batch `in-review` with `pull_request` set.
- **Handlers** (`batches_handlers.py`; split as `batches_handlers_more.py` if it nears 300):
  - registry: `WhenRuns` for `` `work batch start` `` and `` `work batch status` ``; `GivenK batch`, `GivenK_A batch`,
    `GivenK task`, `GivenK_A task`, `GivenR in`, `ThenK_A batch`.
  - `OF_GIVENS` gains `"task"`.
  - `local("ThenDoes", "batch")` and `local("ThenDoes", "batch plan")`: the last run created and committed a
    `plan.md`, bound to the scenario's name.
  - `local("ThenPrints", "task")`, and `local("ThenPrints", "item")` (chained; it returns False unless the last run
    was a `work batch` command): the item's label, the task's `t<k>` line, and `status of the task` as that line's
    status word.
  - The `start` handler sets `context["strict_not"]`.

- [x] **Step 1: Write the failing script tests** (`test_batch_start.py`, on `batch_repo`):
  - `test_start_writes_the_batch_the_branch_and_the_lines`: b1 `ABANDON` and b2 `SECOND`, both ready.
    - Exit 0. HEAD's commit holds exactly `.shop/batches/1/plan.md`, `.shop/backlog/b1.md` and
      `.shop/backlog/b2.md`. Both items are `in-batch`, and the plan has t1 b1 and t2 b2 `pending`.
    - `git show batch-1:spec/capabilities/work-queue.md` has g4/r5 and g5/r6, with `unbuilt: [r5, r6]`.
    - `git show batch-1:features/work-queue.feature` has `@r5` and `@r6`.
    - The message of `batch-1`'s head has `Item: b1` and `Item: b2`.
    - b2's notes name its renumbering.
  - `test_start_leaves_the_checkout_and_spec_alone` (Review Focus 2): an uncommitted edit to `notes.txt` is still
    there and uncommitted. `spec/` and `features/` of `main` are byte-identical to before. The current branch is
    `main`. `git status --porcelain` is ` M notes.txt` alone.
  - `test_start_refuses_while_a_batch_is_open` and `test_start_refuses_a_detached_head` (Review Focus 4): refused
    naming `batch-1 "building"` or the detached HEAD, with HEAD, the tree and the branches unchanged.
  - `test_start_with_no_ready_item_is_refused`; `test_start_with_only_returns_commits_them`: b1 `FROBNICATE` gives
    exit 0, `no batch started`, b1 `shaped`, no `.shop/batches/`, and no branch `batch-1`.
  - `test_status_prints_items_tasks_and_their_statuses`, and `test_status_json_is_one_object`.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_batch_start.py -q`
  Expected: FAIL; `work` has no `batch` command.

- [x] **Step 3: Implement `batch_start.py`, `batch_cli.py`'s `start` and `status`, and the `scripts/work` lines.**

- [x] **Step 4: Run the script tests.**
  Run: `python3 -m pytest tests/scripts/test_batch_start.py tests/scripts/test_batch_pick.py -q | tail -1`
  Expected: all pass.

- [x] **Step 5: Write the world and the handlers, bind `test_batches.py`, and remove r1-r4 from `unbuilt:`.**
  Run: `python3 -m pytest tests/scenarios/test_batches.py -q -rxX -n 0 | tail -15`
  Expected: r1-r4 passed; r5-r13 xfailed (no XPASS).

- [x] **Step 6: Check that each scenario fails for its point** (in a scratch edit, reverted):
  - With `start` not moving items, r1 fails.
  - With the bar's alone-check skipped, r2 fails.
  - With `blocked` ignored, r3 fails, on exit 0 and the item `in-batch`.
  - With status not printing the task's status, r4 fails.

  Record each in the report.

- [x] **Step 7: The baselines.**
  Run: `python3 -m pytest -q | tail -1; python3 scripts/model check | tail -1; python3 scripts/features vocab --check | tail -1; python3 scripts/features generate --check; python3 scripts/tools size --limit 300`
  Expected: `23 xfailed`, no failures; the rest at baseline; `size` silent.

- [x] **Step 8: Commit.**
  ```bash
  git add scripts/batch_start.py scripts/batch_cli.py scripts/work tests/scenarios/batches_world.py tests/scenarios/batches_handlers*.py \
    tests/scenarios/work_queue_world.py tests/scenarios/backlog_handlers.py tests/scenarios/test_batches.py \
    tests/scripts/test_batch_start.py spec/capabilities/batches.md CLAUDE.md
  git commit -m "batches: work batch start picks and lays the lines on batch-<n>, work batch status (batches r1-r4)"
  ```

### Task 4: `resume`, `done` and `park` — the tasks in their worktrees

Builds `batches#r5` and `r6`.

**Files:**
- Create: `scripts/batch_tasks.py`
- Modify:
  - `scripts/batch_cli.py`: `resume`, `done`, `park`.
  - `tests/scenarios/batches_handlers*.py`: `WhenRuns` for `` `work batch resume` ``; `WhenHappens park`;
    `ThenDoes use`; the chained `local("ThenR", "question")`; `local("ThenDoes", "question")`.
  - `spec/capabilities/batches.md`: r5 and r6 out of `unbuilt:`; the citation and tests keys in `## Implementation,
    may change`.
  - `CLAUDE.md`: a row for `batch_tasks.py`.
- Test: `tests/scripts/test_batch_tasks.py`

**Interfaces:**
- Consumes: Tasks 1-3.
- Produces, in `batch_tasks.py`:
  - `resume(root, name) -> list[tuple[Task, Path | None]]` (D16).
  - `done(root, name, tid) -> Task`, which checks in this order and refuses at the first failure:
    1. the batch is `building`;
    2. the task is `running`;
    3. its worktree has no uncommitted change (`.shop/scratch` aside);
    4. no commit on the branch since the lines commit changes `.shop/backlog/` or `.shop/batches/`;
    5. every such commit cites the item (D10);
    6. none of the item's ids is in `unbuilt:` in the worktree;
    7. the tests pass (D12).

    Then the task is `done`, committed on the base as `work batch done: batch-1 t1 b3 "…"`. The worktree is kept
    until the review.
  - `park(root, name, item_name, question) -> Item` (D15).
  - Shared with Task 5:
    - `lines_commit(root, batch) -> str`: the batch branch's first commit after `forked_from`.
    - `uncited(root, since, branch, item_name) -> list[str]`: `<short sha> "<subject>"` of each.
    - `under_shop(root, since, branch) -> list[str]`: the paths.
    - `run_tests(root, tree) -> CompletedProcess`.
    - `item_ids(root, item) -> list[str]`.
- `resume` prints:
  - `batch-1 building: plan .shop/batches/1/plan.md`;
  - for each task: `t1 b3 "…": running in <worktree> on batch-1-b3: build work-queue#r5, work-queue#r6; then work
    batch done batch-1 t1, or work batch park batch-1 b3 --question <text>`;
  - `t2 b4 "…": done`, or `t2 b4 "…": parked (needs-input)`.

- [x] **Step 1: Write the failing script tests** (`test_batch_tasks.py`, on a batch started from `batch_repo`):
  - `test_resume_makes_worktrees_and_runs_pending_tasks`: both tasks are `running`, both worktrees exist on
    `batch-1-b1`/`batch-1-b2` at the lines commit, the plan's commit is on `main`, and a second `resume` changes
    nothing and commits nothing.
  - `test_resume_recreates_a_lost_worktree_with_its_commits` (Review Focus 5): after a cited commit on
    `batch-1-b1`, the worktree is removed by `git worktree remove --force` and pruned. `resume` gives it back on
    `batch-1-b1` with that commit at HEAD, and t1 is still `running`.
  - `test_resume_asks_nothing`: run with stdin at `/dev/null`, no output line ends with `?`.
  - `test_done_marks_the_task_done`: in t1's worktree, `unbuilt:` loses r5 and a commit cites `Item: b1`. `done`
    exits 0 and t1 is `done`.
  - `test_done_refuses`: parametrised over the cases below. Each is refused naming what it names, with the plan
    unchanged:
    - not running (`t1 b1 "…" is pending`);
    - an uncommitted file (its path);
    - a commit changing `.shop/backlog/b1.md` (the path);
    - an uncited commit (`<sha> "<subject>"`);
    - r5 still unbuilt (`work-queue#r5`);
    - `tests = "python3 -c 'import sys; sys.exit(3)'"` (the command and exit 3).
  - `test_two_dones_at_once_both_land` (Review Focus 1): both tasks are made doneable, and two `work batch done`
    processes start together. Both exit 0, both tasks are `done`, and `main` has two new commits.
  - `test_park_parks_the_item_and_keeps_the_rest`: `park batch-1 b1 --question "Which reading?"` gives:
    - b1 `needs-input` with `## Question` and the branch note;
    - t1 `pending`, with its worktree gone and branch `batch-1-b1` kept;
    - the batch `building`, and t2 untouched;
    - a later `resume` that leaves t1 pending and prints it `parked (needs-input)`.
  - `test_batch_commands_refuse_off_the_base_branch` and `test_moves_refuse_the_wrong_status` (Review Focus 4):
    `resume`/`done`/`park` on an `abandoned` batch (written by hand), `park` of an item not in the batch, and
    `done` from a checkout on another branch. Each is refused naming it, with nothing changed.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_batch_tasks.py -q`
  Expected: FAIL; `batch_tasks` does not exist.

- [x] **Step 3: Implement `batch_tasks.py` and the three parsers.**

- [x] **Step 4: Run them.**
  Run: `python3 -m pytest tests/scripts/test_batch_tasks.py -q | tail -1`
  Expected: all pass.

- [x] **Step 5: The handlers, and r5 and r6 out of `unbuilt:`.**
  - r5's `ThenDoes use` is the run naming `plan.md`, every task of the plan by `t<k>`, and its pending task now
    `running` with a worktree.
  - `ThenDoesNot ask` is readiness's `asks_nothing`.
  - r6's handlers: the item file gained `## Question` (`ThenDoes write question`); it is on that item (`ThenR on`);
    the batch is not `abandoned`, with exit 0.

  Run: `python3 -m pytest tests/scenarios/test_batches.py -q -rxX -n 0 | tail -12`
  Expected: r1-r6 passed; r7-r13 xfailed.

- [x] **Step 6: Mutations,** each reverted: `resume` printing `Carry on?` fails r5, and `park` setting the batch
  `abandoned` fails r6. Record them.

- [x] **Step 7: The baselines** (Task 3's Step 7 command).
  Expected: `21 xfailed`, no failures.

- [x] **Step 8: Commit.**
  ```bash
  git add scripts/batch_tasks.py scripts/batch_cli.py tests/scenarios/batches_handlers*.py tests/scripts/test_batch_tasks.py \
    spec/capabilities/batches.md CLAUDE.md
  git commit -m "batches: work batch resume, done and park, one task an item in its worktree (batches r5, r6)"
  ```

### Task 5: `work batch review` publishes the pull request

Builds `batches#r7`, `r8`, `r11`, `r12` and `r13`.

**Files:**
- Create: `scripts/batch_review.py`
- Modify:
  - `scripts/batch_cli.py`: `review`.
  - `tests/scenarios/batches_handlers*.py`, with these handlers:
    - `WhenRuns` `` `work batch review` ``;
    - `GivenK commit`, `GivenK_C commit`, `GivenK pull request`;
    - `OF_GIVENS` `commit` and `pull request`;
    - `ThenDoes publish`, `ThenDoesNot publish`, `ThenR cites`;
    - `local("ThenR", "pull request")`, `local("ThenExitsErr", "task")`, `local("ThenExitsErr", "commit")`.
  - `spec/capabilities/batches.md`: the five ids out; D11 in `## Implementation, may change`.
  - `CLAUDE.md`: a row for `batch_review.py`.
- Test: `tests/scripts/test_batch_review.py`

**Interfaces:**
- Consumes: Tasks 1-4.
- Produces: `batch_review.review(root, name) -> str`, the pull request's URL. Under `locked`, in this order:
  1. the batch is `building` and `on_base`;
  2. every task of an `in-batch` item is `done` (r12), refused as `work batch review: batch-1: t1 b3 "…" is running,
     not done`, one line for each;
  3. at least one item is `in-batch`;
  4. `uncited` and `under_shop` for each in-batch item's branch (r13);
  5. in the batch worktree (re-made if missing), each in-batch item's branch merged `--no-ff`, with the message
     `batch-1: b3 "…"` and `Item: b3`; a conflict runs `git merge --abort` and is refused naming the item;
  6. `run_tests` there;
  7. `push`;
  8. `gh` create, unless `pull_request` is set;
  9. `in-review` and `pull_request` committed on the base as `work batch review: batch-1 -> in-review <url>`.

  A refusal at steps 5-8 resets `batch-<n>` to its head from before (`git reset --hard` in the batch worktree) and
  commits nothing.
- `batch_review.title(batch, items) -> str`: `batch-1: <title>; <title>`. `batch_review.body(root, batch) -> str`
  (D11).

- [x] **Step 1: Write the failing script tests** (`test_batch_review.py`, on a batch with both tasks done):
  - `test_review_publishes_the_pull_request`:
    - Exit 0, printing `https://github.com/ex/ctx/pull/1`.
    - The batch is `in-review` with that `pull_request`.
    - `git ls-remote origin batch-1` equals the local `batch-1`, which holds both items' commits.
    - The gh call is `pr create --draft --base main --head batch-1`, and its `--body` cites `b1 "…"` and `b2 "…"`.
  - `test_a_parked_items_commits_are_not_published`: with b2 parked, b2's commit is not in `git rev-list
    origin/batch-1`, and the body names `parked: b2`.
  - `test_review_refuses_a_task_not_done` and `test_review_refuses_an_uncited_commit`: refused, naming `t2 b2 "…"`
    or `<sha> "<subject>"`. Nothing is pushed (`ls-remote` empty), no gh call is made, and HEAD is unchanged.
  - `test_a_failed_review_leaves_the_batch_building` (Review Focus 3), parametrised:
    - (a) both items change `src/shared.txt` differently;
    - (b) the tests fail after the merge;
    - (c) the remote is a path that does not exist;
    - (d) `STUB_GH_FAIL="pr create"`.

    Each is refused naming the item, the command, the push or `gh pr create`. The batch is `building`, `batch-1` is
    at its head from before, and `main`'s HEAD is unchanged. For (d), a rerun after unsetting `STUB_GH_FAIL`
    publishes.
  - `test_a_second_review_pushes_only`: with `pull_request` set and the batch `building`, a new commit on `batch-1-b1`
    (the fix) is pushed, no `pr create` call is made, and the batch is `in-review`.
  - `test_review_leaves_the_checkout_alone` (Review Focus 2).

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_batch_review.py -q`
  Expected: FAIL; `review` does not exist.

- [x] **Step 3: Implement `batch_review.py` and the parser.**

- [x] **Step 4: Run them.**
  Run: `python3 -m pytest tests/scripts/test_batch_review.py -q | tail -1`
  Expected: all pass.

- [x] **Step 5: The handlers, and r7, r8, r11, r12, r13 out of `unbuilt:`.**
  - `ThenDoes publish`: the stand-in's `pr create` call, and the remote's `batch-1`.
  - `ThenR of pull request`: its `--head` is the batch's branch.
  - `ThenDoesNot publish commit`: the commit's sha is not reachable from the remote's `batch-1`, and the command
    exited 0.
  - `ThenR cites`: the `--body` holds the item's label.
  - The `ThenExitsErr` locals: exit 1, naming `t1` or the commit's short sha. They also assert that nothing was
    pushed and no gh call was made.

  Run: `python3 -m pytest tests/scenarios/test_batches.py -q -rxX -n 0 | tail -6`
  Expected: r1-r8 and r11-r13 passed; r9, r10 xfailed.

- [x] **Step 6: Mutations,** each reverted:
  - merging a parked item's branch fails r7;
  - leaving the label out of the body fails r11;
  - skipping the task check fails r12;
  - skipping `uncited` fails r13.

- [x] **Step 7: The baselines.** Expected: `16 xfailed`, no failures.

- [x] **Step 8: Commit.**
  ```bash
  git add scripts/batch_review.py scripts/batch_cli.py tests/scenarios/batches_handlers*.py tests/scripts/test_batch_review.py \
    spec/capabilities/batches.md CLAUDE.md
  git commit -m "batches: work batch review merges the in-batch items and publishes the pull request (batches r7, r8, r11-r13)"
  ```

### Task 6: `work batch merged` and `work batch abandon`

Builds `batches#r9` and `r10`.

**Files:**
- Create: `scripts/batch_close.py`
- Modify:
  - `scripts/batch_cli.py`: `merged`, `abandon`.
  - `spec/index.md`: the transition `` `in-review` → `merged`: merge; `` after the `awaiting-merge` one (D13). It is
    the only glossary change.
  - `tests/scenarios/batches_handlers*.py`: `WhenHappens merge` (the world merges `batch-1` into `main` with `--no-ff`,
    writes the stand-in's state `MERGED` with that merge's sha, then runs `work batch merged batch-1`), and `WhenRuns`
    `` `work batch abandon` ``.
  - `spec/capabilities/batches.md`: `unbuilt: []`, `## Implementation, may change` (D13, D14), and a new `## Not
    yet`:
    - tasks finer than an item (D3);
    - a task `failed` by a command;
    - the delivered item's request resolved (`work resolve`) at the merge;
    - the session `work` would start (D2).
  - `CLAUDE.md`: a row for `batch_close.py`.
- Test: `tests/scripts/test_batch_close.py`

**Interfaces:**
- Produces: `batch_close.merged(root, name) -> Batch` (D13) and `batch_close.abandon(root, name) -> Batch` (D14). Each
  is one commit on the base: `work batch merged: batch-1 -> merged; <labels> delivered`, or `work batch abandon:
  batch-1 -> abandoned; <labels> -> ready`.

- [x] **Step 1: Write the failing script tests:**
  - `test_merged_delivers_the_in_batch_items`:
    - After a review, the test merges `batch-1` into `main` and writes the stand-in's state.
    - `merged` gives b1 and b2 `delivered` and the batch `merged`; a parked b3 stays `needs-input`.
    - The worktrees are gone and `batch-1-b1` is deleted.
    - `spec/capabilities/work-queue.md` on `main` now has r5 and r6 (the merge brought them).
  - `test_merged_refuses_an_open_pull_request` (state `OPEN`, naming it) and `test_merged_refuses_a_merge_not_pulled`
    (a merge sha not in `main`'s history, naming `git pull`). Nothing is changed in either.
  - `test_abandon_returns_the_items` (building): b1 and b2 `ready`, the batch `abandoned`, the worktrees gone and
    the branches kept.
  - `test_abandon_closes_the_pull_request` (in-review): a `pr close <url>` call. With `STUB_GH_FAIL="pr close"` it is
    refused and nothing is changed.
  - `test_abandon_refuses_a_merged_batch`.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_batch_close.py -q`
  Expected: FAIL.

- [x] **Step 3: Implement, and the glossary transition.**
  Run: `python3 scripts/model logic | tail -1; python3 scripts/model lexicon --check | tail -1`
  Expected: `11 findings: 6 L5, 5 L6` and `401 terms, 0 problems`, as measured by the planner.

- [x] **Step 4: The handlers, and r9, r10 out of `unbuilt:`.**
  Run: `python3 -m pytest tests/scripts/test_batch_close.py tests/scenarios/test_batches.py -q -rxX -n 0 | tail -3`
  Expected: all pass; all 13 batches scenarios passed.

- [x] **Step 5: Mutations,** each reverted: `merged` not moving items fails r9; `abandon` leaving items `in-batch`
  fails r10.

- [x] **Step 6: The baselines.** Expected: `14 xfailed`, no failures; `model check` at baseline.

- [x] **Step 7: Commit.**
  ```bash
  git add scripts/batch_close.py scripts/batch_cli.py spec/index.md tests/scenarios/batches_handlers*.py \
    tests/scripts/test_batch_close.py spec/capabilities/batches.md CLAUDE.md
  git commit -m "batches: work batch merged delivers, work batch abandon returns the items (batches r9, r10)"
  ```

### Task 7: The backlog — a batch's progress, `work depend --drop`

Builds no new requirement; closes backlog's two plan-4 `## Not yet` bullets (D26, D27).

**Files:**
- Modify:
  - `scripts/backlog_view.py`: the progress cell and the `batch` JSON key.
  - `scripts/backlog_moves.py`: `undepend`.
  - `scripts/backlog_cli.py`: `depend`'s `--on | --drop`.
  - `spec/capabilities/backlog.md`: `## Not yet` loses the two bullets, and `## Implementation, may change` names
    both.
- Test: `tests/scripts/test_backlog_view.py`, `tests/scripts/test_backlog_moves.py` (additions only).

**Interfaces:**
- `backlog_view.progress(root, item) -> dict | None`: `{"name", "status", "tasks_done", "tasks"}` of
  `batch_plan.of_item`, counting the item's batch's tasks.
- `backlog_moves.undepend(root, name, on) -> Item`.

- [x] **Step 1: Failing tests:**
  - `test_an_in_batch_item_shows_its_batch`: the row's `waiting on` cell holds `in batch-1 (building): 1 of 2 tasks
    done`, and `--json`'s row has `batch` with those four values.
  - `test_rows_of_items_in_no_batch_are_unchanged`: the JSON keys of an `idea` row are exactly as before.
  - `test_drop_removes_a_dependency`: b2 on b1, then `--drop b1`, gives `depends_on: []`, the printed line, and one
    commit.
  - `test_drop_of_a_missing_item`: b2 depends on `b9`, which has no file; dropping it prints `b9 (missing)`.
  - `test_drop_refuses_one_it_lacks`.
  - `test_depend_takes_on_or_drop`: neither, or both, is a usage error (exit 2).

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_backlog_view.py tests/scripts/test_backlog_moves.py -q`
  Expected: the new tests fail.

- [x] **Step 3: Implement.**

- [x] **Step 4: Run them and the backlog scenarios.**
  Run: `python3 -m pytest tests/scripts/test_backlog_view.py tests/scripts/test_backlog_moves.py tests/scenarios/test_backlog.py -q | tail -1`
  Expected: all pass.

- [x] **Step 5: The baselines.** Expected: `14 xfailed`, no failures.

- [x] **Step 6: Commit.**
  ```bash
  git add scripts/backlog_view.py scripts/backlog_moves.py scripts/backlog_cli.py spec/capabilities/backlog.md \
    tests/scripts/test_backlog_view.py tests/scripts/test_backlog_moves.py
  git commit -m "backlog: an item in a batch shows how far the batch is along; work depend --drop"
  ```

### Task 8: A request whose counter-proposal is settled closes; `request_text.py`

Builds no new requirement (D24). It closes plan-3 S4, the doubled turn rule and M12.

**Files:**
- Create: `scripts/request_text.py`
- Modify:
  - `scripts/workqueue_request.py`: it imports the helpers; `turn` calls `turned`; `refuse_upstream_part` is public.
  - `scripts/intake_moves.py`: public imports; the rewritten path writes `## Counter-proposals` and calls `turned`.
  - `scripts/readiness_bar.py`: `request_text.entries` if it used `_entries`.
  - `scripts/model_requests.py`: `SECTIONS` gains `Counter-proposals`.
  - `tests/scripts/test_intake_outcome.py`, `tests/scenarios/intake_handlers.py`: `workqueue_request._entries`
    becomes `request_text.entries`, and nothing else changes.
  - `spec/capabilities/requests.md`: a bullet in `## Implementation, may change`. `spec/capabilities/intake.md`:
    the `## Not yet` bullet on counter-proposals goes, and `## Implementation, may change` names the section.
  - `CLAUDE.md`: a row for `request_text.py`; the `workqueue_request.py` row.
- Test: `tests/scripts/test_request_counter.py`

**Interfaces:**
- `request_text`: `SETTLED`; `COUNTERS = "Counter-proposals"`; `entries(text, name)`, `with_entries(text, name,
  entries)`, `with_field(text, field, value)`, `field(text, field)`, `numbered(entries, number, text)`, moved
  unchanged.
- `countered(text) -> set[str]`: the numbers n of `## Counter-proposals`' `<n>. <m>` entries.
- `turned(text) -> str`: `turn`'s edit, verbatim, but with the lines in `countered(text)` left out of the
  Lines/Outcomes count.

- [x] **Step 1: Failing tests** (`test_request_counter.py`, on `ready_repo` with a peer's request taken in):
  - `test_a_counter_proposed_request_closes`:
    1. line 1 is `rewritten --line <ABANDON>`, so line 2 appears and `## Counter-proposals` holds `1. 2`;
    2. the asker's `work turn`;
    3. `outcome q1 2 accepted --into work-queue`;
    4. `work turn` gives `status: accepted`, with the turn still the upstream's (r21).
  - `test_without_the_section_turn_is_as_before`: a request whose line 1 is `rewritten` with no section. `work turn`
    gives `awaiting-asker`, with bytes equal to what the old `turn` gives on a copy (the old function kept in the
    test as text).
  - `test_the_rewritten_path_and_turn_share_one_rule`: `intake_moves` holds no `"awaiting-asker"` literal.
  - `test_model_check_takes_the_section`: `model --root <repo> check` names no problem with `q1.md`.

- [x] **Step 2: Run them to verify they fail.**
  Run: `python3 -m pytest tests/scripts/test_request_counter.py -q`
  Expected: FAIL.

- [x] **Step 3: Implement.**

- [x] **Step 4: Run every request and intake test.**
  Run: `python3 -m pytest tests/scripts/test_request_counter.py tests/scripts/test_intake_outcome.py tests/scripts/test_intake_moves.py tests/scenarios/test_requests.py tests/scenarios/test_intake.py tests/scripts/test_work_*.py -q | tail -1`
  Expected: all pass.

- [x] **Step 5: The baselines,** with `model check` (it reads request sections). Expected: at baseline, `14 xfailed`.

- [x] **Step 6: Commit.**
  ```bash
  git add scripts/request_text.py scripts/workqueue_request.py scripts/intake_moves.py scripts/readiness_bar.py scripts/model_requests.py \
    tests/scripts/test_request_counter.py tests/scripts/test_intake_outcome.py tests/scenarios/intake_handlers.py \
    spec/capabilities/requests.md spec/capabilities/intake.md CLAUDE.md
  git commit -m "requests: a request whose counter-proposals are settled closes; the turn rule written once in request_text"
  ```

### Task 9: The batch session's skill, `building-a-batch`

Builds no requirement. It is how the loop runs without a person (D2).

**Files:**
- Create: `skills/building-a-batch/SKILL.md`, `tests/scripts/test_skill_building_a_batch.py`
- Modify:
  - `tests/scripts/test_skill_shaping_items.py`: its command check reads the three skills.
  - `README.md`: the skills list.
  - `spec/capabilities/intake.md`: `## Not yet`'s intake-session bullet says the batch session takes requests in
    first (D25).

**The skill:**
- **Frontmatter:**
  - `name: building-a-batch`
  - `description: Use when the person asks to build, run or carry on a batch, or to build what is ready in the
    backlog, in a repository with .shop/backlog/; also when a session starts with a batch building.`
- **Process:**
  1. Take each request in the upstream's turn with `taking-in-a-request`.
  2. `work batch start`, or `work batch status` to find the open batch.
  3. `work batch resume <batch>`.
  4. For each running task, dispatch one subagent, all at once.
     - Each subagent is given its worktree, the item file, its requirement ids, `bdd-red-green` and
       `CLAUDE.md`.
     - It builds the scenarios one at a time, removes each id from `unbuilt:` as its scenario passes, and commits
       with `Item: b<j>`.
  5. For each subagent that returns, from the base checkout, run `work batch done <batch> <task>`, or `work batch
     park <batch> <item> --question "<its question>"` when it could not finish without an answer. A refused `done`
     goes back to the same subagent with the refusal.
  6. When every task of an in-batch item is done, run `work batch review <batch>`, and give the person the pull
     request's link.
  7. A later session starts again at step 2.
- **The rule:** nothing waits on the person between steps 1 and 6.

- [x] **Step 1: Failing test** (`test_skill_building_a_batch.py`):
  - `test_the_process_runs_the_batch_commands_in_order`: `work batch start`, `work batch resume`, `work batch done`,
    `work batch park` and `work batch review` are named in that order in the Process.
  - `test_tasks_are_dispatched_in_parallel_with_their_trailer`: it says `subagent`, `worktree`, `in parallel` (or `at
    once`) and `Item: b`.
  - `test_nothing_waits_on_the_person`: no step before the one naming `work batch review` holds "ask the person" or
    "wait for".
  - `test_description_starts_use_when` (name equals the directory).

- [x] **Step 2: Run it to verify it fails.**
  Run: `python3 -m pytest tests/scripts/test_skill_building_a_batch.py -q`
  Expected: FAIL.

- [x] **Step 3: Write the skill.**

- [x] **Step 4: Run it, the skills' command check and the agents' test.**
  Run: `python3 -m pytest tests/scripts/test_skill_building_a_batch.py tests/scripts/test_skill_shaping_items.py tests/scripts/test_agents.py -q | tail -1`
  Expected: all pass.

- [x] **Step 5: Commit.**
  ```bash
  git add skills/building-a-batch/SKILL.md tests/scripts/test_skill_building_a_batch.py tests/scripts/test_skill_shaping_items.py \
    README.md spec/capabilities/intake.md
  git commit -m "skills: building-a-batch, the batch session that starts, resumes, dispatches a subagent a task and publishes"
  ```

### Task 10: Whole-plan verification and records

**Files:**
- Create: `.shop/records/2026-11-04-workflow-simplification/plan-4-implementation.md`
- Modify: `.shop/records/README.md` (a row for the report); this plan (every box ticked)

- [ ] **Step 1: Every requirement of the plan is built.**
  Run: `python3 -c "import sys; sys.path.insert(0,'scripts'); import pathlib, spec_unbuilt as u; d=u.unbuilt(pathlib.Path('.')); print('batches' in d, sum(map(len,d.values())), u.problems(pathlib.Path('.')))"`
  Expected: `False 23 []` (36 − 13).

- [ ] **Step 2: The baselines, all at once.**
  Run: `python3 -m pytest -q | tail -2; python3 -m pytest -m timing -n 0 -q | tail -1; python3 scripts/model check | tail -1; python3 scripts/model logic | tail -1; python3 scripts/model lexicon --check | tail -1; python3 scripts/features generate --check; python3 scripts/features vocab --check | tail -1; python3 scripts/features bindings --unbound; python3 scripts/tools size --limit 300; python3 scripts/tools check $(git diff --name-only 3be6b387...HEAD -- '*.py' scripts/work)`
  Expected:
  - the suite: `14 xfailed`, no failures, passed = 1153 + 13 + the new script tests;
  - the timing run: `1 passed`;
  - `model check`: `53 violations, 16 warnings, 19 unresolved references, 0 file problems`;
  - `model logic`: `11 findings: 6 L5, 5 L6`;
  - the lexicon: `401 terms, 0 problems`;
  - `generate --check`: exit 0;
  - `vocab --check`: `every step has one handler`;
  - `bindings --unbound`: `every binding names a scenario`;
  - `size`: silent;
  - `check`: nothing to report.

- [ ] **Step 3: A smoke run of the whole loop** in a scratch repository under the job's tmp directory, in bash. Each
  `cp` and each `rm` is its own command (the person's rule).
  ```bash
  d=$(mktemp -d -p /home/vscode/.claude/jobs/7e9ba079/tmp) && git -C "$d" init -q -b main && git -C "$d" config user.name t && git -C "$d" config user.email t@example.com
  cp -r tests/scripts/fixtures/generate/repo/spec "$d/"
  rm "$d/spec/capabilities/legacy.md"
  sed -i 's#^id: bounded-context/.*#id: bounded-context/ex.com/prod/ctx#' "$d/spec/index.md"
  mkdir -p "$d/.shop" && printf '[batch]\ntests = "python3 -c pass"\n' > "$d/.shop/delivery.toml"
  git -C "$d" add -A && git -C "$d" commit -qm init && git init -q --bare "$d.git" && git -C "$d" remote add origin "$d.git" && git -C "$d" push -q origin main
  export SHOPSYSTEM_WORK_GH="$PWD/tests/scripts/stub_gh.py" STUB_GH_CALLS="$d.calls" STUB_GH_STATE="$d.state"
  r=$PWD; W() { python3 "$r/scripts/work" --root "$d" "$@"; }
  W idea "Abandon a started initiative" && W shape b1 && W line b1 --into work-queue 'When the person runs `work abandon` on an initiative that is `started`, `work` shall set its status to `abandoned`.' && W ready b1
  W idea "Abandon quietly" && W shape b2 && W line b2 --into work-queue 'When the person runs `work abandon` on an initiative that is `started`, `work` shall exit successfully.' && W ready b2
  time W batch start && W backlog && W batch resume batch-1
  ```
  Then, for each task: in its worktree, take its ids out of `unbuilt:` in `spec/capabilities/work-queue.md` and commit
  with `-m "build b<j>" -m "Item: b<j>"`; then `W batch done batch-1 t<k>`. Then:
  ```bash
  W batch review batch-1 && W batch status batch-1
  git -C "$d" merge -q --no-ff batch-1 -m "merge the pull request" && printf '{"https://github.com/ex/ctx/pull/1": {"state": "MERGED", "mergeCommit": {"oid": "%s"}}}' "$(git -C "$d" rev-parse HEAD)" > "$d.state"
  W batch merged batch-1 && W backlog
  ```
  `stub_gh.py` must be executable (`chmod +x` in Task 1) and start with `#!/usr/bin/env python3`. Expected:
  - `start` prints `batch-1 building` with both tasks and b2's renumbering (record its time);
  - `resume` prints two `running in` lines;
  - `review` prints `https://github.com/ex/ctx/pull/1`;
  - `merged` delivers b1 and b2, and `work backlog`'s `delivered (2)` table holds them;
  - `git -C "$d" status --porcelain` is empty;
  - `main`'s `spec/capabilities/work-queue.md` has r5 and r6 with `unbuilt` empty of them.

- [ ] **Step 4: Write the implementation report** at `plan-4-implementation.md`, in `plan-3-implementation.md`'s form
  (no frontmatter):
  - Final state: each Step 2 figure as measured, and the smoke run's times.
  - The commits: a table of each task's commit, what was done and its verification, the mutations included.
  - Deviations, each with its reason.
  - D1-D27, each kept or changed.
  - Open problems for plan 5 and later.
  - Files.

- [ ] **Step 5: Index the records.** Add a row to `.shop/records/README.md` after the row for `plan-4-batches.md`:
  `| \`2026-11-04-workflow-simplification/plan-4-implementation.md\` | plan 4 executed: batches built (\`work batch start\`, \`status\`, \`resume\`, \`done\`, \`park\`, \`review\`, \`merged\`, \`abandon\`; one task an item in its worktree, the pull request published through gh), the backlog's batch progress and \`work depend --drop\`, a counter-proposed request closing, the building-a-batch skill, 13 requirements out of \`unbuilt:\` | report |`.
  Tick every box of this plan.

- [ ] **Step 6: Commit.**
  ```bash
  git add .shop/records/2026-11-04-workflow-simplification/plan-4-implementation.md .shop/records/README.md \
    .shop/records/2026-11-04-workflow-simplification/plan-4-batches.md
  git commit -m "records: plan 4 verified, its implementation report"
  ```
  The end-of-branch review follows, by a separate reviewer, into `plan-4-review.md`. It reads `<this plan's
  commit>..HEAD` on `workflow-simplification` against this plan's Review Focus.
