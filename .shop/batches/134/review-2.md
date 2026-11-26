---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-134/review-2
kind: review
batch: batch-134
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/157
head: d45e833f9c16f1db615076b9ead1215d3d6581de
range: 3ec52a8b90d6add5414038dbfd61ca3d0109a971..d45e833f9c16f1db615076b9ead1215d3d6581de
result: fix-now
---

# batch-134 review 2

## Verdict

The fix adds decisions#r26, with its scenario, handlers, corpus block and cli.toml annotation. That covers a `superseded` decision naming a retired requirement. But `retired_history` still also excuses a `rejected` decision, and no line asks for that, so f1 is only partly fixed. No other commit of the range introduces a new problem.

## Findings

### f5 Minor drop: the amend left a blank line at the end of two corpus files
- item: b735
- where: grammar/corpus/spec/checking.md:1907
- Commit 987aeef3f appends an empty line after the last block of `grammar/corpus/spec/checking.md` and of `grammar/corpus/spec/contract-registry.md`. Neither file gets a new block. It is noise from `work batch amend` relaying the corpus and changes no reading. Nothing to do on this batch.

### f6 Minor observation: the amend's relay undid b732's regenerated feature, and a later commit put it back
- item: -
- where: features/batches.feature:1099
- Commit 9c265f367 (`work batch amend` relaying b735) regenerated `features/batches.feature` with the base's generator. That turned b732's counter-example of batches#r153 (`the status of the task t5 is `running``) back into `done`. Commit 70be476e0 restores it by hand, and `features generate --check` exits 0 at Head, so the net change is nil. The risk is in `work batch amend`: it regenerates features with the base checkout's generator, not the batch branch's, so it can silently undo another item's generated scenarios. Worth an item against batch_amend.

## Earlier findings
- f1: not fixed: decisions#r26 traces only the `superseded` case, but `scripts/model_work.py:74` still excuses every status in `model_decisions.HISTORY`, which is `("superseded", "rejected")` (`scripts/model_decisions.py:24`), and the docstring at `scripts/model_work.py:71-72` still says "superseded or rejected". So `spec check` still silently accepts a retired requirement named by a `rejected` decision, and no line or Implementation section asks for that. Fix on b735: narrow `retired_history` to `superseded` (compare the status with `"superseded"` in place of `HISTORY`) and correct the docstring. The other way is to give the item a line for the `rejected` case too and amend.
