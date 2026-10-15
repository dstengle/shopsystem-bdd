---
id: decision/model-pinned-in-agent-definitions
summary: "Each agent's model is set in its definition: Opus for spec writers and reviewers, Sonnet for the implementer and spec-round, Haiku for the scout."
date: 2026-10-10
status: accepted
revisit_when: "a measured batch runs an agent on a model other than its definition's in more than half of its dispatches"
revisit_signal: measurement/kb-batches-32-35
source: "README, Models; agents/*.md"
---

# 0021. Model pinned in agent definitions

## Decision

`model:` in `agents/*.md` is the default; a dispatch that names a model overrides it.

## Context

A skill's `model:` field did not change a session's model; the plan's `Model:` line is advice to a controller.

## Alternatives

Model chosen per task by the plan.

## Consequences

Implementers ran Opus 32 of 42 times in kb batches 32-35 against "Sonnet by default". The signal has fired.
