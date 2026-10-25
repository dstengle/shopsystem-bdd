## Budget

- scripts/workqueue_start.py
- tests/scenarios/work_queue_start_steps.py
- tests/scenarios/work_queue_git_steps.py

## Changed

- `workqueue_start.start` writes through `workqueue.committed` (commit of the new initiative.md only); a refused commit leaves no empty directory; a non-git directory is refused before writing.
- The request Given writes `spec/index.md`; the git Then steps resolve "the new initiative's initiative.md" / "...directory under .shop/work/" to the one new initiative (asserting exactly one, directory exists).

## Red / green

- Red: `python3 -m pytest -q --work-item w166` -> r25 fails: "work: spec/index.md, which names the context, is missing" (Given lacked index); after the step fix, fails on the Then: no new commit (`ca02377 the repository as the scenario gives it` only). Expected: start did not commit.
- Green: `python3 -m pytest -q --work-item w166` -> 143 passed, 1 skipped. `tests/scenarios/test_work_queue.py` -> 1 passed (only one test collects there, as the plan noted; no test for r22 collects, so r22 was not run).
- Suite at start: 849 passed, 1 failed (the r25 test) plus the listed expected failures.

## Tests changed under an allowance
none (setup of the r25 scenario's Given is a step definition for that scenario itself)

## Open questions
- Detached HEAD: counts as "the current branch"? Unchosen (committed commits there).
- Commit refused (e.g. no git identity): rollback by `committed` and directory removal, not probed by a test.
- D1: existing `.shop/work/i<n>/` with no initiative.md crashes with FileExistsError; not fixed here.

The plan contained no code. Size: `tools size` printed nothing.

Someone can now run `work start q1` and find the initiative committed on the current branch.

Commit: 9b8def0e. Files: the three above.
