---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/living-plan-to-work-items
summary: "A living plan's open slices become work-items under one capability-change initiative, migrated-plan, with one formulated capability-proposal per capability; its backlog and open log entries become observations; the plan itself becomes a record."
date: 2026-10-19
status: accepted
source: [observation/2026-10-19-final-state-only]
by: "the person, 2026-10-19"
---

# 0050. A living plan becomes work-items and observations

## Decision

- Each slice that is not green and that the person keeps at the gate is a `planned` work-item
  `work-item/<context path>/slice-<n>` (dots in `n` as hyphens). A capability slice is `under` the capability
  of its first scenario and `accepts` the requirements its scenarios are tagged with. An enabling or stack
  slice keeps its `check` and is `for` the first capability slice after it in the plan; with none after it,
  nothing needs it yet, and it is an observation.
- The work-items are parts of `initiative/<context path>/migrated-plan` (capability-change, `started`), through
  one `capability-proposal/<context path>/migrated-<capability>` per capability, `formulated` with no `adds`:
  its requirements are approved and formulated already. Its source is an observation of the migration.
- Each Backlog entry, and each Log entry that is a `QUESTION FOR THE SPEC:`, a `REQUEST` or a `RE-FORMULATE`,
  is an observation `about` the bounded context, unless the person leaves it out at the gate. Origins are
  triaged like any other.
- The plan's order is not kept as `blocked_by`: it said what should come first, not what must. Each
  work-item's body notes its place in the old plan.
- The plan file and its archives are `initiative-archive` records under `.shop/records/archive/plans/`.

## Alternatives

One defect initiative per slice (a defect initiative takes one work-item, and a slice is not a defect);
backlog entries as work-items (most are hardening noticed in review, which v3 makes origins, not work).
