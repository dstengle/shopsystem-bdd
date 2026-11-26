---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-124/review-1
kind: review
batch: batch-124
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/147
head: a2e8fda691dabef56469460aaf8512afd521f451
range: 4bbaeae052b4d739ae98af4540f80dace254759c..a2e8fda691dabef56469460aaf8512afd521f451
result: clean
---

# batch-124 review 1

## Verdict

The batch builds all five items. b706's r34 has its Given of the shop's product, and the Then checks the kept product against that shop's id. b707's lay writes the features and corpus blocks its model change reaches again. b710's poll returns `fix task` with the later task and the files when two task branches conflict. b711's r159 is met by the existing build task pick, because a running task that is already built takes `finish task` first. b712's chore check holds. No test is removed or weakened. The r152 and r18 scenarios are retired through r159 and r34. Every run exits 0, and the change is under the size limit. Nothing is to fix now; there are four observations.

## Findings

### f1 Minor observation: a park or unlay leaves the features and corpus blocks b707's lay rewrote
- item: b707
- where: scripts/batch_start.py:99
`lay_lines` now calls `batch_reached.regenerated`, which rewrites other capabilities' features and the whole corpus after the lay's model or vocabulary change. `unlay_lines` does not call it: it regenerates only the capabilities the parked item holds lines of. Parking an item like batches_handlers_beyond's (a notes model restating `add`, no notebook line) puts `spec/model/notes.md` back. But `features/notebook.feature` and r4's block in `grammar/corpus/spec/notebook.md` stay as the lay wrote them. The next `work batch review` would then fail `features generate --check` and the corpus test. No line of this batch asks about parks, so this is hardening. A fix: take the digest before the unlay and call `batch_reached.regenerated` in `unlay_lines` too, which would also cover `work batch amend`'s take-out.

### f2 Minor observation: the commands reference does not say that `fix task` also covers conflicting task branches
- item: b710
- where: docs/reference/commands.md:501
b712's text says `fix task` means "every task done and the last whole-suite run of `shop work batch review` failed". It gives the order as "... prepare task, fix task, look at failure, submit batch". After b710, `fix task` also comes from two task branches that conflict, it is picked before the failed-run case, and it gets `file:` lines and a report that names the merge. The reference does not cover any of that, while batch_next's docstring does ("fix task (a conflict first)"). The chore's check passes either way. One clause in the reference would close the gap.

### f3 Minor observation: the module map rows of batch_next and batch_merge do not say what b710 added
- item: b710
- where: CLAUDE.md:256
`scripts/batch_merge.py` now has `clashes` (every conflicting path of two branches, the `unbuilt:` conflicts aside), and `clashing` is built on it. `scripts/batch_next.py` now has `_conflict` and the conflict form of `fix task` (later task, earlier task, files; the `files` key; the merge report). Neither module's row in CLAUDE.md was updated: batch_merge's row names only `clashing`, and batch_next's row describes `fix task` only as batch_broken's task. The fix is to add both to their rows.

### f4 Minor observation: the conflict check and the corpus rewrite cost more as batches grow
- item: -
- where: scripts/batch_next.py:79
Once every task is done, `_conflict` runs `git merge-tree` on every pair of task branches each time the batch is polled, which is O(n²) per poll. Separately, `batch_reached.corpus` runs `spec_corpus_write.form` (a full grammar 4 parse and logical form) on every block of every codified-2 corpus file whenever the digest changes. The digest covers the index, packs, model and vocabulary, so any item with a model line or a new capability changes it, and the rewrite then covers the laid capabilities too, which spec_corpus_write has just written. Both work correctly. The cost only shows with larger batches and corpora, so this is recorded and does not hold the merge.
