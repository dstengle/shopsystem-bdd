# w210 report

## Budget
scripts/supervise_raise.py (new), scripts/supervise_rounds.py, scripts/supervise_draft.py, scripts/workqueue_request.py,
scripts/work, CLAUDE.md, tests/scenarios/supervision_raise_steps.py (new), tests/scenarios/test_supervision.py,
tests/scenarios/supervision_rounds_steps.py. (9 files)

## Outside the file set
`tests/scenarios/supervision_rounds_steps.py` (not in the work-item's set): the shared Given "i1 is proposed and fulfils the
request q1, whose ... " matched the r135 line 1447 but ignored "which gives the delegation". It now writes `delegation:`
when the text names one. `spec_integration_steps.py` (in the set) was not touched (see below).

## What changed
- `work request --raised-for <q>` (`workqueue_request.request(..., raised_for=)`): written as `raised_for:`; counts as
  naming where the request comes from (decision 1).
- `scripts/supervise_raise.py` (new, module-map row added): raises each `requests` entry of an integrate result with
  `workqueue_request.request` in the upstream's repository (the directory above its published spec), `--from` this
  context, raised for the fulfilled request, with its delegation; writes `raised.jsonl` lines (upstream, request,
  initiative, status open, round = the drafts path the proposals name); `waits(proposal)` reads whether a proposal's round
  has a request not read as `delivered` in its upstream (unreadable = held).
- `supervise_rounds.py`: raise after the r96/r107 checks, before proposals are written; record committed with the round's
  proposals. On a failed raise: merge undone (`reset --hard` to the pre-merge head), stage dir kept via `keep_round`,
  error naming round, upstream and work's reason; no proposal written, status kept.
- `supervise_draft.py`: `draft_proposals` skips a held proposal.

## Red and green
Red (observed before my changes, per the research notes and the suite record): both scenarios failed with
StepDefinitionNotFoundError (r135 at feature line 1448, r136 at 1165), and `work request --raised-for` was refused
exit 2. I wrote steps and code in one pass after reading, so I did not re-run a separate red of my own.
Green: `python3 -m pytest -q --work-item w210 -n 0` -> 152 passed, 1 skipped, 850 deselected.
Also `--whole-suite` on test_spec_integration, test_supervision, test_requests, test_work_queue: 370 passed, 25 xfailed;
tests/scripts: 149 passed, 1 skipped.
Suite record at start: 975 passed, 2 failed (the two w210 scenarios), plus the expected-failing requests ones.

## Tests changed under an allowance
- tests/scenarios/supervision_rounds_steps.py `proposed_fulfilling` (setup): writes a `delegation:` field into q1 when the
  step text names one; no assertion touched. Other scenarios' text names none.

## Open questions
- The plan's open cases stand: one round with several proposals (all held); a second raise failing after a first
  succeeded (first request stays in its upstream, raised again next time); the same upstream named twice; the
  upstream's commit is never pushed.
- Decision 9 says to commit nothing on a failed raise; I commit the stage directory and log lines with `keep_round`
  (as r96 does) because leaving them uncommitted makes the next run refuse (r46). The merge itself is undone.
- Plan part 4 predicted the spec-integration @r44 scenario would break (billing is no repository). It passes unchanged:
  its Thens read the brief and the kept result, which survive the failed raise. Left untouched.

The plan contained no code; nothing was pasted.

## Completeness check
`tools size --limit 300` printed nothing.

## Files changed
CLAUDE.md, scripts/supervise_draft.py, scripts/supervise_rounds.py, scripts/work, scripts/workqueue_request.py,
scripts/supervise_raise.py, tests/scenarios/supervision_rounds_steps.py, tests/scenarios/test_supervision.py,
tests/scenarios/supervision_raise_steps.py. Commit b762072b.
