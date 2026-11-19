---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/batches-0-37
title: Batches
narrator: a person or session building a batch
group: service
language: codified-2
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: [g1, r1, g2, r2, g3, r3, g4, r4, g5, r5, g6, r6, g7, r7, g8, r8, g10, r10, g12, r12, g13, r13, g16, r16, g17, r17, g18, r18, g19, r19, g27, r27, g33, r33, g9, r9, g11, r11, g14, r14, g15, r15, g22, r22, g23, r23, g24, r24, g25, r25, g26, r26, g37, r37, g28, r28, g29, r29, g30, r30, g31, r31, g32, r32, g38, r38, g34, r34, g35, r35, g36, r36, g39, r39, g40, r40, g42, r42, g43, r43, g41, r41, g44, r44, g45, r45, g46, r46, g47, r47, g48, r48, g49, r49]
unbuilt: []
---

# Batches

## Purpose
Ready items are built together in batches, like a sprint (design goal 5): a batch takes several ready, unblocked items
in rank order, which may be unrelated, writes its own plan of tasks and builds them on one branch closed by one pull
request. The plan and each task's status are on disk, so a session can stop and any later session carry on. A
question while building parks its item and the rest of the batch carries on. The person merges; the merge delivers.

## Terms

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Relations

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Behaviour

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
- `work accept` records on the item it makes which line of the request each of its requirements came from, as
  `request_lines: [<cap>#r<n>=<k>, ...]` in the item's frontmatter, kept under the new ids when a batch renumbers
  them. After the merge is recorded, `work batch merged` resolves the request of each delivered item taken in from
  one by `work resolve`'s path, each recorded line delivered as `<cap>#r<n> <merge commit>`, and prints
  `<q> resolved: delivered by <item>`. A request that is not `accepted`, an item that records no line of it, or a
  resolve that is refused is left alone and named as `<q> not resolved (<why>); run work resolve`, for a later
  `work resolve`.
- A chore item's task names its chore in place of requirement ids: `work batch resume` prints the chore's files and
  check where it prints an item's ids, and the batch brief `work batch start` writes, and the brief `work batch brief`
  writes for `pr-reviewer`, hold the chore's files and check under the item. `work batch done` runs the check in the
  task's worktree after the tests (b316).

## Not yet
- Tasks finer than an item: a batch has one task for each item, and the batch session splits a task further among
  its own subagents.
- A task set `failed` by a command.
- A session `work` starts itself: the batch session is a Claude Code session following the `building-a-batch`
  skill, and `work batch` keeps the state.
## Moved

Every line moved to a new capability with a new id (the domain contract, 0.38.0).

| old | new |
|---|---|
| g9 | batches#g50 |
| r9 | batches#r50 |
| g11 | reviews#g1 |
| r11 | reviews#r1 |
| g14 | batches#g51 |
| r14 | batches#r51 |
| g15 | batches#g52 |
| r15 | batches#r52 |
| g22 | batches#g53 |
| r22 | batches#r53 |
| g23 | batches#g54 |
| r23 | batches#r54 |
| g24 | batches#g55 |
| r24 | batches#r55 |
| g25 | batches#g56 |
| r25 | batches#r56 |
| g26 | batches#g57 |
| r26 | batches#r57 |
| g37 | reviews#g2 |
| r37 | reviews#r2 |
| g28 | batches#g58 |
| r28 | batches#r58 |
| g29 | reviews#g3 |
| r29 | reviews#r3 |
| g30 | reviews#g4 |
| r30 | reviews#r4 |
| g31 | batches#g59 |
| r31 | batches#r59 |
| g32 | batches#g60 |
| r32 | batches#r60 |
| g38 | batches#g61 |
| r38 | batches#r61 |
| g34 | batches#g62 |
| r34 | batches#r62 |
| g35 | reviews#g5 |
| r35 | reviews#r5 |
| g36 | batches#g63 |
| r36 | batches#r63 |
| g39 | batches#g64 |
| r39 | batches#r64 |
| g40 | batches#g65 |
| r40 | batches#r65 |
| g42 | batches#g66 |
| r42 | batches#r66 |
| g43 | batches#g67 |
| r43 | batches#r67 |
| g41 | batches#g68 |
| r41 | batches#r68 |
| g44 | batches#g69 |
| r44 | batches#r69 |
| g45 | batches#g70 |
| r45 | batches#r70 |
| g46 | batches#g71 |
| r46 | batches#r71 |
| g47 | batches#g72 |
| r47 | batches#r72 |
| g48 | batches#g73 |
| r48 | batches#r73 |
| g49 | batches#g74 |
| r49 | batches#r74 |
