# w160 research notes

Work-item: `.shop/work/i24-requests-and-the-context-loop/w160.md`, accepts `work-queue#r23`, retry fix of branch review 1 F5.
Accepted scenarios (`features/work-queue.feature`):
- A: the Outline "a command whose change leaves every work-item ... sets the initiative to done" (4 Examples).
- B: "retry that makes an initiative's last open work-item green again sets the initiative to done".

Method notes: `tools tests-of` answers "no map" (I did not make one), so every test list below is `by search` or `read`. `tools refs workqueue.retry` says 0 references, yet `scripts/work:45` calls it: `refs` missed the module-attribute call, so callers are `by search`.

## 1. Why each scenario is red today

- **A (Outline, 4 rows)**: green today. `python3 -m pytest -q -s -n 0 "tests/scenarios/test_work_queue.py" -k sets_the_initiative_to_done` gives 4 passed. Withdraw already ends the initiative (`scripts/workqueue.py:withdraw`, lines 231-248, calls `workqueue_done.becomes` and `mark`). Nothing to fix for A.
- **B (retry)**: red. `python3 -m pytest -q "tests/scenarios/test_work_queue.py::test_retry_that_makes_an_initiatives_last_open_workitem_green_again_sets_the_initiative_to_done"` fails at `status_is` (`tests/scenarios/test_work_queue.py:242`): `assert 'started' == 'done'` on `.shop/work/i1/initiative.md`. The w2 step passes (w2 becomes green).
  - Cause: `scripts/workqueue.py:retry` (lines 202-215) makes the move and never calls `workqueue_done.becomes` or `mark`. Its commit (`rels_of`, lines 218-220) lists only the work-item file and `log.jsonl`, not `initiative.md`.
  - Steps: all Givens and Thens of B exist and run (`with_items`, `last_moves`, `no_request` in `tests/scenarios/test_work_queue.py` and `work_queue_start_steps.py`). No undefined step.

## 2. What the system answers today

Probe file: `.shop/scratch/w160-1-research/probe_retry_done.py` (in scratch, not tracked). Command: `python3 -m pytest -q -s -n 0 .shop/scratch/w160-1-research/probe_retry_done.py` (`-n 0` because xdist hides prints). Each probe makes its own repo under the scratch dir and runs `scripts/work` of this worktree. All `run`.

