---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-2-0-agents
summary: "The plugin's agents in 2.0 are three, each with exactly its role's tools and its model in its definition: `pr-reviewer` (opus; no Edit, Write or shell), `architecture-reviewer` (opus; no Edit or Write) and `trial-runner` (sonnet); no agent can start an agent."
date: 2026-11-05
status: accepted
tier: check
enforced_by: [tests/scripts/test_agents.py::RoleBoundaries]
supersedes: [design-decision/the-v3-agents]
source: [record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-9]
by: "workflow simplification plan 9, decided by the planner; revisit"
---

# 0083. The 2.0 agents

## Context

Decision 0053 gave the agents of design model v3: the stage workers `work run` started (code-scout, bdd-planner,
bdd-implementer, bdd-task-reviewer, bdd-branch-reviewer), the spec rounds (initiative-round, capability-writer,
spec-checker, delegation-answerer) and batch-analyst. Plugin 2.0.0 retires `work run` and its stages
(design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired); a batch is built by a session
with superpowers' process, and reviewed once at its pull request.

## Decision

The plugin's agents are:

| agent | model | tools it does not have |
|---|---|---|
| `pr-reviewer` | opus | Edit, Write, Bash |
| `architecture-reviewer` | opus | Edit, Write |
| `trial-runner` | sonnet | |

No agent has Agent or Task, so no agent can start an agent. Each names its model in its definition. A reviewer's findings are its reply, saved by the
session that started it: the harness refuses a subagent's Write of a findings file (plan-7 Q1; the reviewer's Write
removed by the plan-9 review's S4).

## Consequences

The other agents and the skills that only drove them are deleted with `work run`. `tests/scripts/test_agents.py`
holds the set, the tools and the models.
