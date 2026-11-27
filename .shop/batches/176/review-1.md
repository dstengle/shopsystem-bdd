---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-176/review-1
kind: review
batch: batch-176
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/198
head: 3c30be1c3443bc7f3c09920416c425a92482b7e5
range: bf8a80b7d6c999cf19bcc0c953debeb72bfe6148..3c30be1c3443bc7f3c09920416c425a92482b7e5
result: fix-now
---

# batch-176 review 1

## Verdict

The batch builds both of b882's lines: drafting#r113 (`work line --into <cap> --retires <other>#r<n>` puts the line into `--into`'s block and the `<cap>#r<n> r<m>` pair under the retired id's block) and batches#r193 (`batch_laid.fresh` now reads a pair under another capability's block as a retiring line). The check run fails at Head and passes at the base on one ruff error, which has to be fixed. Two hardening gaps are observations.

## Findings

### f1 Minor fix now: `tools check` fails at Head on ruff RUF059 in the new r193 handler
- item: b882
- where: tests/scenarios/batches_handlers_cross_retires.py:47
`python3 scripts/tools check --base bf8a80b7d` exits 1 at Head and 0 at the base:

```
tests/scenarios/batches_handlers_cross_retires.py:47:16: RUF059 Unpacked variable `k2` is never used
```

In `has`, the line `(k1, n1), (k2, n2) = parts(step)` unpacks `k2` and never uses it. While this stays, the batch's check is red. Fix: rename it `_k2`, or unpack `(k1, n1), (_, n2)`.

### f2 Minor observation: `--into` with `--retires` of another capability is refused unless `--into` is a codified-2 file already in the spec
- item: b882
- where: scripts/backlog_retires.py:243
`check` lets `--into` differ from the retired id's capability only when `_codified(root, into)` holds, meaning the spec has a file for `into` with `language: codified-2`. r113 sets no such condition. Three cases are refused instead of kept:
- the target capability is still codified-1;
- the target is recodified on this item (`work line --recodify`);
- the target is new on this item (`--capability`).

I checked `spec/capabilities/*`: every file has a `language:` line, so for the capabilities the spec holds today the refusal mostly falls on edges no current item reaches. Reproduction: make an item that adds a new capability `x` with `--capability x`, then run `work line <item> --into x --retires work-queue#r1 '<line>'`. It is refused with "goes into work-queue or another capability of the spec". Consider accepting any capability the item's blocks or the spec hold.

### f3 Minor observation: `work split` does not take a cross-capability pair along with its line
- item: -
- where: scripts/backlog_split.py:57
`_apart` moves a `retires:` pair only when the pair's line is in the same block (`p[0] in moved`, a bare `r<n>`). Say a `review#r<n>` line that retires `work-queue#r1` is split into a new item. The pair `review#r<n> r1` and `retired: [r1]` stay in the original item's work-queue block. The original item then retires an id with a line it no longer holds, and the new item's line reads as fresh to `batch_laid.fresh`, which is the reopen r193 rules out. No line of this batch names split, so this is hardening. Reproduction: draft as `drafting_handlers_into_retires` does, then run `work split b1 --requirement review#r<n>`.
