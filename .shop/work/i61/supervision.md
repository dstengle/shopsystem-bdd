---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i61-supervision
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i61
status: awaiting-answer
argues: [supervision]
adds: [supervision#r212, supervision#r213]
changes: []
removes: []
date: 2026-10-29
---

# supervision

The drafts of this proposal are in .shop/work/i61/runs/i61/1-integrate/drafts/round-1/.

## Questions
- supervision r213 vs r171. r213 (added): "**If** a round of the kind `integrate` ends with a change list that names the glossary and adds, changes and removes no term, **then** `work run` shall write no glossary-proposal." r171 (in spec): "**When** a round of the kind `integrate` that `work run` started ends with a change list that names the glossary, `work run` shall write a `drafted` glossary-proposal with the terms the change list adds, changes and removes in the glossary." They conflict for a change list naming the glossary with no term. Readings: (a, recommended) narrow r171 to "...names the glossary and adds, changes or removes a term...", so r213 stays a plain rule; (b) keep r171 as is and r213 an exception to it.
- supervision r212 vs r159, r142 and r68. r212 (added): "**If** a round of the kind `integrate` ends with a change list that adds, changes and removes nothing for a capability-proposal, **then** `work run` shall keep the proposal's status and its requirement ids and start no round of the kind `gate` for it." r159 writes a `drafted` capability-proposal for each capability the change list names; r142 sets a re-drafted proposal `drafted`; r68 starts a gate when a proposal is `drafted`. Readings: (a, recommended) narrow r159 to a capability for which the change list adds, changes or removes a line, and r142 likewise, so r68 never meets an empty proposal; (b) keep them and r212 an exception to each.
- supervision r212 has two responses under one "shall" (keeps status and ids; starts no gate). Readings: (a, recommended) split: r212 "...**then** `work run` shall keep the proposal's status and its requirement ids." and a new r214 "**If** ... nothing for a capability-proposal, **then** `work run` shall start no round of the kind `gate` for it."; (b) keep as one line.
