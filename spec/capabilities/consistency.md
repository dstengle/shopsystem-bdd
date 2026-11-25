---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/consistency
title: Consistency
narrator: the person
group: service
area: specification
specifies: service specification: examine; service language: explain
language: codified-2
retired: []
unbuilt: []
---

# Consistency

## Purpose
The requirements examined together: contradictions, what a line adds over the others, and what a requirement also means.

## Behaviour

### [g1] `model explain` prints a requirement
- [r1] When the person explains a requirement, the language service shall return the requirement and complete the
  request.

### [g2] A pair that cannot be unified leaves the clash of two other requirements
- [r2] While two requirements of a capability use a code that the specification service does not unify and a requirement
  of the capability obliges an act that another requirement of the capability forbids, when the person examines this
  specification, the specification service shall return a requirement and return `L1`.

### [g3] `model logic` finds no clash between only and a change of that kind
- [r3] While a requirement of a capability uses `only` and the requirement allows an act that another requirement of the
  capability obliges, when the person examines this specification, the specification service shall complete the request.

### [g4] `model logic` finds the clash of every and a forbidden print
- [r4] While a requirement of a capability uses `every` and the requirement obliges an act and another requirement of
  the capability that has the trigger of the requirement forbids the act, when the person examines this specification,
  the specification service shall return `L1`.

### [g5] `model logic` reads an If line as taking precedence over a When line
- [r5] While a requirement of a capability overrides another requirement of the capability, when the person examines
  this specification, the specification service shall complete the request.

### [g6] `model logic` pairs a universal condition with the lines it bears on
- [r6] While a universal condition forbids an act that a requirement of a capability obliges, when the person examines
  this specification, the specification service shall return the universal condition.

### [g7] `model logic` reports a requirement that other requirements entail
- [r7] While a requirement has a consequence and the requirement adds no consequence, when the person examines this
  specification, the specification service shall return `L8`.

### [g8] `model logic` finds two counts that cannot both hold
- [r8] While a capability holds a count that contradicts a count, when the person examines this specification, the
  specification service shall return `L1`.

### [g9] `model logic` finds a line that forbids what another permits
- [r9] While a requirement of a capability forbids an act that another requirement of the capability permits, when the
  person examines this specification, the specification service shall return `L7`.

### [g10] `model logic` checks a capability in the new language
- [r10] While the language of a capability is `codified-2`, when the person examines this specification, the
  specification service shall complete the request.

### [g11] `model explain` prints what a refusal entails and where it comes from
- [r11] When the person explains a requirement that uses a refusal, the language service shall return a universal
  condition and a term.

### [g12] `model explain` prints the If requirement that takes precedence
- [r12] When the person explains a requirement that a requirement overrides, the language service shall return a
  requirement that uses a refusal.

### [g13] `model explain` refuses an id that no capability holds
- [r13] If the person explains a requirement id that no capability holds, then the language service shall refuse the
  request and name the requirement id.

### [g14] `model logic` translates every requirement that conforms to the language reference
- [r14] While a requirement of a capability conforms to the language reference, when the person examines this
  specification with the capability, the specification service shall return a translation of the requirement.

### [g15] `model logic` translates only over a relation in a response
- [r15] While a requirement of a capability uses `only` and the requirement uses `holds-relation`, when the person
  examines this specification with the capability, the specification service shall return a translation of the
  requirement.

### [g16] `model logic` translates a count over a relation in a response
- [r16] While a requirement of a capability uses `count` and the requirement uses `holds-relation`, when the person
  examines this specification with the capability, the specification service shall return a translation of the
  requirement.

### [g17] `model logic` names a requirement it has no translation of
- [r17] While a requirement of a capability has no translation, when the person examines this specification with the
  capability, the specification service shall return the requirement and not return `no findings`.

### [g18] `model logic` reads `holds-exactly` as every and only
- [r18] While a requirement of a capability uses `holds-exactly` and the requirement obliges an act and another
  requirement of the capability that has the trigger of the requirement forbids the act, when the person examines this
  specification, the specification service shall return `L1`.

### [g19] `model logic` reads `is-in` as `holds-relation`
- [r19] While a requirement uses `is-in` and the requirement obliges an act and another requirement that forbids the act
  uses `holds-relation`, when the person examines this specification, the specification service shall return `L1`.

### [g20] `model logic` finds the clash of two lines under one comparison
- [r20] While a requirement of a capability uses `value-compare` and the requirement obliges an act and another
  requirement of the capability that has the trigger of the requirement forbids the act, when the person examines this
  specification, the specification service shall return `L1`.

### [g21] `model logic` finds no clash between two lines whose comparisons contradict
- [r21] While a requirement of a capability obliges an act that another requirement of the capability forbids and a
  comparison of the precondition of the requirement contradicts a comparison, when the person examines this
  specification, the specification service shall complete the request.

### [g22] `model logic` finds two contradicting orders
- [r22] While a capability holds an order that contradicts an order, when the person examines this specification, the
  specification service shall return `L1`.

### [g23] `model logic` finds the clash of two lines under a comparison of two senses of one term
- [r23] While a sense of a term has a value order and another sense of the term has the value order and a requirement of
  a capability uses the term and `value-compare` and the requirement obliges an act and another requirement of the
  capability that has the trigger of the requirement forbids the act, when the person examines this specification, the
  specification service shall return `L1`.

