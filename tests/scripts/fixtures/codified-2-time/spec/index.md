---
id: bounded-context/example.org/fixture/codified-2-time
title: The smallest codified-2 context with time
language: codified-2
imports: [cli, time]
---

# The smallest codified-2 context with time

The smallest codified-2 context (tests/scripts/fixtures/codified-2/) with the time pack imported too (the CNL 4
design, I16): grammar/corpus/time-4.txt is parsed in it, and the scenario world copies it for a timed, clocked,
historical or unitless line (tests/scenarios/codified2_world.py). A stage's deadline is a moment of the stage.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| worktree | of | session | one |
| file | in | worktree |  |
| deadline | of | stage | one |

## Glossary

- **the person** (proper noun): the human who runs the tools. Kind of: agent.
- **`work`** (proper noun): the tool of the backlog. Kind of: tool.
- **session** (noun): an agent that runs in a terminal. Kind of: agent.
- **file** (noun): a file of a repository.
- **stage** (noun): a step of a piece of work.
- **worktree** (noun): a checkout a session works in.
- **deadline** (noun): the moment a stage is due. Kind of: moment.
- **status** (attribute of stage): Values: `open`, `done`.
- **write** (verb, action): an agent puts text into a file. Forms: writes, written. Frame: agent writes file.
- **end** (verb, action): an agent stops a stage. Frame: agent ends stage.
- **follow** (verb, state): an agent keeps track of a stage. Frame: agent follows stage.
- **give** (verb, action): an agent hands a file to an agent. Frame: agent gives file to agent.
