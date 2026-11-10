---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-integration
title: Spec integration
narrator: the person at the gate
group: guarantees
rests_on: [design-decision/one-spec-per-context, design-decision/gate-on-behaviour-lines, design-decision/spec-writers-blind-to-code, design-decision/controller-per-spec-round, design-decision/light-decisions, design-decision/references-are-ids, design-decision/workflow-capabilities-are-guarantees, design-decision/the-ledger-is-tracked, design-decision/the-context-runs-without-a-coordinator, design-decision/the-glossary-is-a-target-of-spec-work]
language: codified-1
retired: [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16]
---

# Spec integration

## Purpose
**Retired in plugin 2.0.0** (design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired): every requirement of this capability is retired, and the file is kept as the record of its ids and of where its 0.29 lines went.

Merges an approved brainstorming note, or a question's answer, into the bounded context's one spec,
and stops at the one human gate: the Behaviour lines. It is `integrating-a-proposal`, run in rounds of
`initiative-round` that `work run` starts (supervision): the `integrate` and `apply` rounds dispatch the
`capability-writer`, and the `gate` round gives the gate as questions in its result, which `work run` writes
on the capability-proposal; no session writes spec itself (design-decision/the-context-runs-without-a-coordinator).
It is not formulation and not planning; it writes nothing a client can run.

## Terms

- **`integrating-a-proposal`** (proper noun): the skill that integrates an approved design note into the spec.
- **design note** (noun): an approved brainstorming note or design spec, the source of a capability-proposal.
- **second spec** (noun): a `spec/` begun in a context that has one.
- **fresh id** (noun): an id one above every id the capability, or `spec/decisions/`, has used or retired, and above every id other initiatives' drafts add on it.
- **decision source** (noun): the `source` of a design-decision: records, initiatives and decisions by id, with the person, a date, a delegation or anything outside the repository in its `by`.
- **recommended reading** (noun): the reading a gate question marks as recommended, with the statements it concerns in full.
- **retire** (verb, action): an id is added to its capability's `retired:` list. Forms: retires, retired. Frame: round retires requirement.
- **apply** (verb, action): a round writes approved drafts into `spec/`. Forms: applies, applied. Frame: round applies file.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| requirement | quotes | design note |  |
| requirement | added by | capability-proposal |  |
| question | on | term |  |
| term | added by | glossary-proposal |  |
| term | changed by | glossary-proposal |  |
| term | removed by | glossary-proposal |  |

## Behaviour

## Implementation, may change
- None: retired in plugin 2.0.0.

## Not yet
- None.

## Dropped
- r13@0.29: a changed statement is removed and its replacement added with a fresh id (design model v5, C18); no id is kept across a change.
- r16@0.29: moved to design-model-check
- r22@0.29: moved to design-model-check
- r44@0.29: moved to supervision
- r45@0.29: moved to supervision
- r46@0.29: moved to supervision
- r54@0.29: moved to supervision
- r55@0.29: moved to supervision
- r1@0.29: retired with spec-integration#r1, #r2 in 2.0.0 (the-old-workflow-retired).
- r2@0.29: retired with spec-integration#r3 in 2.0.0 (the-old-workflow-retired).
- r3@0.29: retired with spec-integration#r4 in 2.0.0 (the-old-workflow-retired).
- r4@0.29: retired with spec-integration#r5 in 2.0.0 (the-old-workflow-retired).
- r6@0.29: retired with spec-integration#r6 in 2.0.0 (the-old-workflow-retired).
- r7@0.29: retired with spec-integration#r7 in 2.0.0 (the-old-workflow-retired).
- r12@0.29: retired with spec-integration#r1 in 2.0.0 (the-old-workflow-retired).
- r14@0.29: retired with spec-integration#r8 in 2.0.0 (the-old-workflow-retired).
- r15@0.29: retired with spec-integration#r6 in 2.0.0 (the-old-workflow-retired).
- r19@0.29: retired with spec-integration#r10 in 2.0.0 (the-old-workflow-retired).
- r20@0.29: retired with spec-integration#r11 in 2.0.0 (the-old-workflow-retired).
- r21@0.29: retired with spec-integration#r11 in 2.0.0 (the-old-workflow-retired).
- r33@0.29: retired with spec-integration#r16 in 2.0.0 (the-old-workflow-retired).
- r35@0.29: retired with spec-integration#r12 in 2.0.0 (the-old-workflow-retired).
- r39@0.29: retired with spec-integration#r13 in 2.0.0 (the-old-workflow-retired).
- r40@0.29: retired with spec-integration#r14 in 2.0.0 (the-old-workflow-retired).
- r43@0.29: retired with spec-integration#r15 in 2.0.0 (the-old-workflow-retired).
- r59@0.29: retired with spec-integration#r9 in 2.0.0 (the-old-workflow-retired).
