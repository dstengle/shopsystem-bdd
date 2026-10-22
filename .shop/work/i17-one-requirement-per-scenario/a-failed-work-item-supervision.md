---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/a-failed-work-item-supervision
kind: capability-proposal
part_of: initiative/i17
status: merged
date: 2026-10-22
argues: [supervision]
adds: [supervision#r33-r41]
changes: [supervision#r28]
source: [design-decision/a-failed-work-item]
---

# supervision: a failed work-item

The fault design of 0.22.0 (decision 0056): a fault outside a work-item's work transitions it to `failed`, its work
kept, and `work retry` returns it. These lines were committed in cd42cd6 with the glossary entry **failed** and
0056, with no capability-proposal; recorded here so that `model why` traces them (0.22.0 final review, I1).
