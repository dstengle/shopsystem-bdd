---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/records-are-kept-never-cited
summary: "Records are a store of reports and research kept beside the specification; no item, request or decision of the current system cites one."
date: 2026-11-19
status: accepted
tier: check
enforced_by: [tests/scripts/test_records_policy.py]
---

# 0106. Records are kept, never cited

## Decision

A record (.shop/records/) is a report or research kept and indexed, never referenced by the current system: an item's provenance cites only quotes, requests and decisions, never a record (v_r1, a violation on a new item and a warning on an existing one). A record a live artifact must stand on is restated as a decision.
