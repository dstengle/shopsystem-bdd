---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/review-of-work-items
summary: "A done work-item with a named risk (contract, concurrency, data) gets a task review of its commits; every other is reviewed once by the initiative's branch review; findings to fix now become fix work-items, the rest observations, and every review is a review-finding record."
date: 2026-10-19
status: accepted
supersedes: design-decision/review-by-risk
revisit_when: "more than half of a measured initiative's task reviews find nothing to fix now"
revisit_signal: requests
source: [initiative/i10, design-decision/review-by-risk, measurement/kb-batches-32-35]
by: "(7 of 17 task reviews clean)"
---

# 0040. Review of work-items

## Decision

Risk is set when a work-item is drafted: `contract`, `concurrency`, `data` or `none`. `work run` starts
`bdd-task-reviewer` on a done item with one of the first three, and `bdd-branch-reviewer` over the initiative
branch from its base once every item is done, green or withdrawn. Each finding is graded, names its work-item and is
triaged fix now (correctness, data loss), observation (hardening, with its reproduction) or drop. Fix now becomes a
fix work-item (`fixes:`, `findings:`), planned, whose done is followed by a scoped re-review; after it only data
left invalid, the system's own fault on input, or a write where a refusal belongs gets another round. Observations
are appended to `.shop/records/observations.md`. Models are the agent definitions'; a work-item names none.
