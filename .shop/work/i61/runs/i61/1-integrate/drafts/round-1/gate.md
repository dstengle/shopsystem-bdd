# Gate, integrate round 1 (i61, request q40)

## Behaviour lines added

### spec-integration
- [r58] **When** a round of the kind `apply` gives the answers its drafts do not hold, `initiative-round` shall leave out each answer that a later answer of the same proposal replaces.
- [r59] **When** a round of the kind `gate` is started for a glossary-proposal, `initiative-round` shall ask only about the terms the glossary-proposal adds, changes and removes.

### supervision
- [r212] **If** a round of the kind `integrate` ends with a change list that adds, changes and removes nothing for a capability-proposal, **then** `work run` shall keep the proposal's status and its requirement ids and start no round of the kind `gate` for it.
- [r213] **If** a round of the kind `integrate` ends with a change list that names the glossary and adds, changes and removes no term, **then** `work run` shall write no glossary-proposal.

Changed: none. Removed: none. Glossary entries: none. Decisions: none.

## Questions
1. spec-integration r46 vs r58: r46 gives each answer the applied drafts do not hold; r58 leaves out the replaced ones. (a) Narrow r46 to "...each answer of the capability-proposal that the drafts it applied do not hold and that no later answer of the same proposal replaces." (r58 then merged), or (b) keep both, r58 an exception to r46.
2. supervision r171 vs r213: r171 writes a glossary-proposal whenever the change list names the glossary. (a) Narrow r171 to "...names the glossary and adds, changes or removes a term...", or (b) keep r171, r213 an exception.
3. supervision r159 / r142 / r68 vs r212: (a) narrow r159 to a capability for which the change list adds, changes or removes a line, and r142 likewise, or (b) keep them, r212 an exception.
4. supervision r212 has two responses under one "shall". (a) Split: r212 "...shall keep the proposal's status and its requirement ids." and r214 "...shall start no round of the kind `gate` for it.", or (b) keep as one line.
5. supervision r164/r168 vs spec-integration r59: keep both (round's side and `work run`'s side), or drop r59 as given by r164.
