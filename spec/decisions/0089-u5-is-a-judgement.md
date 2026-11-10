---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/u5-is-a-judgement
summary: "U5 (a session shall not write a status) is verified by judgement: the implementer and the reviewer."
date: 2026-11-10
status: accepted
tier: judgement
verified_by: [judgement]
rests_on: [U5]
by: "the session for b169, 2026-11-10"
---

# 0089. U5 is a judgement

## Decision

U5 is verified by judgement: no scenario can show that no session ever writes a status, so it is put before every batch task's implementer and the pull request's reviewer; only work's commands write a status.
