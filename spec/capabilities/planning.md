---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/planning
title: Planning
narrator: the supervisor that started the planner
group: service
rests_on: [design-decision/plans-carry-intent-not-code, design-decision/plans-list-the-tests-they-break, design-decision/worker-results-are-files, design-decision/the-file-set-is-the-claim]
formulated_as: features/planning.feature
retired: []
---

# Planning

## Purpose
Turns one researched work-item into a plan an implementer can follow alone: the decisions the spec leaves open,
the tests those decisions break and what becomes of each, the final file set, what to reuse and how to verify. It
is `bdd-planner`, started by `work run` on a `researched` work-item. It plans from the researcher's notes and
gives intent, never code. A decision a client would observe that nothing settles is a question, not a plan.

## Behaviour
- [r1] **When** planning ends, the plan is in the plan file the brief names, the result file gives the final file set, the capabilities the work depends on and the questions, and the checkout is unchanged.
- [r2] The plan says, for each scenario the work-item accepts or for its check, why it is red today from the researcher's notes, marking as unverified each reason the notes mark `read`.
- [r3] The plan states each decision the capability's Behaviour leaves open, with the requirement or design-decision it rests on.
- [r4] The plan lists under Tests the decisions break every test the researcher's notes name and every test in the file set that a decision of the plan changes, each with what becomes of it: rewritten, and to assert what, or a question; an empty list says what was checked.
- [r5] The plan names the step definitions and fixtures to reuse, the commands that verify the work with the number of scenarios each runs, and the deprecated scenarios the work-item retires.
- [r6] The plan has no code block, file contents, diff or step-definition body.
- [r7] **If** a decision would change what the capability's narrator observes and no requirement or design-decision settles it, the result is `QUESTION`, giving the question, its readings and what the plan becomes under each.
- [r8] **If** what becomes of a broken test would change what a client observes, it is a question, not a rewrite.
- [r9] The final file set is the researcher's, with each file the plan's decisions add, each named.
- [r10] **When** the researcher's notes report a defect a probe found, the plan fixes it in this work-item when it is a wrong answer or lost data on the work-item's path, and otherwise the result gives it as an observation with its reproduction.
- [r11] **When** the notes list refusals and effects that only a skipped stage produces, the plan's decisions say for each what the new path does about it.
- [r12] **Where** the system has a dry run and a real run of an operation the work-item touches, the plan names the randomized test that they agree, and the work-item writes it when none exists.
- [r13] The planner reads the work-item, the researcher's notes, `spec/`, `features/`, `CLAUDE.md` and the files of the file set, and no other code.
- [r14] The result's status is `DONE`, `QUESTION` or `NEEDS_CONTEXT`, and its summary is under fifteen lines.

## Implementation, may change
- `agents/bdd-planner.md`: tools Read, Glob, Grep, Write; Opus. The plan is `plan.md` in the stage's run directory.
- A ruled work-item is not planned again: the ruling is under its `## Rulings`, for the implementer.

## Not yet
- None.
