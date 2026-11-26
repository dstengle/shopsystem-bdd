---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-142/review-1
kind: review
batch: batch-142
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/165
head: 933ce950d6972d69cad8e4aaf58082839d102102
range: fd5b0ef2bc57f53cc939db675842fa3eef97c997..933ce950d6972d69cad8e4aaf58082839d102102
result: clean
---

# batch-142 review 1

## Verdict

The batch builds b758's lines. Opening a batch now lays each item, prepares the workspace once for the batch, then checks each item (batches r188 and r189). The new reopening line names every bar check the item fails (r187). Laying r6, r9-r21 sit on the new `prepare` operation, and scenarios drive it in process. All five checks in `## Runs` exit 0, as they do at the base. Nothing needs fixing before the merge. There are three observations: the module map is stale, the old regeneration path is left dead with the only unit tests, and the change is over the size limit.

## Findings

### f1 Minor observation: module map rows still say the lay generates features and batch_start lays per item
- item: -
- where: CLAUDE.md:242
After this change, `lay` only lays an item's lines and their `unbuilt:` ids. `prepare` now writes the features, corpus, catalogues, Composition, annotation and successors. Several module-map rows in the batch's CLAUDE.md still describe the old split:
- the `scripts/laying.py` row says `lay(item, workspace)` has "their scenarios generated there", cites laying r1-r4, and never names `prepare`;
- the `scripts/laying_inprocess.py` row puts features, corpus, Composition, catalogues and successors under `lay` (`lay_lines`);
- the `scripts/batch_start.py` row has no prepare step;
- the `scripts/batch_generator.py` row says it is "read by batch_start's lay and unlay";
- the `scripts/batch_reached.py` row (line 271) still cites batches r157 and "batch_start's lay";
- the `scripts/readiness_bound.py` row (line 242) still cites batches r169;
- the `batches_handlers4.py` row (line 343) still says `batches_handlers_corpus.py` holds the lay's bookkeeping (r46-r49), which has moved to laying_handlers_prepare.

The commits did edit CLAUDE.md, but only to add rows for the new handler modules and drop rows for the deleted ones. b758's note gives these rows to the main session, so this does not hold the merge. They should still say `laying.prepare` before the merge.

### f2 Minor observation: `batch_reached.regenerated` and `digest` are dead in production, and only they have unit tests
- item: b758
- where: scripts/batch_reached.py:89
`laying_inprocess.prepared` now calls the new `batch_reached.prepared`. That function asks `git status` whether anything changed since HEAD, instead of comparing digests taken before and after the lay. I searched the scripts and tests: nothing in `scripts/` calls `regenerated` or `digest` any more. Only `tests/scripts/test_batch_reached.py` (lines 30-58) calls them. So the unit tests cover a function production no longer runs, and the new `reached` has no unit test; only the scenarios of laying g17 and g18 exercise it.

`reached` also differs in a few cases. It treats every uncommitted change since HEAD as a change, where the digest compared before and after the lay. Its path list is hand-written rather than taken from `spec_held.inputs`, so the plugin's packs and base grammar are left out. Its glob for provider contracts is `provider/**/contract.toml` at the top of the repository only.

Fix: move the `test_batch_reached` cases onto `prepared`/`reached`, and delete `regenerated` and `digest`.

### f3 Minor observation: the change exceeds the review size limit
- item: b758
- where: -
`## Size` gives 31 files, +1229 -1187 (2416 changed lines) against a limit of 1000. All of it is b758's. Most of it is the retired batches lines moved to laying: their scenarios, corpus blocks and adapter annotations, and their worlds moved from batches' handlers to `laying_handlers_prepare.py` and `laying_handlers_reached.py`. The item's own note estimated about 1000 lines and proposed splitting laying#r9-r18 out at the pick if it ran past the limit.
