# w168 plan: answer named by its initiative (work-queue#r30)

## 1. What goes green

- **work-queue#r30**: features/work-queue.feature, Scenario Outline "answer named by its initiative answers the <kind> <name> of that initiative". It has two rows:
  - `capability-proposal p1` (i1 also has a capability-proposal p1 awaiting-answer);
  - `work-item w2` (i1 has work-item w1 awaiting-answer).

  Both rows are red today. `work answer i2/<name> ...` exits 1 with `there is no work-item i2/<name> under .shop/work`. The cause is that `workqueue.find` refuses any name that contains `/`, and `workqueue_answer.answer` passes it the whole `i2/<name>` (notes §1). The Given steps already pass, and no step definition is missing.

The work-item retires nothing and has no rulings.

## 2. Where the change lands

- `scripts/workqueue_answer.py`: `answer` takes a name of the form `<initiative>/<name>`. It splits the name, checks each part, finds the file in that one initiative, and passes the bare `<name>` on to `agrees`, `move`, `committed`, `asked_from` and the log line. A bare name still goes through `find` as it does today.
- `README.md` (line 141): the `work answer` entry also gives the `<initiative>/<name>` form. This is text only.

Removed from the researcher's set:
- `scripts/workqueue.py` stays unchanged. `find` keeps refusing `/` (decision 1). `entry` is only called, not changed.
- `scripts/work` stays unchanged. `cmd_answer` keeps printing the name as given (decision 3).

## 3. Decisions

1. **The split happens in `workqueue_answer.answer`, not in `workqueue.find`.** If `find` accepted `/`, `work retry` and `work withdraw` would accept `<initiative>/<name>` without any requirement asking for it. Those commands are named by a bare work-item (work-queue#r8, #r10), and only `work answer` gets the prefixed form (work-queue#r30). The choice also keeps `scripts/workqueue.py`, which has 10 lines of room, under the size limit (CLAUDE.md).
2. **Both parts are checked the way `work add` checks an initiative.** The initiative part and the name part each go through `workqueue.entry`, and the initiative must exist as a directory under `.shop/work/`. A name with no file `<name>.md` in that initiative is refused the same way `agrees` refuses a missing file today. Any failure exits with an error that says why and changes nothing (work-queue#r7). This keeps the path checks the bare form gets from `find` (notes §5), so `../i1/w1`, `i1/`, `/w1` and `i1/w1/extra` are still refused. The one-match check is unnecessary because the initiative is named, and that is what r30 is for.
3. **The printed line stays `<name as given> <status>`.** r30 does not cover what `work answer` prints, and the notes found no assertion on it. Leaving it unchanged takes no decision about what the narrator sees.
4. **The bare form stays as it is.** That includes its refusal when a name exists in more than one initiative (notes probe C1). work-queue#r13, #r24 and #r14 keep naming the bare `<work-item>` / `<capability-proposal>`.
5. Once resolved, the prefixed form behaves exactly like the bare form: the asked-from transition (r14), the line-break refusal (r15) and the commit (r9). This follows from r30, which says "shall answer", meaning the same answer.

## 4. Tests the decisions break

None. I checked the notes' search (§4): no test or feature asserts that `work answer`, `retry` or `withdraw` refuses `i<n>/<name>`, and none asserts what `work answer` prints. The bare-name answer scenarios (features/work-queue.feature 275-321, tests/scenarios/work_queue_answer_steps.py) still go through the unchanged bare path and must stay green. The notes say they were not run (pytest.ini deselected them), so the implementer runs them. No step file or test module changes. `tests/scenarios/test_work_queue.py`, which has 12 lines of room, is untouched.

## 5. Open cases

These are for the implementer to name, not to choose:
- A glob character in the name part of the prefixed form (`i1/w*`). On the bare path today, `find` globs and then refuses with "does not exist" (notes defect D1). Whether `entry` refuses glob characters is not recorded. The scenarios say nothing about it.
- A name of the prefixed form whose initiative is `done` or archived. The scenarios say nothing about it.
- How the refusal for an unknown initiative is worded (`nosuch/w1`), compared with the wording for an unknown name in a known initiative.
- Defect D1 on the bare path is reported only and is not in this work-item.
