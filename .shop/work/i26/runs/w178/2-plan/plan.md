# plan of w178

Work-item w178, under supervision, accepts supervision r100, r101, r9, r67, r82. Planned from the research notes
(`.shop/work/i26/runs/w178/1-research/notes.md`), the capability, decisions 0055, 0067, 0027, and w177's research
notes (w177 accepts requests r20, the question command this work uses).

One question is open (part 3, D1); the plan below is complete except for what D1 decides: which requests r101's check counts.

## 1. What goes green

- **supervision#r9**: "when every work-item is green or withdrawn and no request whose asker is this context is in the asker's turn, `work run` exits successfully, printing each work-item's status" (supervision.feature:217). Red: the Given "a request q2 whose asker is this context, awaiting-upstream, its turn the upstream's" is undefined. No code is needed for the exit 0, but D2 adds the request check to the same exit.
- **supervision#r101**: "when `work run` ends while a request whose asker is this context is in the asker's turn, it exits with an error, printing the request with its open questions" (:226). Red: the Given "a request q2 kept in this context ... with the question ... and no answer" and the Then "`work run` prints q2 with the question ..." are undefined. In the code, `Run.run`/`Run.show` (supervise.py) and `run_all` (supervise_all.py) never read requests. Probes 1 and 2: the exit is 0 or 3, and the request is not named.
- **supervision#r67**: the outline "a request this context is the upstream of that is <status> is given to an intake round that writes each line's line outcome or a question on it", [open] and [awaiting-upstream] (:887). Red: the Given "the intake round writes a line outcome for q1's line 1, gives a question on q1's line 2 and passes the turn" and both Thens ("... its brief asking for each line's line outcome or a question on it and for the turn passed with `work turn`", "q1's line 1 has a line outcome, and q1's turn is its asker's") are undefined.
- **supervision#r100**: "a question an intake round gives on a line of a request is written in the request" (:901). Red: the Given with the quoted question and the Then "q1 holds the question ... on its line 2" are undefined. In the code, `Intake.take` never reads the result's `questions`.
- **Retired** (all pass today; this work removes them from features/supervision.feature): r9 deprecated (:207-214), r67 deprecated outline (:872-886), r82 deprecated (:1270-1279).
- **supervision#r82**: "`work run` started with no initiative, ending with no node awaiting-answer or failed and no request whose asker is this context in the asker's turn, exits successfully ..." (:1282). Red: the same undefined Given as r9. `run_all` gets the request check (D2).

## 2. Where the change lands

- `scripts/workqueue_request.py`: a reader of the requests whose asker is this context and that are in the asker's turn (D1, D4), each with its open questions: the questions under `## Questions` with no n-th entry under `## Answers` (supervision Implementation r101; requests Implementation r20, r21). It reads the form w177 writes. It adds no question writer, because w177 adds that (D5).
- `scripts/supervise.py`: the request check at the end of a run, in `Run.show`. It prints each such request with its open questions and makes the exit an error (D2, D3).
- `scripts/supervise_all.py`: the same check at the end of `run_all`, for the run with no initiative (D2, D3).
- `scripts/supervise_intake.py`: the brief asks for a question instead of a line outcome on a line the round cannot judge, given in the result's `questions` as "<n>. <text>" (D6, D7). `take` writes each question with `work`'s question command before it merges the round branch (D8).
- `tests/scenarios/supervision_request_steps.py` (new): the two Givens for q2 (asker `internal`) and the Then "`work run` prints q2 with the question ...".
- `tests/scenarios/supervision_intake_steps.py`: the round Givens with a question on line 2, with and without quoted text, given through the stub's `questions`; the Then on the brief's wording; "q1's line 1 has a line outcome, and q1's turn is its asker's"; "q1 holds the question ... on its line 2". The steps used only by the retired outline are removed: the all-lines round Given, the exact-text `intake_started` and `lines_have_outcomes`. The vulture check in `tools check` would otherwise flag them as unused.
- `tests/scenarios/test_supervision.py`: import the new steps module (258 lines, 42 lines of room).
- `features/supervision.feature`: remove the three deprecated scenarios named in Retires.

These files are removed from the research file set:
- `scripts/work`: the question subcommand belongs to w177, which accepts requests r20 (D5).
- `scripts/workqueue.py`: it has 10 lines of room, and the asker is read inside the new reader, so `requests()` keeps its 4-tuple.

## 3. Decisions

