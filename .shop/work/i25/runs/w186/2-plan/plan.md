# Plan: w186, fix the findings of branch review 3 of i25

Work-item `.shop/work/i25/w186.md`, under work-queue, accepts work-queue#r14, #r26, #r27, #r28; findings
`.shop/work/i25/runs/branch-review/3/findings.md`. No `## Retires`, no `## Rulings`.

## 1. What goes green

None of the four is red today. The researcher ran them (notes §1): `-k "reviewer or implementers_question"` on
`tests/scenarios/test_work_queue.py` gave 6 passed. w176 (green, `a2d1083e`) delivered them.

- work-queue#r14: "answer to a researcher's, a planner's or an implementer's question transitions the work-item to the
  status that stage started from" (outline, 3 rows). Green.
- work-queue#r26: "answer that asks for a change, to a reviewer's question, transitions the work-item to ready". Green.
- work-queue#r27: "answer that accepts the work-item as it is, to a reviewer's question, transitions the work-item to
  done". Green.
- work-queue#r28: "answer to a reviewer's question that says neither whether it asks for a change nor whether it
  accepts the work-item is refused, and nothing changes". Green.

Deprecated scenarios retired: none. w176 already removed the deprecated @r14 outline (notes §4).

The implementer cannot see these red. Their job is to confirm that they are green at the work-item's base, using the
command above and the work-item check `-p work_items --work-item w186`. They write no production code for them.

## 2. Where the change lands

The file set is **empty**. No file of the repository changes for this work-item. The research set (notes §7) is only
candidates the branch review named. Each is left out for the reason given:

- `scripts/workqueue_answer.py`: the code meets r14 and r26-r28. The defect D1 refusal is not taken (decision 2). The
  dead `asked_from` call for reviewers stays: `supervise_answers.py` still uses `asked_from` (decision 3), and the
  r26-r28 scenarios do not need the call removed.
- `scripts/supervise_answers.py` (finding 3): this is supervision behaviour that no line names (decision 3).
- `scripts/supervise.py`: this would only change if `--accept` were to end the review at `green`. r27 rules that out
  (decision 1).
- `scripts/supervise_brief.py` (findings 4 and 5): these belong to w173 under supervision#r98, which this work-item
  does not accept. Finding 4 would also change the outcome a malformed log gives (a refusal instead of a crash).
- `scripts/work` (finding 6): the review triaged it "drop".
- `spec/decisions/0063-...md` (finding 2): this is a design-decision change. The review routes it through
  integrating-a-proposal, not through implementation.
- `.shop/work/i25/w176.md` (findings 1 and 7): these are edits to another work-item's record. Finding 1 is the review's
  open question to the person ("add w174's Retires entry to w176.md, or rule that the Answers sanction stands"). It is
  not a change for this work-item's implementer.
- `scripts/workqueue.py`, `scripts/workqueue_done.py`, `tests/scenarios/work_queue_answer_steps.py`,
  `tests/scenarios/test_work_queue.py`: the research listed these as read only, or as changing only if D1 changed.

## 3. Decisions

1. A reviewer's `--accept` lands `done`, as it does today. It does not land `green`. This rests on work-queue#r27,
   which names `done` as the status. The researcher's first question is settled by that line, not by a reading. The
   consequence is that the next `work run` reviews the item again (notes §3 row 3, §5). That is supervision behaviour.
   Decision 0063 (design-decision/a-ruling-returns-to-the-asking-stage, line 21) agrees that a reviewer's question
   exits to `done`.
2. An empty answer text (defect D1) is left as it is today: rc 0, with an empty Answers line. No work-queue line asks
   for a refusal, and r7 does not cover it, because an empty answer can be written. A refusal would change what the
   narrator observes. This work-item's accepted lines do not need it, so the plan takes no decision on it. It is put
   to the coordinator (summary) as a candidate line, not as a question for this work-item.
3. A delegated answer to a reviewer's question in `supervise_answers.py` still lands `done`. The second research
   question is left untaken: it is a supervision matter outside work-queue#r14/r26-r28. The branch review (finding 3)
   triaged it "not fix now; fix: a supervision line".

## 4. Tests the decisions break

None. Verified from the notes: §4 finds no live test that asserts what r26-r28 forbid. The reviewer → `done` row of
the old outline was removed by w176. `test_work_queue.py:79`, which maps a reviewer to `done` in the Given's log,
agrees with `asked_by_reviewer`. No decision above changes a file, so no other test is touched.

## 5. Open cases

These are for the coordinator and the person to name, not for the implementer:

- An empty answer (D1): refused or accepted, on every asker. No line covers it.
- `--change`/`--accept` given on a capability-proposal or on a non-reviewer's question is silently ignored (O1). The
  scenarios are silent about it. The work-queue proposal's answer 2 (a) sanctions it.
- A reviewer's `--accept` leaves the item `done`, so the next `work run` reviews it again (O2). No supervision line
  says whether an accepted review question ends the review.
- A delegated answer to a reviewer's question has no `--change`/`--accept` route (finding 3).
- `work answer` moves with `workqueue.move`, not `moved_to`, so the r23 initiative-done check does not run after an
  answer (notes §5). It has no effect today, because `ready` and `done` are neither green nor withdrawn.
