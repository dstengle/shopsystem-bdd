# Research of w135: supervision#r67, intake round for an upstream request

Brief: `.shop/work/i24-requests-and-the-context-loop/w135.md`, accepts supervision#r67, under supervision, blocked_by w127.
Accepted scenario (1 outline, 2 examples): features/supervision.feature:834-846, "a request this context is the upstream of that is <status> is given to an intake round".
Tools: `tools refs` ran (names only); `tools tests-of` refused, no map (`tools map` not built): every "tests that execute" below is `by search`. `tools untested` not run.
Scripts used for probes: the worktree's `scripts/work` (same code as base). This session is itself a worker of w135's run: `SHOPSYSTEM_WORK_RUN_WORKER` is set, so probes clear it.
Probe files: `.shop/scratch/w135-1-research/probe_intake.py`, `probe_intake_edges.py`, `probe_intake_zero.py` (scratch, git-ignored; `git status --porcelain` is clean).

## 1. Why each scenario is red today

Command: `python3 -m pytest -q -n 0 -rfEx "tests/scenarios/test_supervision.py::test_a_request_this_context_is_the_upstream_of_that_is_status_is_given_to_an_intake_round[open]"` (and `[awaiting-upstream]`). Both run.
- Failure, both examples: `StepDefinitionNotFoundError` for the first Given, `a request q1 of which this context is the upstream, <status>, its turn the upstream's, with two lines` (feature line 837).
- Missing: no step text in `tests/scenarios/` matches it (search by text: "of which this context" and "upstream, " find nothing). The Given, the intake round's "writes a line outcome ... passes the turn" step (line 838), and the Then "an `initiative-round` session of the kind intake was started, given q1" (line 840) and "each of q1's lines has a line outcome" (line 841) are all unbound. Search for "initiative-round" in tests/scenarios finds none.
- Code behind it, missing: `scripts/supervise.py:run` (and `Run.run`, line 182) starts only work-item stages of one initiative. Nothing in `scripts/supervise*.py` reads requests (search: `request|upstream|intake` in `scripts/supervise*.py` finds only `supervise_faults.py:21`, "upstream's remote"). No intake kind exists: `agents/initiative-round.md` jobs are `integrate`, `gate`, `apply`, `formulate` only (read).
- Second red cause, not in the scenario's first failure but on its When: `scripts/work:147` (`r.add_argument("initiative")`) makes `work run` with no initiative a usage error (probe P3). The When "the person runs `work run`" is the r66 path, owned by w134 (accepts supervision#r66, r81, r82; status researched). See Questions.

## 2. What the system answers today

Probes run serially (`python3 -m pytest -q -s -n 0 -p no:warnings <file>`). Each line: command, result, `run`.

