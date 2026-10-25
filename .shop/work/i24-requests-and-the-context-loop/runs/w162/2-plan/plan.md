# Plan of w162: fix branch review 2's R2-F1 (supervision#r79)

The work-item accepts supervision#r79 and names branch review 2's findings. One finding is to fix now: R2-F1. A `proposed` initiative whose `fulfils` names a request the queue does not hold is moved to `started`. A round branch is made, the log is left uncommitted, and every later `work run` is refused.

## 1. What goes green

supervision#r79. Its accepted scenarios in `features/supervision.feature`:
- "a proposed initiative is given to an integrate round with the accepted lines of the request it fulfils". It is not red today: the notes ran it and it passed.
- "a proposed initiative that fulfils no request is given no integrate round, stays proposed and leaves nothing behind". It is not red today either: it was run and passed.

No accepted scenario covers R2-F1, so the work adds one, tagged `@r79` (see Decision 2):
- "a proposed initiative whose fulfils names a request the queue does not hold is given no integrate round, and nothing changes".
- It is red today. The notes' probe P-a and the review's reproduction show this: exit 1, but `initiative.md` is `started`, `log.jsonl` is left modified and uncommitted, and `round/i1-1-integrate` is made.

What the scenario says, step by step, following R2-F1's "Keep as a test":
- It begins with i1 `proposed`, its `fulfils` naming q9. The queue holds no q9.
- Every round ends, and the person runs `work run i1`.
- Its outcomes reuse steps that already exist:
  - the r10 outline's steps: work says why (that there is no request q9 under `.shop/work/requests`), it exits with an error, and nothing in the repository has changed, its commits included;
  - the r79 steps: no round of the kind integrate was started for i1, i1 is proposed, and no branch is made for a round.
- Only its opening step, the initiative fulfilling a request the queue does not hold, is new.

There is no `## Retires` section and no scenario is deprecated under r79, so nothing is retired.

## 2. Where the change lands

- `features/supervision.feature`: the new `@r79` scenario above, placed after the two r79 scenarios.
- `tests/scenarios/supervision_rounds_steps.py` (236 lines, room 64): the new opening step. It writes and commits an `initiative.md` that is `proposed`, with q9 as its `fulfils` and no q9 request file. It sits beside the step for "fulfils no request" (`proposed_fulfilling_none`).
- `scripts/supervise_rounds.py` (97 lines): before the initiative is moved and before any round branch is made (`due` or `round`, ahead of `start_initiative`), the request the initiative fulfils is read for its accepted lines. A request the queue does not hold then refuses with nothing changed.
- `scripts/supervise_brief.py` (129 lines): `integrate_lines` is touched only if the lines read up front are handed to the brief rather than read a second time. It is the implementer's choice whether it changes at all.

Removed from the researcher's set, and why:
- `scripts/workqueue_request.py`: `accepted_lines` already refuses a request that is missing, with the message the scenario expects. Nothing in it changes.
- `spec/capabilities/supervision.md`: the r79 text (review O3) is spec work. It goes through an initiative round, not through this work-item.
- `scripts/supervise.py`, `supervise_worker.py`, `workqueue.py`, `workqueue_done.py`, `supervise_faults.py`, `tests/scenarios/supervision_world.py` and `tests/scenarios/test_supervision.py`: these are on the path but nothing in them changes. `test_supervision.py` binds the feature file with `scenarios()`, so the new scenario binds on its own.

## 3. Decisions

1. **A `fulfils` the queue does not hold is a refusal under r10, made before anything moves.**
   - `work run` cannot give the integrate round "the accepted lines of the request it fulfils" (supervision#r79).
   - So it cannot start that delivery. supervision#r10 then says: exit with an error, say why, change nothing.
   - In practice this means: no move to `started`, no `log.jsonl` line, no round branch and no commit.
   - supervision#r84 moves the initiative only when the round starts, and here it does not start.
   - supervision#r46 is why nothing may be left uncommitted: otherwise every later run is refused.
   - Of the review's two fixes, this takes "check before anything moves" over "catch `Refused`, put the status back and run `keep_round`". With this one there is nothing to undo.
2. **The new scenario is tagged `@r79`, not `@r10`.** It pins how r79's integrate round behaves when the request is missing. Under supervision#r22 the option `--work-item w162` selects only scenarios of the requirements the work-item accepts, which is r79 alone. Tagged `@r10`, the scenario would not be in w162's check.
3. **The message is the one the queue already gives**: there is no request q9 under `.shop/work/requests`, from `workqueue_request.accepted_lines`. That is r10's "say why". The review's wording ("saying the queue does not hold q9") is a paraphrase, not a requirement.
4. **A held request with no accepted line (notes D2) keeps today's behaviour**: a round with an empty list of lines. R2-F1 does not name this case and this work does not change it. See Open cases.

## 4. Tests the decisions break

None. I checked that:
- the notes' part 4 search found no test asserting that a missing request is moved or integrated;
- both r79 scenarios and the r84 scenario at `supervision.feature:1043` have a request the queue holds, so the earlier read refuses none of them;
- the steps the new scenario reuses (`i1 is proposed`, `no branch is made for a round`, `no round of the kind integrate was started for i1`, and the r10 outline's Then steps) are only reused, not changed.

## 5. Open cases

- **A held request with no accepted line, or with no `## Outcomes`** (notes D2, probes P-b and P-c). The integrate round starts with no lines. Reading (a), r79 read literally, keeps that round. Reading (b), from scenario 2's Pins, gives no round. No scenario settles it and this work does not choose. The implementer names it in the report.
- **A DONE integrate round leaves its stage directory uncommitted** (notes D3, probe P-d), so the next `work run` is refused under r46. No finding of review 2 names it and no accepted scenario covers it. It is not in this work. The implementer names it in the report so a later review or work-item can take it.
- **`work run` with no initiative (r66), one initiative of which fulfils a missing request.** No scenario gives whether the other initiatives are still taken.
- **A `fulfils` that names more than one request, or a list form** (review O1, for `measure_read`). No scenario gives it here.
- **Measure refusing the stand-in's integrate `session.json`** (notes O1). This is outside this work.
