---
name: delivering-an-initiative
description: Use when the person asks to deliver, build or implement an initiative whose capability-proposals are formulated (their feature files written), in a repository with .shop/work/. Drafts the initiative's work-items from the spec alone with `work add`, commits them, runs `work run` and shows the person what it printed. Not for writing spec or feature files, and not for implementing a work-item yourself.
---

# Delivering an Initiative

## Overview

You turn an initiative's formulated capability-proposals into drafted work-items and have `work run` deliver them. `work run` is a script: it starts a fresh worker for each stage of each work-item (research, plan, implementation, review), reads only their result files, writes every transition itself and ends printing where each work-item stands. Your part is before and after it: draft, commit, start it, and show the person what it printed.

You draft from the spec and the feature files, never the code, and you never read what the workers write.

The plugin's scripts are in `scripts/`, two levels above this skill's base directory: `work` is `python3 <that directory>/work`.

## Before anything

Stop, saying why, and change nothing, when any of these holds:

- `git status --porcelain` shows anything: the checkout has uncommitted changes, which `work run`'s commits and worktrees would not carry;
- `.shop/work/<initiative>/initiative.md` is not there: no such initiative;
- no capability-proposal in `.shop/work/<initiative>/` (a file with `kind: capability-proposal`) has `status: formulated`;
- the plugin's `work` is not there, or `python3 <scripts>/work --help` lists no `run`.

## What you read

`spec/`, `features/` and `.shop/work/` alone. No source file, no test, no script's code, nothing else in the repository: you run the plugin's scripts, you do not read them. Within `.shop/work/` you read the initiative's `initiative.md`, its capability-proposals and its work-item files, and nothing under a `runs/` directory.

## Drafting

1. **The requirements.** For each `formulated` capability-proposal of the initiative: the requirement ids in its `adds:` and its `changes:` (`<capability>#r<n>`, or a range such as `delivery#r1-r7`). Leave out those a work-item of the initiative already accepts (its `accepts:`) unless that work-item is `withdrawn`. When none is left, every requirement is accepted already: draft nothing, commit nothing, and go straight to "Run `work run`".
2. **The work-items.** One for each proposal and capability: it accepts every requirement of that proposal on that capability. Its title says what it delivers; `work add` numbers it and prints its id `w<n>`: take that id as its name, never one you choose.
3. **Check before the first `work add`.** Read `features/` for each scenario tagged `@r<n>` with `<n>` among the requirements of the `formulated` proposals' `adds:` and `changes:` (those the formulation added or reworded). When one names a requirement that no planned work-item accepts, stop, naming each such scenario (feature file and title), and run no `work add`: `work add` commits as it goes, so no work-item may be drafted.
4. **Draft each** with `python3 <scripts>/work add <initiative> <title> --part-of capability-proposal/<the proposal's file name without .md> --under <capability> --accepts <id>`, one `--accepts` for each requirement id. It prints the work-item's id: keep it.
5. **List its Retires.** In `features/`, find each scenario tagged `@deprecated` whose own `@r<n>` tags name a requirement the work-item accepts. When there is one, append to the work-item's file a `## Retires` section: one line for each, the scenario's exact title as it stands in the file, with its ` (deprecated)` suffix, in quotes, followed by its feature file. When there is none, add no section.

If a `work add` refuses, delete the work-item files this session drafted, so nothing is changed, and stop, giving the person its message.

Show the person the drafted work-items as one table: name, accepts, risk (`work add` sets none: write `not set`).

## Commit them, alone

Only when this session drafted work-items, and `work add` has committed each one already. `git add` the drafted work-item files and commit them with a pathspec that names only them, so nothing else goes into the commit: `git commit -m "work: draft <initiative>: <names>" -- <the files>`; that commit holds the Retires sections written after `work add`, and is made only when `git status --porcelain` shows a change in those files.

## Run `work run`

Start `python3 <scripts>/work run <initiative>` as a **background** command, exactly as written: nothing before it (no `cd`) and nothing after it (no `; echo`), since its exit code comes with the background command's end. Wait to be woken when it exits.

While it runs, read nothing its workers write: no file under `.shop/work/<initiative>/runs/`, no `log.jsonl`, nothing under `.shop/worktrees/`, no work-item file, and not the background command's output until it has exited. Do not poll it. If the person asks how it is going, say it is running and that you will show what it prints when it ends.

## When it exits

Show the person what `work run` printed, as it printed it, in one code block: each work-item with its status, and under a work-item that is `awaiting-ruling`, its open questions, indented. Then say in one line what its exit code means: 0, every work-item `green`; 3, a question awaits the person; anything else, it stopped (its `work: <why>` line, shown as it is).

Do not explain, summarise or answer the questions yourself, and do not read the work-items or the stage directories to say more. What happens next is the person's.

## Fixes, rulings and the ledger

- A fix to code that a review or a trial finds is drafted as a work-item for `work run` to deliver. You change no code yourself.
- A fix that needs a new scenario, or a new row of a scenario's examples, goes to the `feature-formulator` through a `formulate` round of `initiative-round`, never to the implementer.
- Ask each dispatch to reply in a few lines and leave the rest in files. Read a file a dispatch wrote only to decide what to do next.
- Each ruling the person gives is one line appended to the initiative's ledger, `.shop/scratch/run/ledger-<initiative>.md`.
- When `work run` exits with every work-item of the initiative `green` or `withdrawn`, move the ledger to `.shop/records/archive/`.

## Red Flags

- Opening a source file, a test or a script's code "to see what the work-item needs"
- Reading a stage directory, `log.jsonl` or a worktree while `work run` is running, or after it, to explain what it printed
- A commit that holds anything but the drafted work-items
- An empty commit, or a work-item drafted again, when every requirement is accepted already
- Starting `work run` with uncommitted changes in the checkout
- Rewording `work run`'s printout instead of showing it
