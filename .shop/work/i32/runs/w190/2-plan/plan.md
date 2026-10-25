# Plan of w190 (supervision#r118, supervision#r119)

## 1. What goes green

- **supervision#r118**: "under a delegation, an answer to a reviewer's question that asks for a change makes the work-item ready again". Red today: `StepDefinitionNotFoundError` on the Given "i1's work-item w1 is awaiting-answer on its reviewer's question ..., with no answer". The When's "an answer that asks for a change" clause and the Then "w1's transition from awaiting-answer to ready was made once the session had answered" have no step either. Behind them, `Answers.answers` in `scripts/supervise_answers.py` moves the item to `workqueue_answer.asked_from`, which gives `done` for a reviewer's question, so the item would end at `done`, not `ready` (defect D1 in the notes).
- **supervision#r119**: "under a delegation, an answer to a reviewer's question that accepts the work-item as it is transitions the work-item to done". Red for the same missing Given, an unmatched "accepts ..." clause and a missing Then. The answering session's result has no change/accept verdict for `work run` to read.
- Retired scenarios: none. The work-item has no Retires section.

## 2. Where the change lands

- `scripts/supervise_answers.py`: in `answers()`, a branch for a reviewer's question that moves the item to `ready` on a change verdict and to `done` on an accept verdict, logged as the other moves of this path are. Answers to other questions still go through `asked_from`. `answer_brief` gets the instruction to give the verdict, and only in a reviewer's question's brief. `ask` reads the verdict from the result. The answer bullet and its `by` stay as r78 has them.
- `scripts/workqueue_answer.py`: the reviewer's ready/done rule now lives inside `answer`. It moves into one exported helper that takes the change/accept verdict and returns the status. `answer` and `supervise_answers.answers` both call it, so the rule exists in one place. `asked_by_reviewer` is reused as it is.
- `tests/scenarios/supervision_delegation_steps.py`: three new steps:
  - the Given of a reviewer's question with no answer, which writes a log whose last move into awaiting-answer is from `done`;
  - the When-clause Given that accepts "an answer that asks for a change" / "an answer that accepts the work-item as it is", which puts the verdict field in the stand-in plan of `delegation-answerer`;
  - the Then that reads `log.jsonl` for the move from awaiting-answer to the named status, made after the answering session's end.

  The file has 175 lines and room for these.

Removed from the researcher's set:
- `scripts/supervise.py`: decision 3 below needs no guard there.
- `tests/scenarios/supervision_answers_steps.py`: the new Given sits with the other delegation steps.

## 3. Decisions

1. **How a question counts as a reviewer's (notes C1):** by the log, as `workqueue_answer.asked_by_reviewer` reads it: the work-item's last move into awaiting-answer was from `done`. The new Given therefore writes a `done → awaiting-answer` log line, not the `drafted` one that `asked_by_the_log` writes. This rests on design-decision/an-answer-to-a-reviewer-returns-to-ready-or-done (0069). Its guard "the question was a reviewer's" is the same for `work answer` and `work run`, so both read it the same way. It also matches r98, whose findings route (`supervise_brief.findings_lines`) reads that log shape.
2. **How `work run` learns the verdict (notes C3):** from a field of the answering session's result file, with the value change or accept. It does not come from the answer text. This rests on design-decision/worker-results-are-files. The scenario answers ("No, remove the old reader.", "Yes, keep it as it is.") carry no marker, so the text cannot carry the verdict. The implementer names the field. `stub_claude.py` already passes stand-in fields through generically, so the stub does not change.
3. **What `done` leads to after an accept (notes C2):** nothing new. r2 already starts a `bdd-task-reviewer` for a `done` work-item, and r105 already keeps the initiative open while any item is not `green` or `withdrawn`. The accepted item goes through the review stage as any `done` item does, exactly as after `work answer --accept`. This rests on supervision#r2 and supervision#r119 (0069's `done`), so `scripts/supervise.py` does not change.
4. **A reviewer's question whose session gives an answer but no valid verdict** (no verdict field, or both): `work run` writes no answer and makes no move, and leaves the question for the person, as `ask` already does for an answer with a line break. This rests on 0069: neither guard holds, so no transition is allowed, and the old row to `done` is superseded. It also rests on supervision#r77: a question the session does not answer is left for the person. `work answer` refuses the same case.
5. **The `by` of the answer and of the log line:** unchanged, "work run, under the delegation". The move is not made through `workqueue_answer.answer`, whose commit and `by: work answer` would contradict r78. Rests on supervision#r78.

## 4. Tests the decisions break

None found. I checked `supervision_delegation_steps.py`: the r77/r78 scenarios write a `drafted → awaiting-answer` log, so they stay on the `asked_from` path that decision 1 leaves as it is. Their brief assertions require the delegation and the read list, and forbid `spec/` and `.shop/work/` before "Run directory:". The verdict instruction is added only to a reviewer's question's brief, and it must name neither path. The r98 scenario (`supervision_answers_steps.py`) writes its own log and does not go through `answers()` (notes §4). The `work answer` scenarios (`work_queue_answer_steps.py`) keep their behaviour after the rule moves into a helper (decision on `workqueue_answer.py`). None of this has been run, because there is no coverage map. The implementer runs those three step modules' scenarios and the whole suite.

## 5. Open cases

- A work-item whose every question is answered but whose log has no move into awaiting-answer: `asked_from` raises Refused and the run exits with an error (notes D2). The scenarios do not cover it.
- A work-item with two questions, one of them a reviewer's, answered in one run: which verdict moves it when only some questions are answered.
- A verdict given on a question that is not a reviewer's: whether it is ignored, as `workqueue_answer.answer` ignores `--change` for a `drafted` origin in the notes' probe.
- Whether the run's commit for the delegated answer also names the move in its message.
