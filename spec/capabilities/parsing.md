---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/parsing
title: Parsing
narrator: the person
group: service
area: specification
specifies: service language: parse
language: codified-2
retired: [g4, r4]
unbuilt: [r27]
---

# Parsing

## Purpose
A line parsed in the controlled language to one meaning or refused with why, its logical form returned, and its parse kept.

## Terms

## Behaviour
### [g1] A requirement in the language is parsed
- [r1] When the person parses a requirement that conforms to the language reference, the language service shall complete the request.

### [g2] The logical form of a requirement is returned
- [r2] When the person parses a requirement that conforms to the language reference with the logical form, the language service shall return one logical form of the requirement and complete the request.

### [g3] A requirement outside the language is refused
- [r3] If the person parses a requirement that does not conform to the language reference, then the language service shall refuse the request and name the requirement.

### [g5] A requirement that breaks a reading rule is refused
- [r5] If the person parses a requirement that violates a reading rule, then the language service shall refuse the request and name the reading rule.

### [g6] A construct the construct catalogue does not define is refused
- [r6] If the person parses a requirement that uses a construct that has no catalogue entry, then the language service shall refuse the request and name the construct.

### [g7] A fragment is refused with the terms that may follow
- [r7] If the person parses a fragment, then the language service shall refuse the request, name the fragment and return a term.

### [g8] The corpus's logical form of a requirement is returned
- [r8] While the corpus holds a logical form of a requirement, when the person parses the requirement with the logical form, the language service shall return the logical form.

### [g9] A kept parse is returned
- [r9] While a parse cache holds the parse of a requirement, when the person parses the requirement, the language service shall return the parse of the requirement, keep no compiled grammar and complete the request.

### [g10] A new parse is kept
- [r10] While a requirement has a parse that no parse cache holds, when the person parses the requirement, the language service shall keep a parse cache and complete the request.

### [g11] An unchanged grammar is not compiled again
- [r11] While a requirement has a parse that no parse cache holds and the compiled grammar of the requirement exists, when the person parses the requirement, the language service shall keep no compiled grammar and complete the request.

### [g12] The logical form puts an order after a collection on its members
- [r12] When the person parses a requirement that uses `order-by` with the logical form, the language service shall return a logical form that uses an order of a member of a collection.

### [g13] A requirement of a verb of two frames is read by one frame
- [r13] While a verb has two frames, when the person parses a requirement that uses a frame of the verb, the language service shall return one logical form of the requirement and complete the request.

### [g14] A request on more than one thing is outside the language
- [r14] If the person parses a requirement that has a plural object, then the language service shall refuse the request and name the requirement.

### [g15] A requirement of two meanings is refused naming its ambiguous text
- [r15] If the person parses a requirement that has more than one logical form, then the language service shall refuse the request and name the requirement and the ambiguous text of the requirement.

### [g16] A requirement read by two frames of a verb is refused naming the two frames
- [r16] If the person parses a requirement whose ambiguous text uses two frames of a verb, then the language service shall refuse the request and name every frame that the ambiguous text uses.

### [g17] A request parameter's value that is another thing's value is parsed
- [r17] When the person parses a requirement that uses `param-of`, the language service shall complete the request.

### [g18] The logical form keeps a value in use
- [r18] When the person parses a requirement that uses `param-of` with the logical form, the language service shall return a logical form that holds a value in use.

### [g19] A requirement that uses an item's term is parsed for the item
- [r19] While an item holds a term, when the person previews a requirement that uses the term for the item, the language service shall complete the request.

### [g20] The logical form of a requirement that uses an item's term is returned for the item
- [r20] While an item holds a term, when the person previews a requirement that uses the term for the item with the logical form, the language service shall return one logical form of the requirement and complete the request.

### [g22] A requirement outside the language is refused for an item
- [r22] If the person previews a requirement that does not conform to the language reference for an item, then the language service shall refuse the request and name the requirement.

### [g23] A response that makes a request with its parameters is parsed
- [r23] When the person parses a requirement that uses `response-request`, the language service shall complete the request.

### [g24] The logical form reads a response's request with its parameters
- [r24] When the person parses a requirement that uses `response-request` with the logical form, the language service shall return a logical form that uses `request-params`.

### [g25] A trigger on a reply to a request about its object is parsed
- [r25] When the person parses a requirement that uses `reply-trigger`, the language service shall complete the request.

### [g26] The logical form keeps the request a reply is on
- [r26] When the person parses a requirement that uses `reply-trigger` with the logical form, the language service shall return a logical form that holds a replied request.

### [g27] A reply trigger on a request of a plural object is refused
- [r27] While a requirement uses `reply-trigger` and the requirement has a plural object, if the person parses the requirement, then the language service shall refuse the request and name the requirement.

### [g29] A trigger on a failed request about its object is parsed
- [r29] When the person parses a requirement that uses `reply-failure`, the language service shall complete the request.

### [g28] The logical form keeps the request a failure is on
- [r28] When the person parses a requirement that uses `reply-failure` with the logical form, the language service shall return a logical form that holds a replied request.

