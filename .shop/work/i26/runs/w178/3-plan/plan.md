# plan of w178

Work-item w178, under supervision, accepts supervision r100, r101, r9, r67, r82. Planned from the research notes
(`.shop/work/i26/runs/w178/1-research/notes.md`), the capability, the work-item's Answers, and the earlier plan
(`.shop/work/i26/runs/w178/2-plan/plan.md`). That plan's one open question (D1) is now answered: reading B. This plan
replaces the earlier one. Since then w177 has landed `work ask` (`workqueue_request.ask`, requests r20) on the base.

## 1. What goes green

- **supervision#r9**: "when every work-item is green or withdrawn and no request whose asker is this context is in the asker's turn, `work run` exits successfully, printing each work-item's status". Red today: the Given "a request q2 whose asker is this context, awaiting-upstream, its turn the upstream's" is undefined (StepDefinitionNotFoundError). The exit 0 needs no new code, but D2 puts the request check on this exit.
- **supervision#r101**: "when `work run` ends while a request whose asker is this context is in the asker's turn, it exits with an error, printing the request with its open questions". Red today: the Given "a request q2 kept in this context whose asker is this context, awaiting-asker, its turn the asker's, with the question … and no answer" and the Then "`work run` prints q2 with the question …" are undefined. `Run.run`/`Run.show` (supervise.py) and `run_all` (supervise_all.py) never read requests. Probes 1 and 2 show the exit is 0 or 3 and the request is not named.
- **supervision#r82**: "`work run` started with no initiative, ending with no node awaiting-answer or failed and no request whose asker is this context in the asker's turn, exits successfully …". Red today: the same undefined q2 Given as r9.
- **supervision#r67**: the outline "a request this context is the upstream of that is <status> is given to an intake round that writes each line's line outcome or a question on it", with [open] and [awaiting-upstream]. Red today: three steps are undefined. They are the Given "the intake round writes a line outcome for q1's line 1, gives a question on q1's line 2 and passes the turn with `work turn`", the Then on the brief's wording ("… its brief asking for each line's line outcome or a question on it and for the turn passed with `work turn`") and the Then "q1's line 1 has a line outcome, and q1's turn is its asker's".
- **supervision#r100**: "a question an intake round gives on a line of a request is written in the request". Red today: the Given with the quoted question "Which unit is the limit in?" and the Then "q1 holds the question … on its line 2" are undefined. `Intake.take` never reads the result's `questions`.
- **Retired** (all pass today). The work removes these scenarios from features/supervision.feature: the r9 deprecated scenario, the r67 deprecated outline ([open], [awaiting-upstream]) and the r82 deprecated scenario.

## 2. Where the change lands

- `scripts/workqueue_request.py`: a reader of the requests kept here whose asker is this context (D4) and whose status is `awaiting-asker` (D1). It gives each one with its open questions: the entries under `## Questions` that have no entry of the same number under `## Answers`. It reads the form `ask` writes ("<n>. line <line>: <question>") and adds no second question writer (D5).
- `scripts/supervise.py`: the request check at the end of a run, in `Run.show`. It prints each request it finds with its open questions and makes a successful exit an error (D2, D3).
- `scripts/supervise_all.py`: the same check at the end of `run_all`, for a run with no initiative (D2, D3).
- `scripts/supervise_intake.py`: the brief asks, for a line the round cannot judge, for a question instead of a line outcome. The round gives it in its result's `questions` as "<n>. <text>" (D6, D7). `take` writes each question with `ask` before it merges the round branch (D8).
- `tests/scenarios/supervision_request_steps.py` (new): the two q2 Givens (asker `internal`). The r101 Given writes its question in `ask`'s form under `## Questions`, with `## Answers` empty. The module also holds the Then "`work run` prints q2 with the question …".
- `tests/scenarios/supervision_intake_steps.py`: the round Givens with a question on line 2, with and without the quoted text, given through the stub result's `questions`. Also the brief Then, "q1's line 1 has a line outcome, and q1's turn is its asker's" and "q1 holds the question … on its line 2". Three steps only the retired outline uses are removed, because `tools check` (vulture) would flag them: the all-lines round Given, the exact-text `intake_started` and `lines_have_outcomes`.
- `tests/scenarios/test_supervision.py`: imports the new steps module. It has 258 lines, so 42 lines of room.
- `features/supervision.feature`: the three deprecated scenarios named in Retires are removed.

