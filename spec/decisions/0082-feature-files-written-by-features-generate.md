---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/feature-files-written-by-features-generate
summary: "Every feature file is what `features generate` writes from its codified capability; no session or person edits one."
date: 2026-11-05
status: accepted
tier: check
enforced_by: [tests/scripts/test_decision_checks.py::test_the_features_are_what_features_generate_writes]
supersedes: [design-decision/feature-files-read-only-in-red-green]
source: [record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-9]
by: "workflow simplification plan 9, decided by the planner; revisit"
---

# 0082. Feature files are written by `features generate`

## Context

Decision 0006 kept the implementer from editing a feature file during red-green. Since the GF conversion, a feature
file is generated from its capability's groups, and the implementer it named is gone with `work run`. Its check
already held the newer rule.

## Decision

Every feature file under `features/` is what `features generate` writes from its codified capability, byte for byte;
a scenario is changed by changing its group, never the file. `features generate --check` holds it.
