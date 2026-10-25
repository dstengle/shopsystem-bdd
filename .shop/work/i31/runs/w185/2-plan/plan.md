# Plan of w185: every node as far as it can go, formulate questions, proposal ids from the apply

From the research notes (`.shop/work/i31/runs/w185/1-research/notes.md`), the capability `supervision` and its
accepted scenarios in `features/supervision.feature`.

## 1. What goes green

- supervision#r111, "an initiative that a work-item's transition leaves able to be done is set done before `work run`
  ends": red on steps only. No step defines the Given "i1 is started and its work-item w1 is ready", nor the Thens
  "w1 is green" and "i1's transition to done was made after w1's transition to green, before `work run` exited". The
  code already runs set_done after the pull (supervise.py run path). Nothing past the Given was checked, so the
  implementer confirms it once the steps exist.
- supervision#r70, "a capability-proposal whose every question has an answer is given to an apply round with its
  answers": passes today. It has to stay green under decision D1 (no record of who asked means apply).
- supervision#r116, "a capability-proposal whose every question from its formulate round has an answer is given to a
  formulate round with the answers": red. Its Then "a round of the kind formulate was started for p1, given the
  answer …" has no step, because the apply_started step takes only apply. The code is also wrong: due() and the AFTER
  map send every answered awaiting-answer proposal to apply (probe D2).
- supervision#r114, "… the proposal's adds, changes and removes are written from the change list the round
  applied": red. Three Givens have no step: "… its adds naming …, given by its gate round …", "the apply round for p1
  gives DONE with a change list …" and "every other round ends …". The Then "p1's adds name … and its removes name
  nothing" has no step either. The code is also wrong: an apply round's `changes` are never read (probe D3).
- supervision#r83, "… ends without giving a question, the proposal is formulated": red. The Given "the formulate
  round for p1 gives DONE with no question" has no step. The Then is defined (rounds_steps "transition to formulated
  …"). The code is also wrong: under D1 this proposal is awaiting-answer from its formulate round, so it has to go to
  formulate, not apply.
- supervision#r112, "… gives questions, each is written under the proposal's ## Questions": red. The Given "the
  formulate round for p1 gives DONE with the questions …" has no step. The Then matches questions_hold, which unpacks
  four quoted strings and fails on two. The code is also wrong: only a gate round's questions are kept (probe D1).
- supervision#r113, "… gives a question, the proposal is awaiting-answer": red. The Given "the apply round for p1
  ends, and the formulate round for p1 gives DONE with the question …" has no step. Neither do the Thens "p1's
  transition from approved to awaiting-answer was made once the formulate round had ended" and "p1 is
  awaiting-answer" (the status step takes only "drafted"). The code is also wrong: the proposal goes to formulated and
  w2 is drafted from it (probe D1).
- supervision#r115, Scenario Outline "when the gate round of a capability-proposal <ending>, the initiative's other
  nodes are taken through their transitions before `work run` exits with an error", four examples: red. None of the
  four "the gate round for p1 <ending>, and every worker gives DONE" Givens has a step, and "w1 is green" has none.
  The code is also wrong: pull_through runs the rounds before the pull and the draft, and a Refused from a round
  skips both (probe D4: w1 stays drafted).
- Retired: "when the formulate round `work run` started for a capability-proposal ends, the proposal is formulated
  (deprecated)" (@r83 @deprecated, feature lines 1233-1240). It passes today and is deleted from the feature.

## 2. Where the change lands

- `scripts/supervise_rounds.py`: due() and the round's after-status follow the asking round (D1, D2). run_round keeps
  a formulate round's questions and moves the proposal by them (D2). After an apply round, it reads the round's
  change list and has the proposal's lists rewritten (D3).
- `scripts/supervise_change.py`: rewrites one existing proposal's `adds`, `changes` and `removes` from a change list,
  reusing the entry reading and the capability check that integrate already uses (D3).
- `scripts/supervise.py`: pull_through holds a round's Refused, takes the other nodes through (the other proposals'
  rounds, the pull, the draft, set_done), then raises it (D4). It is at 265 lines with 35 lines of room, so the
  change stays small.
- `features/supervision.feature`: delete the retired @r83 @deprecated scenario.
- `tests/scenarios/supervision_rounds_steps.py`: widen apply_started to any round kind (the r116 Then), widen the
  proposal status Then to awaiting-answer, and make questions_hold take any number of quoted questions. Lines moved
  out to the new module keep it under 300; it has 25 lines of room.
- `tests/scenarios/supervision_formulate_steps.py` (new): the Givens and Thens of r112, r113, r114, r115 and r83's
  formulate-result Given. This includes the "given by its gate round" and "given by its formulate round" wording of
  the awaiting-answer Given (D1) and "w1 is green".
- `tests/scenarios/supervision_done_steps.py`: the r111 Given "i1 is started and its work-item w1 is ready" and its
  done-after-green Then.
