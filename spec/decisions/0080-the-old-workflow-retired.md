---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired
summary: "The requirement lines of plugin 1.x's workflow (its stages, `work run`, the work-item queue, delegations, `measure initiative` and `model check` on `.shop/work/`) are retired in bulk in 2.0.0; a retired capability keeps its file as the record of its ids, and the guarantees left are checked by script tests, never as fixture sessions."
date: 2026-11-05
status: accepted
tier: judgement
supersedes: [design-decision/workflow-capabilities-are-guarantees]
source: [record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-design, record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-9]
by: "workflow simplification plan 9, decided by the planner; revisit"
---

# 0080. The old workflow retired

## Context

The workflow simplification (0074) replaces initiatives, work-items, proposals, the stage pipeline and `work run` with
items, a backlog, batches and one review at the pull request. The design says the old capabilities' requirements are
retired in bulk under one decision, never rewritten (retire, never edit). Decision 0065 made the ten workflow
capabilities guarantees checked by `measure` on real batches; most of what they guarantee is now gone.

## Decision

These codified lines are retired in plugin 2.0.0, each id written into its capability's `retired:` and never reused:

- every line of `supervision`, `work-queue`, `review`, `spec-consistency`, `spec-integration`, `red-green`,
  `spec-migration`, `delivery`, `planning`, `code-research`, `role-boundaries` and `formulation` (which had none left);
- `batch-measurement` r1-r17 (`measure initiative`);
- `requests` r3, r4 and r10-r13 (delegations);
- `design-model-check` r8, r9, r12-r18, r21, r26, r27, r29, r31-r35, r37, r39, r45, r46 and r53 (work-items,
  initiatives, proposals and `model why`'s proposals);
- `migration-tools` r22 and r23 (the hooks' initiative text).

A capability whose every line is retired keeps its file: its Purpose opens with the notice of the retirement, its
Terms, Relations and `rests_on` stay (so the lexicon does not move), its Behaviour is empty, and each of its 0.29 ids
that only its retired groups restated is listed under `## Dropped` as retired with the lines that restated it. It is
listed under "Retired in 2.0.0" in `spec/index.md`, and a service capability with no group has no feature file.

The guarantees left are `trials`, `pr-review` and `brainstorming`. They are checked by script tests under
`tests/scripts/`, never as fixture sessions.

## Consequences

The retired ids stay unreusable (v15c), and frozen references to them under `.shop/work/` still name a file.
`model restates` keeps every 0.29 id covered, restated by a kept group or dropped with its reason.
