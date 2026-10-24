# w130 research notes

Accepted: work-queue#r22 (start), work-queue#r23 (done). Scenarios: features/work-queue.feature lines 34-62.
Search basis: `tools refs` works; `tools tests-of` and `untested` refuse (no map, `tools map` not run). Test lists below are `by search` or `read`.
Probes: `.shop/scratch/w130-1-research/probe_start_done.py`, `probe_commit.py`; run with `-n 0`. Repos made there only.

## 1. Why each scenario is red today

- r22 `start on an accepted request ...` — `python3 -m pytest -q "tests/scenarios/test_work_queue.py::test_start_on_an_accepted_request_..."` (run): StepDefinitionNotFoundError at feature line 38, Given "a request q1 that is accepted, whose origins are o1 and o2". Missing: a step writing `.shop/work/requests/q1.md`; Thens for "one new initiative", "fulfils q1 ... source", "prints that initiative's id" (grep: no `fulfils` in tests or scripts). Code: `scripts/work` has no `start` (subparsers lines 64-85; probe P1 exit 2, "invalid choice: 'start'"); `start` absent in `scripts/workqueue*.py`.
- r23 outline, 4 rows — `python3 -m pytest -q "tests/scenarios/test_work_queue.py::...sets_the_initiative_to_done[<row>]"` (run, all 4): StepDefinitionNotFoundError at line 51 (the request Given): "no request kept in this context names i1", "...asker is this context, names i1 and is delivered", "...asker is another context, names i1 and is accepted", "...names i2 and is accepted". Line 49 resolves; line 50 is `last_for`. Missing: steps for the four request phrasings and for the Background Given; no step creates `.shop/work/requests/`. Code: `scripts/workqueue.py:withdraw` (214-224) has no done check; `move` (127-150) writes file and log only.

## 2. What the system answers today

