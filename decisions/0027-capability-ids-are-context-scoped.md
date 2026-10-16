---
id: decision/capability-ids-are-context-scoped
summary: "Ids follow shopsystem-knowledge's IRIs: the context is missingmass.io/shopsystem/shopsystem-bdd, a capability <context>/<name>, a requirement <capability>#r<n>, short for the part <capability>#behaviour/r<n>."
date: 2026-10-16
status: proposed
source: "shopsystem-knowledge decision/an-artifacts-iri-is-its-types-then-its-owners-path (adrs/0073) and decision/names-are-iris-printed-short; shopsystem-kb decision/iri-grammar; docs/design-model/grammar.md v3 section 6 (CAP = CTX '/' NAME); the person, 2026-10-16"
---

# 0027. Capability ids are context scoped

## Decision

The bounded context's id is `missingmass.io/shopsystem/shopsystem-bdd`: its owner's domain, its product and its context name, the path shopsystem-knowledge puts below a type's IRI. A capability `spec/capabilities/<name>.md` has id `missingmass.io/shopsystem/shopsystem-bdd/<name>`, so its full IRI is `https://missingmass.io/shopsystem/capability/missingmass.io/shopsystem/shopsystem-bdd/<name>`. A requirement is written `<capability>#r<n>`, the form of grammar.md's RID, and stands for the part `<capability>#behaviour/r<n>`, the form kb's IRI grammar accepts; `scripts/model` reads both as one requirement. Inside this context a capability may be written `<name>` or `shopsystem-bdd/<name>`, and `shopsystem-bdd` alone names the context. Other nodes (decisions, observations, records, work) keep their `<kind>/<name>` ids until shopsystem-knowledge gives the model's types their IRIs.

## Context

The model is to move into shopsystem-knowledge, which owns the shop's types and their IRIs (obs/2026-10-16-model-owned-by-knowledge). Ids chosen here that fit its IRIs move into the store by a fixed rule; ids that do not would be renamed, and every reference with them. grammar.md's `CAP "#r" DIGITS` has no collection, which kb's part IRIs need.

## Alternatives

`shopsystem-bdd/<name>`, the context name alone as the context's id (not an IRI path; renamed on the way into the store). `capability/<name>`, kb's present spelling (no owner, product or context). The part form `#behaviour/r<n>` in every file (longer, and not grammar.md's RID).

## Consequences

Observations written with `shopsystem-bdd/<name>` stay as they are and still resolve. i3 teaches the same form to consuming repositories, each with its own owner, product and context name. grammar.md's RID, and whether a type can require part names of the form `r<n>`, go with the model to shopsystem-knowledge.
