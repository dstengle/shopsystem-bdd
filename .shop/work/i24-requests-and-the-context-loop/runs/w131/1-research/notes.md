# w131 research: model reads requests; an initiative of kind job is a file problem

Accepted: design-model-check#r19, #r112, #r118. Retired: the deprecated r19 outline.
Search: no `tools map` exists, so `tests-of` and `untested` cannot answer; every test count below is `by search`.
`tools refs` used for names. Probes: `.shop/scratch/w131-1-research/probe_w131*.py`, run `-n 0`.

## 1. Why each scenario is red today

- **r19, "model reads the repository's files under its root"** (outline, 14 rows)
  `python3 -m pytest -q "tests/scenarios/test_design_model_check.py::test_model_reads_the_repositorys_files_under_its_root"`
  Run: 1 failed, 13 passed. Failing row `.shop/work/requests/q1.md ... include`: `KeyError` at
  `tests/scenarios/design_model_check_reading.py:118` (`_files_read()` has no entry for that path).
  Missing in the step data: that row and a marker fact for a request. Missing in code: `scripts/model_facts.py`
  `Model.read()` (99-109) has no request reader; `scripts/model_work.py:93` globs `.shop/work/*` so `requests/`
  is taken for an initiative folder (see 6). `model facts` prints no request line (probe 1, run).

- **r112, "a request not of the form `work request` writes is a file problem"**
  Run: `... ::test_a_request_not_of_the_form_work_request_writes_is_a_file_problem`. Failed:
  `StepDefinitionNotFoundError: Given "a request in .shop/work/requests/q1.md with no asker"` (feature line 905).
  No step module has "a request in ..." nor "that `work request` wrote". Code: no request reader; the only
  file problem today is `file: .shop/work/requests: no initiative.md`, which names no q1.md, so the Then at 908
  would fail as well (probe 1, run). `work request` is not implemented (`grep request scripts/work` finds nothing),
  so the fixture for "wrote" must be built from `spec/capabilities/requests.md` Implementation (read).

- **r118, "an initiative of kind job or job-path is a file problem"** (3 rows)
  Run: `... ::test_an_initiative_of_kind_job_or_jobpath_is_a_file_problem`. All three fail with
  `StepDefinitionNotFoundError: Given "a repository with an initiative in .shop/work/i1/initiative.md of kind <kind>"`.
  The step is missing; `tests/scenarios/conftest.py:130` `World.initiative(kind=...)` already takes the kind.
  Code: `scripts/model_work.py:106-107` writes an `ikind` fact and nothing else; no file problem for job/job-path.
  The capability-change row expects no print, which today's code gives (probe 2, run).

- **r19 deprecated outline** `test_model_reads_the_repositorys_files_under_its_root_deprecated`: 14 passed (run,
  in the same run as above). It is retired by the Retires section, not red.

## 2. What the system answers today

Probe 1 (`probe_w131.py`, run `python3 -m pytest -q -s -n 0 .shop/scratch/w131-1-research/probe_w131.py`):
- r19 Given+When: request `q1.md` (kind request, id `request/<path>/q1`) under `.shop/work/requests/`, `model facts`
  exit 0, no line containing `request`. Expected by the outline: "include" fails.
- r112 Given: `q1.md` with no asker, `q2.md` in full form. `model check` exit 1:
  `file: .shop/work/requests: no initiative.md`, `0 violations ... 1 file problems`. No line names `q1.md`; `q2.md`
  is not named either (so "no file problem naming q2" holds only by accident).
- r118 Given: initiative `i1` of kind `job` / `job-path` / `capability-change` (no parts): `model check` prints no
  file problem for any of them. (Lines `v10a` and `unresolved` in the job runs come from my probe lacking an
  observation, not from the kind.)

Probe 2 (`probe_w131b.py`, run):
- Nearest, empty data: `.shop/work/requests/` with no file. `model check` exit 1, `file: .shop/work/requests: no initiative.md`.
- Nearest, kind `job` with a `job-proposal` part (`part_of` the initiative): exit 0, no file problem. The r118
  case with a part that the kind's rule accepts.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/model_work.py:93 `read_work` (glob `.shop/work/*` dirs) | takes `requests/` as an initiative folder: file problem `no initiative.md` | skip `requests/`; read `requests/*.md` as requests (r19, r112) | by search: the model suites run it on every initiative; none makes a `requests/` dir (grep `requests` in tests: migrate only) | read; probe 1, 2 |
| scripts/model_work.py:106-107 `read_work` (`ikind` fact) | accepts any kind, job and job-path included | job, job-path: file problem naming initiative.md (r118) | by search: none (no test uses kind job or job-path; `kind=` in tests is capability-change or defect) | read; grep `job` in tests |
| scripts/model.lp:191-193 (`v_k1`, `v_k2`) | first-part rules for ikind job and job-path | unreachable as a clean result: facts still produce them. grammar.md:202 says v_k1/v_k2 "are gone in v4" | none (grep `v_k1`, `v_k2` in tests and features: no match) | read; grep |
| scripts/model_facts.py:23-26 `KINDS` (used at 67-81 `qualify`) | no `request` kind; `request/<path>/q<n>` ids are not read as a kind | `request` becomes a node kind for `request/<context path>/q<n>` ids (requests.md Implementation) | by search: none passes a `request/` id to `qualify` | `tools refs KINDS`: 2 prod refs (measure_build has its own KINDS) |
| scripts/model_facts.py:99-109 `Model.read` | no request read step | a request read step is added | by search: every model test runs `read` | read |
| scripts/model (header 35-38) | says "It reads no other layout" | requests are read: text is wrong after the change | none (docstring) | read |
| scripts/workqueue.py:63-72 `highest`, 101-106 `items` (glob `*/*.md`, filter kind work-item) | request files are read and skipped by kind | none for r19/r112; `kind` filter already excludes requests | by search: none makes a `requests/` dir | read |
| scripts/workqueue.py:207-211 `find` (glob `*/<name>.md`) | a name `q1` finds `requests/q1.md` | none for these scenarios; the requests capability's `work turn q1` will meet it (other work-item) | by search: none | read |
| scripts/workqueue_status.py:113-115 `open_names` (glob `*/initiative.md`) | ignores `requests/` (no initiative.md) | none | by search: none | read |
| scripts/migrate_upgrade_ids.py:36 (`iterdir` dirs matching `i\d+`) | ignores `requests/` | none | by search: migrate tests only | read |

