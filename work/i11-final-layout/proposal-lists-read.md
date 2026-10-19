---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/proposal-lists-read
kind: work-item
part_of: capability-proposal/final-layout-design-model-check
status: drafted
wkind: capability
under: design-model-check
accepts: [design-model-check#r23, design-model-check#r66]
blocked_by: [work-item/design-model-check-scenarios-2]
fileset: [scripts/model, tests/scenarios/test_design_model_check.py]
---

# Terms in a proposal's lists, and a merged removal resolved

Goes green: r23's and r66's scenarios, and `model check` on this repository reports no unresolved entry for
final-layout-design-model-check's `removes: [design-model-check#r45]` or final-layout-feature-file-tools's
`term/` entries once they are merged.

- `read_part`, for a capability-proposal: an entry of `adds`, `changes` or `removes` written `term/<term>`
  (or in full) is qualified and resolved against the glossary's term nodes, not passed to `resolve_req`;
  one the glossary lacks is unresolved, unless the list is `removes` and the proposal's status is `merged`
  or `formulated`. No fact is written for it (grammar.md has no relation for a proposal and a term).
- A `removes` entry naming an id its capability lists as retired, in a `merged` or `formulated` proposal,
  writes the `removes` fact and is not unresolved; in any other status it is unresolved as today.
