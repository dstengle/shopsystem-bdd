---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-review
kind: capability-proposal
part_of: initiative/i10
status: merged
date: 2026-10-19
argues: [review]
adds: [review#r12-r14]
changes: [review#r1, review#r3-r4, review#r6, review#r8, review#r10-r11]
removes: []
---

# Review: work-items and initiatives

What the gate approves: added `review#r12-r14`, changed `#r1`, `#r3`, `#r4`, `#r6`, `#r8`, `#r10`, `#r11`, and the
narrator "the supervisor closing a work-item or an initiative" (was "the controller closing a task or a batch").

A task review covers one work-item's commits, a branch review the initiative branch (r13); each finding names its
work-item and its triage (r12), from which `work run` makes fix work-items and observations; the backlog is gone
(r8). The architecture reviewer gives a refactor as an observation with a check, not a slice (r14). The Not yet
entry is done. Decision: design-decision/review-of-work-items (supersedes design-decision/review-by-risk).

Glossary, added:
- **fix work-item**: a work-item `work run` adds for a review's findings to fix now, naming the work-item it fixes.
