---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/design-model-check-2
kind: work-item
part_of: capability-proposal/delivery-on-v3-design-model-check
status: withdrawn
wkind: capability
under: design-model-check
accepts: [design-model-check#r6, design-model-check#r22-r24, design-model-check#r43, design-model-check#r67]
blocked_by: [work-item/proposal-lists-read]
risk: none
---

# design-model-check-2

## Observable
`model check` reports `<capability>#behaviour/r<n>` as unresolved, checks a work-item's `fixes` and `findings`, and lets a
merged proposal name an id retired after it.

## Unknown
none

## What goes green
design-model-check#r6, r22, r23, r24, r43, r67. v15e in `scripts/model.lp` and the unresolved check of `removes` read the
proposal's status: a merged, formulated or withdrawn proposal may name a retired id. The scenario of the retired r42 is removed by formulation; its code (the
`(?:behaviour/)?` in `scripts/model`'s `REF`) and the `--help` sentence that reads both forms go, and
`docs/capability-format.md`'s sentence on `#behaviour/r<n>` with them. Any reference this repository's own files
write as `#behaviour/r<n>` is rewritten (a search first; none is expected).

## Files, roughly
`scripts/model`, `scripts/model.lp`, `docs/capability-format.md`, the model check step definitions, `tests/scripts/test_model.py`.

## Notes
Needs this repository's scenarios bound as pytest-bdd step definitions and the `.shop/` layout, both from initiative i11; the coordinator links i11's work-item into `blocked_by`.

Withdrawn 2026-10-19: deferred until the skeleton runs (initiative notes)
