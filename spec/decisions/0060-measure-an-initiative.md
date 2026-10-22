---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/measure-an-initiative
summary: "`measure initiative` measures one initiative's deliveries from what `work run` records, and the old system's `measure batch` is removed with every line of it."
date: 2026-10-22
status: proposed
source: [initiative/i12, observation/2026-10-19-final-state-only]
by: "the person, 2026-10-22, delegating the drafting decisions to the coordinator's recommendations"
---

# 0060. Measure an initiative

## Decision

`scripts/measure` measures one initiative's deliveries: its work-items, the stages `work run` ran for them, the
sessions of those stages and the commits that landed them, written as one measurement record under
`.shop/records/measurements/`. The old `measure batch` (a superpowers batch: a plan, an archive file under
`docs/superpowers/`, a ledger, slices, a suite record) is removed with every line of it; its lines are retired and
its scenarios deprecated for removal. The capability keeps its file name `batch-measurement`, its ids being scoped
by it; its title, narrator and Purpose become measurement of an initiative's deliveries. It starts as a walking
skeleton measuring what `work run` already records, and grows from the measurements of 0.21.0's, 0.22.0's and
0.23.0's deliveries.
