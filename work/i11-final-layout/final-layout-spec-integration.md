---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/final-layout-spec-integration
kind: capability-proposal
part_of: initiative/i11
status: approved
date: 2026-10-19
argues: [spec-integration]
adds: [spec-integration#r20-r22]
changes: [spec-integration#r15, spec-integration#r17, spec-integration#r19]
---

# Spec integration: decision files in the light form

A decision is drafted as its own file in `spec/decisions/`, in the light form (design-decision/light-decisions),
its `source` naming ids and its `by` the rest (design-decision/references-are-ids), and the index is
regenerated in the spec commit (r20-r22). r9 says the delegation in `by`, where it said it in the source;
r17 and r19 name `.shop/work/`. Implementation: drafts under `.shop/scratch/drafts/`, no ledger. The
proposed file is `capabilities/spec-integration.md`.

The Not yet entry's trigger named i8, which is now migration only; it is reworded to a consuming
repository asking for it.

Re-synced 2026-10-19 to the EARS lines (initiative/i13, approved by the person): spec-integration#r9 -> r15. The ids in the text above are the drafted ones.
