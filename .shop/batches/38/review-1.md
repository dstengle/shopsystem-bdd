---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-38/review-1
kind: review
batch: batch-38
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/59
head: fa1e3abbafe3ffe7331d765811fb753186e7ddd1
range: 3ba1e171ffda14e22eae4f3f4ef1a5f492711109..fa1e3abbafe3ffe7331d765811fb753186e7ddd1
result: clean
---

# batch-38 review 1

## Verdict

The batch builds all four items. b297's design-model-check#r314 and #r315 and feature-file-tools#r125 and #r126, b298's #r127, b299's #r128 and b307's readiness#r41 each have their translation or step and a scenario that drives it. No test is removed or weakened: the membership rows of `design_model_check_worlds.py` moved word for word into `design_model_check_worlds_member.py`, at the same place in TABLE. `features generate --check` exits 0. The one run that fails, `model decisions --check`, failed at the base too. The change is 606 lines, under the 1000 limit. Two observations, nothing to fix now.

## Findings

### f1 Minor observation: the module map's readiness_bar.py row does not name r41's refusal
- item: b307
- where: CLAUDE.md:243
`_logic` in `scripts/readiness_bar.py` now refuses an item when `model logic` has no translation of one of its lines or its universal conditions (`spec_solve.unread`, r41). The module docstring says so; the module-map row still reads only:
```
`model logic` finds no L0 nor an L1 naming them
```
The map is binding, and this row is the one a reader takes as the bar's contract. Fix: add ", and reads each of them (r41)" to the row.

Related: the `scripts/spec_steps4_boxes.py` row does not mention the two new Thens on a response's object, "holds nothing" (b297) and "holds no K" (b299). They appear only in the `spec_lf_member.py` row.

### f2 Minor observation: order-by-every still assumes a frame slot that takes `thing`
- item: b298
- where: scripts/spec_lf_ordered.py:144
`said` now walks `r.vocab.ancestors(x.kind)` only when `arg` is callable. Only `then` (order-by) passes a callable. The order-by-every path (line 178) still passes a fixed `k_thing_Arg` tree, so the loop tries only the slot `"thing"`. A requirement like "`work` shall return every worktree, ordered by version, in descending order to the person", with a `return` whose one frame names `worktree`, still raises `TraceError("no step of an order of worktree there")`. No line names this case: r127 covers `order-by` only. Hardening: build order-by-every's argument per slot the same way.
