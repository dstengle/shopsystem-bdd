---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/requests-only-propose
summary: "A request's lines only propose; the upstream writes the requirement in its own terms, and how a request is kept or exchanged is the upstream's implementation, never a line."
date: 2026-11-05
status: accepted
tier: judgement
source: [request/missingmass.io/shopsystem/shopsystem-bdd/q14, initiative/missingmass.io/shopsystem/shopsystem-bdd/i39]
by: "the person's ruling on i39 (q14), 2026-10-27, restated 2026-11-05 when b1 was started over as b26"
---

# 0084. Requests only propose

## Context

Request q14 from subscriptions-viewer gave lines in its own words: "carriers" behind "one port", a file and a GitHub
issue as the first two. The integrate round of i39 took that wording into Behaviour lines and the glossary. On
2026-11-05 the same wording led backlog item b1 to be described in q14's terms rather than this context's, and b1
was withdrawn and started over as b26.

## Decision

A request's lines are a proposal against the capability contract. The asker has no final say on wording,
terminology or implementation: the upstream writes each accepted line as a requirement in its own terms, and a
request is resolved with the ids that cover what its lines asked for. Where or how a request is kept or exchanged (a
file in a git repository, a GitHub issue) is the upstream's implementation, and appears in no Behaviour line or term
because a request asked for it.

## Alternatives

- A request's accepted lines taken into the spec as written: the asker's terms then leak into the upstream's
  glossary, and an accepted line binds the implementation.
