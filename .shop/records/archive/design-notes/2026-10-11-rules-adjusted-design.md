---
id: decision-argument/missingmass.io/shopsystem/shopsystem-bdd/2026-10-11-rules-adjusted-design
kind: decision-argument
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-11
---

# Rules Adjusted Design

Date: 2026-10-11
Status: Written while the person was away, at their instruction; not read by them. Unreleased, on branch
`0.13.0-rules-adjusted`, stacked on 0.12.0.
Release: 0.13.0
Request: `docs/superpowers/requests/2026-10-11-predictable-batches-and-analysis-tools.md`, section E
Baseline: `docs/superpowers/testing/2026-10-11-kb-baseline/`

## Purpose

0.11.0's rules did what they were written for. This release adjusts the ones the request and the baseline show
costing more than they return, and leaves alone the ones where the person said they could not judge. Each change
names the number in a batch's facts (`measure`, 0.12.0) that should move, so one batch of kb on this version says
whether to keep it.

The request's section E has ten items. Six are taken, one is replaced by what the baseline measured, and three and
a half are held as open choices.

## What the baseline says about section E

- **Hand-backs.** Four in batches 33 to 35, all for an existing test the task did not list. One was a test the
  same batch had written a slice earlier. One was three tests of which two needed only their setup changed. Two
  needed assertions rewritten.
- **Steps.** Batch 33 ran 16 implement dispatches for 11 slices; slice 161 took four.
- **The floor is not the brief.** An implementer's first request holds 29k tokens and a reviewer's or a scout's
  15k, before any file is read. About 6k of the implementer's is the listing of every installed skill, which it is
  sent because it has the Skill tool. The repository's `CLAUDE.md` is already in every agent's first request. No
  implementer opened `CLAUDE.md`; before its first edit it read its brief (about 900 tokens), sometimes the report,
  and source.
- **The controller is the largest reader.** 26M to 31M cache-read tokens a batch, about 100 requests, in one
  session whose context went from 412k to 585k across four batches.
- **Reviews.** 7 of 17 task reviews had no Critical or Important finding.
- **Scouts.** 20% of output and new input.

## Changes

### 1. Two allowances under "Tests the decisions break" (E1)

`agents/bdd-implementer.md`, `skills/bdd-red-green`, both reviewers, the hand-off.

An implementer may, without the test being listed:

- **change a test's setup**, where the task's decisions make the old setup impossible: the lines that arrange the
  test, with no assertion, expected value or parametrize case added, removed or changed;
- **rewrite a test written in this batch that pinned an interim state**: a test first committed after the brief's
  `Batch base:` commit, changed to assert what a decision in the brief says, with that decision cited.

It lists each in its report under `## Tests changed under an allowance`: the test, which allowance, and for the
second the decision. Changing what any other test asserts is still a stop, `BLOCKED`, as in 0.11.0. Both reviewers
check every row of that list against the diff, and a change beyond its allowance is Important. Each task carries
`Batch base: <commit>`.

It worked if: hand-backs a batch fall, and the report's judgement of their cause no longer shows a setup or a
same-batch test; and no review finds a weakened test under an allowance.

### 2. Steps where an order must be seen (E2)

The hand-off. A task has Steps only where something must land and be seen green alone before what uses it: a
contract field, a stored layout, a port or a seam. A task with no such order is one dispatch, whatever its file
count: a slice within the budget (12 files) is within a dispatch's (15). 0.11.0's "more than about 5 files" goes.

It worked if: dispatches per slice fall (2.3 in batches 32 and 33) and no implementer's peak context rises past
the baseline's (139k to 161k on 0.11.0).

### 3. The implementer loses the Skill tool (in place of E4)

`agents/bdd-implementer.md`. `bdd-red-green` reaches the implementer through its `skills` field. The Skill tool
was its fallback, and it brings the listing of every installed skill into every dispatch. Without it, an
implementer whose context lacks the skill replies `NEEDS_CONTEXT`.

E4 itself, a brief that carries the rows of `CLAUDE.md` its task needs, is not taken: the baseline shows nothing it
would save.

It worked if: the implementers' mean starting context falls from 29k by about 6k.

### 4. A slice that needs steps only (E6)

`agents/code-scout.md`, the hand-off. The scout's "why it is red" ends with one line per scenario, `steps only` or
`behaviour`. A task whose scenarios are all `steps only` is `Model: sonnet` and `Review: batch-end`, whatever area
it touches, and has no Steps. An implementer who finds such a scenario red on behaviour hands back, as now.

It worked if: implementer output for those slices falls, and none of them hands back.

### 5. Sizes are measured one batch ahead (E8, first half)

`skills/slicing-into-increments`. A `Lands:` probe is run for the slices of the batch about to be planned, and at
most the batch after it. Slices further ahead carry no `Lands:` line until the batch before them closes. `plan`
already accepts a slice without one.

It worked if: scout dispatches described as probes for slices outside the batch fall to none.

### 6. Lanes are marked, not hoped for (E9)

The hand-off. A plan is not ordered or cut to make lanes. A `Lane:` is written only where two tasks' file lists
from the scouts are disjoint. Reviews and scouts run beside the implementer; that is where a batch's parallelism
comes from.

### 7. The controller: one line a slice, one session a batch (E10, and the baseline)

The plan's execution rules.

- The controller writes to the person once when a slice goes green and once when it takes a decision or needs
  one. An agent's notification is acted on, not narrated.
- At the close, after the archive and the measurement, the controller stops and says the next batch is to be
  started in a new session that reads its plan.

It worked if: the controller's cache read a batch falls (26M to 31M), with its peak context under the baseline's
412k.

## Held, with what would decide each

- **Resuming an implementer (E3).** 0.11.0's "no agent is resumed" stands. Changes 2 and 3 take the same cost from
  the other side. Decided by: the facts' "starting context, summed" after this release. If the floor is still a
  large share, try resuming within a task under a context limit; `measure` already counts resumed dispatches.
- **`Review: per-task` by narrower triggers (E5).** The triggers stand. Decided by: `analyzing-a-batch`'s findings
  table over two more batches. If the clean reviews are all of one kind of task, drop that trigger.
- **A budget by kind of change (E7).** The count stands for every kind. Decided by: a batch with a mechanical
  migration cut into migrate slices, its cost per file against slice 156's.
- **One research scout a batch (E8, second half).** A scout a task stands. kb ran one scout for a whole batch and
  it reached 226k of context. Decided by: scouts' share of a batch after change 5.

## Verification

- **Change 1**, headless on a fixture (`/home/vscode/scratch/shopsystem-bdd/allow/`): a task whose decisions need
  one old test's setup changed and one same-batch interim test rewritten, with neither listed. Before: `BLOCKED`.
  After: `DONE`, both listed under the allowance heading. And the same task with an old test whose expected value
  would have to change: `BLOCKED` naming that test, before and after.
- **Change 3**, in the same runs: the implementer's first request, read from the run's transcripts, before and
  after; and that it still works under `bdd-red-green`.
- **Changes 2, 4, 5, 6, 7** are text for the planner and the controller. They are tested by the batch that runs on
  this version, measured against the baseline. The test log says so.
