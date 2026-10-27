# w211 implement report (narrowed: no transport)

## Budget

scripts/workqueue_request.py, scripts/work, scripts/workqueue_list.py, features/requests.feature (`features retire` only),
tests/scenarios/requests_world_steps.py (new), requests_flow_steps.py (new), requests_write_steps.py, test_requests.py.
(8 of 15.) Outside the file set: the two new step modules (300 limit / new concern; tests only).

## What changed

- `workqueue_request.gate` (called by `work request` only, so supervision's raise is unchanged): refuses `--from` other than the repository's own id (r32); in a repository whose spec/index.md has `## Upstreams` (an asker), refuses `--source` (r30) and a request with neither `--raised-for` nor `--thread` (r31). An upstream with no upstreams keeps r45's existing refusal.
- `outcome` in a repository with an upstream, on a request whose asker is this repository, is refused naming the upstream (r34), before the turn check. r33's other cells already held.
- `work show <request>` prints `<q> <status> <turn>` (r25).
- Tests: one shared repository takes the identity of the role that runs a command (`requests_world_steps.be`); r25's table steps in `requests_flow_steps`. The two deprecated scenarios (@r1, @r3) retired with `features retire`, and the steps only they used removed.

## Runs

Red: at the start the 15 scenarios failed as in the brief's Suite record (all `StepDefinitionNotFoundError` at their first Given). I wrote the production code and the steps together before re-running, so I did not observe each red one at a time (departure from the one-scenario cycle).
Green: `python3 -m pytest -q -n 0 --work-item w211` -> all pass (150+15; 1 skipped). Touched modules (test_requests, test_work_queue, test_supervision, tests/scripts): 164 passed, 1 skipped.
Suite at the start (brief): 977 passed, 15 failed (the 15 above) at 31862091.

## Tests changed under an allowance

- tests/scenarios/requests_write_steps.py `upstream_keeps_none` (shared Given of r19, r22, r2 and work-queue r7): setup only; the repository's id is ctx-a (gate r32 needs `--from` to match it).
- Removed with `features retire`: `keeps_one_open`, `keeps_one`, `lines_and_asker`, `names_origin`, `prints_id` of requests_write_steps, which the retired scenarios used; r44/r29 use new generalised versions in requests_world_steps (new request = the one the command kept).

## Open questions

- No transport: where an asker's request "the upstream keeps" (r44 rows 2-3, r29, r28-family) is bound to the one shared repository, so `work request` in an asker's repository keeps the request there. Real delivery to the upstream is w212.
- r25's "takes in what has been sent to it" runs no command (no take-in exists); its Then "each step was done by one command" counts steps with a command only.
- Side check only refuses `outcome` by the asker; `ask` and `resolve` by an asker, and `reply` by an upstream, are not refused (no scenario asks).
- Retired r1 had also accepted a request with only `--raised-for` in an internal repository; unchanged.
- A title/answer text with a newline (review finding 3), id used as path, etc.: belong to take-in, not built.

## Plan contained code

No (prose); nothing pasted.

## Completeness

`tools size --limit 300` printed nothing.

## Result

Someone can now raise a request with the repository's own asker only, with origins and thread rules per side, see the asker refused an outcome, and `work show q1`. Surprising: the asker/upstream distinction in a single repository comes only from `## Upstreams` of spec/index.md.
Commit: 91b7750d.

Files changed: scripts/work, scripts/workqueue_list.py, scripts/workqueue_request.py, features/requests.feature (retire), tests/scenarios/requests_world_steps.py, requests_flow_steps.py, requests_write_steps.py, test_requests.py.
