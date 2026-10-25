---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i29-supervision
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i29
status: awaiting-answer
argues: [supervision]
adds: [supervision#r105, supervision#r106, supervision#r107, supervision#r108]
changes: []
removes: []
date: 2026-10-25
---

# supervision

The drafts of this proposal are in .shop/work/i29/runs/i29/1-integrate.

## Questions
- supervision r105, the term 'every raised request'. Line (added): [r105] When `work run` finds an initiative that is not `done`, whose every work-item is `green` or `withdrawn`, whose kept branch review lists nothing to fix now and whose every request kept in this context whose asker is this context and that names the initiative is `delivered`, `work run` shall set the initiative's status to `done`. Readings: (a) keep the wording, as work-queue r23 words it [recommended]; (b) 'every request that a round of the initiative raised'.
- supervision r105, an initiative with no work-item. Line (added): r105 as above. As drafted it also fires for an initiative with none. Readings: (a) add 'that has at least one work-item' [recommended]; (b) as drafted.
- supervision r105 against r106 and the measure/analysis rounds, order. Line (added): r105 as above. An initiative set `done` first may never be measured or analysed (r66 skips `done`). Readings: (a) r105 adds 'and whose measurement and analysis record `work run` has committed' [recommended]; (b) as drafted.
- Commit of the `done` status. Concerns r105 and [r106] (added): When `work run` has written an initiative's measurement and its analysis record, `work run` shall commit them on the initiative branch. Readings: (a) add a line: 'When `work run` sets an initiative's status to `done`, `work run` shall commit the initiative on the initiative branch.' [recommended]; (b) add nothing.
- supervision r107, a capability the round adds. Line (added): [r107] If a change list that `work run` reads names a capability that `spec/capabilities/` does not have, then `work run` shall write no capability-proposal for it and exit with an error, naming the capability. Readings: (a) exempt it: '...neither `spec/capabilities/` nor the round's drafts have...' [recommended]; (b) refuse it too, as drafted.
- supervision r107 and r92, what is written when one capability is missing. Line (added): r107 as above. Readings: (a) only the missing capability gets no proposal, r92 still writes the others, as drafted [recommended]; (b) none: '...shall write no capability-proposal for the change list and exit with an error, naming the capability.'

## Answers
- 2026-10-25: 1: (a), keep the wording as work-queue r23 words it (the coordinator under the person's delegation 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release")
- 2026-10-25: 2: (a), add 'that has at least one work-item' (the coordinator under the person's delegation 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release")
- 2026-10-25: 3: (a), r105 adds 'and whose measurement and analysis record work run has committed' (the coordinator under the person's delegation 2026-10-25: "Do not involve me in fixing all of the bugs. Please get the system into a correctly working state before doing a release")
