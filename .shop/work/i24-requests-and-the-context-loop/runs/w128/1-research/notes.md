# Research of w128: requests accepted, refused, resolved, committed

Method: no `tools map` exists, so `tests-of` and `untested` were not used; `tools refs` used for `committed`. Other callers and tests by search. Probes in `.shop/scratch/w128-1-research/` (`probe_red.py`, `probe_system.py`, `probe_withdraw.py`), run `run`. Scripts under test: this worktree's `scripts/work`, `scripts/model`.

Accepted: requests r8, r9, r10, r11, r12 (`features/requests.feature` lines 108-145). Sibling work-items: w126 (r1-r5), w127 (r7, r15-r18), w129 (r13-r14). No `Retires` section.

## 1. Why each scenario is red today

Command: `python3 -m pytest -q -s -n 0 .shop/scratch/w128-1-research/probe_red.py` (run). No node id exists: no `tests/scenarios/test_requests.py` binds `requests.feature`, so the probe binds it with pytest-bdd. 5 of 23 requests scenarios collected; the other 18 were deselected by a cause not identified (no `--work-item`, `-m ""` and `-o addopts=""` made no difference). All 5 fail with `StepDefinitionNotFoundError` on their first Given:

- r8 (line 109, "upstream ending its turn, accepted"): Given "a request q1 ... with three lines whose line outcomes are accepted, refused and withdrawn" undefined (line 111). When `work turn q1` absent: `scripts/work` has no `turn` (run).
- r9 (line 116, "refused"): Given undefined (line 118). When `work turn` absent.
- r10 (line 123, "resolve ... requirement id and version"): Given undefined (line 125). When `work resolve` absent (run).
- r11 (line 132, "delivered"): Given undefined (line 134). When `work resolve` absent.
- r12 (line 139, "commits the request"): Given undefined (line 141). When `work outcome` absent (run). Its Thens have no step: "main has a new last commit, which holds q1 as work left it" matches `tests/scenarios/work_queue_git_steps.py:47` only as a path (`{rel}`), so `git show main:q1` would fail; "nothing work keeps for q1 differs from main's last commit" matches nothing (`work_queue_git_steps.py:56` reads "nothing under {where} ...").

Missing in code: `scripts/work` dispatch (lines 88-90) has no `outcome`, `turn`, `resolve`, `request`; no module keeps requests (`grep request` over `scripts/` finds none). Missing in tests: no step module for requests; no `test_requests.py`.

## 2. What the system answers today

Probe 1 (`probe_system.py::test_01`, run): against a scratch repo with `q1` hand-written at `.shop/work/requests/q1.md`:
- `work outcome q1 1 accepted`, `work turn q1`, `work resolve q1`, `work request ...` → rc 2, `argument cmd: invalid choice`. Nothing written.
- `work show` → rc 0, no output (lists only initiative work-items).

Probe 2 (`test_02`, run): with the request file committed:
- `work status` → rc 0, `initiative i1 started`, ignores the request.
- `work show --json` → `{"work-items": []}`, ignores the request.
- `model check` → rc 1, `file: .shop/work/requests: no initiative.md` (see defect D2).

Not run: the Givens' other shapes (absent q1, twice, empty lines). The request's Givens are hand-written files; no command creates one today.

## 3. Old assumptions

Requests are kept under `.shop/work/requests/`, a directory the work-queue code reads as if it held initiatives or work-items.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/model_work.py:read_work (93-96) | every directory under `.shop/work/` must hold `initiative.md` | `.shop/work/requests/` holds no initiative.md: `model check` reports it (D2) | tests/scenarios/test_design_model_check.py (scenarios r112, r114, r119 name `.shop/work/requests/`) | read, probe 2 |
| scripts/workqueue.py:find (206-211) | globs `*/<name>.md` under `.shop/work/`, any kind | `work withdraw q1` finds `requests/q1.md` (D1) | none (no test withdraws a request; tests/scenarios/work_queue_withdraw_steps.py and tests/scripts/test_work_withdraw.py use work-items) | read, probe_withdraw |
| scripts/workqueue.py:highest (65), items (102) | globs `*/*.md`, keeps `kind: work-item` only | requests skipped by kind: no change needed | by search: tests/scripts (work add/numbering) | read |
| scripts/workqueue_status.py:113-117, 133-137 | globs `*/initiative.md` only | requests ignored: no change needed | by search: tests/scenarios/work_queue_status_steps.py | read, probe 2 |
| scripts/work_items.py:acceptors (62), accepted (52) | globs `*/*.md`, keeps `kind: work-item` | requests ignored by kind | by search: tests/scripts/test_work_items.py | read |
| scripts/model_work.py:read_part (127-131), model.lp:54 (`delivered` closes a part) | reads parts of initiatives only; no request facts | a `delivered` request status has no effect today | none | read: model_work.py never opens `requests/` |
| scripts/workqueue.py:committed (236) | commit way: rev-parse, write, `git add`/`commit -- rels`, rollback on failure | r12 needs it for request files; used as is | by search: work add/note/retry/withdraw steps (tests/scenarios/work_queue_*_steps.py) | tools refs: 7 refs (scripts/workqueue.py:96,196,222; scripts/supervise_faults.py:101,106; tests/scenarios/supervision_review_steps.py:63-64) |

`scripts/supervise_faults.py:114` has its own `committed` method (a second commit way, not called by requests).

