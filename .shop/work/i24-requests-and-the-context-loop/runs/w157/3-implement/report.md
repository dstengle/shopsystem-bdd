## Budget

- scripts/supervise_answers.py
- tests/scenarios/supervision_delegation_steps.py
- tests/scripts/stub_claude.py

## Changed

- `answers()` commits each answer as soon as it is written (D1). The closing commit now happens only when something is uncommitted (new `uncommitted()`), so it never fails on an empty commit.
- Four new steps (two-question Given, answers-per-question Given, the "given to a/another session" Then). The stand-in picks a step by a `question:<Q>` plan key (D2); its docstring says so.

## Red and green

- Red: `python3 -m pytest -q --work-item w157` gave 1 failed, 144 passed. The scenario was red for missing steps first. With the steps in place it failed on its Then line: `ValueError: not enough values to unpack` on w1's answer. The run's stderr said "w1.md changed in the repository's own checkout and not committed; work run put it back", which is the expected defect.
- Green: the same command plus `tests/scenarios/test_supervision.py` and `tests/scripts` gave 144 passed, 1 skipped. `test_supervision.py` alone gave 3 passed.
- Suite at the start: 823 passed, 1 failed (this scenario's test, plus the expected failures the brief lists).

## Tests changed under an allowance

none

## Open questions

- A second answer whose commit or push fails after the first is committed and pushed.
- Whether a fault in a later session should mention the already-committed first answer.
- The push at the end of `answers()` is kept; it is redundant after the per-answer pushes.

## Other

- The plan contained no code.
- `tools size --limit 300` printed nothing.
- Commit: c4db04a.
- Someone can now have two questions of one work-item answered in a single `work run`.
- Not covered by the scenario: D3 (a refused `measure initiative` still exits 0) is left alone, as the plan says.
