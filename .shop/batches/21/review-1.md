---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-21/review-1
kind: review
batch: batch-21
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/34
head: b5d907198c7c101fc24af6b501b0a86653c0ac58
range: 3a3de9225b23e95ee790ee37781ca9b32b845afa..b5d907198c7c101fc24af6b501b0a86653c0ac58
result: fix-now
---

# batch-21 review 1

## Verdict

All four items build their lines: b119 (r71), b128 (r13, r14), b130 (r34, r35) and b123 (r72, r73). There are two findings to fix now. The `tools check` run exits 1 at the head and 0 at the base, because ruff finds 7 new errors in this batch's files, split between b123 and b119. There are also two observations (b128's `unlay`, the size) and one drop.

## Findings

### f1 Important fix now: `tools check` fails on ruff errors in model_rules.py
- item: b123
- where: scripts/model_rules.py:26
The `tools check` run exits 1 at the head and 0 at the base (`Exit code: 1 (base: 0)`). Four of its seven ruff errors are in b123's new module:
```
scripts/model_rules.py:26:14: ISC004 Unparenthesized implicit string concatenation in collection
scripts/model_rules.py:32:15: ISC004 Unparenthesized implicit string concatenation in collection
scripts/model_rules.py:34:15: ISC004 Unparenthesized implicit string concatenation in collection
scripts/model_rules.py:115:12: ISC004 Unparenthesized implicit string concatenation in collection
```
These are the multi-line strings inside the `LEXICON` tuples and the header line inside `render`'s `out` list. The batch must not make the repository's own check go from passing to failing. Fix: wrap each concatenated string in parentheses (or join the pieces) so ISC004 is satisfied, then rerun `tools check`.

### f2 Important fix now: `tools check` fails on ruff errors in b119's test and handler
- item: b119
- where: tests/scripts/test_check_scale.py:16
The same failing `tools check` run reports three errors in files b119 added or changed:
```
tests/scenarios/design_model_check_handlers_conditions.py:43:15: ISC004 Unparenthesized implicit string concatenation in collection
tests/scenarios/design_model_check_handlers_conditions.py:45:15: ISC004 Unparenthesized implicit string concatenation in collection
tests/scripts/test_check_scale.py:16:19: RUF100 [*] Unused `noqa` directive (non-enabled: `E402`)
```
The first two are in the `UNPAIRABLE` list, which is the r71 scenario's capability. The third is the `# noqa: E402` on `import toolchain`, a rule the project does not enable. Fix: parenthesise the two concatenated strings in `UNPAIRABLE` and drop the unused `noqa`.

### f3 Important observation: `unlay` leaves a live id in `retired:` when one item retires two lines of one group
- item: b128
- where: scripts/backlog_retires.py:967
In `unlay`, the loop is `for rid in rids: if _group_of(text, rid) is not None: continue`. Here is what happens when an item retires `r3` and `r4`, both in group `g2`:
- `lay` keeps the group when it takes `r3` out (`r4` is still in it), then removes the group when it takes `r4` out. That gives `gone = [r3, g2, r4]`.
- `unlay` handles `r3` first. The group is gone, so it puts back the whole group as git held it, with both lines in it, and records `back = [r3, g2]`.
- For `r4`, `_group_of` now finds the restored group, so the loop hits `continue` and never adds `r4` to `back`.
- `_listed(..., drop=True)` therefore leaves `r4` in the capability's `retired:` while `- [r4]` is live again. `model check` then reports v15c ("a retired id is used again").

`unlay` is what `batch_start.unlay_lines` uses, and what `work batch review` and park use to take a parked item's lines out, so the spec would be left wrong there. No line names this case and the tests do not reach it: `test_a_group_s_last_line_takes_its_group_out_and_back` uses `r3` and `r4` in different groups. Fix: always add `rid` to `back`, including when its line is already back in place. Add a test where both retired ids are in one group.

### f4 Minor observation: the change is over the size limit
- item: -
- where: -
The change is 38 files, +2691 −157, against a limit of 1000 changed lines. Most of it is b123's generated `grammar/rules.md` (1356 lines) together with the `% fail`/`% pass` examples in `scripts/model.lp`. Next come b119's rewrite of `grammar/check.lp` with `spec_solve_pairs.py`, and b128's `backlog_retires.py` with its tests.

### f5 Minor drop: a test's docstring still describes the old witness solve
- item: b119
- where: tests/scripts/test_spec_solve.py:215
The docstring of `test_the_whole_context_is_one_grounding` still says each L1's witness is "a focused solve ... its pair's external `focus` set true". check.lp no longer has those externals: the witnesses now come from one solve of the part `witness`. The assertion itself (one Control built) still holds. Rewording the docstring is polish.
