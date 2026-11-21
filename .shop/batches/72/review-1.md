---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-72/review-1
kind: review
batch: batch-72
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/96
head: 8c5a10b7f543dc7c2e8850af1375afc75e646321
range: 5def563408ff32337a61827225cb761c92ab6a8c..8c5a10b7f543dc7c2e8850af1375afc75e646321
result: fix-now
---

# batch-72 review 1

## Verdict

The batch builds all three items: b49's records r3, r5 and r6, b75's batches r98 and r99, and b54's chore. There are two findings to fix, both on b75. A malformed `[batch] rules` is refused only after the batch has been committed, and the `tools check` run fails at Head while it passed at the base. There are also two observations on b49.

## Findings

### f1 Important fix now: a malformed `[batch] rules` is refused after the batch is committed on the base
- item: b75
- where: scripts/batch_start.py:172
`batch_driver.batch_rules` raises `Refused` when `[batch] rules` is not a list of texts (scripts/batch_driver.py:300-301). It is first called from `batch_driver.write`, at scripts/batch_start.py:172. That line comes after the `try` block. By then the `batch-<n>` branch and worktree exist, the picked items are `in-batch` and the plan is committed on the base (line 166), and the `except` that removes the tree and branch no longer covers it. So a hand-edited `rules = "one"` leaves the batch `building` with no brief, and the command still exits with a refusal. `[batch] push` does not have this problem, because `push_prefix(root)` is called at line 145 "before anything is written". Fix: call `batch_driver.batch_rules(root)` beside `push_prefix(root)` at line 145, so the refusal changes nothing. Add a test that `work batch start` with `rules = "one"` commits nothing and leaves no branch.

### f2 Minor fix now: `tools check` exits 1 at Head (base: 0), because vulture flags the touched test file
- item: b75
- where: tests/scripts/test_batch_driver.py:13
The run's output:
```
== vulture ==
tests/scripts/test_batch_driver.py:13: unused variable 'blocks' (100% confidence)
```
The line is `monkeypatch.setattr(batch_driver.backlog_lines, "ids", lambda blocks: list(ids))`. It is older than the batch, but `tools check --base` checks the files the change touches, and b75 added a test to this file, so the check now fails. Fix: rename the parameter to `_blocks`, or use `lambda *_: list(ids)`.

### f3 Minor observation: `work record --about` of a node now reads the whole spec, parsing every line in grammar 4
- item: b49
- where: scripts/record_write.py:440
For every `--about` that is not an item or a batch, `denotes` runs `Model(root).read()`. That is the full read: capabilities, features, decisions, records, work, requests and catalogues. Per CLAUDE.md, model_spec's reading parses each requirement in grammar 4. Before, `work record` only imported `model_facts.KINDS`. Now a `work record --about capability/x` costs a full `spec` read and needs the GF toolchain to be installed. I checked `Model.read` (scripts/model_facts.py:130-146) for what it reads; I did not measure the time. A lighter check would be enough: the node's file by its kind, the way shop_ids resolves an item or a batch.

### f4 Minor observation: r5's scenario files "the record r1 with the record r1", and an unheld item or batch id is refused only in unit tests of `held`
- item: b49
- where: features/records.feature:152
The generated When of r5 reads "with the text" as the parameter given the record (form: `param(e1, text, x6)`). `records_handlers_about.names_text` works around this by checking whatever the When gave as `--about`. The idea b527 tracks the grammar issue. The scenario's "denotes no node/item/batch" Given always passes `capability/.../nowhere` (`H.full("capability", "nowhere")`). So no test drives `work record` with an `item/b<n>` or `batch/batch-<n>` id this repository does not hold. tests/scripts/test_shop_ids.py checks `held` directly, but not the refusal through `attributed`. A case in tests/scripts/test_record_write.py with `--about item/b99` would close that gap.
