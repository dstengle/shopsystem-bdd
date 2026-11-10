---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/measure-a-batch
summary: "`measure batch <batch>` measures one batch from git and its sessions' transcripts: wall time, session time, tokens and cost by role, the pull request's findings by grade, its defects and its knobs."
date: 2026-11-05
status: accepted
tier: requirement
enforced_by: [telemetry#r5, telemetry#r6, telemetry#r7, telemetry#r8]
supersedes: [design-decision/measure-an-initiative]
source: [record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-design]
by: "workflow simplification plan 7, decided by the planner; revisit"
---

# 0078. Measure a batch

## Decision

`measure batch <batch>` measures one batch from git and its sessions' transcripts on disk: wall time, session time,
tokens and cost by role, the pull request's findings by grade, the defects traced to their items (`measure defect`)
and the knobs it ran with, written as one measurement record. It replaces 0060's measurement of an initiative, which
`work run` keeps until the old queue is retired.
