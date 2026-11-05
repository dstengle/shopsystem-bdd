---
name: building-a-batch
description: Use when the person asks to build, run or carry on a batch, or to build what is ready in the backlog, in a repository with .shop/backlog/; also when a session starts with a batch building.
---

# Building a Batch

## Overview

A batch builds several ready items together, like a sprint: one branch `batch-<n>`, one task for each item, one pull request at the end. `work batch` keeps the state on disk (the batch file `.shop/batches/<n>/plan.md`, the items, the branches and worktrees) and runs the checks; this session orchestrates. It dispatches one subagent for each running task, all in parallel, the way superpowers' subagent-driven development does, and nothing waits on the person until the pull request is published. Any later session carries the batch on from where the last one stopped.

Scripts: `<this skill's base directory>/../../scripts/`. Every `work batch` command runs from the base checkout (the branch the batch was started on), never from a task's worktree.

## Process

1. **Take in the requests first.** For each request of a peer or the product in this context's turn (`python3 <scripts>/work list`), follow `taking-in-a-request`, so that what is ready can join the batch.
2. **Start, or find the open batch.** `python3 <scripts>/work batch start` picks the ready, unblocked, passing items in rank order and lays their lines on `batch-<n>`; it prints the batch and its tasks, and each item it returned to `shaped` or left out, with the reason. With a batch already open, `python3 <scripts>/work batch status` names it. With nothing picked, the session ends there and says so.
3. **Resume.** `python3 <scripts>/work batch resume <batch>` gives each pending task its worktree and prints, for each running task, its worktree, its branch and the requirement ids it builds.
4. **Dispatch the running tasks, all at once:** one subagent for each running task, in parallel, each in its own task's worktree. Give each:
   - its worktree and branch, and the item's file `.shop/backlog/b<j>.md`;
   - its requirement ids, whose generated scenarios in `features/` are its acceptance tests;
   - the skill `bdd-red-green` and the repository's `CLAUDE.md`.

   Each builds its scenarios one at a time, takes each id out of its capability's `unbuilt:` in the same commit that makes the scenario pass, and ends every commit message with the line `Item: b<j>`. It changes nothing under `.shop/backlog/` or `.shop/batches/`. A subagent that cannot go on without an answer returns its question instead of guessing.
5. **Close each task as its subagent returns**, from the base checkout: `python3 <scripts>/work batch done <batch> <task>`, which checks the worktree, the commits and the ids and runs the tests there. A refused `done` goes back to the same subagent with the refusal. A subagent that returned a question: `python3 <scripts>/work batch park <batch> <item> --question "<its question>"`; the item leaves the batch as `needs-input`, its branch kept, and the rest carries on.
6. **Publish.** When every task of an in-batch item is done, `python3 <scripts>/work batch review <batch>` merges the in-batch items' branches into `batch-<n>`, runs the tests, pushes it and opens the draft pull request; give the person its link. The person merges it, and `python3 <scripts>/work batch merged <batch>` then delivers the items.
7. **A later session** starts again at step 2: `work batch status` finds the batch, and `work batch resume` gives back any worktree that was lost, with its commits.

The rule: nothing waits on the person between steps 1 and 6. A question goes onto its item with `work batch park`, never to the person.

## Red Flags

| Seen | Fix |
|---|---|
| A `work batch` command run inside a task's worktree | Run it from the base checkout; it refuses another branch |
| Tasks dispatched one after another | Dispatch every running task at once, one subagent each |
| A commit without `Item: b<j>` | `done` and `review` refuse it; amend the message on the task's branch |
| A task's commit that edits `.shop/backlog/` or `.shop/batches/` | Only the base branch's batch commands write those |
| A question put to the person mid-batch | `work batch park` the item with the question; the batch carries on |
| An id left in `unbuilt:` after its scenario passes | The strict xfail fails the suite; take it out in the same commit |
