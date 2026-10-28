---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i56-supervision
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i56
status: awaiting-answer
argues: [supervision]
adds: [supervision#r183]
changes: []
removes: []
date: 2026-10-28
---

# supervision

The drafts of this proposal are in .shop/work/i56/runs/i56/1-integrate/drafts/round-1/.

## Questions
- supervision r183, "takes in". Line: [r183] **When** `work run` takes in a request that has a reason and no lines, `work run` shall start a round that drafts its lines from its reason and gives them to the person as a question. (a) The take-in of requests r39/r40, of what is sent from another repository, as drafted. (b) Any request of which this context is the upstream, an internal one included: r183 becomes `**When** a request of which this context is the upstream is `open` or `awaiting-upstream` and has a reason and no lines, `work run` shall start a round that drafts its lines from its reason and gives them to the person as a question.` Recommended: (a).
- supervision r183, the round and r67. Line: [r183] as above. (a) The round is a new kind (an `initiative-round` session of a kind named in Implementation), and add `**While** a request has no lines, `work run` shall start no round of the kind `intake` for it.` (b) It is the `intake` round, given the reason; r132 then changes to give, for an intake round of a lineless request, its drafted lines as its output. Recommended: (a), because the intake round judges lines and a lineless request has none.
- supervision r183, where the question goes. Line: [r183] as above. (a) In the request, as the upstream's question (r100, requests r20), with the turn passed to the asker: add `**When** the round r183 starts gives a request's drafted lines, `work run` shall write them in the request as a question.` (b) To the person at the end of `work run`: add `**When** `work run` ends while a request's drafted lines have no answer, `work run` shall exit with an error, printing the request with its drafted lines.` (design-decision/exits-are-successful-or-errors) Recommended: (a), because the request already carries the upstream's questions and the asker's answers.
