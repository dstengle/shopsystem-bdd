---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/feature-file-tools-scenarios
kind: work-item
part_of: capability-proposal/final-layout-feature-file-tools
status: green
wkind: capability
under: feature-file-tools
accepts: [feature-file-tools#r1-r2, feature-file-tools#r4-r5, feature-file-tools#r7, feature-file-tools#r12-r14, feature-file-tools#r16-r17, feature-file-tools#r25-r26, feature-file-tools#r28-r29, feature-file-tools#r35, feature-file-tools#r46, feature-file-tools#r51-r52, feature-file-tools#r56]
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

Accepts re-synced 2026-10-19 to the EARS lines (initiative/i13): feature-file-tools#r3 -> r2; feature-file-tools#r6 -> r5; feature-file-tools#r10 -> r35; feature-file-tools#r11 -> r46; feature-file-tools#r15 -> r46; feature-file-tools#r18 -> r17; feature-file-tools#r27 -> r46; feature-file-tools#r36 -> r46; feature-file-tools#r37 -> r17; feature-file-tools#r38 -> r5; feature-file-tools#r41 -> r29; feature-file-tools#r42 -> r29; feature-file-tools#r53 -> r35; feature-file-tools#r54 -> r35; feature-file-tools#r55 -> r35.
