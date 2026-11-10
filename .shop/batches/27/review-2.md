---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-27/review-2
kind: review
batch: batch-27
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/39
head: d6f77092cd13b45f716da0b16290fb885932c941
range: 38ac8c84c067c3517d2208b4d4f51d9683f0b7b6..d6f77092cd13b45f716da0b16290fb885932c941
result: fix-now
---

# batch-27 review 2

## Verdict

The fixes close all five earlier findings, and `tools check` is green at Head. One fix leaves the module map wrong: commit 73895478 took the negated-restriction reading out of `spec_entail_rules`, but `CLAUDE.md`'s row for that module still describes it.

## Findings

### f9 Minor fix now: the module map row of spec_entail_rules still describes the negated restrictions the fix removed
- item: b142
- where: CLAUDE.md:81
Commit 73895478 (finding f3) removed the `nattr`/`na0` lines from `Premises.world`. It also removed the `nrel` lines from `Premises.world` and `Premises.rule`, and the "a premise with a `nrel` over a kind forces nothing" guard. It rewrote the module docstring to say only "an `each` object is an `every` one". It did not touch `CLAUDE.md`, and the module map is binding. At Head, the row for `scripts/spec_entail_rules.py` still says:
```
codified-1 and codified-2 facts read alike (`each` an `every`, a negated restriction a stated negation, a negated relation over a kind forcing nothing)
```
A search of the batch's tree finds no `nattr` and no object `nrel` anywhere in `scripts/` or `grammar/` now. The only `nrel` left is the condition-side `crel` negation, which existed before. So the row describes behaviour the module no longer has. Commit c4a4acbf updated the rows of `spec_lf_facts`, `spec_logic_vocab` and `grammar/` for the same removal, but not this one. Fix: in `CLAUDE.md`, cut the row's parenthesis to "(`each` an `every`)", on b142's branch.

## Earlier findings
- f1: fixed
- f2: fixed
- f3: fixed
- f4: fixed
- f5: fixed
