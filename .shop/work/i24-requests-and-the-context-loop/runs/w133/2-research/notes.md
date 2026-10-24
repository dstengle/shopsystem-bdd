# Research of w133 (stage 2): measure gives the origin of the initiative's request

Work-item w133 accepts batch-measurement#r63 and #r64. Accepted scenarios (features/batch-measurement.feature, not changed):
- the request an initiative fulfils is given as <origin> when its asker is <asker> (r63; 2 examples, lines 171-182)
- an initiative that fulfils no request is measured without saying internal or external (r64; lines 185-193)

Plugin scripts: `/home/vscode/shopsystem-bdd/scripts`. `tools map` was not made (refused: "no map"), so `tests-of`
and `untested` gave nothing. `tools refs` gave 0 references for `measure_build.figures_of` and
`measure_read.read_log`; it misses the extensionless `scripts/measure`, which calls `figures_of` (line 49). Counts
below say how made: `refs` (0 hits, not trusted), `by search` (grep), `run`, or `read`.

## 1. Why each scenario is red today

Command (run): `python3 -m pytest -q "tests/scenarios/test_batch_measurement.py::<node id>"`, one node id each.
- r63 internal: `...[this bounded context-internal]`. StepDefinitionNotFoundError: Given "i7-cart fulfils the request q3,
  whose asker is this bounded context" (feature line 174). (run)
- r63 external: `...[another bounded context-external]`. The same error for "whose asker is another bounded context". (run)
- r64: `test_an_initiative_that_fulfils_no_request_is_measured_without_saying_internal_or_external`. StepDefinitionNotFoundError:
  Given "i7-cart fulfils no request" (feature line 189). (run)
- Behind the first undefined step, read (no run reaches them): r63 Then "the measurement gives the request q3 as <origin>"
  matches no step (`batch_measurement_then_steps.py` has no "gives the request"). r64 Then "the measurement gives the stage
  of cart-1's research" (line 192) does not match "the measurement gives the stage" (then line 77, exact text).
  r64 Then "the measurement gives no request as internal or external" (line 193) matches no step.
  Existing and matching: "measure exits successfully" (batch_measurement_reading_steps.py:42, read in stage 1 by search);
  "it gives work-item ... a start and an end, run in the session" (given steps line 115, read).
- Missing in code: `scripts/measure_build.py` `figures_of` (lines 117-139) gives no request figure; `scripts/measure_read.py`
  has no reader of a request or of an initiative's link to one (by search: no `fulfil` in any script; read of
  measure_read.py 1-60). Today's code already gives r64's measurement, since it reads no request.
- Missing in steps: the two Givens (new module, see 7); the three Thens above; `World.flush` (`batch_measurement_world.py:88`,
  read by search) writes no request file and no initiative link. Its line 90 already writes spec/index.md with
  bounded-context/ex.com/prod/ctx, which `text_of` (measure_write.py:31) needs (grep, run).

## 2. What the system answers today

