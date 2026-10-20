---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/design-model-check-scenarios-2
kind: work-item
part_of: capability-proposal/final-layout-design-model-check
status: drafted
wkind: capability
under: design-model-check
accepts: [design-model-check#r12, design-model-check#r14, design-model-check#r16-r17, design-model-check#r24, design-model-check#r36, design-model-check#r43, design-model-check#r46, design-model-check#r48-r49, design-model-check#r55, design-model-check#r105]
blocked_by: [work-item/design-model-check-scenarios-1]
fileset: [tests/scenarios/test_design_model_check.py, tests/scripts/test_model.py]
---

# design-model-check's scenarios as pytest-bdd, second half

Goes green: the scenarios of the lines listed, in the module design-model-check-scenarios-1 made. `BindingTest` and the `binding` import leave `test_model.py`; the unit tests that
bind no scenario stay.

Accepts re-synced 2026-10-19 to the EARS lines (initiative/i13): design-model-check#r38 -> r14; design-model-check#r39 -> r105; design-model-check#r40 -> r16; design-model-check#r41 -> r16, r17; design-model-check#r47 -> r24; design-model-check#r50 -> r48; design-model-check#r56 -> r55; design-model-check#r57 -> r12; design-model-check#r58 -> r36.
