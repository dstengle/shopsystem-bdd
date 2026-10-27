---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/an-asker-is-told-by-its-registered-asker-id
summary: "For now `work` tells one asker from another by the asker id its repository is registered under, and the upstream's allow list holds those asker ids."
date: 2026-10-27
status: accepted
source: [request/missingmass.io/shopsystem/shopsystem-bdd/q14, initiative/missingmass.io/shopsystem/shopsystem-bdd/i39]
by: "the answer to question 1 of request q14 (product/missingmass.io/subscriptions-viewer), on its line 21"
---

# 0071. An asker is told by its registered asker id

## Context

Line 21 of request q14 asks that `work` tell one asker from another by an identity each asker holds alone, and
line 20 that a request or a message from an identity the upstream does not allow for the asker it names is left
untaken. The identity could be a signing key, a GitHub account or token, or the asker id a repository is
registered under; the choice decides what the allow list holds.

## Decision

For now, an asker is told from another by the repository it is registered as: the identity is the asker id a
repository is registered under, and the upstream's allow list holds those asker ids.

## Alternatives

- A signing key each asker holds.
- A GitHub account or token.
