# Research notes: w192 (work-queue r31, r32)

Accepted: features/work-queue.feature `add given an initiative that is <status> is refused…` (r32, outline: done, abandoned);
`withdraw that leaves every work-item of an initiative withdrawn…` (r31).
Search: no map (`tools map` not made), so `tests-of` unavailable: callers and tests by search. `tools refs` gave 0 for
`workqueue.withdraw`, `workqueue_done.becomes`, `mark` and "nothing defined as workqueue.add": not trusted, callers by search.
Scripts: `/home/vscode/shopsystem-bdd/scripts/tools`. Probe file: `.shop/scratch/1-research/probe_w192.py` (git-ignored).

## 1. Why each scenario is red today

- add [done], add [abandoned]: `python3 -m pytest -q "tests/scenarios/test_work_queue.py::test_add_given_…[done]"` (and [abandoned]).
  Undefined step: `Then "the add is refused because i1 is done, naming done"` (feature line 39). The Given
  `an initiative i1 under .shop/work/ that is done, whose work-item w1 is green` is defined (work_queue_status_steps.py:21, read).
  Missing: a Then step for `the add is refused because i1 is <status>, naming <status>`, in work_queue_add_steps.py.
  Code behind it: `workqueue.add()` (scripts/workqueue.py:76-102) reads no initiative status; it refuses only a missing
  directory (line 88-89). Probe A1 shows the add succeeds, so once the step exists the Then fails on exit 0 and w2.md written.
- withdraw: `python3 -m pytest -q "tests/scenarios/test_work_queue.py::test_withdraw_that_leaves_…"`. All steps match.
  Fails at `status_is` (test_work_queue.py:242): `AssertionError: assert 'done' == 'started'` on .shop/work/i1/initiative.md.
  Code: `workqueue_done._holds()` (scripts/workqueue_done.py:22-38) accepts any non-empty set of green/withdrawn items, with no
  "at least one green" test; `becomes()` (47-54) then says done; `workqueue.moved_to()` (workqueue.py:242-252) calls `mark()`.

## 2. What the system answers today

Probe: `python3 -m pytest -q -s -n0 .shop/scratch/1-research/probe_w192.py` (run; each case a fresh git repo in the scratch dir,
running the worktree's scripts/work).
- A1 `work add i1 "Show the queue" --part-of capability-proposal/p1 --under thing --accepts thing#r1`, initiative status done,
  w1 green: rc=0, stdout `w2`, initiative stays done, w2.md written. (r32 says refuse.)
- A2 same, status abandoned, w1 withdrawn: rc=0, stdout `w2`, w2.md written. (r32 says refuse.)
- A3 control, status started: rc=0, `w2`.
- A4 initiative directory with no initiative.md: rc=0, `w2` (r32 silent on this; a plan must choose).
- W1 scenario shape: w1 withdrawn, w2 ready, log last line w2 to ready; `work withdraw w2`: rc=0 `w2 withdrawn`; initiative now `done`. (r31 says stays started.)
- W2 only item: w1 ready, `work withdraw w1`: rc=0, initiative `done`.
- W3 control: w1 green, w2 ready, `work withdraw w2`: rc=0, initiative `done` (r23 says done; correct).
- W4 w1 withdrawn, w2 drafted, `work withdraw w2`: rc=0, initiative `done`.
All these probes had no .shop/records: W3 and W4 reached done with no measurement or analysis record (see 5).
Read (not run): `supervise.py:214-224` is `work run`'s own gate: non-empty and all green/withdrawn, then review, then
`supervise_done.set_done()` -> `holds()`, so an all-withdrawn initiative reaches `done` on `work run` too (read).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| workqueue_done.py:_holds | non-empty, all green/withdrawn, requests delivered: true | r31: all-withdrawn stays; r23 (already in spec): needs at least one green | supervision_done_steps.py (w1 green, w2 withdrawn); supervision_proposal_steps.py:37; supervision_tests_steps.py:99; test_work_queue.py r31 scenario (red) | search (no map) |
| workqueue_done.py:becomes | done if `_holds` flips with the change | same clause; also reached from `resolve` | test_work_queue.py withdraw/retry scenarios; none executes resolve with all-withdrawn | search, refs gave 0 |
| workqueue.py:moved_to (withdraw, retry) | mark done, commit initiative.md with the move | follows becomes; keeps as is for r31 | test_work_queue.py withdraw scenario (red); r23 green scenarios | search |
| workqueue_request.py:resolve (line 176) | becomes(...delivered) then mark | an initiative with only withdrawn items no longer ends on resolve | none found by search | search |
| supervise.py:214-224 and supervise_done.py:31 (set_done -> holds) | run marks an all-withdrawn initiative done after review | with the at-least-one-green clause, not marked | none runs all-withdrawn; supervision_done_steps.py (green+withdrawn) keeps passing | search, read |
| workqueue.py:add (76-102) | no initiative status read | r32: refuse done/abandoned, naming status | test_work_queue.py add outline (red); work_queue_add_steps.py | search |
| supervise_draft.py:53 and :76 (draft_proposals, fix_work_item) | add a work-item to the initiative | after r32 a Refused for a done/abandoned initiative; supervise.py:210 `self.draft()` is outside the round's try | none found by search for a done initiative being drafted | search, read |
| supervise_rounds.py:179 start_initiative (mark) | proposed -> started | none; not via becomes | none | read |

## 4. Tests the requirements make impossible to keep

By search (no map). Searched tests for `withdrawn`, `status: done`, `abandoned`, `work add` on a done/abandoned initiative.
- test_work_queue.py withdraw scenario: asserts `started`; it is the target, red, keep as written.
- tests/scripts/test_work_withdraw.py: withdrawing a withdrawn item refused; checked (read): sound, unaffected.
- supervision_done_steps.py, supervision_proposal_steps.py, supervision_tests_steps.py: green + withdrawn -> done; sound, unaffected by the clause (at least one green).
- features r23 scenarios (lines 69, 88): green + withdraw -> done; sound.
- No test asserts an all-withdrawn initiative becomes done, nor that `work add` into done/abandoned succeeds: none found.
Not run: the supervision tests above (read only).

## 5. A step the work-item skips

- Withdraw path to done (moved_to -> becomes/mark) skips supervise_done's checks: records_committed() (supervise_done.py:17-25,
  r105) and its own `work run` log line and commit (set_done: `by: work run`). Effects only that step gives: a log line
  `by: work withdraw`, and initiative.md marked done committed with the move. Probe W3 and W4 show done with no records (run).
  Whether withdraw should wait for records is for the plan; r23 as spec'd names no records.
