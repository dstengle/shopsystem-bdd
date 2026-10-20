---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/scout-on-haiku-at-low-effort
summary: "code-scout runs on Haiku at low effort."
date: 2026-10-11
status: accepted
source: "0.11.0, 0.17.0 (a84031a); records/measurements/fixture-runs/2026-10-11-effort-test-log.md"
---

# 0015. Scout on haiku at low effort

## Decision

`agents/code-scout.md` sets `model: haiku` and `effort: low`.

## Context

64% of the scouts' output tokens were reasoning; at low effort output fell by about a third with the same findings on the fixtures and on kb.

## Alternatives

Medium effort, as every agent ran before.

## Consequences

Implementers and reviewers keep their effort: a reviewer's reasoning is what finds defects.
