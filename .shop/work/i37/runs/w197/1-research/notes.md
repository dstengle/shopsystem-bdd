# Research of w197 (requests r7, r23, r24)

Method: no `tools map` exists (`tools tests-of` answers "no map"), so every test list below is `by search`. `tools refs` ran on the helpers; the `work` command has no `.py`, so `refs` cannot see its dispatch (`scripts/work:83-85`, `:152-161`): `read`. `tools size --limit 300` printed nothing: no file over the limit. `git status --porcelain` was empty at start and is empty now.

Accepted scenarios (features/requests.feature, bound in tests/scenarios/test_requests.py):
- S1 deprecated r7 (two Examples): `test_turn_passes_the_requests_turn_from_the_side_to_the_other_side_deprecated[upstream-asker]`, `[asker-upstream]`
- S2 r7: `test_turn_on_a_request_it_does_not_set_to_accepted_passes_the_requests_turn_from_the_side_to_the_other_side[upstream-asker]`, `[asker-upstream]`
- S3 r23: `test_the_upstream_ending_its_turn_on_a_request_that_turn_sets_to_accepted_keeps_the_requests_turn_the_upstreams`
- S4 r24: `test_resolve_setting_a_requests_status_to_delivered_passes_the_requests_turn_to_its_asker`

## 1. Why each scenario is red today

Command, run from the worktree: `python3 -m pytest -q <node id>` for the six node ids above (`-n 0` for serial output). Result: 4 failed, 2 passed. (The two passing are S1, both Examples.)

- S1 deprecated [upstream-asker], [asker-upstream]: **pass** (run). Retired by w197; its binding is generated from features/requests.feature line 121 and stays until that scenario is removed.
- S2 [upstream-asker], [asker-upstream]: **red in the step, not the code**. `tests/scenarios/requests_steps.py:71` (`status_is`) asserts `status_of(...) == "not accepted"`, a literal string equality, so it cannot pass whatever the code does (actual: `awaiting-asker` / `awaiting-upstream`). The turn Then of these scenarios is already right today (probes B, C in section 2). See defect D2.
- S3 r23: `tests/scenarios/requests_steps.py:93` (`turn_is`): expected `upstream`, got `asker`. Status step passes (`accepted`). Cause: `scripts/workqueue_request.py:turn`, lines 156-160: after setting `accepted` it runs `_with_field(text, "turn", "asker")` unconditionally.
- S4 r24: `requests_steps.py:93`: expected `asker`, got `upstream`. Cause: `scripts/workqueue_request.py:resolve`, line 173: writes the resolution and `status: delivered` only; it never writes `turn`.

## 2. What the system answers today

Probe file: `.shop/scratch/w197-1-research/probe_turn.py` and `probe_request.py`. Command: `python3 -m pytest -q -s -n 0 -p no:warnings <file>`. Each case in its own scratch git repo; `work` run as `python3 scripts/work <args>` from that repo. All `run`.

