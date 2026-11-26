---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-139/review-1
kind: review
batch: batch-139
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/162
head: cd316e3b7785e4f8672ca31c03ae333b68da9fa6
range: cc2d5fcf9fa463b95947b82252bdef688beba2fa..cd316e3b7785e4f8672ca31c03ae333b68da9fa6
result: clean
---

# batch-139 review 1

## Verdict

The batch builds all ten of b611's lines. The port, the in-process adapter and the stand-in are in place, and the lay, check, reopen, lift and kept change go through them as the lines say. Nothing needs fixing before the merge. There are five observations: decision 0125's architecture decision for this port was never written, the change is over the size limit, and three are small: printed output, cost and stale module-map text.

## Findings

### f1 Important observation: no decision records which adapter the laying port is wired to
- item: b611
- where: scripts/laying.py:21
Decision 0125 (judgement tier) says a downstream records which adapter of a port it runs as a technical architecture decision. The contract registry has one, decision 0146. The laying port is hard-wired to `laying_inprocess` with no such decision. b611's own note says the batch session writes it with `work decision` at tier judgement, citing 0125. Nothing under `spec/decisions/` mentions laying, in the batch's worktree or on `main`. The docstrings and the CLAUDE.md rows cite 0125 for a decision that was never written. Fix: run `work decision "The laying port is wired to the in-process adapter" --tier judgement ...` on the base before the merge, as was done for 0146.

### f2 Minor observation: `work batch start` now prints every bar reason of a returned item, not only rule failures
- item: b611
- where: scripts/batch_start.py:153
The `-> shaped:` line changed from `r[0]` to `"; ".join(r)` for every entry of `pick.returned`. That is right for r181 (a failed check names every rule). But `pick.returned` also holds the items `batch_pick` returns because they fail the readiness bar alone, and the items `batch_laid.passing` returns. For those, the printed line now lists every bar reason where it used to list the first. No line asks for that change. The item's reopen note already joined all reasons (batch_pick.py:73), so nothing is lost either way. Reproduction: make an item `ready` that breaks two bar checks, then run `work batch start`. Its `-> shaped:` line now holds both reasons.

### f3 Minor observation: each picked item is laid on its own, so features and catalogues are written once per item
- item: b611
- where: scripts/batch_start.py:64
`_laid` calls `laying.lay` once per item, and `laying_inprocess.lay_lines` runs once for each call. The old code did one lay for the whole pick. So each of the following now runs N times for N picked items:
- `_generated` of each capability (in the plugin's own tree, a `features generate` subprocess each time)
- `batch_reached.regenerated`, which rewrites every service feature when the vocabulary inputs change
- `spec_composition.write`
- `_annotated`
- `batch_catalogues.write`

A catalogue problem may also be added to `unwritten` once per item, so the batch brief can name it twice. I read decision_successor.lay: it supports being called again for later items (`_pending`/`_again`), so r177 still holds. This is a cost of opening a batch, not a wrong answer. The fix is to let one lay request carry the pick, or to deduplicate `unwritten`.

### f4 Minor observation: module map rows and a docstring still say batch_start lays and unlays
- item: b611
- where: CLAUDE.md:270
The `scripts/batch_generator.py` row says "read by batch_start's lay and unlay". The `scripts/batch_reached.py` row (CLAUDE.md:271) says "which batch_start's lay calls". The docstring at scripts/batch_generator.py:5 says the same. Those functions moved to `laying_inprocess.lay_lines` and `unlay_lines`, and the other rows this change touched (decision_successor, batch_start) were updated. Fix: name `laying_inprocess` in these places.

### f5 Minor observation: the change is over the review size limit
- item: b611
- where: -
`## Size` gives 25 files, +1131 -265 against a limit of 1000 changed lines. All of it is b611's. The item's note estimated about 800 lines. The largest parts are the two handler modules (`laying_handlers.py`, `batches_handlers_laying.py`), `laying_inprocess.py` (mostly code moved out of batch_start), the regenerated batches feature and the spec corpus.
