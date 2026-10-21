---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/v-s2-one-tag
kind: work-item
part_of: capability-proposal/one-requirement-design-model-check
status: drafted
wkind: capability
under: design-model-check
accepts: [design-model-check#r20, design-model-check#r107]
fileset: [scripts/model, scripts/model.lp, scripts/model_*.py, tests/scripts/test_model.py, tests/scenarios/*design_model_check*.py, features/design-model-check.feature, docs/capability-format.md]
---

# `model check` reports a scenario with more than one `@r<n>` tag

Goes green: design-model-check r20 and r107 as changed: a scenario not tagged `@deprecated` with more than one
`@r<n>` tag, its own and its feature's together, is printed under v_s2 with its plain label (today model.lp's FIX
note says v_s2 is gone, per the superseded decision 0052). docs/capability-format.md's Verifying lists v_s2 once it
is printed.
