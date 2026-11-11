---
id: bounded-context/example.org/grammar/constructs
title: The context of the construct catalogue
language: codified-2
imports: [cli, time]
---

# The context of the construct catalogue

The words `model constructs` parses each example of the construct catalogue (`grammar/constructs.md`) in: the
smallest codified-2 context (tests/scripts/fixtures/codified-2/) with the time pack imported too and a stage's
deadline, a moment of the stage, so that its grammar holds every family of functions grammar 4 generates. It is
part of the acceptance corpus, not a spec of this repository.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| worktree | of | session | one |
| file | in | worktree |  |
| layout | of | worktree | one |
| line | of | stage |  |
| push | of | command | one |
| deadline | of | stage | one |

## Glossary

- **the person** (proper noun): the human who runs the tools. Kind of: agent.
- **`work`** (proper noun): the tool of the backlog. Kind of: tool.
- **the stage form** (artifact): the fields a file of a stage holds, and their order. Schema: markdown frontmatter, `docs/stage.md`.
- **session** (noun): an agent that runs in a terminal. Kind of: agent.
- **file** (noun): a file of a repository.
- **stage** (noun): a step of a piece of work.
- **line** (noun): a sentence a stage is to meet.
- **worktree** (noun): a checkout a session works in.
- **deadline** (noun): the moment a stage is due. Kind of: moment.
- **layout** (artifact): the files a worktree is to hold, and where each is.
- **status** (attribute of stage): Values (adjective): `open`, `done`.
- **write** (verb, action): an agent puts text into a file. Forms: writes, written. Frame: agent writes file.
- **end** (verb, action): an agent stops a stage. Frame: agent ends stage.
- **follow** (verb, state): an agent keeps track of a stage. Frame: agent follows stage.
- **give** (verb, action): an agent hands a file to an agent. Frame: agent gives file to agent.
- **version** (attribute of file): the release a file was written for. Values (noun): `1.0.0`, `2.0.0`, `2.5.0`. Order: by number.
- **priority** (attribute of stage): how soon a stage is to be ended. Values (adjective): `low`, `high`, `urgent`. Order: as listed.
- **push** (noun): the commits a command sends to a remote.
- **commit** (noun): a change a command records in a repository. This: the commit the run makes.
- **make** (verb, state): a command has brought a commit about. Frame: command makes commit.
- **outcome** (attribute of line): what became of a line. Values (adjective): `proposed`, `accepted`, `refused`, `withdrawn`.
- **cover** (verb, state): a thing answers for a line. Forms: covers, covered. Frame: file covers line. Frame: stage covers line.
