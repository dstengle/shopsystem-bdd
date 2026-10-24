# Research of w133: measure gives the origin of the initiative's request

Work-item w133 accepts batch-measurement#r63 and #r64. Accepted scenarios (features/batch-measurement.feature):
- the request an initiative fulfils is given as <origin> when its asker is <asker> (r63; 2 examples)
- an initiative that fulfils no request is measured without saying internal or external (r64)

Plugin scripts: `/home/vscode/shopsystem-bdd/scripts` (`tools` run by that path). Coverage map: none (`tests-of`
answers "no map: make one with tools map"; `map` runs the whole suite, not run). Counts below say how made.
`tools refs` misses the extensionless `scripts/measure` and some `from X import` uses; those were found by text.

## 1. Why each scenario is red today

Command (run): `python3 -m pytest -q "<node id>"` for the three node ids of test_batch_measurement.py.

- r63 internal: `...test_the_request_an_initiative_fulfils_is_given_as_origin_when_its_asker_is_asker[this bounded context-internal]`
  -> StepDefinitionNotFoundError: Given "i7-cart fulfils the request q3, whose asker is this bounded context" (feature line 174).
- r63 external: same test, `[another bounded context-external]` -> the same error for "whose asker is another bounded context".
- r64: `...test_an_initiative_that_fulfils_no_request_is_measured_without_saying_internal_or_external`
  -> StepDefinitionNotFoundError: Given "i7-cart fulfils no request" (feature line 189).
- Read (grep of tests/scenarios, no run): the steps after the first undefined one are undefined too:
  - r63 Then "the measurement gives the request q3 as internal|external" (no step matches "gives the request").
  - r64 Then "the measurement gives the stage of cart-1's research" (line 192; the existing "the measurement gives the stage" has no "of").
  - r64 Then "the measurement gives no request as internal or external" (line 193).
  - "measure exits successfully" exists (batch_measurement_reading_steps.py:42); "it gives work-item ... a start and an end, run in the session" exists (given_steps:115).
- What is missing in code: `scripts/measure_build.py` `figures_of` (line 117) gives no request figure; nothing reads the
  initiative's fulfilled request or its asker (`scripts/measure_read.py`, no reader). Code already gives r64's
  measurement, because it ignores requests; the missing part is the steps and the r63 figure.
- What is missing in steps: the Givens that write the fulfilment and the request, the Thens above. World.flush
  (`tests/scenarios/batch_measurement_world.py:88`) writes no initiative.md and no requests dir.

## 2. What the system answers today

Probe file: `.shop/scratch/w133-1-research/probe_measure.py` (9 tests, each a fresh repository under the scratch
directory, `scripts/measure initiative i7-cart` as a subprocess, cwd the repository, CLAUDE_CONFIG_DIR in scratch).
Command (run): `python3 -m pytest -q -s -n 0 .shop/scratch/w133-1-research/probe_measure.py`. Result: 9 passed.
The probe's form of the link, `fulfils: request/ex.com/prod/ctx/q3` in initiative.md, and of the request file
(`asker:` in its frontmatter) is the probe's own guess (read: no spec line or code names the initiative's key, see 4/5).

Each probe's figure keys are `date, initiative, stages, totals, window, work_items`; no request key in any.

