---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/batches
title: Batches
narrator: a person or session building a batch
group: service
language: codified-2
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: [g1, r1, g2, r2, g3, r3, g4, r4, g5, r5, g6, r6, g7, r7, g8, r8, g10, r10, g12, r12, g13, r13, g16, r16, g17, r17, g18, r18, g19, r19]
unbuilt: [r9, r11, r14, r15, r22, r23, r24, r25, r26, r27, r28, r29, r30, r31, r32, r33, r34, r35, r36]
---

# Batches

## Purpose
Ready items are built together in batches, like a sprint (design goal 5): a batch takes several ready, unblocked items
in rank order, which may be unrelated, writes its own plan of tasks and builds them on one branch closed by one pull
request. The plan and each task's status are on disk, so a session can stop and any later session carry on. A
question while building parks its item and the rest of the batch carries on. The person merges; the merge delivers.

## Terms
- **batch brief** (noun): the brief `work batch start` writes for the one fresh agent that runs the batch: the batch, its tasks and worktrees, the skill it follows, the rules and the lessons, and where it stops. Kind of: file.
- **review folder** (noun): the scratch directory `batch-<n>-review-<k>` under the batch's worktrees directory, which `work batch brief` writes a review's brief and change into and where the review's findings are saved, and which is never committed. Kind of: file.
- **readiness bar** (noun): the checks `work ready` makes of an item on a copy of `spec/` with its lines laid in. This: the readiness bar of the plugin that runs the command. Kind of: thing.
- **pass** (verb, state): an item meets every check of the readiness bar. Forms: passes, passed. Frame: item passes readiness bar.
- **pass** (verb, state): the test that binds a scenario passes when it runs in a worktree. Forms: passes, passed. Frame: scenario passes in worktree.
- **fail** (verb, state): the test that binds a scenario fails when it runs in a worktree. Forms: fails, failed. Frame: scenario fails in worktree.
- **cite** (verb, state): a commit's message or a pull request's body names an item by its `Item: b<n>` line. Forms: cites, cited. Frame: commit cites item. Frame: pull request cites item.

## Relations
| from | word | to | cardinality |
|---|---|---|---|
| review folder | of | batch | one |
| scenario | of | item | one |
| batch plan | of | batch | one |
| commit | in | pull request |  |
| commit | of | git branch | one |
| requirement | of | item |  |
| requirement | in | git branch |  |
| task | of | item | one |
| worktree | of | task | one |
| git branch | of | batch | one |

## Behaviour

### [g9] The merge delivers
- [r9] While an item in a batch is `in-batch`, when the person merges the pull request of the batch, `work` shall set the status of the item to `delivered` and set the status of the batch to `merged`.

### [g11] The pull request cites its items
- [r11] While an item in a batch is `in-batch`, when the person runs `work batch review` on the batch, `work` shall publish a pull request that cites the item.

### [g14] `work batch start` writes the batch brief for a fresh agent
- [r14] When the person runs `work batch start`, `work` shall write a batch brief and print the batch brief.

### [g15] `work batch abandon` removes the batch's review folders
- [r15] When the person runs `work batch abandon` on a batch, `work` shall remove every review folder of the batch.

### [g22] `work batch start` picks a ready item that passes the readiness bar and has no dependency on an item that is not delivered
- [r22] While an item is `ready` and the item passes the readiness bar and the item has no dependency on an item whose status is not `delivered`, when the person runs `work batch start`, `work` shall pick the item, set the status of the item to `in-batch`, write a batch whose status is `building` and write a batch plan of the batch.

### [g23] A ready item that no longer passes the readiness bar is returned
- [r23] While an item is `ready` and the item does not pass the readiness bar, when the person runs `work batch start`, `work` shall set the status of the item to `shaped`.

### [g24] A ready item with a dependency on an item that is neither ready nor delivered is not picked
- [r24] While an item is not `ready` or `delivered` and a dependency on the item exists and another item whose status is `ready` has the dependency, when the person runs `work batch start`, `work` shall not pick the item.