### [g24] `model logic` reads `holds-exactly` whose restriction is a relative clause
- [r24] While a requirement of a capability uses `holds-exactly` and `rc-object` and the requirement obliges an act and
  another requirement of the capability that has the trigger of the requirement forbids the act, when the person
  examines this specification, the specification service shall return `L1`.

### [g25] `model logic` reads `nothing` on a response's object
- [r25] While a requirement of a capability uses `nothing` and `rc-subject` and the requirement obliges an act and
  another requirement of the capability that has the trigger of the requirement forbids the act, when the person
  examines this specification, the specification service shall return `L1`.

### [g26] `model logic` translates every over a negated value in a precondition
- [r26] While the precondition of a requirement of a capability uses `every` and `not-condition`, when the person
  examines this specification with the capability, the specification service shall return a translation of the
  requirement.

### [g27] `model logic` finds no clash between an object that holds nothing and a forbidden object that holds a thing
- [r27] While a requirement uses `nothing` and `rc-subject` and the requirement obliges an act and another requirement
  that forbids the act uses `holds-relation`, when the person examines this specification, the specification service
  shall complete the request.

### [g28] `model logic` finds no clash between an object that holds no thing of a kind and a forbidden object that holds one
- [r28] While a requirement uses `no-noun` and `holds-relation` and the requirement obliges an act and another
  requirement that forbids the act uses `holds-relation`, when the person examines this specification, the specification
  service shall complete the request.

### [g29] `model logic` finds the clash of two objects that hold a thing
- [r29] While a requirement uses `holds-relation` and `rc-subject` and the requirement obliges an act and another
  requirement that forbids the act uses `holds-relation`, when the person examines this specification, the specification
  service shall return `L1`.

### [g30] `model logic` reads `holds-exactly` whose restriction reaches a second thing
- [r30] While a requirement of a capability uses `holds-exactly` and `of-relation` and the requirement obliges an act
  and another requirement of the capability that has the trigger of the requirement forbids the act, when the person
  examines this specification, the specification service shall return `L1`.

### [g31] `model logic` finds the clash of a forbidden object whose value is not one code with an obliged object of another value
- [r31] While a requirement uses `not-relative` and a code and the requirement forbids an act and another requirement
  obliges the act and the requirement uses `rc-whose` and the requirement does not use the code, when the person
  examines this specification, the specification service shall return `L1`.

### [g32] `model logic` finds no clash of a forbidden object whose value is not one code with an obliged object of that value
- [r32] While a requirement uses `not-relative` and a code and the requirement forbids an act and another requirement
  obliges the act and the requirement uses `rc-whose` and the code, when the person examines this specification, the
  specification service shall complete the request.

### [g33] holds-exactly in a precondition
- [r33] While the precondition of a requirement of a capability uses `holds-exactly` and `rc-subject`, when the person examines this specification with the capability, the specification service shall return a translation of the requirement.

### [g34] `spec logic` reads a value in use and a code of the same value as one request
- [r34] While a requirement uses `param-of` and the requirement obliges an act and another requirement that forbids the act has the trigger of the requirement, when the person examines this specification, the specification service shall return `L1`.

### [g35] Lines on two terms of one element clash as lines on one thing
- [r35] While a term means an element and a requirement that uses the term obliges an act and another term means the element and another requirement that uses the term forbids the act, when the person examines this specification, the specification service shall return `L1`.

### [g36] spec logic translates a response that makes a request
- [r36] While a requirement of a capability uses `response-request`, when the person examines this specification with the capability, the specification service shall return a translation of the requirement.

### [g37] spec logic follows a response's request to the line that governs its operation
- [r37] While a requirement has a trigger and the requirement uses `response-request` and an operation and another requirement that governs the operation has a consequence and a requirement that has the consequence has the trigger, when the person examines this specification, the specification service shall return `L8` and return every requirement that governs the operation.

### [g38] spec logic follows the consequence of a governing line to the line triggered on it
- [r38] While a requirement governs an operation and the requirement has a consequence and a requirement whose trigger uses the consequence has a consequence and a requirement that uses `response-request` and the operation has a trigger and a requirement that has the consequence has the trigger, when the person examines this specification, the specification service shall return `L8`.

### [g39] spec logic reads a response's request with its parameters
- [r39] While a requirement has a trigger and the requirement obliges an act and the requirement uses `response-request` and a code and another requirement that has the trigger forbids the act and the requirement does not use the code, when the person examines this specification, the specification service shall complete the request.

### [g40] spec logic finds the clash of a response's request with its parameters and a forbidden request of the operation with none
- [r40] While a requirement has a trigger and the requirement obliges an act and the requirement uses `response-request` and a code and another requirement that has the trigger forbids the act and the requirement uses no code, when the person examines this specification, the specification service shall return `L1`.

### [g41] spec logic finds the clash of a counted request of an operation and a forbidden request of it
- [r41] While a requirement has a trigger and the requirement obliges an act and the requirement uses `count` and an operation and another requirement that has the trigger forbids the act, when the person examines this specification, the specification service shall return `L1`.

### [g42] spec logic finds the clash of only over requests of an operation and an obliged request of it outside the restriction
- [r42] While a requirement has a trigger and the requirement obliges an act and another requirement that has the trigger does not allow the act and the requirement uses `only` and an operation, when the person examines this specification, the specification service shall return `L1`.

