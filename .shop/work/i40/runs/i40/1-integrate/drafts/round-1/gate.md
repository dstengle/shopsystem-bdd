# Gate: i40, round 1 (request q18, lines 1-4)

## supervision (`.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/supervision.md`)
Added:
- [r137] **When** a round of the kind `apply` applies nothing because a capability-proposal's answers give what its drafts do not hold, `work run` shall start a new round of the kind `integrate` for the capability-proposal.
- [r138] **When** `work run` starts a round of the kind `integrate` for a capability-proposal that has answers, `work run` shall give the round the capability-proposal's questions and answers and the initiative's ledger, with the accepted lines of the request the initiative fulfils.
- [r139] **When** a round of the kind `integrate` drafts a capability-proposal anew from its answers, `work run` shall set the capability-proposal `drafted`, its earlier drafts kept in their round's directory.

Changed: none. Removed: none.

## spec-integration (`.../round-1/spec/capabilities/spec-integration.md`)
Added:
- [r45] **When** a round of the kind `integrate` is given answers that ask for lines the request's accepted lines do not, `initiative-round` shall draft those lines under the capabilities the answers name.

Changed: none. Removed: none.

Glossary: no entry added, changed or removed. Decisions: none.

## Questions
1. r80, r71, r114 (supervision) fire whenever an `apply` round ends, so an `apply` that applies nothing would also set the proposal `approved`, start `formulate` and write `adds`/`changes`/`removes`, against r137.
   - (a, recommended) change each to "**When** a round of the kind `apply` that `work run` started for a capability-proposal ends having applied its drafts, ..." (ids kept: changed lines r80, r71, r114).
   - (b) leave them, so both happen.
2. r132/r131 (supervision): an `apply` round's output is its change list; one that applies nothing may give none, and r131 would write a question and set `awaiting-answer`.
   - (a) an empty change list counts as the output: no line changes.
   - (b) change r132 to "... an integrate round's change list; an apply round's change list, or that it applied nothing because the answers give what the drafts do not hold; ...".
3. The proposal's status while the new `integrate` round runs is not given.
   - (a) kept: add "**When** `work run` starts a round of the kind `integrate` for a capability-proposal, `work run` shall keep the proposal's status until the round ends."
   - (b) set `drafted` at once: r139 moves to the start of the round.
4. r92 (supervision) writes a `drafted` proposal for each capability a change list names. In a redrafting round, does it write a second proposal for the proposal's own capability, or does r139 alone apply? And for other capabilities r45 drafts?
   - (a) r139 replaces r92 for the proposal's own capability: change r92 to "... for each capability the change list names that no capability-proposal of the initiative is redrafted for, ...".
   - (b) both apply: no change.
5. r79/r93 start `integrate` for an initiative; r138 for a capability-proposal. Confirm r138's round is the one r137 starts and no other (yes: no change).

Current text of r92: "**When** a round of the kind `integrate` that `work run` started ends with a change list, `work run` shall write a `drafted` capability-proposal for each capability the change list names, with the requirement ids and terms it adds, changes and removes on that capability."
r80/r114/r71 current: "**When** a round of the kind `apply` that `work run` started for a capability-proposal ends, `work run` shall transition the proposal to `approved`." / "... shall write the proposal's `adds`, `changes` and `removes` from the change list the round applied." / "... shall start a round of the kind `formulate` for the proposal."

Cut sentences: 0.
