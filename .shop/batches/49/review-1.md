---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-49/review-1
kind: review
batch: batch-49
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/73
head: 4538338717ad8e8a77b9bef19a5d07dd1f7658ba
range: 498f844fd665a706da6ed87f767cc987c5c81a91..4538338717ad8e8a77b9bef19a5d07dd1f7658ba
result: clean
---

# batch-49 review 1

## Verdict

The batch builds both chores. b378 now passes `models=blocks.models` to `renumber`'s new Blocks, and its test shows the model block survives a renumber and is still laid. b379 annotates the laid copy in the readiness bar before `_violations`, and annotates the worktree in `batch_start.lay_lines` with the contract among the committed paths. Each part has a test of what the item's note asks for. Every run exits 0, as it does at the base. No test was removed or weakened. The change is well under the size limit. Nothing to fix now; three observations.

## Findings

### f1 Minor observation: the module map rows of readiness_bar and batch_start do not name the annotation
- item: b379
- where: CLAUDE.md:1
CLAUDE.md's module map is binding, and its rows describe each module's concern. The `scripts/batch_start.py` row lists what the lay writes: "lines into `spec/`, ids into `unbuilt:`, features generated, the corpus blocks (spec_corpus_write) and the catalogues (batch_catalogues) written". It does not list the adapter contract that `adapter_annotate` now annotates (`scripts/batch_start.py:53`, `_annotated`). The `scripts/readiness_bar.py` row does not say the laid copy's contract is annotated before the model check either (`scripts/readiness_bar.py:158`). The chore's `Files:` leave out CLAUDE.md, so the fix cannot go on b379's branch. Fix: a later item adds "the adapter contracts annotated (adapter_annotate, b379)" to both rows.

### f2 Minor observation: a park or a review takes lines out without annotating the contract again
- item: b379
- where: scripts/batch_start.py:47
The lay now writes requirement entries into `spec/adapters/cli.toml`. The reverse, `unlay_lines`, which `work batch review` and `batch_parked` use, does not annotate the contract again. So the contract on `batch-<n>` would still hold a parked item's lines, which is v_a6 (a held requirement that no longer governs). This batch parks no item, so it does not happen here. Idea b380 ("batch_start.unlay_lines re-annotates the adapter contract") is already in the backlog for it. It is recorded here so the gap is on the pull request.

### f3 Minor observation: the lay rewrites a base contract that is already stale, beyond the picked lines
- item: b379
- where: scripts/batch_start.py:57
`_annotated` writes every stale contract as `spec annotate` would (`adapter_annotate.stale(tree)`). If `main`'s `spec/adapters/cli.toml` is already out of date when a batch starts, the lay commit also rewrites operations no picked item touches. That change then shows up in the batch's diff and pull request as if it were the batch's own. The readiness bar does the same on its copy (`scripts/readiness_bar.py:158`). There it is harmless, because `before_lay` is read before the annotation, so a v_a5 or v_a6 that was already on the base is still told apart from the item's. What I checked: `stale` compares the whole annotated text, not only the operations the picked lines govern (`scripts/adapter_annotate.py:102-116`). To reproduce: commit a stale contract on the base, mark an item ready and run `work batch start`; the lay commit's change to `cli.toml` includes the unrelated operations.
