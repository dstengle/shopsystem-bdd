# Review of w149: work turn on a delivered request leaves it delivered

**Verdict: DONE.** No Critical finding, none triaged fix now. The one-line guard does what r8 and r9 now say, and nothing beyond it.

## Commits reviewed

The branch `work/w149` is gone, so the commits are the ones between `d2c0ffd work: w149 ready -> claimed` and `9c8bbfd work: w149 claimed -> done` on HEAD, leaving out `work:` commits (f3fde06 is w150's):

- `d4be501 work turn: the upstream ending its turn leaves a delivered request delivered (r8, r9)`: scripts/workqueue_request.py, +2 -1.

These match the implementer's result.json (`commits: [d4be501 ...]`). Outside `.shop/`, the diff `d2c0ffd..9c8bbfd` touches only scripts/workqueue_request.py, which is the work-item's fileset.

## The change

In scripts/workqueue_request.py:107-108, `turn()` (the upstream's branch, every line settled) now sets `accepted`/`refused` only when `field(text, "status") != "delivered"`. In every case the turn still passes to the asker (r7, line 111), and `_change` still commits the request (r12). If any line's outcome is not settled, the request goes to `awaiting-asker` as before (r17 has no `delivered` exception, plan D2). This matches r8 and r9 as worded ("a request that is not `delivered`"), and it matches plan decision 1.

Risk checked: whether the name `field` is shadowed inside `turn`. It is not. `field` is the module function at line 42, and `edit` has no local of that name.

## Removed and weakened tests

None. `git diff --stat d2c0ffd 9c8bbfd -- tests features` is empty: the commits change no test function, no parametrize case, no assertion, no skip or xfail, and no feature file.

## Allowances

The report's `## Tests changed under an allowance` says "none". That holds, since no test changed.

## Cannot verify

- The report's full-suite figures ("813 passed, 1 failed at start"; "145 passed, 1 skipped" for `--work-item w149`). The suite was not rerun, per the brief. I reran only the focused probes listed below.
- The implementer's result.json gives its report path as `/tmp/.../w149/.shop/scratch/3-implement/report.md`, which is the implementer's own worktree. The report in the stage directory is what I read.

## Findings

None against these commits.

Not a finding of these commits, but a note for the coordinator (spec level, already named in plan D3): in the usual sequence (`work resolve`, then the asker's `work turn`, then the upstream's `work turn`), r18 sets `awaiting-upstream` on the asker's turn and overwrites `delivered`. The upstream's turn then sets `accepted` under r8. So `delivered` survives only an upstream turn taken straight after resolve. Closing that gap needs a line under r18 through integrating-a-proposal. It is not code missing from w149.

## Commands run

- `git log --format='%H %s' -1 --grep="^work: w149 ready -> claimed$"` gave d2c0ffd (`work/w149` is an unknown revision)
- `git log --format='%H %s' -1 --grep="^work: w149 claimed -> done$"` gave 9c8bbfd
- `git log --oneline -12`, `git show d4be501`, `git diff --stat d2c0ffd 9c8bbfd`
- `git diff --stat d2c0ffd 9c8bbfd -- tests features`: empty
- `python3 -m pytest -q tests/scenarios/test_requests.py`: 3 passed
- `python3 -m pytest -q --work-item w149 -k delivered`: 1 passed
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base d2c0ffd...`:
  - ruff: All checks passed!
  - vulture: clean
  - import-linter: the project states no import contracts
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: no output, so no file is over the limit
- grep over spec/capabilities/requests.md and features/requests.feature for r7/r8/r9/r12/r17 and the delivered scenario
