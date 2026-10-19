---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/delivery-on-v3-work-queue
kind: capability-proposal
part_of: initiative/i10
status: drafted
date: 2026-10-19
argues: [work-queue]
adds: [work-queue#r1-r24]
changes: []
removes: []
---

# Work queue: a new capability

What the gate approves: `work-queue#r1-r24`, a new capability, as written in `capabilities/work-queue.md`.

The design model's work-queue (design-model.md v3, section 3, "Three structures") as a script, `scripts/work`,
over `.shop/work/`: drafting, the queue view, the guards of the lifecycle, claims, rulings and the move log. It
replaces `scripts/plan` (the living slice plan) and, through `work plugin`, `slice_expectations.py`: a scenario of
a work-item not yet claimed is a strict expected failure, as a scenario of a planned slice was, so the suite stays
green between work-items.

Decisions: design-decision/work-item-lifecycle-as-run, design-decision/the-file-set-is-the-claim.

Glossary (`spec/index.md`), added with this proposal:
- **work-item**: the unit of delivery under a capability-proposal, done when the scenarios it accepts or its check pass, moved through its stages by `work run`.
- **file set**: the paths a work-item's work changes, found by its researcher and made final by its planner.
- **claim**: a claimed work-item's hold on its file set, which no other claimed work-item's file set shares.
