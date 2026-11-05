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
6. **Publish.** When every task of an in-batch item is done, `python3 <scripts>/work batch review <batch>` takes the parked items' lines out of `batch-<n>`, merges the in-batch items' branches into it, runs the tests, pushes it and opens the draft pull request, then prints the next step: its review (step 7). A refused review changes nothing and is safe to run again once its cause is fixed:
   - a conflict between two items' branches: have the later item's subagent merge the earlier item's branch into its own and resolve it there, in a commit citing its own item (a branch may carry an earlier in-batch item's commits), then `done` it again; or park one of the two;
   - the tests fail on the merged branch: send the failure to the subagent of the item that broke them, fix it on that item's branch, `done` it again;
   - a push or gh failure: fix the cause (the remote, gh's login), then run the review again.
7. **Review and fix.** The published pull request gets one review, and no review is written when a task becomes `done`: the reviewer is dispatched only after `work batch review`, each time by a fresh agent. Nothing in this step goes to the person until the pull request is clean.
   - After `work batch review`, run `python3 <scripts>/work batch brief <batch>`; it prints the brief's path.
   - Dispatch one fresh `pr-reviewer` agent (`subagent_type` `shopsystem-bdd:pr-reviewer`) with the brief's path as its whole prompt, and no other context: not this session's notes, not the subagents' replies. It writes the findings file the brief names.
   - Run `python3 <scripts>/work batch reviewed <batch>`. It records the review under `.shop/batches/<n>/`, posts it on the pull request, and prints `-> awaiting-merge` or `-> building` with each open finding.
   - On `-> awaiting-merge`, give the person the pull request's link; it is marked ready. The person merges it, and `python3 <scripts>/work batch merged <batch>` then delivers the items.
   - On `-> building`, run `python3 <scripts>/work batch resume <batch>`: it prints each open finding with its task's worktree and branch. Dispatch one subagent for each item an open finding names, all at once, each in that task's worktree, with the finding's text and this rule: fix only what the finding says, red first where a test can show it, and end each commit with the two lines `Item: b<j>` and `Finding: f<m>` together, as the message's last paragraph (`git commit -m "<subject>" -m "Item: b<j>`, a newline, `Finding: f<m>"`): git reads trailers from the last paragraph only, so two `-m` lines leave `Item:` unread and `review` refuses the commit.
   - Then run `python3 <scripts>/work batch review <batch>` again, which checks that each fix commit cites an open finding and each open finding has one, and pushes only; then `work batch brief` again, which is a re-review of what the fixes changed, and so on.
   - After the third review that leaves a finding open, park each item an open finding names (`work batch park <batch> <item> --question "<the finding's title>"`), and review again: its findings close with it.
8. **A later session** starts again at step 2: `work batch status` finds the batch, and `work batch resume` gives back any worktree that was lost, with its commits.

The rule: nothing waits on the person between steps 1 and 7, until the pull request is clean. A question goes onto its item with `work batch park`, never to the person.

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
| A `pr-reviewer` dispatched after a task's `done` | The one review is of the published pull request: `work batch review`, then `work batch brief` |
| A reviewer given the session's context | Give it the brief's path and nothing else; a fresh agent each review |
| A fix commit with no `Finding: f<m>` line | `review` refuses it; amend the message on the item's branch |
| A finding argued with instead of fixed or parked | Fix it on its item's branch, or park the item with the finding as its question |
