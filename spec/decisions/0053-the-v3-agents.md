---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-v3-agents
summary: "The plugin's agents on design model v3, each with exactly its role's tools and its model in its definition: bdd-planner joins them, the supervisor starts the delivery workers, and only initiative-round can start an agent."
date: 2026-10-19
status: accepted
supersedes: [design-decision/rules-held-by-agent-tools, design-decision/model-pinned-in-agent-definitions]
source: [initiative/i10]
by: "the coordinator, 2026-10-19, on the i10 drafter's question 6 (ledger, ruling Q6); the person approves at the gate"
---

# 0053. The v3 agents

## Decision

Each role is an agent under `agents/` whose tool list is exactly the role's, and whose `model:` is the
default for every start of it; `work run` passes `--model` only where `.shop/delivery.toml` overrides it.

| agent | role | tools | model |
|---|---|---|---|
| `capability-writer` | writes capability files, blind to code | Read, Glob, Grep, Write | Opus |
| `feature-formulator` | writes feature files, blind to code | Read, Glob, Grep, Write | Opus |
| `spec-checker` | judges a spec's consistency, blind to code | Read, Glob, Grep, Write | Sonnet |
| `initiative-round` | runs a spec round (integrate, formulate) | Read, Glob, Grep, Bash, Write, Edit, Agent | Sonnet |
| `code-scout` | researcher of a `drafted` work-item | Read, Glob, Grep, Bash, Write | Haiku, low effort |
| `bdd-planner` | planner of a `researched` work-item | Read, Glob, Grep, Write | Opus |
| `bdd-implementer` | implementer of a `claimed` work-item | Read, Edit, Write, Glob, Grep, Bash, Skill; `skills:` its own, `bdd-red-green` among them, the only skills `work run` allows | Sonnet |
| `bdd-task-reviewer` | reviewer of a done work-item | Read, Glob, Grep, Bash, Write | Opus |
| `bdd-branch-reviewer` | reviewer of an initiative's branch | Read, Glob, Grep, Bash, Write | Opus |
| `architecture-reviewer` | architecture review, when the person asks | Read, Glob, Grep, Bash, Write | Opus |

Only `initiative-round` has the Agent tool. The delivery workers (researcher, planner, implementer,
reviewers) are started by `work run`, a script, one `claude -p --agent` session each. No reviewer, scout or
planner has Edit, and the planner has no shell, so a planner cannot build what it plans. What a tool list
cannot enforce (no push, one write path) is asked in the brief, checked by `work run` from the files a worker
leaves, or set in `permissions.deny` in the consuming repository: a plugin agent's hooks and permissionMode
are ignored. capability/role-boundaries states the guarantees; `tests/scripts/test_agents.py` checks them.