- A `turn q1`, upstream's turn, lines accepted/refused/withdrawn, status open: rc 0, `status: accepted`, `turn: asker`. (S3 fails here.)
- B `turn q1`, upstream's turn, one line with outcome `question`: rc 0, `awaiting-asker`, `turn: asker`. (S2 turn part correct.)
- C `turn q1`, asker's turn: rc 0, `awaiting-upstream`, `turn: upstream`.
- D `resolve q1 --line 1 thing#r3 0.26.0`, accepted, upstream's turn: rc 0, `status: delivered`, `turn: upstream`, resolution `1. thing#r3 0.26.0`. (S4 fails here.)
- E nearest, request with zero lines and zero outcomes, upstream's turn: `turn` gives `refused`, `turn: asker`, rc 0. See D1.
- F `turn`, status `delivered`, both lines accepted, upstream's turn: `delivered`, `turn: asker` (the status guard holds).
- G second `turn` on the accepted request of A (now the asker's turn): `awaiting-upstream`, `turn: upstream`. Under r23 the first `turn` keeps the upstream's turn, so a second `turn` by the upstream would pass it to the asker: ambiguous, see section 6.
- H `resolve q1` on an `open` request: rc 1, stderr `work: q1 is open, not accepted; work resolve resolves only an accepted request`; nothing written.
- I `outcome q1 1 maybe` (any word accepted, no check of the word), then `turn`: `awaiting-asker`. Read: r17's "other than accepted, refused or withdrawn" allows other words, so no defect.
- J `resolve q1` on accepted, asker's turn: `delivered`, `turn: asker`, unchanged turn.
- K `request "No lines" --from ctx-a --lines <file holding one blank line> --source x`: rc 0, writes `q1.md` with empty `## Lines`. See D1.
- L `turn q9` (missing): rc 1, `there is no request q9 under .shop/work/requests`.
- Read: `turn` takes no side argument, so either side's run flips the turn. Commands `outcome`, `ask`, `reply` do refuse in the other side's turn (`workqueue_request.py:123, 132, 142`).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_request.py:turn, lines 156-160 | after the status is set, always `turn: asker` | r23: an upstream's end that sets `accepted` keeps `turn: upstream`; r7 narrowed to requests it does not set to accepted | by search: S2 (two), S3 red; r8/r9 accepted/refused tests (`test_requests.py`, status only), r17/r18 tests, S1 (two), intake: `supervision_intake_steps.py` (turn asserted only with a question, unaffected) | read of `turn`; search of `"turn"` in tests/scenarios |
| scripts/workqueue_request.py:resolve, line 173 | sets `status: delivered`, leaves `turn` | r24: a resolve that sets `delivered` passes the turn to the asker | by search: r10, r11 (run in asker's turn, no turn Then), S4 red | read of `resolve`; search for `work resolve` in tests |
| scripts/work:cmd_turn (lines 83-85) and cmd_resolve | pass to `workqueue_request.turn` / `resolve` only | none: no change, dispatch only | by search: as above | read |
| scripts/supervise_intake.py:Intake brief, lines 63-64 | brief says "Then pass the turn once with `work turn`" and the round's end leaves a request awaiting the asker | after an accepted outcome the turn stays the upstream's; the text stays true, but its consequence changes (nothing asks the upstream to resolve) | by search: tests/scenarios/supervision_intake_steps.py (intake_started, line_one_has_outcome: question present, so awaiting-asker, unaffected) | read; `supervise_intake.py:WAITING` = open, awaiting-upstream, so a request left accepted is not re-run |
| scripts/workqueue.py:requests (line 124) and `work show` (scripts/work:39-40) | yields and prints each request's turn | an accepted request now shows the upstream's turn | by search: requests_show_steps.py (fixture turns; unaffected) | read |
| scripts/workqueue_done.py:becomes and scripts/supervise_all.py:24 | read `status` only (delivered, accepted) | none: turn not read | none | read |
| spec/index.md:134 (glossary "turn") | already says: passed unless the request becomes accepted, and to the asker when delivered | none: already the new rule | none (doc) | read |

## 4. Tests the requirements make impossible to keep

Mark: `by search` (no map). I listed every test that asserts a turn: the `turn_is` step (requests_steps.py:91-93) and the literal `\nturn: asker\n` in supervision_intake_steps.py:52.

- tests/scenarios/test_requests.py S2 [upstream-asker], [asker-upstream]: cannot pass as written, whatever the code does (step literal, D2). Keep the scenario; fix the step (section 7).
- S3 and S4: red now, wanted green. Not kept as they are: they describe the new rule.
- S1 deprecated: passes today and under the new code (it uses a `question` line, so status awaiting-asker and turn asker on both sides). Kept until the Retires removal; then removed with its feature scenario.
- Turn asserted as `asker` after an accepted turn or after a resolve: none found by search. r8, r9, r10, r11, r17, r18 check only status.
- supervision_intake_steps.py:47-52 (intake with a question on line 2): sound under r23 (the request is awaiting-asker, not accepted).
- Verified sound, looked at: requests_show_steps.py (fixtures set turn by hand), supervision_request_steps.py (awaiting-upstream/awaiting-asker fixtures), supervision_done_steps.py (delivered fixture, turn upstream, no turn Then), design_model_check_requests.py (fixtures with `turn: upstream`, delivered), test_work_queue.py (no `work turn` or `work resolve` in it).

## 5. A step the work-item skips

The r23 path (accepted, upstream keeps the turn) skips the last step of `turn`, `_with_field(text, "turn", "asker")` (`workqueue_request.py:160`). Effects only that step produces, both `read`:
- `turn: asker` makes the asker the side that may `work reply` (`workqueue_request.py:142` refuses `reply` in the upstream's turn) and makes the upstream's `outcome`/`ask` refuse (`:123`, `:132`). Under r23 the upstream keeps `outcome`/`ask` and the asker's `reply` stays refused. Probe A shows the value that changes.
- The commit (`workqueue.committed`) is the same; nothing else.

The r24 path adds to `resolve` a step it does not have (`turn` write). No existing refusal or effect of `resolve` is skipped by it: `resolve` already refuses a non-accepted request (probe H). `workqueue_done.becomes` (`:176`) is evaluated on status only.

## 6. Defects

D1. `work request` writes a request with no lines, and `turn` then refuses the request it did not judge.
Command: `python3 .shop/scratch/w197-1-research/probe_request.py` (test K), `run`. An empty lines file (one blank line) gives rc 0 and a `q1.md` with `## Lines` empty; then `work turn q1` gives rc 0, `status: refused`, `turn: asker`.
Where: `scripts/workqueue_request.py:request`, lines 97-102: the lines loop checks each line's form; nothing checks that there is at least one line.

D2. Test defect: `Then q1's status is not accepted` cannot pass.
Command: `python3 -m pytest -q "tests/scenarios/test_requests.py::test_turn_on_a_request_it_does_not_set_to_accepted_passes_the_requests_turn_from_the_side_to_the_other_side[upstream-asker]"`, `run`. Result: `tests/scenarios/requests_steps.py:71`: `AssertionError`, status `awaiting-asker`. The Then at `requests_steps.py:69-71` compares `status_of(...) == status` with `status` = the literal "not accepted".

No other defect found. Turn with the status and turn left as-is (`turn` run twice) is an ambiguity, not a defect: under r23 a second upstream `turn` on an accepted request reads "a request it does not set to accepted" (r7) two ways: pass the turn, or keep it because it sets accepted again. Two readings for the plan.

## 7. The file set

Production:
- `scripts/workqueue_request.py` (183 lines, room 117): `turn` keeps `turn: upstream` when it sets `accepted` (r23); `resolve` writes `turn: asker` with `delivered` (r24). Read of `turn` and `resolve`; probes A, D; failures S3, S4.

Tests:
- `tests/scenarios/requests_steps.py` (108 lines, room 192): the `status is {status}` Then must accept `not accepted` (not accepted = anything but `accepted`), or the feature's wording changes. Needed for S2 to pass (D2).
- `features/requests.feature` (245 lines, a feature file, no line limit): remove the deprecated scenario at lines 121-132 (the Retires of w197), so S1 is no longer run. Not needed to pass S2-S4; the work-item's Retires asks for it. The `@r7 @deprecated` tag is in it.
- `tests/scenarios/test_requests.py` (9 lines): no change (generated from the feature).

Not edited, on the change path:
- `scripts/work` (171 lines, room 129): dispatch only; read.
- `scripts/workqueue.py` (294 lines, room 6): `committed` and `requests` used; no edit needed.
- `scripts/workqueue_done.py` (73 lines, room 227): `becomes` read by `resolve`; no edit.
- `scripts/supervise_intake.py` (123 lines, room 177): the brief text (lines 63-64) may be reconsidered by the plan; not needed by any accepted scenario.
- `spec/index.md` (147 lines): glossary already states the new rule; no edit.
