---
id: bounded-context/example.org/fixture/mixed-index
title: A codified-2 index over codified-1 files
language: codified-2
imports: [cli]
---

# A codified-2 index over codified-1 files

tests/scripts/fixtures/codified-2's index with a few words of its own (b151, CNL 4's I20): the index says codified-2
and imports the CLI pack, while `universal.md` and the capability `shelf` say codified-1 and are read in the old
grammar over the same glossary.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| worktree | of | session | one |
| file | in | worktree |  |

## Glossary

- **the person** (proper noun): the human who runs the tools. Kind of: agent.
- **`work`** (proper noun): the tool of the backlog. Kind of: tool.
- **session** (noun): an agent that runs in a terminal. Kind of: agent.
- **file** (noun): a file of a repository.
- **stage** (noun): a step of a piece of work.
- **worktree** (noun): a checkout a session works in.
- **status** (attribute of stage): Values: `open`, `done`.
- **write** (verb, action): an agent puts text into a file. Forms: writes, written. Frame: agent writes file.
- **end** (verb, action): an agent stops a stage. Frame: agent ends stage.
- **follow** (verb, state): an agent keeps track of a stage. Frame: agent follows stage.
- **give** (verb, action): an agent hands a file to an agent. Frame: agent gives file to agent.
- **clerk** (noun): a worker who keeps shelves.
- **shelf** (noun): a board that holds goods.
- **stock** (verb, action): a clerk fills a shelf. Forms: stocks, stocked. Frame: clerk stocks shelf.
- **count** (verb, action): a clerk counts the goods on a shelf. Forms: counts, counted. Frame: clerk counts shelf.
