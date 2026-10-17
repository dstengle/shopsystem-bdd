---
id: initiative/missingmass.io/shopsystem/shopsystem-bdd/i4
title: Work-items in place of slices, tasks, steps and lanes
summary: Slicing drafts work-items under a capability-proposal, filled in stages (drafted, researched, planned, ready), with the scout's file set kept as the claim; writing-plans is no longer invoked.
kind: capability-change
owner-level: shopsystem-bdd
status: proposed
priority: 4
source: [review-finding/2026-10-13-kb-and-bdd-assessment]
date: 2026-10-15
---

Run by hand first: one session pulls items one at a time, to learn whether an item is self-contained
enough that a fresh agent needs nothing else. `scripts/plan` becomes a `work` script over `work/`.

The workflow capabilities get their first scenarios here, as fixture sessions
(design-decision/workflow-scenarios-run-as-fixture-sessions), against the behaviour this initiative brings
rather than 0.18.0's; i1 leaves them unformulated for that reason. The fixture generators and run
harness move into the repository with them.
