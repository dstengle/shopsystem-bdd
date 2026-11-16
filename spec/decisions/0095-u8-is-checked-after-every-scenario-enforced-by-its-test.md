---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/u8-is-checked-after-every-scenario-enforced-by-its-test
summary: "U8 (where --json is given, a tool prints one JSON object) is verified by the check that runs after every generated scenario, enforced by the test of that check."
date: 2026-11-16
status: accepted
tier: check
enforced_by: [tests/scripts/test_features_vocab.py::test_the_u11_and_u8_checks_after_a_scenario]
verified_by: [check]
rests_on: [U16]
supersedes: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/u8-is-checked-after-every-scenario]
by: "the session for b179, 2026-11-16"
---

# 0095. U8 is checked after every scenario, enforced by its test

## Context

Decision 0087 named tests/scenarios/vocab.py as its enforcing test; that file holds the checks, not tests, so `model decisions --check` ran it and pytest exited 5 (b179, b224).

## Decision

U8 is verified by the check tests/scenarios/vocab.py runs after every generated scenario whose command is given --json: the output is one JSON object. No scenario states it again. The check itself is enforced by tests/scripts/test_features_vocab.py::test_the_u11_and_u8_checks_after_a_scenario.
