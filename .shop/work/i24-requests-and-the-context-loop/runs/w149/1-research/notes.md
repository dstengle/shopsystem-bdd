# w149 research notes

Work-item w149: requests r8, r9 (fix: a delivered request stays delivered on the upstream's `work turn`).
Accepted scenarios: 3 in features/requests.feature (lines 113-132). Tools: `tools map` absent (no map), so every
test list below is `by search`; `refs` gives 0 for scripts/work (no .py name) and is not relied on.
Probes: scratch `.shop/scratch/w149-1-research/probe_turn.py`, repos under `.../repos/` (git-ignored, tree clean).

## 1. Why each scenario is red today

Command for all: `python3 -m pytest -q <node id>` (node ids from `--collect-only`), run.

- `test_the_upstream_ending_its_turn_with_every_line_accepted_refused_or_withdrawn_and_one_accepted_sets_the_status_to_accepted`: **green** (run, passed).
- `test_the_upstream_ending_its_turn_on_a_delivered_request_with_every_line_accepted_leaves_the_status_delivered`: **red** (run).
  Failure: `tests/scenarios/requests_steps.py:71 status_is`, `assert status_of(...) == status` gives `accepted`, expected
  `delivered`. Missing: `scripts/workqueue_request.py:turn` (lines 97-109) has no guard for a `delivered` status; its
  r8/r9 branch (lines 103-107) sets `accepted` or `refused` over it. Step definitions exist (requests_steps.py:44-49, 69-71).
- `test_the_upstream_ending_its_turn_with_every_line_refused_or_withdrawn_sets_the_status_to_refused`: **green** (run, passed).

## 2. What the system answers today

Probes (run, `python3 -m pytest -q -s .shop/scratch/w149-1-research/probe_turn.py -n 0`, 10 passed). Each drives
`scripts/work` (the worktree's) in a fresh repo, through `work request`, `work outcome`, `work turn`, `work resolve`,
`work start`.

- Scenario 2 Given, written by hand (status delivered, turn upstream, outcomes accepted, accepted), then `work turn q1`:
  exit 0, status `accepted`, turn `asker`. Reproduces the red scenario.
- Scenario 1 Givens through commands (lines 3: accepted, refused, withdrawn), then `work turn`: `accepted`, turn asker.
- Scenario 3 Givens (lines 2: refused, withdrawn): `refused`. Also withdrawn, withdrawn: `refused`.
- Nearest cases:
  - 2 lines, one outcome only (accepted): `awaiting-asker`.
  - 2 lines, accepted + question: `awaiting-asker`.
  - 2 lines, accepted + accepted, plus an outcome for line 3 (no line 3): `awaiting-asker` (words 3 != lines 2).
  - 2 lines, accepted + accepted: `accepted`.
  - 0 lines (empty `--lines` file): `work request` exit 0; `work turn`: status `refused` (vacuous "every line refused or withdrawn"). Question, see part 6.
- Real chain (`probe_turn.py::test_real_chain_delivered_then_turn_back_to_accepted`), 2 accepted lines:
  - `work turn` (upstream): `accepted`, asker.
  - `work resolve q1 --line 1 thing#r1 0.26.0 --line 2 thing#r2 0.26.0`: `delivered`, turn asker.
  - `work turn` (asker): `awaiting-upstream`, turn upstream. The delivered request is reopened (r18 applies to it).
  - `work turn` (upstream): `accepted`, turn asker. The delivered request is reset (the defect).
  - `work start q1`: exit 0, prints `i1`. After the reset, an initiative is begun from the request (see part 3 row 4).

## 3. Old assumptions

Table: the old form is "a request's status is set by its line outcomes on every upstream `turn`" (no delivered case),
and "a request's `delivered` status is what finishes its initiative". Found by: `scripts/workqueue_request.py` read, its
callers in `scripts/work` (cmd_turn, cmd_resolve; lines 72-79), then the greps of `accepted|delivered` in scripts/.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_request.py:turn (lines 103-108) | sets `accepted`/`refused` from the outcomes, whatever the status before | must not touch a `delivered` request; r8/r9 hold only when not delivered | test_requests.py r8, r9, r17/r18 scenarios (by search; the delivered one fails) | read; `scripts/work` cmd_turn:72 |
| scripts/workqueue_request.py:turn (lines 101-102) | in the asker's turn, sets `awaiting-upstream` whatever the status | a `delivered` request is reopened by it (probe, part 2); r18 as written covers it, the requirement does not say what a delivered request does | test_requests.py r18 scenario (by search; status awaiting-asker, not delivered) | probe |
| scripts/workqueue_request.py:resolve (line 116) | refuses unless `accepted`; then writes the resolution and `delivered` | after the reset, `resolve` is allowed again on a delivered request (read) | test_requests.py r10, r11 scenarios (by search) | read |
| scripts/workqueue_done.py:_holds (line 36) | an initiative qualifies only when each request it names is `delivered` | a reset request stops qualifying; read from workqueue.py:240 (withdraw) and workqueue_request.py:124 (resolve) | tests/scenarios/test_work_queue.py "sets the initiative to done" examples (by search; they give delivered, accepted, and never turn a request) | read |
| scripts/workqueue_start.py:start (line 31) | refuses unless `accepted` | the reset reopens `work start` on a delivered request (probe: start succeeded) | test_work_queue.py "start on an accepted request ..." (by search) | search "accepted" |
| scripts/workqueue.py:requests (lines 113-120) and scripts/work cmd_show/cmd_status (lines 33-39) | print each request's status | a reset request shows `accepted` (read) | tests/scenarios/requests_show_steps.py (by search; not run) | read |
| scripts/model.lp:247-250 (v_d1, v_d3) | a done initiative needs a delivered request; a delivered request needs a done initiative | after the reset, a done initiative with its request `accepted` is flagged by v_d1 (read) | tests/scenarios/design_model_check_requests.py (delivered Givens, by search) | read of model.lp |

## 4. Tests the requirements make impossible to keep

`tools tests-of` has no map: `by search`. Searched tests for `work turn`, `accepted`, `delivered` (tests/).
- test_requests.py + requests_steps.py: the delivered scenario (r8) is the target and fails now; it asserts the new
  behaviour, so it stays as written. Scenarios r8-accepted, r9 pass both before and after.
- No test asserts that an upstream `turn` on a delivered request sets `accepted`. Checked: test_work_queue.py,
  work_queue_start_steps.py, design_model_check_requests.py, requests_show_steps.py (their statuses are given, not reached by `turn`).
- Verified sound: the start and done tests in test_work_queue.py (given statuses only).
- Result: none that can no longer pass; the only red one is the target.

## 5. A step the work-item skips

`turn` has one path (`_change`: read, commit). The change is a guard on the status branch of the same path; it skips no
step. Read: `_change` (workqueue_request.py:47-52) commits the file for every outcome, including a delivered request.
Effects only the status branch produces (r8/r9/r17/r18): the status written. Probed in part 2 (delivered reopened by
asker's `turn`, delivered reset by upstream's `turn`).

## 6. Defects

Each reproduced by probe_turn.py (run).

### D1 upstream `work turn` resets a delivered request to accepted
Commands: `work request`, `work outcome q1 1 accepted`, `work outcome q1 2 accepted`, `work turn q1`, `work resolve q1 --line 1 thing#r1 0.26.0 --line 2 thing#r2 0.26.0`, `work turn q1` (asker), `work turn q1` (upstream).
Came back: after resolve `delivered`; after the last turn `accepted`, turn `asker`. Same with a hand-written delivered Given (scenario 2): `accepted`.

### D2 asker's `work turn` on a delivered request sets awaiting-upstream
Same chain, step `work turn q1` (asker): `awaiting-upstream`, turn `upstream`. Resolution is still written.

### D3 `work outcome` accepts a line number the request does not have
`work request` with 2 lines, `work outcome q1 3 accepted` exit 0; with 2 accepted and 3 accepted, `work turn` gives
`awaiting-asker`, not `accepted`. Question: the spec (r15) says "line n" but refuses nothing about n beyond Lines.

### D4 (question) a request with no lines
`work request` with an empty file exits 0; `work turn` gives `refused`. Question: whether a request needs a line (r2/r3 say nothing).

## 7. The file set

Production:
- scripts/workqueue_request.py (131 lines, room 169): `turn` guards the r8/r9 status branch so a `delivered` request keeps its status (and decides D2). Found by: the red scenario, read of turn, probe.
Tests: none need changing (step definitions and the scenario exist: requests_steps.py:44-49, test_requests.py, features/requests.feature:121-125). Tests that must keep passing: test_requests.py (9 lines) and requests_steps.py (108 lines); test_work_queue.py (287 lines, room 13) executes workqueue_start/done, changed by nothing.

Modules on the change path, edited or not:
- scripts/workqueue_request.py: 131 lines, room 169 (edited).
- scripts/workqueue.py: 286 lines, room 14 (`committed`, `read`, `requests`; not edited).
- scripts/work: 147 lines, room 153 (cmd_turn, cmd_resolve; not edited).
- scripts/workqueue_done.py: 67 lines, room 233 (`_holds` reads the delivered status; not called by `turn`; not edited).
- scripts/workqueue_start.py: 43 lines, room 257 (accepted check; not edited).
Size limit: CLAUDE.md gives 300 lines; `tools size` not run.
