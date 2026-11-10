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

- **`trial-runner`** (proper noun): the agent that runs one trial. Kind of: dispatch.
- **read** (verb, action): a session or a tool reads a file, a commit or another thing. Forms: reads, read. Frame: agent reads thing.
- **name** (verb, state): a message or a file names a thing. Forms: names, named. Frame: agent names thing. Redefines: cli.
- **keep** (verb, action): a session leaves a thing as it was. Forms: keeps, kept. Frame: agent keeps thing.

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
