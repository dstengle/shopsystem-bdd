/tmp/work-run-i61-u3u9ha_7/i61-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec-integration.md
/tmp/work-run-i61-u3u9ha_7/i61-1-integrate/.shop/scratch/1-integrate/drafts/round-1/supervision.md

## Change list

| change | capability | id | line | source |
|---|---|---|---|---|
| added | spec-integration | r58 | **When** a round of the kind `apply` gives the answers its drafts do not hold, `initiative-round` shall leave out each answer that a later answer of the same proposal replaces. | q40 Line 1: "**When** a round of the kind `apply` gives the answers its drafts do not hold, `initiative-round` shall leave out each answer that a later answer of the same proposal replaces." |
| added | spec-integration | r59 | **When** a round of the kind `gate` is started for a glossary-proposal, `initiative-round` shall ask only about the terms the glossary-proposal adds, changes and removes. | q40 Line 4: "**When** a round of the kind `gate` is started for a glossary-proposal, `initiative-round` shall ask only about the terms the glossary-proposal adds, changes and removes." |
| added | supervision | r212 | **If** a round of the kind `integrate` ends with a change list that adds, changes and removes nothing for a capability-proposal, **then** `work run` shall keep the proposal's status and its requirement ids and start no round of the kind `gate` for it. | q40 Line 2: "**If** a round of the kind `integrate` ends with a change list that adds, changes and removes nothing for a capability-proposal, **then** `work run` shall keep the proposal's status and its requirement ids and start no round of the kind `gate` for it." |
| added | supervision | r213 | **If** a round of the kind `integrate` ends with a change list that names the glossary and adds, changes and removes no term, **then** `work run` shall write no glossary-proposal. | q40 Line 3: "**If** a round of the kind `integrate` ends with a change list that names the glossary and adds, changes and removes no term, **then** `work run` shall write no glossary-proposal." |

Changed: none. Removed: none. Glossary terms: none. Decisions: none.

Placement: r58 after r46 and r59 after r55 (spec-integration); r212 after r187 and r213 after r171 (supervision).

## Questions

1. spec-integration r46 vs r58: r46 gives *each* answer the applied drafts do not hold; r58 leaves out the replaced ones. Should r46 be narrowed? Yes: change r46 to "**When** a round of the kind `apply` ends, `initiative-round` shall give in its result each answer of the capability-proposal that the drafts it applied do not hold and that no later answer of the same proposal replaces." (r58 then retired as merged), or no: keep both, with r58 read as an exception to r46.
2. supervision r171 vs r213: r171 writes a `drafted` glossary-proposal whenever the change list names the glossary; r213 writes none when it names the glossary with no term. Yes, narrow r171: "**When** a round of the kind `integrate` that `work run` started ends with a change list that names the glossary and adds, changes or removes a term, `work run` shall write a `drafted` glossary-proposal with the terms the change list adds, changes and removes in the glossary." No: keep r171 as it is, with r213 as an exception to it.
3. supervision r159 / r142 / r68 vs r212: r159 writes a `drafted` capability-proposal for each capability the change list names, r142 sets a re-drafted proposal `drafted`, and r68 starts a gate for every `drafted` proposal; r212 keeps the status and starts no gate when the change list adds, changes and removes nothing for it. Yes, narrow r159: "... `work run` shall write a `drafted` capability-proposal for each capability for which the change list adds, changes or removes a line, with the requirement ids it adds, changes and removes on that capability." and r142: "**When** a round of the kind `integrate` drafts a capability-proposal anew from its answers with a change list that adds, changes or removes a line for it, `work run` shall set the capability-proposal `drafted`, ...". No: keep them, with r212 as an exception.
4. supervision r212 has two responses (keep status and ids; start no gate) under one "shall", against the one-response rule of docs/capability-format.md. Split it? Yes: r212 "... **then** `work run` shall keep the proposal's status and its requirement ids." and r214 "**If** a round of the kind `integrate` ends with a change list that adds, changes and removes nothing for a capability-proposal, **then** `work run` shall start no round of the kind `gate` for it." No: keep it as one line, as drafted.
5. supervision r164/r168 vs spec-integration r59: r164 has `work run` ask the gate round for questions only on the glossary-proposal's terms; r59 has `initiative-round` itself ask only about them. Not a contradiction, but r59 may duplicate r164 from the round's side. Keep both (as drafted), or drop r59 as given by r164.

## Cut sentences

- "A redraft from replaced answers undoes an applied proposal" (the request's title: rationale, no behaviour).
