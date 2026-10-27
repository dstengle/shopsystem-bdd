---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/requests-kept-behind-one-port
summary: "`work` keeps the carrier of a request behind one port, a file in the upstream's repository and an issue on the upstream's GitHub repository being its first two carriers."
date: 2026-10-27
status: proposed
source: [request/missingmass.io/shopsystem/shopsystem-bdd/q14, initiative/missingmass.io/shopsystem/shopsystem-bdd/i39]
by: "request q14 of product/missingmass.io/subscriptions-viewer, its line 2, accepted at this context's intake"
---

# 0070. Requests are kept behind one port

## Decision

`work` keeps the carrier of a request behind one port. A file in the upstream's repository and an issue on the
upstream's GitHub repository are its first two carriers; each side's commands, refusals and statuses are the same
whichever carrier a request is kept on.
