# Plan of w135: the intake round of an upstream request

Work-item: `.shop/work/i24-requests-and-the-context-loop/w135.md`, under supervision, accepts supervision#r67,
blocked_by w127 (green). No `## Retires`, no `## Rulings`. Planned from `runs/w135/1-research/notes.md`.

Outcome: QUESTION. Parts 1-5 are planned as far as they go. Two questions (end of part 3) are not mine to take.

## 1. What goes green

- **supervision#r67**: the outline "a request this context is the upstream of that is <status> is given to an
  intake round" (features/supervision.feature:834-846), with the examples `open` and `awaiting-upstream`.
  Red today in both examples: the first Given (:837) has no step definition (notes part 1). The second Given, the
  Then "an `initiative-round` session of the kind intake was started, given q1" and the Then "each of q1's lines
  has a line outcome, and q1's turn is its asker's" are unbound as well. Below the steps:
  - `work run` with no initiative is a usage error (notes P3, scripts/work:147).
  - Nothing in `scripts/supervise*.py` reads requests.
  - `agents/initiative-round.md` has no `intake` job.
  `work outcome` and `work turn` already produce the state the last Then asks for (notes P5).
- Deprecated scenarios retired: none.

## 2. Where the change lands

- `scripts/work`: the `run` parser's `initiative` becomes optional. `cmd_run` sends a run with no initiative to
  the no-initiative path (question 1 says how far this goes).
- `scripts/supervise.py`: `run` with no initiative runs the run-wide checks (decision 7) and then the intake pass.
  It then exits as decision 8 says. The one-initiative path is unchanged unless question 2 is answered with
  reading A. Room 82 lines; anything bigger goes in the new module.
- `scripts/supervise_intake.py` (new): selects the requests (decision 1), writes the intake brief (decision 3),
  starts the session (decision 4), checks what the session changed, brings its commits onto the checked-out branch
  and pushes (decision 5), and handles its faults (decision 6). It is a new concern, so it is a new module.
- `scripts/supervise_worker.py`: an `intake` entry in its tools table. The entry's Bash allows pytest-free
  `python3 <scripts>/work outcome *`, `work turn *` and `work show`, by path, plus the git reads the round needs.
  `initiative-round` gets an entry in its role table. If `worker()` cannot start a session without a work-item,
  the part that starts a `claude -p` session and reads how it ended moves into a helper that both paths call. The
  claude command, plugin dir, skills, transcript and cut-short detection all belong to that part. Room 71 lines.
- `scripts/supervise_faults.py`: the worktree change check (`tree_changes`) takes the paths a session may change,
  so the intake round may change q1's request file and no other file under `.shop/work/` (decision 5).
- `agents/initiative-round.md`: an `intake` job (decision 3, decision 9). The description no longer says it is
  dispatched only by integrating-a-proposal and formulating-features.
- `CLAUDE.md`: a module-map row for `scripts/supervise_intake.py`.
- `tests/scenarios/supervision_intake_steps.py` (new): the two Givens and the two Thens of the outline. The second
  Given scripts the stub's `run` steps (`work outcome` per line, then `work turn`) as the stub already allows for a
  permitted Bash (notes part 7).
- `tests/scenarios/test_supervision.py`: one import line for the new steps module.
- Not changed (notes part 7): `scripts/workqueue_request.py` and `scripts/workqueue.py`, whose `outcome`, `turn`
  and `requests` are used as they are, and `tests/scripts/stub_claude.py`.

## 3. Decisions

