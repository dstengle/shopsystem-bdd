---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i56-work-queue
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i56
status: awaiting-answer
argues: [work-queue]
adds: [work-queue#r46]
changes: []
removes: []
date: 2026-10-28
---

# work-queue

The drafts of this proposal are in .shop/work/i56/runs/i56/1-integrate/drafts/round-1/.

## Questions
- work-queue r46 (added, from q27 line 3): `**While** a request has no lines, `work start` shall start no initiative for it.` A request with a reason and no lines can never be `accepted` (requests r8 needs one accepted line), so work-queue r22 and supervision r103 never fire for it and r46 is only a guard. Readings: (a) r46 as drafted, a guard and nothing more. (b) r46 as drafted, and also add `**If** `work start` is run on a request that has no lines, **then** `work start` shall refuse, because the request has no lines, and change nothing.` (c) Drop r46 here and place the guard in supervision: `**While** a request has no lines, `work run` shall start no initiative for it with `work start`.` Recommended: (a).
