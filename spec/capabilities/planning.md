---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/planning
title: Planning
narrator: the script `work run`, which started the planner
group: service
rests_on: [design-decision/plans-carry-intent-not-code, design-decision/plans-list-the-tests-they-break, design-decision/worker-results-are-files, design-decision/the-file-set-is-the-claim]
retired: []
---

# Planning

## Purpose
Turns one researched work-item into a plan an implementer can follow alone: the decisions the spec leaves open,
the tests they break, and the final file set. It is `bdd-planner`, started by `work run` on a `researched`
work-item; it plans from the researcher's notes and gives intent, never code. A walking skeleton
(design-decision/behaviour-lines-are-ears): it grows from what running it shows.

## Behaviour
- [r1] **When** the planner is started on a work-item, the planner shall write a plan to the plan file its brief names.
- [r2] **When** the planner writes the plan, the planner shall name in it each decision the capability's Behaviour leaves open, with the requirement or design-decision it rests on.
- [r3] **When** the planner writes the plan, the planner shall list in it each test a decision of the plan breaks, with what becomes of it.
- [r4] The planner shall put in the plan no code block, file contents, diff or step-definition body.
- [r5] **When** planning ends, the planner shall write its result with the outcome `DONE` or `QUESTION` and the final file set.
- [r6] **If** a decision would change what the capability's narrator observes and no requirement or design-decision settles it, then the planner shall give the outcome `QUESTION`, with the question and its readings.
- [r7] **While** planning, the planner shall change no file but the plan and its result.
- [r8] **If** the planner cannot do what it was asked, then the planner shall stop with the outcome `NEEDS_CONTEXT`, saying why.

## Implementation, may change
- `agents/bdd-planner.md`: tools Read, Glob, Grep, Write. The plan is `plan.md` in its stage directory.

## Not yet
- What the plan names to reuse and to verify with, reasons a test is red today, defects from probes, skipped
  steps, dry-run agreement tests, a bound on the reading and on the summary (see skeleton-notes.md).
