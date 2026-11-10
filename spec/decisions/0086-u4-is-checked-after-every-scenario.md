---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/u4-is-checked-after-every-scenario
summary: "U4 (work commits every transition and pushes the commit) is verified by the check that runs after every generated scenario."
date: 2026-11-10
status: accepted
tier: check
enforced_by: [tests/scenarios/vocab.py]
verified_by: [check]
rests_on: [U4]
by: "the session for b169, from b119/b129's verification routes, 2026-11-10"
---

# 0086. U4 is checked after every scenario

## Decision

U4 is verified by the check tests/scenarios/vocab.py runs after every generated scenario whose run commits: the commit on the branch checked out is on its remote. No scenario states it again.
