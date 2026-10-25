# Review of w140: work answer answers a capability-proposal's question and commits it

**Verdict: DONE.** Nothing is Critical and nothing is triaged fix now. There are two Minor findings.

## Commits reviewed

- The branch `work/w140` is gone. The commits are the ones between `ac6cd13 work: w140 ready -> claimed` and `8a79d9c work: w140 claimed -> done` on HEAD, less `work run`'s `work:` commits (ecd3386, c10f66f, 52923ad belong to other work-items). That leaves one commit:
  - `2a2c0de work answer answers an awaiting-answer capability-proposal and commits its file`
- The implementer's result lists `862a5f8`. That commit exists, and it has the same message, author, date and stat as 2a2c0de: it is the same change rebased onto the main line. This is not a difference in content.
- Files changed: README.md, scripts/work, scripts/workqueue_answer.py, tests/scenarios/work_queue_answer_steps.py. All four are in the work-item's fileset. Nothing under `features/` changed.

## Removed and weakened tests

None. What I searched for in the diff: deleted `def test_`/step functions, removed `assert`s, parametrize or Examples changes, skip/xfail markers, and step text changes. The only test change is one added `@given` step, "an initiative {ident} under .shop/work/ whose capability-proposal {name} is {status}". It is new.

## Allowances

The report says "none", and the commit uses none.

## Cannot verify

- That the whole suite passes. It was not run here, as the brief says, and `work run` runs it. The focused run of `-k "answer or commits"` gave 10 passed.
- The report's "Red" run (2 failed before the change). It cannot be seen from the commit.
- The open case the implementer reported: `scripts/model_work.py`'s capability-proposal statuses lack `awaiting-answer`, so `model check` would flag an awaiting-answer proposal. That file is outside this work-item's fileset and outside work-queue's lines. It is not judged here, but it should be picked up by the model capability's work.

## Findings

### F1. Minor: observation. scripts/workqueue_answer.py:33. The capability-proposal is detected by a raw substring match
- **What is wrong.** The code tells a proposal from a work-item with `"\nkind: capability-proposal\n" in <header text>` instead of the frontmatter parser `workqueue.frontmatter` that `agrees()` already uses.
- **Why it matters.** A proposal whose `kind` value is written in another valid form (quoted, or with trailing spaces) is not recognised. It then takes the work-item path and is refused by `asked_from` ("log.jsonl gives no transition…"). The result is a refusal, not a wrong write. No client writes such a file today: `item_text` and `work` write `kind: capability-proposal` exactly.
- **Reproduction.** This comes from reading the code only. I did not run it, because the review's shell allows no ad-hoc Python, and no scenario exercises such a file.
- **Fix.** `proposal = workqueue.frontmatter(workqueue.read(path, root))[0].get("kind") == "capability-proposal"`.

### F2. Minor: drop. scripts/workqueue_answer.py:1 and :25-27. The docstrings were not updated
- **What is wrong.** The module docstring cites only r9, r13 and r14 and speaks of "a work-item's question". `answer()`'s docstring still says it returns the work-item to the asking stage. Neither mentions r24 or capability-proposals.
- **Why it matters.** Readers can be misled. Behaviour is not affected.
- **Fix.** Name r24, and say what happens to a capability-proposal.

### Risks checked
- **The behaviour against r24, r9, r7 and r15.** The one-line check still runs first. `agrees()` still refuses a status that is not awaiting-answer, and its refusal text now names both kinds. A proposal keeps its status `awaiting-answer`, gets no `move` and no log line, and its commit holds only its own file. This matches r9's "the log.jsonl line the change made, if it made one". The work-item path is unchanged.
- **A proposal with no log.jsonl.** `agrees()` returns the file's status when `last_logged` is None (workqueue.py:191-195), so the proposal passes. This is the plan's D2.
- **Code that no requirement asks for.** The output `p1 awaiting-answer` comes from the existing `cmd_answer`, and the commit message `work answer: p1` is mechanism. I found nothing new that no requirement asks for.

## Commands run
- `git log --oneline -25 --grep=w140`, `git log --oneline -8`, `git log --oneline ac6cd13..8a79d9c`
- `git show --stat 862a5f8`, `git show --stat 2a2c0de`, `git show 2a2c0de`
- `grep` on spec/capabilities/work-queue.md, scripts/workqueue.py and scripts/work
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base ac6cd13`: ruff "All checks passed!"; vulture "clean"; import-linter "the project states no import contracts"
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: printed nothing, so no file is over the limit
- `python3 -m pytest -q tests/scenarios/test_work_queue.py -k "answer or commits" -p no:cacheprovider`: 10 passed
