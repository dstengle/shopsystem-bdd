# w151 research: integrate round of a proposed initiative (r79, r84)

Tools: `tools refs` run (supervise_rounds: 0 references). `tools tests-of` and `untested`: no map, not made; test lists are `by search`. `tools size --limit 300`: none over. Probes: `.shop/scratch/w151-1-research/probe_integrate.py`, `probe_commit.py`, `conftest.py` (git identity only); run as `python3 -m pytest -q -s -n 0 <path> -p no:cacheprovider`. Stand-in claude: `.shop/scratch/w151-1-research/bin/claude`.

## 1. Why each scenario is red today

Both run as `python3 -m pytest -q "tests/scenarios/test_supervision.py::<name>"` (run).

- `a proposed initiative is given to an integrate round with the accepted lines of the request it fulfils` (r79): `StepDefinitionNotFoundError` at its first Given, line 851 "i1 is proposed and fulfils the request q1, whose lines 1 and 3 have the line outcome accepted and line 2 the line outcome refused". Missing: that step (none in tests/scenarios; `supervision_delegation_steps.py` writes `fulfils: q1` with no `## Outcomes`), and the Then at line 854 (`rounds(repo, kind)` matches only `# <kind> of p1`). Code: `supervise.py:Run.run` never starts an integrate round; `supervise_rounds.py:Rounds.due` (lines 27-34) and `AFTER` (line 12) cover capability-proposals only.
- `when work run starts the integrate round of a proposed initiative, the initiative is started` (r84): `StepDefinitionNotFoundError` at line 999 ("...whose line 1 has the line outcome accepted"). Missing: that Given and the Then at line 1002 (no step names an initiative's transition). Code: `workqueue.py:move` refuses `started` (probe P4); no code writes an initiative's status except `workqueue_done.py:mark` (to `done`).

## 2. What the system answers today

P1 (run): `python3 -m pytest -q -s -n 0 .shop/scratch/w151-1-research/probe_integrate.py -k p1`. Setup = r79/r84 Givens: i1 `status: proposed`, `fulfils: request/<ctx>/q1`, q1 `## Lines` 1-3, `## Outcomes` 1 accepted, 2 refused, 3 accepted; the base commit is the only commit. Then `work run i1` gave: `exit 0`, stdout empty, stderr empty, 0 sessions, i1 still `status: proposed`. The scenario's "every round ends" is not reached: no round is due.

P2 (run): same, plus a drafted `p1.md` (capability-proposal) and no work-item, `-k p2`. `work run i1` gave: exit 0; sessions: `initiative-round` (`1-gate`) then `bdd-branch-reviewer` (`branch-review`); stderr `work run: measure initiative i1 was refused ...` (the stand-in's session.json has no usage); log `branch review 1 of i1`, `work: p1 drafted -> awaiting-answer`, `round`. See D1.

P3 (run, in-process `supervise.Run.brief("i1", "integrate", "initiative-round", ...)`): `FileNotFoundError: .shop/work/i1/i1.md`. Brief reads `self.dir/<name>.md` (`supervise_brief.py:23-24`). See D4.

P4 (run, in-process `workqueue.move(root, "i1", "i1", "started", by="work run")`): `Refused: started is no status of the work-item lifecycle; i1 is not moved`.

P5 (run, `probe_commit.py`, in-process `Run("i1").commit("i1", "proposed", "started")` after `status: started` is written to initiative.md): `GitFailed: git commit ... failed: On branch main` (nothing staged); `git status --porcelain -- .shop/work` afterwards: ` M .shop/work/i1/initiative.md`. See D3.

Nearest cases not probed (read): a request with no `## Outcomes` section or a line with no outcome: `workqueue_request._entries` (lines 25-27) returns `[]`, so no line would count as accepted (read). `fulfils:` in the full form (`work start` writes `request/<ctx>/q1`) and the short form (`q1`, used by the Givens): both resolve in `supervise_answers.py:Answers.delegation` (rsplit on `/`) (read).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| supervise.py:Run.run, `all(s in green/withdrawn)` over `self.items()` (~l.197) | an empty list is vacuously all green: branch review and analysis follow | an integrate round commits on a zero-work-item initiative, so the same `work run` reaches branch review and `measure` (P2, D1) | unknown (no map); by search: none names a zero-item run | run P2, read |
| supervise_review.py:Reviews.unread (l.19-33), branch_review (l.35-78) | review due for any non-review commit after base | the round's merge commit counts as unread (P2) | unknown (no map) | read, run P2 |
| supervise_rounds.py:Rounds.due (l.27-34), proposals() (l.18-25) | only `kind: capability-proposal` gets a round | an initiative must also be offered a round | by search: supervision rounds tests (r68-r71, r80, r83, r85) | read |
| supervise_rounds.py:AFTER (l.12) | proposal statuses only | `proposed` -> integrate, `started` | by search: as above | read |
| supervise_rounds.py:Rounds.round, `self.move(name, before, after, asked)` (l.65) | `workqueue.move`: work-item STATUSES plus proposal statuses; writes log line | `started` is refused (P4); initiative needs its own write | by search: as above | run P4 |
| workqueue.py:STATUSES / PROPOSAL_STATUSES (l.16-19), move (l.142-167) | refuses any other status | must admit `started` for an initiative, or use a separate writer | by search: work_queue_* tests | run P4, read |
| workqueue.py:agrees, last_logged (l.123-199) | file status must agree with last log line of the name | an initiative transition written to log.jsonl under `i1` must not clash (`items()` ignores initiatives) | by search: work_queue_* tests | read |
| supervise.py:Run.commit (l.94-104) | commits `<name>.md`, `runs/<name>`, `log.jsonl` (only those that exist) | `i1.md` absent, so `initiative.md` is not committed; commit fails (P5, D3) | by search: supervision tests (work-item moves) | run P5, read |
| supervise_worker.py:Workers.brief via supervise_brief.py:Briefs.brief (l.19-61) | reads `<name>.md`, `Work-item:` line, `Work-item branch:` line unless ROUNDS | `i1.md` missing (P3, D4); integrate needs `Kind: integrate` and the accepted lines | by search: round tests (gate/apply/formulate) | run P3, read |
| supervise_worker.py:ROUNDS (l.45), TOOLS loop (l.46-48) | gate, apply, formulate get round tools | integrate must be added: tools, `with_scripts(rounds=)` (no `--work-item`) | by search: round tests | read |
| supervise_worker.py:Workers.session (l.211-219), with_scripts (l.71-83) | `--max-turns` only for research; `PYTEST_ADDOPTS --work-item` for non-rounds | an integrate round must not get `--work-item i1` | by search: round tests | read |
| workqueue_done.py:mark (l.51-56), becomes (l.41-48) | rewrites `status:` of initiative.md to done via regex | a precedent to reuse for `started` | by search: work_withdraw/resolve tests | read |
| workqueue_status.py:ENDED (l.15), open list (l.130-134); migrate_session.py | any status other than done/abandoned is listed | `started` is listed as today's `started` does | by search: work_queue_status tests | read |
| supervise_answers.py:Answers.delegation (l.34-46) | reads `fulfils` of initiative.md, delegation of request | the integrate round reads the same request; no change | by search: delegation tests | read |
| model_work.py:10 | vocabulary includes proposed, started, done, abandoned | `started` valid; no change | by search | read |

## 4. Tests the requirements make impossible to keep

`tools tests-of` has no map: list by search. No existing test runs `work run` on a `proposed` initiative: `grep proposed tests/` finds only `work_queue_start_steps.py` (work start), `migration_session_steps.py` (migrate hook) and `supervision_given.py:171` (i2 in an "elsewhere" commit, never run). Every `supervision` Background writes i1 `status: started`. So: none of the existing tests can no longer pass by the change to the proposed path. Not verified: the gate scenarios (r68-r69, r85), which will now have a branch review after their round commit only if their stand-in commits (not run). The two accepted scenarios are red at their first Given (section 1), so they say nothing about the new path.

## 5. A step the work-item skips

The integrate round, if it is written as a fourth round of `Rounds`, skips the initiative's own transition step, which only `workqueue.move` plus `Run.commit` do for a work-item:
- `workqueue.move` refuses any status not in STATUSES/PROPOSAL_STATUSES (P4), and appends `{time, work-item, before, after, by}` to log.jsonl (read, l.158-167). Effects only it produces: the log line (read by `agrees`, `retry`, `last_logged`), and the refusal that a file gets only the status the log names (read, l.186-199).
- `Run.commit` makes the commit and the push (read, l.94-104). An initiative's `initiative.md` is not among its paths: transition not committed, file left in .shop/work/ (P5, D3). The next `work run` is then refused: `check()` lists uncommitted .shop/work/ (read, supervise.py:82-86, r46).
- `supervise_worker.py:Workers.worker` runs the round's `verify_push` and log `start`/`end` lines (read): these happen for an integrate round through `worker()`, so only the transition is skipped.

## 6. Defects

### D1 zero-work-item initiative: a round's commit starts branch review and analysis
Reproduction (P2): `python3 -m pytest -q -s -n 0 .shop/scratch/w151-1-research/probe_integrate.py -k p2`. Result: exit 0; `bdd-branch-reviewer` started; `measure initiative i1` refused, printed on stderr. Cause: supervise.py `run()` (~l.197) `all()` over no work-items is True; `Reviews.unread` (supervise_review.py l.19-33) sees the round's commit. The integrate round would do the same (read): the same `work run` reaches `branch_review` after the round merges. A reading the plan must choose: vacuous truth (current code) or at least one work-item (spec r27/r75 wording "every work-item ... green").

### D2 analysis refused, exit 0
Reproduction: as D1, stderr: `work run: measure initiative i1 was refused, so there is no analysis: ... session.json is not a session.json of a shape measure knows`. Exit code 0. Observed only; with the stand-in's session.json (no usage). The exit rule for this case is r9 and r75-76; not judged.

### D3 initiative file not committed by `Run.commit`
Reproduction: `python3 -m pytest -q -s -n 0 .shop/scratch/w151-1-research/probe_commit.py`. Result: `GitFailed: git commit ... failed: On branch main`; `git status --porcelain -- .shop/work` shows ` M .shop/work/i1/initiative.md`. Not reached by any path today; latent for the new one.

### D4 `Briefs.brief` reads `<name>.md`
Reproduction: P3. `FileNotFoundError` for `.shop/work/i1/i1.md`. Not reached today; reached if an integrate round reuses `brief()` for an initiative name.

## 7. The file set

Production (paths relative to the repository):
- `scripts/supervise.py` (236; room 64): call the integrate round in `run()` before `rounds()`/`pull()`; the zero-items branch review (D1) sits in `run()`.
- `scripts/supervise_rounds.py` (76; room 224): offer an initiative `proposed` a round, `integrate` -> `started`; the transition written by a helper, not `move()`.
- `scripts/supervise_worker.py` (243; room 57): integrate in ROUNDS and TOOLS; `with_scripts(rounds=)` for it.
- `scripts/supervise_brief.py` (120; room 180): the initiative's own file (D4); `Kind: integrate`; the request's accepted lines (read from `workqueue_request`).
- `scripts/workqueue.py` (286; room 14): if the transition goes through `move()`: admit `started` for an initiative. Or leave it and write through `workqueue_done`-style code instead. Small room: any addition here must be short.
- `scripts/workqueue_done.py` (67; room 233): a `mark`-like writer of `status: started`, following `mark` (read, l.51-56).
- `scripts/workqueue_request.py` (133; room 167): a reader of accepted lines (uses `_entries`, read l.25-27).
- `scripts/supervise_review.py` (78; room 222): only if D1 is fixed here (plan's choice).
- `scripts/supervise_faults.py` (160) / `Run.commit` in supervise.py: the commit of the initiative's file (D3) if it goes through `commit()`.

Tests (paths relative to the repository):
- `tests/scenarios/supervision_rounds_steps.py` (123; room 177): the integrate Then (`# integrate of i1` heading, accepted lines) and the transition Then.
- a new module under `tests/scenarios/` for the two Givens (request with outcomes): `supervision_rounds_steps.py` may hold them too (room 177); a new module needs an import line in `tests/scenarios/test_supervision.py` (250; room 50).
- `tests/scenarios/supervision_delegation_steps.py` (108): unchanged; its Given writes no outcomes.
- `features/supervision.feature`: unchanged.

Modules on the change path, edited or not (wc): supervise.py 236, supervise_rounds.py 76, supervise_worker.py 243, supervise_brief.py 120, supervise_review.py 78, supervise_answers.py 120, supervise_faults.py 160, workqueue.py 286, workqueue_done.py 67, workqueue_request.py 133, workqueue_status.py 170, model_work.py (not counted). `tools size --limit 300`: none over.
