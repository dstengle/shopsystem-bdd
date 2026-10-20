---
id: decision-argument/missingmass.io/shopsystem/shopsystem-bdd/2026-10-11-research-probes-design
kind: decision-argument
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-11
---

# Research Probes Design

Date: 2026-10-11
Status: The short design was approved in conversation ("Build 0.16.0 and we'll have kb test it"). Unreleased, on
branch `0.16.0-research-probes`, stacked on 0.15.0.
Release: 0.16.0
Request: `docs/superpowers/requests/2026-10-11-research-probes-current-behaviour.md`

## Purpose

A plan is written from what the system does today, and that is found by running it. The scout probes current
behaviour and marks what it ran apart from what it read; the plan decides what a new path loses when it skips a
stage; a dry run and its real run are held to agree by a test that stays; and a batch stops fixing when what is
left is not severe.

## Evidence

From the request, and from kb's batches 38 and 39 measured with `measure` (both ran on 0.11.0):

| | batch 38 | batch 39 |
|---|---|---|
| research | one Haiku scout, read and red markers only, 4.3 min, peak context 171k | one Opus scout, with probes, 13.2 min, peak context 276k |
| slices, dispatches | 6, 15 | 12, 25 |
| fix dispatches, re-reviews | 4, 3 | 6, 3 |
| share of agent time closing | 0.14 | 0.64 |

- Batch 38's misses were each a question of the form "what does the system answer today when…": a refusal made
  only at landing, which a new path that never lands did not meet; a read with a place that returns the whole
  artifact; a crash on the scenario's own data.
- Batch 39's probing research found two live defects before planning and corrected two slice sizes, one from
  "0 production" to 6. The request says so; this was not checked against the scout's notes.
- The two batches differ in the scout's model as well as in probing. Verification here holds the model the same.
- Each batch used one scout for all its slices, against 0.11.0's one a task.
- Batch 39's three re-reviews ran 30, 26 and 14 minutes. Its reviewers probed "what the check reports is what the
  import does" over tens of thousands of random pairs each round, and that found every important defect.

## Changes

### 1. The scout probes what the system answers today

`agents/code-scout.md`.

- A new section, Probes: the system driven through its real entry point, every probe working under
  `.superpowers/scratch/<run>/` and never on the checkout's data; each recorded with its command, what came back,
  and `run`; a conclusion from the code alone recorded the same way and marked `read`. A defect a probe finds is
  reported, not fixed and not judged.
- Task research gains a fifth part, **What the system answers today**: the Givens and Whens of the slice's
  scenarios against today's code, and the nearest cases they do not state (the store already holding something;
  the thing asked for missing; the scenario's data at its edges).
- **A path that leaves a stage out:** every refusal and effect that stage alone produces, each shown by a probe of
  the existing way.
- **Sizes:** the line count and room of every module the change's path passes through.
- A `steps only` line rests on a probe that was run.

### 2. The hand-off plans from runs

`skills/slicing-into-increments`.

- One scout a task, said again with the number: a scout for a whole batch reached 276k of context.
- "Why it is red" comes from the scout's run and probes; a line marked `read` is carried into the task as
  unverified.
- `Lands: 0 production` stands only on a probe that was run and logged.
- A defect a probe found is triaged as a review's finding is. A module with no room is split first.
- **A stage left out:** the task's decisions name each refusal and effect the skipped stage alone produces, and say
  what the new path does about each.

### 3. A dry run agrees with the real run

The hand-off; `agents/bdd-branch-reviewer.md`.

Where a system has a dry run and a real run of one operation, the plan's Review Focus carries the property, and
the first task that touches either writes or extends one randomized test of it that stays in the suite. It is an
invariant in 0.15.0's sense. The branch reviewer runs that test and says how many cases it tried, or writes the
probe and hands it on as a test to keep.

### 4. Fix rounds end

The execution rules, slicing's Review Findings, `agents/bdd-task-reviewer.md`.

After the fix wave's re-review, another round is run only for a finding that leaves data invalid, is the system's
own fault on input, or lands a write where a refusal belongs; as many rounds as that takes. Every other finding of
a re-review is a backlog line. The re-review is dispatched with that triage and keeps to it.

## Not yet

- **The scout's model.** It stays Haiku by default; a dispatch may name another. Promoted to a rule if kb's probing
  research on Haiku misses what Opus found.
- **A script that makes the scratch store.** How a project points its system at scratch is the project's, said in
  its `CLAUDE.md`.

## What should move

On a batch of kb run on this version: fix dispatches and re-reviews a batch (4 and 3, 6 and 3); the share closing
(0.64 in batch 39); minutes in re-review once the agreement test is in the suite; one scout dispatch a task, each
with a peak context well under 171k; no finding of the kind "what the system already did" in
`analyzing-a-batch`'s findings table.

## Verification

Headless on a fixture (`/home/vscode/scratch/shopsystem-bdd/probe/`), the scout on Haiku before and after: a
library where `read` takes a part in its own code but a wrapper applied at import drops it, and where a duplicate
is refused, and an add counted, only at landing. Two slices: a read naming a part; a check of an add that does not
land. Scored from the notes and from git: whether a read with a part is said to give the whole item today; whether
the refusal and the count are named as landing's alone; whether probes are recorded with commands and marked
`run`; module sizes; and the checkout clean afterwards.
