---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/move-to-inside-dir
kind: work-item
part_of: capability-proposal/release-gate-feature-file-tools
status: drafted
wkind: capability
under: feature-file-tools
accepts: [feature-file-tools#r35]
fileset: [scripts/features, scripts/features_edit.py, features/feature-file-tools.feature, tests/scenarios/feature_file_tools_*.py]
---

# `features move --to` outside `--dir` refused

Goes green: feature-file-tools r35 as changed: `--to` naming a file outside `--dir` is refused, naming the file, and no file changes. For after the 0.21.0 release.
