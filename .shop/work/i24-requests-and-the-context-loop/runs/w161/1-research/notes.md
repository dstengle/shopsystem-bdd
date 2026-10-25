# w161 research notes

Work-item w161 (under batch-measurement, accepts r65, r66, r67). Tools: `tools refs`, `tests-of`, `untested` ran; `tests-of` and `untested` said "no map" (not made), so tests are listed by search. `refs request_of` said 0 references, but `scripts/measure_build.py:10,138` import and call it: refs answer discounted.

## 1. Why each scenario is red today

Run: `python3 -m pytest -q "tests/scenarios/test_batch_measurement.py::<name>"` for each of the three. All three fail at their first Given, a StepDefinitionNotFoundError (run).

- an initiative fulfilling a request the queue does not hold is refused (features/batch-measurement.feature:23): undefined Given `i7-cart fulfils the request q3` (line 26). Also undefined, by reading: `the queue does not hold the request q3`, `measure initiative refuses because the queue does not hold that request`, `no measurement is written`.
- an initiative fulfilling a request with no asker is refused (:33): undefined `i7-cart fulfils the request q3, which the queue holds` (line 36). Also undefined: `the request q3 has no asker`, `measure initiative refuses because the request has no asker`, `no measurement is written`.
- an initiative fulfilling more than one request is refused (:43): undefined `i7-cart fulfils the requests q3 and q4, which the queue holds, each with an asker` (line 46). Also undefined: `measure initiative refuses because the initiative fulfils more than one request`, `no measurement is written`.

Step definitions missing: `tests/scenarios/batch_measurement_request_steps.py` (defines only `fulfils the request {request}, whose asker is {asker}` and `fulfils no request`). `tests/scenarios/batch_measurement_then_steps.py` has `nothing is written` (line 29) but not `no measurement is written`.

Code behind: `scripts/measure_read.py:request_of` (46-67) already refuses all three cases (see section 2). Missing in code: nothing for behaviour; the refusal texts differ from the Then wording (`there is no request q3 under .shop/work/requests`; `has no asker`; `fulfils must hold one request id, not ...`), so a Then must match a text the code does not yet use, or the plan changes the text.

World support missing: `tests/scenarios/batch_measurement_world.py`. `World.request` (line 64) is one (id, asker) tuple, and `flush` (93-101) writes one request file and one `fulfils:` line. Needed: several requests, a `fulfils` naming a request with no file, and an empty `asker:`.

## 2. What the system answers today

Probe: `python3 -m pytest -q -s -n 0 .shop/scratch/w161-1-research/probe_measure.py` (and `probe_measure2.py`). `-n 0` is needed, since pytest.ini runs xdist and hides output. Each case builds a scratch repo (initiative i7-cart with log.jsonl, spec/index.md, the requests given) and runs `python3 <worktree>/scripts/measure initiative i7-cart` in it. All run.

| case | exit | what came back |
|---|---|---|
| no fulfils (baseline) | 0 | measurement written, no `request` figure |
| fulfils request/q3, q3 absent (the queue does not hold it) | 1 | `there is no request q3 under .shop/work/requests`; nothing written |
| fulfils q4, queue holds only q3 | 1 | `there is no request q4 ...`; nothing written |
| fulfils q3, q3 with `asker: internal` | 0 | request `{id: q3, origin: internal}` |
| q3 with `asker:` empty | 1 | `.shop/work/requests/q3.md has no asker`; nothing written |
| q3 with no asker line | 1 | same text; nothing written |
| `fulfils: request/q3, request/q4`, both asked | 1 | `fulfils must hold one request id, not 'request/q3, request/q4'`; nothing written |
| `fulfils: request/q3 request/q4` (space) | 1 | same kind of text |
| `fulfils: request/q3, request/q4`, q4 absent | 1 | the multi-id text, not the queue text (shape check runs first) |
| `fulfils: request/q3, request/q4`, q4 no asker | 1 | the multi-id text, not the asker text |
| two `fulfils:` lines, q3 and q4, both asked | 0 | measurement written; request `q3` only (see D1) |
| `fulfils: q3` (bare id) | 0 | request q3 internal |
| q3 file with `status: withdrawn` | 0 | measured as held, request q3 internal (open reading, sec 6) |
| `fulfils:` blank | 0 | measurement written, no request figure |

Every refusal writes nothing: `figures_of` (measure_build.py:118-143) reads the request before `measure_write.write`, and `check_unwritten` runs first.

## 3. Old assumptions