- A (scenario r63 Given+When, asker `internal`): exit 0, record written, no origin given. (run)
- B (scenario r63, asker `bounded-context/ex.com/prod/other`): exit 0, no origin given. (run)
- C (asker = this context's own id `bounded-context/ex.com/prod/ctx`): exit 0, no origin given. (run)
- D (scenario r64 setup: no initiative.md, no requests dir): exit 0, record with no request key. (run)
- E (nearest: fulfils q9, requests/q9.md absent): exit 0, measured silently, no origin, no refusal. (run)
- F (nearest: no log.jsonl, with fulfilment present): exit 1, stderr "the initiative i7-cart has no log.jsonl", nothing written. (run)
- G (nearest: no spec/index.md): exit 1, stderr "spec/index.md, which names the context, is missing", nothing written. (run)
  Note: the context id is read before writing, so the refusal writes nothing.
- H (nearest: second run): H2 without --replace exit 1 "exists; --replace writes over it"; H3 with --replace exit 0. (run)
- I (nearest: a log of one transition and no stage): exit 0, `stages: none`, totals of zero. (run)

## 3. Old assumptions

none. The requirement adds a figure and reads a link that no code writes or reads today. Searched: `tools refs`
on `measure_read.read_log`, `measure_build.figures_of`, `workqueue.context_path`, `workqueue_request._path`
(by tool, counts above); text search of scripts/ and tests/ for `fulfil`, `initiative.md`, `requests` (by search):
the only readers of an initiative's file are `scripts/model_work.py` (status, `source`) and `scripts/workqueue.py`
(by search); nothing reads a fulfilment. `work start` (r22, which would write it) has no subcommand in `scripts/work`
(by search). No test asserts the exact figure key set (by search, `figures()` uses named keys only).

## 4. Tests the requirements make impossible to keep

none. Tests-of: not run (no map). By search, the constraints the new read must keep:
- tests/scripts/test_measure_runs.py (two tests, `build()`): calls `measure_build.figures_of("i1", tmp_path)` with
  no initiative.md and no spec/index.md. Must keep passing: an absent initiative.md means no request, and
  `workqueue.context_path` must not be called on that path. Read.
- The other 28 tests of test_batch_measurement.py (31 collected, 3 accepted): their Givens write no initiative.md
  and no requests (by search of batch_measurement_given_steps.py). Same constraint. Read.
- Checked and sound: the 28 do not assert figure keys; their Thens read named keys only (by search).

## 5. A step the work-item skips

- The request is kept by `work`: `spec/capabilities/requests.md` (line 42-43) says the asker writes and reads it
  "through the upstream's `work`"; decision 0067 says each side uses only `work`. `measure` would read
  `.shop/work/requests/<q>.md` directly (read). The existing read, `scripts/workqueue_request.py` `_path` (line 17),
  refuses "there is no request <q> under .shop/work/requests" and `_field` (line 41) reads the frontmatter by regex.
  Effects only that step produces: that refusal, and the UTF-8 refusal of `workqueue.read` (read; not probed).
- The link is checked by nothing `measure` reads: that the fulfilled request is of this context and `accepted`
  (design note R4; grammar.md v16a-d; `model check`). A measurement of a request that is not accepted would be
  given (read; probe E shows the same for a missing file).

## 6. Defects

none. Probes A-I showed no crash and no refusal that should not be. E (a fulfilment whose request file is missing
is measured silently) is a gap of r63 not yet built, see questions.

## 7. The file set

Production:
- `scripts/measure_build.py` (139 lines; room 161): `figures_of` gives the origin figure, r63/r64. Read at 117-139.
- `scripts/measure_read.py` (182; room 118): a reader of the initiative's fulfilled request and its asker; absence
  means no request. Alternatively a new module such as `scripts/measure_request.py` (then a row in CLAUDE.md's
  module map, "a new concern gets a new module"). Read of measure_read.py 1-50 and 105-125.
- `scripts/measure` (93; room 207): CONTRACT text lists the figures; add the origin line (optional). Read whole.
- `scripts/measure_show.py` (110; room 190): not needed by the accepted scenarios; see question 5.
Read only (on the path, not edited): `scripts/measure_write.py` (41; `text_of` calls `workqueue.context_path`),
`scripts/workqueue.py` (262; room 38; `context_path`, `read`, `frontmatter` via `_load_model`), `scripts/model`
(137; the frontmatter parser). `scripts/workqueue_request.py` (114) is not on the path; its `_path` is the existing request read.

Tests:
- `tests/scenarios/batch_measurement_given_steps.py` (276; room 24): the Givens "fulfils the request q3, whose asker is <asker>"
  and "fulfils no request" do not fit in 24 lines; a new step module is the way.
- `tests/scenarios/batch_measurement_then_steps.py` (202; room 98): the Thens "the measurement gives the request q3 as
  internal|external", "gives no request as internal or external", "gives the stage of cart-1's research".
- `tests/scenarios/batch_measurement_world.py` (141; room 159): flush writes initiative.md and requests when the world holds them.
- `tests/scenarios/test_batch_measurement.py` (15; room 285): imports a new step module (star import, as the others).
- New `tests/scenarios/batch_measurement_request_steps.py` (proposed name): the Givens, and the Thens if they do not fit then_steps.
Not edited: `tests/scripts/test_measure_runs.py` (43; must keep passing, section 4); `features/` (not to be changed);
`spec/capabilities/batch-measurement.md` (r63, r64 already there).

Size: `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` printed nothing (run): no tracked Python over 300.

## Questions the plan must settle (both readings given, not chosen)

1. Asker vocabulary. "this bounded context" as the request's `asker`:
   A: `asker: internal` (requests.md line 45 lists `internal`); B: the context's own id `bounded-context/<owner>/<product>/<context>`
   (grammar.md line 112: internal(Q) :- asker(Q, X), upstream(Q, X)). The Given writes one; measure must accept which?
2. Product-level asker (`product`): not "this bounded context", so external by elimination (A), or refused (B). The
   feature gives two examples only.
3. A fulfilled request whose file is missing (probe E): A: refuse, naming the file (batch-measurement Purpose: "refuses
   rather than guesses"); B: give the measurement without the origin (r64 covers only "fulfils no request").
4. The key that links an initiative to its request. design-model.md (initiative table) and grammar.md name `fulfils`;
   no spec line or code writes or reads it, and `work start` (work-queue r22) is not built. The plan chooses the form.
5. `measure show` (r44: "print the measurement's figures as tables"): A: show prints the origin; B: show unchanged,
   r63 covers the record only.
