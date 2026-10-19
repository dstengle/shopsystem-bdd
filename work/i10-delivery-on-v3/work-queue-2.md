---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/work-queue-2
kind: work-item
part_of: capability-proposal/delivery-on-v3-work-queue
status: drafted
wkind: capability
under: work-queue
accepts: [work-queue#r9-r12, work-queue#r16]
blocked_by: [work-item/work-queue-1]
risk: concurrency
---

# work-queue-2

## Observable
A planned work-item becomes ready only when its blockers are green and no claimed item shares a path; `work claim`
and `work withdraw` work and refuse as the lines say.

## Unknown
How paths are compared for overlap (normalised relative paths; a directory claimed as a prefix of the paths under it, or not).

## What goes green
work-queue#r9-r12, r16.

## Files, roughly
`scripts/workqueue.py` (guards), `scripts/work` (claim, withdraw), their step definitions.
