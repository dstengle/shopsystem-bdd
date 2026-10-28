# Gate, round 1 (q22)

## supervision
Added:
- [r149] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal.  (q22 line 1)
- [r150] **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal.  (q22 line 3)

## spec-integration
Added:
- [r46] **When** a round of the kind `apply` ends, `initiative-round` shall give in its result each answer of the capability-proposal that the drafts it applied do not hold.  (q22 line 2)

No glossary entries, no decisions, no changed or removed lines.

## Questions
1. supervision r150 vs r140: with r46, an apply that applies nothing also gives the answers its drafts do not hold, so r150 covers r140's case. (a) Retire r140, keep r150 (recommended); r140's scenario deprecated for r150. (b) Keep both.
2. supervision r150 vs r144-r146: a partial apply still fires "having applied its drafts" (proposal `approved`, formulate starts beside the new integrate). (a) Meant: no line. (b) r151 **When** an apply round gives an answer its drafts do not hold, `work run` shall start no `formulate` round for the proposal until the new `integrate` round has been applied. (c) As (b) plus r152: keep the proposal's status. Recommended: (b).
3. supervision r149 vs r83: a formulate that formulates nothing and gives no question would be set `formulated`. (a) r151 **When** a formulate round formulates nothing because answers change lines not in `spec/`, `work run` shall keep the proposal's status (recommended). (b) Let r83 apply.
4. supervision r149 vs r131/r132: a formulate that formulates nothing lacks its output. (a) r151 **When** ... formulates nothing because answers change lines not in `spec/`, `work run` shall take that as the round's output, as r147 does for apply (recommended). (b) No line.
5. formulation, counterpart of r46: how the formulate round reports it formulated nothing. (a) Add **When** a round of the kind `formulate` is given answers that change lines not in `spec/`, `initiative-round` shall formulate nothing and give in its result each answer that changes them (recommended). (b) No line.

## Cut sentences
1: the request's title (lines 1 to 3 cover it).
