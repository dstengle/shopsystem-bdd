# w159 research notes

Method: `tools refs` for names; `tools tests-of` has no map (no map made), so test lists are `by search` (grep of tests/) unless marked.
Scripts: /home/vscode/shopsystem-bdd/scripts. `model` run from this worktree's `scripts/model`.
Probes ran with `-n 0`: under the default xdist, `-s` output is swallowed.
Accepted scenarios: 5 (design-model-check.feature, r27). Two are red, three already green.

## 1. Why each scenario is red today

- **a status in its kind's lifecycle is no file problem** (outline, 2 rows): red.
  Run: `python3 -m pytest -q -p no:warnings "tests/scenarios/test_design_model_check.py::test_a_status_in_its_kinds_lifecycle_is_no_file_problem"` gives 2 failed, 0 passed.
  - Row "a work directory .shop/work/i1 has the part p1.md with the kind capability-proposal and the status awaiting-answer": fails at the Given "a repository in which {case}", `tests/scenarios/design_model_check_problems.py:147` AssertionError. `malformed_record` (problems.py:123) has no branch for the case and falls through to the assert.
  - Row "a request in .shop/work/requests/q1.md ... has the status withdrawn": same, at problems.py:147.
  - Code, also red (probe P1, read):
    - `scripts/model_work.py:11` STATUSES["capability-proposal"] lacks `awaiting-answer`. `status()` (model_work.py:216) flags it.
    - `scripts/model_work.py:14` STATUSES["request"] lacks `withdrawn`. Called from `scripts/model_requests.py` (`read_requests`).
- **a malformed work directory or work file is a file problem** (outline, 9 rows): green. Run: 9 passed.
- **a work-item accepting a requirement no scenario names is a file problem**: green. Run: passed.
- **a work-item accepting a requirement of a guarantees capability that no scenario names is no file problem**: green. Run: passed.
- **a green work-item accepting a retired id is no file problem**: green. Run: passed.

Run totals: `python3 -m pytest -q -p no:warnings` on the five node ids: 12 passed, 2 failed.

## 2. What the system answers today

Probe P1: `python3 -m pytest -q -s -n 0 .shop/scratch/w159-1-research/probe_lifecycle.py` (`run`). Each case is a repository with a good capability, `model check --root <repo>`:

| case | exit | answer |
|---|---|---|
| control: proposal drafted | 0 | 0 file problems |
| proposal awaiting-answer | 1 | `file: .shop/work/i1/p1.md: status 'awaiting-answer' is not one of approved, drafted, formulated, merged, withdrawn` |
| control: proposal withdrawn | 0 | 0 file problems |
| control: request open | 1 | v17 only (no origin cited; not a file problem) |
| request withdrawn | 1 | `file: .shop/work/requests/q1.md: status 'withdrawn' is not one of accepted, awaiting-asker, awaiting-upstream, delivered, open, refused` |
| request refused (in set) | 1 | v17 only, no file problem |
| request awaiting-asker (in set) | 1 | v17 only, no file problem |

Probe P2: `python3 -m pytest -q -s -n 0 .shop/scratch/w159-1-research/probe_items_done.py` (`run`). Work-item cases: the capability `thing` has r1 (scenario), r2 (no scenario), retired r3. The v_b1, v_k3 and v_s3 lines in its output come from the repository's shape, not the cases.

| case | file problem naming w1.md |
|---|---|
| W1 drafted accepts thing#r2 (no scenario) | yes |
| W2 withdrawn accepts thing#r2 | no |
| W3 awaiting-answer accepts thing#r2 | yes |
| W4 green accepts retired thing#r3 | no |
| W5 drafted accepts retired thing#r3 | yes |
| W6 drafted accepts thing#r9 (no such requirement) | yes, and 0 unresolved |

Done cases (P2, `run`):
- D1 initiative done, kept request withdrawn: `v_d1` names initiative/ex.com/prod/ctx/i1 (1), plus the file problem above.
- D2 initiative done, kept request refused: `v_d1` names the same initiative, no file problem.
- D3 initiative done, proposal withdrawn: no `v_d1`.
- D4 initiative done, proposal awaiting-answer: `v_d1` names the initiative, plus the file problem.

Nearest cases the scenarios do not give:
- Status "built" on a capability-proposal stays a file problem (scenario row, passes).
- A missing scenario-named requirement for a withdrawn work-item stays silent (W2).

## 3. Old assumptions

The old assumption: a capability-proposal's lifecycle has no `awaiting-answer`, and a request's has no `withdrawn`. The glossary (spec/index.md:128) already gives both. `tools refs STATUSES`: 2 production files, 0 test files (scripts/model_work.py:216, scripts/workqueue.py:151).

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/model_work.py:11 STATUSES["capability-proposal"] | omits awaiting-answer; flags it (P1) | add awaiting-answer | design_model_check_problems.py malformed_work row "status built" (passes); test_model.py WithdrawnTest (by search) | read, refs, P1 |
| scripts/model_work.py:14 STATUSES["request"] | omits withdrawn; flags it (P1) | add withdrawn | none (by search: no test has a request with status withdrawn) | read, refs, P1 |
| scripts/model_work.py:216-219 status() | the one check; flags both | unchanged | test_model_reading.py:49 test_failed_is_a_work_item_status (by search) | read, refs |
| scripts/model_requests.py read_requests (status call) | calls the request set for every request | gets withdrawn | none (by search) | read |
| scripts/model.lp:247 v_d1 (own request not delivered) | a kept withdrawn request is not delivered: blocks `done` (D1) | requirement silent; reading needed (see 6.3) | none (by search: design_model_check_requests.py request rules, no withdrawn row) | read, P2 |
| scripts/workqueue_done.py:31-36 | a kept request not delivered blocks done; withdrawn included | silent; reading needed | none (by search) | read |
| scripts/workqueue_request.py:112-118 | writes request statuses awaiting-asker, awaiting-upstream, accepted, refused, delivered; never withdrawn | the requirement accepts withdrawn, but no command writes it | none (by search) | read, grep `withdrawn` |
| scripts/workqueue.py:16,19,151 | a capability-proposal may take any work-item status plus approved, formulated (includes awaiting-answer) | agrees with the glossary; the model's list is now the stricter one | test_work_queue.py:78 mentions awaiting-answer (by search) | refs, read |

