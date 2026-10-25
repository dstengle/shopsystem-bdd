## Budget

scripts/supervise_worker.py, scripts/supervise.py, scripts/supervise_done.py (new), scripts/supervise_analysis.py, scripts/workqueue_done.py, CLAUDE.md, tests/scripts/stub_claude.py, tests/scenarios/supervision_proposal_steps.py, tests/scenarios/supervision_done_steps.py (new), tests/scenarios/test_supervision.py, features/supervision.feature (retire only)

## What changed
- `MAX_TURNS` research 40 -> 80; the 40-turn deprecated scenario retired with `features retire` (r19).
- `supervise.py`: `pull_through` now calls `review_loop` (review, fix pulled, next review when the fix is green, r110; analysis then `finish`, r109).
- `supervise_done.py` (new, row in CLAUDE.md): `Dones.finish` sets done when `workqueue_done.holds` (new public) and commits/pushes initiative.md + log.
- `supervise_analysis.py`: `analyse` returns True after committing and pushing the measurement and analysis record (`keep_records`).
- Tests: stub plan entry may be a list (one per session); new `supervision_done_steps.py`; r110 steps and r74 Given in `supervision_proposal_steps.py`.

## Red and green
Red (research, before edits): `python3 -m pytest -q <the three node ids>`: 80-turn failed at its last Then (argv `--max-turns 40`); r109 and r110 failed on undefined Givens. I wrote production code before re-running red myself, relying on that run.
Green: `python3 -m pytest -q --work-item w182` -> 145 passed, 1 skipped. `python3 -m pytest -q -p work_items --whole-suite tests/scenarios/test_supervision.py` -> 2 failed (both in the starting failing list: gate-no-question, formulate-with-answers), 183 passed, 14 xfailed, 2 xpassed.
Suite at start: 875 passed, 4 failed at a0be069f.

## Tests changed under an allowance
- tests/scenarios/test_supervision.py `is_green`: step pattern respelled from `{name} is green` to `(?P<name>w\d+) is green$` (setup), because it swallowed the r110 Then "... and it is green". No assertion changed.
- supervision_proposal_steps.py `reviewer_lists` (r74 Given): listed by the plan (decision 4); plan now a per-session list (findings, then nothing).

## Open questions
- Loop bound when each review keeps listing findings and fixes go green.
- Records committed on an earlier run but request delivered later; and unread() sees the records/done commits as unread on a later run.
- Analysis cut short: no records commit, no done.
- w181 adds the same modules/steps (r105 Given "i1 is started and its work-items ..." is now defined here, so r105/r106 scenarios xpass); expect add/add conflicts at merge.

## Outside the file set
none. Plan contained no code. Commit: e4d34ce9.

## Size
`tools size --limit 300` printed nothing.
Files: scripts/supervise.py, supervise_done.py, supervise_analysis.py, supervise_worker.py, workqueue_done.py, CLAUDE.md, tests/scripts/stub_claude.py, tests/scenarios/{supervision_done_steps,supervision_proposal_steps,test_supervision}.py, features/supervision.feature (retire).
