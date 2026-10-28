# w219 research notes

Tools: `tools refs` ran on `entries`, `write_proposals`, `rewrite_lists` (refs misses methods and the imports in supervise_rounds.py). `tools tests-of` and `untested` unavailable: no coverage map (`tools map` not run). Test counts below are `by search`.

## 1. Why each scenario is red today

Command (run): `python3 -m pytest -q --work-item w219`. Result: 2 failed, 180 passed, 1 skipped.

- r54, "a round of the kind integrate that drafts a change to the glossary ..." (features/spec-integration.feature:39): StepDefinitionNotFoundError at its first Given, "spec/index.md's glossary has the terms order and basket" (line 41). pytest-bdd stops there. By search, also undefined: "an approved note asks that the customer sees the refund of a cancelled order" (only the "returned order" step exists, tests/scenarios/spec_integration_steps.py:52), "that note adds the term refund, changes the term order and removes the term basket", "the round drafts a line under the capability refunds ...", "the round drafts a change to the glossary", "the change list's entry for the glossary gives ...", "the change list's entry for refunds gives none of ...".
  Missing in code: no stand-in writer result carries a glossary entry (spec_integration_steps.py:60 and :97 build capability entries only; entry() in supervision_integrate_steps.py:32). The code reads every entry as a capability: supervise_change.py:entries (16), unknown (41), write_proposals (91); supervise_rounds.py:136-148 would refuse a `glossary` entry as naming no known capability. The writer contract (agents/initiative-round.md:28, supervise_brief.py:11-13) says "one entry for each capability".
- r55, "while the person has not approved the terms of a glossary-proposal ..." (features/spec-integration.feature:51): StepDefinitionNotFoundError at its first Given, "spec/index.md's glossary has the term order and no term refund" (line 53). By search, also undefined: "an initiative with a glossary-proposal that adds the term refund and changes the term order", "the person has not approved the terms of that glossary-proposal", "a capability-proposal of that initiative the person has approved", "work run starts a round of the kind apply on that capability-proposal" (only "... with those drafts" is defined, spec_integration_apply_steps.py:45), "the round applies the capability-proposal's drafts", "spec/index.md's glossary has no term refund", "... has the term order as it was before the round".
  Missing in code: no glossary-proposal kind anywhere in scripts/ (grep). Apply lists come from entries only (supervise_rounds.py:153-165). Nothing keeps a term out of spec/index.md; that is left to the agent (agents/initiative-round.md:34).

## 2. Old assumptions

Every change-list entry names a capability. Terms appear only inside a capability's lists.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_change.py:entries | reads each entry as a capability; `capability` required | a `glossary` entry must carry terms, not be a capability | tests/scripts/test_supervise_change.py (by search); supervision scenarios (by search) | refs (name collisions), grep |
| scripts/supervise_change.py:unknown | a name is known only with spec/capabilities/<name>.md or a kept draft | `glossary` is known without a capability file | none (no glossary case) | grep |
| scripts/supervise_change.py:write_proposals | one capability-proposal file per entry name | a glossary entry must not become glossary.md | tests/scripts/test_supervise_change.py:16,34,52 (by search) | grep |
| scripts/supervise_change.py:rewrite_lists | sets a proposal's lists from entries whose capability is its `argues` | a glossary entry must not match any proposal | none (by search) | refs: supervise_rounds.py:165 via method |
| scripts/supervise_rounds.py:run_round (136-148) | integrate: refuses when every entry names an unknown capability | glossary entry counted as unknown; refusal | supervision scenarios on r107 (by search, not run) | grep |
| scripts/supervise_rounds.py:run_round (153-165) | apply: writes the lists from applied entries; refuses unknown names | glossary terms of an apply must go to glossary-proposal, not a list | none (by search) | grep |
| scripts/supervise_rounds.py:raise_before_merge (218-221) | counts entries naming unknown capabilities | glossary-only list counts as unknown, no raise | none (by search) | grep |
| scripts/supervise_brief.py:CHANGE_LIST (11-13), used at 81, 136 | "one entry for each capability", ids `term/<term>` allowed | the brief must name the glossary entry and say terms go there only | none assert the text (by search) | grep |
| agents/initiative-round.md:28, 35 | writer contract: one entry per capability | same as the brief | not executed by tests | grep |
| tests/scenarios/supervision_integrate_steps.py:32-38 (entry) | folds `and the term "X"` into a capability's adds as term/X | r54: terms in no capability entry | steps at :140-150 (by search) | grep "and the term" |
| tests/scenarios/supervision_proposal_steps.py:99-106, 145 | term ids inside a capability proposal's adds | terms of a glossary-proposal, not a capability's adds | by search | grep "term/" |

