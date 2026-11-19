---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/parsing
title: Parsing
narrator: the person
group: service
language: codified-2
retired: []
unbuilt: [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11]
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

### [g4] A requirement of two meanings is refused
- [r4] If the person parses a requirement that has more than one logical form, then the language service shall refuse the request and name the requirement.

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

