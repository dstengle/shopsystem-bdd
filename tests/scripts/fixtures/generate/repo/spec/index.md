---
id: bounded-context/example.org/fixture/generate
title: The generation fixture
language: codified-2
imports: [cli]
---

# The generation fixture

A small codified-2 context for the tests of `features generate`, the readiness bar and the batches. It is not this
repository's spec.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| work-item | under | capability-proposal | one |
| capability-proposal | of | initiative | one |
| stage | for | work-item | one |

## Glossary

- **the person** (proper noun): the human who runs the commands. Kind of: agent.
- **`work`** (proper noun): the queue's tool. Kind of: tool.
- **initiative** (noun): the delivery of one request.
- **work-item** (noun): a unit of delivery.
- **capability-proposal** (noun): a proposal of one capability.
- **request** (noun): lines another context proposes.
- **session** (noun): one conversation. Kind of: agent.
- **stage** (noun): one session for a node. Kind of: session.
- **file** (noun): a file of the repository.
- **brief** (noun): the input of a stage.
- **transition** (noun): a change of a status.
- **status** (attribute of initiative): Values: `proposed`, `started`, `done`, `abandoned`.
  Transitions: `proposed` → `started`: `work start`; `started` → `done`: complete; `started` → `abandoned`: `work abandon`.
- **status** (attribute of work-item): Values: `drafted`, `ready`, `done`, `green`, `withdrawn`.
- **start** (verb, action): an agent begins a stage. Frame: agent starts stage.
- **take** (verb, action): `work run` takes an initiative through its transitions. Forms: takes, taken. Frame: agent takes initiative.
- **give** (verb, action): an agent hands a brief to a stage. Forms: gives, given. Frame: agent gives brief to stage.
- **commit** (verb, action): an agent records a thing in the repository. Frame: agent commits thing.
- **fulfil** (verb, state): an initiative delivers a request. Frame: initiative fulfils request.
