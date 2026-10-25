# Review of w159: model check takes awaiting-answer proposals and withdrawn requests as the statuses they are

**Verdict: DONE.** Nothing is Critical and nothing is to be fixed now. One Minor finding: the move left an import unused. The commit does what the plan says, and the r27 rows are green.

## Commits reviewed

The branch `work/w159` is gone. The commits are those between `5ce32c7 work: w159 ready -> claimed` and `1e48fde work: w159 claimed -> done` on HEAD, less `work run`'s `work:` commits. Other work-items' commits are interleaved in that range: d04cc02 (F5, workqueue.py) and 6e6d314 (r77, supervise_answers.py). They touch none of w159's fileset and are not w159's. The one w159 commit:

- `460e639` model check: awaiting-answer proposals and withdrawn requests are in their lifecycles (r27). It changes scripts/model_work.py, tests/scenarios/design_model_check_problems.py, tests/scenarios/design_model_check_records.py (new) and tests/scenarios/test_design_model_check.py.

The implementer's result lists `11d8024`. That commit still exists. `git diff 11d8024 460e639 --stat -- scripts tests` shows only the other work-items' files, so for w159's four files 460e639 is 11d8024 replayed when it was merged. The commits match and there is no finding here. All four files are in the work-item's fileset.

## Removed and weakened tests

None. I looked for deleted test functions or steps, dropped parametrize or Examples rows, loosened or removed asserts, and added skip or xfail markers.

- `malformed_record` (the Given "a repository in which {case}") moved from design_model_check_problems.py to design_model_check_records.py. I compared the two texts line by line: every existing branch is unchanged, and so is the final `assert case == ...`. The only additions are two `elif` branches for the new rows.
- features/ is unchanged.
- The focused run of the move's users (r27, r29 and r110 rows) passed: 11 passed.

## Allowances

The report's `## Tests changed under an allowance` says "none". That holds, because the moved step is unchanged for its existing rows.

## Cannot verify

- The report's red run (2 failed before the code change). It was not re-run, because that would need the tree at an earlier revision. The plan's probe P1 and the diff are consistent with it.
- The report's whole-suite figures (263 passed, 1 xfailed, 4 xpassed; 833 passed at start). `work run` runs the suite itself.

## Findings

### F1. Minor (observation): `CONTEXT` is imported but no longer used in design_model_check_problems.py
- **Where:** tests/scenarios/design_model_check_problems.py:6, `from .conftest import CONTEXT, I1, P1, THING, cap, feature, full`.
- **What is wrong:** `CONTEXT` was used only by `malformed_record`, which moved out. The plan said that "helpers and imports that only `malformed_record` used ... leave with it". `re` is still used in the module, but `CONTEXT` is not.
- **Why it matters:** `tools check` reports it under ruff as F401, so a ruff finding is new with this commit.
- **Fix:** remove `CONTEXT` from the import.
- **Reproduction:** `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 5ce32c7…` prints `tests/scenarios/design_model_check_problems.py:6:23: F401 `.conftest.CONTEXT` imported but unused`. A grep for `CONTEXT` in the module matches only line 6.
- **Work-item:** w159.

### Note (no finding): I001 on tests/scenarios/test_design_model_check.py:7
Ruff also reports an unsorted import block in test_design_model_check.py. The block was already out of order before this commit (`requests` comes before `reading`). The new `records` line was added after `reading`, which leaves the block no more out of order than it was. The ruff findings in workqueue.py, supervision_delegation_steps.py and stub_claude.py come from other work-items' commits in the range.

### Behaviour
- In `STATUSES`, awaiting-answer is now in the capability-proposal's lifecycle and withdrawn is in the request's. Both are what r27 ("a status ... not in its kind's lifecycle") and the scenario's Pins line ask for.
- No other kind changes, and `SETTLED` is unchanged. The row "status built" still keeps the capability-proposal's set closed.
- I found no code that no line asks for.

## Checks
- `tools check --base 5ce32c7`:
  - ruff: 6 findings. One is w159's (F1). The I001 in test_design_model_check.py was there before this commit. The rest come from other work-items.
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: prints nothing. No file is over the limit.

## Commands run
- `git log --format='%H %s' -1 --grep="^work: w159 ready -> claimed$"` (and the same for `claimed -> done`), `git log --oneline -15`
- `git log --stat --format='%H %s' 5ce32c7..1e48fde`
- `git show 460e639`, `git show --stat 11d8024`, `git diff 11d8024 460e639 --stat -- scripts tests`
- greps of design_model_check_problems.py, tests/scenarios/conftest.py, design_model_check_requests.py, features/design-model-check.feature and spec/capabilities/design-model-check.md
- `python3 -m pytest -q -p no:warnings tests/scenarios/test_design_model_check.py -k "lifecycle or malformed or file_name or w_n"`: 11 passed
- `python3 -m pytest -q -p no:warnings tests/scenarios/test_design_model_check.py -k lifecycle -v`: 3 passed
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 5ce32c7211837cba0f4123637c636206cfeafb91`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