The old form: `fulfils` holds one request id and the first `fulfils:` line is the one read (`workqueue_request.field`, workqueue_request.py:50-52, `re.search` takes the first match).

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/measure_read.py:request_of (55-67) | reads first `fulfils`; refuses a multi-token value, a missing queue request, an empty asker | r65, r66 already refused; r67 refused only for a multi-token value, with wording "must hold one request id" | by search: test_batch_measurement.py scenarios at features :200 (outline) and :214 (not run) | search of scripts/ for `request_of`, `fulfils` |
| scripts/workqueue_request.py:field (50-52) | first match only | r67 needs every `fulfils` line seen: two lines pass silently (D1) | none (no test has two `fulfils:` lines) | search `fulfils` in scripts and tests |
| scripts/supervise_answers.py:35-41 (delegation) | first `fulfils`, rsplit, reads that request's delegation | r67 is scoped to `measure`; here two lines give q3's delegation silently | by search: tests/scenarios/supervision_delegation_steps.py (not run) | search `fulfils` in scripts |
| scripts/supervise_brief.py:67-68 | `data.get("fulfils")`, rsplit, first id | same as above; a brief of the first id only | none (by search, no test has two lines) | search `fulfils` in scripts |
| scripts/supervise_analysis.py:37-42 | runs `measure initiative`; a refusal prints "was refused, so there is no analysis" | the new refusals (r65-67) reach here as the existing refusal path | by search: tests/scenarios/supervision_analysis_steps.py (not run) | search `measure` in scripts |
| scripts/model_work.py:120 | frontmatter `fulfils` to a model fact | not in the requirements; a two-line frontmatter read unknown | none (read only) | search `fulfils` in scripts |
| scripts/model.lp:26,254 | `fulfils/2` fact | not changed | none | search |

## 4. Tests the requirements make impossible to keep

`tests-of` unavailable (no map), so by search. Tests asserting the old single-id behaviour: none found. Search for `must hold`, `one request`, `has no asker`, `there is no request` in tests: only the scenario files named above, no assertion of old text. `tests/scripts/test_measure_runs.py` (two tests, lines 31 and 39) concern empty session.json only: unaffected. `batch_measurement_request_steps.py`'s `gives the request ... as` (line 26) and `gives no request` (line 32) are unaffected by refusals. Read, not run: those scenarios should keep passing. None found that the requirements make impossible.

## 5. A step the work-item skips

None. The work-item adds no path: it only refuses inputs that `request_of` already reads on the one `measure initiative` path. (read)

## 6. Defects

Open reading (not a defect as stated): a request file with `status: withdrawn` still counts as held (probe `probe_measure2.py::test_withdrawn_request_still_held`: exit 0, request q3 internal). r65 says "the queue does not hold" and does not say whether a withdrawn request counts as held.

### D1: two `fulfils:` lines: second request silently dropped

Reproduction: `python3 -m pytest -q -s -n 0 .shop/scratch/w161-1-research/probe_measure.py -k two_fulfils` (case "two fulfils lines q3 and q4"). initiative.md has `fulfils: request/q3` and `fulfils: request/q4` (both requests asked, internal). Came back: exit 0, measurement written, `request: {id: q3, origin: internal}`. Expected per r67: refused, nothing written. `workqueue_request.field` takes the first match.

## 7. The file set

Edited (the changes the scenarios need):
- tests/scenarios/batch_measurement_request_steps.py (35 lines; room 265): the Givens `fulfils the request {r}, which the queue holds`, `fulfils the requests {a} and {b}, ... each with an asker`, `the queue does not hold the request {r}`, `the request {r} has no asker`, and the Thens for the three refusals and `no measurement is written`. Search: the undefined-step error lines in the run.
- tests/scenarios/batch_measurement_world.py (151; room 149): `request` becomes a list; a request may be named with no file; an empty asker. Search: `World.request`, `flush` lines 93-101.
- tests/scenarios/batch_measurement_then_steps.py (202; room 98): `no measurement is written` (or reuse of `nothing is written` at line 29). Search: then-steps file.
- scripts/measure_read.py (206; room 94): request_of: the refusal texts the Thens will match; a count of `fulfils` lines for D1 (or workqueue_request.field returns all values). Search: request_of read in full.
- scripts/workqueue_request.py (142; room 158): only if `field` is changed to see every `fulfils` line (D1). Search: `def field`, its callers in measure_read.py:55, supervise_answers.py:37, supervise_brief.py:67 (by grep of `fulfils`).

Not edited, on the path (read):
- scripts/measure (97 lines; room 203, if counted): entry; CONTRACT line 31-32 already says "a fulfils holding more than one id is refused".
- scripts/measure_build.py (143; room 157): figures_of calls request_of at line 138.
- scripts/measure_write.py (41; room 259): check_unwritten and write; no change.
- scripts/workqueue.py (286; room 14): `read`, `context_path`, `Refused`; no change expected, but the line room is 14.
- tests/scenarios/test_batch_measurement.py (16; room 284): binds the scenarios; star-imports the request steps.

Must keep passing: the batch-measurement scenarios at features :200 and :214 (World.request tuple use), the test_measure_runs.py tests. `tools size --limit 300` printed no file over the limit.
