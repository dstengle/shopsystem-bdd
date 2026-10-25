---
name: delivering-an-initiative
description: Use when the person asks to deliver, build or implement an initiative, in a repository with .shop/work/. Starts `work run` on the initiative, which does the drafting and the delivery, and shows the person what it printed. Not for writing spec or feature files, and not for implementing a work-item yourself.
---

# Delivering an Initiative

## Overview

You have `work run` deliver an initiative. `work run` is a script: it takes every transition of the initiative's nodes, drafting work-items included, starts a fresh worker for each stage (research, plan, implementation, review), reads only their result files, writes every transition itself and ends printing where each node stands. Your part is to start it and show the person what it printed.

You start no `claude -p` session yourself and merge no branch yourself, even when `work run` fails. You never read what the workers write.

The plugin's scripts are in `scripts/`, two levels above this skill's base directory: `work` is `python3 <that directory>/work`.

## Before anything

Stop, saying why, and change nothing, when any of these holds:

- `git status --porcelain` shows anything: the checkout has uncommitted changes, which `work run`'s commits and worktrees would not carry;
- `.shop/work/<initiative>/initiative.md` is not there: no such initiative;
- the plugin's `work` is not there, or `python3 <scripts>/work --help` lists no `run`.

## What you read

`.shop/work/` alone, and only the initiative's `initiative.md`, its capability-proposals and its work-item files, never anything under a `runs/` directory. No source file, no test, no script's code: you run the plugin's scripts, you do not read them.

## Run `work run`

When asked to deliver an initiative, start `python3 <scripts>/work run <initiative>` as a **background** command, exactly as written: nothing before it (no `cd`) and nothing after it (no `; echo`), since its exit code comes with the background command's end. Wait to be woken when it exits.

While it runs, read nothing its workers write: no file under `.shop/work/<initiative>/runs/`, no `log.jsonl`, nothing under `.shop/worktrees/`, no work-item file, and not the background command's output until it has exited. Do not poll it. If the person asks how it is going, say it is running and that you will show what it prints when it ends.

## When it exits

Show the person what `work run` printed, as it printed it, in one code block: each work-item with its status, and under a work-item that is `awaiting-answer`, its open questions, indented. Then say in one line what its exit code means: 0, every work-item `green`; 3, a question awaits the person; anything else, it stopped (its `work: <why>` line, shown as it is).

Do not explain, summarise or answer the questions yourself, and do not read the work-items or the stage directories to say more. What happens next is the person's.

## Questions to the person

- When `work run`'s printout says a worker needed a tool `work run` does not allow, put the tool to the person as a question, naming the stage as printed.
- For each `failed` work-item, and for a `work: <why>` stop of `work run`, put the change to the person as a question, naming the work-item or the change and its fault as printed. Retry nothing, run `work run` again for nothing, edit no file and dispatch nobody to deliver it.

## Fixes, rulings and the ledger

- A fix to code that a trial finds is drafted as a work-item for `work run` to deliver: `python3 <scripts>/work add <initiative> <title> --part-of capability-proposal/<the proposal's file name without .md> --under <capability> --accepts <id>`, one `--accepts` for each requirement id; `work add` prints the work-item's id and commits it. You change no code yourself.
- A fix that needs a new scenario, or a new row of a scenario's examples, goes to the `feature-formulator` through a `formulate` round of `initiative-round`, never to the implementer.
- Ask each dispatch to reply in a few lines and leave the rest in files. Read a file a dispatch wrote only to decide what to do next.
- Each ruling the person gives is one line appended to the initiative's ledger, `.shop/scratch/run/ledger-<initiative>.md`.
- When `work run` exits with every work-item of the initiative `green` or `withdrawn`, move the ledger to `.shop/records/archive/`.

## Red Flags

- Opening a source file, a test or a script's code "to see what the work-item needs"
- Reading a stage directory, `log.jsonl` or a worktree while `work run` is running, or after it, to explain what it printed
- Drafting work-items from a capability-proposal yourself, or committing anything but a trial's fix
- Starting a `claude -p` session, or merging a branch, because `work run` failed
- Starting `work run` with uncommitted changes in the checkout
- Rewording `work run`'s printout instead of showing it
