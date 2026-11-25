---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-language-toolchain-is-a-bounded-context-of-a-supporting-subdomain
summary: "The grammar, logic and language processing form at least one bounded context, addressing a supporting subdomain, not a module of specification."
date: 2026-11-25
status: accepted
tier: judgement
source: [quote-84]
---

# 0130. The language toolchain is a bounded context of a supporting subdomain

## Context

The disentangling worked example proposed keeping it a module of specification for now (Q2).

## Decision

The language toolchain (the grammar, the logic checks, the language processing) is at least one bounded context of its own, and the subdomain it addresses is supporting. Other contexts reach it through its published contract, not a shared kernel.

## Alternatives

A module of specification: rejected. A generic subdomain: rejected, it is specific to this product.
