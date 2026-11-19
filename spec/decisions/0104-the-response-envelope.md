---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-response-envelope
summary: "Every operation answers with one envelope of outcome, content, errors and notices, its errors naming business references; a failure of the infrastructure is outside the domain. U16 retires into this decision."
date: 2026-11-19
status: accepted
tier: check
enforced_by: [tests/scripts/test_domain_envelope.py]
supersedes: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/u8-is-checked-after-every-scenario-enforced-by-its-test]
---

# 0104. The response envelope

## Decision

Every operation answers with the response envelope: its outcome (done, returned, passed, refused, failed, broken), its content, its errors and its notices; errors name business references (parameter:tier, item:b12), which the adapter spells for its port. A failure of the infrastructure (broken) is outside the domain. The CLI prints the envelope as one JSON object under --json. U16 retires into this decision.
