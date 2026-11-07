---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/role-boundaries
title: Role boundaries
narrator: the person using the workflow
group: guarantees
rests_on: [design-decision/the-v3-agents, design-decision/spec-writers-blind-to-code, design-decision/the-session-keeps-the-gate]
language: codified-1
retired: [r1, r2, r3, r4, r5, r6]
---

# Role boundaries

## Purpose
**Retired in plugin 2.0.0** (design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired): every requirement of this capability is retired, and the file is kept as the record of its ids and of where its 0.29 lines went.

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
- **read** (event): a session or a tool reads a file. Forms: reads, read. Frame: session reads file.
- **show** (event): a session shows the person a thing. Forms: shows, shown. Frame: session shows file.
- **name** (event): a message or a file names a thing. Forms: names, named. Frame: session names file.
- **list** (event): a session or a file lists things. Forms: lists, listed. Frame: session lists file.
- **keep** (event): a session leaves a thing as it was. Forms: keeps, kept. Frame: session keeps file.
- **delete** (event): a file or a scenario is removed. Forms: deletes, deleted. Frame: session deletes file.

## Behaviour

## Implementation, may change
- None: retired in plugin 2.0.0.

## Not yet
- None.

## Dropped
- r1@0.29: retired with role-boundaries#r1 in 2.0.0 (the-old-workflow-retired).
- r2@0.29: retired with role-boundaries#r2 in 2.0.0 (the-old-workflow-retired).
- r3@0.29: retired with role-boundaries#r3 in 2.0.0 (the-old-workflow-retired).
- r4@0.29: retired with role-boundaries#r4 in 2.0.0 (the-old-workflow-retired).
- r5@0.29: retired with role-boundaries#r5 in 2.0.0 (the-old-workflow-retired).
- r6@0.29: retired with role-boundaries#r6 in 2.0.0 (the-old-workflow-retired).
- r7@0.29: retired with role-boundaries#r6 in 2.0.0 (the-old-workflow-retired).
