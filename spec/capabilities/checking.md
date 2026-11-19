---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/checking
title: Checking
narrator: the person
group: service
area: specification
specifies: service specification: check, consult, renew, inventory, translate
language: codified-2
retired: []
unbuilt: [r48, r49, r50, r51]
---

# Checking

## Purpose
This specification checked as a whole: its rules, the catalogue of the rules, the file forms it keeps and the facts the
checks read.

## Behaviour

### [g1] `model rules` prints every rule
Restates: design-model-check#r65@0.29.
- [r1] When the person consults the rule catalogue, the specification service shall return every rule and complete the
  request.

### [g2] `model forms` lists every file form
- [r2] When the person inventories this specification, the specification service shall return every file form and
  complete the request.

### [g3] the check exits successfully when nothing violates a rule
Restates: design-model-check#r1@0.29.
- [r3] While nothing violates a rule, when the person validates this specification, the specification service shall
  return `0 violations` and complete the request.

### [g4] the check prints a violation under its rule's code
Restates: design-model-check#r2@0.29, design-model-check#r3@0.29, spec-integration#r16@0.29.
- [r4] While a capability violates `v15a`, if the person validates this specification, then the specification service
  shall fail the check and name `v15a`.

### [g5] Two requirements with one id
Restates: design-model-check#r4@0.29.
- [r5] While a capability violates `v15b`, if the person validates this specification, then the specification service
  shall fail the check and name `v15b`.

### [g6] A retired id used again
Restates: design-model-check#r5@0.29.
- [r6] While a capability violates `v15c`, if the person validates this specification, then the specification service
  shall fail the check and name `v15c`.

### [g7] A group with more than one statement
- [r7] While a requirement group violates `v15l`, if the person validates this specification, then the specification
  service shall fail the check and name `v15l`.

### [g8] Two groups of a capability that share their features, condition and trigger
- [r8] While a requirement group violates `v15n`, if the person validates this specification, then the specification
  service shall fail the check and name `v15n`.

### [g9] A given line that is not example data
- [r9] While a requirement group violates `v15m`, if the person validates this specification, then the specification
  service shall fail the check and name `v15m`.

### [g10] A requirement with no scenario
Restates: design-model-check#r8@0.29.
- [r10] While a requirement group violates `v_s3`, if the person validates this specification, then the specification
  service shall fail the check and name `v_s3`.

### [g11] A scenario that names more than one requirement
Restates: design-model-check#r107@0.29.
- [r11] While a scenario violates `v_s2`, if the person validates this specification, then the specification service
  shall fail the check and name `v_s2`.

### [g12] A request with no origin
Restates: design-model-check#r120@0.29.
- [r12] While a request violates `v17`, if the person validates this specification, then the specification service shall
  fail the check and name `v17`.

### [g13] A delivered request resolved by no requirement of the spec
Restates: design-model-check#r116@0.29.
- [r13] While a request violates `v3`, if the person validates this specification, then the specification service shall
  fail the check and name `v3`.

### [g14] A requirement that uses an avoided word
Restates: design-model-check#r52@0.29.
- [r14] While a requirement violates `v_t1`, if the person validates this specification, then the specification service
  shall fail the check and name `v_t1`.

### [g15] Two glossary entries with one term
Restates: design-model-check#r53@0.29.
- [r15] While a term violates `v_t2`, if the person validates this specification, then the specification service shall
  fail the check and name `v_t2`.

### [g16] An avoided word that is a term
Restates: design-model-check#r54@0.29.
- [r16] While a term violates `v_t3`, if the person validates this specification, then the specification service shall
  fail the check and name `v_t3`.

### [g17] A requirement that does not parse
Restates: design-model-check#r103@0.29, design-model-check#r104@0.29.
- [r17] While a requirement violates `v_p1`, if the person validates this specification, then the specification service
  shall fail the check and name `v_p1`.

### [g18] A request not of the form `work request` writes
Restates: design-model-check#r112@0.29.
- [r18] While a request does not conform to the request form, if the person validates this specification, then the
  specification service shall fail the check and name the request.

### [g19] A scenario that names a requirement its capability does not have
Restates: design-model-check#r9@0.29.
- [r19] While a scenario refers to a requirement id that the capability of the scenario does not hold, if the person
  validates this specification, then the specification service shall fail the check and name the scenario.

### [g20] A capability with no capability id
Restates: design-model-check#r25@0.29.
- [r20] While a capability does not conform to the capability id form, if the person validates this specification, then
  the specification service shall fail the check and name the capability.

### [g21] A capability with no Behaviour section
Restates: design-model-check#r25@0.29.
- [r21] While a capability has no section whose heading is `Behaviour`, if the person validates this specification, then
  the specification service shall fail the check and name the capability.

### [g22] A feature file of no capability
Restates: design-model-check#r26@0.29.
- [r22] While a feature does not conform to the feature form, if the person validates this specification, then the
  specification service shall fail the check and name the feature.

### [g23] A glossary bullet in no form of a term entry
Restates: design-model-check#r48@0.29, design-model-check#r49@0.29.
- [r23] While a term does not conform to the entry form, if the person validates this specification, then the
  specification service shall fail the check and name the term.