## 4. Tests the requirements make impossible to keep

`tools tests-of` unavailable (no map). By search (grep of `tests/` and `features/` for `requests`, `job`, `ikind`,
`v_k1`, `initiative.md`):
- `tests/scenarios/test_design_model_check.py::test_model_reads_the_repositorys_files_under_its_root_deprecated`
  (14 cases): passes today (run). Retired: remove with the scenario in `features/design-model-check.feature:126-149`.
  Nothing else in them can break.
- No other test asserts the old behaviour: no test has a `requests/` directory; no test uses an initiative of kind
  job or job-path; `tests/scenarios/design_model_check_problems.py:84` "there is no initiative.md" is about `i1`,
  not `requests/`. `tests/scripts/test_model_output.py:19` counts file problems on a fixture with no requests dir.
- Verified sound: `tests/scripts/test_model_reading.py` (no job or requests), `tests/scripts/test_model.py`
  (`initiative(kind="defect")`).

## 5. A step the work-item skips

A request reader that does not go through the part reading's steps (`read_part` in `scripts/model_work.py:127-137`
runs `check_id`, `node`, `status`, `unread`). Each effect shown by the existing way (probe 3, run:
`python3 -m pytest -q -s -n 0 .shop/scratch/w131-1-research/probe_w131c.py`):
- `status()`: part with `status: built` on a capability-proposal -> `file: .shop/work/i1/p1.md: status 'built' is not one of approved, drafted, formulated, merged, withdrawn`.
- `check_id()`: part id `capability-proposal/other/p1` -> `file: ... id 'capability-proposal/other/p1' is not capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/<name>`.
- `unread()`: folded `title: >-` -> `file: ... title uses a folded or literal block, which is not read; write it on one line`.
A request reader that skips these would let a request with a bad status, id or folded block pass without a file problem.
(Status list for `request` does not exist in `STATUSES` today: the plan must add one or accept any status: read.)

## 6. Defects

### D1. An empty `requests/` directory is refused
Reproduction (probe 2, run): repo with `spec/index.md`, `spec/capabilities/thing.md` (group guarantees), and an
empty `.shop/work/requests/`. `scripts/model --root <repo> check` -> exit 1,
`file: .shop/work/requests: no initiative.md`, `0 violations, 0 warnings, 0 unresolved references, 1 file problems`.
The spec's layout (requests.md Implementation; design-model-check r19) makes that directory legitimate.

## 7. The file set

Production (changed by the scenarios' passing):
- `scripts/model_work.py` (213 lines, room 87): `read_work` skips `requests/`; job/job-path kinds add a file problem at ikind (r118).
- `scripts/model_facts.py` (275, room 25): `KINDS` gains `request`; `Model.read()` calls the request reader (r19, r112). Room is tight: the reader belongs in a new module.
- `scripts/model_requests.py` (new; the reader of `.shop/work/requests/*.md`: id, `asker` present (r112), node fact, `status`, `unread`): a new concern, so a row in CLAUDE.md's module map.
- `CLAUDE.md` (module map row for `model_requests.py`).
- `scripts/model` (137, room 163): the header text at lines 35-38.
- `scripts/model.lp` (304; not Python, not counted by `tools size`): `v_k1`, `v_k2` (191-193) may be removed as grammar.md:202 says, or kept: plan's choice.

Tests and features:
- `tests/scenarios/design_model_check_reading.py` (216, room 84): add the `.shop/work/requests/q1.md` row and its marker to `_files_read()` (98-113).
- `tests/scenarios/design_model_check_requests.py` (new, under 300): the Givens "a request in ... with no asker", "... that `work request` wrote", "a repository with an initiative ... of kind <kind>".
  `tests/scenarios/design_model_check_problems.py` is 300 lines (room 0): the steps must not go there.
- `tests/scenarios/test_design_model_check.py` (53, room 247): import the new step module.
- `features/design-model-check.feature`: remove the deprecated r19 outline (126-149) per Retires.

On the change's path, not edited: `scripts/model_check.py` (139, room 161; calls `Model(...).read()` and solves), `scripts/model_parse.py` (271, room 29; `frontmatter`, `as_list`, `scalar` used by the reader; `expand` is used by `read_part`). `tools size --limit 300` printed nothing: no tracked Python file is over the limit.

## Questions for the plan (both readings given, not decided)

- r112's form. `spec/capabilities/requests.md` Implementation says the file's form is `work`'s own and "may change";
  r112 pins it. Reading A: a request is of the form when it has the frontmatter the Implementation section lists
  (id, kind, asker, part_of or source, status, turn) and the sections. Reading B: the form is only the asker (the
  scenario's case). The scenario pins only "no asker" as red.
- r19's marker. The outline's "include" needs a fact a request produces. Reading A: `node("request/<path>/q1", "request")`
  (needs `request` in `KINDS`). Reading B: `asker(...)` fact or the `kind` read. Either way the step data needs the row.
- v_k1, v_k2: keep (facts still emitted, no test) or remove (grammar v4). The Retires section does not say.
