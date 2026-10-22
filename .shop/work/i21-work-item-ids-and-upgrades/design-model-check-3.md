---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/design-model-check-3
kind: work-item
part_of: capability-proposal/ids-model-check
status: ready
under: design-model-check
accepts: [design-model-check#r110]
fileset: [scripts/model_work.py, tests/scenarios/design_model_check_problems.py, tests/scenarios/conftest.py, tests/scenarios/design_model_check_then.py]
---

# design-model-check-3

Readings settled by the coordinator under the person's delegation (formulation round f1): a work-item's id for r110 is the `w<n>` of its file name.

## Faults
- its researcher's session ended at its turn limit (error_max_turns, 26 turns, exit code 1); work run takes no outcome from it, whatever its result file says
