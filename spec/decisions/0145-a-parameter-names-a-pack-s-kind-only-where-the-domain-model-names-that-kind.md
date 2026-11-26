---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-parameter-names-a-pack-s-kind-only-where-the-domain-model-names-that-kind
summary: "An operation's parameter is typed by an imported pack's kind only when an object of the domain model names that kind; otherwise it keeps its own reading, so importing a pack does not retype a context's parameters."
date: 2026-11-26
status: accepted
tier: judgement
---

# 0145. A parameter names a pack's kind only where the domain model names that kind

## Context

b618 (batch-119) switched this repository to the base pack; the broad rule b609's note implied would have read withdraw's reason as the request pack's refusal reason and rewritten the generated features of items and directives.

## Decision

A parameter whose word is a kind of an imported pack reads as that kind only when an object of the context's domain model names the kind (today only version). Elsewhere the parameter keeps its own reading (a reason stays text, not the request pack's refusal reason). Until the item that checks it is delivered this decision is a judgement; that item writes its successor at its own tier, naming its enforcer.

## Alternatives

Every parameter naming a pack kind reads as it: rejected, it retypes parameters a context means as text.
