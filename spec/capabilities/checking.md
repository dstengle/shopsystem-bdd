---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/checking
title: Checking
narrator: the person
group: service
area: specification
specifies: service specification: check, consult, renew, inventory, translate
language: codified-2
retired: [g4, r4, g5, r5, g6, r6, g7, r7, g8, r8, g9, r9, g10, r10, g11, r11, g12, r12, g13, r13, g14, r14, g15, r15, g16, r16, g17, r17, g25, r25, g31, r31, g34, r34, g37, r37, g40, r40, g42, r42, g43, r43, g45, r45, g56, r56]
unbuilt: []
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

### [g32] the check refuses a term with no part of speech
- [r32] While a term has no part of speech, if the person validates this specification, then the specification service
  shall fail the check and name the term.

### [g33] the check reads a frame with a preposition
- [r33] While a frame of a term has a preposition, when the person validates this specification, the specification
  service shall complete the request.

### [g35] `model rules --write` writes the rule catalogue
- [r35] When the person renews the rule catalogue, the specification service shall keep a rule catalogue and complete
  the request.

### [g36] `model rules --check` refuses a catalogue that lacks a catalogue entry
- [r36] While a rule has a catalogue entry that a rule catalogue does not hold, if the person renews the rule catalogue
  with the audit, then the specification service shall fail the check, name the rule catalogue and change no file.

### [g38] the check passes a verb with two frames
- [r38] While a term has more than one frame, when the person validates this specification, the specification service
  shall complete the request.

### [g39] the check passes a verb with two senses told apart by kinds
- [r39] While a term has more than one sense, when the person validates this specification, the specification service
  shall complete the request.

### [g41] `model lexicon` shows the terms of the imported packs
- [r41] While this bounded context imports a pack, when the person looks up the pack, the language service shall return
  every term of the pack and complete the request.

### [g44] the check passes a term marked Redefines:
- [r44] While a term redefines a pack, when the person validates this specification, the specification service shall
  complete the request.

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

### [g52] A violation of a rule fails the check under the rule's code
- [r52] While a capability violates a rule whose severity is `error`, if the person validates this specification, then the specification service shall fail the check and name the rule.

### [g53] A warning is named and the check passes
- [r53] While a capability violates a rule whose severity is `warning` and nothing violates a rule whose severity is `error`, when the person validates this specification, the specification service shall name the rule and complete the request.

### [g54] A requirement that uses a rule the rule catalogue does not define fails the check
- [r54] While a requirement uses a rule that has no catalogue entry, if the person validates this specification, then the specification service shall fail the check and name the rule.

### [g55] A catalogue entry with no purpose fails the check
- [r55] While a catalogue entry has no purpose, if the person validates this specification, then the specification service shall fail the check and name the catalogue entry.

### [g57] A catalogue entry that names an undelivered item fails the check
- [r57] While a catalogue entry mentions an item whose status is not `delivered`, if the person validates this specification, then the specification service shall fail the check and name the catalogue entry and the item.

### [g58] A catalogue entry that names neither an item nor a release fails the check
- [r58] While a catalogue entry mentions no item and the catalogue entry mentions no release, if the person validates this specification, then the specification service shall fail the check and name the catalogue entry.

### [g59] `spec catalogue entry` writes a catalogue entry's purpose
- [r59] When the person describes a catalogue entry with a purpose, the specification service shall keep a catalogue entry that has the purpose and complete the request.

### [g60] `spec catalogue entry` writes the item a catalogue entry came by
- [r60] When the person describes a catalogue entry with an item, the specification service shall keep a catalogue entry that mentions the item and complete the request.

### [g61] `spec catalogue entry` refuses an entry of no rule and no construct
- [r61] If the person describes a catalogue entry in the rule catalogue that no rule has, then the specification service shall refuse the request and name the catalogue entry.

### [g62] `spec catalogue entry` refuses a construct catalogue entry of no construct
- [r62] If the person describes a catalogue entry in the construct catalogue that no construct has, then the specification service shall refuse the request and name the catalogue entry.

## Dropped
- design-model-check#r2@0.29: retired with checking#r4 by b370.
- design-model-check#r3@0.29: retired with checking#r4 by b370.
- spec-integration#r16@0.29: retired with checking#r4 by b370.
- design-model-check#r4@0.29: retired with checking#r5 by b370.
- design-model-check#r5@0.29: retired with checking#r6 by b370.
- design-model-check#r8@0.29: retired with checking#r10 by b370.
- design-model-check#r107@0.29: retired with checking#r11 by b370.
- design-model-check#r120@0.29: retired with checking#r12 by b370.
- design-model-check#r116@0.29: retired with checking#r13 by b370.
- design-model-check#r52@0.29: retired with checking#r14 by b370.
- design-model-check#r53@0.29: retired with checking#r15 by b370.
- design-model-check#r54@0.29: retired with checking#r16 by b370.
- design-model-check#r103@0.29: retired with checking#r17 by b370.
- design-model-check#r104@0.29: retired with checking#r17 by b370.
- design-model-check#r11@0.29: retired with checking#r25 by b370.
