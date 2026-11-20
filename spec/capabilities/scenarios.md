---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/scenarios
title: Scenarios
narrator: the person
group: service
area: specification
specifies: service scenarios
language: codified-2
retired: []
unbuilt: []
---

# Scenarios

## Purpose
The scenarios generated from the requirements of a capability, each group's, with the counter-examples and boundaries
that let them fail, and their steps audited for a handler.

## Behaviour

### [g1] `features generate --check` names a feature with a scenario that no requirement group of its capability has
- [r1] While the feature of a capability has a scenario that no requirement group has, if the person generates the
  feature of the capability with the audit, then the scenarios service shall fail the check, name the feature and change
  no file.
```given
the capability `shelf` holds:
  ---
  id: capability/ex.com/prod/ctx/shelf
  title: shelf
  narrator: a client
  group: service
  language: codified-2
  rests_on: []
  retired: []
  ---
  # shelf
  ## Purpose
  Something.
  ## Terms
  - **book** (noun): a thing.
  ## Behaviour
  ## Not yet
  ## Dropped
the feature file `features/shelf.feature` holds:
  Feature: Shelf
    Scenario: Edited by hand
      Given a step
```

### [g2] `features vocab --check` names a step with no handler and its feature
- [r2] While a step of a feature has no handler, if the person audits the feature, then the scenarios service shall fail
  the check, name the step, name the feature and change no file.
```given
the capability `shelf` holds:
  ---
  id: capability/ex.com/prod/ctx/shelf
  title: shelf
  narrator: a client
  group: service
  language: codified-2
  rests_on: []
  retired: []
  ---
  # shelf
  ## Purpose
  Something.
  ## Terms
  - **book** (noun): a thing.
  ## Behaviour
  ## Not yet
  ## Dropped
the feature file `features/shelf.feature` holds:
  # generated from spec/capabilities/shelf.md by features generate; do not edit
  Feature: shelf
    Narrator: a client
    @g1 @r1
    Scenario: Lending
      When the person lends a book
```

### [g3] generation writes a scenario of every requirement group of a capability in the language reference
- [r3] While the language of a capability is `codified-2` and every requirement of the capability conforms to the
  language reference and every requirement of the capability uses the `shall` construct, when the person generates the
  feature of the capability, the scenarios service shall keep the scenario of every requirement group of the capability.

### [g4] generation leaves out a step that a universal condition entails
- [r4] While the language of a capability is `codified-2`, when the person generates the feature of the capability, the
  scenarios service shall not keep a step that a universal condition entails.

### [g5] generation writes the feature of a codified service capability
- [r5] While the group of a capability is `service` and the language of the capability is `codified-2`, when the person
  generates the feature of the capability, the scenarios service shall keep the feature of the capability and return the
  feature.
```given
the capability `shelf` holds:
  ---
  id: capability/ex.com/prod/ctx/shelf
  title: shelf
  narrator: a client
  group: service
  language: codified-2
  rests_on: []
  retired: []
  ---
  # shelf
  ## Purpose
  Something.
  ## Terms
  - **book** (noun): a thing.
  ## Behaviour
  ## Not yet
  ## Dropped
```

### [g6] generation writes what a requirement says of a referent after the act that brings it in
- [r6] While an act of a requirement of a capability brings in a referent, when the person generates the feature of the
  capability, the scenarios service shall keep a description of the referent that follows the act and not keep a
  description of the referent that precedes the act.
```given
the capability `shelf` holds:
  ---
  id: capability/ex.com/prod/ctx/shelf
  title: shelf
  narrator: a client
  group: service
  language: codified-2
  rests_on: []
  retired: []
  ---
  # shelf
  ## Purpose
  Something.
  ## Terms
  - **book** (noun): a thing. Kind of: thing.
  - **status** (attribute of book): where a book is. Values (adjective): `shelved`, `lent`.
  - **lend** (verb, action): a client gives a book to a reader. Forms: lends, lent. Frame: client lends book.
  ## Behaviour
  ### [g1] Lending
  - [r1] When the person runs `shelf add`, `shelf` shall write a book whose status is `shelved` and print the book.
  ## Not yet
  ## Dropped
```

### [g7] generation writes only over a relation in a response
- [r7] While a requirement of a capability uses `only` and the requirement uses `holds-relation`, when the person
  generates the feature of the capability, the scenarios service shall keep a scenario that uses `only`.

### [g8] generation writes a count over a relation in a response
- [r8] While a requirement of a capability uses `count` and the requirement uses `holds-relation`, when the person
  generates the feature of the capability, the scenarios service shall keep a scenario that uses `count`.

### [g9] generation writes a counter-example of every
- [r9] While a requirement of a requirement group of a capability uses `every` and the requirement has a restriction,
  when the person generates the feature of the capability, the scenarios service shall keep a scenario of the
  requirement group that has a counter-example.

### [g10] generation writes a counter-example of only and asserts no act that only allows
- [r10] While a requirement of a requirement group of a capability uses `only` and the requirement has a restriction,
  when the person generates the feature of the capability, the scenarios service shall keep a scenario of the
  requirement group that has a counter-example and not keep a step that asserts an act that the requirement allows.

### [g11] generation writes a counter-example of an upper bound
- [r11] While a requirement of a requirement group of a capability has an upper bound, when the person generates the
  feature of the capability, the scenarios service shall keep a scenario of the requirement group that has a
  counter-example.

### [g12] generation writes Givens that satisfy a precondition that uses every
- [r12] While the precondition of a requirement of a requirement group of a capability uses `every`, when the person
  generates the feature of the capability, the scenarios service shall keep a scenario of the requirement group that
  satisfies the precondition.

