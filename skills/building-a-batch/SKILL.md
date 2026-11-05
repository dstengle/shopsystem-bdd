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
4. **Dispatch the running tasks, all at once:** one subagent for each running task, in parallel, each in its own task's worktree. Give each this brief, and nothing of `work run`'s:
   - its worktree and branch, and the item's file `.shop/backlog/b<j>.md`;
   - its requirement ids: the scenarios tagged `@r<n>` in `features/<cap>.feature` are its acceptance tests, run in its worktree with `python3 -m pytest -q tests/scenarios/test_<cap>.py -m r<n>`;
   - the repository's `CLAUDE.md`, and these rules of `bdd-red-green`: one scenario at a time, red first (see it fail on its Then line before writing its handler or code), never edit a `.feature` file, and an existing test changed only in its setup;
   - "There is no brief or result file: reply with what you built, or with your one question. `work batch done` runs the whole suite in your worktree and refuses with its last lines, so a test you broke anywhere comes back to you."
   - for an item that returns to a batch after a park, the old branch its notes name (`## Notes`: `its work is on branch batch-<n>-b<j>`): cherry-pick from it what still applies, keeping each commit's `Item: b<j>` line.

   Each builds its scenarios one at a time, takes each id out of its capability's `unbuilt:` in the same commit that makes the scenario pass, and ends every commit message with the line `Item: b<j>`. It changes nothing under `.shop/backlog/` or `.shop/batches/`. A subagent that cannot go on without an answer returns its question instead of guessing.
5. **Close each task as its subagent returns**, from the base checkout: `python3 <scripts>/work batch done <batch> <task>`, which checks the worktree, the commits and the ids and runs the tests there. A refused `done` goes back to the same subagent with the refusal. A subagent that returned a question: `python3 <scripts>/work batch park <batch> <item> --question "<its question>"`; the item leaves the batch as `needs-input`, its branch kept, and the rest carries on.
6. **Publish.** When every task of an in-batch item is done, `python3 <scripts>/work batch review <batch>` takes the parked items' lines out of `batch-<n>`, merges the in-batch items' branches into it, runs the tests, pushes it and opens the draft pull request; give the person its link. The person merges it, and `python3 <scripts>/work batch merged <batch>` then delivers the items. A refused review changes nothing and is safe to run again once its cause is fixed:
   - a conflict between two items' branches: have the later item's subagent merge the earlier item's branch into its own and resolve it there, in a commit citing its own item (a branch may carry an earlier in-batch item's commits), then `done` it again; or park one of the two;
   - the tests fail on the merged branch: send the failure to the subagent of the item that broke them, fix it on that item's branch, `done` it again;
   - a push or gh failure: fix the cause (the remote, gh's login), then run the review again.
7. **A later session** starts again at step 2: `work batch status` finds the batch, and `work batch resume` gives back any worktree that was lost, with its commits.

The rule: nothing waits on the person between steps 1 and 6. A question goes onto its item with `work batch park`, never to the person.

## Red Flags

| Seen | Fix |
|---|---|
| A `work batch` command run inside a task's worktree | Run it from the base checkout; it refuses another branch |
| Tasks dispatched one after another | Dispatch every running task at once, one subagent each |
| A commit without `Item: b<j>` | `done` and `review` refuse it; amend the message on the task's branch |
| `park` or `abandon` refused for uncommitted changes | Commit them on the task's branch with its `Item:` line, or pass `--discard` to drop them |
| A task's commit that edits `.shop/backlog/` or `.shop/batches/` | Only the base branch's batch commands write those |
| A question put to the person mid-batch | `work batch park` the item with the question; the batch carries on |
| An id left in `unbuilt:` after its scenario passes | The strict xfail fails the suite; take it out in the same commit |
