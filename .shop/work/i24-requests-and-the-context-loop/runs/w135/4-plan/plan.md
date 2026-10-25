# Plan of w135: the intake round of an upstream request (fourth plan)

Work-item: `.shop/work/i24-requests-and-the-context-loop/w135.md`, under supervision, accepts supervision#r67,
blocked_by w127 and w134. No `## Retires`, no `## Rulings`. It has two dated answers (2026-10-25, the coordinator under
the person's delegation). They count as decisions already taken:
- **Answer 1, Q1 (reading A):** w135 builds on w134's no-initiative driver (`run_all`).
- **Answer 1, Q2 (reading B):** only `work run` with no initiative starts intake rounds. `work run <initiative>` takes
  that initiative alone.
- **Answer 2, Q1 (reading A):** an intake round that does not end `DONE` is handled as r86-r88 handle the other rounds.
  `work run` prints the fault and exits with an error naming q1's intake round and how it ended. It still takes the
  other requests and initiatives.
- **Answer 2, Q2:** for a line it cannot judge, the round writes the line outcome `question` with `work outcome`. That
  is one of the line outcomes the glossary gives (spec/index.md: accepted, rewritten, refused, question, withdrawn).
  The round gives the question's text in its result.

This plan is built from `runs/w135/1-research/notes.md` and the third plan (`runs/w135/3-plan/plan.md`). The third plan
read the code that w134 merged after the research (`supervise_all.py`, `supervise_rounds.py`, the optional initiative
in `run`'s parser). This plan keeps that plan's decisions and takes the third plan's two open questions as the answers
settle them.

## 1. What goes green

- **supervision#r67.** The scenario outline "a request this context is the upstream of that is <status> is given to
  an intake round" (features/supervision.feature:834-846), with the examples `open` and `awaiting-upstream`.
  - **Why it is red today:** in both examples the first Given (:837) has no step definition (notes part 1). The second
    Given (:838) has none either, nor do the two Thens (:840, :841).
  - **What is missing under the steps:** `run_all` reads no request. No `intake` kind exists in `supervise_worker`'s
    tool table, in the brief, or in `agents/initiative-round.md`.
  - **What already works:** the When, `work run` with no initiative, is no longer a usage error, because w134 made the
    initiative optional. `work outcome` and `work turn` already produce the state the last Then asks for (notes P5).
- **Deprecated scenarios retired:** none.

## 2. Where the change lands

- **`scripts/supervise_intake.py` (new): the intake pass.** It:
  - selects the requests (decision 1);
  - runs the checks that need no initiative (decision 6);
  - for each request, writes the intake brief (decision 3) and starts the round (decision 4);
  - merges the branch of a `DONE` round and commits the round's record (decision 5);
  - turns a round that does not end `DONE` into a fault for the exit (decision 8).

  It builds on `supervise.Run` and reuses its worker, worktree, lock and limit of sessions. Where `Run` uses an
  initiative's directory, the pass uses `.shop/work/requests/`. It is a new concern, so it gets a new module
  (CLAUDE.md).
- **`scripts/supervise_all.py`:** `run_all` runs the intake pass before the initiatives' threads start, and shares
  their lock and limit of sessions (decision 2). It runs the pass even when no initiative is open. Its exit takes
  account of the pass's faults (decision 8). It has about 49 lines today.
- **`scripts/supervise_worker.py`:**
  - an `intake` entry in the tool table (decision 4);
  - the comment that says no stage gets `work` names the intake exception.

  It has about 244 lines, so about 56 lines of room.
- **`scripts/supervise_brief.py`:** `brief` passes the `intake` stage to the intake module's own brief, as it already
  does for `answer`. This is one branch.
- **`agents/initiative-round.md`:** an `intake` job (decision 7). The description no longer says that only
  integrating-a-proposal and formulating-features dispatch the agent. The file is not Python, so the size limit does
  not apply.
- **`CLAUDE.md`:** a module-map row for `scripts/supervise_intake.py`.
- **`tests/scenarios/supervision_intake_steps.py` (new):** the two Givens and the two Thens. The second Given scripts
  the stub's `run` steps for the intake session: `work outcome` for each line, then `work turn`.
- **`tests/scenarios/test_supervision.py`:** one import line for the new steps module.
- **Removed from the researcher's set:**
  - `scripts/work`: w134 already made `run`'s initiative optional and sends a run with no initiative to `run_all`.
  - `scripts/supervise.py`: `work run <initiative>` does not change (answer 1, Q2). The intake module subclasses `Run`
    and does not edit it.
  - `scripts/supervise_faults.py`: the intake round works like the proposal rounds. Those rounds merge a branch and do
    not run the `tree_changes` check of the work-item stages (decision 5).
- **Not changed:** `scripts/workqueue.py` and `scripts/workqueue_request.py`. `requests`, `outcome` and `turn` are used
  as they are. `outcome` already writes any word, so it writes `question` too (notes D2).

## 3. Decisions

1. **Which requests.** The pass takes each request that `workqueue.requests` lists with the status `open` or
   `awaiting-upstream`, in the order `requests` gives them, and no other request (supervision#r67).
   - Every request `work` keeps is one this context is the upstream of: the requests capability's Implementation says
     a request is kept in its upstream's repository. So `asker` does not filter the selection, and `internal` requests
     are included.
   - The pass does not check the request's `turn`, because r67 names only the status.
2. **Only a run with no initiative, and the pass goes first.** The pass is part of `run_all` only (answer 1, Q2). It
   runs after every initiative's `check` and before the initiatives' threads start.
   - Requests are taken one at a time. Each round holds one of the shared slots (supervision#r60).
   - The order does not change what the narrator sees in the end, because no initiative node reads a request that is
     `open` or `awaiting-upstream`.
3. **The brief.** It follows the stage briefs:
   - the session starts in its worktree and never changes directory (supervision#r17);
   - the session writes the result file first, as `PARTIAL` (#r44);
   - the brief names the scripts directory, the base, the worktree and the round's branch (#r25), and no work-item
     branch.

   The brief also gives:
   - `Kind: intake`, the request's path and its lines;
   - the commands the round writes with, `work outcome <q> <n> <outcome>` and `work turn <q>`, each by the plugin's
     path (design-decision/requests-written-through-work);
   - the rule for a line the round cannot judge: write the line outcome `question` on it, and give the question's
     text in the result (answer 2, Q2).
4. **The session.** It is a `claude -p` session of `shopsystem-bdd:initiative-round` (supervision#r67), run through the
   existing worker. That gives it:
   - the push verification (#r35);
   - the start and end log lines;
   - `session.json` with the transcript (#r62);
   - the cut-short detection (#r45);
   - the check of the main checkout's `.shop/work/` when it ends (#r28);
   - the plugin directory and skills (#r11, #r12).

   It runs in its own worktree, on a branch `round/<q>-<label>` from HEAD, as the proposal rounds do. Where #r23 says
   so, the worktree is made outside the plugin directory.
   - **Tools:** the `intake` entry is the reader's list plus `Bash(python3 <scripts>/work outcome *)`,
     `Bash(python3 <scripts>/work turn *)` and `Bash(python3 <scripts>/work show*)`. It has no other `work` command
     and no bare Write or Edit (#r13, #r14).
   - **Override:** an `intake` key in `.shop/delivery.toml`'s `[allowed_tools]` replaces the list (#r30).
   - **No work-item:** the session gets no `--work-item`. Its environment marks it as a worker, so a `work run` it
     starts refuses (#r21).
5. **Where the round's writes go.** `work outcome` and `work turn` commit on the round's branch in its worktree
   (requests#r12). When the round ends with no fault and `DONE`, `work run`:
   - merges that branch onto the checked-out branch and deletes it (as for the other rounds);
   - commits the round's stage directory `.shop/work/requests/runs/<q>/<k>-intake/` and its log lines in
     `.shop/work/requests/log.jsonl`;
   - pushes (#r38).

   The record has to be committed, or the next `work run` refuses on it (#r46). `work run` writes nothing on the
   request file itself (design-decision/requests-written-through-work).

   The new `runs/` directory and `log.jsonl` are invisible to the request readers: `workqueue.requests`,
   `workqueue.items`, `model`'s reading of requests and `workqueue_done` all look no deeper than `requests/*.md`.
6. **Checks with no initiative.** When a request is due, the pass first:
   - refuses inside a worker (#r21);
   - reads `.shop/delivery.toml`;
   - refuses a detached HEAD;
   - refuses uncommitted `.shop/work/` changes and names them (#r46);
   - pushes unpushed commits (#r54).

   A refusal changes nothing and exits with an error (#r10). When an initiative is open, its `check` has already made
   these checks. When no request is due, the pass does nothing, so a no-initiative run with no request behaves as it
   does today (#r66, #r81, #r82).
7. **The agent's `intake` job.** The round reads `spec/` (index, decisions, capabilities) and the request, and no code
   (the agent's existing rule). Then it:
   - writes `accepted`, `refused` or `withdrawn` for each line it can judge, with `work outcome`;
   - writes `question` for each line it cannot judge, with `work outcome` (answer 2, Q2);
   - passes the turn once with `work turn`;
   - writes its result: the outcome, one line per line judged, and the text of each question with the number of its
     line.

   The job dispatches nothing. It writes no `work note` ledger line, because the ledger belongs to an initiative and
   an intake has none. Its reply follows the short form of the other jobs.

   What the narrator sees on a `question` line: `question` under q1's `## Outcomes` on that line, and q1
   `awaiting-asker` after the turn (requests#r17). The question's text is only in the round's
   `result.json`.
8. **A round that does not end `DONE`.** This covers a round that:
   - ends in an error or at its turn limit;
   - leaves no result `work run` can read;
   - fails its push verification;
   - gives an outcome other than `DONE`.

   It is handled as r86-r88 handle the other rounds (answer 2, Q1):
   - none of the round's commits is merged, so q1 stays as it was;
   - the round's record is committed as a faulted round;
   - `work run` prints the fault;
   - the other requests are still given their rounds, and the initiatives are still taken;
   - `work run` exits with an error that names q1's intake round and how it ended, whatever the initiatives' nodes
     are. This takes precedence over r82's successful exit.

## 4. Tests the decisions break

None. What I checked (from the notes and the third plan's checks, which these answers do not change):
- **r66, r81 and r82 scenarios** (supervision.feature:983-1100) run `work run` with no initiative. Their fixtures write
  no request: `requests` appears only in supervision_rounds_steps.py:103 and supervision_delegation_steps.py:18, both
  with an `accepted` q1 and `work run i1`. So the intake pass finds nothing, and decision 8 never applies to them.
- **r79 and delegation scenarios** run `work run i1`, which starts no intake (answer 1, Q2). Their q1 is `accepted`
  anyway.
- **tests/scenarios/supervision_then_workers.py:** :123-126 asserts the researcher's exact tool list and :162-170
  asserts no bare Write or Edit. Both stay sound: the research list does not change, and the intake list has no bare
  Write or Edit.
- **tests/scripts/test_agents.py:** test_r1 and test_r5 check only the agents' tools and models. `initiative-round`'s
  body and description change, but its tools and model do not, and no agent is added.
- **"No stage gets `work`":** no test pins this rule by name (notes part 4).
- **requests scenarios** (tests/scenarios/test_requests.py, requests_steps.py): they are untouched, because `work
  outcome` and `work turn` do not change.

## 5. Open cases

- What a no-initiative run prints for the requests it took in, for example each request with its status after the
  round. No r67 scenario checks a print.
- A request that is `open` or `awaiting-upstream` while its turn is the asker's. `work outcome` would refuse in the
  round, and decision 8 would make that round a fault.
- A round that ends `DONE` but leaves a line with no outcome, or does not pass the turn. The next no-initiative run
  takes the request in again.
- A request with no line (notes D3), an outcome for a line the request does not have (notes D1), and an outcome word
  outside the glossary's five (notes D2). These are refusals for `work` under the requests capability, not for this
  work-item.
- Where the question's text goes beyond the round's result, for example under the request's `## Questions`. The
  requests capability has no upstream-question command yet ("Not yet").
- Commits that another session makes on the checked-out branch while the round works, before the merge.
- An intake round's merge conflicting with an initiative's commits. The pass runs before the threads, so this can
  happen only across separate `work run`s.
