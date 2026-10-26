# findings: review of w198 (i37, retire the deprecated scenarios)

**Verdict: DONE.** Nothing is Critical and nothing is to be fixed now. The commit only deletes: it removes the seven scenarios the Retires section lists and the two step definitions that only those scenarios used.

## Commits reviewed

The branch `work/w198` no longer exists, so the commits were taken from HEAD's history, between `c3474104` (`work: w198 ready -> claimed`) and `8c8cdee0` (`work: w198 claimed -> done`):

- `ac8ed00f` Retire the seven deprecated scenarios of i37 and the two steps only they used. It touches 5 files, with 114 deletions and 0 insertions.

This is the one commit the implementer's result.json lists. There is no difference.

## Changes under features/

Every hunk under `features/` removes a scenario tagged `@deprecated`, and each title matches a Retires entry character for character:

- migration-tools @r15 Outline
- supervision @r75, @r102 and @r105
- work-queue @r1, @r23 (Outline) and @r9 (Outline)

Each scenario's live replacement (the one its `Deprecated for:` line names) is still in the file, unchanged. No other line under `features/` changed. No feature file has a `@deprecated` scenario left; the only matches are the fixture text inside feature-file-tools and design-model-check scenarios.

## Removed and weakened tests

What I searched for: the whole diff, for deleted test functions or step definitions, parametrize cases, `assert` lines, and skip or xfail markers.

- The tests generated from the seven retired scenarios are gone along with them. The scenarios themselves are retired, which is allowed. The plan lists these tests in §4 (Tests the decisions break).
- `tests/scenarios/supervision_integrate_steps.py`, Given step `other_initiative`: it only built fixtures and asserted nothing. Only the deprecated r102 scenario used it. Plan D1 and §2 list it.
- `tests/scenarios/test_work_queue.py`, Then step `drafted`: it asserted that a work-item file has the id, kind and status `drafted`. Only the deprecated r1 scenario used it. Plan D1 and §2 list it. The live r1 scenario checks the same things through the "whose id is" steps in `work_queue_add_steps.py`.

I checked for remaining users of the two removed steps with `grep -rn "is a drafted work-item" features/ | grep -v whose` and `grep -rn "whose kept drafts add .* and whose capability-proposal" features/`. Neither found anything, so no remaining scenario lost a step. No assertion was loosened and no skip or xfail was added.

## Allowances

The report's `## Tests changed under an allowance` says "none". The commit agrees: no test was changed under an allowance.

## Cannot verify

- The report's run results ("10 passed" with `--work-item w198`, `test_bound.py` 1 passed, the integrate `-k` run 2 passed, and a suite of 926 passed at `c3474104`). Per my instructions I did not rerun the suite; `work run` runs it before merging.
- The report says the retirements were done with `features retire` rather than by hand. The result looks the same either way: each hunk is exactly one whole scenario block.

## Findings

### 1. Minor: ruff and vulture hits that were already there, in a file the commit touched (drop)
- **Work-item:** w198
- **Where:** `tests/scenarios/test_work_queue.py:7` (ruff I001, import block unsorted) and `:235` (vulture, unused `name2` in `status_is`).
- **What is wrong:** `tools check --base c3474104` reports both, because the commit touched this file.
- **Why it is not this commit's:** both lines are unchanged from `c3474104`. The import block is identical, and `status_is` was at line 241 before the 6-line deletion moved it up.
- **The fix:** sort the imports and rename `name2` to `_name2`, the next time a work-item owns this file.

### 2. Observations carried from research and plan (not this commit's; already named for a follow-up)
The notes' §6 lists three defects, each with a reproduction: the branch-review fix loop has no bound (D1), a `questions` value given as one string is dropped (D2), and an analysis that was cut short is never retried (D3). They are outside w198's `accepts` and Retires. The plan and the report both leave them for a follow-up work-item. This commit's diff does not touch them.

## Checks

- `tools check --base c3474104`:
  - ruff: 1 error (I001, test_work_queue.py:7, already there)
  - vulture: 1 (test_work_queue.py:235, already there)
  - import-linter: "the project states no import contracts"
- `tools size --limit 300`: printed nothing, so no file is over the limit.

## Commands run

- `git log --format='%H %s' -30 | grep -n -E 'w198|ac8ed00f'` and `git log --format='%h %s' -12`
- `git show --stat ac8ed00f` and `git diff c3474104 ac8ed00f`
- `grep -rn "is a drafted work-item" features/ | grep -v whose`
- `grep -rn "whose kept drafts add .* and whose capability-proposal" features/`
- `grep -rn "@deprecated" features/` and `grep -rn "(deprecated)" tests/`
- `python3 <Scripts>/tools check --base c3474104c62800e8fc794aaf33047ce392019617`
- `python3 <Scripts>/tools size --limit 300`
- `git show c3474104:tests/scenarios/test_work_queue.py | sed -n '1,20p;236,245p'` and `sed -n '1,20p;228,240p' tests/scenarios/test_work_queue.py`
