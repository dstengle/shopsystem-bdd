# Research of w163 (accepts supervision#r79, supervision#r84)

Search: no `tools map` exists, so `tests-of` and `untested` are unavailable; counts below are `by search`. `tools refs` reported 0 callers of `workqueue_request.accepted_lines`, which grep shows are 2 (module-attribute calls not followed), so refs under-reports here. Probes: `.shop/scratch/2-research/probe_integrate.py` (run with `-n 0`).

Brief's Faults item: the branch review 3 finding (no move for an integrate round that ends DONE, so `.shop/work/<init>/runs/<init>/<k>-integrate/` stays uncommitted and the next run is refused under r46). Probe A below reproduces it.

## 1. Why each scenario is red today

None is red. Command: `python3 -m pytest -q -rfE "<4 node ids>"` (node ids from `--collect-only -k integrate`), run: `4 passed in 1.95s`.

- `features/supervision.feature:849` integrate with accepted lines 1 and 3 (test_a_proposed_initiative_is_given_to_an_integrate_round...): passes. Steps: `tests/scenarios/supervision_rounds_steps.py:150`.
- `:857` no request, stays proposed, nothing left: passes (`supervision_rounds_steps.py:109`, `:121`, `:126`, `:132`, `:138`).
- `:870` request q9 not held: passes (`due()` catches `Refused`, `scripts/supervise_rounds.py:33-38`).
- `:1056` r84, started before the round: passes (`supervision_rounds_steps.py:158`; `start_initiative` at `scripts/supervise_rounds.py:86-91`, called at `:53-54`).

So the four scenarios already pass on base f890f2f. Nothing in them covers the commit gap (probe A) or the faulted-round status (probe C): no scenario asserts `.shop/work` clean after an integrate round, and none asserts `proposed` after a faulted integrate round.

## 2. What the system answers today

All probes ran with the stand-in claude (`tests/scripts/stub_claude.py`), this worktree's `scripts/work`, a fresh repo under `.shop/scratch/2-research/probe_repos/`. Stub artifacts, not defects: the `measure initiative ... refused` line on stderr (stub session.json has no usage tokens; probe repo has no `spec/index.md`).

- **A, scenario 1 Givens, integrate round DONE** — `probe_integrate.py::test_a...`, run.
  - first `work run i1`: rc 0. `git status --porcelain -- .shop/work` = `?? .shop/work/i1/runs/i1/`. initiative.md now `status: started`. Log: `work: i1 proposed -> started`, then the branch review commit. Integrate stage dir not committed.
  - second `work run i1`: rc 1, `work: .shop/work/i1/runs/i1/1-integrate/brief.md, result.json, session.json under .shop/work are not committed; commit them before work run starts`. No second round started.
- **B, request held, zero accepted lines (1,2,3 refused)** — run. rc 0. An integrate round IS started; brief has `Kind: integrate | Request: q1 | Accepted lines of the request:` with nothing after it. Read: `supervise_brief.py:66-70` gives it no empty case.
- **C, integrate round ends BLOCKED** — run. rc 1: `the integrate round of i1 (...1-integrate) gave the outcome BLOCKED, and i1 keeps its status started`. initiative.md is `started`; the round's stage dir is committed (`work: i1 integrate round 1-integrate faulted`). Second run: no integrate round started (calls list has one initiative-round start).
- **D, proposed, no `fulfils`** — run. rc 0. No integrate round; initiative stays `proposed`; no round branch. The branch review then ran (zero work-items, so `all()` is true: `supervise.py:205`).
- **Nearest, request q9 not held** — read: `due()` returns no integrate; scenario 3 covers it (passes).
- **Nearest, `fulfils` with a `/` prefix** — read: `rsplit("/",1)[-1]` in `due()` and `integrate_lines()`.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| `scripts/supervise_rounds.py:Rounds.round` (`kind != "integrate"` → `self.move`, line 83-84) | a DONE round is merged and nothing else; `move` is the only committer of `runs/<name>/` (`supervise.py:109-116`) | an integrate DONE never commits its stage dir (r7 needs a commit): probe A | by search: scenarios 1 and 4 run it; neither asserts a clean `.shop/work` | read + probe A |
| `scripts/supervise_rounds.py:Rounds.round` (DONE path, `keep_round` only on fault, lines 77-81) | the faulted path commits (`keep_round`); the DONE path does not | the same gap: the DONE path needs the commit `move` makes | by search: as above | probe A |
| `scripts/supervise_rounds.py:Rounds.due` (line 33-36) and `start_initiative` (line 53-54, 86-91) | `proposed` becomes `started` before the round's session, so a non-DONE round leaves `started` | r86 says keep the initiative's status; r84 says transition when the round starts: probe C | by search: scenario 4 only | probe C |
| `workqueue_request.accepted_lines` (`:30-35`) callers `supervise_rounds.py:35`, `supervise_brief.py:70` | a request with no accepted line gives `[]` and the round still runs | r79 "given the accepted lines": either an empty integrate or no round (reading-dependent) | by search: scenario 1 only (non-empty) | probe B |
| `scripts/supervise_rounds.py:Rounds.round` line 82 (`asked = ... if kind == "gate" else None`) | an integrate's `questions` are read and dropped | none in the requirements; an integrate's questions go nowhere | none | read |
| `scripts/model.lp:309` `w_stale_intake(I) :- status(I,"proposed"), age > 90` | a proposed initiative older than 90 days is flagged stale intake | once integrated it is `started` and no longer flagged | none (no test names `w_stale_intake`) | search |
| `scripts/supervise_all.py` (takes each initiative not `done`/`abandoned`, r66) | a proposed initiative with `fulfils` is now started by a `work run` with no initiative | new behaviour for every proposed initiative with lines | by search: no proposed-with-lines scenario outside the four | read |

