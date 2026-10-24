# Review of w127

**Verdict: DONE.** No Critical or fix-now finding in w127's commits. One Minor observation: the report says something false about the r8 delivered scenario. That scenario is w128's, it fails at HEAD, and it failed the same way before w127.

## Commits reviewed

The branch `work/w127` is gone. The commits are those between `07120b5 work: w127 ready -> claimed` and `727a805 work: w127 claimed -> done` on HEAD, less `work run`'s `work:` commits:

- `fce7a8c` work outcome refused in the asker's turn; work turn sets awaiting-asker and awaiting-upstream (requests r7 r15-r18). It changes `scripts/workqueue_request.py` (+15/-4) and `tests/scenarios/requests_steps.py` (+42/-4).

The implementer's result lists only `fce7a8c`, so the two match. Both files are in the work-item's fileset. `5c686c2` (w133 planned -> ready) is `work run`'s own commit.

## Removed and weakened tests

None. I searched the diff for removed `def test_`/step functions, dropped parametrize or Examples rows, removed or loosened `assert`s, and added skip/xfail. I found none, and `git diff 07120b5 HEAD -- features/` is empty.

- The shared Given `a_request` was refactored into `write_request` and given a `context` fixture. Its no-outcome test widened from `== "that has no line outcome"` to `fullmatch("that (has|have) no line outcomes?")`. This is a Given and holds no assertion. It now reads the plural text of r15, which before wrote a bogus outcome. Every singular text reaches the same branch as before.
- I checked whether the new per-line Given and the shared Given could both match one step text. They cannot: the shared pattern needs a space after `lines?`, and the r17 text has a comma there.

## Allowances

The report gives none ("none"). There are no rows to verify, and no test was changed in a way that would need one.

## Cannot verify

- The report's "149 passed, 1 skipped (--work-item w127)" over the whole suite: I did not run the whole suite. `--work-item w127` on `tests/scenarios/test_requests.py` gives 7 passed: r15, r16, both r7 rows, both r17 rows and r18.
- The report's "Suite at start: 752 passed, 7 failed".

## Findings

### 1. Minor, observation (w127's report): the r8 delivered scenario does not pass, contrary to the report

- **Where:** `runs/w127/4-implement/report.md:13`. The code is `scripts/workqueue_request.py:104-105`, which w127 did not change.
- **What is wrong:** the report says "The r8 delivered scenario (w128) passes with the code as it is". It does not pass. `turn`'s settled branch sets `accepted` whatever the status was before, so a `delivered` request goes back to `accepted`.
- **Reproduction:** `python3 -m pytest -p no:cacheprovider -n 0 -q tests/scenarios/test_requests.py --work-item w128` gave `FAILED test_the_upstream_ending_its_turn_on_a_delivered_request_with_every_line_accepted_leaves_the_status_delivered` (AssertionError in `status_is`), 1 failed, 5 passed.
- **Not caused by w127:** `git show 07120b5:scripts/workqueue_request.py` has the same branch at lines 99-100. w127 kept that branch unchanged, as plan D4 says.
- **Why it matters:** w128 is `green` while one of its r8 scenarios fails, and w127's report would lead a reader to think that case is covered.
- **Fix:** w128's own work (a delivered request keeps its status in the settled branch, per r8's "that is not `delivered`"). In w127, only the report line is wrong.

### Checked, no finding

- **r16:** `outcome` raises `Refused` inside `edit`, before `workqueue.committed` is called (`_change` lines 51-52). So nothing is written or committed, and `work` maps the refusal to exit 1 (design-decision/exits-are-successful-or-errors). It refuses only in the asker's turn, because a line outcome is the upstream's part (r5).
- **r17 / r18:** passing to the upstream sets `awaiting-upstream`. Passing to the asker sets `awaiting-asker` unless every line is settled, and then r8/r9 apply. This matches the lines as written, including a `delivered` request with a line not settled (r17 does not exempt delivered).
- **Code no line asks for:** none. Every observable change (the refusal, the two statuses) serves r16, r17 or r18. The refusal's wording is mechanism.
- **Size:** `workqueue_request.py` is 131 lines and `requests_steps.py` is about 115. `tools size --limit 300` printed nothing.

## Checks

- `tools check --base 07120b5…`: ruff "All checks passed!"; vulture "clean"; import-linter "the project states no import contracts".
- `tools size --limit 300`: no output, so no file is over the limit.

## Commands run

- `git log --format='%H %s' --grep="^work: w127 "`; `git log --oneline -15`
- `git log --stat 07120b5..727a805`; `git diff 07120b5 fce7a8c`; `git diff 07120b5 HEAD -- features/`
- `git show fce7a8c:scripts/workqueue_request.py`; `git show 07120b5:scripts/workqueue_request.py | grep -n ...`
- `grep -n ... features/requests.feature`
- `python3 -m pytest -q tests/scenarios/test_requests.py --work-item w127` gave 7 passed
- `python3 -m pytest -n 0 -q tests/scenarios/test_requests.py --work-item w128` gave 1 failed (the delivered r8 scenario), 5 passed
- `python3 -m pytest --collect-only -q tests/scenarios/test_requests.py`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 07120b5683a3e083ee73948dcb07f5f0f13fdd8d`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
