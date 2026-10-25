# Research of w162: integrate round for a proposed initiative (supervision r79)

Tools: no coverage map (`tools tests-of`/`untested` said "no map"), so every test list here is `by search`. `tools refs` found 0 references to `workqueue_request.accepted_lines`, but `scripts/supervise_brief.py:70` calls it: refs misses module-attribute calls. Callers below are `by search`.
Shell: pytest here collects 2 of 164 `supervision.feature` scenarios (162 deselected), the work-item selection. The r84 scenario is therefore not run from here.

## 1. Why each scenario is red today

Neither accepted scenario is red. Both pass.
- Command: `python3 -m pytest -q "tests/scenarios/test_supervision.py::test_a_proposed_initiative_is_given_to_an_integrate_round_with_the_accepted_lines_of_the_request_it_fulfils" "tests/scenarios/test_supervision.py::test_a_proposed_initiative_that_fulfils_no_request_is_given_no_integrate_round_stays_proposed_and_leaves_nothing_behind"`
- Came back: `2 passed in 1.93s`. Run.
- Scenario 1 (lines 1 and 3 in the brief, not line 2) is met by `scripts/supervise_brief.py:66-70` and `scripts/supervise_rounds.py:32-33`.
- Scenario 2 (no `fulfils`, no round) is met by the `fulfils` gate at `scripts/supervise_rounds.py:32`.
- The gap is not in these two scenarios. Branch review 2 finding R2-F1 (`runs/branch-review/2/findings.md`) names a `fulfils` that the queue does not hold: no scenario gives that case. See part 6, D1.

## 2. What the system answers today

Probe file: `.shop/scratch/w162-1-research/probe_integrate.py` (its own repository, remote and stand-in claude per case, under the scratch directory). Each command: `python3 -m pytest -q -s -p no:xdist -o addopts="" .shop/scratch/w162-1-research/probe_integrate.py -k <name>`. Run for all cases below.

- **P-a, `fulfils: request/ex.com/prod/ctx/q9`, no request file, `work run i1` twice** (`-k missing`). Run.
  - First: exit 1, `work: there is no request q9 under .shop/work/requests`. `initiative.md` now `status: started`. `git status`: ` M .shop/work/i1/log.jsonl`. Branches: `main`, `round/i1-1-integrate`. Log: `proposed -> started`.
  - Second: exit 1, `work: .shop/work/i1/log.jsonl under .shop/work is not committed`.
- **P-b, held request q1, all three lines refused** (`-k refused`). Run.
  - Exit 0. An `initiative-round` session of kind integrate starts; its brief has `Request: q1` and `Accepted lines of the request:` with no line under it.
  - Initiative is `started`. `git status`: `?? .shop/work/i1/runs/i1/`.
  - stderr: `work run: measure initiative i1 was refused ... session.json ... (no usage with input and output tokens)`. The branch-review session then runs.
- **P-c, held request q1 with no `## Outcomes` section** (`-k noout`). Run. Same as P-b.
- **P-d, held request q1 by full id (the form `work start` writes), lines 1 and 3 accepted, `work run i1` twice** (`-k accepted`). Run.
  - First: exit 0. Brief lists `- 1. Line 1 text.` and `- 3. Line 3 text.`, not line 2. Initiative `started`. Measure refusal as in P-b; branch review runs.
  - Second: exit 1, `work: .shop/work/i1/runs/i1/1-integrate/brief.md, result.json, session.json under .shop/work are not committed; commit them before work run starts`.
- **P-e, no `fulfils`, `work run i1` twice** (`-k no_request_twice`). Run.
  - Both exit 0, no session started, `status: proposed`, `git status` empty, no `log.jsonl`. Matches scenario 2.

## 3. Old assumptions

Old form: before w158 (per review 2, not checked in history) every `proposed` initiative got an integrate round, even with no `fulfils`. The requirement now: only a `proposed` initiative with `fulfils`, given the accepted lines of it.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/supervise_rounds.py:due` (32-33) | starts integrate on `proposed` + any `fulfils`; does not check the request exists or has an accepted line | r79 gives "the accepted lines"; scenario 2 says only an initiative with lines is integrated | scenario 1 and P-b/P-c/P-d (run); the missing-request case: none | search `fulfils`, `integrate`; refs |
| `scripts/supervise_rounds.py:round` (48-49) | `start_initiative` (status to `started`, commit) before any check of the request | r84 keeps the transition at round start; r10 says change nothing when the delivery cannot start | P-a (run); none for the missing-request path | search |
| `scripts/supervise_rounds.py:round` (78-79) and `keep_round` (88-97) | integrate skips `move`; a DONE integrate round's stage dir and `session.json` are never committed | r7: a transition commits its stage directories | P-d (run): second `work run` refused; no test checks cleanliness after a DONE round | search `kind != "integrate"` |
| `scripts/supervise_brief.py:integrate_lines` (66-70) | reads the request via `workqueue_request.accepted_lines`; a missing request raises `Refused` (uncaught by `round`'s `except`) | r79 "given the accepted lines" | scenario 1 (run, held request); missing request: none | search |
| `scripts/workqueue_request.py:accepted_lines` (30-35) | returns `[]` when no line is accepted or no `## Outcomes` | the empty-lines case is not defined by r79 | P-b, P-c (run); no test asserts the empty result | search |
| `spec/capabilities/supervision.md:26` (r79 text) | the requirement text is the old unconditional form ("When an initiative is `proposed`") | scenario 2 contradicts it for no request; spec text unchanged | none (text) | search |
| `scripts/model.lp:253-255` (v16a) | an initiative dated after 2026-10-23 with no `fulfils` is a violation | scenario 2 leaves such an initiative `proposed` | design-model-check scenario at `features/design-model-check.feature:819` (by search) | search `fulfils` |
| `scripts/model.lp:308-309` (w_stale_intake) | a `proposed` initiative older than 90 days is a warning | scenario 2's initiative stays `proposed` with no round | none | search |

