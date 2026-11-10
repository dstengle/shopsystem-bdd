---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/u11-is-checked-after-every-scenario
summary: "U11 (a tool that refuses a command exits with an error naming the reason and changes nothing) is verified by the check that runs after every generated scenario."
date: 2026-11-10
status: accepted
tier: check
enforced_by: [tests/scenarios/vocab.py]
verified_by: [check]
rests_on: [U11]
by: "the session for b169, 2026-11-10"
---

# 0088. U11 is checked after every scenario

## Decision

U11 is verified by the check tests/scenarios/vocab.py runs after every generated scenario whose command is refused: it exited with an error and the repository is unchanged. No scenario states it again.
