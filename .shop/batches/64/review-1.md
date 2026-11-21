---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-64/review-1
kind: review
batch: batch-64
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/88
head: 3550423ee4888ed5da231a6dd02a29fd43622d72
range: 4a81676a9cfb48fedbbe96d3faa8d23238a88cb7..3550423ee4888ed5da231a6dd02a29fd43622d72
result: fix-now
---

# batch-64 review 1

## Verdict

The batch builds all seven items, with one problem to fix. The new review-limit check in b483's pick runs before the readiness bar, so a `ready` item that no longer meets the bar can now stay `ready` instead of going back to `shaped` (batches#r54). The other findings are observations.

## Findings

### f1 Important fix now: an item over the review limit skips the bar, so one that fails it stays `ready` against batches#r54
- item: b483
- where: scripts/batch_pick.py:64
In `pick`, the new `batch_estimate.exceeds` check comes before `_alone(root, item)` and ends with `continue`. Take an item that is `ready`, no longer meets the readiness bar, and has an estimate that would pass the limit after the items already taken. It is put in `left_out` and stays `ready`. Before this change, every item the loop reached went through `_alone` and, failing it, was set `shaped` with its reasons noted. That is what batches#r54 asks ("While an item is `ready` and the item does not meet the readiness bar, when the person opens a batch, the batches service shall set the status of the item to `shaped`"). r54 has no review-limit condition, and r93 forbids only `in-batch`, not `shaped`.

To reproduce: take the setting of `test_pick_leaves_out_an_item_that_exceeds_the_review_limit_and_goes_on`, but break b2 so it fails the bar alone (for example a line that does not parse). With this change b2 lands in `left_out` as `ready`. Before it, b2 was in `returned` as `shaped`.

Fix: run the `exceeds` check after the `_alone` check, before the trial lay, so an item that fails the bar goes back to `shaped` whatever its estimate. Add a test for an over-limit item that fails the bar.

### f2 Important observation: the vocabulary's "the ignore file form" still says a leading slash makes no difference
- item: b487
- where: spec/vocabulary/upgrades.md:67
The term's gloss still reads "so that a name with or without its leading or trailing slash is the same entry". b487 changes the behaviour: a leading slash anchors the line at the top, and r42's given block treats `/__pycache__/` as not conforming. upgrades#r42 and r43 both rest on this term, so its definition now contradicts the lines and the code (`migrate_init.ignore_text`, the CLAUDE.md row for `scripts/migrate_init.py`). The item's lines do not change the entry, and the batch could not change it by hand. It needs an item that rewords the term (`work line --reword-term`), for example "a trailing slash is the same entry, and a leading slash anchors a line at the top so it covers no name at any depth".

### f3 Minor observation: `merge`'s docstring cites a retired requirement, and the module map does not list the successor refusals
- item: b484
- where: scripts/backlog_note.py:37
The docstring of `merge` still cites `items#r33`, which this batch retires in favour of items#r44. The successor refusals it describes are now items#r43 and r45 and could be cited by id. Separately, the CLAUDE.md row for `scripts/backlog_note.py` still lists only "a closed item refused, naming it" and not the refusal of a successor that is the item itself or closed. That refusal was already in the code before the batch; b484 states it in lines.

### f4 Minor observation: an entry git reads like an unanchored name is still taken as missing
- item: b487
- where: scripts/migrate_init.py:813
`ignore_text` only strips a trailing slash before comparing. A line such as `**/__pycache__/` or `**/.venv` covers the same paths in git as the bare name, but it still counts as not covering it, so `migrate init` appends `__pycache__/` again. This is harmless (one redundant line), and no line or scenario names this case.

### f5 Minor observation: the gloss of "the review limit" gives a fixed 1000
- item: b483
- where: spec/vocabulary/tracking.md:155
The entry says the review limit is "The number of changed lines a pull request review reads in one batch's change, 1000". `batch_estimate.limit` reads `[review] size` from `.shop/delivery.toml` and uses 1000 only as the default. The docs describe it that way too, as does the r93 scenario, which sets the limit to 1. The gloss could say "`[review] size`, 1000 by default".
