---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/reading
title: Reading
narrator: the person
group: service
area: specification
specifies: service language: parse, look up
language: codified-2
retired: []
unbuilt: []
---

# Reading

## Purpose
A line read in grammar 4: parsed to one meaning or refused with why, its logical form given, the caches its parse keeps,
and the terms of a pack looked up.

## Behaviour

### [g1] `model parse` refuses a verb with no object
- [r1] If the person parses a requirement that omits an object of a term, then the language service shall refuse the
  request and name the term.

### [g2] `model parse` refuses a verb with no recipient
- [r2] If the person parses a requirement that omits a recipient of a term, then the language service shall refuse the
  request and name the term.

### [g3] `model parse` parses a negated verb or relation
- [r3] When the person parses a requirement that uses `not-condition`, the language service shall complete the request.

### [g4] `model parse` refuses a verb with a noun of the wrong kind
- [r4] If the person parses a requirement that uses a noun phrase of a term that no frame takes, then the language
  service shall refuse the request and name the term.

### [g5] `model parse` parses a verb between two kinds in a condition
- [r5] When the person parses a requirement whose precondition uses a term whose aspect is `state`, the language service
  shall complete the request.

### [g6] `model parse` refuses a passive with no agent
- [r6] If the person parses a requirement that uses a passive form that has no by-phrase, then the language service
  shall refuse the request and name the passive form.

### [g7] `model parse` parses a trigger with a recipient
- [r7] When the person parses a requirement whose trigger uses a recipient, the language service shall complete the
  request.

### [g8] `model parse` parses a verb whose frame has a preposition
- [r8] When the person parses a requirement that uses a term whose frame has a preposition, the language service shall
  complete the request.

### [g9] `model parse` passes a plural subject whose verb agrees
- [r9] When the person parses a requirement that uses `bare-plural`, the language service shall complete the request.

### [g10] `model parse` refuses a verb that does not agree with its subject
- [r10] If the person parses a requirement that uses a term that does not agree with its subject, then the language
  service shall refuse the request and name the term.

### [g11] `model parse` refuses an action verb in a While clause
- [r11] If the person parses a requirement whose precondition uses a term whose aspect is `action`, then the language
  service shall refuse the request and name the requirement.

### [g12] `model parse` passes a trigger that runs a command with an option
- [r12] When the person parses a requirement that uses `request-params`, the language service shall complete the
  request.

### [g13] `model parse` passes of and its over a relation row or an attribute
- [r13] When the person parses a requirement that uses `of-relation`, the language service shall complete the request.

### [g14] `model parse` passes no before a subject or an object
- [r14] When the person parses a requirement that uses `no-noun`, the language service shall complete the request.

### [g15] `model parse` passes a derived compound noun
- [r15] When the person parses a requirement that uses `compound`, the language service shall complete the request.

### [g16] `model parse` passes only before an object
- [r16] When the person parses a requirement that uses `only`, the language service shall complete the request.

### [g17] `model parse` passes a relative clause on a verb's frame
- [r17] When the person parses a requirement that uses `rc-object`, the language service shall complete the request.

### [g18] `model parse` passes whose over a relation row or an attribute
- [r18] When the person parses a requirement that uses `rc-whose`, the language service shall complete the request.

### [g19] `model parse` refuses a requirement with two meanings
- [r19] If the person parses a requirement that has more than one logical form, then the language service shall refuse
  the request and name the requirement.

### [g20] `model parse --form` prints the one logical form of a requirement that conforms to the language reference
- [r20] When the person parses a requirement that conforms to the language reference with the logical form, the language
  service shall return one logical form of the requirement and complete the request.

### [g21] `model parse` passes this before a kind whose entry has This:
- [r21] When the person parses a requirement that uses `this`, the language service shall complete the request.

### [g22] `model parse` refuses the with no antecedent
- [r22] If the person parses a requirement that uses a definite noun phrase that has no antecedent, then the language
  service shall refuse the request and name the definite noun phrase.

### [g23] `model parse` refuses a negated indefinite in a While clause
- [r23] If the person parses a requirement whose precondition uses a negated indefinite, then the language service shall
  refuse the request and name the negated indefinite.

### [g24] `model parse` refuses a requirement with no trigger and neither always nor never
- [r24] While a requirement has no trigger and the requirement does not use `always-never`, if the person parses the
  requirement, then the language service shall refuse the request and name the requirement.

### [g25] `model parse` refuses a fragment with the terms that may follow
- [r25] If the person parses a fragment, then the language service shall refuse the request, name the fragment and
  return a term.

### [g26] `model parse` reads a count
- [r26] When the person parses a requirement that uses `count`, the language service shall complete the request.

### [g27] `model parse` reads a comparison of moments
- [r27] When the person parses a requirement that uses `moment-compare`, the language service shall complete the
  request.

### [g28] `model parse` reads the clock as a trigger
- [r28] When the person parses a requirement that uses a clock trigger, the language service shall complete the request.

### [g29] `model parse` reads the perfect as history
- [r29] When the person parses a requirement whose precondition uses a perfect, the language service shall complete the
  request.

### [g30] `model parse` refuses a duration with no unit
- [r30] If the person parses a requirement that uses a number that has no unit, then the language service shall refuse
  the request and name the requirement.

### [g31] `model parse` reads a permission
- [r31] When the person parses a requirement that uses `may`, the language service shall complete the request.

### [g32] `model parse` reads always and never with no trigger
- [r32] When the person parses a requirement that uses `always-never`, the language service shall complete the request.

