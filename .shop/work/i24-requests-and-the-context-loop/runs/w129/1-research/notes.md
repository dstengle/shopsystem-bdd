# Research of w129: work show prints requests; work status prints uncited observations

Method: no `tools map` exists, so every count below is `by search`. `tools refs` was run on some names but missed `open_text`/`open_names` (0 refs, yet migrate_session.py calls them). Probes are in `.shop/scratch/w129-1-research/`.

Accepted: requests#r13 (`show`), requests#r14 (`status` with no initiative).

## 1. Why each scenario is red today

Command: `python3 -m pytest -q -n 0 -k "show_prints_each_request or status_with_no_initiative_prints" .shop/scratch/w129-1-research/probe_bind_requests.py` (a scratch file binding features/requests.feature via `scenarios(...)`; no test in `tests/` binds requests.feature, so no node id exists to run).

- "show prints each request with its status and whose turn it is" (requests.feature:148): FAILED, `StepDefinitionNotFoundError` on the first Given, `a request q1 from the asker ctx-a whose status is open and whose turn is the upstream's`. No step module for requests exists (`tests/scenarios/` has no requests_* file, no `test_requests.py`).
- "status with no initiative prints, with its date, each observation ..." (requests.feature:157): FAILED, `StepDefinitionNotFoundError` on `observations o1, o2 and o3, each with its date`.
- Missing in code, by file and function:
  - `scripts/workqueue.py:items()` (lines 100-105) yields only `kind: work-item` files; it does not read request files under `.shop/work/requests/`.
  - `scripts/work:cmd_show` (27-34) prints `items()` only, no request lines.
  - `scripts/workqueue_status.py:status()` (128-147) and `render()` (96-109) read only initiative dirs and print initiatives; no observation reader. `parts()` (38-48) filters to capability-proposal and work-item kinds.
  - No reader of `.shop/records/observations.md` in `scripts/workqueue*.py`; `scripts/model_work.py:read_records()` (49-63) reads the `about:` lines only, not dates.

Result of the scratch probe, `pytest -p no:work_items` is refused because the environment's `--work-item w129` plus `scripts/work_items.py:94-111` raises SystemExit when none of w129's scenarios are collected. Existing tests were run with `--whole-suite`, which the plugin accepts.

## 2. What the system answers today

Probe file `probe_requests_show_status.py`, run as `python3 -m pytest -q -s -n 0 .shop/scratch/w129-1-research/probe_requests_show_status.py`. Each repo is built under the scratch dir with `spec/index.md`, `.shop/records/observations.md` (o1, o2, o3 with dates) and `.shop/work/requests/q<n>.md` files (kind: request, asker, source, status, turn).

- P1 `work show` with q1 (open, upstream's turn), q2 (awaiting-asker, asker's turn), and work-item w1 drafted: run. Output `i1/w1 drafted`, exit 0. No request line.
- P2 `work status` with i1 (status started, source o1), q1 (source o2): run. Output is the i1 block only (`initiative i1 started`, branch, uncommitted, untracked, ledger, last next). No observation line; o3 is not printed. Exit 0.
- P3 `work status` with observations only, no initiatives: run. Empty output, exit 0.
- P4 `work status` with a request only: run. Empty output, exit 0.
- P6 `work show` with `.shop/work/requests/q9.md` holding non-UTF-8 bytes: run. `STDERR: work: .shop/work/requests/q9.md is not UTF-8 text`, exit 1. `work status` on the same repo exits 0 (status ignores requests).
- P7 `work show` with `requests/q3.md` whose frontmatter has no closing `---`: run. Empty output, exit 0 (frontmatter returns {} and the file is skipped silently).
- P8 `model check` with a `.shop/work/requests/` directory: run. Exit 1, with `file: .shop/work/requests: no initiative.md` (from `model_work.py:read_work`, lines 91-97) and `warning w_uncited_obs ... (2)`. The count includes o2, which request q1 cites: the model reads only initiative `source` lines (`model_work.py:113-116`), not request `source`. The unresolved line about `capability/.../requests` is an artifact of the scratch repo, which has no capability.
- Nearest cases not probed (read): `scripts/work_items.py:acceptors()` (line 62) reads `*/*.md` with `path.read_text()` and no UTF-8 handling, so a non-UTF-8 request file would raise inside the pytest plugin (read).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue_status.py:status (None branch) and open_text (120-125) | `work status` with no initiative prints each open initiative's r16 block (work-queue r17) | requests r14 says it prints observations nothing names. Reading A: additive, keeps the initiative blocks. Reading B: replaces them. Only B breaks work-queue r17 | test_work_queue.py::test_status_with_no_initiative_prints_each_initiative_that_is_neither_done_nor_abandoned (run, passes) | search (refs misses it) |
| scripts/migrate_session.py:open_text / open_names (lines 20, 25, 30) | SessionStart hook text is `work status` output for each open initiative | r14 changes that output; under reading A the hook would also carry observation lines, which migration-tools r32 does not ask for. Conflict to decide | test_migration_tools.py::test_a_session_starting_in_a_repository_with_initiatives_neither_done_nor_abandoned_is_given_what_work_status_prints_for_each_of_them (run, passes); migration_session_steps.py:85-95 | search |
| scripts/workqueue.py:items (100-105) and scripts/work:cmd_show (27-34) | `work show` prints work-items only; `--json` prints `{"work-items": ...}` | r13 adds request lines to the text output. JSON must not change (work-queue r11) | test_work_queue.py::test_show_prints_each_workitem_of_every_initiative_with_its_status (run, passes); test_show_with_json... (read) | search |
| scripts/workqueue.py:items and highest (62-71) | glob `*/*.md` and read every file | `.shop/work/requests/q<n>.md` is read; a non-UTF-8 request file refuses `show` and `add` | test_work_queue.py::test_show_refuses_a_file_under_an_initiative_that_is_not_utf8_text_naming_it (read) | search |
| scripts/model_work.py:read_work (91-97) | every directory under `.shop/work/` must have an initiative.md | a `requests/` directory produces `file: .shop/work/requests: no initiative.md` and exit 1 (probe P8) | none (no test writes a requests dir) | probe |
| scripts/model_work.py:read_records/read_work (`source` at 113-116) | only initiative `source` cites an observation | request `source` is not read, so w_uncited_obs counts o2 as uncited (probe P8) | none (read) | probe |
| scripts/work_items.py:acceptors (57-68) | glob `*/*.md`, read_text | non-UTF-8 request file raises in the plugin | none | read |

