# report of w164 (implement)

## Budget

Files I will touch (14): scripts/supervise_rounds.py, scripts/supervise_change.py (new), CLAUDE.md, scripts/supervise.py,
scripts/supervise_all.py, scripts/supervise_brief.py, agents/initiative-round.md,
tests/scenarios/supervision_integrate_steps.py (new), tests/scenarios/test_supervision.py,
tests/scenarios/supervision_rounds_steps.py, tests/scenarios/supervision_given.py,
tests/scenarios/supervision_review_steps.py, tests/scenarios/supervision_analysis_steps.py,
tests/scenarios/supervision_all_steps.py.

Suite at the start (brief's Suite record): 852 passed, 8 failed at 4910049f; the 8 failing are this work-item's scenarios
(r91 x2, r92, r93, r94, r95, r96, r97).

## What changed
- `scripts/supervise.py`: `pull_through` takes the branch review and measure only when the initiative has a work-item (r94, r97); `commit` takes `also=` paths; `Run` has a `round_lock`.
- `scripts/supervise_rounds.py`: `due` gives the integrate round to a started initiative with no proposal and no work-item that fulfils a request (r93); the proposed-to-started transition only for a proposed one; a DONE integrate's `changes` is read, an empty or malformed one is a Refused naming the round, after `keep_round` has committed its stage directory and drafts (r96); a valid one is written as drafted proposals and committed in the closing commit (r92); integrate/apply/formulate hold `round_lock` (r95).
- `scripts/supervise_change.py` (new, row added to CLAUDE.md): `entries` and `Changes.write_proposals`.
- `scripts/supervise_all.py`: one `round_lock` for all runs (r95, r66 gate rounds stay side by side).
- `scripts/supervise_brief.py`: the integrate brief gives `Drafts path:` and the `changes` form (r91, r92). The drafts need no extra copy: the worker's `here/drafts` is already copied whole into the stage directory, and `keep_round` and the closing commit already commit it.
- `agents/initiative-round.md`: integrate uses the brief's drafts path and gives `changes`.
- Steps: new `supervision_integrate_steps.py`; added to `supervision_given.py`, `supervision_review_steps.py`, `supervision_analysis_steps.py`, `supervision_all_steps.py`, `test_supervision.py` (import), `supervision_rounds_steps.py` (`proposed_fulfilling` takes a status).

## Red and green
- r94, r97: `python3 -m pytest -q -n 0 tests/scenarios/test_supervision.py -k no_workitem`: red on the Then (`measurement(repo)` held `.shop/records/measurements/2026-10-25-i1.md`; a review ran); green after the `pull_through` guard (2 passed).
- r93, r96: red, `([], '', '')` (no integrate round) and the missing "names the round" assertion; green after `due`/`round` (passed).
- r91 (x2), r92: red first showed as a TypeError in my own step, fixed; I did not see them red on their Then lines (the researcher's probes c4-c6 show the old behaviour); green with the above.
- r95: first run passed because the stand-in had no way to make rounds overlap; added `linger` to the stand-in, then red: `[('apply','p3',0,3),('apply','p2',1,4),('integrate','i1',2,7),('formulate','p3',5,8),...]`; green with the round lock.
- Final: `python3 -m pytest -q --work-item w164`: 151 passed, 1 skipped. `python3 -m pytest -q --whole-suite tests/scenarios/test_supervision.py tests/scripts`: 315 passed, 1 skipped.
- Suite at the start: 852 passed, 8 failed (this work-item's 8 scenarios).

## Outside the file set
`tests/scripts/stub_claude.py` (the 15th file): new key `linger` (wait up to n seconds for another worker's start, a signal), needed so r95's "ending only after long enough for another round to start beside it" can be set up.

## Tests changed under an allowance
- `tests/scenarios/supervision_rounds_steps.py::second_not_refused` (the Then "the second `work run` was not refused"): listed in the plan. For the r84 scenario with a round it now asserts not refused over uncommitted work and a second integrate round started; the other two scenarios using it (no round) keep their old assertion.

## Open questions
- The plan's open cases stay unchosen: a proposal file named like an existing node; a capability in `changes` absent from `spec/capabilities/`; a request with no accepted lines for the r93 round; an empty drafts directory; a gate/apply brief naming the kept drafts. In r95's scenario i1's integrate gets DONE with no change list and ends in r96's error without stopping i2/i3.

## Other
The plan contained no code. `tools size --limit 300`: no file printed. Commits: 0ca611cf, a4e922a6, 12d95e83.
