# Plan of w239 (requests r64)

## 1. What goes green

- **requests#r64**: "list prints, with its date, each observation that the source of no initiative and of no request names"
  (features/requests.feature, @r64). It is red today for two reasons (notes §1). First, the When step "the session runs
  `work list`" has no definition in the steps the requests scenarios load (tests/scenarios/requests_show_steps.py has
  only `runs_show` and `runs_status`), so the run stops at StepDefinitionNotFound. Second, behind that, `workqueue_list.listing`
  prints only initiatives, requests and work-items. The only scan of uncited observations is `workqueue_status.uncited`,
  and only `work status` calls it.
- **Retired** (the work-item's Retires): the deprecated scenario "status with no initiative prints, with its date, each
  observation no initiative's or request's source names (deprecated)" (@r14 @deprecated, features/requests.feature
  lines 468-478). It is removed from the feature file.

## 2. Where the change lands

- `scripts/workqueue_list.py`: `listing` lists each uncited observation with its date in the text output, and under an
  `observations` key in the `--json` output (decision 2). The scan `uncited` moves here from workqueue_status.py (decision 1).
- `scripts/workqueue_status.py`: `status` no longer prints observations, either as text lines or as the `observations`
  key of its JSON. `uncited` leaves the module. The `report` parameter, which only gated the observations, can go,
  and `open_text` (in this same module) stops passing it (decision 1).
- `tests/scenarios/requests_show_steps.py`: add the When step "the session runs `work list`", next to the existing
  steps. Remove `runs_status` ("the session runs `work status`"), because the retired scenario was its only user in
  requests.feature. work-queue.feature's `work status` scenario uses the generic `run_work` step of
  test_work_queue.py, not this one.
- `features/requests.feature`: remove the retired r14 scenario (lines 468-478).

The researcher's set also named `scripts/migrate_session.py` as a conditional edit. It drops out:
`migrate_session.py` only calls `open_text`, which lives in workqueue_status.py, and `open_text` already gave no
observations (it passed report=False). The hook's text does not change. `tests/scenarios/test_requests.py` and
`tests/scripts/test_workqueue_list.py` are not edited (notes §4).

Size: workqueue_list.py is 106 lines and grows by about the length of `uncited`. workqueue_status.py is 170 lines and
shrinks. requests_show_steps.py is 72 lines. All three stay well under the 300-line limit of CLAUDE.md.
scripts/workqueue.py (294 lines) is not touched.

## 3. Decisions

1. **The observation listing moves from `work status` to `work list`; `work status` stops printing observations**, as
   text lines and as its JSON `observations` key. This settles the researcher's question 1 as reading A. It rests on:
   - the answer to the question on r14 recorded in capability-proposal i55-requests (2026-10-29, reading (a): retire r14
     and add r64 as worded, against (c) "keep r14"). The question's own text says "r14 is retired with work status";
   - the retired scenario's line "Deprecated for: list prints … each observation …", which names r64 as r14's
     replacement: the behaviour moves, it is not duplicated;
   - requests r14 retired in the capability's `retired:` list. No requirement asks `work status` for observations any more;
   - design-decision 0072 (work-list-and-work-show-replace-work-status, proposed), which retires `work status` in favour
     of `work list`. This work does not retire `work status` itself; other work-items under work-queue do that.
2. **`work list --json` carries the observations**, under an `observations` key: a list of objects, each with the
   observation's id and its date. This is the form `work status --json` used, so a JSON reader loses nothing in the
   move. It rests on requests#r64: "When `work list` is run" names no output form, so the JSON form of `work list` is
   also bound to give each uncited observation with its date. Adding a key leaves
   test_workqueue_list.py's JSON test sound (notes §3).
3. **Text form**: one line per observation, giving the observation's id and its date, after the work-items. This is
   the line form `work status` used. It rests on r64 (id and date printed) and on the scenario's Then steps, which look
   for one line that holds both o3 and its date, and for no o1 or o2 anywhere in the output.

## 4. Tests the decisions break

- `features/requests.feature` / tests/scenarios/test_requests.py: the r14 scenario "status with no initiative prints …
  (deprecated)". Decision 1 breaks it. It is **removed**: the work-item's Retires names it, and its binding goes with
  the feature lines.
- No other test, verified:
  - No test under tests/ asserts an `observations` key of `work status --json` or observation lines from `work status`
    (search for "observation", "uncited" and "report=" under tests/: the only hits are model tests and the requests
    steps).
  - work-queue.feature's deprecated r17 scenario runs `work status` but asserts only initiatives.
  - test_workqueue_list.py's JSON test asserts only `requests`.
  - work_queue_list_steps.py looks up named pairs only.
  - The SessionStart hook path (`open_text`) printed no observations before this change.

## 5. Open cases

For the implementer to name, not to choose:
- An observation heading with no `date:` line: `uncited` gives no date for it today. The scenarios give every
  observation a date.
- No `.shop/records/observations.md`: `work list` lists no observations. The scenario does not cover this, and the
  text output should not change for repositories without observations.
- Where the observation lines sit relative to the initiative, request and work-item lines (decision 3 puts them last).
  The scenario does not check their order.
- An initiative that is done or abandoned: `uncited` counts its `source` as naming an observation, as it does today.
  r64 says "no initiative", and the scenario's i1 is open.