Probes (all `run`, scratch repos, `work` from the worktree's scripts/):
- P1 `work start q1` with requests/q1.md (status accepted, source o1,o2) → exit 2, "invalid choice: 'start'"; no file written under .shop/work.
- P2 `work withdraw w2` (w1 green, w2 ready, no request) → exit 0, "w2 withdrawn"; initiative.md still `status: started`; commit holds w2.md and log.jsonl only. Scenario row 1 wants `done`.
- P3 same plus requests/q1.md (asker this context, part_of i1, delivered) → withdrawn; initiative still `started`. Row 2 wants `done`.
- P4 `work show` and `work status i1` with requests/q1.md present → print the initiative and work-items only; requests/ is ignored (kind check in `items`).
- P5a withdraw w2 twice → 2nd exit 1, "w2 is already withdrawn". P5b w2 claimed → exit 1, refused. P5c w9 missing → exit 1, "there is no work-item w9 under .shop/work".
- P6 not a git repository (GIT_CEILING_DIRECTORIES set) → exit 1, "git rev-parse failed"; w1.md unchanged.
- P7 pre-commit hook refuses → exit 1, "git commit failed: refused by hook"; w2.md restored to `ready`; log unchanged; `git status` clean.
- Nearest, not probed: an initiative with no work-items cannot reach withdraw (find refuses): read.
- Nearest, not probed: a request whose status is not accepted for start: read (no start code).

## 3. Old assumptions

A transition writes the work-item's file and log only; the commit covers only those files. A done write is a second file and is not in any commit.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue.py:move (127-150) | writes work-item file and log line | r23 must run after a green or withdrawn move; a done write here also fires from work run, retry, answer | by search: test_work_queue.py move steps (r4-r6), supervision tests via supervise | refs (2 refs), search |
| scripts/workqueue.py:withdraw (214-224) | commits `rels_of` only | initiative.md must join the same commit or `nothing under .shop/work/ differs from main` fails | read: test_work_queue.py r9 withdraw row (features 220, 236) and r10 scenario (198) | refs, read |
| scripts/workqueue.py:rels_of (201-203) | file + log.jsonl | must include initiative.md when done is written | read: r9 retry and answer rows | read |
| scripts/workqueue_answer.py:answer (24-48) | `committed(rels_of)` around move | the move's hook can run here; awaiting-answer→ready cannot make done | read: work_queue_answer_steps.py (r13-r15, r9 answer row) | refs |
| scripts/workqueue.py:retry (185-198) | committed(rels_of) around move | the hook can run here; failed→before cannot make done | read: test_work_queue.py r8 (190), r9 retry row | refs |
| scripts/supervise.py:move (101-108) and commit (89-99) | move, then commit only the work-item, its runs and log | a done write by work run's green move stays uncommitted | by search: features/supervision.feature:145-147 ("initiative.md is as it was"), test_supervision.py:130 | refs |
| scripts/supervise.py:check (77-81) | refuses any uncommitted change under .shop/work | an uncommitted done write (or uncommitted start) makes the next `work run` refuse | by search: supervision tests (refusal) | read |
| scripts/supervise.py:run (189, 205) | `all green or withdrawn` predicate | unchanged; but the initiative is done by then | by search: supervision tests | read |
| scripts/supervise_merge.py:134, supervise_faults.py:83 | move to done / failed | `done` (work-item) is not `green`: no trigger; `failed` none | by search: supervision tests | refs |
| scripts/model.lp:240 (v_d1) and model_work.py:10 | flags a done initiative whose root (capability-proposal) is not closed | r23 can set done while the proposal is only formulated: model check would flag it | none (no test writes a done initiative) | read |
| scripts/migrate_session.py:30-40 (via workqueue_status.open_names, 113-117) | compaction skips done initiatives | a done initiative leaves the PreCompact ledger compaction | none found: no test sets an initiative done and runs compaction (grep `status: done`) | refs, search |

## 4. Tests the requirements make impossible to keep

No map, so search and read. Nothing found that is impossible to keep if the done write is committed with the work-item.
- features/work-queue.feature r9 withdraw row (220, 236) and "nothing under .shop/work/ differs" (230): kept only if initiative.md is committed in the same commit. read.
- test_work_queue.py r10 scenario (198-204): kept; its Thens do not look at the initiative. read.
- tests/scripts/test_work_withdraw.py: refusal of a withdrawn item commits nothing; the hook must run only after a successful move, and the repo has no initiative.md. Kept. read.
- features/supervision.feature:145-147 and test_supervision.py:130-132: "initiative.md is as it was" breaks if work run's green move counts as a `work` command's change (w1 drafted goes to green). read, not run. Conflict: see question Q4.
- features/supervision.feature:580-583: w1 failed; no green; kept. read.
- test_work_queue.py r23 Examples and r22: currently red (section 1).

## 5. A step the work-item skips

The start path, as r22 reads, writes initiative.md with none of `committed()`'s steps. The existing way of writing .shop/work files is `committed()` (`add`, `retry`, `withdraw`, `answer`), so:
- git-repository check before writing (P6, run): refused "git rev-parse failed", nothing written.
- commit of its own files (P2, run: commit holds the work-item and log only).
- rollback when the commit fails (P7, run): the files are restored and `git reset` runs.
- start's new initiative.md is not committed by any rule in r9; the next `work run` refuses uncommitted changes under .shop/work (supervise.py:77-81, read). Q5.
- The done write in withdraw/answer/retry goes through `move`, inside `committed`; in work run it goes through supervise.commit, which skips it (read).

## 6. Defects

None found by the probes run (P1-P7). `work` refuses each bad input with a message and no traceback. Not a defect, a gap: the done write has no commit path yet (section 3).

## 7. The file set

Production and test files the change needs (r22 and r23 pass; passing tests keep passing):
- scripts/work (97 lines, room 203): add `start` subparser and dispatch entry (grep: subparsers lines 64-90).
- scripts/workqueue.py (262, room 38): `rels_of` and `withdraw` commit initiative.md when done is written; hook point for the done check (`move`). Tight: prefer a new module for the check.
- scripts/workqueue_done.py (new): the r23 check over initiatives and `.shop/work/requests/*.md`.
- scripts/workqueue_start.py (new): r22: read the accepted request, write initiative.md proposed.
- scripts/supervise.py (218, room 82): commit paths include initiative.md when done is written. Only if Q4 says work run counts (read).
- scripts/workqueue_answer.py (48, room 252): no change expected if the hook sits in `move` (read).
- tests/scenarios/test_work_queue.py (286, room 14): one import line for the new step module. Its scenarios bind by `scenarios()`.
- tests/scenarios/work_queue_start_steps.py (new, room 300): request Givens, start When and Thens, the r23 Given phrases.
- tests/scenarios/work_queue_withdraw_steps.py (64, room 236): may take the r23 Given "that is started, whose work-item ...".
- CLAUDE.md: module map row for each new module (the repository's rule).
- tests/scripts/test_work_withdraw.py (32): unchanged; read.
- Modules on the path, edited or not: scripts/supervise_merge.py (135, room 165), scripts/supervise_faults.py (160, room 140), scripts/workqueue_status.py (147, room 153), scripts/migrate_session.py (not counted: `wc` not run). `tools size --limit 300` printed nothing (run): no tracked Python file is over 300.