## 4. Tests the requirements make impossible to keep

None. The requirements add commands and a module; none changes a function an existing test runs. Searched: `tests/` for `invalid choice|usage: work|--help|choose from|subcommand` (none, so no test lists the subcommands); tests of `workqueue.withdraw` (tests/scripts/test_work_withdraw.py, two checks: withdrawn refused and nothing committed) stay true. No test asserts that `withdraw` refuses a request. Caveat: no map, so the lists are by search, not `tests-of`.

## 5. A step the work-item skips

The request commands must take the existing commit way `workqueue.committed` (scripts/workqueue.py:236). Each effect only that step gives, shown by probe_system.py (run):
- Not a git repository: refused before anything is written: `work: git rev-parse failed: ... not a git repository`; ledger not written (test_03).
- Commit fails (pre-commit hook exit 1): refused `git commit failed: exit 1`; the written file is taken back (test_04; the ledger was new, so removed. For an existing file, the bytes are restored: read, workqueue.py:248-250).
- Only the named files are committed: an unrelated staged `other.txt` stays staged; HEAD holds only `.shop/work/i1/ledger.md`, message `work note: i1` (test_05).
- On failure, the named files are unstaged (`git reset -q -- rels`, workqueue.py:250; read).

A request command that writes without this step skips all four. Also read: `supervise_faults.py:114` is a second copy with its own steps (not checked).

## 6. Defects

D1. `work withdraw` takes a request as a work-item (probe_withdraw.py::test_withdraw_a_request_id, run):
- `work withdraw q1` with `.shop/work/requests/q1.md` (`kind: request`, `status: open`) → rc 0, `q1 withdrawn`.
- The file's status became `withdrawn`; `.shop/work/requests/log.jsonl` got `{"work-item": "q1", "before": "open", "after": "withdrawn", ...}`; commit `work withdraw: q1 open -> withdrawn`.
- Cause: scripts/workqueue.py:find (206-211) globs any `.shop/work/*/<name>.md` and never checks `kind`.

D2. `model check` reports the request directory as an initiative with no initiative.md (probe_system.py::test_02, run):
- Output: `file: .shop/work/requests: no initiative.md`, rc 1.
- Cause: scripts/model_work.py:93-96 treats every directory under `.shop/work/` as an initiative.
- The design-model-check scenarios r112 (`features/design-model-check.feature:902-909`) expect no such problem for a request `work request` wrote; they are for another work-item.

## 7. The file set

Production:
- `scripts/work` (97 lines; room 203): add `outcome`, `turn`, `resolve` to argparse and the dispatch dict (lines 56-93). Read whole file.
- New module, name not decided (e.g. `scripts/workqueue_request.py`): the turn, outcome, resolve and the status rules of r8, r9, r10, r11, r12 commit. A new concern gets a new module and a CLAUDE.md row.
- `CLAUDE.md` (module map, lines 9-31): one row for the new module. Read.
- `scripts/workqueue.py` (262 lines; room 38): read only, `committed` reused. Changes only if the plan fixes D1 (find, line 208), which no accepted scenario needs.
- `scripts/model_work.py` (213 lines; room 87): changes only if the plan fixes D2 (line 93). Not needed by the accepted scenarios.

Tests:
- `tests/scenarios/test_requests.py` (new): `scenarios("requests.feature")`, as `test_work_queue.py:30` does (pattern read: `tests/scenarios/test_work_queue.py`).
- `tests/scenarios/requests_*_steps.py` (new, one or more; the concern is the request files and their commands): the Givens that write `q1` with lines, outcomes, status, turn, resolution (form not fixed: see questions); the Whens running `work`; the Thens of r8-r11.
- `tests/scenarios/work_queue_git_steps.py` (59 lines; room 241): its `new_commit_holds` (line 47) takes a path. The r12 Then needs `q1` mapped to `.shop/work/requests/q1.md`: either a new step there or in the new module. Two steps with one pattern would clash.
- `tests/scenarios/conftest.py` (176 lines; room 124): not read. The new steps use the `repo` and `context` fixtures (`context["done"]`, set by a When); check whether the new When sets it.
- `tests/scenarios/test_work_queue.py` (286 lines; room 14): no change; its scenarios are unaffected.

Modules on the change's path, unchanged: `scripts/work_items.py` (131, room 169), `scripts/model_work.py` (213, room 87). Size check: `tools size --limit 300` printed nothing (run; none over 300).

Open points for the plan (both readings given, no choice made):
- Q1. How `work resolve` takes each accepted line's requirement id and version: the capability gives `work resolve <request>` only; r10's When says "giving thing#r3 for line 1 and thing#r4 for line 2, each found in the version 0.26.0". Options: arguments, a file, or stdin. The version may come from the spec or the caller.
- Q2. The form of `## Outcomes` (line outcomes, "one a line") and `## Resolution` (per-line ids and versions): the capability does not fix it. The Givens and Thens depend on it, and model's reading (design-model-check r116, v3) expects a resolution that "names" `thing#r9`.
- Q3. Dependencies: r8 and r9 run `work turn`, which w127 (r7, r17, r18) builds; r10 and r11 run `work resolve` in the asker's turn, which passes only with w127's r16 exemption for `resolve`. Either w128 contains those pieces, or it depends on w127.
- Q4. r12 Thens need new steps (see above).
