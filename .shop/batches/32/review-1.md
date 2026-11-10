---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-32/review-1
kind: review
batch: batch-32
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/46
head: 376776586cb544f87a19bcc5486e7d17b4be8fbe
range: a588eb7c558e0b5e8409f3a65a669ae39510748c..376776586cb544f87a19bcc5486e7d17b4be8fbe
result: clean
---

# batch-32 review 1

## Verdict

The batch builds all fifteen of b197's lines. `features generate` now writes steps for every, only, the counts, or, a row of another word, "the T of x", "no K" and a negated restriction. A group of only may, always or never lines gets no scenario and no warning. `model logic` reads every and a count in a condition, and a negated attribute of an object. The module map has rows for `spec_lf_quant`, `spec_steps4_boxes` and `codified2_constructs`. The change is within the size limit at +706 -90, and every run that the batch could affect exits 0. Two tests were rewritten: one kept refusing a negated state and has a new test beside it for the negated attribute, and the other is stricter (stderr must now be empty). Nothing to fix now; three observations.

## Findings

### f1 Minor observation: a negated restriction finds no clash with a value it rules in
- item: b197
- where: grammar/check.lp:251
`gap`/`pag` count a negated restriction (`onattr(B,Y,T,W)`) as entailed only by the same `onattr` on the other side. An `oattr` of another value on that side does not count, even though it implies the negation.
Reproduction from the rules as read:
```
When the person runs `work start`, `work` shall print a stage whose status is `open`.
When the person runs `work start`, `work` shall not print a stage whose status is not `done`.
```
Line A has `oattr(..,t_status,v_open)` and no `onattr`, so `gap` holds, `cl(pos_neg)` is blocked, and no L1 is reported. But an `open` stage is not `done`, so the two lines do clash. This misses a clash (it never reports a false one), and r173's line is met. Hardening would be an extra rule: an `oattr(A,X,T,V)` with `V != W` entails `onattr(B,Y,T,W)`.

### f2 Minor observation: an "at most" count in a condition is read as no condition
- item: b197
- where: scripts/spec_lf_quant.py:497
`count` returns without emitting anything when the count admits no K, so "While at most one stage is `done`, when …" is paired as if it had no While clause. Set it against "While at least three stages are `done`, when the person runs `work start`, `work` shall exit with an error …" (the other side's `ccount` keeps one `done` stage) and an L1 should follow, although no state meets both counts. The docstring says this is intended ("says nothing the check reads"), and no line names this case. If wanted, hardening would keep a `ccount` with its bound for "at most" / "fewer than" and let `#count` set such a pair aside, as `cl(A,B,count)` already does for two counts in responses.

### f3 Minor observation: a may line beside shall lines carries its tag on a scenario that does not test it
- item: b197
- where: scripts/features_generate4.py:276
Modal lines are filtered out of `forms` before the steps are read, but `features_generate.written` still tags the scenario with every requirement of the group (`group.requirements`). In a group with one shall line and one may line, the may line's `@r<n>` tag therefore sits on a scenario whose steps are only the shall line's. That makes the may id look covered by a scenario: `tools map`, and the strict xfail of an `unbuilt:` id, would read it as tested. The item's notes say a may line "gets no scenario", which fits leaving its tag off. No line of the batch names a mixed group, and none of the fixtures has one.
