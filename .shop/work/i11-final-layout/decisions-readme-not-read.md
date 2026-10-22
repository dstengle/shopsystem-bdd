---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/decisions-readme-not-read
kind: work-item
part_of: capability-proposal/release-gate-design-model-check
status: green
wkind: capability
under: design-model-check
accepts: [design-model-check#r19]
fileset: [scripts/model_parse.py, features/design-model-check.feature, tests/scenarios/design_model_check_*.py]
---

# spec/decisions/README.md not read as a decision

Goes green: design-model-check r19 as changed: `model` reads every `spec/decisions/*.md` but `index.md` and `README.md`, so the README that migrate leaves is not reported as a decision with no id. For after the 0.21.0 release.
