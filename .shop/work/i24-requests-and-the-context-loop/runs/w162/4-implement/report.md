## Budget
- tests/scenarios/supervision_rounds_steps.py
- scripts/supervise_rounds.py

## Changes
- New Given step "i1 is proposed and fulfils the request q9, which the queue does not hold" (supervision_rounds_steps.py).
- `Rounds.due` (supervise_rounds.py): the request's accepted lines are read before the integrate round is due; a request the queue lacks (Refused) gives no round, so nothing moves.

## Red / green
My branch lacked the scenario (it is in e3fbf0b, on the initiative branch; I cannot rebase). I copied it into features/supervision.feature uncommitted, ran, and removed it again before committing; `work run` will rebase it in.
- Red: `python3 -m pytest -q --work-item w162` -> 1 failed, 144 passed. Failure: i1 was `status: started` (the "i1 is proposed" Then), stderr "there is no request q9 under .shop/work/requests". Expected: the code moved the initiative first.
- Green: same command -> 145 passed, 1 skipped; tests/scenarios/test_supervision.py 3 passed (with the scenario in place).
- Suite record at start: Suite: 848 passed, 0 failed at 4cbd265.

## Deviation from the plan
Plan Decision 1 says refuse (exit 1, say why). The scenario's last Then, "the second `work run` was not refused" (exit 0, no "work:" on stderr), cannot hold if the same unchanged state refuses again. So the code gives no round and no error, like "fulfils no request". Nothing in the scenario asserts a message.

## Tests changed under an allowance
none

## Open questions
- Held request with no accepted line (notes D2) keeps today's behaviour: round with no lines.
- A DONE integrate round leaves its stage directory uncommitted (notes D3).
- `work run` with no initiative, one fulfilling a missing request; fulfils naming several requests.
- Whether a missing request should be reported to the person (the scenario forces exit 0 / no "work:" stderr on rerun).

The plan contained no code. supervise_brief.py unchanged.

## Size
`tools size --limit 300` printed nothing.

## Files changed
scripts/supervise_rounds.py, tests/scenarios/supervision_rounds_steps.py. Commit c47a088.
