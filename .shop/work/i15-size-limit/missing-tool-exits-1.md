---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/missing-tool-exits-1
kind: work-item
part_of: capability-proposal/release-gate-analysis-tools
status: green
wkind: capability
under: analysis-tools
accepts: [analysis-tools#r17]
fileset: [scripts/tools, scripts/tools_check.py, scripts/tools_env.py, features/analysis-tools.feature, tests/scenarios/analysis_tools_*.py]
---

# A missing tool named and `tools` exiting 1

Goes green: analysis-tools r17 as changed: a tool that `tools check`, `tests-of`, `untested` or `refs` needs and that is missing is named as missing, and `tools` exits 1 (today `tools check` exits 0 with every tool missing). For after the 0.21.0 release.