## 4. Tests the requirements make impossible to keep

By search (no map). Searched `tests/` for `proposed`, `integrate`, `w_stale_intake`:

- `tests/scenarios/supervision_rounds_steps.py:96-129` (the Givens and `i1 is proposed`): still true; each is run before its round.
- Features `supervision.feature:863` and `:876` (`i1 is proposed` after no-request and q9): still true (no integrate round for either).
- `tests/scenarios/migration_session_steps.py:32,37`: `proposed` initiatives in the migrate tests, not `work run`: unaffected.
- `tests/scenarios/work_queue_start_steps.py:38-44` (a proposed capability-change initiative from `work start`): unaffected by r79/r84.
- `tests/scenarios/supervision_given.py:171` (`.shop/work/i2` proposed, in a worker's "elsewhere" commit): not in the integrate path; unaffected.

None found that can no longer pass. Verified sound: the four accepted scenarios (run, pass). "None" for the rest means I searched and found no test asserting the old behaviour.

## 5. A step the work-item skips

The integrate path skips `move` for the DONE case, and with it the commit of the round's stage dir and `log.jsonl` (r7), and the `keep_round` commit the fault path makes.

- Effect only the step produces: the commit. Without it, the next `work run` is refused (probe A, second run, rc 1). Shown by probe.
- Effect only the step produces: questions. A gate writes `## Questions` through `move`; an integrate's `questions` are dropped (`supervise_rounds.py:82`). Read.
- Effect only the step produces: push. `move` → `commit` → `push()`. An integrate DONE merge (`supervise_rounds.py:67-69`) pushes nothing; the next commit does. Read.
- `start_initiative` does commit and push (`commit(..., push=True)`): the `started` transition is the one step that does land. Probe A's log shows `work: i1 proposed -> started`.

## 6. Defects

### D1. An integrate round that ends DONE is never committed; the next `work run` is refused
Reproduce (probe A, `probe_integrate.py::test_a_done_round_then_second_run`): repo with `.shop/work/i1/initiative.md` `status: proposed`, `fulfils: q1`, request q1 with lines 1 and 3 accepted; stub plan `{"default":{"status":"DONE"},"initiative-round":{"status":"DONE"}}`.
- `python3 scripts/work run i1` → rc 0. `git status --porcelain -- .shop/work` → `?? .shop/work/i1/runs/i1/`.
- `python3 scripts/work run i1` again → rc 1: `work: .shop/work/i1/runs/i1/1-integrate/brief.md, ... not committed; commit them before work run starts`.
Matches the Faults item. Cause: `supervise_rounds.py:83-84` skips the move, so nothing commits the directory.

### D2 (reading-dependent, see §3): a faulted integrate round leaves the initiative `started`
Reproduce (probe C): same repo, plan `"initiative-round": {"status": "BLOCKED"}`. First run rc 1 `... keeps its status started`; initiative.md `status: started`; second run starts no integrate round. Reading 1 (r84 literal): correct, the transition is made when the round starts. Reading 2 (r86 "keep the initiative's status"): wrong, the status should be `proposed`. Code: `supervise_rounds.py:53-54`.

### D3 (reading-dependent, see §2 B): an integrate round runs on a request with no accepted line
Reproduce (probe B): request q1 with all three lines refused, `fulfils: q1`. rc 0; integrate round started with an empty "Accepted lines" list. Reading 1: fine (the round is given the accepted lines, none). Reading 2: should be refused like the missing-request case (no round, stays proposed).

## 7. The file set

Production (must change for the fix to pass the run, D1):
- `scripts/supervise_rounds.py` (102 lines; room 198): `Rounds.round` commits the integrate's stage dir on DONE (r7), as `keep_round` or `move` do. The same spot may hold D2/D3 if the reading is chosen.
- `scripts/supervise.py` (247; room 53): `commit` and `keep_round` are the commit helpers `round` would call; read only, edit only if the commit helper changes.

Read or edit only if D2 or D3 is chosen:
- `scripts/supervise_brief.py` (129; room 171): `integrate_lines` (r79's empty case, D3).
- `scripts/supervise_worker.py` (247; room 53): `worker` copies the stage dir (`:186`); no change needed for D1 (read).
- `scripts/workqueue_request.py` (142; room 158): `accepted_lines` (D3).

Tests and features (must change to keep D1 covered; a new scenario):
- `features/supervision.feature` (1138 lines; not a Python file; no size limit): add a scenario of r84 or r79: after a DONE integrate round `.shop/work` is clean, and a second `work run` is not refused. Per the Faults item.
- `tests/scenarios/supervision_rounds_steps.py` (242; room 58): a Then for the clean `.shop/work` after the round (existing `work_committed` at `:138` already does it: reuse it).
- `tests/scenarios/test_supervision.py` (257; room 43): auto-bound via `scenarios("supervision.feature")` (line 50); no edit needed for a new scenario.
- `tests/scenarios/supervision_world.py` (173; room 127): read only.

Modules on the change's path, edited or not, with line counts and room:
- `scripts/supervise_faults.py` 161 (room 139) — faults and `fault_of`, read.
- `scripts/supervise_all.py` 66 (room 234) — the no-initiative run (r66), read.
- `scripts/workqueue_done.py` 67 (room 233) — `mark` writes `started` (r84), read.
- `scripts/workqueue_request.py` 142 (room 158) — read.
- `scripts/work`, `scripts/workqueue.py` — not measured here; `tools size --limit 300` printed no file over 300 (ran with no output).

`size` check: `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` → no output (no tracked Python file over 300).
