# w210 report (fix round)

## Budget
scripts/supervise_rounds.py, tests/scenarios/spec_integration_steps.py (2 files).

## What changed
Review findings 1 and 2 only, as the person answered.
- `supervise_rounds.py`: the raise (`raise_before_merge`) now runs before the round's merge, when the result has a change list that r96/r107 would not refuse (those checks still run after the merge). A failed raise calls `undo_round`: drops the round branch (`branch -D`), removes the round's uncommitted stage directory, and rewrites `log.jsonl` as committed plus the other sessions' unlogged lines. No `reset --hard`, no commit; Refused names round, upstream and work's reason.
- `spec_integration_steps.py` `billing_gives_no_refund` (setup): billing's directory is now a git repository, since a raise into a non-repository now removes the stage dir its Thens read (plan part 4's predicted break).

## Red/green
Red: after the reorder, `test_spec_integration.py::...needing_what_the_named_upstream_does_not_yet_give...` failed: `drafts == []`, stderr "the raise of the lines of i1 into .../billing failed: git rev-parse failed: not a git repository" (expected: the stage dir is taken back). Green after the setup change.
Suite at start: 977 passed, 0 failed (expected-failing requests scenarios listed). Final: `--work-item w210` 152 passed, 1 skipped; test_supervision, test_requests, test_spec_integration with `--whole-suite`: 294+2 passed, 26 xfailed.

## Tests changed under an allowance
- tests/scenarios/spec_integration_steps.py `billing_gives_no_refund` (setup): makes billing a git repo; no assert changed.

## Open questions
none new (findings 3 and 4 are observations, not fixed here). Not probed: a failed raise's log.jsonl restore when several initiatives run concurrently.

The plan contained no code. `tools size`: printed nothing.
Commit: 08013f27.
