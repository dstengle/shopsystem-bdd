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

- **the person** (actor): the human who runs the commands.
- **`work`** (actor): the queue's command. Kind of: agent.
- **`work run`** (actor): the supervisor. Kind of: agent.
- **agent** (kind): a session or a tool, as the one that does what a verb says.

- **initiative** (kind): the delivery of one request.
- **work-item** (kind): a unit of delivery.
- **capability-proposal** (kind): a proposal of one capability.
- **request** (kind): lines another context proposes.
- **session** (kind): one conversation. Kind of: agent.
- **stage** (kind): one session for a node. Kind of: session.
- **file** (kind): a file of the repository.
- **command** (kind): one run of a tool.
- **reason** (kind): what an error names.
- **brief** (kind): the input of a stage.

- **status** (attribute of initiative): Values: `proposed`, `started`, `done`, `abandoned`.
  Transitions: `proposed` → `started`: `work start`; `started` → `done`: complete; `started` → `abandoned`: `work abandon`.
- **status** (attribute of work-item): Values: `drafted`, `ready`, `done`, `green`, `withdrawn`.
  Transitions: `drafted` → `ready`: `work`; `ready` → `done`: an implement stage; `done` → `green`: a review stage.
- **status** (attribute of capability-proposal): Values: `drafted`, `approved`, `withdrawn`.
- **status** (attribute of request): Values: `open`, `accepted`, `refused`.

- **open** (condition of initiative): An initiative is open when the initiative is not `done` and the initiative is not `abandoned`.

- **start** (event): a stage begins. Frame: agent starts stage.
- **end** (event): a session stops. Frame: agent ends session.
- **take** (event): `work run` takes an initiative through its transitions. Forms: takes, taken. Frame: agent takes initiative.
- **interleave** (event): `work run` runs initiatives side by side. Frame: `work run` interleaves initiative.
- **give** (event): Forms: gives, given. Frame: `work run` gives brief to stage.
- **refuse** (event): Forms: refuses, refused. Frame: agent refuses command.

- **spec lock** (resource, exclusive): held by every integrate round.
- **worker slot** (resource, counted by `workers`): held by every worker.
