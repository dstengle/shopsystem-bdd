# Research of w209: design-model-check r120 (v17) and r121 (v18)

Tools: `tools refs foreign` ran (2 references, 1 production, 0 tests; by refs). `tools tests-of` and `untested` have no map (`tools: no map`), so every test list below is by search. Probes are in `.shop/scratch/w209-1-research/` (`probe_v17_v18.py`, `probe_v17_obs.py`, `probe_work_thread.py`, `probe_work_refusals.py`, `probe_steps.py`), run with `python3 -m pytest -q -s -n 0 <path>`.

## 1. Why each accepted scenario is red today

Scenarios: `features/design-model-check.feature`, r120 at line 864, r121 outline at line 904.

**r120: "a request that is part of no job-thread, cites no origin and is raised for no request is v17"**
- Command: `python3 -m pytest -q "tests/scenarios/test_design_model_check.py::test_a_request_that_is_part_of_no_jobthread_cites_no_origin_and_is_raised_for_no_request_is_v17"` (run).
- Fails at its first step: `StepDefinitionNotFoundError: Given "a request q1 that is part of no job-thread, cites no origin and is raised for no request"` (line 866). The only Given like it, `tests/scenarios/design_model_check_requests.py:96`, matches "...and cites no origin$" alone.
- Also undefined, by matching each step line against the patterns (`probe_steps.py`, run): Given "a request q3 that is part of a job-thread" (line 868, no pattern) and Given "a request q4 raised for the request request/missingmass.io/shopsystem/other/q7" (line 869, no pattern). Then "v17 does not name q2, q3 or q4" (line 872) does not match the pattern at `tests/scenarios/design_model_check_then.py:129` (run: NO MATCH; the pattern takes one id or "and"/"or" pairs).
- Missing in code: `scripts/model.lp:256-259` has no raised-for term in v17. `scripts/model_requests.py:33-35` reads only `part_of` and `source`. No job-thread node is ever created in this context (no reader), so `in_thread` (`model.lp:257`) never holds.

**r121: "an id of a kind kept in .shop/work/ with another context's path is v18 unless a request is raised for it"** (7 rows)
- Command: three rows run by node id (`python3 -m pytest -q "tests/scenarios/test_design_model_check.py::test_an_id_of_a_kind_kept_in_shopwork_with_another_contexts_path_is_v18_unless_a_request_is_raised_for_it[...]"`, run; the other four rows share their Givens, read).
- Each run fails at `StepDefinitionNotFoundError`: Given "no request is raised for it" (line 909) or Given "a request q9 of this context is raised for it" (line 909). Six rows have the first, one the second.
- Missing in code: `scripts/model.lp:260-261` `v18(X) :- foreign(X).` has no exemption. `scripts/model_facts.py:86-90` `foreign()` emits every foreign work id with no look at what requests are raised for. `model_requests.py` reads no raised-for field.

## 2. What the system answers today

Each probe ran `scripts/model --root <repo> check` and `check --json` on a repository built in scratch (run; `probe_v17_v18.py`, `probe_v17_obs.py`, `probe_work_thread.py`).

