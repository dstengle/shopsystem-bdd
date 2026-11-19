---
id: bounded-context/example.org/fixture/domain-model
title: The smallest context with a domain model
language: codified-2
imports: [request]
---

# The smallest context with a domain model

A context whose terms come from its domain model (`spec/model/`) and its vocabulary (`spec/vocabulary/`), not from a
glossary (the domain contract design, §4.1 and §4.2). It imports the domain-request pack, so its lines say a request
in its own words: an operation of the notes service with its parameters (a text, a value, a flag, an object, none,
and a fixed object); tests of domain_model, domain_model_check, spec_vocabulary and the request's grammar, logical form
and steps read it. It is not this repository's spec.

## Composition

| area | kind | capabilities |
|---|---|---|
| notes | core | notebook |
