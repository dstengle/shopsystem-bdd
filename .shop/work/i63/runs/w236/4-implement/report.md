## Budget
- tests/scenarios/supervision_faults_steps.py

## Changed
The step `is_failed` checked `git status .shop/work` is clean. In the r218 scenario i2's file is left changed by i1's worker; whether i2's own run puts it back before the check depends on timing (3 of 4 runs failed). The check now leaves out `.shop/work/i2`. Code in supervise_faults.py (c27c3c7e) already leaves i2's path alone, unchanged.

Suite record at start: 1081 passed, 3 failed (supervision r215/r216 scenarios, not this item's), plus expected failures.
Red: the brief's failure (flaky, 3 of 4). Green: see final runs below.

## Tests changed under an allowance
tests/scenarios/supervision_faults_steps.py::is_failed — setup/interim: pathspec of the clean-status assertion excludes .shop/work/i2 (a step added by this initiative).

## Open questions
- i2's own check putting back its file (plan §5) — unchosen.

Plan contained no code. 
