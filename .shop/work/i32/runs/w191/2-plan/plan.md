# Plan of w191: fix the findings of branch review 1 of i32

w191 was drafted from branch review 1's fix-now finding 1 (`.shop/work/i32/runs/branch-review/1/findings.md`).
It accepts supervision#r118 and #r119, the requirements whose path the finding breaks.

## 1. What goes green

- supervision#r118: "under a delegation, an answer to a reviewer's question that asks for a change makes the work-item ready again".
- supervision#r119: "under a delegation, an answer to a reviewer's question that accepts the work-item as it is transitions the work-item to done".

Neither scenario is red today. The notes (part 1) record 2 passed, both run plainly and with `--work-item w191`. They must stay green.

The work is the defect the review found on their path:
- **D1:** `work run` stops with `KeyError` when a reviewer's work-item is still awaiting-answer but its every question already has a committed answer.
- Every later `work run` meets it again (notes part 6; findings finding 1).

What goes red first is a new script test for D1 (part 2), not a scenario. No scenario can be added: no requirement of w191 covers this state.

Also fixed: finding 5, ruff's FURB167 in a file the work touches.

No deprecated scenario is retired; the work-item has no Retires section.

## 2. Where the change lands

- `scripts/supervise_answers.py`, in `Answers.answers`, the reviewer branch of the move (notes: lines 80-86):
  - a work-item asked by its reviewer that has no verdict from this run's session is not moved (decision 1);
  - the verdict lookup no longer assumes one is there.
- `tests/scenarios/supervision_delegation_steps.py`: line 171, the alias `re.M` becomes `re.MULTILINE` (finding 5). No new step: no scenario is added.
- `tests/scripts/test_supervise_answers.py` (new): the regression test for D1. Added to the researcher's set because the test cannot be a scenario.
  - The module map gives `tests/scripts/` for tests of scripts that no scenario drives, and no scenario drives this state.
  - The test drives `Answers.answers` directly, as the researcher's probe B does (`.shop/scratch/w191-1-research/probe_answers.py::test_keyerror_direct_call`). It stubs the delegation, the held sections, commit, push and move.
  - The item is w1, awaiting-answer on its reviewer's question (log `done -> awaiting-answer`), with its one question already answered.
  - It asserts that no exception is raised and that no move is made (w1 stays awaiting-answer).
  - It also asserts that the answer already written is not written again and that no session is started for w1, since it has no open question.

Removed from the researcher's set: `scripts/workqueue_answer.py`. D2 is not taken (decision 3), and the reviewer rule is not shared with any new reading.

Final set: `scripts/supervise_answers.py`, `tests/scenarios/supervision_delegation_steps.py`, `tests/scripts/test_supervise_answers.py`.

All three stay under 300 lines; the notes give 142 and 202 lines for the first two.

## 3. Decisions

1. **D1 is fixed as a defect, with no new requirement (the researcher's reading b).**
   - The planner adds no line. The finding was triaged fix now and drafted into this work-item, under r118 and r119.
   - The fix is that a run with no verdict for the item makes no move.
   - Rests on: supervision#r118, #r119, and decision 0069 (an-answer-to-a-reviewer-returns-to-ready-or-done). Under 0069, `work run` makes the reviewer's transition only when the answer asks for a change (ready) or accepts the work-item (done). An answer whose verdict this run does not know meets neither guard, so no transition is made.
   - It also rests on r77, "leaves it for the person otherwise". The path where a session gives no verdict (`supervise_answers.py:119-121`) already leaves the question this way, and branch review 1 found that path sound.
   - Refusing, so that the whole run stops naming the item, is not taken: no line asks `work run` to refuse here.
2. **The verdict is not kept with the answer.**
   - Not taken: the findings' "better" fix of writing the verdict into the answer bullet or the log.
   - It would change what `work run` stores, which the narrator can see. No requirement, design-decision or ruling asks for it.
   - The two commits (answer, then move) are left as they are.
3. **D2 is not taken.** D2 is `work answer --accept` on a non-reviewer's question being accepted with the flag ignored.
   - It is `work answer`'s behaviour, not `work run`'s.
   - It is not a finding of the branch review, and neither r118 nor r119 covers it.
   - It is left as it is; it needs a line of its own if it is wanted.

## 4. Tests the decisions break

None.

- Decision 1 changes only the state where a reviewer's item has no verdict from this run. The tests the notes list (part 4) build no such state:
  - the r118 and r119 scenarios get a verdict from the stand-in;
  - the `work answer` refusals (`work_queue_answer_steps.py:19-45`) are untouched;
  - `reviewer_asked` (`supervision_answers_steps.py:40-47`) is untouched.
- The FURB167 edit does not change what the step matches.
- Decisions 2 and 3 change nothing.

## 5. Open cases

- **What `work run` ends with when the left item is the only thing in the way.**
  - w1 stays awaiting-answer with no open question, so r32's exit prints its status and no open question.
  - The person has no question left to answer with `work answer`.
  - The implementer names what the run prints and its exit code in that state, and whether the person has a way out; nothing here chooses it.
- **A reviewer's item with several questions, some answered by an earlier run and the rest by this one.** The scenarios have one question only.
- **Saving the verdict across runs (decision 2) and D2 (decision 3).** Each is for a later request if wanted.
- **Unchanged, from the review's Coupling section:** `agents/delegation-answerer.md` still does not mention `verdict`. Outside this work's file set.