Probes (run): `python3 -m pytest -q -s -n 0 .shop/scratch/w133-2-research/probe_link.py` gives 6 passed. Each test: a fresh
repository under `.shop/scratch/w133-2-research/repos/`, spec/index.md with `bounded-context/ex.com/prod/ctx`, an initiative
i7-cart with a log.jsonl (one stage cart-1 research with start and end, transitions), then `scripts/measure initiative i7-cart`
(the worktree's own script, as a subprocess). The request file is `.shop/work/requests/q3.md`, frontmatter as
`spec/capabilities/requests.md` lines 44-46 gives it, with the link written on the request side (part_of or source).
- P1 asker `internal`, `part_of: i7-cart`: exit 0, record written, figure keys `date, initiative, stages, totals, window,
  work_items`; no request key; record does not contain "internal", "external" or "q3". (run)
- P2 asker `bounded-context/ex.com/prod/other`, `source: [i7-cart]`: exit 0, same keys, no origin. (run)
- P3 asker `product`, `part_of: i7-cart`: exit 0, same keys, no origin. (run)
- P4 no requests directory (r64 setup): exit 0, same keys. (run)
- P5 a request of the wrong form (no asker) with `part_of: i7-cart`: exit 0, silent; no refusal, no origin. (run)
- P6 q3 (internal, part_of) and q4 (other context, source) both naming i7-cart: exit 0, silent. (run)
- Stage 1's probes A-I (run in the stage-1 session, not rerun here) used `fulfils:` in initiative.md, a key no spec
  line or code names. That form is not supported by the spec (question 1). Its probe E (fulfilled request file
  missing: measured silently) and probe G (no spec/index.md: refused, nothing written) still stand as read here.

## 3. Old assumptions

none. The requirement adds a figure and reads a link no code writes or reads today. Searched: `tools refs` on
`measure_build.figures_of` and `measure_read.read_log` (0 hits, not trusted, see top); text search of `scripts/` for
`fulfil` (no hit in any script, only spec lines and docs), `initiative.md` and `requests` (readers: `scripts/model_work.py`
and `scripts/workqueue.py` and `scripts/model_requests.py`, which read requests and never a measurement). By search: no
test asserts the exact figure key set; `figures()` names its keys only.

## 4. Tests the requirements make impossible to keep

none. `tests-of` was not available (no map). By search and read:
- `tests/scripts/test_measure_runs.py` (43 lines, two tests) calls `measure_build.figures_of("i1", tmp_path)` with no
  initiative.md and no spec/index.md. It must keep passing: an absent link means no request, and `workqueue.context_path`
  must not be called on that path. Read: sound as it is, since nothing in the figures path reads a link today.
- The other 28 tests of `test_batch_measurement.py` (31 collected, 3 accepted). Their Givens write no initiative.md and no
  requests (read of `batch_measurement_given_steps.py` in full: no such write). They must keep passing. Sound.
- The 28 do not assert figure keys; their Thens read named keys only (by search). Sound.

## 5. A step the work-item skips

- The request is kept by `work`: `spec/capabilities/requests.md` lines 42-43 say the asker writes and reads it through
  `work`; decision 0067 says each side uses only `work`. A measurement that reads `.shop/work/requests/<q>.md` directly
  skips it (read). The existing read, `scripts/workqueue_request.py` `_path` (line 17, read in stage 1), refuses "there is no
  request <q> under .shop/work/requests"; `_field` (line 41) reads the frontmatter by regex. Effects only that path gives:
  that refusal, and the UTF-8 refusal of `workqueue.read` (read; not probed).
- Form: `scripts/model_requests.py` lines 28-48 (read) refuses a request not of the form `work request` writes (no asker,
  no status, neither part_of nor source, turn not asker or upstream, a section other than Lines/Outcomes/Questions/
  Answers/Resolution); the model reports it as a problem. measure does none of this: P5 shows the silent pass (run).
- Status: `model check` (v_d1, r114) relies on the request's `asker` and `status`; the link is checked by nothing `measure`
  reads: that the request is of this context and `accepted`. A measurement of a request not accepted would give its origin
  (read; P1 used `accepted` only, no probe of `open`).

## 6. Defects

none. P1-P6 show no crash and no refusal that should not be. The gaps P5 and P6 (a wrong-form request and two requests
naming one initiative are passed silently) are a not-yet-built r63 path, not a defect of today's code, since no link is
read today.

## 7. The file set

Production:
- `scripts/measure_build.py` (139 lines; room 161): `figures_of` gives the request origin figure (r63, r64). Read whole.
- `scripts/measure_read.py` (182; room 118): the reader of the initiative's link and the request's asker, or a new module
  such as `scripts/measure_request.py`, which would need a row in CLAUDE.md's module map ("a new concern gets a new module").
  Read 1-60 (run in stage 1 for 105-125). Measure's docstrings say "standard library only": the reader cannot import
  `model_requests.py`, which imports `model_work` and `model_parse` (read).
- `scripts/measure` (92; room 208): CONTRACT text lists the figures; the origin line is optional. Read whole.
- `scripts/measure_show.py` (110; room 190): not needed by the accepted scenarios; question 6 (show prints the origin?).
- `scripts/measure_write.py` (41; room 259): not edited; `text_of` already reads the context id (line 31, read).
Read on the path, not edited:
- `scripts/workqueue.py` (272; room 28, not 38 as stage 1 wrote): `context_path` lines 36-45 (read). A change here is tight.
- `scripts/workqueue_request.py` (114; room 186): `_path` and `_field`, the existing request reader (read in stage 1).

Tests:
- `tests/scenarios/batch_measurement_given_steps.py` (276; room 24): the two Givens do not fit; they go in a new module.
- `tests/scenarios/batch_measurement_then_steps.py` (202; room 98): the Thens "gives the request q3 as internal|external",
  "gives no request as internal or external", "gives the stage of cart-1's research" (or the last one reused).
- `tests/scenarios/batch_measurement_world.py` (141; room 159): `flush` (line 88) writes the request file and the initiative
  link when the world holds them; spec/index.md is already written (line 90).
- `tests/scenarios/test_batch_measurement.py` (15; room 285): imports the new step module (star import, as the others).
- New `tests/scenarios/batch_measurement_request_steps.py` (proposed name): the two Givens.
- Not edited: `tests/scripts/test_measure_runs.py` (43; must keep passing, section 4); `features/` (fixed).
- `spec/capabilities/batch-measurement.md`: r63 and r64 are there; the Implementation section names no link key, so a key
  is a spec choice for the plan (question 1), not this work's edit.

Size: `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` (run) printed nothing: no tracked Python over 300.
Line counts (`wc -l`, run): listed above. `git status --porcelain` (run) is empty: the scratch directory is ignored.

## Questions the plan must settle (both readings given, not chosen)

1. Which side holds the link. (A) The request names the initiative in `part_of` or `source`: `work-queue.md` line 54
   (r23 note), `design-model-check.md` r114 and its feature examples (`source` or `part_of` names i1), `model_requests.py`
   line 38. (B) The initiative names the request: `work-queue.md` r22 says initiative.md is written "that fulfils the request"
   with the request's origins as `source`, but names no field for the request. Conflict: `requests.md` lines 44-46 type `source`
   as origins and `part_of` as a job-thread; under (A) a request's `part_of` names an initiative. Stage 1's `fulfils:` key in
   initiative.md is reading (B) with a key no spec line gives.
2. The asker's vocabulary. (A) `internal` for this context, from `requests.md` line 45. (B) this context's own id,
   `bounded-context/<owner>/<product>/<context>` (`workqueue.context_path`, `model_facts.py` 121-134). The product level's value
   is not given by any spec line, so an asker `product` (P3) is external by elimination or refused: two readings; the feature
   gives two examples only.
3. Who reads the request: a new reader in measure (stdlib only), or the model's reader (`model_requests.py`, which imports
   the model). Both readings are open.
4. A request that names the initiative but is of the wrong form, or whose file is missing (P5; stage 1 probe E). (A) refuse,
   naming the file ("refuses rather than guesses", batch-measurement Purpose). (B) give the measurement without the origin;
   r64 covers only "fulfils no request".
5. Two requests naming one initiative (P6). The spec gives no reading: refuse, or give both, or the first.
6. `measure show` (r44: "print the measurement's figures as tables"): (A) it prints the origin; (B) unchanged, r63 covers the
   record only (stage 1's question 5).
