---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/withdrawn-accepts-not-reported
kind: work-item
part_of: capability-proposal/release-gate-design-model-check
status: drafted
wkind: capability
under: design-model-check
accepts: [design-model-check#r27]
fileset: [scripts/model.lp, scripts/model_check.py, scripts/model_work.py, features/design-model-check.feature, tests/scenarios/design_model_check_*.py]
---

# A withdrawn work-item's accepts not a file problem

Goes green: design-model-check r27's row as changed: only a work-item that is not `withdrawn` is reported for accepting a requirement no scenario names yet (most of the 168 file problems are withdrawn items, which r36 counts as closed). For after the 0.21.0 release.
