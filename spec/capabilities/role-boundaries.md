---
id: missingmass.io/shopsystem/shopsystem-bdd/role-boundaries
title: Role boundaries
narrator: the person running the workflow
group: guarantees
rests_on: [decision/rules-held-by-agent-tools, decision/model-pinned-in-agent-definitions, decision/spec-writers-blind-to-code]
formulated_as: features/role-boundaries.feature
retired: []
---

# Role boundaries

## Purpose
What the plugin's agent definitions guarantee about each role, whatever a dispatch asks. Each is checked
by reading the definitions under `agents/`, not by a scenario; no script checks them yet. Tool lists bound
what an agent can do directly: an agent with Bash can still write files through the shell.

## Behaviour
- [r1] Only `spec-round` can start another agent.
- [r2] No reviewer and no scout has the Edit tool.
- [r3] The `capability-writer` and the `feature-formulator` have no edit and no shell tool.
- [r4] The implementer has `bdd-red-green` in its context and no Skill tool.
- [r5] Each agent names its model: Opus for the spec writers and reviewers, Sonnet for the implementer and `spec-round`, Haiku for the scout.

## Implementation, may change
- Tool lists and `model:` in `agents/*.md`; `skills:` preloads a skill.
- What a tool list cannot hold (no push, one write path) is asked, or `permissions.deny` in the consuming
  repository's settings.

## Not yet
- None.
