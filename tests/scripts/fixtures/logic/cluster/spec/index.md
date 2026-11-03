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
- **`work run`** (actor): the supervisor that starts stages and rounds.
- **`work`** (actor): the command that writes statuses.
- **initiative** (kind): the delivery of one request's accepted lines.
- **status** (attribute of initiative): Values: `proposed`, `started`, `done`, `abandoned`.
  Transitions: `proposed` → `started`: `work start`; `started` → `abandoned`: `work abandon`; `started` → `done`: complete.
- **open** (condition of initiative): Means: its status is not `done` and not `abandoned`.
- **request** (kind): what brings work into the context.
- **status** (attribute of request): Values: `open`, `accepted`, `delivered`, `awaiting-asker`, `awaiting-upstream`.
  Transitions: `open` → `accepted`: accept; `accepted` → `delivered`: deliver; `awaiting-asker` → `awaiting-upstream`:
  turn; `awaiting-upstream` → `awaiting-asker`: turn.
- **stage** (kind): one session `work run` starts for an initiative.
- **stage kind** (attribute of stage): Values: research, plan, implement.
- **status** (attribute of stage): Values: `waiting`, `running`, `ended`.
  Transitions: `waiting` → `running`: start; `running` → `ended`: end.
- **round** (kind): a session of the kinds integrate, apply or formulate.
- **round kind** (attribute of round): Values: integrate, apply, formulate.
- **question** (kind): an open point.
- **resource** (kind): what a session holds while it runs.
- **free** (condition of resource): Means: no session holds it.
- **for** (relation stage → initiative): the initiative a stage runs.
- **for** (relation round → initiative): the initiative a round runs.
- **needs** (relation stage → resource): what a stage must hold to start.
- **start** (event): a stage or a round begins.
- **end** (event): a stage or a round stops.
- **take** (event): Forms: takes, taken.
- **write** (event): Forms: writes, written.
- **spec lock** (resource, exclusive): held by every integrate, apply and formulate round.
- **initiative lock** (resource, exclusive): held by every round of an initiative.
- **worker slot** (resource, counted by `workers`): held by every research stage.
