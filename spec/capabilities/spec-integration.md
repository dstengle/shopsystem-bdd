---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-integration
title: Spec integration
narrator: the person at the gate
group: guarantees
rests_on: [design-decision/one-spec-per-context, design-decision/gate-on-behaviour-lines, design-decision/spec-writers-blind-to-code, design-decision/controller-per-spec-round, design-decision/light-decisions, design-decision/references-are-ids, design-decision/workflow-capabilities-are-guarantees, design-decision/the-ledger-is-tracked, design-decision/the-context-runs-without-a-coordinator, design-decision/the-glossary-is-a-target-of-spec-work]
language: codified-1
retired: []
---

# Spec integration

## Purpose
Merges an approved brainstorming note, or a question's answer, into the bounded context's one spec,
and stops at the one human gate: the Behaviour lines. It is `integrating-a-proposal`, run in rounds of
`initiative-round` that `work run` starts (supervision): the `integrate` and `apply` rounds dispatch the
`capability-writer`, and the `gate` round gives the gate as questions in its result, which `work run` writes
on the capability-proposal; no session writes spec itself (design-decision/the-context-runs-without-a-coordinator).
It is not formulation and not planning; it writes nothing a client can run.

## Terms

- **`integrating-a-proposal`** (actor): the skill that integrates an approved design note into the spec.
- **design note** (kind): an approved brainstorming note or design spec, the source of a capability-proposal.
- **second spec** (kind): a `spec/` begun in a context that has one.
- **fresh id** (kind): an id one above every id the capability, or `spec/decisions/`, has used or retired, and above every id other initiatives' drafts add on it.
- **decision source** (kind): the `source` of a design-decision: records, initiatives and decisions by id, with the person, a date, a delegation or anything outside the repository in its `by`.
- **recommended reading** (kind): the reading a gate question marks as recommended, with the statements it concerns in full.
- **quotes** (relation requirement → design note): a drafted statement that quotes a sentence of the note.
- **added by** (relation requirement → capability-proposal): a statement a capability-proposal adds.
- **on** (relation question → term): a question about a term a glossary-proposal adds, changes or removes.
- **retire** (event): an id is added to its capability's `retired:` list. Forms: retires, retired.
- **apply** (event): a round writes approved drafts into `spec/`. Forms: applies, applied.

## Behaviour

### [g1] A drafted statement is shown with a fresh id
Restates: r1@0.29, r12@0.29.
- [r1] When `integrating-a-proposal` writes a requirement, `integrating-a-proposal` shall show the requirement.
- [r2] When `integrating-a-proposal` writes a requirement, `integrating-a-proposal` shall give the requirement a fresh id.

### [g2] Every open question is shown
Restates: r1@0.29.
- [r3] When `integrating-a-proposal` ends, `integrating-a-proposal` shall show every question.

### [g3] A statement that quotes no sentence of the note is a question
Restates: r2@0.29.
- [r4] When `integrating-a-proposal` writes a requirement that quotes no design note, `integrating-a-proposal` shall ask a question.

### [g4] Nothing is committed before the person approves
Restates: r3@0.29.
- [r5] While a capability-proposal is not `approved`, `integrating-a-proposal` shall not commit a requirement.

### [g5] An answer shows the statements again
Restates: r4@0.29.
- [r6] When the person gives an answer, `integrating-a-proposal` shall show every requirement.

### [g6] The approved drafts are committed, naming what they add
Restates: r6@0.29, r15@0.29.
- [r7] When the person approves a capability-proposal, `integrating-a-proposal` shall commit the capability-proposal.
- [r8] When the person approves a capability-proposal, `integrating-a-proposal` shall name every requirement added by the capability-proposal.

### [g7] No second spec
Restates: r7@0.29.
- [r9] `integrating-a-proposal` shall not write a second spec.

### [g8] A removed statement's id is retired
Restates: r14@0.29.
- [r10] When `integrating-a-proposal` deletes a requirement, `integrating-a-proposal` shall retire the requirement.

### [g9] A gate on a glossary-proposal asks only about its terms
Restates: r59@0.29.
- [r11] While a glossary-proposal is `drafted`, when `work run` starts a `gate` stage, `initiative-round` shall ask only a question on a term.

### [g10] A glossary change goes through the gate
Restates: r19@0.29.
- [r12] When `integrating-a-proposal` writes a glossary-proposal, `integrating-a-proposal` shall show the glossary-proposal.

### [g11] A decision is shown as one numbered file with its source
Restates: r20@0.29, r21@0.29.
- [r13] When `integrating-a-proposal` writes a design-decision, `integrating-a-proposal` shall show the design-decision.
- [r14] When `integrating-a-proposal` writes a design-decision, `integrating-a-proposal` shall give the design-decision a fresh id.
- [r15] When `integrating-a-proposal` writes a design-decision, `integrating-a-proposal` shall write a decision source.

### [g12] A gate asks one question for each decision, with its recommended reading
Restates: r35@0.29.
- [r16] When `work run` starts a `gate` stage, `initiative-round` shall ask a question.
- [r17] When `work run` starts a `gate` stage, `initiative-round` shall name a recommended reading.

### [g13] An apply round applies exactly the approved drafts
Restates: r39@0.29.
- [r18] When `work run` starts an `apply` stage, `initiative-round` shall apply only a capability-proposal that is `approved`.

### [g14] Every round is noted in the ledger
Restates: r40@0.29.
- [r19] When `initiative-round` ends a round, `initiative-round` shall note the round.

### [g15] A round numbers its statements above every id it is given
Restates: r43@0.29.
- [r20] When `initiative-round` writes a requirement, `initiative-round` shall give the requirement a fresh id.

### [g16] A skill that cannot do what it is asked changes nothing
Restates: r33@0.29.
- [r21] If `integrating-a-proposal` refuses a design note, then `integrating-a-proposal` shall show the reason.
- [r22] If `integrating-a-proposal` refuses a design note, then `integrating-a-proposal` shall change nothing.

## Implementation, may change
- `skills/integrating-a-proposal/`, and `agents/initiative-round.md` with `agents/capability-writer.md` for the rounds
  `work run` starts.
- The commit of approved drafts holds `spec/` alone, with the statements exactly as approved, and its message names
  the approval and its date, any delegation it was given under, and each id and each term added, changed and removed.
- A decision is one file `spec/decisions/<nnnn>-<slug>.md`, `nnnn` one above the highest number there. A gate question
  marks its recommended reading and gives the statements it concerns in full. A round's ledger line names the kind,
  the round, and what it ended with or the answers it applied.

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