- P1 (B's Givens, `work retry w2`): rc 0, `w2 green`; w2 green, initiative `started`; commit lists w2.md and log.jsonl only. This is the red case.
- P2 (control: this context's accepted request naming i1, `work retry w2`): `w2 green`, initiative `started`. Correct today; must stay `started` after the fix.
- P3 (another context's accepted request naming i1): `w2 green`, initiative `started`. Should become `done` after the fix (r23 counts only requests this context asked).
- P4 (w3 still `failed` as well): `w2 green`, initiative `started`. Correct today and after.
- P5 (initiative already `done`): `w2 green`, initiative stays `done`. Fine.
- P6 (no initiative.md at all): `w2 green`, exit 0, no traceback. The fix must not crash on a missing initiative.md.
- P7 (initiative.md with no `status:` line): `w2 green`, exit 0, status line still absent.
- P8 (control: `work withdraw w2`, last open item, i1 started): `w2 withdrawn`, initiative `done`; commit lists initiative.md, log.jsonl, w2.md. The existing way that ends an initiative.
- P9 (withdraw as P8, but initiative.md has no `status:` line): `w2 withdrawn`, exit 0, no error. initiative.md unchanged, not done. Silent, see D1.

## 3. Old assumptions

The requirement adds: a retry that completes an initiative ends it, as withdraw does. Places that assume retry never does:

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/workqueue.py:retry (202-215) | moves the item back to its pre-failed status; no done check | must run `becomes` before the move and `mark` after, as withdraw does | test_work_queue.py retry scenarios (r8, r9 retry commit, r23 retry): `run` for the r23 one; the others `by search` | read; search for callers |
| scripts/workqueue.py:rels_of (218-220) | file + log.jsonl only; retry's commit uses it | commit must also list initiative.md when it is marked done (withdraw adds it itself, line 241) | same as above, `by search` | read |
| scripts/work:cmd_retry (44-46) | prints `<name> <status>` | prints the item's status only; done is not printed today. Plan decides whether to print it | `by search`: test_work_queue.py `work retry` runs (r8, r9, r23) | text search `retry` |
| scripts/supervise.py:move (109-116) and pull_through (205) | `work run` moves a work-item to green through `workqueue.move` with no done check; all-green is only tested (line 205), not marked done | reading 1: r23 is about `work retry` only (accepted scope), leave it. Reading 2: r23 says "a `work` command", and `work run` is one, so a worker's green move completing the initiative is in scope too | `by search`, not read: supervision tests under tests/scenarios/supervision_*.py | read |
| scripts/workqueue_done.py:mark (51-56) | rewrites the first `status:` line; silent when none | none for B; see D1 | not searched | read |
| scripts/workqueue_answer.py:48 | `answer` moves an item via `workqueue.move` | cannot reach green, so no requirement effect | none (not searched) | read |

## 4. Tests the requirements make impossible to keep

- Verified sound (read): `tests/scenarios/test_work_queue.py` retry tests (r8 scenario, r9 retry commit, r23 retry). They assert the item's status, its commit contents and that nothing under `.shop/work/` differs. The r9 retry commit still holds w1.md and log.jsonl after a done write (it asserts they are in the commit, not that nothing else is). The `work_queue_git_steps.py` `failed_implementing` Given moves w1 to claimed, not green, so no done.
- Verified sound (read): `tests/scripts/test_work_withdraw.py` (withdrawing a withdrawn item is refused). Withdraw path unchanged.
- Found by search, not read: `tests/scenarios/supervision_*` and `test_supervision.py` assert initiative status around `work run`. Whether any asserts "initiative still started after all-green" is not checked. Matters only under reading 2 of part 3.
- Result: none found that the accepted scope (retry only) makes impossible. Under reading 2, the supervision tests must be read first.

## 5. A step the work-item skips

Retry skips the done check that withdraw runs (`workqueue_done.becomes` and `mark`, `scripts/workqueue.py:withdraw` lines 239-247). Effects only that step produces, each shown:
- initiative.md `status: done` (P8 vs P1: done only on withdraw).
- initiative.md in the commit (P8: listed; P1: not listed).
- No refusal comes from the done step: `becomes` and `mark` return or write, they never raise. Read.
- Read, not probed: withdraw imports `workqueue_done` inside the function because `workqueue_done` imports `workqueue` (comment at line 239). Retry needs the same lazy import, or the cycle breaks at module load. Read.
- Read: retry reads the log and the file (`agrees`, `logged`) before its write inside `committed`, with no lock. Withdraw does the same. No new gap from the done step.

## 6. Defects

### D1: withdraw of the last open work-item, initiative.md with no status line, reports success and does not end the initiative
Reproduction (probe P9, `run`):
```
python3 -m pytest -q -s -n 0 .shop/scratch/w160-1-research/probe_retry_done.py   # test_p9
```
Setup: `.shop/work/i1/` with w1 green, w2 ready, log line planned to ready, and `initiative.md` = frontmatter with id and kind, no `status:` line.
Command: `work withdraw w2`. Came back: rc 0, stdout `w2 withdrawn`, no stderr. w2 withdrawn. initiative.md unchanged, no status line; the commit lists w2.md and log.jsonl only.
Cause (read): `workqueue_done.mark` (`scripts/workqueue_done.py:51-56`) replaces only an existing `status:` line; with none, nothing is written and the commit proceeds.

P7 (retry on such a file) does not reach D1 today, since retry never ends an initiative. After the fix, retry on that file would hit the same silent no-op.

## 7. The file set

Production:
- `scripts/workqueue.py` — `retry`: call `becomes` before the move, `mark` after it, and add initiative.md to the commit when marked; lazy import as withdraw does. Found by read (lines 202-215, 231-248). 286 lines, room 14.

Modules on the change path, not edited:
- `scripts/workqueue_done.py` — `becomes`, `mark`: used as they are (D1 is outside B's scope). 67 lines, room 233.
- `scripts/work` — `cmd_retry` prints the status; no change needed for B. 150 lines, room 150.
- `scripts/model` — frontmatter reader used by workqueue; no change. 139 lines, room 161.

Tests:
- `tests/scenarios/test_work_queue.py` — no change needed; B's step already exists and fails only on the initiative status. 288 lines, room 12.

Conditional (only under reading 2 of part 3):
- `scripts/supervise.py` — `move` or `pull_through` would need the done check too. 247 lines, room 53. Not required by the accepted scenarios.

`tools size --limit 300` printed nothing: no tracked Python file is over 300 lines.