- add: no existing step is skipped by the status read; entry(), title, newline and directory checks all stay before it (read).

## 6. Defects

D1 `work add` into a done or abandoned initiative succeeds (r32).
  Commands: `work --root <repo> add i1 "Show the queue" --part-of capability-proposal/p1 --under thing --accepts thing#r1`
  with .shop/work/i1/initiative.md `status: done` (or abandoned) and w1 green. Came back: `w2`, rc 0, w2.md written. Run (probe A1, A2).
D2 `work withdraw` of the last open work-item ends a started initiative with no green item (r31; r23's clause).
  Commands: initiative `status: started`, w1 withdrawn, w2 drafted; `work withdraw w2`. Came back: `w2 withdrawn`, rc 0,
  initiative.md `status: done`. Run (probe W4). Same with the only item (W2).

## 7. The file set

Production:
- scripts/workqueue.py (290 lines, room 10): add() reads the initiative's status, refuses done/abandoned naming it (r32). Read of add() and refs (0).
- scripts/workqueue_done.py (73 lines, room 227): _holds needs at least one green (r31 and r23). Read of _holds; probe W4.
Tests:
- tests/scenarios/work_queue_add_steps.py (60 lines, room 240): new Then "the add is refused because i1 is <status>, naming <status>";
  its work-queue binding module test_work_queue.py imports it with `*`, so test_work_queue.py (288 lines, room 12) needs no edit.
Unedited, on the path (must keep passing):
- scripts/work (171 lines, room 129): dispatch of add and withdraw; read.
- scripts/supervise.py (271 lines, room 29): run's done gate, reads holds through set_done; read.
- scripts/supervise_done.py (36, room 264): calls holds; read.
- scripts/supervise_draft.py (81, room 219): calls add; read.
- scripts/workqueue_request.py (183, room 117): resolve calls becomes; read.
- scripts/model (139): frontmatter reader; not edited.
- tests/scenarios/work_queue_withdraw_steps.py (64): no change; read.
- tests/scripts/test_work_withdraw.py (32): unaffected; read.
`tools size --limit 300` printed no file over 300.
