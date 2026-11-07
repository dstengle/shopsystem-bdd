---
id: bounded-context/example.org/fixture/logic-cluster
title: The logic check's cluster fixture
language: codified-1
---

# The logic check's cluster fixture

The spike's cluster (supervision r20, r59, r66 and r95, `.shop/scratch/spike-cnl/cluster.ears`) rewritten in the
codified language, for the tests of `model logic` (`scripts/spec_solve.py`). It is not this repository's spec.

## Glossary

- **the person** (actor): the human who runs the tools.
- **`work run`** (actor): the supervisor that starts stages and rounds. Kind of: agent.
- **`work`** (actor): the command that writes statuses. Kind of: agent.
- **initiative** (kind): the delivery of one request's accepted lines. Kind of: thing.
- **status** (attribute of initiative): Values: `proposed`, `started`, `done`, `abandoned`.
  Transitions: `proposed` → `started`: `work start`; `started` → `abandoned`: `work abandon`; `started` → `done`: complete.
- **open** (condition of initiative): An initiative is open when the initiative is not `done` and the initiative is not `abandoned`.
- **request** (kind): what brings work into the context.
- **status** (attribute of request): Values: `open`, `accepted`, `delivered`, `awaiting-asker`, `awaiting-upstream`.
  Transitions: `open` → `accepted`: accept; `accepted` → `delivered`: deliver; `awaiting-asker` → `awaiting-upstream`:
  turn; `awaiting-upstream` → `awaiting-asker`: turn.
- **stage** (kind): one session `work run` starts for an initiative. Kind of: session.
- **stage kind** (attribute of stage): Values: research, plan, implement.
- **status** (attribute of stage): Values: `waiting`, `running`, `ended`.
  Transitions: `waiting` → `running`: start; `running` → `ended`: end.
- **round** (kind): a session of the kinds integrate, apply or formulate. Kind of: session.
- **round kind** (attribute of round): Values: integrate, apply, formulate.
- **question** (kind): an open point.
- **work-item** (kind): one unit of delivery.
- **status** (attribute of work-item): Values: `drafted`, `ready`, `awaiting-answer`.
- **result** (kind): what a session ends a stage with. Kind of: thing.
- **thing** (kind): anything a requirement names.
- **outputless** (condition of result): A result is outputless when the result gives no question.
- **session** (kind): a run of a worker. Kind of: agent.
- **agent** (kind): a session or a tool, as the one that does what a verb says.
- **resource** (kind): what a session holds while it runs.
- **free** (condition of resource): a resource no running session holds.
- **start** (event): a stage or a round begins. Frame: agent starts session.
- **end** (event): a stage or a round stops. Frame: agent ends session.
- **ask** (event): Forms: asks, asked. Frame: agent asks question.
- **take** (event): Forms: takes, taken. Frame: `work run` takes thing.
- **write** (event): Forms: writes, written. Frame: agent writes question.
- **spec lock** (resource, exclusive): held by every integrate, apply and formulate round.
- **initiative lock** (resource, exclusive): held by every round of an initiative.
- **worker slot** (resource, counted by `workers`): held by every research stage.

## Relations

| from | word | to |
|---|---|---|
| stage | for | initiative |
| round | for | initiative |
| stage | needs | resource |
| stage | for | work-item |
| stage | with | result |
| question | on | work-item |
| result | gives | question |
