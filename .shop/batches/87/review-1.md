---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-87/review-1
kind: review
batch: batch-87
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/110
head: 04c343d7600b843918cbfee4daa81153c809f4dc
range: 1f97340d775ebbfc7d1635772fe36de1d70bd2ff..04c343d7600b843918cbfee4daa81153c809f4dc
result: clean
---

# batch-87 review 1

## Verdict

The batch builds both lines of b581. batches#r104 retires r103 into a group with its own title (g104), so g102's scenario is now collected. items#r55 is built by `readiness_titles.shared`, which the readiness bar calls on its laid copy. The refusal names the group title, and a generated scenario drives it. All runs exit 0 at the head and at the base, and the change is well under the size limit. Nothing needs fixing before the merge. There are two observations.

## Findings

### f1 Minor observation: a second `work line` with no `--group` now makes an item the bar refuses
- item: b581
- where: scripts/backlog_lines.py:93
`add_line_to` gives each line added without `--group` or `in_group` a new group titled with the item's title. So an item that gets two lines this way now holds two groups of one title in one capability, and items#r55 refuses it at `work ready`. The same happens on `work batch amend`, through the bar of r96. The refusal is what r55 asks for, so this is no defect of the batch. Still, the default drafting path now produces items that fail the bar.

The batch shows it in its own change: commit 4862da093 adds `--group "Abandon again"` to both `work line` calls in `tests/scripts/test_batch_amend.py`, because the amend's bar would otherwise refuse. The test's assertions are unchanged, so the test is not weakened. The idea b583 ("A second line of an item joins its group of the same title") already tracks the fix.

### f2 Minor observation: the module map row of batch_summary still cites batches#r103
- item: -
- where: CLAUDE.md:224
The change moves `scripts/batch_summary.py`'s docstring and `tests/scenarios/batches_handlers_summary.py`'s from r103 to r104. The `CLAUDE.md` module map row of `scripts/batch_summary.py` still reads "(b580, batches r102, r103)", and r103 is now retired. Fix: write r104 in that row.