## 3. Tests the requirements make impossible to keep

Found by search (tests-of unavailable). Not run: green status today unverified.

- tests/scenarios/supervision_integrate_steps.py `proposals_written` (:140-153), its `expected` at :150: asserts thing's adds are `thing#r4, term/ledger`. Requirement spec-integration r54. Mechanism: write_proposals puts the term in the capability's lists. Feature line features/supervision.feature:1479 and 1482 carry the same expectation. Conflict: r54 says "in no entry for a capability". Two readings: (a) move the term to a glossary entry and reword this scenario (supervision owner); (b) keep it in the capability entry, which contradicts r54. I have not chosen.
- features/supervision.feature:1700-1704: a gate brief for p1 asks about the term "ledger" listed under its adds. Brief lines (supervise_brief.py:76-77) list adds per proposal. Same conflict as above.
- tests/scenarios/supervision_proposal_steps.py:99-106, 145: term in adds, same mechanism.
- tests/scripts/test_supervise_change.py: read at its three call sites (:16, :34, :52): capability names only; found sound for r54.

## 4. The file set

Production:
- scripts/supervise_change.py: entries and unknown take a glossary entry, write_proposals and rewrite_lists skip it. Found by grep, read in full.
- scripts/supervise_rounds.py: integrate and apply and raise_before_merge skip the glossary entry; apply holds r55. Found by grep, read 100-250.
- scripts/supervise_brief.py: CHANGE_LIST names the glossary entry and terms in it. Found by grep.
- agents/initiative-round.md: writer's glossary entry form and the gate's glossary-proposal. Found by grep.
- new module for glossary-proposal (one concern; CLAUDE.md: new concern, new module and row in the module map). Found by grep: none exists.
- agents/capability-writer.md: the writer's change-list form. Not read; check whether it says one entry per capability.

Tests:
- tests/scenarios/spec_integration_steps.py: steps for the r54 scenario.
- tests/scenarios/spec_integration_apply_steps.py: steps for the r55 scenario.
- tests/scenarios/supervision_integrate_steps.py: entry() and :140-150 (conflicting with r54).
- tests/scenarios/supervision_proposal_steps.py: term lines (conflicting with r54).
- features/supervision.feature: :1479, :1482, :1700-1704 (conflicting with r54; the owner's call).

Modules on the path, with lines and room under 300 (wc -l):
- scripts/supervise_rounds.py 265 lines, room 35 (edited; tight)
- scripts/supervise_change.py 126 lines, room 174 (edited)
- scripts/supervise_brief.py 212 lines, room 88 (edited)
- scripts/supervise_outputs.py 103 lines, room 197 (read; term ids skipped at :88; not edited)
- scripts/supervise_drafts.py 32 lines, room 268 (read; drafts glob; not edited)
- tests/scenarios/spec_integration_steps.py 160 lines, room 140 (edited)
- tests/scenarios/spec_integration_apply_steps.py 78 lines, room 222 (edited)
- tests/scenarios/supervision_integrate_steps.py 201 lines, room 99 (edited)
- workqueue*.py, the glossary-proposal's status path: not measured.
