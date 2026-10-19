---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/design-model-check-scenarios-2
kind: work-item
part_of: capability-proposal/final-layout-design-model-check
status: drafted
wkind: capability
under: design-model-check
accepts: [design-model-check#r36, design-model-check#r38-r41, design-model-check#r43, design-model-check#r46-r50, design-model-check#r55-r58]
blocked_by: [work-item/design-model-check-scenarios-1]
fileset: [tests/scenarios/test_design_model_check.py, tests/scripts/test_model.py]
---

# design-model-check's scenarios as pytest-bdd, second half

Goes green: the scenarios of the lines listed, in the module design-model-check-scenarios-1 made. `BindingTest` and the `binding` import leave `test_model.py`; the unit tests that
bind no scenario stay.
