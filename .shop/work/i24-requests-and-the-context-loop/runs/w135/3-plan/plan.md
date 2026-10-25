# Plan of w135: the intake round of an upstream request (third plan)

Work-item: `.shop/work/i24-requests-and-the-context-loop/w135.md`, under supervision, accepts supervision#r67,
blocked_by w127 and w134 (both green). No `## Retires`, no `## Rulings`. It has two answers, dated 2026-10-25, given by the
coordinator under the person's delegation:
- **Answer 1 (reading A):** w135 builds on w134's no-initiative driver.
- **Answer 2 (reading B):** only `work run` with no initiative starts intake rounds. `work run <initiative>` takes that
  initiative alone.

Planned from `runs/w135/1-research/notes.md`. The notes are older than w134's merge. Since then the base has
`scripts/supervise_all.py` (`run_all`), `scripts/supervise_rounds.py` (the proposal rounds, run as `initiative-round`
sessions in a worktree on a `round/...` branch and merged), and a `run` parser whose initiative is optional. I read
those files and `supervise_worker.py`, `supervise.py` and `supervise_brief.py` where the notes' part 3 no longer matches
the code.

Outcome: QUESTION. Two cases the narrator would see are not settled (end of part 3). Everything else is planned.

## 1. What goes green

- **supervision#r67.** The outline "a request this context is the upstream of that is <status> is given to an intake
  round" (features/supervision.feature:834-846), with the examples `open` and `awaiting-upstream`.
  - Why it is red today, in both examples: the first Given (:837) has no step definition (notes part 1). The second
    Given and the two Thens have none either.
  - Under the steps, `run_all` reads no request, and no `intake` kind exists in `supervise_worker`'s tool table, in the
    brief or in `agents/initiative-round.md`.
  - The When, `work run` with no initiative, is no longer a usage error: w134 made the initiative optional.
  - `work outcome` and `work turn` already produce the state the last Then asks for (notes P5).
- **Deprecated scenarios retired:** none.

## 2. Where the change lands

- `scripts/supervise_intake.py` (new). The intake pass:
  - selects the requests (decision 1);
  - runs the checks that need no initiative (decision 6);
  - for each request, writes the intake brief (decision 3) and starts the round (decision 4);
  - merges the round's branch and commits its record (decision 5);
  - handles a round that faults (question 1).

  It is built on `supervise.Run` and reuses its worker, worktree, lock and limit of sessions. Its directory is
  `.shop/work/requests/` in place of an initiative's directory. It is a new concern, so it gets a new module (CLAUDE.md).
- `scripts/supervise_all.py`: `run_all` runs the intake pass before the initiatives' threads start, sharing their lock
  and limit of sessions (decision 2). It also has to run the pass when no initiative is open. Today it has 49 lines.
- `scripts/supervise_worker.py`:
  - an `intake` entry in its tool table (decision 4);
  - the comment on "no stage gets `work`" names the intake exception.

  It has 244 lines, so 56 lines of room.
- `scripts/supervise_brief.py`: `brief` hands the `intake` stage to the intake module's own brief, as it already does
  for `answer`. One branch only.
- `agents/initiative-round.md`: an `intake` job (decision 7). The description no longer says that only
  integrating-a-proposal and formulating-features dispatch the agent. It is not Python, so the size limit does not
  apply.
- `CLAUDE.md`: a module-map row for `scripts/supervise_intake.py`.
- `tests/scenarios/supervision_intake_steps.py` (new): the two Givens and the two Thens. The second Given scripts the
  stub's `run` steps for the intake session: `work outcome` for each line, then `work turn`.
- `tests/scenarios/test_supervision.py`: one import line for the new steps module.
- Removed from the researcher's set:
  - `scripts/work`. w134 already made `run`'s initiative optional and routes a run with no initiative to `run_all`.
  - `scripts/supervise.py`. `work run <initiative>` is unchanged (answer 2). The intake module subclasses `Run` and
    does not edit it.
  - `scripts/supervise_faults.py`. The intake round follows the proposal rounds, which merge a branch and do not run
    the work-item stages' `tree_changes` check (decision 5).
