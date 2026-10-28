# supervision: formulate round 1

## Coverage

| id | line | scenario |
|---|---|---|
| r150 | "**When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal." | an apply round that gives an answer the drafts it applied do not hold is followed by a new integrate round for the proposal (replaces the @r140 scenario, in its place) |
| r151 | "**When** a round of the kind `apply` gives in its result an answer that the drafts it applied do not hold, `work run` shall start no round of the kind `formulate` for the capability-proposal until the new round of the kind `integrate` has been applied." | an apply round that gives an answer the drafts it applied do not hold is followed by no formulate round for the proposal before the new integrate round's drafts are applied |
| r149 | "**When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall start a new round of the kind `integrate` for the capability-proposal." | a formulate round that formulates nothing because the proposal's answers change lines not in spec/ is followed by a new integrate round for the proposal |
| r152 | "**When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall keep the capability-proposal's status." | a formulate round that formulates nothing because the proposal's answers change lines not in spec/ leaves the proposal's status as it was |
| r153 | "**When** a round of the kind `formulate` formulates nothing because a capability-proposal's answers change lines not in `spec/`, `work run` shall take that as the round's output." | a formulate round that formulates nothing because the proposal's answers change lines not in spec/ has given its output |

r140 is removed. Its scenario is replaced by the @r150 scenario, and no scenario is written for r140. No other scenario changes.

## Questions

None. No line here has two readings for the case its scenario shows. The conflicts between lines are listed below.

## Cases no line mentions (no scenario written)

- An apply round that applied p1's drafts and also gives an answer they do not hold. r144 and r146 say p1 goes to approved and a formulate round starts. r151 says no formulate round starts until the new integrate round's drafts are applied. Which line wins needs a ruling. The scenarios for r150 and r151 show only the case where the apply round applies nothing.
- A formulate round that formulates nothing because the answers change lines not in spec/, and gives no question. r83 says p1 goes to formulated; r152 says p1 keeps its status. The draft takes it that r152 wins in this case, but neither line says so.
- r151's "until the new round of the kind integrate has been applied": no line says which apply round counts. Presumably it is the apply round of the proposal drafted anew after its next gate. The scenario checks only one `work run`, where no formulate round starts. It does not check that a formulate round does start once the new drafts are applied.
- r152 does not say how long the status is kept. r143 keeps it while the integrate round runs, and r142 sets drafted after it. The scenario checks only from the formulate round to the start of the integrate round.
- A formulate round that formulates scenarios for some lines and also finds that answers change lines not in spec/. Is this "formulates nothing" (r149, r152, r153), or r83?
- A proposal at approved, coming straight from its apply round, whose formulate round formulates nothing for this reason. The scenarios use only a proposal at awaiting-answer whose formulate round's question has an answer (r116).

## Drafts

- /home/vscode/shopsystem-bdd/.shop/worktrees/supervision-6-formulate/.shop/scratch/6-formulate/drafts/round-1/supervision.feature
