---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-readiness-bar-checks-an-item-s-lines-not-the-adapter-contract-s-annotations
summary: "work ready leaves spec annotate and v_a5/v_a6 to spec check and the batch's tests, so the bar reads the model facts once."
date: 2026-11-21
status: accepted
tier: judgement
---

# 0112. The readiness bar checks an item's lines, not the adapter contract's annotations

## Decision

The readiness bar (work ready) checks that an item's lines are well-formed on a copy of spec/: lexicon, grammar 4, spec check's rules on the item's groups and requirements, spec logic's L0 and L1 and features generate. It does not run spec annotate, and it does not compare v_a5 or v_a6 (a governing requirement missing from or stale in an adapter contract): those are the contract's state, written by spec annotate when the batch lays the lines and checked by spec check and the batch's tests. Nor does it run the entailment check (L8), which refuses nothing. The bar's time is the person's waiting time; what it checks is what the item's lines can break.
