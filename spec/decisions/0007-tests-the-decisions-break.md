---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/tests-the-decisions-break
summary: "A task lists every existing test its decisions make impossible to keep and what becomes of each; any other test an implementer would weaken is BLOCKED."
date: 2026-10-10
status: accepted
source: [decision-argument/2026-10-10-small-slices-and-steps-design, decision-argument/2026-10-11-rules-adjusted-design]
by: "0.11.0, 0.13.0"
---

# 0007. Tests the decisions break

## Decision

Each task has "Tests the decisions break": the test, the decisions, and whether it is rewritten (to assert what), deferred (with the slice that brings it back) or a question for the spec. An implementer may change what a test asserts only when it is listed. Two allowances (0.13.0): a test's setup changed with no assertion touched, and a test first committed after the task's batch base rewritten; each is reported.

## Context

One kb slice removed the tests that covered a regression two of the plan's decisions caused together.

## Alternatives

Trust the implementer to judge which tests move with the change.

## Consequences

Four kb batches, zero tests deleted; every hand-back in them was this rule catching its own omission.
