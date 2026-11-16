---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/u4-is-checked-after-every-scenario-enforced-by-its-test
summary: "U4 (work commits every transition and pushes the commit) is verified by the check that runs after every generated scenario, enforced by the test of that check."
date: 2026-11-16
status: accepted
tier: check
enforced_by: [tests/scripts/test_features_vocab.py::test_the_u4_check_after_a_scenario]
verified_by: [check]
rests_on: [U13]
supersedes: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/u4-is-checked-after-every-scenario]
by: "the session for b179, 2026-11-16"
---

# 0094. U4 is checked after every scenario, enforced by its test

## Context

Decision 0086 named tests/scenarios/vocab.py as its enforcing test; that file holds the checks, not tests, so `model decisions --check` ran it and pytest exited 5 (b179, b224).

## Decision

U4 is verified by the check tests/scenarios/vocab.py runs after every generated scenario whose run commits: the commit on the branch checked out is on its remote. No scenario states it again. The check itself is enforced by tests/scripts/test_features_vocab.py::test_the_u4_check_after_a_scenario.
