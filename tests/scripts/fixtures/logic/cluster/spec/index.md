---
id: bounded-context/example.org/fixture/logic-cluster
title: The logic check's cluster fixture
language: codified-2
imports: [cli]
---

# The logic check's cluster fixture

The spike's cluster (supervision r20, r59, r66 and r95, `.shop/scratch/spike-cnl/cluster.ears`) written in grammar 4,
for the tests of `model logic` (`scripts/spec_solve.py`). It is not this repository's spec.

## Glossary

- **the person** (proper noun): the human who runs the tools. Kind of: agent.
- **`work`** (proper noun): the command that writes statuses. Kind of: tool.
- **initiative** (noun): the delivery of one request's accepted lines.
- **status** (attribute of initiative): Values: `proposed`, `started`, `done`, `abandoned`.
  Transitions: `proposed` → `started`: `work start`; `started` → `abandoned`: `work abandon`; `started` → `done`: complete.
- **open** (adjective of initiative): An initiative is open when the initiative is not `done` and the initiative is not `abandoned`.
- **request** (noun): what brings work into the context.
- **status** (attribute of request): Values: `open`, `accepted`, `delivered`, `awaiting-asker`, `awaiting-upstream`.
  Transitions: `open` → `accepted`: accept; `accepted` → `delivered`: deliver; `awaiting-asker` → `awaiting-upstream`:
  turn; `awaiting-upstream` → `awaiting-asker`: turn.
- **stage** (noun): one session `work` starts for an initiative. Kind of: session.
- **status** (attribute of stage): Values: `waiting`, `running`, `ended`.
  Transitions: `waiting` → `running`: start; `running` → `ended`: end.
- **question** (noun): an open point.
- **result** (noun): what a session ends a stage with.
- **outputless** (adjective of result): A result is outputless when no question is on the result.
- **session** (noun): a run of a worker. Kind of: agent.
- **start** (verb, action): an agent begins a stage. Frame: agent starts stage.
- **end** (verb, action): an agent stops a stage. Frame: agent ends stage.
- **take** (verb, action): Forms: takes, taken. Frame: tool takes initiative.
- **write** (verb, action): Forms: writes, written. Frame: agent writes question.

## Relations

| from | word | to |
|---|---|---|
| stage | for | initiative |
| result | of | stage |
| question | on | result |
