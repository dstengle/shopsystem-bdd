---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-5/review-1
kind: review
batch: batch-5
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/20
head: 9d633b8d6e5d6ff6d4d14b511849982b406bb1cd
range: b535bbc962bcb40af8edabba2ee33bc6df0ee65f..9d633b8d6e5d6ff6d4d14b511849982b406bb1cd
result: clean
---

# batch-5 review 1

## Verdict

The batch builds both of b45's lines. r9: `work decision` now checks `--summary`, `--decision` and `--tier` itself and names every one that is absent in a single refusal, before anything is written. r8's refusal naming `--tier` still holds. r57: `work record` refuses an `--about` that has a line break, has nothing after its kind, or has a kind the design model does not know. The refusal names `--about` and comes before anything is written. No test was removed or weakened, the feature files are what `features generate` writes, the module map rows are updated, every run exits 0 at Head, and the change is within the size limit. Two observations, nothing to fix before the merge.

## Findings

### f1 Minor observation: an `--about` naming a node that does not exist is accepted
- item: b45
- where: scripts/record_write.py:62
The capability defines **unattributed** as "a record whose `--about` is not one line or is not the id of a node of the design model". `attributed` only checks the shape `<kind>/<non-space>` and that the kind is in `model_facts.KINDS` or is `record`. It never checks that the node exists. So `--about capability/no-such-capability` is written into the frontmatter. b45's shaping notes asked for this kind-only check ("not `<kind>/<...>` of a kind the design model knows"), so it is not a wrong answer against the line as shaped. A strict reading of the term's text would refuse it, though. Reproduction: `work record "x" --kind analysis --summary s --body <file> --about capability/nothing` exits 0. The script test does the same with `record/ex.com/prod/ctx/2026-11-05-x`, which names no record. Either narrow the term's wording in a later line or check that the id resolves.

### f2 Minor observation: a record about a backlog item or a batch is now refused
- item: b45
- where: scripts/record_write.py:67
The kinds allowed are `model_facts.KINDS | {"record"}`. `item` and `batch` are not among them (I read `model_facts.KINDS` and `model_work.FROZEN_KINDS`). Yet b45's own file has the id `item/missingmass.io/shopsystem/shopsystem-bdd/b45`, so `work record --about item/.../b31` is refused. No committed record uses `about: item/...` or `batch/...` today (I searched `.shop/records/`), so nothing breaks now. It is a gap a session will hit when it writes an analysis of one item. Fix, if wanted: add the backlog's kinds to the allowed set, or have `model` know them.
