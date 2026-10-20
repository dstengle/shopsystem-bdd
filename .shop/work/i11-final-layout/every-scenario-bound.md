---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/every-scenario-bound
kind: work-item
part_of: capability-proposal/final-layout-feature-file-tools
status: green
wkind: enabling
for: work-item/bindings-unbound
check: "python3 -m pytest passes and includes tests/scripts/test_bound.py; python3 scripts/features bindings --unbound features/analysis-tools.feature features/design-model-check.feature features/feature-file-tools.feature exits 0; no tests/scripts module but test_measure.py imports binding"
blocked_by: [work-item/analysis-tools-scenarios, work-item/deprecate-commands, work-item/bindings-unbound, work-item/final-layout-read, work-item/rule-labels, work-item/deprecated-and-sources]
fileset: [tests/scripts/test_bound.py, tests/scripts/binding.py]
---

# The suite fails when a scenario has no test or two

- `tests/scripts/test_bound.py`, a unittest test: runs `scripts/features --dir features bindings --tests tests
  --unbound` over the feature files of the script capabilities bound by pytest-bdd (analysis-tools,
  design-model-check, feature-file-tools, and migration-tools once i8 adds it) and asserts exit 0, printing
  the report on failure.
- `tests/scripts/binding.py` stays, used only by `test_measure.py`, with a docstring saying i12 removes it.
- `spec/index.md`'s Testing says the same (the text is in `spec-index.md`).