### [g25] `work batch resume` carries on without a person
- [r25] While a batch is `building`, when a session runs `work batch resume` on the batch, `work` shall use the batch plan of the batch and ask no question.

### [g26] `work batch park` parks an item and leaves the rest building
- [r26] While an item in a batch is `in-batch`, when a session runs `work batch park` on the item, `work` shall set the status of the item to `needs-input`, write a question on the item and not set the status of the batch to `abandoned`.

### [g27] A parked item's commits stay out of the pull request
- [r27] While an item in a batch is `needs-input` and a commit cites the item, when the person runs `work batch review` on the batch, `work` shall publish a pull request of the batch that does not hold the commit.

### [g28] `work batch abandon` returns the batch's items
- [r28] While a batch is `building`, when the person runs `work batch abandon` on the batch, `work` shall set the status of the batch to `abandoned` and set the status of every item in the batch whose status is `in-batch` to `ready`.

### [g29] `work batch review` refuses a batch with a task that is not done
- [r29] While a task of a batch is not `done`, if the person runs `work batch review` on the batch, then `work` shall refuse the command and name the task.

### [g30] `work batch review` refuses a commit that cites no item
- [r30] While a git branch of a task of a batch has a commit that cites no item, if the person runs `work batch review` on the batch, then `work` shall refuse the command and name the commit.

### [g31] The merge removes the batch's review folders
- [r31] When the person merges a pull request of a batch, `work` shall remove every review folder of the batch.

### [g32] `work batch park` takes the parked item's lines out of the batch
- [r32] While an item in a batch is `in-batch` and the git branch of the batch holds a requirement of the item, when a session runs `work batch park` on the item, `work` shall remove the requirement from the git branch.

### [g33] A parked item's failing scenario does not hold up another item's task
- [r33] While an item in a batch is `in-batch` and a task of the item is `running` and an item in the batch is `needs-input` and a scenario of the item fails in the worktree of the task, when a session runs `work batch done` on the task, `work` shall set the status of the task to `done`.

### [g34] Another item's passing scenario does not hold up a task
- [r34] While an item in a batch is `in-batch` and a task of the item is `running` and another item in the batch is `in-batch` and a scenario of the item passes in the worktree of the task, when a session runs `work batch done` on the task, `work` shall set the status of the task to `done`.

### [g35] `work batch review` publishes the pull request
- [r35] While a batch is `building` and every task of the batch is `done`, when the person runs `work batch review` on the batch, `work` shall publish a pull request of the batch and set the status of the batch to `in-review`.

### [g36] `work batch status` prints where the batch stands
- [r36] While a batch holds an item and the batch has a task, when the person runs `work batch status` on the batch, `work` shall print the item, the task and the status of the task.

## Implementation, may change

