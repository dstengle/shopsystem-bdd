---
id: bounded-context/example.org/fixture/domain-model
title: The smallest context with a domain model
language: codified-2
imports: []
---

# The smallest context with a domain model

A context whose terms come from its domain model (`spec/model/`) and its vocabulary (`spec/vocabulary/`), not from a
glossary (the domain contract design, §4.1 and §4.2). Its lines use only the words its vocabulary gives; tests of
domain_model, domain_model_check and spec_vocabulary read it. It is not this repository's spec.

## Composition

| area | kind | capabilities |
|---|---|---|
| notes | core | notebook |
