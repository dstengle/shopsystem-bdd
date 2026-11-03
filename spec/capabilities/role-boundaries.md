---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/role-boundaries
title: Role boundaries
narrator: the person using the workflow
group: guarantees
rests_on: [design-decision/the-v3-agents, design-decision/spec-writers-blind-to-code, design-decision/the-session-keeps-the-gate]
language: codified-1
retired: []
---

# Role boundaries

## Purpose
What the plugin's agent definitions guarantee about each role, whatever its input asks. Each is verified by reading
the definitions under `agents/`, not by a scenario. Tool lists bound what a session started as an agent can do directly: one with
Bash can still write files through the shell, which is why `work run` verifies the files a worker leaves.

## Terms

- **the researcher** (actor): the worker of a `research` stage, started as the agent `code-scout`.
- **the planner** (actor): the worker of a `plan` stage, started as the agent `bdd-planner`.
- **the implementer** (actor): the worker of an `implement` stage, started as the agent `bdd-implementer`.
- **the reviewer** (actor): the worker of a `review` stage, started as the agent `bdd-task-reviewer`.
- **`initiative-round`** (actor): the agent of every round.
- **`capability-writer`** (actor): the agent a round dispatches to draft a capability's statements.
- **`spec-checker`** (actor): the agent `checking-spec-consistency` dispatches to read the spec for findings.
- **`trial-runner`** (actor): the agent that runs one trial.
- **read** (event): a session or a tool reads a file. Forms: reads, read.
- **use** (event): a session uses a tool, a model or a file. Forms: uses, used.
- **push** (event): a commit is pushed to a remote. Forms: pushes, pushed.
- **show** (event): a session shows the person a thing. Forms: shows, shown.
- **name** (event): a message or a file names a thing. Forms: names, named.
- **list** (event): a session or a file lists things. Forms: lists, listed.
- **stop** (event): a session ends without doing what it was asked. Forms: stops, stopped.
- **keep** (event): a session leaves a thing as it was. Forms: keeps, kept.
- **commit** (event): a session or a tool commits a change. Forms: commits, committed.
- **append** (event): a line is added at the end of a file. Forms: appends, appended.
- **delete** (event): a file or a scenario is removed. Forms: deletes, deleted.

## Behaviour

### [g1] Only `initiative-round` dispatches
Restates: r1@0.29.
- [r1] The researcher shall not start a dispatch.
- [r2] The planner shall not start a dispatch.
- [r3] The implementer shall not start a dispatch.
- [r4] The reviewer shall not start a dispatch.
- [r5] `trial-runner` shall not start a dispatch.

### [g2] No reviewer, researcher or planner has the Edit tool
Restates: r2@0.29.
- [r6] The reviewer shall not use `Edit`.
- [r7] The researcher shall not use `Edit`.
- [r8] The planner shall not use `Edit`.

### [g3] `capability-writer` has no edit and no shell tool
Restates: r3@0.29.
- [r9] `capability-writer` shall not use `Edit`.
- [r10] `capability-writer` shall not use `Bash`.

### [g4] The implementer loads `bdd-red-green` with the Skill tool
Restates: r4@0.29.
- [r11] The implementer shall use `bdd-red-green`.
- [r12] The implementer shall use `Skill`.

### [g5] Each agent's model
Restates: r5@0.29.
- [r13] `capability-writer` shall use `opus`.
- [r14] The planner shall use `opus`.
- [r15] The reviewer shall use `opus`.
- [r16] The implementer shall use `sonnet`.
- [r17] `initiative-round` shall use `sonnet`.
- [r18] `spec-checker` shall use `sonnet`.
- [r19] `trial-runner` shall use `sonnet`.
- [r20] The researcher shall use `haiku`.

### [g6] The planner and the branch reviewer have no shell tool
Restates: r6@0.29, r7@0.29.
- [r21] The planner shall not use `Bash`.
- [r22] The branch reviewer shall not use `Bash`.

## Implementation, may change
- Tool lists and `model:` in `agents/*.md`; `skills:` names a skill, which a `claude -p --agent` session does not
  preload, so the implementer loads `bdd-red-green` with the Skill tool. `tests/scripts/test_agents.py` reads the
  definitions and verifies each statement.
- What a tool list cannot enforce (no push, one write path) is asked, or `permissions.deny` in the consuming
  repository's settings.
- The actors and events above are used by every guarantees capability; they are written here once, since a term is
  given once in a context.

## Not yet
- None.

## Dropped