| probe | Givens | today's answer | the scenario expects |
|---|---|---|---|
| v17 (no observation file) | q1 part_of initiative; q2 source observation (absent); q3 part_of job-thread (absent); q4 raised_for only | v17 names q1, q2, q3; q4 is a file problem "neither part_of nor source", not v17 | q1 named; q2, q3, q4 not named |
| v17obs (observation file present, as the scenario's `observation()` Given writes it) | as above, q4 with source and raised_for | v17 names q1 and q3; q2 and q4 not named | q3 not named |
| v17b (no observation file) | q4 source observation + raised_for; q5 part_of initiative + raised_for | v17 names q4 and q5 | q4 not named by origin; q5 named |
| v17c (the scenario's own data empty: no request) | none | 0 violations, exit 0 | nothing named |
| v18a | initiative source request other/q3; nothing raised for it | v18 names other/q3 (with v10a and an unresolved row for the initiative's source) | names |
| v18b | as v18a, plus q9 of this context with source observation and raised_for other/q3 | v18 still names other/q3; v17 names q9 | other/q3 not named; q9 not named |
| v18c | initiative source observation/.../other/2026-10-01-x | v10a and unresolved; not v18 | does not name |
| v18d | initiative source request/.../shopsystem-bdd/q3 (own context) | v10a and unresolved; not v18 | does not name |
| v18e | initiative source work-item/.../other/w4 | v18 names it | names |
| v18f | q9 raised_for other/q3, neither part_of nor source | v18 names other/q3; file problem on q9 | - |
| `work request --thread job-thread/.../save-x`, then check (`probe_work_thread.py`) | a request written by the existing way | v17 names q1 "part of no job-thread and cites no origin" | not named |

Nearest case of r120: the cited observation absent makes `cites_origin` fail (`model.lp:258` needs `node(O, K)`), so a request whose origin names nothing is v17, with no unresolved row (D4). `work request --source` and `--thread` both write files that `check` reads (run).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/model.lp:256-259 v17 rule | a request in no thread and with no origin is v17 | a request raised for a request is not v17 (r120) | the r120 scenario (red); deprecated r115 is not collected | search (`grep v17`) |
| scripts/model.lp:257 in_thread | holds only when node(T, "job-thread") exists | never holds in this context: no job-thread node is created (D1) | the r120 scenario and the v17 probes (run) | search (`"job-thread"` in scripts: model.lp and model_facts.py:25 only) |
| scripts/model.lp:260-261 v18 rule | every foreign id is v18 | an id a request is raised for is not v18 (r121) | the r121 scenario (red) | search |
| scripts/model_facts.py:86-90 foreign(), called from qualify (lines 80, 95) | emits foreign for every other-context work id | no change needed: qualify emits foreign for a raised-for target too (read); the exemption fits in the solve | the r121 scenario (red); r117 deprecated is not collected | refs (2 references, 0 tests) |
| scripts/model_requests.py:33-35 request_links | reads part_of and source only | must read the raised-for field as a request-to-request relation | the r120 scenario (red); the request Givens of r113, r114, r116, r119 run through it (read) | search (`req_part_of`, `req_source`) |
| scripts/model_requests.py:53-54 request_form | a request with neither part_of nor source is a file problem (r112) | a raised-for-only request (r120's q4) is a file problem today; the form must accept the raised-for field, or the Given must add an origin (question 2) | none in tests/scripts (search for "neither part_of nor source": none); the r112 scenario executes the function on its `no asker` branch (read) | search |
| scripts/workqueue_request.py:87-106 request() | writes part_of (thread) or source; refuses neither | no raised-for parameter; spec r29 and r44 want one (D2) | tests/scenarios/requests_write_steps.py:94 (refusal) | search (`--raised-for` absent from scripts/work) |
| scripts/workqueue_done.py:14-16 ids a request's part_of and source name | used by the initiative done check (r114) | a raised-for target is a request, not an initiative: no change needed | the r114 scenario (read) | search |
| scripts/model_work.py:116 initiative sources through qualify | emits foreign for an initiative's source | no change; the r121 Given "an initiative whose source names ..." runs through it | the r121 scenario (red) | search |

## 4. Tests the requirements make impossible to keep

- `tests/scenarios/test_design_model_check.py`: `pytest --collect-only -k "v17 or v18 or foreign"` (run) lists the r120 test and seven r121 rows, and nothing else. The deprecated r115 and r117 scenarios are not collected (run). Nothing that stays collected breaks: r115 would still hold for its own data (no origin, no raise), and it is not run.
- `tests/scripts/test_model.py`, `test_model_glossary.py`, `test_model_output.py`, `test_model_reading.py`, `test_model_withdrawn.py`: 42 passed, 26 subtests (run). By search for v17, v18, foreign, `neither part_of`, raised, job-thread: none asserts on those. None impossible to keep.
- `tests/scenarios/requests_*`: the writer refusal "neither an origin nor a job-thread" (`requests_write_steps.py:94`) is unchanged by r120 and r121 (read).
- Not a test: the work-item's Retires quotes the deprecated scenario "...v17 (deprecated)" under `(design-model-check @r120)`, while the feature has it tagged `@r115 @deprecated` (`features/design-model-check.feature:853-854`, read). Question 3.
- Read, not run: `model.lp:243-247` `own_request` (r114) uses `req_part_of` and `req_source` unchanged by r120 and r121.

## 5. A step the work-item skips

The raised-for path is the writer `work request --raised-for` that spec r29 and r44 name. The existing `work request` path:
- refuses an empty delegation (read, `workqueue_request.py:93`);
- refuses a request with neither `--source` nor `--thread`, writing nothing: "the request names neither an origin (--source) nor a job-thread (--thread)", exit 1, no requests directory (run, `probe_work_refusals.py`);
- refuses a line not in the strict EARS form: "line 1 is not in the strict form model check holds", exit 1 (run, `probe_v17_v18.py`, `test_work_request_raised_for` second call);
- commits the request file (`workqueue.committed`): run, the log shows "work request: q1" and the tree is clean (`probe_work_refusals.py`).
A raised-for path must keep the r31 refusal ("neither --raised-for nor --thread"); it is not produced today, since no raised-for path exists. `scripts/work` rejects the option: run, `work request ... --raised-for q7` exits 2 "unrecognized arguments: --raised-for q7" (`probe_v17_v18.py`).

## 6. Defects

**D1. A request written with `--thread` is reported v17.**
- Repro: `work request "Show the queue" --from ctx-a --lines lines.md --thread job-thread/missingmass.io/shopsystem/shopsystem-bdd/save-x` (in a git repo with spec/index.md), then `scripts/model --root <repo> check` (run, `probe_work_thread.py`).
- Came back: exit 1, "v17 a request that is part of no job-thread and cites no origin (1): request/.../q1". The request's `part_of` names a job-thread, and no job-thread node exists in this context (model reads none, r19).

**D2. `work request --raised-for` is refused.** Spec requests r29, r44.
- Repro: in a git repo, `scripts/work request "Show the queue" --from ctx-a --lines lines.md --raised-for q7` (run, `probe_v17_v18.py`).
- Came back: exit 2, "unrecognized arguments: --raised-for q7".

**D3. A hand-written request raised for a request, with no origin, is a file problem.** Spec r44 and r31 against the form check r112.
- Repro: `.shop/work/requests/q9.md` with `id: request/missingmass.io/shopsystem/shopsystem-bdd/q9`, `asker: internal`, `raised_for: request/missingmass.io/shopsystem/other/q3`, no `source`, no `part_of`; then `check` (run, `probe_v17_v18.py`, v18f).
- Came back: "file: .shop/work/requests/q9.md: not the form `work request` writes: neither part_of nor source". Both readings: question 2.

**D4. A request whose `source` names nothing is not printed unresolved.** Spec design-model-check r24 says a `source` that names nothing is unresolved.
- Repro: `.shop/work/requests/q2.md` with `source: [observation/missingmass.io/shopsystem/shopsystem-bdd/obs-1]` and no observation file; then `check` (run, `probe_v17_v18.py`, v17).
- Came back: "v17 names q2", "0 unresolved references". `model_requests.request_links` never calls `want()` (read), so no unresolved row. With the observation file present, q2 is not v17 (run, `probe_v17_obs.py`).

## 7. The file set

Production files to change:
- `scripts/model.lp`: the v17 rule (256-259) and v18 rule (260-261) take the raised-for relation; a `#defined` for it beside line 26. No new label needed. Found by search and read. Not Python: no size limit.
- `scripts/model_requests.py`: `request_links` (29-41) reads the raised-for field as a request relation; `request_form` (53) accepts it as an origin, if question 2 gives that reading. Found by read and run (D3).

Test and feature files to change:
- `tests/scenarios/design_model_check_requests.py`: Givens for r120's three phrases, r121's "no request is raised for it", and r121's "a request q9 of this context is raised for it". Found by run (StepDefinitionNotFoundError).
- `tests/scenarios/design_model_check_then.py`: the Then pattern at line 129 and the split at line 133 take a comma list ("q2, q3 or q4"). Found by `probe_steps.py` (run).
- `features/design-model-check.feature`: remove the deprecated `@r115` scenario (853-861), as the Retires says. The `@r117 @deprecated` outline (884-901) is deprecated for removal and is not in the Retires (question 3).

Path modules, edited or not. Line count by `wc -l`; room is 300 minus the lines. `tools size --limit 300` printed no file over the limit (run).
- `scripts/model`: 139 lines, room 161. The CLI; no change (read).
- `scripts/model_check.py`: 139, room 161. Solves and prints; no change unless a label is added (read).
- `scripts/model_facts.py`: 287, room 13. `foreign` and `qualify` need no change (read, refs). Little room if one is needed.
- `scripts/model_requests.py`: 63, room 237. Edited (above).
- `scripts/model_work.py`: 219, room 81. Initiative sources and observation nodes through qualify and `read_records`; no change (read).
- `scripts/model_parse.py`: 271, room 29. Frontmatter reader; no change (read).
- `scripts/workqueue_request.py`: not edited for r120 and r121; read for D1 to D3 (line count not taken).
- `tests/scenarios/design_model_check_requests.py`: 132, room 168. Edited.
- `tests/scenarios/design_model_check_then.py`: 255, room 45. Edited.
- `tests/scenarios/test_design_model_check.py`: 55. No change; generated by `scenarios()`.
- `tests/scenarios/conftest.py`: 176, room 124. `observation()` and `write()` used by the Givens; no change (read).

## Questions for the plan (both readings given, no choice made)

1. Job-thread in this context. Reading A: a `part_of` naming a job-thread counts as in-thread from the id alone, as r121 judges foreign ids. Then `model.lp` changes and the r120 Given "is part of a job-thread" needs no file. Reading B: only a job-thread file of this context counts. Job-threads are product-level and "Not yet" (`spec/capabilities/design-model-check.md`, "Not yet"), so the Given can pass only by writing a file model does not read (r19). Today the thread request is v17 (D1).
2. Raised-for alone. Reading A: a request with the raised-for field and no origin is well formed; `request_form` accepts it, and r120's q4 is neither v17 nor a file problem. Reading B: the form check stands, and r120's Given must add `source` or `part_of` to q4. Under B the Then "does not name q4" passes only because q4 is a file problem.
3. Retires. The work-item retires "...v17 (deprecated)" under `@r120`; the feature tags it `@r115 @deprecated`. Reading A: retire the `@r115` scenario, the one the feature has. Reading B: the Retires id is right and names no scenario. The `@r117 @deprecated` outline is not in the Retires either.
4. The field name. The spec (r29, r44) does not name the request field. `docs/design-model/design-model.md:95` and `grammar.md:77` name it `raised_for`. Nothing writes it (D2). The probes used `raised_for` by hand.
5. The r121 exemption applies to request ids only (the spec says "the request a request is raised for"). Reading A: exempt through a raised-for fact, which only requests name. Reading B: exempt any id a raised-for field names. The scenario rows are the same under both.
6. The r121 Given "a request q9 of this context is raised for it" needs q9 with an origin, or D3 applies. The Given must write one.
