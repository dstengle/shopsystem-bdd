# Gate, round 1 (q22, drafted anew from its answers)

Drafts: .shop/scratch/3-integrate/drafts/round-1/spec/capabilities/supervision.md

## supervision

Added (each under supervision):
- [r149] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal.  (q22 line 1)
- [r150] **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal.  (q22 line 3)
- [r151] **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start no round of the kind `formulate` for the capability-proposal until the new round of the kind `integrate` has been applied.  (answer "r150 against r144-r146", the person, 2026-10-28)
- [r152] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall keep the capability-proposal's status.  (answer "r149 against r83", the person, 2026-10-28)
- [r153] **When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall take that as the round's output.  (answer "r149 against r131/r132", the person, 2026-10-28)

Removed:
- [r140] **When** a round of the kind `apply` applies nothing because a capability-proposal's answers give what its drafts do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal.  Id retired (frontmatter `retired` gets r140); its scenario is deprecated for r150. (answer "r150 against r140", the person, 2026-10-28)

spec-integration r46 is applied already; nothing drafted for it. No glossary entries, no decisions, no changed lines.

## Questions

1. supervision r152 against r83: both fit a formulate round that formulates nothing for answers that change lines not in `spec/` and gives no question; r152 keeps the status, r83 sets `formulated`. (a) r152 is read as the exception, r83 stands: no change (recommended). (b) Narrow r83: retire r83 and add r154 **When** a round of the kind `formulate` that `work run` started for a capability-proposal ends without giving a question and having formulated its scenarios, `work run` shall transition the proposal to `formulated`.
2. supervision r150/r151 against r144 and r145: a partial apply still transitions the proposal to `approved` (r144) and writes its `adds`, `changes` and `removes` (r145) while the new integrate round runs. (a) Meant: no line (recommended). (b) Add r154 **When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall keep the capability-proposal's status.

## Cut sentences
0 (the request's title was cut in round 1 of i42's earlier drafts and is not drafted here).