## 4. Tests the requirements make impossible to keep

- By search (`by search`: no map): tests mentioning `integrate`, `proposed` or `fulfils` under `tests/`. Hits: `tests/scenarios/supervision_rounds_steps.py` (the two accepted scenarios' steps), `supervision_given.py:171` (an `i2` proposed in another session, not a `work run i1` subject), `migration_session_steps.py:32,37` (migration, not `work run`), `batch_measurement_*` and `design_model_check_*` (no `work run`).
- No test asserts the old unconditional form. Result: none to change.
- Verified sound: both accepted scenarios (run, pass). `supervision.feature:1043` (r84, `fulfils: q1`): its Given has a request, so the `fulfils` gate keeps it. Not run here (deselected); read only.

## 5. A step the work-item skips

The integrate path skips the existing round path's status check and its commit with the transition.
- Existing way (read): `supervise_rounds.py:52` `workqueue.agrees(...)` before a gate/apply/formulate round; `supervise_rounds.py:79` `self.move(...)`, which commits the stage directory with the transition (`supervise.py:109`, read).
- Integrate skips both. Effects only that path produces, each shown by a probe:
  - status written to `started` before any check of the request (P-a, run).
  - the round branch made and left behind when the round is refused (P-a, run: `round/i1-1-integrate` in `git branch`).
  - a DONE round's stage directory left uncommitted, so the next `work run` is refused (P-d, run).

## 6. Defects

D1 (= R2-F1 in review 2). `fulfils` names a request the queue does not hold: the run refuses, but only after moving the initiative to `started`, and leaves an uncommitted log and a round branch. Repro: P-a above. Expected by r10: change nothing. Not judged here.

D2. `fulfils` names a held request with no accepted line: the integrate round still starts, with an empty list of lines. Repro: P-b, P-c above. Two readings, both kept: (a) r79 read literally ("given the accepted lines") gives a round with zero lines, so the code is right; (b) scenario 2's Pins ("only an initiative with a request's accepted lines to work from is integrated") gives no round, so the code is wrong. Not judged here.

D3. A DONE integrate round leaves its stage directory (`runs/i1/1-integrate/`: `brief.md`, `result.json`, `session.json`) uncommitted. The next `work run` is refused under r46. Repro: P-d, second run. Read: `start_initiative` commits before the round (`supervise_rounds.py:84-86`); `round()` skips `move` for integrate (`:78`), so nothing commits the stage directory afterwards.

O1 (observation, not a defect yet). In P-b, P-c, P-d the measure step refuses the stand-in's integrate `session.json` (no usage tokens) and the run still exits 0 with that message. I did not check whether real `claude -p` output carries usage; the stand-in's output may be the cause.

## 7. The file set

For the two accepted scenarios: none. Both pass today, and no other test asserts the old form (part 4).

For the finding R2-F1 and D3 (if the work-item takes them):
- `scripts/supervise_rounds.py` (97 lines, room 203). `due`/`round`: check the request before `start_initiative`, refuse with nothing changed, commit the integrate round's stage directory.
- `scripts/supervise_brief.py` (129 lines, room 171). `integrate_lines`: its refusal path, if the check moves out.
- `scripts/workqueue_request.py` (142 lines, room 158). `path_of`/`accepted_lines`: a request-exists check, if one is added there.
- `tests/scenarios/supervision_rounds_steps.py` (236 lines, room 64). Givens for a missing request and for no accepted line, if the new scenario is written.
- `features/supervision.feature`: a new r10 or r79 example for a missing request (not Python; no size limit).
- `spec/capabilities/supervision.md` (spec, not Python): r79 text, if D2 reading (b) is chosen.

On the change's path, edited or not (`wc -l`; room = 300 minus lines; `tools size --limit 300` printed nothing, so no file is over):
- `scripts/supervise.py` 247 lines, room 53. `Run`; calls `self.rounds()` (`:202`), `commit` (`:96`), `move` (`:109`).
- `scripts/supervise_worker.py` 247 lines, room 53. `worker()` (`:165`), `ROUNDS`.
- `scripts/workqueue.py` 290 lines, room 10. `agrees` (`:186`), `move` (`:142`).
- `scripts/workqueue_done.py` 67 lines, room 233. `mark` (`:51`), called by `start_initiative`.
- `scripts/supervise_faults.py` 161 lines, room 139. `Fault`, `fault_of`.
- `tests/scenarios/supervision_world.py` 173 lines, room 127. Shared helpers.
- `tests/scenarios/test_supervision.py` 257 lines, room 43. Binds `supervision.feature` by `scenarios()`.
