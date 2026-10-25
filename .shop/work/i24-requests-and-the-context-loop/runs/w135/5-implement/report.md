# Report of w135 (implement)

## Budget
scripts/supervise_intake.py (new), scripts/supervise_all.py, scripts/supervise_worker.py, agents/initiative-round.md,
CLAUDE.md, tests/scenarios/supervision_intake_steps.py (new), tests/scenarios/test_supervision.py (7 files).
scripts/supervise_brief.py was not touched: `Intake` overrides `brief`.

## What changed
- `supervise_intake.py`: `Intake(Run)` on `.shop/work/requests/`. It has its own `check`, `brief` and `take`. `take` runs the
  round in a worktree on `round/<q>-<k>-intake`, merges it on DONE and commits the round's record. A round that faults or
  does not give DONE raises Refused (r86-r88 style) and merges nothing.
- `supervise_all.run_all`: it checks and takes the intake rounds (requests `open` or `awaiting-upstream`) after the
  initiatives' checks and before their threads. It shares the lock and slots. A faulted round goes into `refused`, so the exit is 1,
  and the other requests and the initiatives are still taken. `work run <initiative>` is unchanged.
- `supervise_worker`: an `intake` tool list (reader plus `work outcome`, `work turn`, `work show`) and no `--work-item` for intake.
- `agents/initiative-round.md`: an `intake` job. `CLAUDE.md`: a module-map row.
- Steps: `supervision_intake_steps.py` (two Givens, two Thens); one import line in test_supervision.py.

## Red and green
- Red: `python3 -m pytest -q -n 0 -k intake_round tests/scenarios/test_supervision.py` gave 2 failed on the Then "an
  `initiative-round` session of the kind intake was started" (no session started for q1), as expected: nothing read requests.
  After the code, the second Then failed once because my Given used an unsubstituted `{scripts}`; fixed in the step.
- Green: the same command, 2 passed. `python3 -m pytest -q --work-item w135`: 144 passed, 1 skipped. Module:
  `--whole-suite tests/scenarios/test_supervision.py` 162 passed; tests/scripts/test_agents.py 8 passed.
- Suite at the start (brief): 838 passed, 2 failed (the two examples of this outline). I did not run the whole suite.

## Tests changed under an allowance
none

## Open questions
- What `work run` prints for the requests it took in (no scenario checks a print).
- A request `open` or `awaiting-upstream` while its turn is the asker's: `work outcome` refuses and the round is a fault.
- A round that ends DONE but leaves a line without an outcome or does not pass the turn: it is taken in again next run.
- Where the question's text goes beyond the round's result.
- The fault path (round not DONE, exit 1 naming the round) is coded as answer 2 asks but no scenario of this work-item
  asserts it, so it is untested.

## Plan contained code
No; nothing pasted.

## Completeness check
`tools size --limit 300` printed nothing.

## Result
A no-initiative `work run` now starts an intake round for each waiting upstream request; the stand-in's `work outcome`
/ `work turn` leave q1 with line outcomes and the asker's turn. Commit: 3b24b69.

## Files changed
CLAUDE.md, agents/initiative-round.md, scripts/supervise_all.py, scripts/supervise_worker.py, scripts/supervise_intake.py,
tests/scenarios/supervision_intake_steps.py, tests/scenarios/test_supervision.py.
