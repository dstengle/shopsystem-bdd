## Budget
- tests/scenarios/supervision_faults_steps.py
- scripts/supervise_faults.py (untouched)

## Changed
tests/scenarios/supervision_faults_steps.py: the Given (p2's gate round, `round:gate:p2`, meets i1's researcher's start, then writes and commits i2's initiative.md via the stub's `elsewhere` commit form, per the answer: the i2 session's own end takes it in) and four Thens (r214 green/naming, r215 file as changed, r216 no faults, not failed). No production code changed.

## Runs
Red (from research notes, same command): `python3 -m pytest -q --work-item w237`: 3 failed, 180 passed, 1 skipped, all at the undefined Given (StepDefinitionNotFoundError). I wrote the Given and Thens together, as the three scenarios share them, so I did not re-run the red myself.
Green: `python3 -m pytest -q --work-item w237`: 183 passed, 1 skipped, repeated 10 times (also -n 8) all passing, plus test_supervision.py.
Concern: the very first run (cold) had the r215 scenario failing once; I could not reproduce it in ~10 reruns. Suspect: the stub's `git commit` in the main checkout racing with a git index.lock held by i1's run (stub_claude.py, outside the set, uses check=True); then the file stays uncommitted and i2's own round puts it back (reading A). The r215 Then now prints status and log on failure.

Suite at start: 1081 passed, 3 failed (these 3 scenarios), plus expected failures per the brief.
Tests changed under an allowance: none
Open questions: none
Plan contained no code. tools size --limit 300: no output (no file over).
Commit: 482257b0
