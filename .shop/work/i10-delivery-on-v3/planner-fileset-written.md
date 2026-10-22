---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/planner-fileset-written
kind: work-item
part_of: capability-proposal/release-gate-supervision
status: green
wkind: capability
under: supervision
accepts: [supervision#r31]
fileset: [scripts/supervise.py, scripts/workqueue.py, tests/scenarios/test_supervision.py, tests/scenarios/supervision_*.py]
---

# The planner's file set written into the work-item

Goes green: supervision r31 (card r20-fileset, choice A). A planner's `DONE` result with a `fileset` is written into the work-item as `fileset:` as it moves to `planned`, so that r20 can fire in a real run. For after the 0.21.0 release.
