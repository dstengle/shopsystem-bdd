---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/feature-file-tools-scenarios
kind: work-item
part_of: capability-proposal/final-layout-feature-file-tools
status: drafted
wkind: capability
under: feature-file-tools
accepts: [feature-file-tools#r1-r7, feature-file-tools#r10-r18, feature-file-tools#r25-r29, feature-file-tools#r36-r38, feature-file-tools#r41, feature-file-tools#r42, feature-file-tools#r46, feature-file-tools#r51-r56]
blocked_by: [work-item/pytest-bdd-suite]
fileset: [tests/scenarios/test_feature_file_tools.py, tests/scripts/test_features.py]
---

# feature-file-tools' unchanged scenarios as pytest-bdd

Goes green: the scenarios of `features/feature-file-tools.feature` for every line whose behaviour this
proposal does not change, bound by `scenarios("feature-file-tools.feature")` in
`tests/scenarios/test_feature_file_tools.py`. The deprecate scenarios (r19-r24, r35, r39, r40) and the
bindings ones (r57-r59) are formulated already and stay red here: they are work-item/deprecate-commands and
work-item/bindings-unbound. Mark nothing xfail; the work-item is done when only those are red.

- As for analysis-tools: each docstring test in `tests/scripts/test_features.py` that binds a scenario becomes
  step definitions and is deleted; `BindingTest` goes; other unit tests stay.
- The lines i10 retires (slice tags, `slice_expectations.py`) are not converted if i10 has removed them by
  the time this starts; convert whatever the feature file has.
- No change to `scripts/features` here.
