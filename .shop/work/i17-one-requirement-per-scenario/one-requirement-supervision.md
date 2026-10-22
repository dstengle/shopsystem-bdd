---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/one-requirement-supervision
kind: capability-proposal
part_of: initiative/i17
status: formulated
date: 2026-10-21
argues: [supervision]
adds: [supervision#r32]
changes: [supervision#r9, supervision#r10]
removes: []
---

# supervision: work run exits successfully or with an error

r9 exits successfully when every work-item is `green` or `withdrawn`; the new r32 exits with an error when one is `awaiting-ruling`; r10 exits with an error (design-decision/exits-are-successful-or-errors). Implementation keeps the codes 0, 3 and 1. Approved by the person, 2026-10-21.
