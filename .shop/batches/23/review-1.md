---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-23/review-1
kind: review
batch: batch-23
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/35
head: 67c0b40e66503f63eb1619e5e23a678283503a90
range: f0039c8a8eb44a059a4ae5f4379345051d7c0735..67c0b40e66503f63eb1619e5e23a678283503a90
result: clean
---

# batch-23 review 1

## Verdict

The batch builds both of b166's lines: batches#r19 and readiness#r15. `work batch done` now runs a task's tests with unbuilt xfails non-strict. The task's own ids are still refused first, while they are in `unbuilt:`. `work batch review` still runs strict. The readiness bar now refuses lexicon problems that the item's lines bring and that the spec without them does not have. The refusal names the term. No test is removed or weakened, every run exits 0, the size is within the limit, and the module map rows of the three modules the change touches are updated. Nothing needs fixing now. I make two minor observations.

## Findings

### f1 Minor observation: work_items still documents every unbuilt scenario as a strict xfail
- item: b166
- where: scripts/work_items.py:2
The module's docstring still says a scenario of an `unbuilt:` requirement "is a strict xfail (spec_unbuilt)". The comment at line 23 says the same, and so does CLAUDE.md's module-map row for `scripts/work_items.py`. Since 82ef2ef7 the xfail is non-strict when `$SHOPSYSTEM_UNBUILT_NONSTRICT` names the spec root. The rows for `spec_unbuilt.py` and `batch_tasks.py` were updated to say so, but this one was not. Behaviour is unaffected. Fix: in the docstring, the comment and the module-map row, add "strict unless `$SHOPSYSTEM_UNBUILT_NONSTRICT` names the tree".

### f2 Minor observation: an item's lexicon problem whose tuple equals one already present is not reported
- item: b166
- where: scripts/readiness_bar.py:151
The bar compares the problems after the item's lines are laid with those before as sets of `(code, term, message)` tuples. If the item brings a problem whose tuple is identical to one the spec or an earlier item already has, the set comparison hides it. This needs the same code, term and message, which can happen for a value-level `v_t5`, or a `v_t6` whose message does not carry the file. I verified that `spec_lexicon.problems` builds `v_t5` messages from the value, kind and attributes only, with no file. No client produces this today. A count comparison (a multiset) would close it.
