---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/delivery
title: Delivery
narrator: the person delivering an initiative
group: guarantees
rests_on: [design-decision/a-script-supervises-delivery, design-decision/gate-on-behaviour-lines, design-decision/formulation-needs-no-second-approval, design-decision/spec-writers-blind-to-code, design-decision/review-of-work-items, design-decision/workflow-capabilities-are-guarantees, design-decision/the-ledger-is-tracked, design-decision/the-context-runs-without-a-coordinator]
language: codified-1
retired: [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11]
---

# Delivery

## Purpose
**Retired in plugin 2.0.0** (design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired): every requirement of this capability is retired, and the file is kept as the record of its ids and of where its 0.29 lines went.

Has `work run` deliver an initiative and shows the person what it ends with. It is `delivering-an-initiative`; it
drafts no work-item but a trial's fix (`work run` drafts the rest, supervision), starts no `claude -p` session and
merges no branch itself, and reads what `work run` ends with, never what its workers write
(design-decision/the-context-runs-without-a-coordinator). A walking skeleton
(design-decision/behaviour-lines-are-ears): it grows from what using it shows.

## Terms

- **`delivering-an-initiative`** (proper noun): the skill that has `work run` deliver an initiative and shows the person what it ends with.
- **disallowed tool** (noun): a tool a worker needs that `work run` does not allow it.
- **note** (verb): a line naming an event is appended to an initiative's ledger with `work note`. Forms: notes, noted. Frame: session notes ledger.

## Behaviour

## Implementation, may change
- None: retired in plugin 2.0.0.

## Not yet
- None.

## Dropped
- r4@0.29: retired with delivery#r1 in 2.0.0 (the-old-workflow-retired).
- r5@0.29: retired with delivery#r2 in 2.0.0 (the-old-workflow-retired).
- r6@0.29: retired with delivery#r3 in 2.0.0 (the-old-workflow-retired).
- r7@0.29: retired with delivery#r4 in 2.0.0 (the-old-workflow-retired).
- r10@0.29: retired with delivery#r5 in 2.0.0 (the-old-workflow-retired).
- r11@0.29: retired with delivery#r6 in 2.0.0 (the-old-workflow-retired).
- r12@0.29: retired with delivery#r6 in 2.0.0 (the-old-workflow-retired).
- r13@0.29: retired with delivery#r9 in 2.0.0 (the-old-workflow-retired).
- r14@0.29: retired with delivery#r10 in 2.0.0 (the-old-workflow-retired).
- r15@0.29: retired with delivery#r11 in 2.0.0 (the-old-workflow-retired).
- r19@0.29: retired with delivery#r6 in 2.0.0 (the-old-workflow-retired).
- r20@0.29: retired with delivery#r6 in 2.0.0 (the-old-workflow-retired).
- r21@0.29: retired with delivery#r7 in 2.0.0 (the-old-workflow-retired).
- r22@0.29: retired with delivery#r8 in 2.0.0 (the-old-workflow-retired).