1. **Which requests.** The intake pass takes every request that `work` lists on the upstream side whose status is
   `open` or `awaiting-upstream`, read through `workqueue.requests`. It takes no other request (supervision#r67,
   requests#r13). One session is started per request.
2. **The intake round writes through `work`, itself.** The round runs `work outcome` for each line and `work turn`
   once. `work run` writes nothing on the request (supervision#r67 and its Implementation note,
   design-decision/requests-written-through-work). This settles the notes' Q2 as reading A. The round's Bash
   allows `work outcome`, `work turn` and `work show` by path and no other `work` command (supervision#r14: the
   scripts its stage runs). The "never `work`" comment in supervise_worker.py is reworded to say this exception.
3. **Brief.** The brief follows the stage briefs:
   - start in the worktree and never change directory (supervision#r17);
   - write the result file first with `PARTIAL` (supervision#r44);
   - the scripts directory and the worktree are named (supervision#r25), with no work-item branch.
   It names the job `intake`, the request (q1 and its file) and its lines. It also names the two commands the round
   writes with. A line the round cannot judge gets a question. The question is written as that line's outcome
   with `work outcome`, as text that is not one of `accepted`, `refused` or `withdrawn`. Under requests#r17, such
   a line makes the request `awaiting-asker` when the turn passes. No other command writes an upstream question
   today (requests#r15, #r17, design-decision/requests-written-through-work). The defect D2 in the notes is this
   path, so it is not fixed here.
4. **The session.** It is a `claude -p` session of `shopsystem-bdd:initiative-round` (supervision#r67) in a
   worktree of its own from the checked-out branch's head (supervision#r23). It is started as stage workers are:
   plugin dir (#r11), skills (#r12), no bare Write or Edit (#r13), `.shop/delivery.toml`'s `[allowed_tools]` for
   `intake` in place of its own (#r30). Before it starts, `work run` verifies the push (#r35).
5. **Where its commits go.** Under requests#r12, `work outcome` and `work turn` commit in the worktree. When the
   session ends with no fault, `work run` brings those commits onto the checked-out branch and pushes it
   (supervision#r38). The scenario's last Then reads q1 after the run, so the round's writes must be on the
   checked-out branch. Before that, the worktree is checked as for stages (supervision#r6). A change under
   `.shop/work/` other than q1's file and the round's scratch directory is put back and is a fault. So is any
   change outside `.shop/`. The main checkout's `.shop/work/` is checked when the session ends (#r28). Nothing
   else is committed: no run directory and no `log.jsonl` line, because supervision#r7 and #r8 are about
   work-items, and design-decision/requests-written-through-work keeps the request written only through `work`.
6. **A fault in the round.** These cases are faults: a session that ends in an error or at its turn limit, exits
   with an error, or leaves no JSON result (the cases of supervision#r45, by its sense); a failed push
   verification (#r39 by its sense); a forbidden change (decision 5); or a failed git command (#r41). On a fault,
   `work run` brings none of the round's commits over. It exits with an error that names the request and the fault
   (design-decision/exits-are-successful-or-errors, supervision#r10). A request has no `failed` status, so nothing
   is written on it.
7. **Run-wide checks with no initiative.** These come before any session:
   - the refusal inside a worker (supervision#r21);
   - the refusal of uncommitted `.shop/work/` changes (#r46);
   - the push of unpushed commits (#r54).
   A refusal changes nothing (#r10). The checks that need an initiative (`Run.check`'s initiative directory and
   `agrees`) are not run.
8. **Exit of a no-initiative run (until w134).** It exits successfully when every intake round ended without a
   fault and no request was to be taken in (supervision#r82's sense: no node `awaiting-answer` or `failed`). It
   exits with an error on a fault (decision 6). w134 later puts the initiatives' pass after the intake pass and
   adds their statuses to this exit.
9. **The agent's `intake` job.** The round reads `spec/` (index, decisions, capabilities) and the request. It does
   not read code (the agent's existing rule). For each line it writes an outcome or a question (decision 3),
   passes the turn, and writes its result file with the outcome and one line per line outcome. It dispatches
   nothing. It writes no ledger line, because an intake has no initiative and the ledger is per initiative.
   Its reply follows the other jobs' short form.

Questions (not taken; outcome QUESTION):

- **Q1, the no-initiative entry and w134.** The outline's When is `work run` with no initiative. That is supervision#r66,
  which w134 accepts. w134 is researched and blocked_by w146 and w136, which are drafted. w135 is blocked_by w127
  only.
  - Reading A: w135 gets `blocked_by: [work-item/w134]` and builds on w134's no-initiative driver. The narrator sees
    no intake round from any `work run` until w146, w136, w134 and then w135 are green.
  - Reading B: w135 makes `work run`'s initiative optional and runs only the intake pass when none is given
    (decisions 7, 8). w134 then adds the initiatives' pass. Both touch `scripts/work` and `scripts/supervise.py`,
    so their implementers do not run side by side (supervision#r20). The narrator sees `work run` take in upstream
    requests as soon as w135 is merged. Until w134 is green, that run takes no initiative.
- **Q2, `work run <initiative>` and requests.** r67's trigger is the request's state, with no word on which `work
  run`. The Purpose says that `work run <initiative>` takes "that initiative".
  - Reading A: every `work run`, with or without an initiative, first gives each open or awaiting-upstream upstream
    request to an intake round. The narrator running `work run i1` with q1 open sees an intake round of q1, and
    q1's outcomes are committed on i1's branch.
  - Reading B: only `work run` with no initiative starts intake rounds. The narrator running `work run i1` sees q1
    untouched, and q1 is taken in only by a `work run` with no initiative.

## 4. Tests the decisions break

None. Verified from the notes, part 4, and by reading:
- No test pins the usage error of a `work run` with no initiative. The notes searched for "the following
  arguments" and "usage".
- No test asserts by name that `work` is absent from a worker's Bash. Decision 2's exception holds for `intake`
  only.
- tests/scenarios/supervision_then_workers.py:123-126 (the researcher's exact tool list) and :162-170 (no bare
  Write or Edit) stay sound, because the research list is unchanged and decision 4 keeps r13.
- tests/scripts/test_agents.py test_r1 and test_r5 check only the agents' tools and models. The body and
  description of `initiative-round` change, but its tools and model do not, and no agent is added.
- `tree_changes` taking allowed paths (decision 5) leaves the r6/r34 scenarios as they are for stages, which pass
  only their stage directory.

## 5. Open cases

- What a no-initiative run prints about the requests it took in. No scenario of r67 checks a print.
- The order of intake rounds when several requests are taken, and whether they run side by side within
  supervision#r60's limit.
- A request with no line (notes D3), and an outcome for a line the request does not have (notes D1). These are
  `work`'s refusals (requests capability), not this work-item's. The implementer names them and does not fix them
  here.
- A round that ends `DONE` but leaves a line with no outcome, or does not pass the turn.
- Commits on the checked-out branch made by other sessions while the round worked, before the round's commits are
  brought over (decision 5).
- The scratch directory of the round (brief and result) is lost when its worktree is removed (supervision#r33).
  Nothing keeps it (decision 5).
