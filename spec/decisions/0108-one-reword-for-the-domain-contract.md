---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/one-reword-for-the-domain-contract
summary: "Every live line moved by the domain contract got a new id in its new capability, the old ids retired with a Moved entry; no exemption from requirements-retired-never-edited."
date: 2026-11-19
status: accepted
tier: judgement
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/requirements-retired-never-edited]
---

# 0108. One reword for the domain contract

## Decision

The domain contract reworded every live requirement into request words and moved it to one of 22 capabilities by service and object lifecycle; each moved line has a new id there, and the old ids retire with a ## Moved entry and spec/moves.json. No line was edited in place: requirements-retired-never-edited holds without exemption.
