## Budget
tests/scripts/stub_claude.py (added to the file set by the coordinator's answer). Earlier commit 482257b0 holds the steps (tests/scenarios/supervision_faults_steps.py).

## Changes
- 482257b0 (earlier stage): Given and four Thens for r214-r216; scripts/supervise_faults.py unchanged (reading A).
- This stage: stub_claude.py gains `git_retry`, used by `bash` for git commands and by the `elsewhere` commit: retried for up to 10 s while index.lock is held. Cause of the flake: under -n auto the stub's git add/commit raced with work run's git status holding index.lock, the stub died after writing the file, and p2's gate round was faulted for an uncommitted change.

## Runs
- Start: pytest --work-item w237 failed 2 of 3 under -n auto (flaky, the lock race): `2 failed, 181 passed`. Suite record: 1083 passed, 1 failed (the r215/r216 scenario, plus expected failures).
- Final: `183 passed, 1 skipped` for --work-item w237, three runs in a row; tests/scenarios/test_supervision.py and tests/scripts: 182 passed, 1 skipped.

## Tests changed under an allowance
none

## Open questions
none

Plan contained no code. `tools size`: prints nothing (stub_claude.py 289 lines).
