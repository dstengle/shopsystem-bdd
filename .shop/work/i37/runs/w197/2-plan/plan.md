# Plan of w197 (requests r7, r23, r24)

From the research notes of `.shop/work/i37/runs/w197/1-research/notes.md`; the scenarios are those of `features/requests.feature`, bound in `tests/scenarios/test_requests.py`.

## 1. What goes green

- **requests#r7**: "turn on a request it does not set to accepted passes the request's turn from the <side> to the <other side>" (Examples upstream→asker, asker→upstream). Red today in the test, not the code: the Then "q1's status is not accepted" is bound to the `status_is` step of `tests/scenarios/requests_steps.py`, which compares the status to the literal words "not accepted" and so fails on `awaiting-asker` / `awaiting-upstream` (notes D2). The turn Then already holds (probes B, C).
- **requests#r23**: "the upstream ending its turn on a request that turn sets to accepted keeps the request's turn the upstream's". Red: `turn` in `scripts/workqueue_request.py` writes the asker's turn after every upstream end, also when it has just set `accepted` (probe A: `accepted`, turn asker).
- **requests#r24**: "resolve setting a request's status to delivered passes the request's turn to its asker". Red: `resolve` writes the resolution and `delivered` and never the turn (probe D: turn stays upstream).
- **Retired**: the deprecated "turn passes the request's turn from the <side> to the <other side> (deprecated)" (`@r7 @deprecated`, both Examples). It passes today and would keep passing; the work-item's Retires removes it from the feature, and its generated tests go with it.

## 2. Where the change lands

- `scripts/workqueue_request.py`: `turn` keeps the upstream's turn when the upstream's end sets the status `accepted`, and passes the turn otherwise as today; `resolve` writes the asker's turn together with `delivered`. Both docstrings name r23 / r24. (183 lines; well under the limit.)
- `tests/scenarios/requests_steps.py`: the status Then takes "not accepted" as "any status but `accepted`"; every other status word is compared as today.
- `features/requests.feature`: the deprecated `@r7 @deprecated` Scenario Outline (with its Examples) removed, per the Retires.

The researcher's set, unchanged. Not edited (read only, on the path): `scripts/work` (dispatch), `scripts/workqueue.py`, `scripts/workqueue_done.py`, `spec/index.md` (its glossary already says the new rule), `tests/scenarios/test_requests.py` (generated from the feature). `scripts/supervise_intake.py` stays out: its brief's "pass the turn once with `work turn`" stays true under r23, and no accepted scenario asks for a change there.

## 3. Decisions

1. **Which `turn` keeps the turn.** `turn` keeps the upstream's turn exactly when, in the upstream's turn, it sets the status `accepted` under r8 (every line accepted, refused or withdrawn, at least one accepted, request not `delivered`). Every other `turn` passes the turn to the other side as today: the upstream's end that sets `refused` (r9) or `awaiting-asker` (r17), the upstream's end on a `delivered` request (status unchanged, turn to the asker), and every asker's end (r18). Rests on requests#r23 and requests#r7 (narrowed to "a request it does not set to accepted").
2. **A second upstream `turn` on an already accepted request.** The notes flag it as two readings. r8's condition does not exclude a request already `accepted`, so that `turn` sets the status `accepted` again, r23 applies and r7 does not: the turn stays the upstream's, the status stays `accepted`. Taken from requests#r8 with requests#r23 and r7's narrowed wording; it is what the change of decision 1 does without any further branch, so no special case is written for it.
3. **Where the asker's turn on delivery is written.** In `resolve`, in the same edit that sets `delivered`, so the one commit of `work resolve` (r12) holds both; whichever side's turn it was before (r10: resolve runs in either turn; probe J's asker's-turn case ends with the asker's turn, unchanged). `resolve` is the only command that sets `delivered`, so r24 needs no other place. Rests on requests#r24, r11, r12.
4. **The "not accepted" Then.** "not accepted" in the status Then means the status is anything but `accepted`; the feature's wording is kept (it is accepted text). Rests on the r7 scenario as formulated and requests#r7's "a request it does not set to accepted".
5. **The Retires.** The deprecated scenario is removed from the feature with this work, not left for later. Rests on the work-item's Retires section.

## 4. Tests the decisions break

- `tests/scenarios/test_requests.py`: `test_turn_passes_the_requests_turn_from_the_side_to_the_other_side_deprecated[upstream-asker]` and `[asker-upstream]`: removed, by decision 5 (their scenario leaves the feature; the bindings are generated from it).
- `tests/scenarios/requests_steps.py` `status_is`: rewritten by decision 4 to assert "status is not `accepted`" for the words "not accepted", and equality otherwise; every other scenario using it (r8, r9, r11, r17, r18 and the r23, r24 Thens) keeps asserting the exact status.
- No other test breaks. Verified from the notes' search (no coverage map exists): every turn assertion is the `turn_is` step or the literal asker's turn in `tests/scenarios/supervision_intake_steps.py`, which follows a `question` line (status `awaiting-asker`, untouched by decision 1); r8, r9, r10, r11, r17, r18 assert status only; the fixtures of `requests_show_steps.py`, `supervision_request_steps.py`, `supervision_done_steps.py`, `design_model_check_requests.py` set turns by hand; `test_work_queue.py` runs neither `work turn` nor `work resolve`.

## 5. Open cases

- After r23 an accepted request stays in the upstream's turn, so the upstream keeps `work outcome` / `work ask` on it and the asker's `work reply` is refused (r16) until `work resolve`; no scenario says what an outcome changed on an accepted request then does. The implementer names it, does not choose.
- `supervise_intake.py`'s waiting set (open, awaiting-upstream) does not rerun an `accepted` request now left in the upstream's turn; nothing in this work asks it to. To name, not to change.
- Notes D1: `work request` accepts a request with no lines, and `turn` then sets it `refused`. Outside r7, r23, r24; to name as a finding, not to fix here.
