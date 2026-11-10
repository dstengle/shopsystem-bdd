---
name: building-a-batch
description: Use when the person asks to build, run or carry on a batch, or to build what is ready in the backlog, in a repository with .shop/backlog/; also when a session starts with a batch building.
---

# Building a Batch

## Overview

A batch builds several ready items together, like a sprint: one branch `batch-<n>`, one task for each item, one pull request at the end. `work batch` keeps the state on disk (the batch file `.shop/batches/<n>/plan.md`, the items, the branches and worktrees) and runs the checks; one fresh agent, the batch's driver, orchestrates it from the batch brief `work batch start` writes, never the long main session. It dispatches one subagent for each running task, all in parallel, the way superpowers' subagent-driven development does, and nothing waits on the person until the pull request is published. Any later session carries the batch on from where the last one stopped.

Scripts: `<this skill's base directory>/../../scripts/`. Every `work batch` command runs from the base checkout (the branch the batch was started on), never from a task's worktree.

## Process

1. **Take in the requests first.** `python3 <scripts>/work sync` records what was posted on each request's issue; for each request waiting on this context as its upstream, follow `taking-in-a-request`, so that what is ready can join the batch. While a request waits on the other side, start `python3 <scripts>/work watch --forward` with the Monitor tool too (its timeout at the maximum, in place of Bash `run_in_background`); when it ends, run `work sync` and that skill, and start it again, as again when it times out and after each `work sync`.
2. **Start, or find the open batch, and hand it to one fresh agent.** `python3 <scripts>/work batch start` picks the ready, unblocked, passing items in rank order and lays their lines on `batch-<n>`; it prints the batch and its tasks, each item it returned to `shaped` or left out, with the reason, and the path of the batch brief it wrote (`batch brief: <path>`, under `.shop/worktrees/batch-<n>-driver/`, never committed). With a batch already open, `python3 <scripts>/work batch status` names it. With nothing picked, the session ends there and says so.
   The session that starts the batch does not run it: it dispatches one fresh `general-purpose` agent, the batch's driver, with the description `batch-<n> driver` and the brief's path as its whole prompt, and no other context. The driver follows steps 3 to 7 below, dispatching the task, fix and review subagents itself, and stops at `-> awaiting-merge` with the pull request's link. The starting session relays that link to the person and, after the merge, runs `work batch merged` and `measure batch` (step 7). If the driver cannot dispatch subagents, a fresh session per batch runs steps 3 to 7 instead, given the same brief.
