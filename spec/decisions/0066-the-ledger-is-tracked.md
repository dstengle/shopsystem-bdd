---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-ledger-is-tracked
summary: "Each initiative's ledger is `.shop/work/<initiative>/ledger.md`, tracked and archived with the initiative, and `delivering-an-initiative` and `initiative-round` write it with `work note`."
date: 2026-10-23
status: accepted
source: [observation/2026-10-23-decision-0030-misread, observation/2026-10-21-session-keeps-the-gate, design-decision/the-session-keeps-the-gate]
by: "the coordinator, 2026-10-24, under the person's delegation (\"Please get everying delivered. Do not stop to ask me questions or permission.\"), on the design note 2026-10-23-requests-and-the-context-loop-design, R2, which the person approved 2026-10-23"
---

# 0066. The ledger is tracked

## Decision

Each initiative keeps one ledger, `.shop/work/<initiative>/ledger.md`, one line an event, tracked and archived with
the initiative. `delivering-an-initiative` and `initiative-round` write it with `work note`. This replaces the
ledger sentence of design-decision/the-session-keeps-the-gate; the rest of that decision stands.
