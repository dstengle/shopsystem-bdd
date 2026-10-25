# Plan of w140: work answer answers a capability-proposal's question and commits it

## 1. What goes green

- **work-queue#r24**: "answer on an awaiting-answer capability-proposal writes the answer with the date under the proposal's Answers". Red today (notes part 1): no step matches the Given "an initiative i1 under .shop/work/ whose capability-proposal p1 is awaiting-answer" (StepDefinitionNotFound, features line 260). Behind it, `work answer p1` refuses in `asked_from` (scripts/workqueue_answer.py), since log.jsonl has no transition of p1 into awaiting-answer (probe a).
- **work-queue#r9**: the outline "`work <command>` commits the change it makes to a work-item or a capability-proposal on the current branch". Its four work-item rows pass today; its row `answer p1` is red for the same missing Given, and behind it for the same refusal, and then for the commit, which always names log.jsonl (`workqueue.rels_of`) although the scenario makes none.
- Deprecated: the work-item has no Retires section, so it retires nothing. The deprecated r9 outline "`work <command>` commits the change it makes to a work-item on the current branch (deprecated)" passes today and stays passing (notes part 4).

## 2. Where the change lands

- `scripts/workqueue_answer.py`: `answer` takes a capability-proposal, known by its frontmatter `kind`. For one it checks the line and the status, writes the dated answer under `## Answers`, and commits the proposal's file alone. It makes no transition, writes no log line and does not call `asked_from`. The refusal for a target that is not awaiting-answer names the target's kind, not "work-item" only. The work-item path does not change.
- `tests/scenarios/work_queue_answer_steps.py`: the new Given "an initiative {ident} under .shop/work/ whose capability-proposal {name} is {status}". It writes `.shop/work/<ident>/<name>.md` as a capability-proposal with that status and makes no log.jsonl line. test_work_queue.py star-imports this module, so test_work_queue.py (287 lines) stays as it is.
- `scripts/work`: the help text of `answer` (line 109) says it answers an awaiting-answer work-item or capability-proposal.
- `README.md`: the `work answer` line (141) says the same.

The researcher's "may change" files that this plan leaves out:
- `scripts/workqueue.py`: D3 keeps the "if it made one" choice in workqueue_answer.py, so `rels_of`, which retry and withdraw also use, does not change. The file has only 21 lines of room.
- `scripts/model_work.py`: see section 5.

## 3. Decisions

- **D1. Answering a capability-proposal leaves its status `awaiting-answer` and makes no transition or log line.** This fixes the notes' defect D1, where probe c showed the status returned to drafted. It rests on work-queue#r24, which writes the answer only. work-queue#r14 makes a transition for a work-item only, and r4/r5 are a work-item's transitions. Under it the narrator sees p1 still awaiting-answer, with its answer written.
- **D2. A proposal needs no log.jsonl move into awaiting-answer to be answered.** The status comes from its file. This rests on work-queue#r24, whose trigger is the proposal's being awaiting-answer, and the r24 scenario's Given has no log. The `agrees` check (r6) stays in its current place before the change. A log that disagrees with the file is still refused, and a proposal with no log lines passes it.
- **D3. The commit of a proposal's answer holds the proposal's file and no log.jsonl.** It rests on work-queue#r9 ("the `log.jsonl` line the change made, if it made one") and D1. The proposal path names only its own file. The work-item path keeps committing the file and log.jsonl.
- **D4. A proposal is told from a work-item by the frontmatter `kind: capability-proposal`.** It rests on design-decision/work-file-forms, which gives every part file `kind`. Lookup stays as `workqueue.find`, which does not depend on kind.
- **D5. The one-line check (r15) stays first for both kinds.** It rests on work-queue#r15 and r7 ("change nothing"). Probe d shows it already runs first.

## 4. Tests the decisions break

None. The notes found 17 tests that run `answer()` (pytest collection, `-k answer`). 15 pass and assert work-item behaviour that the work-item path keeps unchanged under D1 to D5. The other 2 are the red targets. No test asserts the refusal text "answers only an awaiting-answer work-item" (search in the notes, part 3), so D4's change to the refusal text breaks nothing. The deprecated r9 rows and the r9 work-item rows assert the file and a clean tree, and these hold under D3. `rels_of` does not change, so the retry and withdraw tests are untouched.

## 5. Open cases

- The new Given's wording must not clash with the existing Givens "… whose work-item w3 is claimed and whose capability-proposal p1 is merged" (features line 68) and "… that is neither done nor abandoned, whose capability-proposal p1 is approved" (line 307). The implementer should check how each matches.
- The scenarios do not say what the proposal file the Given writes holds beyond kind and status. Whether it has a `## Questions` section, and whether `## Answers` exists before the answer, is left to the implementer to name.
- What `work answer` prints for a proposal. The scenarios assert only the file and the commit. The work-item path prints `<id> <status>`.
- The commit message for a proposal's answer, which has no "before -> after".
- `model_work.py`'s capability-proposal statuses do not include awaiting-answer, so `model check` would flag an awaiting-answer proposal (notes part 3). No scenario of w140 runs `model`, and the change belongs to the model's capability, not work-queue. It is left for the implementer to report, not to fix here.
- `work answer` on a capability-proposal that is not awaiting-answer (for example approved): refused under r7 (probe e). The scenarios do not pin the wording.
