---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i34-supervision
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i34
status: awaiting-answer
argues: [supervision]
adds: [supervision#r122]
changes: []
removes: []
date: 2026-10-25
---

# supervision

The drafts of this proposal are in .shop/work/i34/runs/i34/1-integrate/drafts/round-1/.

## Questions
- Scope of supervision#r122. The line reads: "[r122] **When** `work run` checks a work-item against the whole suite, `work run` shall count as expected to fail each scenario whose requirement a capability-proposal that is neither `formulated` nor `withdrawn` adds or changes." Readings: (a) the check is only the whole-suite run before a merge (r43, which r4 uses), so the line would say "runs the whole suite before a merge"; (b) the check is every whole-suite run for a work-item, the run before an implementer starts (r24) as well as the one before a merge (r43), as the line reads now. Recommended: (b), the line as drafted.

## Answers
- 2026-10-25: (b) every whole-suite run for a work-item, both the run before an implementer starts (r24) and the one before a merge (r43), keeping supervision#r122 as drafted; answered under the person's delegation of 2026-10-25 (recommended reading).
  by: work run, under the delegation "The person, 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release". Answer every question with its recommended reading; where no reading is recommended, choose the one a test can check."
