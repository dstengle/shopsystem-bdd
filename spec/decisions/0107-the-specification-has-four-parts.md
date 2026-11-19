---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-specification-has-four-parts
summary: "A bounded context's specification is its domain model, vocabulary, requirements and decisions, with its adapter contracts beside them; the grammar is no part of a context."
date: 2026-11-19
status: accepted
tier: judgement
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/final-layout]
---

# 0107. The specification has four parts

## Decision

The specification of a bounded context has four parts: the domain model (spec/model/), the vocabulary (spec/vocabulary/), the requirements (spec/capabilities/, spec/universal.md) and the decisions (spec/decisions/). The adapter contracts (spec/adapters/) sit beside them. The grammar is the same in every bounded context and is no part of one.
