---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/design-model-check-scenarios-1
kind: work-item
part_of: capability-proposal/final-layout-design-model-check
status: drafted
wkind: capability
under: design-model-check
accepts: [design-model-check#r1, design-model-check#r9, design-model-check#r12, design-model-check#r13, design-model-check#r16-r18, design-model-check#r21-r25, design-model-check#r27-r32]
blocked_by: [work-item/pytest-bdd-suite]
fileset: [tests/scenarios/test_design_model_check.py, tests/scripts/test_model.py]
---

# design-model-check's scenarios as pytest-bdd, first half

Goes green: the scenarios of the lines listed, bound by `scenarios("design-model-check.feature")` in
`tests/scenarios/test_design_model_check.py`; the module's other scenarios stay red until
design-model-check-scenarios-2, final-layout-read, rule-labels and deprecated-and-sources bind them.

- Each docstring test of `tests/scripts/test_model.py` binding one of these scenarios becomes step definitions
  and is deleted. The `ModelTest` helpers that build a repository (index, capability, feature, decision, work
  files) become fixtures or plain functions in `tests/scenarios/conftest.py`, so the later work-items reuse
  them; write them for the final layout's paths from the start where a step names no path
  (`spec/decisions/`, `.shop/work/`, `.shop/records/`), and leave the current paths where a scenario names
  them (final-layout-read changes those).
- `BindingTest` stays in `test_model.py` until design-model-check-scenarios-2 removes it.
