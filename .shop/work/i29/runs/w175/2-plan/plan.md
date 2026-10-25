# Plan of w175: requests#r22, the empty delegation refused

## 1. What goes green

- `requests#r22`: scenario "request with an empty delegation is refused, and nothing changes" (features/requests.feature:33).
  Red today (notes §1): the Then "the command is refused because the delegation is empty" has no step definition
  (StepDefinitionNotFoundError). Behind it, `request()` in `scripts/workqueue_request.py` has no check for an empty
  delegation. It writes `delegation: ""` and commits `work request: q1`, exiting successfully (probe P1, defect D1).
  The Thens after it, "it exits with an error" and "the upstream keeps no request", already exist. They pass once
  the refusal comes before the commit.
- Retires: none. The work-item has no Retires section and no deprecated scenario is named.

## 2. Where the change lands

- `scripts/workqueue_request.py`: `request()` refuses an empty delegation with `workqueue.Refused`, before any write
  or commit (before `workqueue.committed`). The message says the delegation is empty. Today a given delegation,
  empty or not, is written.
- `tests/scenarios/requests_write_steps.py`: a new Then "the command is refused because the delegation is empty",
  modelled on the existing "names neither an origin nor a job-thread" Then (notes §1). It checks that stderr names
  the delegation as empty.

Read, not edited (they must keep passing): `scripts/work` (passes `--delegation` through), `scripts/workqueue.py`
(`Refused`, `committed`; 290 lines, so no room to edit it), `scripts/supervise_answers.py` (already reads a stored
empty delegation as none), `tests/scenarios/test_requests.py`. No decision below adds or removes a file. Both
edited files have plenty of room under the 300-line limit (144 and 122 lines).

## 3. Decisions

- D-a. The refusal is in the library (`request()`), not in argument parsing in `scripts/work`. It sits with the r2
  and r3 refusals, so the "change nothing" part of r22 holds the same way theirs does: no file is written, no commit
  is made and no q-number is taken (notes §5). Rests on requests#r22 ("change nothing") and
  design-decision/requests-written-through-work (0067: `work` alone writes a request).
- D-b. A refused run exits with an error, the same error exit as the other refusals of `work request`. Rests on
  design-decision/exits-are-successful-or-errors (0055) and requests#r22.
- D-c. What counts as "empty" is **not taken here**. See the question in the result. The empty string is refused
  under every reading. Whether a whitespace-only delegation (`--delegation "   "`, probe P2) is refused too, or is
  written under r19, is something the narrator can see. No requirement, decision or ruling settles it.

## 4. Tests the decisions break

None. Verified from the notes (§4), searching `tests/` for `--delegation`, `delegation` and `delegation=""`:
- The r19 scenario (features/requests.feature:23) and its step "its delegation is ..." use a delegation that is not
  empty. They stay green under either reading of D-c.
- `tests/scenarios/supervision_delegation_steps.py`: every delegation there is non-empty text, so none can fail.
- No test asserts that an empty delegation is written. The only test with one is the red r22 scenario.
- If D-c is answered "whitespace refused", no test breaks either: no test passes a whitespace-only delegation.

## 5. Open cases

For the implementer to name, not to choose:
- The order of refusals when a run has more than one fault: an empty delegation together with no `--source` or
  `--thread` (P5), or together with a line not in strict form (P6). Today the origin and line checks run first.
  The scenarios are silent on which refusal is reported.
- A request kept before r22 with `delegation: ""` stored. `supervise_answers.py` reads it as having no delegation.
  This work does not change that.
- The exact text of the refusal, beyond its saying that the delegation is empty.
