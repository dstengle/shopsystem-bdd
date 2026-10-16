---
id: model-check
kind: capability-proposal
part_of: i2
status: drafted
date: 2026-10-15
argues: [design-model-check]
adds: [design-model-check#r1-r43]
---

# Design model check

Built ahead of the gate, on the same branch, so the gate sees it working: approving these ids approves
`scripts/model` and `scripts/model.lp` as they stand. r1-r18 are formulated in
`features/design-model-check.feature`; r19-r43, added 2026-10-16, are not yet.

Decisions: model-check-solves-with-clingo, scenario-names-requirement-by-tag,
retired-ids-in-capability-frontmatter, work-file-forms, capability-ids-are-context-scoped,
plugin-scenarios-run-as-unittest.