Dropped from the research file set:
- `scripts/work`: w177 has already added the question command (`work ask`).
- `scripts/workqueue.py`: only 10 lines of room are left. The new reader reads the asker and the status itself, so `requests()` keeps its 4-tuple.

## 3. Decisions

- **D1 (taken by the work-item's Answer, 2026-10-25, reading B).** "In the asker's turn" in r9, r82 and r101 counts only a request whose asker is this context and whose status is `awaiting-asker`, its negotiation still open. A settled request (accepted, refused, delivered) whose turn is the asker's leaves the exit successful and is not printed. Rests on the Answer and on supervision r9, r82, r101.
- **D2.** The check runs wherever a run ends with its print: in `Run.show` for `work run <initiative>`, and at the end of `run_all` for `work run`. Each request is printed after the work-item or initiative statuses: its name, then each open question. Rests on supervision r101 ("When `work run` ends") and r82.
- **D3.** A request the check finds turns a successful exit into an error with exit code 3, the code for awaiting an answer. An exit that is already 3 stays 3, and one that is already 1 stays 1. Rests on design-decision/exits-are-successful-or-errors and supervision r101 (its Pins: "something for the person").
- **D4.** A request's asker is this context when its `asker` is `internal` or `bounded-context/<context path>`, this context's id. Rests on supervision Implementation r101 and design-decision/capability-ids-are-context-scoped (0027). The bare-path form that workqueue_done.py:35 uses is left unchanged (part 5).
- **D5.** `work run` writes a question only through `work ask`'s library function `workqueue_request.ask`, which commits on the current branch and is refused in the asker's turn (requests r20, r12, r16). Rests on design-decision/requests-written-through-work and supervision Implementation r100.
- **D6.** The intake brief stops asking for the line outcome word `question`. A line the round questions gets no line outcome, so the round's `work turn` sets `awaiting-asker` (requests r17; `turn` does this when not every line is settled). Rests on supervision r67 ("each line's line outcome or a question on it") and requests r5.
- **D7.** The round gives each question in its result's `questions` as one string, "<n>. <text>": the line number, a full stop and a space, then the question. Rests on supervision r100 (`work run` must know which line) and the Implementation rule that a `questions` string is read as one question.
- **D8 (research C1).** On a DONE result, `take` does two things in order, both under the run lock. First, on the main checkout, it writes each question with `ask`. At that point q1 is still in the upstream's turn, because the round's `work turn` is on the round branch and not yet merged. Second, it merges the round branch. If a question write or the merge fails, the checkout is reset to its head from before the questions and the existing faulted path runs, so the request stays as it was. Rests on supervision Implementation r100 ("in the upstream's turn, before the round's `work turn`") and requests r16: a write after the merge would be refused.
- **D9 (research C3).** An intake round that leaves an `internal` request `awaiting-asker` makes r101's check count that request in the same run. No exception is made. Rests on supervision r101 together with D1. The r67 and r100 scenarios do not assert the exit.

## 4. Tests the decisions break

- The four deprecated scenario tests (r9; r67 [open] and [awaiting-upstream]; r82) are removed with their scenarios, per Retires. The steps only they use are removed with them (part 2).
- No other test breaks. The researcher's search found no test that runs `work run` with a request in the asker's turn. In the r9 and r82 scenarios q2 is `awaiting-upstream`, so `exits_successfully` still holds under D1. The requests scenarios r15, r17, r18 and w177's `ask`/`reply` scenarios are untouched, because `outcome`, `turn` and `ask` do not change (D6 changes only the brief).

## 5. Open cases (for the implementer to name in its report)

- A result question that does not start with a line number, or that names a line the request does not have. Today the only route for it is `take`'s faulted path.
- A DONE round that gives a question on a line and also writes a line outcome on the same line.
- Whether a run refused before it starts (r10, r46) also prints the requests the check finds.
- The order in which several requests and several open questions are printed.
- An `awaiting-asker` request whose questions all have answers (so no open question): printed with no questions, as r101 says.
- workqueue_done.py:35 (bare path) and measure_read.py:71 (prefixed id) read "this context" differently. D4 follows the prefixed form, and neither file is changed here.
- `work outcome` accepts any word and any line number (research D1, D2). That belongs to requests r15, not to this work.
