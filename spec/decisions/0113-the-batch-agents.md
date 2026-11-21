---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-batch-agents
summary: "The plugin's agents are four, each with exactly its role's tools and its model in its definition: `batch-implementer` (opus; builds one task of a batch), `pr-reviewer` (opus; no Edit, Write or shell), `architecture-reviewer` (opus; no Edit or Write) and `trial-runner` (sonnet); no agent can start an agent."
date: 2026-11-21
status: superseded
tier: check
enforced_by: [tests/scripts/test_agents.py::RoleBoundaries]
supersedes: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-2-0-agents]
source: [quote-42]
by: "batch-70's driver, under directive-1"
---

# 0113. The batch agents

## Context

Decision 0083 fixed the plugin's agents at three. A batch's driver dispatched each task to a general-purpose subagent with its fixed rules retyped in every brief (b34). An agent definition carries those rules, its tools and its model once, as pr-reviewer does for the review.

## Decision

The plugin's agents are:

| agent | model | tools it does not have |
|---|---|---|
| `batch-implementer` | opus | Agent, Task |
| `pr-reviewer` | opus | Edit, Write, Bash |
| `architecture-reviewer` | opus | Edit, Write |
| `trial-runner` | sonnet | |

No agent has Agent or Task, so no agent can start an agent. Each names its model in its definition. building-a-batch's step 4 dispatches each running task to `batch-implementer`; the brief holds only what is the task's own. A reviewer's findings are its reply, saved by the session that started it.