### [g13] generation gives a count in a precondition at its boundary
- [r13] While the precondition of a requirement of a requirement group of a capability holds a count, when the person
  generates the feature of the capability, the scenarios service shall keep a scenario of the requirement group that has
  the boundary of the count.

### [g14] generation introduces each instance of two Ks
- [r14] While a requirement of a requirement group of a capability uses `two`, when the person generates the feature of
  the capability, the scenarios service shall not keep a step that mentions an instance that no given step introduces.

### [g15] generation writes the member a collection must not hold
- [r15] While a requirement of a capability uses `holds-exactly`, when the person generates the feature of the
  capability, the scenarios service shall keep a scenario whose step uses `not-condition`.

### [g16] generation writes `nothing` in a precondition
- [r16] While the precondition of a requirement of a capability uses `nothing`, when the person generates the feature of
  the capability, the scenarios service shall keep a scenario whose step uses `nothing`.

### [g17] generation writes an order's Then and Givens that can fail it
- [r17] While a requirement of a requirement group of a capability uses an order, when the person generates the feature
  of the capability, the scenarios service shall keep a scenario that has an order counter-example.

### [g18] generation writes the scenario of `order-by` on a term of two senses
- [r18] While a term has two senses and a requirement of a requirement group of a capability uses the term and
  `order-by`, when the person generates the feature of the capability, the scenarios service shall keep a scenario of
  the requirement group that has an order counter-example.

### [g19] generation writes the scenario of `order-by-every` on a term of two senses
- [r19] While a term has two senses and a requirement of a requirement group of a capability uses the term and
  `order-by-every`, when the person generates the feature of the capability, the scenarios service shall keep a scenario
  of the requirement group that has an order counter-example.

### [g20] generation writes the member outside a relative clause's restriction
- [r20] While a requirement of a capability uses `holds-exactly` and `rc-object`, when the person generates the feature
  of the capability, the scenarios service shall keep a scenario whose step uses `not-condition`.

### [g21] generation writes `nothing` on a response's object
- [r21] While a requirement of a capability uses `nothing` and `rc-subject`, when the person generates the feature of
  the capability, the scenarios service shall keep a scenario whose step uses `nothing`.

### [g22] generation writes the scenario of `order-by` on the object of a verb whose frames name its kind
- [r22] While a requirement of a requirement group of a capability uses `order-by` and the requirement uses a verb that
  has no frame that takes `thing`, when the person generates the feature of the capability, the scenarios service shall
  keep a scenario of the requirement group that has an order counter-example.

### [g23] generation writes the Then of a response's object that holds no K
- [r23] While a requirement of a requirement group of a capability uses `no-noun` and `holds-relation` and the
  precondition of the requirement does not use `no-noun`, when the person generates the feature of the capability, the
  scenarios service shall keep a scenario of the requirement group that has a counter-example.

### [g24] generation satisfies every over a negated value in a precondition
- [r24] While the precondition of a requirement of a requirement group of a capability uses `every` and `not-condition`,
  when the person generates the feature of the capability, the scenarios service shall keep a scenario of the
  requirement group that satisfies the precondition.

### [g25] generation writes the scenario of `order-by-every` on the object of a verb whose frames name its kind
- [r25] While a requirement of a requirement group of a capability uses `order-by-every` and the requirement uses a verb
  that has no frame that takes `thing`, when the person generates the feature of the capability, the scenarios service
  shall keep a scenario of the requirement group that has an order counter-example.

### [g26] generation introduces the thing a printed thing holds
- [r26] While a requirement of a requirement group of a capability uses `holds-relation` and `rc-subject`, when the
  person generates the feature of the capability, the scenarios service shall not keep a step that mentions an instance
  that no given step introduces.

### [g27] generation introduces each instance of an order
- [r27] While a requirement of a requirement group of a capability uses `order-by`, when the person generates the
  feature of the capability, the scenarios service shall not keep a step that mentions an instance that no given step
  introduces.

### [g28] generation writes the scenario of `order-by-every` on every K in a collection
- [r28] While a requirement of a requirement group of a capability uses `order-by-every` and `of-relation`, when the
  person generates the feature of the capability, the scenarios service shall keep a scenario of the requirement group
  that has an order counter-example.

### [g29] generation writes a counter-example of a count over a relation in a response
- [r29] While a requirement of a requirement group of a capability uses `count` and `holds-relation` and the requirement
  has an upper bound, when the person generates the feature of the capability, the scenarios service shall keep a
  scenario of the requirement group that has a counter-example.

### [g30] generation writes the member outside a restriction that reaches a second thing
- [r30] While a requirement of a capability uses `holds-exactly` and `of-relation`, when the person generates the
  feature of the capability, the scenarios service shall keep a scenario whose step uses `not-condition`.

### [g31] holds-exactly in a precondition
- [r31] While the precondition of a requirement of a capability uses `holds-exactly`, when the person generates the feature of the capability, the scenarios service shall keep a scenario whose step uses `not-condition`.

### [g32] holds-exactly with a subject relative clause in a precondition
- [r32] While the precondition of a requirement of a capability uses `holds-exactly` and `rc-subject`, when the person generates the feature of the capability, the scenarios service shall keep a scenario whose step uses `not-condition`.

### [g33] generation introduces the thing a response names by its owner
- [r33] While a requirement of a requirement group of a capability uses `of-relation` and the precondition of the requirement does not use `of-relation`, when the person generates the feature of the capability, the scenarios service shall not keep a step that mentions an instance that no given step introduces.

