---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i42-supervision
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i42
status: awaiting-answer
argues: [supervision]
adds: [supervision#r149, supervision#r150]
changes: []
removes: []
date: 2026-10-28
---

# supervision

The drafts of this proposal are in .shop/work/i42/runs/i42/1-integrate/drafts/round-1/.

## Questions
- r150 against r140: an apply that applies nothing also gives the answers its drafts do not hold, so r150 covers r140's case. Line concerned (added): [supervision#r150] **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal. Readings: (a) retire r140 and keep r150, r140's scenario deprecated for r150 (recommended); (b) keep both.
- r150 against r144-r146: a partial apply still fires 'having applied its drafts' (proposal `approved`, formulate starts beside the new integrate). Line concerned (added): [supervision#r150] **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal. Readings: (a) meant, no further line; (b) add r151 '**When** an apply round gives an answer its drafts do not hold, `work run` shall start no `formulate` round for the proposal until the new `integrate` round has been applied.' (recommended); (c) (b) plus r152, keeping the proposal's status.
- r149 against r83: a formulate that formulates nothing and gives no question would be set `formulated`. Line concerned (added): [supervision#r149] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal. Readings: (a) add r151 '**When** a formulate round formulates nothing because answers change lines not in `spec/`, `work run` shall keep the proposal's status.' (recommended); (b) let r83 apply.
- r149 against r131/r132: a formulate that formulates nothing lacks its output. Line concerned (added): [supervision#r149] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal. Readings: (a) add a line that `work run` shall take that case as the round's output, as r147 does for apply (recommended); (b) no line.
