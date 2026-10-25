# Plan of w160: work retry back to green runs the done check (branch review 1, F5)

Accepts `work-queue#r23`. Under `work-queue`. No `Retires`, no `## Rulings`.

## 1. What goes green

`work-queue#r23`, scenarios in `features/work-queue.feature`:

- **"a command whose change leaves every work-item of an initiative green or withdrawn, and every request this context asked naming it delivered, sets the initiative to done"** (Outline, 4 Examples). Already green: the notes ran its 4 rows and all passed. `withdraw` already runs the done check. It must stay green.
- **"retry that makes an initiative's last open work-item green again sets the initiative to done"**. Red today. It fails at the initiative status step (`status_is` in `tests/scenarios/test_work_queue.py`) with `started` where `done` is expected. The cause: `retry` in `scripts/workqueue.py` makes the move but never runs `workqueue_done.becomes` or `mark`. Its commit (through `rels_of`) also lists only the work-item file and `log.jsonl`. Every step exists and runs, and the w2 step already passes.

No deprecated scenarios are retired.

## 2. Where the change lands

- `scripts/workqueue.py`: `retry` runs the done check the way `withdraw` does. Before the move it asks `workqueue_done.becomes` whether the move completes the initiative. After the move it calls `mark` when the answer is yes, and it adds the initiative's `initiative.md` to the commit in that case. It imports `workqueue_done` inside the function, as `withdraw` does, because the two modules import each other. The file has 286 lines, so the change must fit in the 14 lines left (CLAUDE.md size limit). If that is not enough, move the shared done-check-and-commit step into a helper that `withdraw` and `retry` both call. The helper stays inside `workqueue.py` or goes into `workqueue_done.py`, whose concern it is (that file has 67 lines). Behaviour stays the same either way.

These are on the change path but are not edited: `scripts/workqueue_done.py` (unless the helper goes there, as above), `scripts/work` (`cmd_retry`, see D2), `tests/scenarios/test_work_queue.py` (the scenario's steps already exist).

The researcher's set was `scripts/workqueue.py`, and it stays the same. `scripts/supervise.py` stays out (see D3). `scripts/workqueue_done.py` is added only if the helper goes there.

## 3. Decisions

- **D1: retry ends the initiative the same way withdraw does.** `retry` uses the same predicate (`becomes`), the same write (`mark`) and the same commit contents: the work-item, `log.jsonl` and `initiative.md` when it is marked. This rests on `work-queue#r23` ("a `work` command's change") and on the F5 fix the work-item names. Because the predicate is shared, r23's request rule (only requests this context asked and keeps, naming the initiative, can hold it open) applies to retry exactly as it does to withdraw. The notes' probes then go as follows. P2: this context's accepted request stays `started`. P3: another context's request ends as `done`. P4: another failed item stays `started`. P5: an initiative that is already done stays `done`.
- **D2: `work retry`'s output stays `<name> <status>`.** It does not print that the initiative ended. `withdraw` prints nothing about it either (probe P8), and the scenario only checks the files and the exit. This rests on `work-queue#r23` and on `design-decision/query-commands-answer-in-their-output`, since retry is not a query.
- **D3: the scope is `work retry` only.** `work run`'s green moves (`supervise.py` `move` and `pull_through`) are left as they are. The work-item is the F5 fix and accepts only this scenario. Whether a worker's green move through `work run` must also end the initiative is the supervision capability's concern, and none of this work-item's scenarios asks for it. The notes record it as reading 2. It is reported in the summary and not taken here.
- **D4: a missing `initiative.md` must not crash retry.** Today retry exits 0 without one (probe P6), and it must still do so. `becomes` and `mark` are used as they are, and they never raise (notes, part 5).

## 4. Tests the decisions break

None. The notes read the existing retry tests in `tests/scenarios/test_work_queue.py` (the r8 scenario, the r9 retry commit and the r23 retry) and `tests/scripts/test_work_withdraw.py`. Those tests assert the item's status, that given files are in the commit (not that no other file is), and that nothing else under `.shop/work/` differs. None of their setups completes an initiative through retry. The `failed_implementing` Given in `work_queue_git_steps.py` moves w1 to claimed, not green. The supervision tests are not touched, because D3 keeps `supervise.py` out.

## 5. Open cases

- An `initiative.md` with no `status:` line, when retry completes the initiative (probe P7). After D1, retry inherits defect D1 from the notes: `withdraw` reports success and leaves the initiative unmarked. Whether either command should refuse, write a status line or stay silent is not settled by the scenarios. The implementer names it and does not choose.
- An initiative that is already `done` when retry is run (P5). Whether `mark` rewrites it, and whether `initiative.md` then joins the commit when nothing changed.
- Retrying an item back to a status other than green, such as claimed. `becomes` should answer no, and nothing about the initiative changes. No scenario pins this.
