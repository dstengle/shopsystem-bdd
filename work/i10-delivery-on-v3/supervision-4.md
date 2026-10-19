---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/supervision-4
kind: work-item
part_of: capability-proposal/delivery-on-v3-supervision
status: drafted
wkind: capability
under: supervision
accepts: [supervision#r19, supervision#r20]
blocked_by: [work-item/supervision-3]
risk: none
---

# supervision-4

## Observable
A worker is ended at its role's time or spending limit, and the run stops starting workers at its budget and exits 4.

## Unknown
Whether `--max-budget-usd` ends a session cleanly enough to leave its `session.json`, or the supervisor must read
the cost from the transcript.

## What goes green
supervision#r19, r20.

## Files, roughly
`scripts/supervise.py`, the `[limits]` table, step definitions.

## Notes
Driven with `$SHOPSYSTEM_WORK_CLAUDE` pointing at `tests/scripts/stub_claude.py` (from supervision-1), so no model runs.
