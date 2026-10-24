# w126 research notes

Work-item: `.shop/work/i24-requests-and-the-context-loop/w126.md`, under `requests`, accepts r1-r5.
Tools: plugin's `scripts/tools` runs `refs`, `size`. `tools tests-of` and `untested`: **no map** (`tools: no map`), so every test list is `by search`. I did not run `tools map`.
Probe file: `.shop/scratch/w126-1-research/probe_requests.py`. Run: `python3 -m pytest -q -s -n 0 --work-item= ...`.
Note: my pytest environment sets `--work-item w126` (source not identified, not read). With that value every run stops at collection (D2). `--work-item=` lets collection run.

## 1. Why each accepted scenario is red today

Command: `python3 -m pytest -q --work-item= -k requests --collect-only` → `3/816 tests collected`; none from `features/requests.feature` (the 3 are batch-measurement and design-model-check tests with "request" in their names). Run: `python3 -m pytest -q --collect-only` with `--work-item w126` set → INTERNALERROR `w126 accepts none of the scenarios it collected` (run).

Shared causes (read + run):
- No binding: no `tests/scenarios/test_requests.py` (`scenarios("requests.feature")` absent); no `requests_steps` module (Glob `tests/**/*request*`: no files).
- No commands: `scripts/work` has no `request`, `outcome`, `turn` or `resolve` (probe `test_request_commands_absent`: each → exit 2, `invalid choice`). Subparsers `scripts/work:64-86`, dispatch `scripts/work:89-90`.
- No library: no module in `scripts/` writes a request (grep `request|outcome|resolve` in `scripts/`: only measure, model, supervise hits).

Per scenario:
- r1 outline (`request with <given> ...`, two rows): the same causes. `work request` has no `--source`, `--thread`, `--from` or `--lines` options. Upstream write path undefined (question 3).
- r2 outline (five faults): the same causes. The strict-form check exists for capability lines only: `model_parse.ears` (`scripts/model_parse.py:216`), called from `model_facts.py:216-220`. Not called for a lines file.
- r3 (neither `--source` nor `--thread`): the same causes; the refusal is not coded.
- r4 (`outcome` leaves lines as written): needs `work outcome` (r15, not accepted by this work-item) and a request fixture with two lines. Red for the same causes.
- r5 (`turn` leaves outcomes, writes no resolution): needs `work turn` (r7, not accepted) and a request fixture. Red for the same causes.

## 2. What the system answers today (probes)

Run (`probe_request_commands_absent`): `work request|outcome|turn|resolve` → exit 2, `invalid choice`.

Run (`probe_request_file_present_to_work_and_model`): a `kind: request` file at `.shop/work/requests/q1.md` in a scratch repo, git initialised.
- `work show` → exit 0, prints nothing (the request is not a work-item).
- `work status` → exit 0: `initiative i1 started`, `uncommitted: none`, `untracked: .shop/work/requests/q1.md`.
- `work add i1 "After request" ...` → exit 0, `w1` (numbering ignores the request, `workqueue.highest`).
- `model --root <repo> check` → exit 1: `file: .shop/work/requests: no initiative.md`, plus w1 problems the empty repo causes. Defect D1.
- `model check --root <repo>` → exit 2 (argument order is `model --root X check`; not a finding).

Run (`probe_add_refusals_of_the_existing_way`): nearest cases of the existing write path.
- `work add i1 "bad\ntitle" ...` → exit 1 `the title has a newline in it`; nothing written.
- `work add i1 "" ...` → exit 1 `the title is empty`; nothing written.
- `work add i1 t --under "a\nb" ...` → exit 1 `the value of --under has a newline in it`; nothing written.
- Initiative dir after these: `['initiative.md']`.
- No-git case: the scratch directory sits inside the worktree's own git repository, so `git rev-parse` passed; `git add` refused the ignored path (`git add failed: The following paths are ignored`), and `w1.md` was removed again (`committed()` rollback). This is a probe artifact for "not a repository": the non-git refusal is `read` only.