- `tests/scenarios/test_supervision.py`: one import of the new step module.
- `CLAUDE.md`: a row for the new module `tests/scenarios/supervision_formulate_steps.py`. The researcher's set left
  this out, but CLAUDE.md says "A new concern gets a new module and a row here". The existing row for
  `tests/scenarios/` covers step modules generally, so if the implementer judges that row enough, CLAUDE.md is left
  alone. Either way it is listed here in case it is touched.

`scripts/workqueue.py`, `scripts/supervise_brief.py` and `scripts/supervise_draft.py` are not changed. The route
reads the log's existing before/after (D1). answer_lines already goes into every brief, the formulate brief
included. draft_proposals already reads the lists in the file, and after this work those are the applied lists.

## 3. Decisions

- **D1: which round an answered proposal goes to.** The asking round is read from the proposal's last log move into
  awaiting-answer. A move from drafted means a gate round asked, and the answers go to apply (r70). A move from
  approved means a formulate round asked, and the answers go to formulate (r116). With no such move in the log, the
  route is apply, which keeps r70's scenario green: that scenario's Given writes no log line. This rests on
  supervision#r70 and supervision#r116, and on design-decision/a-ruling-returns-to-the-asking-stage, which reads the
  asking stage from the status the node moved from, the way workqueue_answer.asked_from already does. In the step
  Givens, "given by its gate round" writes a drafted → awaiting-answer move and "given by its formulate round" writes
  an approved → awaiting-answer move.
- **D2: a formulate round's status after it ends.** It depends on whether the round gave questions, not on the round
  kind. With no question, the proposal moves to formulated (supervision#r83). The move is approved → formulated, or
  awaiting-answer → formulated when the round came from D1's formulate route. With questions, each one is written
  under `## Questions` after the questions already there (supervision#r112), so they pair with answers by position
  as today. From approved, the proposal moves to awaiting-answer (supervision#r113). From awaiting-answer it stays
  awaiting-answer and only gets the new questions, so its last move into awaiting-answer is still from approved and
  D1 still routes its next answers to formulate. The writing of questions reuses the question writing that move
  already does for a gate round.
- **D3: the apply round's change list.** When an apply round ends DONE with a `changes` list, the proposal's `adds`,
  `changes` and `removes` are each replaced by that list's entries on the proposal's capability, and a list the
  round gives nothing for becomes empty (supervision#r114; the scenario's "removes name nothing"). This happens before
  the approved move, in the same commit as the round. The capability check of r107 applies to this list too, because
  r107 covers "a change list that `work run` reads": an unknown capability writes nothing and exits with an error
  naming it. When an apply round gives no change list, the proposal's lists are left as integrate wrote them (r92).
  r114 writes "from the change list the round applied", and a round that gives none applied no list to write from.
  This also keeps the r70, r71, r80 and r95 scenarios green: their stand-in apply gives no list. Unlike integrate
  (r96), a missing list is not an error.
- **D4: other nodes before the error.** In pull_through, a Refused from a round of one proposal does not stop the
  others. The remaining proposals' rounds, the pull of work-items, the drafting of formulated proposals and set_done
  all still run. After that the first Refused is raised, so the exit and message stay as r88 gives them. The failed
  round's own handling (keep_round's commit and push, no transition, status kept) is unchanged (supervision#r115,
  r86, r87, r88). r111 needs nothing beyond the existing loop and set_done after the pull. If the scenario shows a
  node left able to move, pull_through repeats until nothing moves (supervision#r111).

## 4. Tests the decisions break

- The retired @r83 @deprecated scenario is removed by the Retires section. It is not broken.
- r70 (feature 948): kept green by D1's default route. Verified in the notes: its Given writes no log line.
- r71, r80, r95 scenarios ("every round ends", apply giving no change list): kept green by D3's no-list case. The
  steps were not read beyond the notes. The implementer runs them after D3.
- r86, r87, r88 (feature 1269-1293, rounds_steps 229-244): the initiative holds only p1, so D4 has no other node to
  move and their Thens still hold (checked in the notes by reading).
- questions_hold (rounds_steps 57) is widened from four quoted strings to any number. Its existing four-string
  callers keep their meaning.
- No other test asserts that a formulate round's questions are dropped, that an apply's list is ignored, or that a
  Refused skips the pull. The notes found none by search (no tests-of map exists), and the Thens of the
  r72/r73 scenarios in supervision_proposal_steps.py write formulated files directly.

## 5. Open cases

- An apply round's change list that is unreadable (not a list of entries): whether it is refused like integrate's
  "its result cannot be read", and what status the proposal keeps then.
- An apply round's change list that names other capabilities besides the proposal's: those entries are ignored or
  refused.
- A formulate round re-run from awaiting-answer that is refused (r86, r87): the proposal stays awaiting-answer with
  its answers. Whether the next `work run` re-runs it unchanged.
- Under D4, more than one round refused in one run: whether the message names the first round only or every one.
- A formulate round giving questions while the proposal's earlier questions are not all answered cannot happen under
  due(). The scenarios are silent if it does.
- The r113 scenario: after the formulate question, the proposal has more questions than answers, so due() waits and
  no work-item is drafted from it. The implementer checks that nothing in the run drafts from it.
