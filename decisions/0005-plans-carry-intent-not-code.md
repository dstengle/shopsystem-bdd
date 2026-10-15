---
id: decision/plans-carry-intent-not-code
summary: "A plan says which scenarios go green, why they are red today and what was decided; it carries no code, file contents or diffs."
date: 2026-09-27
status: accepted
source: "records/archive/design-notes/2026-09-22-bdd-workflow-design.md; 0.6.0 (0b18857)"
---

# 0005. Plans carry intent not code

## Decision

The planner plans and the implementer implements. A task carries the scenarios or check, why each is red today, where the change lands, the decisions the spec left open, reusable steps and fixtures, and verification commands with counts from the tags. No code blocks, file contents, diffs or step-definition bodies.

## Context

Plans that carried code made red a performance: the implementer pasted what had gone green elsewhere and hand-backs stopped happening.

## Alternatives

superpowers:writing-plans' own template, which shows code in every step.

## Consequences

Under the pull model the work-item, filled in stages, takes the task's place; the rule carries over to the item.
