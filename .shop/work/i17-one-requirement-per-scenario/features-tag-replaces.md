---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/features-tag-replaces
kind: work-item
part_of: capability-proposal/one-requirement-feature-file-tools
status: drafted
wkind: capability
under: feature-file-tools
accepts: [feature-file-tools#r51]
fileset: [scripts/features, scripts/features_edit.py, features/feature-file-tools.feature, tests/scenarios/*feature_file_tools*.py]
---

# `features tag` replaces the scenario's requirement tag

Goes green: feature-file-tools r51 as changed: `features tag <title> r<n>` makes `@r<n>` the scenario's one
requirement tag, in place of any `@r<m>` tag it has, and leaves its other tags and every other line unchanged
(today it adds `@r<n>` beside the others, per the superseded decision 0052).
