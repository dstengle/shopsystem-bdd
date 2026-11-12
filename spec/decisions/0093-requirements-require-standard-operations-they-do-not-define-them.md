---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/requirements-require-standard-operations-they-do-not-define-them
summary: "A requirement line names a standard operation such as ordering, uniqueness or a count with its key and direction in neutral words, the logical form keeps it as one named atom of the standard meaning, the test checks it with ordinary code on the actual output, and the glossary adds an order only where a value's type gives none."
date: 2026-11-12
status: accepted
tier: judgement
by: "the person, 2026-11-12"
---

# 0093. Requirements require standard operations, they do not define them

## Context

subscriptions-viewer-feed's latest-videos r9 (plugin 0.34.1) could not say 'every video from the channel, newest first'; the research record .shop/records/2026-11-12-collections-research.md (b269) proposed expanding an order into a pairwise box in the logical form, a per-list Order: default in the glossary, an Order: by time on the key, and a generator that computes the expected sequence as an explicit table. The person, 2026-11-12: there is too much focus on proving things like list order rather than instructing the code to test it; explicit listing works only for very small sets of data; the attribute and direction belong in the statement, not the glossary; an Order: by time would make ordering by title difficult; and 'I also want to be careful trying to define order as opposed to require order. There are many things that we could define that would be redefinition of widely accepted algorithms.'

## Decision

1. A requirement line requires a standard operation (an order, uniqueness, a count, a first or top n, an aggregate) by naming it; the language never defines its meaning. 2. An order is said in the line with its key and a neutral direction: 'ordered by <attribute>, in ascending order' or 'in descending order' (e.g. 'a video list that holds every video from the channel, ordered by publication time, in descending order'). Type-flavoured words ('newest first', 'A to Z', 'highest first') are not part of the language. 3. The glossary declares no order for a value whose type already orders it (a time, a number, a text). It declares one only where the values do not (an Order: as listed for named values such as priorities, an Order: by number for dotted codes such as releases), as Order: does today; there is no per-collection order in the glossary. 4. The logical form keeps the requirement as one atom of the standard meaning, e.g. ordered(x7, publication time, descending); model logic reads it as a fact (two lines that require one list in opposite orders conflict) and does not prove it or expand it into pairs. 5. The generated Then states the property ('the video list v3 is ordered by publication time, in descending order'); its handler checks it on the actual output with ordinary code (a sorted comparison), at any size of data. The Givens give data that lets the check fail (at least three distinct key values not in the required order), stated as a population or produced by test setup; an explicit expected table is used only where a group's given block lists small example data on purpose.

## Alternatives

The research record's design: an order expanded into a pairwise before/cmp box in the logical form, the generator as oracle printing the expected sequence, a per-collection Members/Order default and an Order: by time on the key: it redefines sorting, does not scale past a few listed items, and an Order: by time would make ordering by title awkward. Type-flavoured direction words: read better but tie each direction to a kind of value the glossary would have to declare.
