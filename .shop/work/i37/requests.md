---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i37-requests
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i37
status: awaiting-answer
argues: [requests]
adds: [requests#r23, requests#r24]
changes: [requests#r7]
removes: []
date: 2026-10-26
---

# requests

The drafts of this proposal are in .shop/work/i37/runs/i37/1-integrate/drafts/round-1/.

## Questions
- Decision: narrow r7 (adds r23, r24 are drafted with it).
  Lines: r23 (added) "**When** the upstream ends its turn on a request and `work` sets the request's status to `accepted`, `work` shall keep the request's turn the upstream's." r24 (added) "**When** `work` sets a request's status to `delivered`, `work` shall pass the request's turn to its asker." r7 (changed) "**When** `work turn <request>` is run on a request that it does not set to `accepted`, `work` shall pass the request's turn to the other side." Was: "**When** `work turn <request>` is run, `work` shall pass the request's turn to the other side."
  Readings: (a) narrow r7 as drafted (recommended: r7 and r23 otherwise contradict for an upstream that accepts); (b) leave r7 unchanged, with r23 and r7 contradicting.
- Decision: the glossary entry term/turn.
  Reading (a, recommended): change the entry to "- **turn**: the side of a request, its asker or its upstream, whose part of the request is to be written next, passed to the other side by `work turn` unless the request becomes accepted, and to the asker when the request is delivered." (the old definition disagrees with r23, r24). Reading (b): leave the entry as it is.
- Decision: the Not yet entry "The detail of turns, which the person reserved".
  Readings: (a, recommended) keep it, since this note settles two transitions (r23, r24), not the detail; (b) remove the entry, if this note is taken to give that detail.
- Decision: a line for an already `accepted` request in the asker's turn (q15 itself). Not in the note.
  Reading (a, recommended): no line. Reading (b): add "**While** a request is `accepted` and its turn is the asker's, **when** `work turn <request>` is run, `work` shall pass the request's turn to its upstream."
- Decision: r10's scope of turn (r10 is not changed by the draft; this asks whether to change it).
  Reading (a, recommended): keep "whichever side's turn it is" (the r10 scenario's given is an accepted request in the asker's turn; narrowing would break it). Reading (b): narrow to "**When** `work resolve <request>` is run in the upstream's turn on an `accepted` request with each accepted line's requirement id and the version that holds it, `work` shall write them as the request's resolution."
