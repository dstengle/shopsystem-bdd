# Plan of w175: requests#r22, the empty delegation refused

This plan replaces the 2-plan's, which stopped on one question (whether a whitespace-only delegation is empty). The
work-item's Answers settle it: reading B (see D-c).

## 1. What goes green

- `requests#r22`: scenario "request with an empty delegation is refused, and nothing changes"
  (features/requests.feature:33).
  Red today (notes §1): the Then "the command is refused because the delegation is empty" has no step definition
  (StepDefinitionNotFoundError). Behind it, `request()` in `scripts/workqueue_request.py` has no check for an empty
  delegation: it writes `delegation: ""`, commits `work request: q1` and exits successfully (probe P1, defect D1).
  The Thens after it, "it exits with an error" and "the upstream keeps no request", already exist and pass once the
  refusal comes before the write and the commit.
- Retires: none. The work-item has no Retires section.

## 2. Where the change lands

- `scripts/workqueue_request.py`: `request()` refuses, with `workqueue.Refused`, a delegation that is given and is
  empty after stripping whitespace (D-c), before any write, commit or q-number (before `workqueue.committed`). The
  message says the delegation is empty. A delegation that is not empty is still written as given (r19).
- `tests/scenarios/requests_write_steps.py`: a new Then "the command is refused because the delegation is empty",
  modelled on the existing "names neither an origin nor a job-thread" Then (notes §1, line 94): it checks that stderr
  says the delegation is empty.

Read, not edited (they must keep passing): `scripts/work` (passes `--delegation` through), `scripts/workqueue.py`
(`Refused`, `committed`; 290 lines, no room to edit), `scripts/supervise_answers.py`, `tests/scenarios/test_requests.py`.
No decision adds or removes a file. Both edited files have room under the 300-line limit (144 and 122 lines).

## 3. Decisions

- D-a. The refusal is in the library, in `request()`, not in argument parsing in `scripts/work`. It sits with the r2
  and r3 refusals, so "change nothing" holds the same way: no file written, no commit, no q-number taken (notes §5).
  Rests on requests#r22 and design-decision/requests-written-through-work.
- D-b. A refused run exits with an error, the same exit as the other refusals of `work request`. Rests on
  design-decision/exits-are-successful-or-errors and requests#r22.
- D-c. "Empty" means empty after stripping whitespace: `--delegation ""` and `--delegation "   "` are both refused,
  exactly alike. Taken by the work-item's Answer of 2026-10-25 (reading B), resting on requests#r22.
- D-d. A delegation that has text is written as given, its whitespace not stripped. Rests on requests#r19 ("write the
  delegation") and its scenario's Pins line ("as they were given").
- D-e. Only a delegation that is given is checked; no `--delegation` at all stays a request with no delegation (probe
  P3). Rests on requests#r19 ("Where `--delegation <text>` is given") and r22 ("the delegation given").

## 4. Tests the decisions break

None. Verified from the notes (§4: search of `tests/` for `--delegation`, `delegation`, `delegation=""`):
- The r19 scenario (features/requests.feature:23) and its step "its delegation is ..." use non-empty text with no
  surrounding whitespace; it stays green under D-c and D-d.
- `tests/scenarios/supervision_delegation_steps.py`: every delegation is non-empty text; none can fail.
- No test asserts that an empty or whitespace-only delegation is written. The only test with an empty one is the red
  r22 scenario.

## 5. Open cases

For the implementer to name, not to choose:
- The order of refusals when a run has more than one fault: an empty delegation with no `--source`/`--thread` (P5),
  or with a line not in strict form (P6). Today the origin and line checks run first; the scenarios are silent on
  which refusal is reported.
- Requests kept before r22 with `delegation: ""` or a whitespace-only delegation stored. `supervise_answers.py`
  reads `""` as no delegation but `"   "` as a delegation (notes §2, §3). This work does not change that.
- The exact text of the refusal, beyond its saying that the delegation is empty.
- Whitespace other than spaces (tabs, newlines) only: covered by D-c as stripping, not pinned by a scenario.