- `work batch start` takes the ready items in rank order (the backlog's WSJF, ties to the item added first), up to
  `batch_size` of `.shop/delivery.toml` (a new key, default 4).
- A batch keeps each item's commits apart (one worktree or one commit series an item); a parked item's commits stay on
  its own branch for when it returns.
- The batch and its plan are one file, `.shop/batches/<n>/plan.md`: frontmatter `id`, `kind: batch`, `status`,
  `base` (the branch `work batch start` ran on), `forked_from` (the base's commit the batch branch starts at),
  `branch` and `pull_request`; a `# batch-<n>` heading; a `## Tasks` table `| task | item | status | branch |`, one
  task `t<k>` for each item in pick order; and a `## Plan` kept as written. It is committed on the base branch only,
  with the items it moves; the batch and item branches never change `.shop/backlog/` or `.shop/batches/`.
- `work batch start` makes the branch `batch-<n>` at the base's HEAD and, in a worktree of its own under
  `.shop/worktrees/` (`[batch] worktrees` of `.shop/delivery.toml`), commits on it every picked item's lines laid
  into `spec/`, their ids appended to the capability's `unbuilt:`, and each service capability's feature generated
  again, with one `Item: b<j>` line for each item. Each item's task builds on the branch `batch-<n>-b<j>`, which
  starts at that commit; the item branches are merged into `batch-<n>` only by `work batch review`.
- Once the batch is laid, `work batch start` writes the batch brief `batch-<n>-driver/brief.md` under the worktrees
  directory, never committed, and prints its path: the batch, its base checkout, each task with its worktree, branch,
  item and requirement ids, the skill `building-a-batch`, the prefix of every push and gh call (`[batch] push` of
  `.shop/delivery.toml`, a string, when given), the rules every subagent is given, where the agent stops
  (`awaiting-merge`: no merge, no `work batch merged`) and what it replies. `work batch merged` and
  `work batch abandon` remove the folder `batch-<n>-driver/` with the batch's worktrees.
- Each picked item is checked by the readiness bar again, alone and then laid over the items picked before it; one
  that no longer passes alone goes back to `shaped` with its reasons under `## Notes`, one that clashes with those
  picked stays `ready`. An item's ids that collide with its capability's or with an item picked before it are
  renumbered, with a `## Notes` line naming each change. One batch is open (`building`, `in-review` or
  `awaiting-merge`) at a time.
- A commit cites an item when its message has the line `Item: b<j>` (a git trailer). `work batch done` and `work
  batch review` refuse a commit on an item's branch since the lines commit that cites no item, and one that changes
  `.shop/backlog/` or `.shop/batches/`, naming the commit as `<short sha> "<subject>"` or the path.
- A task is done when its item's ids have left `unbuilt:` in its worktree and the tests pass there: `[batch] tests` of
  `.shop/delivery.toml`, default `python3 -m pytest -q -p work_items`, run with the plugin's scripts on PYTHONPATH.
  `work batch resume` gives each pending task of an `in-batch` item its worktree `batch-<n>-t<k>` and sets it
  `running`; a parked item's task goes back to `pending`, its branch kept for when the item returns.
- `work batch review` merges each `in-batch` item's branch into `batch-<n>` with `--no-ff`, in plan order, in the
  batch's worktree; two items of one capability each take their own ids out of its one `unbuilt:` line, and that
  conflict alone is settled by the merge, any other refuses. It runs the tests there, pushes `batch-<n>` with `git
  push -u` to the base branch's upstream remote (else `origin`), and creates a draft pull request with `gh pr create
  --draft`, its body naming each `in-batch` item with its requirement ids and each parked one; a batch that has a
  pull request already is pushed only; once a review of it is recorded, each commit on an `in-batch` item's branch
  after that review's head must cite an open finding of its item (`Finding: f<m>`) and each open finding must have
  such a commit, else the review is refused, naming the commit or the finding (pr-review's fix loop). gh is `$SHOPSYSTEM_WORK_GH`, else `gh`. A review refused while merging,
  testing, pushing or creating puts the batch branch, and the remote's, back where they were.
- The merge is recorded by `work batch merged <batch>`, on a batch that is `in-review` or `awaiting-merge`: gh must
  say the pull request is `MERGED`, and its merge commit must be in the base branch's history (else `git pull`
  first). It sets every `in-batch` item `delivered` and the batch `merged`, removes the batch's worktrees and
  deletes the merged item branches. `work batch abandon` takes a batch that is `building` or `in-review`: it closes
  the pull request when there is one (refused, with nothing changed, if gh fails), sets every `in-batch` item `ready`
  and the batch `abandoned`, removes the worktrees and keeps the branches.

## Not yet
- Tasks finer than an item: a batch has one task for each item, and the batch session splits a task further among
  its own subagents.
- A task set `failed` by a command.
- The request a delivered item was taken in from resolved (`work resolve`) at the merge.
- A session `work` starts itself: the batch session is a Claude Code session following the `building-a-batch`
  skill, and `work batch` keeps the state.