- Not changed: `scripts/workqueue.py` and `scripts/workqueue_request.py`. `requests`, `outcome` and `turn` are used
  as they are.

## 3. Decisions

1. **Which requests.** The pass takes each request that `workqueue.requests` lists whose status is `open` or
   `awaiting-upstream`, in the order `requests` gives them, and no other request (supervision#r67).
   - Every request `work` keeps is one this context is the upstream of: the requests capability's Implementation says
     a request is kept in its upstream's repository. So `asker` does not filter the selection, and `internal` requests
     are included.
   - The request's `turn` is not checked: r67 names only the status.
2. **Only a run with no initiative, and the pass goes first.** The pass is part of `run_all` only (answer 2). It runs
   after every initiative's `check` and before the initiatives' threads start.
   - Requests are taken one at a time, each round holding one of the shared slots (supervision#r60).
   - The order does not change what the narrator sees in the end, because no initiative node reads a request that is
     `open` or `awaiting-upstream`.
3. **Brief.** The brief follows the stage briefs:
   - it starts in the worktree and never changes directory (supervision#r17);
   - it writes the result file first, as `PARTIAL` (#r44);
   - it names the scripts directory, the base, the worktree and the round's branch (#r25). There is no work-item
     branch.

   It gives `Kind: intake`, the request's path, its lines, and the commands the round writes with: `work outcome <q>
   <n> <outcome>` and `work turn <q>`, each by the plugin's path (design-decision/requests-written-through-work). What
   it says about a line the round cannot judge waits on question 2.
4. **The session.** It is a `claude -p` session of `shopsystem-bdd:initiative-round` (supervision#r67), run through the
   existing worker. That gives it:
   - the push verification (#r35);
   - the start and end log lines;
   - `session.json` with the transcript (#r62);
   - the cut-short detection (#r45 by its sense);
   - the main checkout's `.shop/work/` check when it ends (#r28);
   - plugin dir and skills (#r11, #r12).

   It runs in a worktree of its own on a branch `round/<q>-<label>` from HEAD, as the proposal rounds do, made outside
   the plugin directory where #r23 says so.
   - Its tools are `intake`'s entry: the reader's list plus `Bash(python3 <scripts>/work outcome *)`,
     `Bash(python3 <scripts>/work turn *)` and `Bash(python3 <scripts>/work show*)`, with no other `work` command and
     no bare Write or Edit (#r13, #r14).
   - `.shop/delivery.toml`'s `[allowed_tools]` for `intake` replaces the list (#r30).
   - It gets no `--work-item` (no work-item), and its environment marks it as a worker, so a `work run` it starts
     refuses (#r21).
5. **Where the round's writes go.** `work outcome` and `work turn` commit on the round's branch in its worktree
   (requests#r12). When the round ends with no fault and `DONE`, `work run`:
   - merges that branch onto the checked-out branch and deletes it (as for rounds, #r18 by its sense);
   - commits the round's stage directory `.shop/work/requests/runs/<q>/<k>-intake/` and its log lines in
     `.shop/work/requests/log.jsonl`;
   - pushes (#r38).

   The record has to be committed: otherwise the next `work run` refuses on it (#r46). `work run` writes nothing on
   the request file itself (design-decision/requests-written-through-work). Neither `workqueue.requests`,
   `workqueue.items`, `model`'s request reading nor `workqueue_done` looks below `requests/*.md`, so the new
   `runs/` and `log.jsonl` there are invisible to them.
6. **Checks with no initiative.** When a request is due, the pass first:
   - refuses inside a worker (#r21);
   - reads `.shop/delivery.toml`;
   - refuses a detached HEAD;
   - refuses uncommitted `.shop/work/` changes, naming them (#r46);
   - pushes unpushed commits (#r54).

   A refusal changes nothing and exits with an error (#r10). When an initiative is open, its `check` has already made
   these checks. When no request is due, the pass does nothing, so a no-initiative run with no request behaves as it
   does today (#r66, #r81, #r82).
7. **The agent's `intake` job.** The round reads `spec/` (index, decisions, capabilities) and the request, and no code
   (the agent's existing rule). Then it:
   - writes `accepted`, `refused` or `withdrawn` for each line it can judge, with `work outcome`;
   - handles a line it cannot judge as question 2's answer says;
   - passes the turn once with `work turn`;
   - writes its result: the outcome and one line per line judged.

   It dispatches nothing, and it writes no `work note` ledger line, because the ledger is per initiative and an intake
   has none. Its reply follows the other jobs' short form.

### Questions (not taken: outcome QUESTION)

- **Q1, an intake round that does not end `DONE`.** The case: the round ends in an error or at its turn limit, leaves
  no readable result, fails its push verification, or gives an outcome other than `DONE`. Requirements r86-r88 cover
  such rounds only "for a capability-proposal or an initiative". r82 says a no-initiative run whose initiatives' nodes
  are all settled exits successfully. Under both readings, none of the round's commits are merged, q1 stays as it was,
  and the round's record is committed as a faulted round.
  - Reading A (as r86-r88 for the other rounds): `work run` prints the fault and exits with an error naming q1's intake
    round and how it ended, whatever the initiatives' nodes are. The other requests and the initiatives are still
    taken, as `run_all` already does for one initiative's refusal.
  - Reading B (r82 as written): `work run` prints the fault, and its exit follows r81 and r82 alone. With no initiative
    node `awaiting-answer` or `failed`, the narrator sees a successful exit, with the fault on stderr.
- **Q2, a line the intake round cannot judge.** r67 lets the round write "a question on it". The requests capability
  has no command for the upstream's questions yet (its "Not yet"), and design-decision/requests-written-through-work
  wants each part written by its own command.
  - Reading A: the round writes the question's text as that line's outcome with `work outcome`. The narrator sees the
    question under q1's `## Outcomes` on that line, and after `work turn` q1 is `awaiting-asker` (requests#r17).
  - Reading B: the round writes no outcome on that line and gives the question in its result. The narrator sees no
    outcome on that line. q1 is `awaiting-asker` after `work turn` (requests#r17), and the question is only in the
    round's record, `.shop/work/requests/runs/q1/<k>-intake/result.json`.

## 4. Tests the decisions break

None. What I checked:
- The scenarios of r66, r81 and r82 (supervision.feature:983-1100) run `work run` with no initiative. Their fixtures
  write no request (`requests` appears only in supervision_rounds_steps.py:103 and supervision_delegation_steps.py:18,
  both with an `accepted` q1 and `work run i1`). So the intake pass finds nothing and they are unchanged (decision 6).
- The r79 and delegation scenarios run `work run i1`, which starts no intake (answer 2), and their q1 is `accepted`
  anyway.
- tests/scenarios/supervision_then_workers.py:123-126 (the researcher's exact tool list) and :162-170 (no bare Write or
  Edit) stay sound. The research list does not change, and the intake list has no bare Write or Edit.
- tests/scripts/test_agents.py test_r1 and test_r5 check only the agents' tools and models.
  `initiative-round`'s body and description change, but its tools and model do not, and no agent is added.
- No test pins "no stage gets `work`" by name (notes part 4).

## 5. Open cases

- What a no-initiative run prints for the requests it took in (each request with its status after the round?). No
  scenario of r67 checks a print.
- A request that is `open` or `awaiting-upstream` but whose turn is the asker's. `work outcome` would refuse in the
  round.
- A round that ends `DONE` but leaves a line with no outcome or does not pass the turn. The next no-initiative run
  takes the request in again.
- A request with no line (notes D3), an outcome for a line the request does not have (notes D1), and an outcome word
  that is not settled (notes D2, except as question 2 reading A uses it). These are `work`'s refusals under the
  requests capability, not this work-item's.
- Commits made on the checked-out branch by another session while the round worked, before the merge.
- An intake round's merge conflicting with an initiative's commits. The pass runs before the threads, so this happens
  only across separate `work run`s.
