---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/planning
title: Planning
narrator: the script `work run`, which started the planner
group: guarantees
rests_on: [design-decision/plans-carry-intent-not-code, design-decision/plans-list-the-tests-they-break, design-decision/worker-results-are-files, design-decision/the-file-set-is-the-claim, design-decision/workflow-capabilities-are-guarantees]
language: codified-1
retired: []
---

# Planning

## Purpose
Turns one researched work-item into a plan an implementer can follow alone: the decisions the spec leaves open,
the tests they break, and the final file set. It is `bdd-planner`, started by `work run` on a `researched`
work-item; it plans from the researcher's notes and gives intent, never code. A walking skeleton
(design-decision/behaviour-lines-are-ears): it grows from what running it shows.

## Terms

- **plan** (kind): the file `plan.md` a planner writes in its stage directory: intent, never code.
- **plan decision** (kind): a decision a plan makes that the capability's requirements leave open, named with the requirement or design-decision it rests on.
- **code block** (kind): code, file contents, a diff or a step-definition body written out in a plan.
- **broken by** (relation test → plan decision): a test a decision of the plan makes impossible to keep, with what becomes of it.
- **settled by** (relation plan decision → requirement): the requirement or design-decision that settles a decision.

## Behaviour

### [g1] The planner writes a plan
Restates: r1@0.29.
- [r1] When `work run` starts a `plan` stage, the planner shall write a plan.

### [g2] The plan names its decisions and the tests they break
Restates: r2@0.29, r3@0.29.
- [r2] When the planner writes a plan, the planner shall name every plan decision.
- [r3] When the planner writes a plan, the planner shall list every test broken by a plan decision.

### [g3] A plan holds no code
Restates: r4@0.29.
- [r4] The planner shall not write a code block.

### [g4] Planning ends with a result and the final file set
Restates: r5@0.29.
- [r5] When the planner ends a `plan` stage, the planner shall write a result.
- [r6] When the planner ends a `plan` stage, the planner shall write a file set.

### [g5] A decision no requirement settles is a question
Restates: r6@0.29.
- [r7] If the planner finds a plan decision settled by no requirement, then the planner shall write a result that is `QUESTION`.
- [r8] If the planner finds a plan decision settled by no requirement, then the planner shall ask a question.

### [g6] The planner changes no file of the worktree
Restates: r7@0.29.
- [r9] The planner shall not change a file in a worktree.

### [g7] A planner that cannot do what it is asked says why
Restates: r8@0.29.
- [r10] If the planner refuses a brief, then the planner shall write a result that is `NEEDS_CONTEXT`.
- [r11] If the planner refuses a brief, then the planner shall write a reason.

## Implementation, may change
- `agents/bdd-planner.md`: tools Read, Glob, Grep, Write. The plan is `plan.md` in its stage directory, and the plan
  and its result are the only files the planner writes.
- A question gives its readings.

## Not yet
- What the plan names to reuse and to verify with, reasons a test is red today, defects from probes, skipped
  steps, dry-run agreement tests, a bound on the reading and on the summary (see skeleton-notes.md).

## Dropped
