---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/u17-is-checked-after-every-scenario-enforced-by-its-test
summary: "U17 is verified by the check tests/scenarios/vocab.py runs after every generated scenario: a refused request named a reason and changed nothing."
date: 2026-11-19
status: accepted
tier: check
enforced_by: [tests/scripts/test_vocab_u17.py]
supersedes: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/u11-is-checked-after-every-scenario-enforced-by-its-test]
---

# 0109. U17 is checked after every scenario, enforced by its test

## Decision

U17 is verified by the check tests/scenarios/vocab.py runs after every generated scenario whose request is refused: it named a reason and the repository is unchanged. No scenario states it again. The check itself is enforced by tests/scripts/test_vocab_u17.py.
