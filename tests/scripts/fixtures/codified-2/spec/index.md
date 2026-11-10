---
id: bounded-context/example.org/fixture/codified-2
title: The smallest codified-2 context
language: codified-2
imports: [cli]
---

# The smallest codified-2 context

The words grammar 4's tests parse in (the CNL 4 design, I7a): the CLI pack imported, and a few words of its own. The
scenario worlds copy it (tests/scenarios/codified2_world.py), and grammar/corpus/core-4.txt is parsed in it. It is
not this repository's spec.

## Glossary

- **the person** (proper noun): the human who runs the tools. Kind of: agent.
- **`work`** (proper noun): the tool of the backlog. Kind of: tool.
- **session** (noun): an agent that runs in a terminal. Kind of: agent.
- **file** (noun): a file of a repository.
- **stage** (noun): a step of a piece of work.
- **status** (attribute of stage): Values: `open`, `done`.
- **write** (verb, action): an agent puts text into a file. Forms: writes, written. Frame: agent writes file.
- **end** (verb, action): an agent stops a stage. Frame: agent ends stage.
- **follow** (verb, state): an agent keeps track of a stage. Frame: agent follows stage.
