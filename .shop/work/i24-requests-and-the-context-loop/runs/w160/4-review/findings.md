# Review of w160: work retry back to green runs the done check (F5)

**Verdict: DONE.** No Critical finding, none triaged fix now. One Minor lint finding.

## Commits reviewed

Branch `work/w160` is gone; commits taken between `804d543 work: w160 ready -> claimed` and `147611d work: w160 claimed -> done` on the checked-out history, less `work run`'s `work:` commits (w157/w158/w159 moves of side-by-side work-items, and w160's own done move):

- `d04cc02 work retry back to green runs the done check (F5)`: `scripts/workqueue.py` +11 −7.

The implementer's result lists `9a83476` with the same subject. `9a83476`'s parent is the ready -> claimed commit, and `git diff 9a83476 d04cc02 -- scripts/workqueue.py` is empty: the same change, rebased onto the interleaved `work:` commits when merged. Not a finding.

The change: a helper `moved_to(root, path, name, after, message, by)` holds the done check that `withdraw` had inline (`workqueue_done.becomes` before the move, `mark` and `initiative.md` in the commit when it is true). `withdraw` and `retry` both call it. Risk checked: that `withdraw` behaves differently after the refactor. Read: same predicate, same `rels`, same message, same `by`; `retry` passes `found[0]`, whose `parent.name` is the `initiative` it used before. Equivalent.

## Removed and weakened tests

None. `git diff 804d543 147611d --stat -- features tests` is empty. No test, parametrize case, assertion, skip or xfail touched.

## Allowances

The report's `## Tests changed under an allowance` is "none". Nothing to verify.

## Cannot verify

- The report's "Suite at start: 825 passed, 1 failed" — the whole suite was not run here (`work run` runs it).

## Findings

### F1 (Minor) — scripts/workqueue.py:244: ruff I001 on the moved lazy import — triage: drop
`tools check --base 804d543` reports `scripts/workqueue.py:244:5: I001 Import block is un-sorted or un-formatted`, on `import workqueue_done     # imports this module, so it is read here`. The same line (five spaces before the comment) was at line 239 at the base, inside `withdraw`. The commit moved it into the touched lines, so the check now flags it. Matters only for the lint gate's output; behaviour is not affected. Fix: `ruff --fix` (two spaces before the inline comment). Cheap, but it is polish with no effect on behaviour.

No behaviour against r23 or the Purpose: retry now ends the initiative exactly as withdraw does, which is what r23 ("a `work` command's change") asks. No code beyond what a line asks for: the helper only re-homes withdraw's existing r23 behaviour and gives it to retry. D3 (`work run`'s green moves left alone) is a scope choice recorded in the plan and the report, not a change in these commits.

## Probe results

- `tools check --base 804d543`: ruff — 1 error (F1); vulture — clean; import-linter — the project states no import contracts.
- `tools size --limit 300`: no output; `scripts/workqueue.py` is 290 lines.
- `python3 -m pytest -q tests/scenarios/test_work_queue.py tests/scripts/test_work_withdraw.py`: 6 passed.
- `python3 -m pytest -q tests/scenarios/test_work_queue.py -k "retry or sets_the_initiative_to_done" -n 0`: 5 passed.

## Commands run

- `git log --format='%H %s' -1 --grep="^work: w160 ready -> claimed$"` / `... claimed -> done$`
- `git log --format='%H %s' --stat 804d543..147611d`
- `git show d04cc02`; `git show 9a83476 --stat`; `git diff 9a83476 d04cc02 -- scripts/workqueue.py | wc -l`; `git log --format='%H %P' -1 9a83476`
- `git diff 804d543 147611d --stat -- features tests`
- `git show 804d543:scripts/workqueue.py | grep -n "import workqueue_done"`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 804d543...`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- the two pytest runs above
