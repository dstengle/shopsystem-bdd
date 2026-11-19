# batch-1: the batch brief

You run batch-1, from `work batch resume` until its pull request is `awaiting-merge`, as the one fresh agent of this batch: you dispatch its task, fix and review subagents yourself.

- Batch: batch-1 (`.shop/batches/1/plan.md`)
- Base checkout: /tmp/claude-1000/-home-vscode-shopsystem-bdd/0871dbcd-a17a-4bbe-aee5-3445375f749d/scratchpad/ux-checklists, on main: run every `work batch` command there, never in a task's worktree
- Batch branch: batch-1, its worktree /tmp/claude-1000/-home-vscode-shopsystem-bdd/0871dbcd-a17a-4bbe-aee5-3445375f749d/scratchpad/ux-checklists/.shop/worktrees/batch-1
- Scripts: /home/vscode/shopsystem-bdd/scripts

## The skill

Follow the skill `shopsystem-bdd:building-a-batch` from step 3 (Resume) to step 7's `-> awaiting-merge`: `work batch resume batch-1`, one subagent for each running task, all at once, `work batch done` or `park` as each returns, `work batch review`, then `work batch brief`, a fresh `shopsystem-bdd:pr-reviewer` and `work batch reviewed`, and the fix loop until the review is clean.

## Tasks

### t1 b1 "Create checklists, add items, check items off and list them"

- Worktree: /tmp/claude-1000/-home-vscode-shopsystem-bdd/0871dbcd-a17a-4bbe-aee5-3445375f749d/scratchpad/ux-checklists/.shop/worktrees/batch-1-t1 (made by `work batch resume`)
- Branch: batch-1-b1
- Item file: /tmp/claude-1000/-home-vscode-shopsystem-bdd/0871dbcd-a17a-4bbe-aee5-3445375f749d/scratchpad/ux-checklists/.shop/backlog/b1.md
- Requirement ids: checklists#r1, checklists#r2, checklists#r3, checklists#r4, checklists#r5, checklists#r6
- Acceptance tests (in the worktree): `python3 -m pytest -q tests/scenarios/test_checklists.py -m "r1 or r2 or r3 or r4 or r5 or r6"`
- Subagent description: `batch-1 t1 b1`

## The lay's bookkeeping

The lay's commit wrote each laid line's corpus block, took out each retired id's and wrote the catalogues again (b333): a block's form is the parser's, so the task whose item changes the grammar reads it against the line and corrects it.

## Push

`.shop/delivery.toml` gives no `[batch] push`: git push and gh run as they are; `work` pushes its own commits.

## The rules every subagent is given

- Read the repository's CLAUDE.md in its worktree and follow it; the `tier: judgement` design-decisions (`grep -l '^tier: judgement' spec/decisions/*.md`) are followed in the code it writes.
- One scenario at a time, red first: see it fail on its Then line before writing its handler or code.
- Never edit a `.feature` file; an existing test is changed only in its setup.
- Take each id out of its capability's `unbuilt:` in the same commit that makes its scenario pass.
- End every commit message with the line `Item: b<j>` (`git commit -m "<subject>" --trailer "Item: b<j>"`); a fix also `--trailer "Finding: f<m>"`, both in the message's last paragraph.
- Change nothing under `.shop/` (`.shop/backlog/`, `.shop/batches/` are the base checkout's batch commands' only).
- Worktrees of older work (`.shop/worktrees/*` of other or earlier batches, `.claude/worktrees/`) are never reference material: the reference is the base branch and its own worktree.
- Don't chain `cp` and `rm` in one shell command; keep shell variables few.
- Never use `git stash`: every worktree shares one stash list, so two tasks' stashes swap; to see a test red, put files back with `git checkout <commit> -- <path>` or a scratch copy.
- Don't push and don't run `work` commands that commit.
- A scenario that passes before it is built (an XPASS) means a test step is too loose: say so in the reply.
- There is no brief or result file: reply with what was built and its commits, or with one question, never a guess. `work batch done` runs the whole suite in the worktree and refuses with its last lines.

## Where you stop

At `-> awaiting-merge`, once the pull request is clean and marked ready. You never merge the pull request, and never run `work batch merged` nor `measure batch`: the session that started you does, after the person merges it. A question you cannot settle goes onto its item with `work batch park`, never to the person.

## What you reply

The pull request's URL, each item delivered in it and each item parked with its question, in a few lines; or, if the batch was abandoned, that and why.
