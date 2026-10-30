# Review of w232, round 7 (the fix for round 4's finding 1)

**Verdict: DONE.** The commit does what the answer asked: `work show <request>` now lists every line of the request, and a line with no line outcome is shown as `unsettled` (work-queue#r59). Nothing under `features/` changed, no test was removed or weakened, and no finding is Critical or fix now.

## Commits reviewed
- cb26926247a31f6adf5067b10507f6e8b7603d77, "work show of a request lists every line, an unsettled one as unsettled (r59)". It touches:
  - scripts/workqueue_list.py: +1/-3
  - tests/scripts/test_work_show_request.py: new, +22
- The implementer's result names d32ec491. `work run` merged it as cb269262, on top of 7f7dab72. `git diff d32ec491 cb269262 -- scripts tests features` is empty, so the code and tests are the same. The rest of the difference between those two commits is other initiatives' `.shop/` files.
- Suite: taken from the brief's record, 1088 passed and 0 failed at cb269262. That is the 1087 of the earlier run plus the new test. The expected failures are the same requests, supervision and work-queue scenarios as before, none of them this work-item's.

## Removed and weakened tests
None. In the diff I searched for:
- deleted `def test_` or step functions
- changed or removed `assert` lines
- parametrize cases
- skip or xfail
- changed step patterns

The commit only adds a file of tests: `test_a_line_with_no_line_outcome_is_listed_as_unsettled`.

## Allowances
The report's `## Tests changed under an allowance` says "none". None is needed, because no existing test was changed.

## Cannot verify
- The report's red run, where the new test failed on the old code before the fix. The commit holds the test and the fix together, so that state is not in the history.

## Findings

### 1. Minor, drop: new test file outside the work-item's fileset (w232)
- **Where:** tests/scripts/test_work_show_request.py.
- **What:** the work-item's fileset does not list this file. The report says so under "Outside the file set". The file is a unit test of the case the fix-now answer asked to be tested.
- **Why it is minor:** the module map has `tests/scripts/` for tests of scripts. A scenario step in work_queue_list_steps.py could have covered the case instead, but the fileset is a guide, and nothing behaves differently either way.
- **Fix:** none needed.

### Behaviour and unrequested code
- `unsettled` is the word the answer named for a line with no outcome. It serves r59's "its lines with their line outcomes".
- No other output changed.
- The `--json` form of `work show <request>` (workqueue_list.py:100) is unchanged. It still gives only name, status and turn, as decision D4 of the plan left it; the round 4 review accepted that.
- No code is unrequested.

### Earlier findings (round 4)
- Finding 1, fix now: fixed by this commit. workqueue_list.py:86 now prints every line under `## Lines`.
- Findings 2 and 3, Minor: not touched, as their triage (drop, observation) allows.

## Checks
- `tools check --base 7f7dab72` (the parent of cb269262):
  - ruff: all checks passed
  - vulture: clean
  - import-linter: the project states no import contracts
- `tools size --limit 300`: no output. No file is over the limit.
- `python3 -m pytest -q tests/scripts/test_work_show_request.py`: 1 passed.

## Commands run
- `git show --stat cb269262`, `git show cb269262`, `git show --stat d32ec491`
- `git diff d32ec491 cb269262 -- scripts tests features` (empty)
- `git log --oneline -3 cb269262`
- `grep -n "r59\|r60\|r61" spec/capabilities/work-queue.md`
- `grep -n "def \|json\|Outcomes" scripts/workqueue_list.py`
- `python3 -m pytest -q tests/scripts/test_work_show_request.py`
- `python3 <Scripts>/tools check --base 7f7dab72`
- `python3 <Scripts>/tools size --limit 300`
- reads of the brief, the work-item, the round 6 report, its result and brief, and the round 4 findings
