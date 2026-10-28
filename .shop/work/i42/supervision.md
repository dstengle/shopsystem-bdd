---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i42-supervision
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i42
status: awaiting-answer
argues: [supervision]
date: 2026-10-28
adds: [supervision#r149, supervision#r150, supervision#r151, supervision#r152, supervision#r153]
changes: []
removes: [supervision#r140]
---

# supervision

The drafts of this proposal are in .shop/work/i42/runs/supervision/3-integrate/drafts/round-1/.

## Questions
- r150 against r140: an apply that applies nothing also gives the answers its drafts do not hold, so r150 covers r140's case. Line concerned (added): [supervision#r150] **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal. Readings: (a) retire r140 and keep r150, r140's scenario deprecated for r150 (recommended); (b) keep both.
- r150 against r144-r146: a partial apply still fires 'having applied its drafts' (proposal `approved`, formulate starts beside the new integrate). Line concerned (added): [supervision#r150] **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal. Readings: (a) meant, no further line; (b) add r151 '**When** an apply round gives an answer its drafts do not hold, `work run` shall start no `formulate` round for the proposal until the new `integrate` round has been applied.' (recommended); (c) (b) plus r152, keeping the proposal's status.
- r149 against r83: a formulate that formulates nothing and gives no question would be set `formulated`. Line concerned (added): [supervision#r149] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal. Readings: (a) add r151 '**When** a formulate round formulates nothing because answers change lines not in `spec/`, `work run` shall keep the proposal's status.' (recommended); (b) let r83 apply.
- r149 against r131/r132: a formulate that formulates nothing lacks its output. Line concerned (added): [supervision#r149] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal. Readings: (a) add a line that `work run` shall take that case as the round's output, as r147 does for apply (recommended); (b) no line.
- r152 against r83 (supervision). Line concerned (added): [supervision#r152] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall keep the capability-proposal's status. Existing r83 sets a proposal `formulated` when its formulate round ends without a question; both fit this case. Readings: (a) r152 is read as the exception and r83 stands, no change (recommended); (b) narrow r83: retire r83 and add r154 '**When** a round of the kind `formulate` that `work run` started for a capability-proposal ends without giving a question and having formulated its scenarios, `work run` shall transition the proposal to `formulated`.'
- r150/r151 against r144 and r145 (supervision). Lines concerned (added): [supervision#r150] **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal. [supervision#r151] **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start no round of the kind `formulate` for the capability-proposal until the new round of the kind `integrate` has been applied. A partial apply still transitions the proposal to `approved` (r144) and writes its adds, changes and removes (r145) while the new integrate round runs. Readings: (a) meant, no further line (recommended); (b) add r154 '**When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall keep the capability-proposal's status.'

## Answers
- 2026-10-28: r150 against r140: reading (a), retire r140 and keep r150, r140's scenario deprecated for r150 (the person, 2026-10-28: take recommendations).
- 2026-10-28: r150 against r144-r146: reading (b), add r151 'When an apply round gives an answer its drafts do not hold, work run shall start no formulate round for the proposal until the new integrate round has been applied.' (the person, 2026-10-28: take recommendations).
- 2026-10-28: r149 against r83: reading (a), add a line 'When a formulate round formulates nothing because answers change lines not in spec/, work run shall keep the proposal's status.' (the person, 2026-10-28: take recommendations).
- 2026-10-28: r149 against r131/r132: reading (a), add a line that work run shall take that case as the round's output, as r147 does for apply (the person, 2026-10-28: take recommendations).
- 2026-10-28: r152 against r83: reading (a), r152 is read as the exception and r83 stands, no change (answered by the coordinator under the person's delegation of 2026-10-28, taking the recommended reading).
