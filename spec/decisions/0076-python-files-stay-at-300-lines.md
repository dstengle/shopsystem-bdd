---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/python-files-stay-at-300-lines
summary: "Every tracked Python file stays at 300 lines or fewer, and the suite fails on one over it."
date: 2026-11-05
status: accepted
tier: check
enforced_by: [tests/scripts/test_decision_checks.py::test_every_tracked_python_file_is_300_lines_or_fewer]
source: [record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-design]
by: "workflow simplification plan 6"
---

# 0076. Python files stay at 300 lines

## Decision

Every tracked Python file stays at 300 lines or fewer; `tools size --limit 300` prints each one over it and exits 1,
and the suite fails on it.
