---
id: decision/capability-ids-are-context-scoped
summary: "Ids are type-first: <kind>/<context path>/<name>, with the design model's kind names; the context is bounded-context/missingmass.io/shopsystem/shopsystem-bdd, a requirement capability/<path>/<name>#r<n>, short forms <kind>/<name> and, where a field fixes the kind, <name>."
date: 2026-10-17
status: proposed
source: "the person's direction, 2026-10-17; shopsystem-knowledge decision/an-artifacts-iri-is-its-types-then-its-owners-path (adrs/0073) and decision/names-are-iris-printed-short; shopsystem-kb decision/iri-grammar; docs/design-model/grammar.md v3 section 6"
---

# 0027. Ids are type-first

## Decision

Every id is `<kind>/<context path>/<name>`, the kind first, using the design model's kind names. The context path is `<owner>/<product>/<context>`: for this repository `missingmass.io/shopsystem/shopsystem-bdd`. The bounded context's id is `bounded-context/<context path>`. A capability `spec/capabilities/<name>.md` has id `capability/<context path>/<name>`; a decision, an observation, a work item and every other node follows the same form with its own kind (`design-decision`, `observation`, `work-item`, `capability-proposal`, `initiative`, and the rest of the model's kinds). A `<name>` matches `[a-z0-9]+(-[a-z0-9]+)*`. A requirement is `capability/<context path>/<name>#r<n>`, standing for the part `capability/<context path>/<name>#behaviour/r<n>`; `scripts/model` reads both as one requirement.

A frontmatter `id` is written in full form. A reference may be written `<kind>/<name>` inside this context, or the bare `<name>` where the field fixes the kind (`rests_on` takes design-decisions, `argues` and `under` capabilities, and so on). A reference written `<context name>/<name>`, `decision/<name>` or `obs/<name>` is refused as unresolved.

## Context

The model is to move into shopsystem-knowledge, which owns the shop's types and their IRIs and puts the type first, then the owner's path. Ids chosen here that fit those IRIs move into the store by a fixed rule; ids that do not would be renamed, and every reference with them. The earlier form of this decision put the context path first and left other nodes on `<kind>/<name>`, so two id shapes met in one repository. The person directed on 2026-10-17 that every id take the one type-first form before consuming repositories migrate to it.

## Alternatives

The context path first for capabilities (`<context path>/<name>`), the earlier form of this decision: kind-less, and unlike the IRIs of every other node. `<kind>/<name>` with no context path, kb's present spelling: no owner, product or context, so two contexts collide. The part form `#behaviour/r<n>` in every file: longer, and not grammar.md's RID. Accepting the old spellings (`decision/…`, `obs/…`, `<context name>/<name>`) alongside the new: two forms for one node, and a reference that resolves in one repository and not another.

## Consequences

Every existing id is renamed once, by a mechanical migration that changes no content; that is a migration, not an edit of an accepted decision or observation. A name that once held a `/` is renamed with `-`. Consuming repositories migrate their `decision/<name>` references and ledger headings to `design-decision/<name>`. i3 teaches the same form, each repository with its own owner, product and context name. grammar.md's RID, and whether a type can require part names of the form `r<n>`, go with the model to shopsystem-knowledge.
