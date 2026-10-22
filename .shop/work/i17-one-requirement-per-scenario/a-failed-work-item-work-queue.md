---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/a-failed-work-item-work-queue
kind: capability-proposal
part_of: initiative/i17
status: formulated
date: 2026-10-22
argues: [work-queue]
adds: [work-queue#r8]
source: [design-decision/a-failed-work-item]
---

# work-queue: a failed work-item retried

The fault design of 0.22.0 (decision 0056): a fault outside a work-item's work transitions it to `failed`, its work
kept, and `work retry` returns it. These lines were committed in cd42cd6 with the glossary entry **failed** and
0056, with no capability-proposal; recorded here so that `model why` traces them (0.22.0 final review, I1).
