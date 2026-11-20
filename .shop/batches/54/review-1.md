---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-54/review-1
kind: review
batch: batch-54
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/78
head: a036ba6fa0a58c0d2a00cae2546f8c56f72c780d
range: e2409376f10814ce88f9e249cb34ca7c5b80bd5e..a036ba6fa0a58c0d2a00cae2546f8c56f72c780d
result: clean
---

# batch-54 review 1

## Verdict

The batch builds both in-batch items. b423's upgrade rewrites a scenario conftest of the old form and commits it (upgrades#r36). It names a conftest of neither form and leaves it unchanged (upgrades#r37). b421's `owner` now accepts an indexical owner, and the While-part owner is now tested (scenarios#r34, scenarios#r35). No requirement line is built wrong, no test was removed or weakened, every run exits 0 as it did at the base, and the change is under the size limit. There are two observations and nothing to fix now.

## Findings

### f1 Minor observation: check.lp's candidate pairing was rewritten, and no line of the batch asks for it
- item: b421
- where: grammar/check.lp:86
Commits dbd3f6d11 (b421) and 0c54a7829 (b423) replace `tdem`/`tkey`/`tc` with versions that carry the kind of the response's object (`ko`, `keyo`, `do`, `dfree`, `tcd`). They now pair two lines on one trigger only when their keys' objects are of compatible kinds. The commit message gives the reason as performance: the new scenarios lines grounded 960k rules in 5.5 s on the scaled spec. No line of scenarios or upgrades asks for this, but it changes `spec logic`'s candidate pairs.

The risk is a lost pair, and so a lost L1. I read `grammar/check.lp` to check it:
- Every `dem` rule (lines 71-84) has a `do` or `dfree` copy (lines 97-104).
- The demands that need no shared object (exit_ok/exit_error, an outcome's `oclash`, change nothing) are `dfree` and pair with `any`.
- `term/2` (lines 41-46) covers every object of a `resp`, `set`, `uses`, `nouse`, `only`, `ordx` and `count`, so `ko` always gives a key either `k(K)` or `any`.

So no key loses its object's kind, and a pair is dropped only where `kin` and the unification could never make the two objects one thing. The new test covers only the pos/neg case (`test_responses_on_things_of_disjoint_kinds_are_never_paired`). The `at(T,V)`, `ord` and `cnt` keys with kinds have no test. Consider a case for a `set` clash across kinds, and one across compatible sub-kinds, to pin the `compat` branch of `tcd`.

### f2 Minor observation: one commit is duplicated on both items' branches
- item: -
- where: -
dbd3f6d11 (Item: b421) and 0c54a7829 (Item: b423) have the same subject, message and patch: check.lp, its CLAUDE.md row and test_check_lp.py. The b423 copy carries a comment and a module-map row that cite b421. The merge settles to one copy, so nothing is wrong in `change.diff`. But the b423 copy contributes no b423 behaviour, and so b423's history is not its own change alone. Reproduction: compare commits/dbd3f6d11.patch with commits/0c54a7829.patch; they are the same apart from their `Item:` trailer.
