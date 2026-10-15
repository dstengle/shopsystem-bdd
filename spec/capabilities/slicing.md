---
id: shopsystem-bdd/slicing
title: Slicing
narrator: the session that plans a batch
group: service
rests_on: [decision/plans-carry-intent-not-code, decision/slice-budget-refused-by-plan, decision/tests-the-decisions-break, decision/review-by-risk, decision/superpowers-dependency, decision/one-batch-one-session]
formulated_as: features/slicing.feature
retired: []
---

# Slicing

## Purpose
Turns approved feature files into one living plan of thin vertical slices, and hands it to
`superpowers:writing-plans` to become a batch of tasks that carry intent, not code. It is
`slicing-into-increments`, and the only place that decides whether a hand-back changes the contract.
It does not write scenarios and does not implement.

## Behaviour
- [r1] Each slice in the plan is a capability slice with scenarios, or an enabling or stack slice with a check, never both, and has one unknown.
- [r2] **When** slicing starts, the plan's log holds the analysis tools found, and the person is told of any that are missing, what each is for and what the workflow does without it.
- [r3] **When** slices are cut, every scenario that passes in the latest suite record is credited to a slice or to "satisfied by existing behaviour", never to a later slice.
- [r4] **If** the suite takes over 60 seconds and runs serially, with no reason in `CLAUDE.md`, the batch's first slice makes it fast.
- [r5] **If** a slice needs something another project provides and a probe of the installed version fails, the slice is `blocked: awaiting <project>`, a REQUEST is logged and no task is written for it.
- [r6] **If** a slice of the next batch would land in more than 8 production or 4 test modules, it is cut again before it is planned.
- [r7] **When** a decision replaces something existing code assumes, each place that still holds the assumption is owned by a slice, a question for the spec, or a deferral logged with its price.
- [r8] Each capability slice's scenarios carry the tag `@slice-<n>`, and slicing changes nothing else in a feature file.
- [r9] **When** the plan is handed to writing-plans, each task carries its scenarios or check, why each is red today, where the change lands, the decisions taken, the tests those decisions break and what becomes of each, `Review:`, `Model:` and `Retires:`, and no code.
- [r10] **If** a hand-back needs a Given, When or Then line to differ, slicing logs RE-FORMULATE and sends it to formulation, and writes no task for that slice until the line is decided.
- [r11] **When** a semantic the scenarios do not cover must be chosen, slicing logs it as a question for the spec and the slice that depends on it is blocked.
- [r12] **When** a review finding is triaged, correctness and data loss become work in this batch or the next, hardening becomes a backlog line with its reproduction, and polish is fixed only when cheap.
- [r13] **When** the plan is ready for execution, slicing recommends a new session that reads the plan file.

## Implementation, may change
- The plan is `docs/superpowers/plans/*-slices.md`, edited only through `scripts/plan`; slices are numbered in
  execution order, dotted for a slice placed between two.
- `code-scout` dispatches: Lands probes, consequence sweeps, and one research scout per task, all at once.
- The execution rules (paths in, short replies out; by step; review per-task or batch-end; fresh fixes;
  lanes; descriptions; measure at the close; one batch, one session) are copied into the plan's Global
  Constraints for the controller.
- Rationalization and red-flag tables in the skill.

## Not yet
- Slicing drafts work-items under a capability-proposal, filled in stages and pulled from a queue, in place of slices, tasks, steps and lanes — trigger: initiative i4 is approved.
