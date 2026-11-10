---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/u8-is-checked-after-every-scenario
summary: "U8 (where --json is given, a tool prints one JSON object) is verified by the check that runs after every generated scenario."
date: 2026-11-10
status: accepted
tier: check
enforced_by: [tests/scenarios/vocab.py]
verified_by: [check]
rests_on: [U8]
by: "the session for b169, 2026-11-10"
---

# 0087. U8 is checked after every scenario

## Decision

U8 is verified by the check tests/scenarios/vocab.py runs after every generated scenario whose command is given --json: the output is one JSON object. No scenario states it again.