- P1 `work --root repo3 request "Titles" --from asker1 --lines lines.txt --source observation/o1` (repo3 has spec/index.md with a bounded-context id). Result: `q1`, commit `work request: q1`. `run`.
- P2 `work show` with q1 open upcoming upstream: `q1 open upstream`. `run`. (Probe `probe_intake.py`.)
- P3 `work run` (no initiative), with q1 open: exit 2, `usage: work run [-h] initiative ... the following arguments are required: initiative`. Same with q2 (awaiting-upstream) listed. `run`. This is the scenario's When today, and it is the "scenario's own data present" case.
- P4 `work run i1`, no initiative directory: exit 1, `the initiative i1 does not exist (no .shop/work/i1)`. `run`. (Shows `work run` with an initiative ignores requests: no request line is printed or touched; `read` of supervise.run confirms.)
- P5 `work outcome q1 1 accepted`, `work outcome q1 2 refused`, `work turn q1` (q1 in the upstream's turn): all exit 0; q1 becomes `status: accepted`, `turn: asker`, Outcomes `1. accepted`, `2. refused`. `run`. This is the post-state the scenario's last Then asks for; `work outcome`/`turn` already produce it (`scripts/workqueue_request.py:88-109`, read).
- P6 nearest cases, `probe_intake_edges.py`, serially on q1 (2 lines):
  - `work outcome q1 9 accepted`: exit 0, writes `9. accepted` under Outcomes (line 9 does not exist). `run`. See D1.
  - `work outcome q1 1 maybe`: exit 0, writes `1. maybe`. `run`. See D2.
  - `work turn q1` with no outcome written: exit 0, status `awaiting-asker`, turn `asker`. `run`.
  - `work outcome q1 1 accepted` in the asker's turn: exit 1, `q1 is in the asker's turn; the upstream writes a line outcome only in its own turn`. `run`.
  - `work request "Empty" --lines <empty file>`: exit 0, writes q2 with no lines. `run`. See D3.
  - `work outcome q9 1 accepted` (no such request): exit 1, `there is no request q9`. `run`.
- P7 `probe_intake_zero.py`: `work turn q2` on the zero-line request: exit 0, status `refused`, turn `asker`, no outcome written. `run`. See D3.
- `work run` with no initiative cannot be probed to a request effect today: it stops at argparse (P3). The intake behaviour the scenario wants (session started, given q1) has no code path at all: `read`.

## 3. Old assumptions

The requirement adds a second kind of `work run` subject (a request) and a worker that has no work-item. Each row is a place that makes an assumption the new path breaks or must extend. "tests that execute it" is `by search` (no `tools` map); `none` where no test runs the place.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/work:147 (`run` subparser, `r.add_argument("initiative")`) and `cmd_run` (scripts/work:88) | `work run` needs one initiative | the scenario's When runs `work run` with none; r66 (w134) makes it optional too | none (no test runs `work run` with no argument; usage error path untested) | read; probe P3 |
| scripts/supervise.py:run (line 217) and `Run.__init__`/`check` (lines 41, 63) | one initiative: `check` refuses a missing initiative, `items()` filters by it | intake gets no initiative; a new entry or a loop over requests is needed | tests/scenarios/test_supervision.py via `work run i1` (by search: supervision scenarios) | read; probe P4 |
| scripts/supervise_worker.py:worker (line 149) | takes a work-item: calls `verify_push(name, stage)`, `run_dir(name, stage)`, `brief(name, ...)` (reads `<initiative>/<name>.md`, supervise_brief.py:21) | an intake session is given a request, no work-item | by search: supervision stage scenarios | read |
| scripts/supervise_worker.py:ROLE (line 40) | maps agents to role names; `ROLE[agent]` in worker() (lines 178, 181, 188) | `initiative-round` is not in ROLE: a KeyError on any fault or message for it | by search: supervision fault scenarios (agents of the four stages only) | read |
| scripts/supervise_worker.py:TOOLS and STAGE_SCRIPTS (lines 28-37) with the comment "never `work`" (lines 25-27) | stage Bash = pytest, `features`, `model`, `tools`, git; `work` is excluded on purpose | the intake round must run `work outcome` and `work turn` (r67's note, `work` writes requests) | by search: tests/scenarios/supervision_then_workers.py:123-126 (researcher's exact list) and :162-170 (no bare Write/Edit) | read |
| scripts/supervise_faults.py:tree_changes (line 118) and stage() (supervise.py:145-161) | any change under `.shop/work/` outside the stage directory is a Fault and is put back (r6, r34) | requests live under `.shop/work/requests/`; `work outcome`/`turn` write there. An intake worker's writes would fault | by search: supervision faults scenarios (r6/r34, supervision.feature:160) | read |
| scripts/supervise_faults.py:checkout_changes (line 91) and Run.check's loose check (supervise.py:77-81) | the main checkout's uncommitted `.shop/work/` changes are put back (r28) or refuse the start (r46) | a request file written in the main checkout (outside a worktree) is one of these | by search: supervision.feature:808 scenario (r46) | read |
| scripts/workqueue_request.py:_change (line 47) and `workqueue.committed` (workqueue.py:253) | commits the request with `git` in `root` | an intake worker runs in its worktree, so its `work outcome` commit lands on the worktree's detached HEAD, not the initiative branch or the main checkout | by search: tests/scenarios/test_requests.py (repo run, not worktree) | read |
| scripts/supervise.py:commit (line 89) | commits only the work-item file, `runs/<name>`, `log.jsonl` (r7) | an intake round's commit is a request file, not in this list | by search: supervision commit scenarios | read |
| agents/initiative-round.md (body, lines 13-34) | jobs `integrate`, `gate`, `apply`, `formulate`; "dispatched by integrating-a-proposal and formulating-features; not for general use" | no `intake` job, no intake skill, no reply format for outcomes | none (tests/scripts/test_agents.py checks only frontmatter: r1 "only initiative-round starts an agent") | read; search for "intake" in agents/ and skills/: none |
| scripts/workqueue.py:requests (line 108) | lists requests with status and turn, by number | the intake selection (status open or awaiting-upstream, turn upstream) reads it | none found by search for a caller other than `work show` (scripts/work:47-55) | refs (0 callers: refs does not follow the extensionless `scripts/work`); search |

## 4. Tests the requirement makes impossible to keep

Searched: no `tools` map, so `tests-of` is `by search` (tests asserting the old behaviour of the functions above).
- tests/scenarios/supervision_then_workers.py:123-126 "the researcher was given --allowedTools {tools}" and :162-170 "no worker was given a bare Write or Edit": they assert the research stage's list and no bare Write. An intake stage with its own list keeps both sound. Verified by read: still passes if intake gets its own list.
- tests/scripts/test_agents.py test_r1 (only initiative-round starts an agent) and test_r5 (each agent names its model): intake keeps initiative-round as the only agent with Agent/Task, and no new agent is added. Sound by read.
- No test asserts `work` is absent from a worker's Bash list by name (search for `Bash(` and `allowedTools` in tests: only the two above and the stub). So the "never `work`" rule is held by a comment, not a test; an intake that allows `work` breaks no test. `none` for a failing test.
- No test asserts `work run` requires an initiative (search for "the following arguments" and "usage" in tests: none). `none`.
- No test asserts that a `.shop/work/` change by a worker always faults in a way an intake's would not. `none`.
So: no existing test becomes impossible to keep; the conflicts are between the requirement and the design (Questions), not with tests.

## 5. A step the work-item skips

The intake path is not a work-item stage. If the plan reuses `Workers.worker` for it, it gets these effects; if it writes a separate path, it skips them. Each is `read` (not probed; no intake path exists to probe).
- `verify_push` (supervise_faults.py:64): refuses with "could not verify that it can push the initiative branch ... before the <stage> stage" (a Fault, r39) and writes a `push verified` log line. An intake worker not using `worker()` starts without the push check (r35).
- `log` of start and end of the session (supervise_worker.py:165, 172), keyed on work-item; with the intake, no log line of the session unless added (r8).
- `session.json` with the transcript path (`with_transcript`, supervise_worker.py:171; r62); not written for an intake path unless added.
- `cut_short` (supervise_worker.py:179): a session ending in error or at its turn limit is a Fault whatever its result says (r45). An intake path that reads only `result.json` would accept a cut session.
- `checkout_changes` in the main checkout (supervise_faults.py:91, r28) and `tree_changes` in the worktree (r6): see Old assumptions. Skipping them lets a request change leave the main checkout dirty, or lets a request change commit on a worktree branch.
- `Run.check` loose-change refusal (supervise.py:77-81, r46): an intake that starts without it can run over uncommitted `.shop/work/requests/` changes.
- `push` after each commit (supervise.py:98-99, r38): a commit by an intake path that does not push is not on the remote.

## 6. Defects

Each reproduced by a probe (`run`), today's code.

### D1 `work outcome` writes an outcome for a line that does not exist
Command: `work --root <repo> outcome q1 9 accepted` on q1 with two lines.
Result: exit 0, `9. accepted` added under `## Outcomes`. Probe `probe_intake_edges.py`, `run`.
Expected by the intake rule (r67: a line outcome per line): refused.

### D2 `work outcome` accepts a word that is not an outcome
Command: `work --root <repo> outcome q1 1 maybe`.
Result: exit 0, `1. maybe` written. Then `work turn q1` sets `awaiting-asker` (not refused, not a settled word). `run`, probe `probe_intake_edges.py`.

### D3 `work request` with an empty lines file, and `turn` on it
Commands: `work --root <repo> request "Empty" --from asker2 --lines <empty file> --source observation/o2`; then `work --root <repo> turn q2`.
Result: request written with no lines (exit 0, q2); after the turn, `status: refused`, `turn: asker`, no outcome. Probes `probe_intake_edges.py` and `probe_intake_zero.py`, `run`. A request with no line is settled as refused by the upstream's turn with no line judged.

## 7. The file set

Production and test files the change must touch (or keep passing), relative to the repository. "Changes" is a plan statement.

- scripts/work: `cmd_run` and the `run` subparser's `initiative` argument, if the no-initiative path (w134's r66) is not in: the intake dispatch needs `work run` with no argument. Found by read (scripts/work:147, 88) and probe P3.
- scripts/supervise.py (218 lines): `run` starts the intake round for each open or awaiting-upstream request whose upstream this is; `Run.check` and `items` are per-initiative. Found by read.
- scripts/supervise_intake.py (new): the intake session, its brief (names q1 and its lines, the `work outcome`/`work turn` commands), its start and end log lines. New concern, so a new module (CLAUDE.md rule). Found by read (no existing module reads requests for supervision).
- scripts/supervise_worker.py (229 lines): ROLE gets `initiative-round` (or intake gets its own path); TOOLS gets an intake stage whose Bash allows `work outcome` and `work turn` only (or the plan keeps `work` out and gives the outcomes another way, see Questions). Found by read (lines 25-41, 178-188).
- scripts/supervise_faults.py (160 lines), only if the intake's `.shop/work/requests/` writes stay under the r6/r34 check: `tree_changes` exempts requests for the intake stage. Found by read (line 118).
- agents/initiative-round.md (55 lines, not Python): an `intake` job, its reply, its ledger line. Found by read (lines 13-34).
- CLAUDE.md: a module-map row for scripts/supervise_intake.py. Found by read of the module map.
- tests/scenarios/supervision_intake_steps.py (new): the Given, the intake round's writes (run steps), the two Thens. Found by search (no step text exists).
- tests/scenarios/test_supervision.py (246 lines): import of the new step module (lines 25-32). Found by read.
- Not expected to change: scripts/workqueue_request.py (131) and scripts/workqueue.py (279): `outcome`, `turn`, `requests` already do what r67 needs; the change is to who calls them. Found by read and probe P5.
- Not expected to change: tests/scripts/stub_claude.py (258): the scenario's writes can run as its `run` steps with an allowed Bash. Found by read of its header.
- Keep passing: tests/scripts/test_agents.py; tests/scenarios/test_requests.py and requests_steps.py (they run `work outcome`/`turn` in a repo); tests/scenarios/supervision_then_workers.py (research tool list).

Line counts and room under the limit (CLAUDE.md: 300 for code and test files; `wc -l`):
- scripts/work 147, room 153
- scripts/supervise.py 218, room 82
- scripts/supervise_worker.py 229, room 71
- scripts/supervise_faults.py 160, room 140
- scripts/supervise_brief.py 110, room 190 (read for the intake brief's shape; not edited)
- scripts/supervise_pool.py 142, room 158 (`pull`; not edited)
- scripts/workqueue.py 279, room 21 (`requests`, `committed`; not edited)
- scripts/workqueue_request.py 131, room 169 (not edited)
- tests/scenarios/test_supervision.py 246, room 54
- tests/scenarios/supervision_given.py 250, room 50 (not edited; read for step style)
- tests/scripts/stub_claude.py 258, room 42 (not edited)
- agents/initiative-round.md 55 lines (not Python: the limit does not apply)
- New scripts/supervise_intake.py: its room is 300 at the start.

## Questions for the plan (both readings given, not decided)

Q1. Dependency on w134. The scenario's When is `work run` with no initiative, which is r66 (w134, researched, not green). w135 is blocked_by w127 only. Reading A: w135 waits on w134's no-initiative path. Reading B: w135 adds the no-initiative entry itself and w134 does the rest. Both touch scripts/work and supervise.py run.
Q2. Worker Bash and `work`. supervise_worker.py:25-27 keeps `work` out of every worker's Bash so a worker cannot move statuses. The intake round writes through `work outcome`/`work turn` (r67's note). Reading A: allow `Bash(python3 <scripts>/work outcome *)` and `turn *` for the intake stage only. Reading B: the intake's result file names each outcome, and work run writes them through the library.
Q3. `.shop/work/` changes by a worker. r6/r34 make any worker's change there a fault, and requests are under `.shop/work/requests/`. Reading A: exempt requests for the intake stage (tree_changes). Reading B: intake writes its outcomes in the main checkout after it ends (work run writes them), so no worker change exists.
Q4. Where the intake session runs: in a worktree (worker rule, r17/r23) or in the main checkout (where the request file is). Both readings have effects in part 5.