- **D1 (a QUESTION; not taken).** Which requests count as "in the asker's turn" in r9, r82 and r101. Reading A: every request whose `turn` is `asker`. Reading B: only one that is `awaiting-asker` (its negotiation open). The result's `questions` gives what the narrator sees under each. Until it is answered, the plan is written for the check named by a single predicate in the reader, so either reading is a one-place change.
- **D2.** The check runs wherever a run ends with a print: `Run.show` for `work run <initiative>` and the end of `run_all` for `work run`. Each request is printed after the work-item or initiative statuses, as its name followed by each open question. This rests on supervision r101 ("When `work run` ends") and r82.
- **D3.** A request found by the check turns a successful exit into an error with code 3. An exit that is already 3 stays 3, and one that is already 1 stays 1. The run stops because it waits on an answer, and the Implementation says "3 awaiting an answer, 1 otherwise". This rests on design-decision/exits-are-successful-or-errors and supervision r101's Pins ("something for the person").
- **D4.** "This context's id" is `bounded-context/<context path>`, as spec/index.md gives it. A request's asker is this context when its `asker` is `internal` or that id. This rests on design-decision/capability-ids-are-context-scoped (0027) and supervision Implementation r101. workqueue_done.py:35 compares with the bare path; it is not changed here (part 5).
- **D5.** `work run` writes a question only through `work`'s question command and its library writer, which w177 adds (requests r20, r12, r16). This work adds no second writer. If the implementer does not find that command on the initiative branch, it stops with a question and does not write one. This rests on design-decision/requests-written-through-work (0067) and supervision Implementation r100.
- **D6.** On a line it cannot judge, the intake round gives a question instead of a line outcome. The brief stops asking for the line outcome `question`, so that line has no line outcome, and `work turn` sets `awaiting-asker` (requests r17). This rests on supervision r67 ("each line's line outcome or a question on it") and requests r5.
- **D7.** The round gives each question in its result's `questions` as one string, "<n>. <text>": the line number, a full stop and a space, then the question. This mirrors the request's numbered entries. It rests on supervision r100 (`work run` must know the line) and the Implementation rule "a result's `questions` given as one string is read as one question".
- **D8 (timing, research C1).** On a DONE result, `take` holds the run lock and does two things in order. First, on the main checkout, it writes each question with the question command (one commit each, on the current branch, requests r12). There q1 is still in the upstream's turn, because the round's `work turn` is on the round branch and not yet merged. Second, it merges the round branch. If the merge or a question write fails, the main checkout is reset to its head from before the questions. Then the existing faulted path runs, so the request "stays as it was", as `take`'s refusal already says. This rests on supervision r100 and its Implementation note ("in the upstream's turn, before the round's `work turn`") and on requests r16. Leaving the question writes until after the merge would be refused, because by then it is the asker's turn.
- **D9 (research C3).** An intake round that passes an `internal` request to the asker leaves a request that r101's check counts in the same run. This is accepted as r101 says it, with no exception for a request the round has just passed. It rests on supervision r101. The r67 and r100 scenarios do not assert the exit.

## 4. Tests the decisions break

- The four deprecated scenario tests (r9, r67 [open] and [awaiting-upstream], r82) are removed with their scenarios, per the work-item's Retires (held-scenarios). Their steps that become unused are removed (part 2).
- No other test breaks. The researcher searched for tests that run `work run` with a request in the asker's turn and found none. Under either reading of D1, the r9 and r82 scenarios have only q2, which is `awaiting-upstream` with the turn the upstream's, so `exits_successfully` still holds. The r103, r79 and accepted-request Givens write no `turn: asker`. The requests scenarios r15, r17 and r18 are untouched, because `outcome` and `turn` are not changed (D6 changes only the brief).

## 5. Open cases (for the implementer to name in its report)

- A question in the round's result that does not start with a line number, or that names a line the request does not have. Today the only route is `take`'s faulted path, which gives a refusal and leaves the request as it was.
- A DONE round that gives a question but also writes a line outcome on the same line.
- Whether a run refused before it starts (r10, r46) also prints the asker-turn requests.
- The order in which several requests and several open questions are printed.
- workqueue_done.py:35 (bare path) and measure_read.py:71 (prefixed id) read "this context" differently from each other. D4 follows the prefixed form, and neither file is changed here.
- `work outcome` accepts any word and any line number (research D1, D2). This belongs to w177 and requests r15, not to this work.
