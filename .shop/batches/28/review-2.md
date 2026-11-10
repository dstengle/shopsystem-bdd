---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-28/review-2
kind: review
batch: batch-28
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/40
head: 31a49d5acc8a13d00a9a5a2d1622e4b4a68a2adc
range: e4fffd5ee3e75b3e864b5821e3c35f9c4d738e17..31a49d5acc8a13d00a9a5a2d1622e4b4a68a2adc
result: clean
---

# batch-28 review 2

## Verdict

All three earlier findings are fixed. "the newest K" is gone from the grammar and the logical form. `check.lp` no longer reads time or necessity, and none of it remains in the tree. `model logic` now refuses a comparison or a history, naming it. A necessity puts no pair out. The four check runs that pass at the base pass at `Head:`. `model decisions --check` exits 1, as it does at the base. Two observations, neither holding the merge.

## Findings

### f8 Minor observation: a timed line now stops `features generate` and the readiness bar
- item: b147
- where: scripts/features_generate.py:51
The risk was that refusing the time atoms in spec_lf_facts reaches past `model logic`. I checked that `model parse` is safe. `scripts/model` parses codified-2 lines through spec_grammar4 and spec_lf, and the only caller of `spec_lf_facts` is `spec_context`. But `spec_context.load` puts each refused line in `ctx.refused`, and `features_generate.py:51-52` raises `GenerateError` for any line in it:
```
if ident in ctx.refused:
    raise GenerateError("%s: %s" % (ident, ctx.refused[ident]))
```
The readiness bar runs `features generate`. So once a codified-2 consumer writes a line with "after", "before", "within the last" or "has V-ed", that line parses under r138–r141. But `features generate` then stops on it with "no translation of a comparison of moments", and `work ready` refuses any item carrying it. The base never parsed such a line, so nothing that worked before breaks. This is what the refusal option of f2 costs. It is recorded so that the item giving `model logic` a reading of time also covers `features generate`.

### f9 Minor observation: a necessity is read silently while a time line is refused
- item: b148
- where: scripts/spec_lf_modal.py:24
After the fix, `necessity` emits only `form(R,nec)` and `cnl4(R)` and never refuses anything. A line like "While a stage is `done`, a session never follows the stage." used to be refused with "no translation of a necessity under …". Now `model logic` accepts it and reports nothing (`test_a_necessity_under_while_is_not_refused`). The time constructs, fixed the other way in the same review, are refused by name. A person running `model logic` cannot tell that the check ignored their "always"/"never" line. Both choices meet the finding, but they differ. A follow-up item could make a necessity's absence from the check visible, by a refusal or a note, the same way for both constructs.

## Earlier findings
- f1: fixed
- f2: fixed
- f3: fixed