Run (`probe_ears_of_the_five_faults_and_a_good_line`): `model_parse.ears` on lines.
- `The queue shall show each item.` → (True, True).
- `While idle, when a request arrives, the system shall answer it.` → (True, True).
- `Show the queue to the caller.` (none of EARS's patterns) → (False, True): v_e1.
- `When a request arrives, while idle, the system shall answer it.` (When before While) → (False, True): v_e1.
- `If a request arrives the system shall answer it.` (If with no then) → (False, True): v_e1.
- `When ..., the system shall answer and the system shall log it.` (two shalls) → (True, False): v_e2.
- `The system shall answer. The system shall log it.` (two sentences; this probe line also has two shalls) → (True, False): v_e2.
- Two sentences with one shall: `read` only. `ears` splits sentences on `[.!?](?=\s+\S)` (`model_parse.py:227-228`), so it should give (True, False).
- The clingo route: `model check` ran, so the solver is present in this interpreter. `model_check.solve` needs clingo; without it `needing_clingo` exits 2 (`model_check.py:79-91`, `read`).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/model_work.py:read_work` (91-125) | treats every directory under `.shop/work/` as an initiative and needs its `initiative.md`; `.shop/work/requests/` gets `no initiative.md` | requests are kept in `.shop/work/requests/q<n>.md` (capability Implementation, design-model-check r19): the dir must be skipped or read as requests | by search: `tests/scenarios/test_design_model_check.py` (its request scenarios already red, part 4) | probe run; read |
| `scripts/model_work.py:PART_KINDS`, `read_part` (16-17, 127-) | the model's request kind is `cross-context-request` (model.lp v7, v_b2, v_b3, w_many_requests); `kind: request` is not a part kind | the capability's form is `kind: request` with `asker`, `source`, `status`, `turn` | by search: `tests/scripts/test_migrate_layout.py`, `tests/scenarios/migration_spec_steps.py`, `tests/scenarios/test_migration_tools.py` name the old kind; they assert migration, not model reading | read (model_work.py, model.lp:111-114, 211-214, 285-286) |
| `scripts/workqueue.py:items` (100-105) | globs `*/*.md`, yields `kind: work-item` only | a request at `requests/q1.md` matches the glob and is skipped by kind; no change needed | `tools refs`: 2 production refs (`supervise.py:61`, `supervise_pool.py:62`), 0 test refs; by search: `tests/scripts/test_work_*.py`, `tests/scenarios/work_queue_*_steps.py`; none writes a requests dir | `tools refs`; probe (work show, work add) |
| `scripts/workqueue.py:highest` (62-71) | same glob, kind check | a request file does not raise the work-item number | by search: as above | probe (work add → w1) |
| `scripts/workqueue_status.py` (113-137) | globs `*/initiative.md` | the requests dir has no initiative.md and is skipped; r14 not accepted | by search: `tests/scenarios/work_queue_status_steps.py`, `tests/scenarios/test_work_queue.py` | probe (work status lists the q1 file as untracked only) |
| `scripts/workqueue.py:committed` (236-251) | makes a change, `git add` and `git commit` of only those files, rolls back on failure | r1-r5 do not require it (r12 commit is not accepted); a request write that skips it commits nothing | `tools refs`: 3 refs (`workqueue.py:96,196,222`), 0 test refs; by search: `tests/scripts/test_work_*.py` | `tools refs`; probe (no-git rollback) |
| `scripts/work:main` dispatch and subparsers (64-93) | eight commands (add, show, withdraw, run, retry, answer, note, status); an unknown one → argparse exit 2 | four subcommands are added to the dispatch dict and the subparsers | by search: `tests/scripts/test_work_*.py`, `tests/scenarios/test_work_queue.py`; grep `choose from`, `usage: work` in tests: no hits | read; probe (exit 2 for `request`) |
| `scripts/model_parse.py:ears` (216-260) | strict-form check for capability Behaviour lines, called from `model_facts.py:216-220` | r2 reuses it for `lines.md` lines (or solves model.lp v_e1/v_e2 via clingo); the function itself unchanged | by search: `tests/scripts/test_model*.py` (test_model_reading among them); not read | read; probe |
| `scripts/model.lp` v_e1, v_e2 (269-272) | flags Behaviour lines in the solver only | r2 says "holds (v_e1, v_e2)": either the solver (needs clingo, `model_check.needing_clingo`) or `ears` | by search: model tests; not read | read |

## 4. Tests the requirements make impossible to keep

No map, so by search.
- Grepped the tests for `.shop/work/requests`, `requests/`, `cross-context-request`: hits only in the migration tests (`tests/scripts/test_migrate_layout.py`, `tests/scenarios/migration_spec_steps.py`, `tests/scenarios/test_migration_tools.py`). Named, not read in full; they assert migration of old paths. None breaks by the change, as far as searched. Not run.
- Grepped for tests asserting the `work` usage or the unknown-command text: none.
- Tests that write `.shop/work/` (`tests/scripts/test_model*.py`, `test_work_*.py`, `test_migrate_upgrade*.py`) were named by grep, not read; none is known to create a directory there without `initiative.md`. Not verified.
- Already red, not made impossible: `python3 -m pytest -q --work-item= tests/scenarios/test_design_model_check.py -k "request or asker or q1"` → 13 failed, 32 warnings (run). Includes v_d1 (4 of 5 rows), v_d3, v17, v3, v16a, v18 (2 rows), "a request not of the form `work request` writes is a file problem" (r112), and "model reads the repository's files under its root [.shop/work/requests/q1.md]". These belong to design-model-check; this work-item neither fixes nor breaks them.
- `tests/scenarios/test_work_queue.py` (286 lines) is not changed by r1-r5; its tests are sound for the change by search, not run.

## 5. A step the work-item skips

Existing way: `work add` (`workqueue.add`). Its effects that only that path produces (each as probed, or `read`):
- Refusal, empty title (run: exit 1, no write).
- Refusal, newline in title (run: exit 1, no write).
- Refusal, newline in `--under` (run); `--part-of` and `--accepts` `read`, same loop at `workqueue.py:81-83`.
- Refusal, initiative name with `/`, `\`, `.` or `..` (`entry`, 56-59, `read`).
- Refusal, initiative directory missing (`add`, 85-86, `read`).
- Refusal, not a git work tree (`committed` → `git rev-parse`, `read`; not reproduced, part 2).
- Refusal, git add or commit fails, files restored (run: `no git, add` → `ls` shows only `initiative.md`).
Request writes (r1) inherit none of these unless written with the same steps. r1-r3 check only the lines (r2) and the origin options (r3). The title and the values of `--from`, `--source`, `--thread` have no newline or empty check in r1-r3 (`read`, not probed). Whether r1 commits is a conflict (r12 not accepted; question 2).

## 6. Defects

### D1: `model check` reports a file problem for the requests directory
Reproduction (run): scratch repo with `spec/index.md`, `.shop/work/i1/initiative.md`, `.shop/work/requests/q1.md` (`kind: request`, `asker: ctx-a`, `source: [o1]`, `status: open`, `turn: upstream`).
`python3 scripts/model --root <repo> check` → exit 1 with `file: .shop/work/requests: no initiative.md`.
Expected by design-model-check r19, which reads `.shop/work/requests/*.md`: no problem for a request in that form. Cause: `model_work.py:read_work` (lines 91-96) takes the requests dir as an initiative. Not fixed.

### D2: `--work-item` aborts the whole collection
Reproduction (run): `python3 -m pytest -q --collect-only` with `--work-item w126` set in the environment → `INTERNALERROR ... SystemExit: --work-item w126: w126 accepts none of the scenarios it collected`; 60 INTERNALERROR lines; `tests/scenarios/test_work_queue.py` alone the same. Source of the option not identified. With `--work-item=` collection runs (part 1). Reported as observed; not judged.

## 7. The file set

Production:
- `scripts/work` — add `request`, `outcome`, `turn`, `resolve` to the subparsers (64-86) and dispatch (89-90). Found by read and probe.
- `scripts/workqueue_request.py` (new) — the request library: write `.shop/work/requests/q<n>.md`, check lines with `model_parse.ears`, refuse with `workqueue.Refused`. A new concern: a module-map row in `CLAUDE.md`.

Tests:
- `tests/scenarios/test_requests.py` (new) — `scenarios("requests.feature")`.
- `tests/scenarios/requests_steps.py` (new) — the Givens, Whens, Thens of the five scenarios.

Not changed by r1-r5 (read, verified): `scripts/workqueue.py` (262 lines; `Refused`, `frontmatter`, `read`, `entry`, `committed` reused), `scripts/model_parse.py` (`ears` reused), `scripts/model_work.py` (D1 lives here, not this work-item's), `scripts/model_facts.py`, `scripts/model_check.py`, `scripts/workqueue_status.py`, `tests/scenarios/test_work_queue.py`. `features/requests.feature` needs no change for the five.

Modules on the change's path, lines and room under the 300 limit (CLAUDE.md):
- `scripts/work` 97 (room 203) — edited.
- `scripts/workqueue.py` 262 (room 38) — reused.
- `scripts/model_parse.py` 271 (room 29) — reused.
- `scripts/model_facts.py` 275 (room 25) — calls `ears`.
- `scripts/model_work.py` 213 (room 87) — D1 site.
- `scripts/model_check.py` 139 (room 161) — solver route.
- `scripts/workqueue_status.py` 147 (room 153) — globs initiatives.
- new `scripts/workqueue_request.py` and the two new test modules start at 0.

## Questions for the planner (both readings given)

1. r4 and r5 scenarios use `work outcome` (r15) and `work turn` (r7), neither accepted. Accept them, or leave the scenarios red?
2. r12 (commit) is not accepted, but the existing write path commits (`committed`). Does r1 commit the request? Reading A: yes, via `committed`, which needs a git repository. Reading B: no commit, r12 later.
3. Where `work request` writes: the scenarios name no upstream option, and the capability says the asker writes the upstream's `.shop/work/requests/` through the upstream's `work`. Which root does `work request` use?
4. Form of `lines.md`: the capability does not give it; scenarios say "two lines in strict EARS". One line each, or bullets with `[r<n>]`?
5. r2 check: `model_parse.ears` (no clingo) or model.lp v_e1/v_e2 (clingo, `needing_clingo`)?
6. D1 and design-model-check's red request scenarios: outside w126 unless the plan has `model` read requests.