## 4. Tests the requirements make impossible to keep

No map, so `by search`. Searched test files for `work show`, `work status`, `items`, `model check` on requests dirs.
- test_work_queue.py: the two status scenarios and the show scenarios above pass today (run). They keep passing under additive reading A. Under reading B, test_status_with_no_initiative_... can no longer pass, since it asserts the initiative blocks.
- test_migration_tools.py r32 scenario (run, passes) can no longer pass unchanged under reading B and fails under A only if the hook output is asserted exact (it asserts `printed in done.stdout`, which holds under A).
- No existing test writes a requests directory, so no test breaks from model or work_items changes today (search).

## 5. A step the work-item skips

The new reader of request files skips the UTF-8 check that `workqueue.read` applies, if written outside `items()`. Frontmatter with no closing `---` is ignored silently (P7), as work-item files already are (read). Request files are not validated against any status list (model STATUSES has no request kind) (read).

## 6. Defects

- D1 (probe P6): `work show` exits 1 with `.shop/work/requests/q9.md is not UTF-8 text`, the same refusal the existing test asserts for work-items (test_show_refuses...). Whether a request file should refuse `show` is a question for the plan; both readings are open.

## 7. The file set

Changes needed, by search and read:
- scripts/work: `show` prints request lines (cmd_show, lines 27-34). 97 lines.
- scripts/workqueue.py: a `requests()` reader or items() skip logic. 262 lines, room 38.
- scripts/workqueue_status.py: no-initiative status prints observations (reading A) and the observation reader. 147 lines, room 153.
- scripts/model_work.py: `requests/` dir not an initiative dir, and request `source` as a cite. 213 lines, room 87.
- scripts/migrate_session.py: only if the hook text must stay per-initiative. 54 lines.
- tests/scenarios/test_requests.py (new): scenarios("requests.feature"). New.
- tests/scenarios/requests_*_steps.py (new): the Givens and Thens. New; the module size limit is 300.
- CLAUDE.md module map: a row for the requests concern if a new module is added.
- Modules on the path, unedited: scripts/work_items.py (131 lines, room 169), tests/scenarios/conftest.py (176 lines, room 124), tests/scenarios/test_work_queue.py (286 lines, room 14 — near the limit), tests/scenarios/work_queue_status_steps.py (157, room 143), scripts/model_facts.py (275, room 25).

Size limit: CLAUDE.md says 300 lines. Rooms are 300 minus the count.

## Conflict for the plan (both readings)

Requests r14 versus work-queue r17 on `work status` with no initiative. Reading A: print both the initiative blocks and the observations. Reading B: observations replace the initiative blocks. Reading B breaks work-queue r17 and the SessionStart hook text. The plan decides.