### [g33] `model parse` refuses a requirement that does not conform to the language reference
- [r33] If the person parses a requirement that does not conform to the language reference, then the language service
  shall refuse the request and name the requirement.

### [g34] `model parse --form` prints the logical form the corpus holds
- [r34] While the corpus holds a logical form of a requirement, when the person parses the requirement with the logical
  form, the language service shall return the logical form.

### [g35] `model parse` reads a requirement from the parse cache that holds its parse
- [r35] While a parse cache holds the parse of a requirement, when the person parses the requirement, the language
  service shall return the parse of the requirement, keep no compiled grammar and complete the request.

### [g36] `model parse` parses a requirement whose parse no parse cache holds and keeps it
- [r36] While a requirement has a parse that no parse cache holds, when the person parses the requirement, the language
  service shall keep a parse cache and complete the request.

### [g37] `model parse` reuses the compiled grammar of unchanged sources
- [r37] While a requirement has a parse that no parse cache holds and the compiled grammar of the requirement exists,
  when the person parses the requirement, the language service shall keep no compiled grammar and complete the request.

### [g38] `model parse` refuses a state verb in a trigger
- [r38] If the person parses a requirement whose trigger uses a term whose aspect is `state`, then the language service
  shall refuse the request and name the requirement.

### [g39] `model parse` reads `holds-exactly`
- [r39] When the person parses a requirement that uses `holds-exactly`, the language service shall complete the request.

### [g40] `model parse` reads `nothing` in a precondition
- [r40] When the person parses a requirement whose precondition uses `nothing`, the language service shall complete the
  request.

### [g41] `model parse` reads `is-in`
- [r41] When the person parses a requirement whose precondition uses `is-in`, the language service shall complete the
  request.

### [g42] `model parse` reads one thing's value compared with another's
- [r42] When the person parses a requirement that uses `value-compare`, the language service shall complete the request.

### [g43] `model parse` reads one thing's value said to be the same as another's
- [r43] When the person parses a requirement that uses `value-same`, the language service shall complete the request.

### [g44] `model parse` refuses a comparison of an attribute that has no order
- [r44] While a term has no value order and a requirement uses the term and `value-compare`, if the person parses the
  requirement, then the language service shall refuse the request and name the term.

### [g45] `model parse` reads an order on a collection
- [r45] When the person parses a requirement that uses `order-by`, the language service shall complete the request.

### [g46] `model parse` reads an order on a printed every
- [r46] When the person parses a requirement that uses `order-by-every`, the language service shall complete the
  request.

### [g47] `model parse --form` prints an order as one atom
- [r47] When the person parses a requirement that uses an order with the logical form, the language service shall return
  the order and complete the request.

### [g48] `model parse` refuses an order on an attribute whose values have no order
- [r48] If the person parses a requirement that uses an order on a term that has no value order, then the language
  service shall refuse the request and name the term.

### [g49] `model parse` refuses an order in a precondition
- [r49] If the person parses a requirement whose precondition uses an order, then the language service shall refuse the
  request and name the order.

### [g50] `model parse` refuses an order in a trigger
- [r50] If the person parses a requirement whose trigger uses an order, then the language service shall refuse the
  request and name the order.

### [g51] `model parse` refuses an order in a forbidden act
- [r51] If the person parses a requirement that forbids an act that holds an order, then the language service shall
  refuse the request and name the order.

### [g52] `model parse` reads a comparison of two senses of one term with one value order
- [r52] While a sense of a term has a value order and another sense of the term has the value order and a requirement
  uses the term and `value-compare`, when the person parses the requirement, the language service shall complete the
  request.

### [g53] `model parse` reads two senses of one term with one value order said to be the same
- [r53] While a sense of a term has a value order and another sense of the term has the value order and a requirement
  uses the term and `value-same`, when the person parses the requirement, the language service shall complete the
  request.

### [g54] `model parse` refuses a comparison of two senses of one term with different value orders
- [r54] While a sense of a term has a value order and another sense of the term has a different value order and a
  requirement uses the term and `value-compare`, if the person parses the requirement, then the language service shall
  refuse the request and name the term.

### [g55] `model parse` refuses two senses of one term with different value orders said to be the same
- [r55] While a sense of a term has a value order and another sense of the term has a different value order and a
  requirement uses the term and `value-same`, if the person parses the requirement, then the language service shall
  refuse the request and name the term.

### [g56] `model parse` reads an order on every K that a verb whose frames name its kind takes
- [r56] While a requirement uses `order-by-every` and the requirement uses a verb that has no frame that takes `thing`,
  when the person parses the requirement, the language service shall complete the request.

### [g57] `model parse` reads an order after every K in a collection one way
- [r57] While a requirement uses `order-by-every` and `of-relation`, when the person parses the requirement, the
  language service shall complete the request.

### [g58] `model parse` refuses a state verb in a response as the response's
- [r58] If the person parses a requirement whose response uses a term whose aspect is `state`, then the language service
  shall refuse the request, name the term and the response and not name the trigger.

### [g59] `model parse` reads an order that a closing comma ends before the recipient
- [r59] While a requirement uses `order-by` and a closing comma, when the person parses the requirement, the language
  service shall complete the request.

### [g60] `model parse` reads an order on every K that a closing comma ends before the recipient
- [r60] While a requirement uses `order-by-every` and a closing comma, when the person parses the requirement, the
  language service shall complete the request.

### [g61] `model parse` still reads an order before the recipient with no closing comma
- [r61] While a requirement uses `order-by` and a recipient and the requirement uses no closing comma, when the person
  parses the requirement, the language service shall complete the request.
