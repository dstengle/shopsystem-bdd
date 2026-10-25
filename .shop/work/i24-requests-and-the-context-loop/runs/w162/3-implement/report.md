## Budget
No file edited (stopped before any edit).

# Report w162: HAND-BACK

Stop condition: a scenario the work-item accepts passes before any code is written, and the one scenario that would be red does not exist in `features/`.

Evidence:
- `python3 -m pytest -q --work-item w162` -> `144 passed, 1 skipped, 36 warnings, 56 subtests passed`. Every accepted scenario of r79 is green today.
- `grep` of `features/supervision.feature` for the plan's new scenario ("a proposed initiative whose fulfils names a request the queue does not hold ...") finds nothing.
- The plan (Decision 2, section 2) has me add that `@r79` scenario to `features/supervision.feature`. My rules forbid editing or committing any `.feature` file; only `formulating-features` writes features. So the red scenario cannot come from me.

Needed: the scenario added through a formulation round (tagged `@r79`, as the plan describes), then the work-item re-run. The code change is then: in `scripts/supervise_rounds.py`, read the fulfilled request's accepted lines before `start_initiative`/the round branch, so a missing request refuses with nothing changed; plus one new opening step in `tests/scenarios/supervision_rounds_steps.py`.

Scenarios green: both r79 scenarios. Red: none (the new one is absent).
Suite at start: 848 passed, 0 failed at 4cbd265.
Plan contained code: no.
Tests changed under an allowance: none. Open questions: the plan's Open cases (D2 empty lines, D3 uncommitted DONE integrate stage dir) remain unchosen.
Commits: none. Files changed: none.
