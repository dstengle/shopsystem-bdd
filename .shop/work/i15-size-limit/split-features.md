---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/split-features
kind: work-item
part_of: capability-proposal/size-analysis-tools
status: drafted
wkind: enabling
for: work-item/size-check
check: "python3 -m pytest -q passes with the same tests as before, and each named file and every file split from it is under 300 lines"
fileset: [scripts/features, scripts/features_*.py, tests/scripts/test_features.py, tests/scenarios/test_feature_file_tools.py, tests/scenarios/*feature_file_tools*.py]
---

# split-features

Split, with no change of behaviour: scripts/features (657), tests/scenarios/test_feature_file_tools.py (976), tests/scripts/test_features.py (473)
