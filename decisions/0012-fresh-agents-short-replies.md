---
id: decision/fresh-agents-short-replies
summary: "No agent is resumed; the controller passes paths and reads short replies, never diffs, reports or source."
date: 2026-10-10
status: accepted
source: "records/archive/design-notes/2026-10-10-small-slices-and-steps-design.md; 0.11.0"
---

# 0012. Fresh agents short replies

## Decision

Findings go to a file and then to a fresh implementer. The controller dispatches with paths and reads replies, `plan show` and `git log --oneline`; it opens a report only for a BLOCKED or NEEDS_CONTEXT reply.

## Context

A controller that read diffs and reports reached half a million tokens of context.

## Alternatives

Resume the implementer for its fix round.

## Consequences

Resuming in place of a fresh agent is held, with the measurement that would decide it.