3. **Resume.** `python3 <scripts>/work batch resume <batch>` gives each pending task its worktree and prints, for each running task, its worktree, its branch and the requirement ids it builds.
4. **Dispatch the running tasks, all at once:** one subagent for each running task, in parallel, each in its own task's worktree, with the description `batch-<n> t<k> b<j>` (its batch, task and item: `measure batch` reads a subagent's role from it). Give each this brief:
   - its worktree and branch, and the item's file `.shop/backlog/b<j>.md`;
   - its requirement ids: the scenarios tagged `@r<n>` in `features/<cap>.feature` are its acceptance tests, run in its worktree with `python3 -m pytest -q tests/scenarios/test_<cap>.py -m r<n>`;
   - what each line means, read before building it: `python3 <scripts>/model explain <cap>#r<n>` (the line, what it also means through a pack's definition or a universal condition, and the If lines that take precedence over it) and `python3 <scripts>/model parse --form "<line>"` (its logical form; it marks every code `(parameter)`, a command's too: the values the group's `given` block binds are what `model check`'s `w_example` names, paths, message texts and sample values, never constants to hard-code, while a command or an option is a constant). A `# entailed: <U or definition>` comment in a scenario is a Then no step builds: the check after every scenario holds it;
   - an item that rewords lines (its `## Requirements` has `retired:` ids): each retired id's scenario is gone from the feature, so its step handlers that no scenario reaches any more go too; a new id whose scenario passes before any code changes (an XPASS) is a reworded line whose behaviour exists: confirm its steps check the line as now worded, take its id out of `unbuilt:` and say so in the reply (an XPASS of a line that is no reword is a step too loose);
   - the `tier: judgement` design-decisions (`grep -l '^tier: judgement' spec/decisions/*.md`), to follow in the code it writes;
   - the repository's `CLAUDE.md`, and these rules: one scenario at a time, red first (see it fail on its Then line before writing its handler or code), never edit a `.feature` file, and an existing test changed only in its setup;
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
   - Dispatch one fresh `pr-reviewer` agent (`subagent_type` `shopsystem-bdd:pr-reviewer`, description `batch-<n> review <k>` for the k-th review) with the brief's path as its whole prompt, and no other context: not this session's notes, not the subagents' replies. It has no Write (the harness refuses a subagent's findings file): its reply is the findings file's content.
   - Save the reviewer's reply byte for byte at the brief's `Findings file:` path (Write), then run `work batch reviewed`. Saving is not editing: never change a byte of it, not even to fence a line it asks you to.
   - `python3 <scripts>/work batch reviewed <batch>` records the review under `.shop/batches/<n>/`, posts it on the pull request, and prints `-> awaiting-merge` or `-> building` with each open finding.
   - A refused `reviewed` names the line of the findings file it could not read: run `work batch brief` again (it removes the old file) and dispatch a fresh `pr-reviewer` with the brief's path and the refusal's text, and save its reply as before; never edit the findings file.
   - On `-> awaiting-merge`, give the person the pull request's link; it is marked ready. The person merges it, and `python3 <scripts>/work batch merged <batch>` then delivers the items. Then this session runs `python3 <scripts>/measure batch <batch>` and commits its record (analyzing-a-batch reads it, and measures only a batch that has none). Then, when `python3 <scripts>/work backlog` shows an item `ready`, start the next batch at step 1 without asking the person.
   - On `-> building`, run `python3 <scripts>/work batch resume <batch>`: it prints each open finding with its task's worktree and branch. Dispatch one subagent for each item an open finding names, all at once, each in that task's worktree with the description `batch-<n> fix f<m>`, with the finding's text (the record `.shop/batches/<n>/review-<k>.md` of the review that raised it) and this rule: fix only what the finding says, red first where a test can show it, and end each commit with the two lines `Item: b<j>` and `Finding: f<m>` together, as the message's last paragraph: `git commit -m "<subject>" --trailer "Item: b<j>" --trailer "Finding: f<m>"`. Git reads trailers from the last paragraph only, so two `-m` lines leave `Item:` unread and `review` refuses the commit.
   - Then run `python3 <scripts>/work batch review <batch>` again, which checks that each fix commit cites an open finding and each open finding has one, and pushes only; then `work batch brief` again, which is a re-review of what the fixes changed, and so on. Two fixes that conflict: the later item's subagent merges the earlier item's branch into its own and resolves it there, in a commit citing its own item and finding; the merged-in commits cite another item's open finding, which `review` accepts.
   - A commit after a review must cite a `fix now` finding, so an `observation` is not fixed in the loop: one worth doing becomes an item of the backlog (`work idea`).
   - After the third review that leaves a finding open, park each item an open finding names (`work batch park <batch> <item> --question "<the finding's title>"`), and review again: its findings close with it. When no item is left in-batch, `review` refuses: `work batch abandon <batch>`, then `python3 <scripts>/measure batch <batch>` and commit its record, as after a merge.
8. **A later session** starts again at step 2: `work batch status` finds the batch, and `work batch resume` gives back any worktree that was lost, with its commits.

The rule: nothing waits on the person between steps 1 and 7, until the pull request is clean. A question goes onto its item with `work batch park`, never to the person.

Every commit `work`, `measure` and `migrate` make is pushed to the branch's upstream remote, else `origin`. A push git refuses keeps the commit and prints `not pushed: <remote>: <git's reason>`: fix the cause (the remote, the login), then push the branch with `git push`.

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
| `not pushed: <remote>: …` after a command | The commit is kept; fix the remote, then `git push` |
| The main session running the batch's tasks itself | Dispatch one fresh driver with the batch brief's path (step 2) |
| Asking the person whether to start the next batch | An item is `ready`: start it (step 1) |
| A fix commit with no `Finding: f<m>` line | `review` refuses it; amend the message on the item's branch |
| A finding argued with instead of fixed or parked | Fix it on its item's branch, or park the item with the finding as its question |
