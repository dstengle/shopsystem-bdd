---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i33-work-queue
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i33
status: formulated
argues: [work-queue]
adds: [work-queue#r31, work-queue#r32]
changes: []
removes: []
date: 2026-10-25
---

# work-queue

The drafts of this proposal are in .shop/work/i33/runs/i33/1-integrate/drafts/round-1/.

## Questions
- r31 against work-queue r23 (and supervision r105, r75). Line: [r31] If every work-item of an initiative is `withdrawn`, then `work` shall leave the initiative's status as it is. r23 sets an initiative `done` when every work-item is `green` or `withdrawn`, which an all-`withdrawn` initiative meets, so they contradict. Readings: (a, recommended) change r23 to "[r23] When a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`.", change supervision r105 "that has at least one work-item" to "that has at least one work-item that is `green`", and add to r75 "and at least one of them is `green`"; (b) leave r23, r105, r75 as they are; r31 overrides them and they read as contradicting it.
- r120's subject. Line: [r120] When the delegation-answerer answers a reviewer's question on a work-item, the delegation-answerer shall give in its result whether its answer asks for a change or accepts the work-item as it is. "the delegation-answerer" is no glossary term; r77 calls it "a session of its own, given the delegation". Readings: (a, recommended) recast: "[r120] Where the request an initiative fulfils gives a delegation, when a session that `work run` started under it answers a reviewer's question on a work-item, the session shall give in its result whether its answer asks for a change or accepts the work-item as it is."; (b) keep r120 as drafted and add the glossary entry "- **delegation-answerer**: the session `work run` starts under a request's delegation to answer one question of an initiative."
- r120, the result's field (the note gives none). Readings: (a, recommended) draft none; (b) add under Implementation: "- r120: the answer's result gives `change` or `accept`, as `work answer`'s `--change` and `--accept` (work-queue r26, r27)."
- r121, "whatever its status". Line: [r121] When a kept branch review's result gives no question, `work run` shall take the review as listing nothing to fix now, whatever its status. Readings: (a, recommended) the status of the review's result (its outcome, e.g. `DONE` or `PARTIAL`): r121 as drafted; (b) the review's verdict: "[r121] When a kept branch review's result gives no question, `work run` shall take the review as listing nothing to fix now, whatever verdict the review gives."
- r121 and a branch reviewer's session that ends in error, at its turn limit, or with no readable result. Readings: (a, recommended) add nothing; (b) add "[r122] If a branch reviewer's session ends in an error or at its turn limit or leaves no result `work run` can read, then `work run` shall take the review as not read."

## Answers
- 2026-10-25: (a) Change r23, supervision r105 and r75 as proposed, so that an initiative is set done only when it has at least one green work-item. This answers under the person's delegation of 2026-10-25: answer every question with its recommended reading.
  by: work run, under the delegation "The person, 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release". Answer every question with its recommended reading."
- 2026-10-25: (a) recast r120 as: [r120] Where the request an initiative fulfils gives a delegation, when a session that `work run` started under it answers a reviewer's question on a work-item, the session shall give in its result whether its answer asks for a change or accepts the work-item as it is. (Answered under the person's delegation of 2026-10-25: every question with its recommended reading.)
  by: work run, under the delegation "The person, 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release". Answer every question with its recommended reading."
- 2026-10-25: (a) draft none, under the person's delegation 2026-10-25 to answer every question with its recommended reading
  by: work run, under the delegation "The person, 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release". Answer every question with its recommended reading."
- 2026-10-25: (a) the status of the review's result (its outcome, e.g. DONE or PARTIAL): r121 as drafted, under the person's delegation of 2026-10-25 to answer every question with its recommended reading.
  by: work run, under the delegation "The person, 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release". Answer every question with its recommended reading."
- 2026-10-25: (a) Add nothing, under the person's delegation of 2026-10-25: "Answer every question with its recommended reading."
  by: work run, under the delegation "The person, 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release". Answer every question with its recommended reading."
