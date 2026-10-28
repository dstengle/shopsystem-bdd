# Report of w225 (implement)

## Budget
No file edited in this session; the two commits already on the branch touch 12 files (supervise_brief, supervise_glossary, supervise_rounds, workqueue, supervise, supervise_done; supervision_formulate/proposal/reintegrate/rounds/done steps).

## What I found
On start the branch already held two commits made after "w225 ready -> claimed", before this session: 9ebc483f (routing of a glossary-proposal through gate, apply, approved: r164 r165 r166 r167 r169 r170) and 58c712f0 (glossary-only done: r161). I wrote no code, so there was no red run of mine. Whether the scenarios were red before those commits was not seen by me (the research notes record 8 failed).

## Runs
- Suite record at start: 1062 passed, 0 failed at 58c712f0 (the brief's line; expected failures are w212's parked scenarios).
- Final: `python3 -m pytest -q --work-item w225`: 189 passed, 1 skipped, 56 subtests passed.
- `tools size --limit 300`: prints nothing; no file over.

## Answer given (r167)
Accepted as covered by r166's routing: the apply round for g1 now runs, so r167's Then checks no formulate round follows it.

## Tests changed under an allowance
Not verified by me. 9ebc483f changed `tests/scenarios/supervision_reintegrate_steps.py` (6 lines) and widened p1-only steps in supervision_rounds_steps.py and supervision_proposal_steps.py; the plan lists no test the decisions break. Check these diffs at review.

## Open questions
The plan's section 5 cases stay unchosen: a glossary-proposal gate giving no question; unheld answers on a glossary apply; answers dropping a drafted term; a glossary-only initiative with an undelivered raised request; `show` output of glossary-proposals.

## Plan code
The plan contained no code.

## Commits
9ebc483f, 58c712f0. Nothing uncommitted.