## 4. Tests the requirements make impossible to keep

Searched (`by search`): grep for "is not one of", "not in its kind", "awaiting-answer", "withdrawn" under tests/. No test asserts that an awaiting-answer proposal or a withdrawn request is a file problem. The one "is not one of" assertion (tests/scripts/test_model_reading.py:56) is about `failed`, which stays.

Verified sound (read, by search):
- tests/scripts/test_model_reading.py `test_failed_is_a_work_item_status`: `failed` unchanged. Keeps.
- tests/scripts/test_model_withdrawn.py `test_r27_a_withdrawn_work_item...`: the withdrawn work-item exemption (model_work.py:199) unchanged. Keeps.
- tests/scripts/test_model.py WithdrawnTest.test_r59: a withdrawn proposal is still closed. Keeps.
- tests/scenarios/design_model_check_problems.py malformed_work, row "built": still a file problem. Keeps (run: passed).
- tests/scenarios/design_model_check_requests.py request-rule rows (v16a, v_d1, v_d3, v17): no withdrawn request in them. Keeps (read; not run).

Result: none can no longer pass as it is.

## 5. A step the work-item skips

None. The work-item widens two accepted sets in one existing check (`status()`, model_work.py:216); it adds no path. The request's status and the part's status both go through `status()` (model_requests.py; model_work.py:142). `work` writes no withdrawn request status (read, 2 above). Nothing is skipped (read).

## 6. Defects

Reproduction for each: the command, then what came back. Scripts: the worktree's `scripts/model`.

### 6.1 An awaiting-answer capability-proposal is a file problem
Command: `python3 -m pytest -q -s -n 0 .shop/scratch/w159-1-research/probe_lifecycle.py`.
Came back, for case "proposal awaiting-answer": `exit=1`, `file: .shop/work/i1/p1.md: status 'awaiting-answer' is not one of approved, drafted, formulated, merged, withdrawn`. The control "proposal drafted" gives exit 0.

### 6.2 A withdrawn request is a file problem
Same command. Case "request withdrawn": `exit=1`, `file: .shop/work/requests/q1.md: status 'withdrawn' is not one of accepted, awaiting-asker, awaiting-upstream, delivered, open, refused`.

### 6.3 A kept withdrawn request blocks `done` (reading-dependent)
Command: `python3 -m pytest -q -s -n 0 .shop/scratch/w159-1-research/probe_items_done.py`. Case D1 (initiative done, kept request withdrawn): `v_d1  a done initiative has a part or a request of its own open (1)` names initiative/ex.com/prod/ctx/i1. D2 (refused) gives the same. `delivered` needs `done` (v_d3), so nothing in the model lets a withdrawn request reach `delivered`. Reading A: `not delivered` in r114 is literal, so this is as designed. Reading B: a withdrawn request should not block `done`, as work-queue's `done` condition also reads "delivered" (workqueue_done.py:36). Both readings are open.

### 6.4 A work-item accepting a missing requirement is a file problem (reading-dependent)
Command: probe P2, case W6 (`accepts thing#r9`, r9 does not exist). Came back: `file: .shop/work/i1/w1.md: accepts ...thing#r9, which no scenario names yet` and `0 unresolved references`. r27 read literally gives this; r9 ("a scenario names a requirement its capability does not have") is about scenarios, not accepts. Whether a file problem or an unresolved reference is right is open.

## 7. The file set

Production:
- `scripts/model_work.py` (219 lines; room 81): add `awaiting-answer` to STATUSES["capability-proposal"] (line 11) and `withdrawn` to STATUSES["request"] (line 14). Found by read, refs, P1.

Tests:
- `tests/scenarios/design_model_check_problems.py` (300 lines; room 0): `malformed_record` (123-147) needs branches for the two status rows. Any added line goes over 300 under CLAUDE.md, so the branches go elsewhere.
- New module, e.g. `tests/scenarios/design_model_check_lifecycle.py` (new): the two rows' Given. Two modules with the same Given pattern "a repository in which {case}" collide, so either move `malformed_record` out of problems.py or give the rows a module of their own; the plan picks.
- `tests/scenarios/test_design_model_check.py` (54 lines; room 246): one import line for the new module (lines 11-19 import the step modules).

Kept passing (not changed): `tests/scripts/test_model_reading.py` (258; room 42), `tests/scripts/test_model_withdrawn.py` (30), `tests/scripts/test_model.py` (213), `tests/scenarios/design_model_check_requests.py` (132).

Modules on the change's path (edited or not), `wc -l`, room under 300:
- `scripts/model` (139; room 161): the entry; loads model_check and model_facts.
- `scripts/model_check.py` (139; room 161): check and its output.
- `scripts/model_facts.py` (287; room 13): Model; calls read_work and read_requests.
- `scripts/model_parse.py` (271; room 29): frontmatter reading.
- `scripts/model_requests.py` (63; room 237): request status call.
- `scripts/model.lp` (326 lines; not Python, so no limit in CLAUDE.md): v_d1 and v_d3 read by reading 6.3.
- `scripts/workqueue_done.py` (67; room 233): reading 6.3's second side, not edited.

`tools size --limit 300`: no Python file printed (no file over the limit today).
