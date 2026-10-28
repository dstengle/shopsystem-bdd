---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i55-work-queue
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i55
status: awaiting-answer
argues: [work-queue]
adds: [work-queue#r47]
changes: []
removes: []
date: 2026-10-28
---

# work-queue

The drafts of this proposal are in .shop/work/i55/runs/i55/1-integrate/drafts/round-1/.

## Questions
- Decision: r47 against work-queue r23 (done set with no condition on capability-proposals). Line concerned: [work-queue r47] **If** every work-item of an initiative is `green` or `withdrawn` while one of its capability-proposals is neither `formulated` nor `withdrawn`, **then** `work` shall keep the initiative `started`. (added; q21 line 11). Readings: (a, recommended) retire work-queue r23 for "[r48] **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn`, that every capability-proposal of it is `formulated` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`." and retire supervision r105 for the same condition; (b) keep r23 and r105, r47 the exception; (c) change only r23.
- Decision: r47 and `merged` capability-proposals. Line concerned: [work-queue r47] **If** every work-item of an initiative is `green` or `withdrawn` while one of its capability-proposals is neither `formulated` nor `withdrawn`, **then** `work` shall keep the initiative `started`. (added; q21 line 11). Readings: (a, recommended) as drafted, word for word; (b) "neither `formulated`, `merged` nor `withdrawn`".
