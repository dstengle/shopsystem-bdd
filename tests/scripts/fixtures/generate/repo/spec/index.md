---
id: bounded-context/example.org/fixture/generate
title: The generation fixture
language: codified-1
---

# The generation fixture

A small codified context for the tests of `features generate` and `features vocab` (design §14). It is not this
repository's spec.

## Glossary

- **the person** (actor): the human who runs the commands.
- **`work`** (actor): the queue's command.
- **`work run`** (actor): the supervisor.

- **initiative** (kind): the delivery of one request.
- **work-item** (kind): a unit of delivery.
- **capability-proposal** (kind): a proposal of one capability.
- **request** (kind): lines another context proposes.
- **session** (kind): one conversation.
- **stage** (kind): one session for a node.
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

- **open** (condition of initiative): Means: its status is not `done` and not `abandoned`.

- **under** (relation work-item → capability-proposal): a work-item delivers part of a proposal.
- **part of** (relation capability-proposal → initiative): a proposal is part of one initiative.
- **fulfils** (relation initiative → request): an initiative fulfils one request.

- **start** (event): a stage begins.
- **end** (event): a session stops.
- **take** (event): `work run` takes an initiative through its transitions. Forms: takes, taken.
- **interleave** (event): `work run` runs initiatives side by side.
- **give** (event): Forms: gives, given.
- **refuse** (event): Forms: refuses, refused.

- **spec lock** (resource, exclusive): held by every integrate round.
- **worker slot** (resource, counted by `workers`): held by every worker.
