---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/feature-file-tools-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-feature-file-tools
status: withdrawn
wkind: capability
under: feature-file-tools
accepts: [feature-file-tools#r11, feature-file-tools#r21, feature-file-tools#r40]
blocked_by: [work-item/work-queue-4, work-item/every-scenario-bound]
risk: none
---

# feature-file-tools-1

## Observable
`features` knows no slice: `tag` takes only `r<n>`, `holding` reports no slice tag, and `features plugin` and
`slice_expectations.py` are gone.

## Unknown
none

## What goes green
feature-file-tools#r11, r21, r40. Removed with their tests and scenarios: `features plugin` (r30, r43-r45),
`scripts/slice_expectations.py` (r31-r34, r47-r50), slice tags in `tag` (r8, r9).

## Files, roughly
`scripts/features`, delete `scripts/slice_expectations.py`, `tests/scripts/test_features.py` (the plugin and slice
tests go), the feature-file-tools step definitions.

Withdrawn 2026-10-19: deferred until the skeleton runs (initiative notes)
