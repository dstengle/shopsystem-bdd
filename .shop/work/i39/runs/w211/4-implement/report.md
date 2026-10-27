# w211 implement report

## Budget

Files touched (13 of 15): scripts/workqueue_request.py, scripts/work, scripts/workqueue_list.py, scripts/workqueue_sent.py (new), scripts/workqueue_takein.py (new), CLAUDE.md, features/requests.feature (`features retire` only), tests/scenarios/requests_steps.py, requests_write_steps.py, requests_send_steps.py (new), requests_world_steps.py (new), requests_flow_steps.py (new), requests_run_steps.py (new), test_requests.py.
(That is 14 files with the four new step modules; under 15.)

## Outside the file set

Not in the plan's list but needed: `tests/scenarios/requests_world_steps.py`, `requests_flow_steps.py`, `requests_run_steps.py` (new step modules, the 300 limit; the plan allowed more). `scripts/supervise.py` and `scripts/supervise_intake.py` were not touched: the take-in is called from `cmd_run` in `scripts/work`, which covers `work run` with and without an initiative. `scripts/workqueue_list.py` got `show` of a request.

## What changed

- `scripts/workqueue_sent.py`: the carrier (git). Settings in `.shop/requests.toml` (`[asker] remote,id`; `[upstream] remote` and `[upstream.allow]` asker id -> askers). An asker pushes each request/answer/turn as a JSON blob to `refs/sent/<asker id>/<n>` on the upstream's remote and reads the upstream's requests from `refs/published/<q>` by fetching; no checkout of the upstream. The upstream publishes a request of another asker after each change.
- `scripts/workqueue_takein.py`: `raise_request` (gate in the order of D4: delegation, lines file, strict form, asker = this repository's id (r32), `--source` refused in an asker's repository (r30), neither flag (r31 wording; r45 wording for an internal request)), then keep it here or send it; `take_in` (fetches fresh each time, in order sent, allow list check r41/r42, items written through `store`/`reply`/`turn`, taken items removed from the remote, untaken ones told with r41's wording).
- `scripts/workqueue_request.py`: `request` split into `lines_of`, `strict`, `render`, `store`; side checks: in an asker's repository `outcome`/`ask`/`resolve` are refused naming the upstream, `reply`/`turn` read the published request and send (r28, r33, r34); in an upstream, `reply` on a request from another asker is refused except from take-in; publishing after each change.
- `scripts/work`: `take-in` subcommand, `request` through the gate, `run` takes in first (r40). `workqueue_list.show` prints a request (r25).
- Tests: repositories built by `requests_world_steps` (bare remote, upstream/asker repos); the upstream "keeps" a request as its repository holds it plus what is sent and not taken in (the Answer's reading, D10). Steps bound for all 26 scenarios. The shared "an upstream that keeps no request" now gives its repository the id ctx-a (D6), no upstream.
- `features retire` run for the two deprecated scenarios (@r1, @r3), with the steps only they used removed.
- CLAUDE.md: rows for `workqueue_sent.py` and `workqueue_takein.py`.

## Red and green runs

Red: before my edits all 26 accepted scenarios failed at their first Given with `StepDefinitionNotFoundError` (research notes §1; the Suite record's 26 failures). I did not re-run them one at a time before writing code (I wrote the library and steps together, then ran): honest departure from the one-scenario cycle. One red re-observed: with the `work run` take-in commented out, r40 failed (`StopIteration` at `first_intake`: no intake round was started as no request was taken in); restored.

Green: `python3 -m pytest -q -n 0 --work-item w211 tests/scenarios/test_requests.py` -> 26 passed (after the last change: `--work-item w211` over the whole repository: 176 passed, 1 skipped).
Touched/related modules (`--whole-suite`): test_requests, test_work_queue, test_supervision, tests/scripts: 540 passed, 1 skipped.

Suite at the start (brief): 977 passed, 26 failed at a82b4227 (the 26 being these scenarios).

## Tests changed under an allowance

- tests/scenarios/requests_write_steps.py `upstream_keeps_none` (shared Given of r19, r22, r2 and work-queue r7): setup only; the repository now has id ctx-a (D6).
- tests/scenarios/requests_steps.py `status_is` and requests_write_steps.py `has_no_resolution`: step pattern respelled (`parsers.re` with a stricter pattern) so a new step "q2's status is as it was and q2 has no resolution" is not ambiguous; same assertions.
- The Thens of requests_steps.py/requests_write_steps.py now read a request through `text_of` (the upstream's file, or with sent items written in) instead of the file directly: a respelling; for single-repository scenarios the same file is read.
- The steps only the two retired scenarios used were removed with `features retire`.

## Open questions

- A title, question or answer text with a newline (probe J): not chosen; take-in and `work request` write it as given.
- Take-in of a request whose id the upstream already keeps: `store` writes the sent id and would overwrite; not chosen.
- Take-in of an answer or turn on a request the upstream does not keep, or an item whose named asker is not the request's asker: not chosen (a Refused from `reply`/`turn` aborts the take-in with the item left on the remote).
- Exit status of a take-in that leaves items: success (r41 does not say).
- A push or fetch failure at the asker's commands, at publishing and at take-in: surfaces as a git Refused; not chosen.
- An asker repository that has an upstream setting and raises an internal request: every `--from <own id>` request there is sent.
- A repository with more than one upstream: unsupported.
- An asker answering or passing the turn again before the upstream took in its last message: the published request still shows the asker's turn, so the second is sent too.
- `work show <id>` for an id that is no request/initiative/work-item: wording unchanged. In an asker's repository `work show <request>` is not implemented (no scenario).
- Zero-line lines file (probe K): unchanged.

## Plan contained code

No (the plan is prose); nothing pasted.

## Result

What someone can now do: an asker's repository (`.shop/requests.toml` with `[asker]`) raises a request, answers a question and passes the turn with the same `work request`, `reply`, `turn`, with no checkout of the upstream; the upstream (`[upstream]` with an allow list) runs `work take-in`, or `work run`, which takes in first; `work show <q>` prints a request; the side checks and `work request`'s gate refuse as r30-r34, r45 say.
Surprising: the tests cannot import the scripts' modules (the runner's PYTHONPATH shadows the worktree's), so the test world talks to the remote with git directly. Supervision's raise (`supervise_raise`) is unchanged (D9): it still calls `workqueue_request.request`, which has no gate.

Commits: 8712f769 (carrier, take-in, side checks, gate, retire), 31436ec1 (r25, r40, module map).

## Completeness check

`python3 .../tools size --limit 300` printed nothing: no file is over 300.

## Concerns

None blocking. Note `work_queue_request_steps.py` was not touched (its Given calls the shared function).
