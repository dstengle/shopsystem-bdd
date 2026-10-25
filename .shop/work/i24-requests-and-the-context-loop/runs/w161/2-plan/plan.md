# Plan of w161: measure refuses an initiative whose request it cannot read, saying why

Under batch-measurement; accepts r65, r66, r67. No Retires section, no Rulings. Planned from
`runs/w161/1-research/notes.md`.

## 1. What goes green

- **batch-measurement#r65**: "an initiative fulfilling a request the queue does not hold is refused"
  (features/batch-measurement.feature:23). Red today: its first Given, `i7-cart fulfils the request q3`, is undefined
  (StepDefinitionNotFoundError); `the queue does not hold the request q3`, the Then `measure initiative refuses because
  the queue does not hold that request` and `no measurement is written` are undefined too. The code already refuses
  (exit 1, nothing written) but its text is "there is no request q3 under .shop/work/requests", which does not say the
  reason r65 gives.
- **batch-measurement#r66**: "an initiative fulfilling a request with no asker is refused" (:33). Red: undefined
  `i7-cart fulfils the request q3, which the queue holds`, `the request q3 has no asker`, the Then `... because the
  request has no asker`, and `no measurement is written`. The code already refuses with "<path> has no asker".
- **batch-measurement#r67**: "an initiative fulfilling more than one request is refused" (:43). Red: undefined
  `i7-cart fulfils the requests q3 and q4, which the queue holds, each with an asker`, the Then `... because the
  initiative fulfils more than one request`, and `no measurement is written`. The code refuses a single `fulfils:`
  holding several ids, but with "fulfils must hold one request id, not ..."; and two `fulfils:` lines pass silently,
  measured as q3 only (the notes' defect D1).

No deprecated scenarios are retired.

## 2. Where the change lands

- `scripts/measure_read.py`: `request_of` gives the three refusals in the requirements' words (decision 1), and sees
  every `fulfils:` line of the initiative's frontmatter, refusing when they name more than one request (decision 2).
- `tests/scenarios/batch_measurement_world.py`: the World's request becomes a list of requests the initiative
  fulfils, each with whether the queue holds it and its asker, which may be empty; `flush` writes one request file for
  each held request and the initiative's `fulfils` for the requests named (decision 3).
- `tests/scenarios/batch_measurement_request_steps.py`: the new Givens (`fulfils the request {r}`, `fulfils the
  request {r}, which the queue holds`, `fulfils the requests {a} and {b}, which the queue holds, each with an asker`,
  `the queue does not hold the request {r}`, `the request {r} has no asker`) and the three refusal Thens; the two
  existing Givens move to the list form.
- `tests/scenarios/batch_measurement_then_steps.py`: the Then `no measurement is written` (decision 4).

Removed from the researcher's set: `scripts/workqueue_request.py` (decision 2 keeps `field` as it is, so its other
callers in `supervise_answers.py` and `supervise_brief.py` are untouched). Kept from that set but not edited, read
only: `scripts/measure`, `scripts/measure_build.py`, `scripts/measure_write.py`, `scripts/workqueue.py` (14 lines of
room: must not grow), `scripts/supervise_answers.py`, `scripts/supervise_brief.py`,
`tests/scenarios/test_batch_measurement.py`.

## 3. Decisions

1. **The refusal texts say the requirements' reasons.** The r65 refusal says the queue does not hold the request,
   naming it; the r66 refusal keeps saying the request has no asker, naming its file; the r67 refusal says the
   initiative fulfils more than one request, naming the requests (or the value) it read. Each still exits with an
   error and writes nothing (r50, r46's pattern). Rests on r65, r66, r67 ("refuse ... because ...") and
   design-decision/measure-refuses-unknown-shapes (refuse, saying what stopped it). The Thens assert a non-zero exit
   and the reason's words in stderr, in the manner of the existing `refuses because the initiative has no log.jsonl`.
2. **More than one request counts both ways: one `fulfils:` holding several ids, and several `fulfils:` lines.**
   `request_of` reads all the `fulfils` values of the initiative's frontmatter itself, within `measure_read.py`, and
   refuses (r67) when together they name more than one request; `workqueue_request.field` keeps returning the first
   match for its other callers. Rests on r67: an initiative with two `fulfils:` lines naming q3 and q4 fulfils more
   than one request; measuring q3 alone is the guess the scenario's description forbids. The two lines naming the same
   request once more is one request (open case 2 below).
3. **The order of the checks stays as today: more than one request first, then the queue, then the asker.** So an
   initiative naming q3 and q4 where q4 is not held is refused for r67's reason. This is today's observed order (notes
   §2), no change of what the narrator sees for the existing single-value case; rests on r67 (the count is known before
   any request is read). Each scenario has one reason only, so none depends on the order.
4. **`no measurement is written` asserts that no measurement record exists under `.shop/records/measurements/`**
   after the run; on these refusals that is the same observation as `nothing is written`, which stays for the
   scenarios that use it. Rests on r65–r67 ("writing no measurement").
5. **The World keeps the existing scenarios' meaning.** `fulfils the request {r}, whose asker is {a}` becomes a
   one-entry list, held, with that asker; `fulfils no request` an empty list, writing no `fulfils` line. Rests on r63,
   r64, whose scenarios (feature :200 outline, :214) must keep passing.

## 4. Tests the decisions break

None. Verified from the notes §4: no test asserts the old texts ("there is no request", "must hold one request id")
or the first-line-only reading of `fulfils`; `tests/scripts/test_measure_runs.py` concerns empty `session.json` only.
The r63/r64 scenarios' steps (`batch_measurement_request_steps.py` `fulfils`, `fulfils_none`) change in form under
decision 5 but keep asserting the same thing; `supervision_analysis_steps.py` meets the refusals through the existing
"was refused" path, unchanged.

## 5. Open cases

1. A request file in the queue with `status: withdrawn` is measured today as held (notes §6); r65 does not say whether a
   withdrawn request is "held". Not changed by this plan; the implementer names it, does not choose it.
2. Two `fulfils:` lines naming the same request; a blank `fulfils:` line beside one naming a request.
3. A bare id (`fulfils: q3`) is read today as `request/q3`; scenarios are silent.
4. A `fulfils` naming several requests where one is not held or has no asker: decision 3 gives r67's reason; no
   scenario shows it.
