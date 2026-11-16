---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-43/review-1
kind: review
batch: batch-43
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/66
head: 52c26c5ae2498c9c5338a8b80084d538bf767912
range: e558e6e4145022e38e0a3cfd63c96b79afcdf1b5..52c26c5ae2498c9c5338a8b80084d538bf767912
result: fix-now
---

# batch-43 review 1

## Verdict

The batch builds all five requirement lines: b175's r319, b296's r134, b305's r50 and b314's r320-r322. One finding must be fixed: `tools check` passes at the base but fails at the head, because ruff reports two errors in b296's files. The rest are observations.

## Findings

### f1 Important fix now: `tools check` fails at Head on two ruff errors in b296's files
- item: b296
- where: scripts/spec_steps4_held.py:9
`python3 scripts/tools check --base e558e6e41` exits 1 at Head and 0 at the base (`## Runs`):

```
scripts/spec_steps4_held.py:9:1: I001 [*] Import block is un-sorted or un-formatted
tests/scenarios/feature_file_tools_collections.py:39:10: ISC004 Unparenthesized implicit string concatenation in collection
```

b296 caused both errors. Commit 0e041e15c added `import spec_steps4_boxes as boxes` between `from spec_lf_core import ...` and `from spec_steps4_boxes import TraceError`, which unsorts the import block. It also added the `"capped"` row to `LINES` in feature_file_tools_collections.py, whose second line is written as two adjacent string literals inside a tuple with no parentheses (`"... whose " "version is ..."`). The batch's own check is red at Head. Fix: sort the imports in spec_steps4_held.py (`ruff --fix` does it) and put the concatenated literal at feature_file_tools_collections.py:39 in parentheses, then rerun `tools check`.

### f2 Minor observation: a state verb in a relative clause after shall is now refused as the response's verb
- item: -
- where: scripts/spec_grammar4.py:183
`misaspected` takes its clause from the nearest When, If, While or (now) shall before the token where the parse stopped. It cannot tell the response's own verb from a state verb inside a relative clause of the response. Take a line that stops at a state verb in a response's relative clause for another reason, such as a frame break in "shall print a worktree that holds a stage". It is now refused with "the verb hold is a state, and a response takes an action", and spec_refusal4's frame refusal never runs. Before this change the same line got "... a trigger takes an action", so the wrong reason was there already; the batch moves it from the trigger to the response. What I checked: `parse` at spec_grammar4.py:214 calls `misaspected` before `spec_refusal4.refusal`. r319 names only a response that uses the state term itself, so this does not hold the merge.

### f3 Minor observation: a "may" line's state verb is still refused as the trigger's
- item: -
- where: scripts/spec_grammar4.py:173
`CLAUSES` gains "shall" but not "may". So "When a session ends a stage, `work` may follow the stage." still finds "when" as its clause and is refused with "a trigger takes an action". The capability's new term defines a response as "the part of a requirement after shall", so r319 does not cover this line. A later item could add "may" (it takes an action too) so that a permission's state verb is refused the same way.

### f4 Minor observation: the readiness bar skips features generate for a whole capability when one of its lines does not parse
- item: -
- where: scripts/readiness_bar.py:107
`_scenarios` skips every block whose capability holds any unparsed line (`broken`). Suppose an item has one unparsed line in capability C and another group of C that gets no scenario. That second group is not named in this run; it shows up only after the parse is fixed. r50 asks only for the lines with no parse and no translation, so nothing breaks a requirement. Still, b305's docstring promises "one run names every failing line", and this case falls short of it. A later item could run generate over a copy with only the unparsed lines taken out.

### f5 Minor observation: module map rows not brought up to date for two files the batch changes
- item: -
- where: CLAUDE.md:1
- `design_model_check_worlds_member.py`: its row in the module map at Head lists is-in, holds-exactly and holds-nothing. It does not mention b314's new worlds: an object that holds nothing or no file beside a forbidden one that holds a file, and two objects that hold a file.
- `readiness_world.py`: its row at Head does not mention b305's `give_faults` or the world's other item `OTHER`.

Neither row is false. Both leave out the concern this batch added.
