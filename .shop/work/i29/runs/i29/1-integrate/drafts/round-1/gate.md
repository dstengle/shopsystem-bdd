# Gate: i29, round 1 (q5)

## supervision (added)
- [r105] **When** `work run` finds an initiative that is not `done`, whose every work-item is `green` or `withdrawn`, whose kept branch review lists nothing to fix now and whose every request kept in this context whose asker is this context and that names the initiative is `delivered`, `work run` shall set the initiative's status to `done`.
- [r106] **When** `work run` has written an initiative's measurement and its analysis record, `work run` shall commit them on the initiative branch.
- [r107] **If** a change list that `work run` reads names a capability that `spec/capabilities/` does not have, **then** `work run` shall write no capability-proposal for it and exit with an error, naming the capability.
- [r108] **When** `work run` starts a round of the kind `gate` or `apply` for a capability-proposal, `work run` shall give the round the path of the kept drafts of the round of the kind `integrate` that wrote the proposal.

Purpose also changed (no line): `work run` commits the initiative's measurement and analysis and sets the initiative `done`.

## requests (added)
- [r22] **If** the delegation given to `work request` is empty, **then** `work request` shall refuse, because the delegation is empty, and change nothing.

No glossary entries. No decisions.

## Questions
1. r105, "every raised request": no glossary term. Drafted as work-queue r23 words it ("every request kept in this context whose asker is this context and that names the initiative"). Recommended: keep. Other: "every request that a round of the initiative raised".
2. r105, no work-item: as drafted it also fires for an initiative with none. Yes (recommended): add "that has at least one work-item". No: as drafted.
3. r105 and r75/r76/r106, order: an initiative set `done` first may never be measured or analysed (r66 skips `done`). Yes: r105 adds "and whose measurement and analysis record `work run` has committed". No: as drafted. 
4. Commit of the `done` status: yes adds "**When** `work run` sets an initiative's status to `done`, `work run` shall commit the initiative on the initiative branch."; no adds nothing.
5. r107, a capability the round adds: exempt it (r107 reads "...neither `spec/capabilities/` nor the round's drafts have...") or refuse it too (as drafted).
6. r107 and r92: A (only the missing capability; r92 still writes the others; as drafted) or B (none: "...shall write no capability-proposal for the change list and exit with an error, naming the capability.").

## Cut sentences
None.
