---
id: product/missingmass.io/shopsystem
title: shopsystem
form: product identity
---

# shopsystem

## Purpose

A behaviour-driven workflow for bounded contexts kept in repositories: each context's behaviour specified as a model,
a vocabulary, requirement lines and decisions, its acceptance scenarios generated from them, its work shaped into
checkable lines, built in batches and reviewed once as one change, and its contracts exchanged with other contexts.

## Actors

- **the person** (actor/missingmass.io/shopsystem/the-person): the one who keeps a bounded context: shapes its work,
  merges its changes, answers its requests. Every hosted context declares its own actor of this name (its model's
  `actor the person`), and the adapters map them.
- **a session** (actor/missingmass.io/shopsystem/session): an agent working for the person in a context; acts only
  within what the person's directions and the context's rules allow.
- **a downstream context** (actor/missingmass.io/shopsystem/downstream-context): another bounded context that
  obtains this product's contexts' published contracts and raises requests to them.

## Contexts' ids

Every bounded context's id is `bounded-context/missingmass.io/shopsystem/<name>`, flat under this product, whatever
shop hosts it (decision 0129).
