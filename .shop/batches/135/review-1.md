---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-135/review-1
kind: review
batch: batch-135
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/158
head: 1bd6cdc442c305f0308f20546c69d4bf659a84da
range: 5ee9c74df2fc39f3a43b7d7639b25846a74e6886..1bd6cdc442c305f0308f20546c69d4bf659a84da
result: fix-now
---

# batch-135 review 1

## Verdict

The batch builds all six lines (b740's r170–r172, b741's r173–r174, b742's consistency#r45). One check broke at Head (`tools check`'s ruff), and that is the one finding to fix. The rest are observations: hardening of the new subprocess generator and of the decision successor, a preposition edge in `spec explain`, and the size over its limit.

## Findings

### f1 Minor fix now: ruff fails on the new test_batch_generator.py (I001)
- item: b740
- where: tests/scripts/test_batch_generator.py:4
`python3 scripts/tools check --base 5ee9c74df` exits 1 at Head and 0 at base. Its output:
```
== ruff ==
tests/scripts/test_batch_generator.py:4:1: I001 [*] Import block is un-sorted or un-formatted
Found 1 error.
```
b740 added the file. The import block (`import pytest` then a blank line, then `import batch_generator`, `import features_generate`) is not grouped the way ruff's isort settings want. While this check fails, the review's run of `[review] checks` cannot pass. Fix: run `ruff check --fix tests/scripts/test_batch_generator.py`, or regroup the imports by hand, then commit on b740's branch citing the finding.

### f2 Minor observation: a generator subprocess that times out crashes `work batch start`, `park` and `amend` instead of refusing
- item: b740
- where: scripts/batch_generator.py:31
The risk: `_run` calls `subprocess.run(..., timeout=TIMEOUT)` with `TIMEOUT = 600`. When that limit is reached it raises `subprocess.TimeoutExpired`. `generate` does not catch it. `batch_start._generated` only catches `features_generate.GenerateError` (scripts/batch_start.py:93-95), so a hung tree generator ends the command with a traceback instead of the `features generate of <cap> failed` refusal. In `generate_all` the same exception skips the one-by-one fallback. What I verified: the only `except` near either call is for `GenerateError`. Fix: turn `TimeoutExpired` (and `OSError`) into a `GenerateError` inside `generate`, and into a failed batch run inside `generate_all`.

### f3 Minor observation: a consumer tree holding its own `scripts/features` and `scripts/features_generate.py` has those scripts run as the generator
- item: b740
- where: scripts/batch_generator.py:21
`_program` checks only that the two files exist. It does not check that the tree is the plugin itself. A consumer repository that happens to keep its own `scripts/features` would have that program run with the plugin's interpreter, with `generate --root <tree> --preview <file>`, in place of the plugin's generator. r170 names "the feature generator" of the batch's workspace, so the plugin's own case is what the line asks for. No client of this kind is known today. Hardening: also check that the tree is the plugin, e.g. that `.claude-plugin/plugin.json` or the plugin's context id is present.

### f4 Minor observation: two items of one batch that retire ids enforced by one decision leave the second retirement out of the successor
- item: b741
- where: scripts/decision_successor.py:777
`lay` passes over a decision whose status is not `accepted`. Say items A and B of one batch each retire an id that decision D names under `enforced_by`. A's lay writes D's successor and sets D `superseded`. B's lay then skips D, so the successor still names B's retired id under `enforced_by`. If A is later parked, `unlay` sets D `accepted` again, even though B's retirement still leaves it unenforced. r173 and r174 each name one item, so this is an edge no line covers. Reproduction: lay two items whose blocks both retire `work-queue#r1` while 0001 says `enforced_by: [work-queue#r1]`, then read the successor's `enforced_by`.

### f5 Minor observation: `spec explain` says a verb of several two-slot frames with the first frame's preposition
- item: b742
- where: scripts/model_explain.py:830
`self.oblique.setdefault(verb.term.term, ...)` keeps the words before the second slot of the first frame that has more than one slot. A verb with two such frames that use different prepositions (the `list` verb of design_model_check_worlds_frames has three frames) gets its request said with the first frame's word, whichever frame the line used. The world b742 tests has `lodge` with one frame, so it passes. Hardening: pick the frame from the request's operation, or from the kinds of the pair's parts.

### f6 Minor observation: the change is over the review size limit
- item: -
- where: -
`## Size` says 31 files, +1040 -56, which is 1096 changed lines against a limit of 1000.
- **b741** makes the largest share, about 450 lines: `scripts/decision_successor.py` (121), `tests/scenarios/batches_handlers_successor.py` (169), `tests/scripts/test_decision_successor.py` (60), and its feature and corpus blocks.
- **b740** comes next, about 400 lines: `scripts/batch_generator.py`, `tests/scenarios/batches_handlers_generator.py`, its test, and the amend, corpus and handler changes.
