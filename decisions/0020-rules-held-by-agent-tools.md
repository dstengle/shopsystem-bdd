---
id: decision/rules-held-by-agent-tools
summary: "Each role is an agent whose tools are exactly the role's; only spec-round may start agents, and no reviewer can edit."
date: 2026-09-27
status: accepted
source: "0.7.0 (a53d21b); README, Agents"
---

# 0020. Rules held by agent tools

## Decision

Agents: capability-writer, feature-formulator, spec-round, code-scout, bdd-implementer, bdd-task-reviewer, bdd-branch-reviewer, architecture-reviewer, each with its tool list. What a tool list cannot hold (no push, one write path) stays a request, or `permissions.deny` in the consuming repository.

## Context

Rules asked of a general-purpose agent did not hold.

## Alternatives

Instructions only.

## Consequences

A plugin agent's hooks and permissionMode are ignored, so command restrictions need repository settings.
