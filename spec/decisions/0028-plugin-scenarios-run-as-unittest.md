---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/plugin-scenarios-run-as-unittest
summary: "In this repository a scenario's step definition is a unittest test whose docstring is the scenario's title, and a test checks every scenario has one."
date: 2026-10-15
status: rejected
revisit_when: "a capability's scenarios need Given/When/Then steps shared across tests"
revisit_signal: requests
source: [design-decision/scripts-stdlib-only]
by: "docs/design-model/design-model.md v3 section 2 (step definitions are code, outside the model)"
---

# 0028. Plugin scenarios run as unittest

## Decision

A feature file in this repository contains the acceptance-scenarios of one capability, each tagged `@r<n>`. The test that executes a scenario is a `unittest` test under `tests/scripts/` whose docstring is the scenario's title. For each feature file, one test fails when a scenario has no such test.

## Context

v3 makes feature files containers and step definitions code outside the model. The plugin's tests are standard-library `unittest`, run with `python3 -m unittest discover -s tests/scripts`; pytest-bdd would be a dependency for the plugin's own suite.

## Alternatives

pytest-bdd as a development dependency of this repository only; no feature files, with requirement ids in test names.

## Consequences

Only `design-model-check` is formulated this way so far. The workflow capabilities (spec-integration, formulation, slicing, red-green, review, code-research, batch-analysis) are behaviour of agents, not scripts: how their scenarios run is an open question in initiative i1.