### [g24] A repository not on the final layout
Restates: design-model-check#r61@0.29.
- [r24] While this bounded context does not conform to the final layout, if the person validates this specification,
  then the specification service shall fail the check and name `scripts/migrate`.

### [g25] A warning leaves the exit as it is
Restates: design-model-check#r11@0.29.
- [r25] While an observation violates `w_uncited_obs`, when the person validates this specification, the specification
  service shall return `w_uncited_obs` and complete the request.

### [g26] A context with no job has no unserved capability
Restates: design-model-check#r111@0.29.
- [r26] While this bounded context has no job, when the person validates this specification, the specification service
  shall return no capability that violates `w_unserved_cap`.

### [g27] the check tries again under an interpreter that has clingo
Restates: design-model-check#r55@0.29.
- [r27] While this interpreter does not import `clingo` and another interpreter imports `clingo`, when the person
  validates this specification, the specification service shall return `0 violations`.

### [g28] No interpreter has clingo
Restates: design-model-check#r12@0.29.
- [r28] While no interpreter imports `clingo`, if the person validates this specification, then the specification
  service shall fail the check and name this interpreter.

### [g29] `model facts` prints the facts
Restates: design-model-check#r13@0.29.
- [r29] When the person translates this specification, the specification service shall return every fact of this bounded
  context.

### [g30] the check refuses a verb with no frame
- [r30] While a verb has no frame, if the person validates this specification, then the specification service shall fail
  the check and name the verb.

### [g31] the check refuses a condition that relates two kinds
- [r31] While a term violates `v_t12`, if the person validates this specification, then the specification service shall
  fail the check and name the term.

### [g32] the check refuses a term with no part of speech
- [r32] While a term has no part of speech, if the person validates this specification, then the specification service
  shall fail the check and name the term.

### [g33] the check reads a frame with a preposition
- [r33] While a frame of a term has a preposition, when the person validates this specification, the specification
  service shall complete the request.

### [g34] the check refuses a frame that does not read
- [r34] While a term violates `v_t13`, if the person validates this specification, then the specification service shall
  fail the check and name the term.

### [g35] `model rules --write` writes the rule catalogue
- [r35] When the person renews the rule catalogue, the specification service shall keep a rule catalogue and complete
  the request.

### [g36] `model rules --check` refuses a catalogue that lacks a catalogue entry
- [r36] While a rule has a catalogue entry that a rule catalogue does not hold, if the person renews the rule catalogue
  with the audit, then the specification service shall fail the check, name the rule catalogue and change no file.

### [g37] the check refuses a verb with no aspect
- [r37] While a term violates `v_t14`, if the person validates this specification, then the specification service shall
  fail the check and name the term.

### [g38] the check passes a verb with two frames
- [r38] While a term has more than one frame, when the person validates this specification, the specification service
  shall complete the request.

### [g39] the check passes a verb with two senses told apart by kinds
- [r39] While a term has more than one sense, when the person validates this specification, the specification service
  shall complete the request.

### [g40] the check refuses two senses that overlap
- [r40] While a term violates `v_t15`, if the person validates this specification, then the specification service shall
  fail the check and name the term.

### [g41] `model lexicon` shows the terms of the imported packs
- [r41] While this bounded context imports a pack, when the person looks up the pack, the language service shall return
  every term of the pack and complete the request.

### [g42] the check refuses an import of no pack
- [r42] While this bounded context imports a pack that violates `v_t17`, if the person validates this specification,
  then the specification service shall fail the check and name the pack.

### [g43] the check refuses a pack's term redefined without Redefines:
- [r43] While a term violates `v_t16`, if the person validates this specification, then the specification service shall
  fail the check and name the term.

### [g44] the check passes a term marked Redefines:
- [r44] While a term redefines a pack, when the person validates this specification, the specification service shall
  complete the request.

### [g45] the check warns of example data in a line
- [r45] While a requirement violates `w_example`, when the person validates this specification, the specification
  service shall return the requirement.

### [g46] the check refuses a capability in the old language, naming `migrate upgrade`
- [r46] If the person validates this specification with a capability whose language is `codified-1`, then the
  specification service shall refuse the request and name the capability.

### [g47] `model forms --check` refuses a file form written by hand
- [r47] While the writer of a file form is `hand`, when the person inventories this specification with the audit, the
  specification service shall fail the check and name the file form.

### [g48] Each operation of an adapter contract is given the requirements that govern it
- [r48] While a requirement governs an operation that an adapter contract holds, when the person annotates the adapter contract, the specification service shall keep an adapter contract that holds an operation that holds the requirement and complete the request.

### [g49] An operation missing a requirement that governs it fails the check
- [r49] While a requirement governs an operation that an adapter contract holds and the operation does not hold the requirement, if the person validates this specification, then the specification service shall fail the check and name the operation and the requirement.

### [g50] An operation holding a requirement that no longer governs it fails the check
- [r50] While an adapter contract holds an operation and the operation holds a requirement and the requirement does not govern the operation, if the person validates this specification, then the specification service shall fail the check and name the operation and the requirement.

### [g51] A stale adapter contract fails the audit
- [r51] While a requirement governs an operation that an adapter contract holds and the operation does not hold the requirement, if the person annotates the adapter contract with the audit, then the specification service shall fail the check, name the adapter contract and change no file.

