---
id: bounded-context/example.org/fixture/generate
title: The generation fixture
language: codified-1
---

# The generation fixture

A small codified context for the tests of `features generate` and `features vocab` (design §14). It is not this
repository's spec.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| work-item | under | capability-proposal | one |
| capability-proposal | part of | initiative | one |
| initiative | fulfils | request | one |
| stage | for | work-item | one |

## Glossary

- **the person** (proper noun): the human who runs the commands.
- **`work`** (proper noun): the queue's command. Kind of: agent.
- **`work run`** (proper noun): the supervisor. Kind of: agent.
- **agent** (noun): a session or a tool, as the one that does what a verb says.

- **initiative** (noun): the delivery of one request.
- **work-item** (noun): a unit of delivery.
- **capability-proposal** (noun): a proposal of one capability.
- **request** (noun): lines another context proposes.
- **session** (noun): one conversation. Kind of: agent.
- **stage** (noun): one session for a node. Kind of: session.
- **file** (noun): a file of the repository.
- **command** (noun): one run of a tool.
- **reason** (noun): what an error names.
- **brief** (noun): the input of a stage.

- **status** (attribute of initiative): Values: `proposed`, `started`, `done`, `abandoned`.
  Transitions: `proposed` → `started`: `work start`; `started` → `done`: complete; `started` → `abandoned`: `work abandon`.
- **status** (attribute of work-item): Values: `drafted`, `ready`, `done`, `green`, `withdrawn`.
  Transitions: `drafted` → `ready`: `work`; `ready` → `done`: an implement stage; `done` → `green`: a review stage.
- **status** (attribute of capability-proposal): Values: `drafted`, `approved`, `withdrawn`.
- **status** (attribute of request): Values: `open`, `accepted`, `refused`.

- **open** (adjective of initiative): An initiative is open when the initiative is not `done` and the initiative is not `abandoned`.

- **start** (verb, action): a stage begins. Frame: agent starts stage.
- **end** (verb, action): a session stops. Frame: agent ends session.
- **take** (verb, action): `work run` takes an initiative through its transitions. Forms: takes, taken. Frame: agent takes initiative.
- **interleave** (verb, action): `work run` runs initiatives side by side. Frame: `work run` interleaves initiative.
- **give** (verb, action): Forms: gives, given. Frame: `work run` gives brief to stage.
- **refuse** (verb, action): Forms: refuses, refused. Frame: agent refuses command.

- **spec lock** (noun, exclusive): held by every integrate round.
- **worker slot** (noun, counted by `workers`): held by every worker.
