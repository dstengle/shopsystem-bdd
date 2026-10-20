---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/controller-per-spec-round
summary: "A fresh initiative-round agent runs each integration, apply or formulation round; the session the person talks to keeps the gate and nothing else."
date: 2026-10-12
status: accepted
source: [measurement/2026-10-12-spec-round-test-log]
by: "0.18.0 (e3c846d)"
---

# 0014. Controller per spec round

## Decision

`initiative-round` runs one round and ends with it, waiting for its agents by the reply file each writes last. The session with the person shows the gate's text and passes answers to the next round.

## Context

A session that integrated and formulated a note read 30M tokens from cache, eleven times what its writers and formulators read.

## Alternatives

Keep rounds in the person's session.

## Consequences

Each round costs about 6k more output tokens; it saves nothing in a session that holds little.
