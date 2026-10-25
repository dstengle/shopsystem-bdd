# Plan of w192 (work-queue r31, r32)

From the research notes `.shop/work/i33/runs/w192/1-research/notes.md`.

## 1. What goes green

- **work-queue#r32**: features/work-queue.feature, Scenario Outline `add given an initiative that is <status> is refused, naming its status, and changes nothing`, examples `done` and `abandoned`.
  Red today for two reasons. The step `the add is refused because i1 is <status>, naming <status>` has no definition. And `workqueue.add()` reads no initiative status: it refuses only a missing directory. Probes A1 and A2 show the add succeeding, with exit 0, `w2` printed and w2.md written. So once the step exists, the Then fails.
- **work-queue#r31**: Scenario `withdraw that leaves every work-item of an initiative withdrawn leaves the initiative's status as it is`.
  Every step is bound. It fails at `status_is` with `'done' == 'started'`. The cause is `workqueue_done._holds`, which accepts any non-empty set of green or withdrawn work-items without asking that one of them be green. `becomes` then says done and `moved_to` marks the initiative done (probes W1, W2, W4).
- Deprecated scenarios retired: none. The work-item has no Retires section.

## 2. Where the change lands

- `scripts/workqueue.py`: `add()` reads the named initiative's `initiative.md` status. If it is `done` or `abandoned`, `add()` refuses as a `work` error (r7) naming that status, before it numbers, writes or commits anything. The file has 290 lines, so only about 10 lines are free. The read must stay small, or go through a helper already in `workqueue_done.py`; the file must not go over 300 (CLAUDE.md).
- `scripts/workqueue_done.py`: `_holds` also needs at least one work-item whose status, with `over` applied, is `green`. This one condition serves `holds` and `becomes`, so withdraw, retry, `work request resolve` and `work run`'s `set_done` all follow it.
- `tests/scenarios/work_queue_add_steps.py`: a new Then step for `the add is refused because i1 is <status>, naming <status>`. It checks a failing exit and the status word in the error output, the same way the other `refused because` steps check (for example requests_steps.py). `test_work_queue.py` imports this module whole, so it needs no edit. `nothing under the repository has changed` is already bound in test_work_queue.py.

This is the researcher's file set, unchanged.

## 3. Decisions

1. **The at-least-one-green clause goes into the shared condition, not only into withdraw.** Rests on work-queue#r31 and r23. r23 is already in spec and asks for "at least one work-item that is `green`". supervision#r105 asks `work run` for the same clause, so `set_done` going through `holds` stays faithful to it. What `work run` sees changes: an all-withdrawn initiative is no longer set done after review. r105 already requires that, so it is not a question.
2. **An initiative with no `initiative.md` is not `done` or `abandoned`, so `work add` into it goes ahead as r1 says.** Rests on the wording of work-queue#r32 ("an initiative that is `done` or `abandoned`") and on r1. The r1, r12 and r9 add scenarios use an initiative directory with no initiative.md (probe A4). Refusing there would break them, and no requirement asks for it.
3. **The refusal is a r7 error.** It exits with an error, writes nothing and makes no commit, and its message names the initiative's status. Rests on work-queue#r32 and r7. The wording beyond the status is the implementer's.
4. **Withdraw's path to done gets no records check.** Rests on work-queue#r23, which names no measurement or analysis record. The records check stays in `work run`'s own done, supervision#r105 (notes §5). This is out of scope for this work-item.

## 4. Tests the decisions break

None. What I verified, from the notes' §4 search (there is no coverage map):
- No test asserts that an all-withdrawn initiative becomes done, or that `work add` into a done or abandoned initiative succeeds.
- The tests on the green-plus-withdrawn path all have a green item, so decision 1 keeps them passing: supervision_done_steps.py, supervision_proposal_steps.py:37, supervision_tests_steps.py:99, the r23 scenarios at feature lines 69, 88 and 106, and tests/scripts/test_work_withdraw.py.
- The add scenarios with no initiative.md keep passing under decision 2.

The r31 scenario's `started` assertion is the target, and stays as written.

## 5. Open cases

- An `initiative.md` whose status is missing or unknown (neither of the two refused): the scenarios do not cover it.
- `work run`'s drafting (`supervise_draft.draft_proposals` and `fix_work_item`) into an initiative already `done` would now get the refusal. `self.draft()` sits outside the round's try in `supervise.py`. No scenario drives a done initiative being drafted, so the implementer names the case and does not choose its handling.
- `work request resolve`, `retry` and `work run` on an all-withdrawn initiative now leave it unchanged. No scenario of this work-item drives those paths.
