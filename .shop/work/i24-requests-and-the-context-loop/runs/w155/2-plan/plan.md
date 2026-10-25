# Plan of w155: an answering session that ends other than DONE

Work-item w155 accepts supervision#r89 and supervision#r90. Planned from the research notes (`runs/w155/1-research/notes.md`). The probes in those notes are cited by letter (A to G).

## 1. What goes green

- **supervision#r89**: "when a session started under a delegation to answer a question ends at its turn limit, the question is left unanswered for the person" (features/supervision.feature:997).
  - Red today with `StepDefinitionNotFoundError`. No step matches the Given "the session answering under the delegation ends at its turn limit, its result file answering "The queue module.", and every worker gives DONE". The only step near it is `session_answers` in `supervision_delegation_steps.py`, and it matches only "answers "X", and every worker gives DONE".
  - The production code already gives both Thens (probe A): w1 stays awaiting-answer and gets no Answers section. This scenario needs only the step.
- **supervision#r90**: "when a session started under a delegation to answer a question ends in an error, its stage directory and log lines are committed" (features/supervision.feature:1007).
  - Red today with `StepDefinitionNotFoundError`. Nothing matches the Given (ends in an error, having written notes.md beside its brief) or the two Thens: the commit of the stage directory with notes.md and of the log lines, then nothing left uncommitted.
  - With the steps in place, the code would still fail (probe B). `supervise_answers.ask` raises `Refused` on the fault before anything is committed. `answers` commits only after its loop. `supervise.run` calls `answers()` with no handler, so the run exits with `runs/w1/1-answer/` and `log.jsonl` uncommitted. The next `work run` is then refused by the r46 guard (probe C).
- Retires: none. The work-item has no `## Retires` section.

## 2. Where the change lands

- `scripts/supervise_answers.py`: on the fault path of `ask`/`answers`, commit the session's stage directory and its log lines with no transition and push them, then refuse as today. The question stays unanswered.
- `scripts/supervise.py`: changes only if the commit of a stage directory without a transition is lifted out of `keep_round` into a shared helper beside `commit`. It has room for 63 more lines. `run`'s call to `answers()` stays as it is (Decision 2).
- `scripts/supervise_rounds.py`: `keep_round` is the existing way to keep a fault's record. If its body is lifted into the shared helper, it calls that helper and its behaviour does not change. Otherwise this file is untouched.
- `tests/scenarios/supervision_delegation_steps.py`: three new steps. The Given for the turn limit with an answer in the result file. The Given for an error with notes.md beside the brief. The two r90 Thens: one checks the initiative branch has a commit holding `runs/w1/<k>-answer/` (notes.md included) and log.jsonl's start and end lines for that session; the other checks nothing of that stage directory or of log.jsonl is uncommitted.

The research set is kept as it is. `supervise_worker.py`, `supervise_faults.py`, `test_supervision.py` and `supervision_world.py` are on the path but are not expected to change. If either new Given needs a stand-in helper, it goes in `supervision_world.py`. That file has room for 127 more lines.

## 3. Decisions

1. **Keep a faulted answering session's record the way a faulted round's record is kept.**
   - Commit the session's stage directory and its `log.jsonl` lines, with no transition of the work-item, and push the commit. Clear the run's pending `own`/`unlogged` entries for that directory, as `keep_round` does.
   - Rests on: supervision#r90 (the commit), supervision#r89 (no answer written and no transition), supervision#r38 (every commit on the initiative branch is pushed) and supervision#r7 (a transition's commit; here there is no transition, so the work-item file is not touched).
   - Reuse `keep_round`'s way of doing it. Do not write a second commit routine. Lifting it into a shared helper is allowed if rounds do not change.
2. **The run still exits with an error after the record is committed, as it does today.**
   - r89 and r90 do not say whether the run goes on. Today's exit is kept, so the person sees no change beyond the commit.
   - This matches supervision#r88 for rounds and design-decision/exits-are-successful-or-errors: the stop is an error, and stderr names the session and how it ended, as the message in probes A and B already does.
   - Going on to the next question, or to other nodes, would be a new behaviour. It is not taken here.
3. **The commit covers all of r89/r90's endings**: an error, the turn limit, no readable result (probe F), and a result with an outcome other than `DONE`.
   - Each one leaves the session's stage directory and log lines committed and writes no answer.
   - Rests on the text of supervision#r89 and supervision#r90, which name all four.
   - The first three are faults and take Decision 2's exit. The plan changes nothing about whether a non-DONE outcome without a fault ends the run.
4. **A failed commit or push on this path** ends `work run` with an error saying why, not with a traceback.
   - Rests on the capability's Implementation note, "A failed commit of a fault's transition ends `work run` as r10's exit does", and on supervision#r41's spirit.
   - There is no work-item transition to make.

## 4. Tests the decisions break

None. Checked against the notes' search (section 4):
- The r77 Outline rows and the r78 scenario run only DONE paths, and Decision 1 does not touch those.
- `have_none` still holds: no Answers section, status awaiting-answer.
- The round fault scenarios (r86 to r88) only assert status and exit. If `keep_round` is lifted, its commit and push stay the same.
- No test asserts that an answering fault leaves the tree uncommitted.

The implementer should confirm by running the delegation and round-fault scenarios after the change.

## 5. Open cases

The implementer names these and does not choose them:
- The commit message of the faulted answer's record. A round uses "work: p1 gate round 1-gate faulted"; r7's form names a transition, and this commit has none.
- Two open questions under one delegation where the first session faults. Today the second is never asked, because the run stops (notes section 5). Decision 2 keeps that, and no scenario covers it.
- A DONE session that gives no answer commits "work: w1 awaiting-answer -> awaiting-answer" (D2 in the notes). That is outside r89/r90 and is left as it is.
- A session with a readable result whose outcome is `QUESTION` or `PARTIAL`, with no fault. The notes did not probe it. Under Decision 3 its record must end up committed with no answer written; whether today's code already does that (as the DONE-without-answer path does, probe E), and whether the run goes on afterwards, is for the implementer to check and name.
