---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-60/review-1
kind: review
batch: batch-60
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/84
head: 2226e3dffaa684e4c7a259936478f8d30693afd9
range: ad65110d9a6537a8bee13324a37757895fe35dce..2226e3dffaa684e4c7a259936478f8d30693afd9
result: fix-now
---

# batch-60 review 1

## Verdict

The batch builds every requirement line of b458, b461, b281, b452, b456 and b355, and b455's chore. It does not pass its own checks: `tools check` exits 1 at Head and exited 0 at the base. Ruff finds one error in b452's code and one in b458's code, so there are two findings to fix. Four observations follow and do not hold the merge.

## Findings

### f1 Minor fix now: ruff I001 in spec parse --item's import block
- item: b452
- where: scripts/model_report.py:81
`python3 scripts/tools check --base ad65110d9` exits 1 at Head and exited 0 at the base. One of the two errors comes from b452's commit ebd23517b:
```
scripts/model_report.py:81:9: I001 [*] Import block is un-sorted or un-formatted
```
The block is the function-local `import argparse` / `import spec_preview` that `cmd_parse` added for `--item`. The batch leaves the check failing, so the change cannot merge with a clean check. Fix: run `ruff check --fix scripts/model_report.py` (or reorder the block the way ruff wants) on batch-60-b452, with `Finding:`.

### f2 Minor fix now: ruff PERF102 in the amend scenario handler
- item: b458
- where: tests/scenarios/decision_tiers_handlers_amend.py:45
This is the second error behind `tools check` exiting 1 at Head and 0 at the base:
```
tests/scenarios/decision_tiers_handlers_amend.py:45:39: PERF102 When using only the values of a dict use the `values()` method
```
In `for kind, (option, key, value) in GIVEN.items():` the `kind` is never used. Fix: loop over `GIVEN.values()` on batch-60-b458, with `Finding:`.

### f3 Minor observation: the change is over the size limit, mostly because of b355
- item: -
- where: -
`## Size` gives 71 files, +2779 -150, against a limit of 1000 changed lines. b355 makes the largest share, about 850 lines: adapter_tables.py (114), backlog_adapter.py (209), drafting_handlers_adapter.py (191), batches_handlers_adapter.py (96), test_backlog_adapter.py (103), plus its cli.toml, docs, features and backlog_section changes. Next come b458 (decision_amend.py, its handler, readiness_handlers_decision.py, decision_write.py: about 300 lines), b281 (backlog_note.py and its generated scenarios: about 300 lines) and b461 (about 210 lines).

### f4 Minor observation: the adapter unlay can drop or restore the wrong operation table
- item: b355
- where: scripts/backlog_adapter.py:202
`unlay` puts back the newest version git holds whose state of the operation differs from the current one. If there is none, it falls back to "no table, not unexposed". Two cases give a wrong result:
- An item exposes a table identical to the one the contract already holds. Every version then equals the current one, so unlay removes a table the contract held before the item. That is data lost.
- A commit after the lay changes that operation's table, for example `spec annotate` rewriting its `requirements` (which the lay drops when it replaces a table). The newest differing version is then the lay commit's, so unlay puts the parked item's own table back. `batch_parked.tested_tree` unlays on a task's head, which can hold such a commit.

Both inputs are rare today. The fix is to unlay against the version at the commit before the lay (the base of the batch, as `as_laid` reads items) instead of "the newest different one".

### f5 Minor observation: work merge refuses a successor that is itself or closed, which no line asks for
- item: b281
- where: scripts/backlog_note.py:45
items#r33 and r34 refuse only a closed item. The model declares only `refused: item closed` for `backlog.merge`. The code also refuses a successor that is the item itself or is delivered, refused or withdrawn. Separately, `work annotate` and `work merge` refuse an `in-batch` item, which r38 and r39 neither name nor forbid. These refusals are sensible guards, but they are untested behaviour that the spec does not record. A later item should give them lines, or at least declared refusal reasons on `backlog.merge` in spec/model/tracking.md.

### f6 Minor observation: an amendment that adds nothing new fails as a git error
- item: b458
- where: scripts/decision_amend.py:83
Reproduction: `work decision --amend 0049 --enforced-by migration-tools#r27`, where decision 0049 already names that id. `amended()` leaves the text as it was and the index is rendered the same, so `shop_files.committed` runs `git commit` on unchanged files. The command is then refused with git's "nothing to commit" instead of completing or saying the decision already names the id. Fix: when the text is unchanged, return without committing, or refuse naming the id as already held.
