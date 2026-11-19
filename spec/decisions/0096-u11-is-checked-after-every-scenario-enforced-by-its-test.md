---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/u11-is-checked-after-every-scenario-enforced-by-its-test
summary: "U11 (a tool that refuses a command exits with an error naming the reason and changes nothing) is verified by the check that runs after every generated scenario, enforced by the test of that check."
date: 2026-11-16
status: superseded
tier: check
enforced_by: [tests/scripts/test_features_vocab.py::test_the_u11_and_u8_checks_after_a_scenario]
verified_by: [check]
rests_on: [U12]
supersedes: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/u11-is-checked-after-every-scenario]
by: "the session for b179, 2026-11-16"
---

# 0096. U11 is checked after every scenario, enforced by its test

## Context

Decision 0088 named tests/scenarios/vocab.py as its enforcing test; that file holds the checks, not tests, so `model decisions --check` ran it and pytest exited 5 (b179, b224).

## Decision

U11 is verified by the check tests/scenarios/vocab.py runs after every generated scenario whose command is refused: it exited with an error and the repository is unchanged. No scenario states it again. The check itself is enforced by tests/scripts/test_features_vocab.py::test_the_u11_and_u8_checks_after_a_scenario.
