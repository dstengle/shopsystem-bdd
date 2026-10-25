---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i33-supervision
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i33
status: awaiting-answer
argues: [supervision]
adds: [supervision#r120, supervision#r121]
changes: []
removes: []
date: 2026-10-25
---

# supervision

The drafts of this proposal are in .shop/work/i33/runs/i33/1-integrate/drafts/round-1/.

## Questions
- Q1 (work-queue r31, against r23, supervision r105, r75). Added line: [r31] **If** every work-item of an initiative is `withdrawn`, **then** `work` shall leave the initiative's status as it is. r23 sets an initiative `done` when every work-item is `green` or `withdrawn`, which an all-`withdrawn` initiative meets, so r23 and r31 contradict. (a, recommended) Change r23 to: "[r23] **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`."; likewise change supervision r105 "that has at least one work-item" to "that has at least one work-item that is `green`", and add to r75 "and at least one of them is `green`". (b) Leave r23, r105, r75 as they are; r31 overrides them and they read as contradicting it.
- Q2 (work-queue r32). Added line: [r32] **If** `work add` is given an initiative that is `done` or `abandoned`, **then** `work add` shall refuse, naming the initiative's status, and change nothing. (Drafted without a question in the gate text; confirm it as drafted.) (a, recommended) Keep r32 as drafted. (b) Drop r32.
- Q3 (supervision r120, subject). Added line: [r120] **When** the delegation-answerer answers a reviewer's question on a work-item, the delegation-answerer shall give in its result whether its answer asks for a change or accepts the work-item as it is. "the delegation-answerer" is no glossary term; r77 calls it "a session of its own, given the delegation". (a, recommended) Recast: "[r120] **Where** the request an initiative fulfils gives a delegation, **when** a session that `work run` started under it answers a reviewer's question on a work-item, the session shall give in its result whether its answer asks for a change or accepts the work-item as it is." (b) Keep r120 as drafted and add the glossary entry "- **delegation-answerer**: the session `work run` starts under a request's delegation to answer one question of an initiative."
- Q4 (supervision r120, the result's field). The note gives none. (a, recommended) Draft none. (b) Add under Implementation: "- r120: the answer's result gives `change` or `accept`, as `work answer`'s `--change` and `--accept` (work-queue r26, r27)."
- Q5 (supervision r121, "whatever its status"). Added line: [r121] **When** a kept branch review's result gives no question, `work run` shall take the review as listing nothing to fix now, whatever its status. (a, recommended) The status of the review's result (its outcome, e.g. `DONE` or `PARTIAL`): r121 as drafted. (b) The review's verdict: "[r121] **When** a kept branch review's result gives no question, `work run` shall take the review as listing nothing to fix now, whatever verdict the review gives." Related, optional: a branch reviewer's session that ends in error, at its turn limit or with no readable result; (a, recommended) add nothing; (b) add "[r122] **If** a branch reviewer's session ends in an error or at its turn limit or leaves no result `work run` can read, then `work run` shall take the review as not read."
