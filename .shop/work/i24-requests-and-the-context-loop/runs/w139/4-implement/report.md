# report w139

## Budget
scripts/supervise.py, scripts/supervise_analysis.py (new), scripts/supervise_worker.py, agents/batch-analyst.md (new), CLAUDE.md, tests/scenarios/supervision_analysis_steps.py (new), tests/scenarios/test_supervision.py. (stub_claude.py not needed, untouched.)

## Changed
- `Run` gains the `Analyses` mixin (`supervise_analysis.py`): after a branch review kept in this run, if no fix work-item is drafted (r74) and the kept `result.json` is readable with empty `questions`, it runs `measure initiative <i>` from the repo root, starts a `batch-analyst` session (stage `analysis`, detached worktree, one brief naming the measurement by absolute path) and copies its `analysis.md` to `.shop/records/<date>-<i>-analysis.md`. Refused measure or missing record: told on stderr, no fault.
- `supervise_worker.py`: `analysis` stage tools (Read, Glob, Grep, `measure` by path); ROLE entry.
- `agents/batch-analyst.md`: new agent, loads analyzing-a-batch, no Edit/Agent.
- CLAUDE.md module-map row. Steps in `supervision_analysis_steps.py`, bound in test_supervision.py.

## Red / green
- Red: `python3 -m pytest -q -n 0 -k measure_initiative_is_run_on_the_initiative` -> `AssertionError: ([{... 'event': 'end'}], [], '')` (review ended, no measurement): the Then, after Given/Then steps were defined.  Before the steps: StepDefinitionNotFoundError for both scenarios.
- Green: `python3 -m pytest -q -n 0 --work-item w139`: 144 passed, 1 skipped (both r75, r76 pass). `tests/scripts` and `--work-item w139 --whole-suite tests/scenarios/test_supervision.py`: 134 passed, 16 xfailed (other open work-items' scenarios), 5 xpassed, 0 failed.
- Suite at start: 794 passed, 2 failed (the two r75/r76 scenarios) at ff2a18e, plus listed expected failures.

## Tests changed under an allowance
none

## Open questions
- r75's "after the branch review was kept" is shown by the measurement file being no older than the kept review's brief.md and one review-end logged; stronger ordering unchosen.
- A kept review with no readable result: no measure (decision 1), exit 0 as before. A same-day re-measure is refused and gives no analysis. Analysis cost unrecorded. Per the plan, unchosen.

## Other
Plan contained no code. `tools size --limit 300`: prints nothing. Commit: 2fba3c1.
Files: CLAUDE.md, scripts/supervise.py, scripts/supervise_worker.py, scripts/supervise_analysis.py, agents/batch-analyst.md, tests/scenarios/supervision_analysis_steps.py, tests/scenarios/test_supervision.py.
