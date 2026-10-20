---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/model-check-solves-with-clingo
summary: "scripts/model reads facts with the standard library and solves grammar.md's constraints with clingo, from scripts/model.lp."
date: 2026-10-15
status: accepted
source: "grammar-eval (rules.lp, the version-1 evaluator); docs/design-model/grammar.md v3 section 7"
---

# 0025. Model check solves with clingo

## Decision

`model facts` is standard library only and prints facts under grammar.md's relation names. `model check` solves them with `scripts/model.lp`, a clingo translation of grammar.md v3 sections 1, 3 and 4, and says how to install clingo when it is missing.

## Context

Constraints written once in an engine that reads like grammar.md, rather than re-implemented by hand beside it. grammar-eval already showed the translation works and where grammar.md does not compile.

## Alternatives

A hand-written Python checker (two statements of one grammar that drift); Soufflé (a compiler toolchain to install).

## Consequences

The one script whose main command needs a package. The document evaluator (grammar-eval) can share model.lp once it moves to v3 vocabulary.
