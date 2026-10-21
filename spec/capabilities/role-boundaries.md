---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/role-boundaries
title: Role boundaries
narrator: the person running the workflow
group: guarantees
rests_on: [design-decision/the-v3-agents, design-decision/spec-writers-blind-to-code]
retired: []
---

# Role boundaries

## Purpose
What the plugin's agent definitions guarantee about each role, whatever a brief asks. Each is checked by reading
the definitions under `agents/`, not by a scenario. Tool lists bound what an agent can do directly: an agent with
Bash can still write files through the shell, which is why `work run` checks the files a worker leaves.

## Behaviour
- [r1] The plugin's agent definitions shall let only `initiative-round` start another agent.
- [r2] The plugin's agent definitions shall give no reviewer, no scout and no planner the Edit tool.
- [r3] The plugin's agent definitions shall give the `capability-writer` and the `feature-formulator` no edit and no shell tool.
- [r4] The plugin's agent definitions shall give the implementer the skills listed under its `skills:`, `bdd-red-green` always among them, and the Skill tool, which `work run` allows only for those skills.
- [r5] The plugin's agent definitions shall name each agent's model: Opus for the spec writers, the planner and the reviewers, Sonnet for the implementer, `initiative-round` and the `spec-checker`, Haiku for the scout.
- [r6] The plugin's agent definitions shall give the `bdd-planner` no shell tool.

## Implementation, may change
- Tool lists and `model:` in `agents/*.md`; `skills:` names a skill, which a `claude -p --agent` session does not
  preload, so the implementer loads `bdd-red-green` with the Skill tool (supervision r12). `tests/scripts/test_agents.py` reads the
  definitions and checks each line.
- What a tool list cannot enforce (no push, one write path) is asked, or `permissions.deny` in the consuming
  repository's settings.

## Not yet
- None.
