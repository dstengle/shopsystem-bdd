---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-126/review-1
kind: review
batch: batch-126
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/149
head: b3ae594e3b3d627e8bebdedf5a913e09d36ce9bc
range: 4927d3154d662ee1fdac4ea59de743f40130ce36..b3ae594e3b3d627e8bebdedf5a913e09d36ce9bc
result: fix-now
---

# batch-126 review 1

## Verdict

The batch builds all six lines: items#r72, batches#r160 and r161-r164. There is one finding to fix: b715 loosened a test that no line asks to change. There is also one observation about batch opening.

## Findings

### f1 Important fix now: test_grammar4_factored now ignores sense numbers on both sides
- item: b715
- where: tests/scripts/test_grammar4_factored.py:71
This test checks that every live line still reads to the logical form it had before the factoring. It now applies `unsensed` to both the fixture form and the current form, so `take#3(` and `take#1(` compare equal. A line that grammar 4 now reads under a different sense of the same verb, with a different frame, passes. That is a change of meaning the test was there to catch, so the assertion is loosened. The fixture holds eight `#2(` forms that are no longer checked.

No line of the batch asks for this. b715's own line (r164) is about the batch's corpus blocks, and r164 passed with no script change. No item in this batch gives a verb of this repository a new sense: b721 and b713 add only the noun `fix`, and b715's added sense lives only in its scenario world. So this batch's tree does not need the change. The commit says it is there "so a sense an item adds does not break it", which is a future concern.

Fix: put back the exact comparison. If tolerating renumbering is wanted, compare each `verb#n` by the sense it names (for example, its frame read from the vocabulary of the tree the form came from), not by dropping the number. Better still, leave the fixture to be rewritten by the item that adds such a sense.

### f2 Minor observation: `work batch start` counts bound-check violations the base already had; the readiness bar does not
- item: -
- where: scripts/batch_start.py:140
In `readiness_bar._broken`, the bound-check reasons are taken from `found - before`, so a v_pb1 or v_pb2 already on the copy before the lay is not the item's. In `batch_start.violating`, `bound` holds every v_pb1 and v_pb2 on the laid worktree, with nothing filtered against the base.

`readiness_bound.operations` also counts any operation that the item's core lines request (`requester`/`asks`) or that its model lines declare, not only one that a port line of the item governs. Put together: an item that only adds a core line requesting a port operation whose outcome was already unhandled on the base passes `work ready`. `work batch start` then reopens it, naming the outcome, although r160's While part (the item holds a port line that governs the operation) does not hold. Today `main` is expected to be clean of v_pb2, which is why this is an observation.

Reproduction: on a base where `stock.reserve done` is already unhandled, ready an item whose notebook line requests `stock.reserve`; the item passes the bar, and `work batch start` gives it back `shaped`.

What I checked on the points you raised:
- **b713 (r161, r162):** passing before they were built is consistent. `batch_laid` returns only items whose fresh lines pass, and these two lines retire r149 and r154.
- **r164:** it is built by the existing `batch_reached` rewrite of corpus blocks, together with the new scenario handler `tests/scenarios/batches_handlers_added_sense.py`.
