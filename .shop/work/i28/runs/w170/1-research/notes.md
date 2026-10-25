# w170 research notes

Base 4b7dca6. Probes ran the worktree's `scripts/work` (the code at base). Tests lists: `tools tests-of` answered "no map" (no map made: `tools map` runs the whole suite), so every test list here is `by search`. Scripts: `/home/vscode/shopsystem-bdd/scripts` (`tools probe --log`: ruff 0.17.0, vulture 2.16, import-linter 2.15 present). `git status --porcelain` empty at start and at end; scratch dir not listed.

Probe files: `.shop/scratch/w170-1-research/probe_supervise.py` (R-probes), `probe_start.py` (S-probes); output `probe_out.txt`. Probe repos are under the scratch dir; the stub is `tests/scripts/stub_claude.py` via a wrapper.

## 1. Why each scenario is red today

Command for each: `python3 -m pytest -q -rfE tests/scenarios/test_supervision.py::<node>` (run; all 3 FAILED).

- **r103** `test_an_accepted_request_this_context_is_the_upstream_of_..._work_start`: `StepDefinitionNotFoundError` at the first Given, `a request q1 of which this context is the upstream, accepted, that no initiative fulfils` (feature line 1232). The existing step (`supervision_intake_steps.py:11`) needs `its turn the upstream's, with two lines`. Code missing: `scripts/supervise_all.py:run_all` never calls `workqueue_start.start` for an accepted request no initiative fulfils; its `runs` list is taken at line 19, before any start.
- **r102** `test_an_integrate_round_is_given_..._does_not_hold_...`: `StepDefinitionNotFoundError` at `spec/capabilities/thing.md on the branch i1's integrate round starts from holds thing#r1, thing#r2 and thing#r5` (line 1243). Code missing: `scripts/supervise_brief.py:integrate_lines` (lines 66-76) gives only the request's accepted lines, the drafts path and the change-list form; nothing reads other initiatives' kept drafts or compares with spec on the round's branch.
- **r104** `test_the_gate_round_of_a_capabilityproposal_..._adds_changes_or_removes`: `StepDefinitionNotFoundError` at `the capability thing holds thing#r1, thing#r2 and thing#r3` (line 1254). Code missing: `scripts/supervise_brief.py:brief`, gate branch (lines 39-41), writes a fixed sentence and no list of the proposal's ids.

Undefined Givens stop each run; the Then steps (lines 1236-1237, 1248-1249, 1259-1260) are not reached. New step definitions are needed for every Given of the three.

## 2. What the system answers today

Probe A: `python3 -m pytest -q -s .shop/scratch/w170-1-research/probe_supervise.py` (3 passed; the tests print, output in probe_out.txt). Run: `run`.

- **R103-a** `work run` (no initiative), q1 accepted, no initiative fulfils it: rc 0, no output, `.shop/work/` gets no initiative, 0 worker starts. Run.
- **R103-b** `work start q1` by hand: rc 0, prints `i1`. Run.
- **R103-c** `work run` after that: starts `# integrate of i1`, then gate of thing, apply and formulate of thing, research, plan and implement of w1 (w1 ends awaiting-answer: the probe repo has no tests, "no tests ran"; probe artifact). rc 3. Run.
- **R103-d** second `work run`: rc 3, no new starts. Run.
- Not probed (read): q1 accepted with i1 already fulfilling it (run_all does nothing for it, as R103-a); a request q2 that is `open` (not due for start).
- **R102** `work run i1` with i1 proposed fulfilling q1 (lines 1 and 2 accepted), `spec/capabilities/thing.md` holding thing#r1, r2, r5, i2 started with kept drafts `.shop/work/i2/runs/i2/1-integrate/drafts/spec/capabilities/thing.md` adding thing#r4 (and p2 formulated adding thing#r4, r5), i3 with p3 drafted adding other#r1: the integrate brief of i1 mentions none of thing#r1, thing#r2, thing#r4, thing#r5, other#r1. Run.
- **R104** `work run i1` with p1 drafted (adds thing#r4 and term/ledger, changes thing#r2, removes thing#r3) and p2 drafted (adds other#r1): the gate brief of p1 names none of thing#r1..r4, term/ledger, other#r1. Its Read list is `.shop/work/i1/p1.md` only; no spec file (a proposal has no `under:`, so `brief` reads no capability). Run.
- Not probed (read): i1 `started` with neither proposal nor item (r93) given drafts of i2.

Probe B: `python3 -m pytest -q -s .shop/scratch/w170-1-research/probe_start.py` (4 passed). Run; these are the probes of the `work start` step r103 would reuse (part 5).

## 3. Old assumptions

Function reads: `grep`/`tools refs` not run for these names; the list is from reading the callers (`supervise_all.run_all` -> `Run.pull_through`, `supervise_rounds.due`, `supervise_brief.brief`).

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| supervise_all.py:run_all, lines 19-21 | the initiatives taken are those open when `work run` starts; `run.check()` for each before anything moves (r10) | r103 starts an initiative for an accepted request before `runs` is taken, so the new one is taken by the same run; the start must come after the checks | by search: features lines 849, 858, 1209, 1225, 1235 (scenario bodies read: no accepted unfulfilled request except r103's); 1055, 1148 not read | read |
| workqueue_start.py:start, lines 22-53 | written by `work start` only (scripts/work:83-84); no check of the worker marker, the detached HEAD, a second initiative for the same request; commits without a push | r103's path reuses it inside `work run`, which must refuse what `run` refuses (part 5) | by search: tests/scenarios/work_queue_start_steps.py (accepted q1, one new initiative); stays green | by search |
| supervise_rounds.py:due, lines 35-41 | a `proposed` initiative (or `started` with nothing) gets an integrate round; `fulfils` matched by `rsplit("/",1)[-1]` | a started-by-run initiative is `proposed`, so it gets its integrate round as a hand-started one does (R103-c) | by search: supervision_rounds_steps.py and supervision_integrate_steps.py | read |
| supervise_brief.py:integrate_lines, lines 66-76 | the integrate round is given its request's accepted lines, the drafts path, the change-list form | r102 adds ids that other initiatives' kept drafts add and spec on the round's branch lacks; none else | tests: supervision_rounds_steps.py:171 `integrate_started` (asserts "Line 2 text." absent) — still passes | read |
| supervise_brief.py:brief, gate branch, lines 39-41 | the gate's brief is one fixed sentence; read list is the proposal file, and a spec file only when `under` is set (proposals have none) | r104 names the proposal's adds, changes, removes and terms in the brief; asks nothing on other ids | tests: supervision_rounds_steps.py:74-78 `gate_brief_asks` (asserts "questions", "readings", "recommended") — still passes | read |
| supervise_brief.py:brief, read list, lines 26-31 | a round reads `spec/capabilities/<under>.md` only when the item has `under` | the r104 Given puts capability thing's requirements in the scenario; whether the gate reads spec is open (reading A: the brief lists the ids; B: the gate reads the capability too) | none: no test asserts the gate's read list | read |
| supervise_change.py:write_proposals, lines 38-52 | writes proposal frontmatter `argues`, `adds`, `changes`, `removes` (lists) and no `under` | the ids the gate and r102 read come from here; form unchanged | tests: supervision_integrate_steps.py:76-90 `proposals_written` (asserts the lists) — sound, unchanged | by search + read |
| supervise_draft.py:draft_proposals, line 46 | reads `adds` and `changes` of formulated proposals | unchanged | by search: supervision_proposal_steps.py | read |

## 4. Tests the requirements make impossible to keep

`tools tests-of` had no map; the lists are `by search`.

- Tests driving `work run` with no initiative (features 849, 858, 1209, 1225, 1235) and the Givens of their scenarios: none has an accepted request that no initiative fulfils except r103's. Sound: no test can fail by r103's start. Not read: features 1055 and 1148 (their scenario bodies not read).
- `supervision_rounds_steps.py:74-78` (gate brief asks the gate as questions): reads the brief for three words; adding the id list keeps it true. Sound.
- `supervision_rounds_steps.py:160-176` (`second_not_refused`, `integrate_started`): the latter asserts "Line 2 text." is absent from the integrate brief; r102 adds only ids, and no scenario of i1's there has other drafts. Sound.
- `supervision_integrate_steps.py:76-90` (`proposals_written`): asserts the proposal's list fields as written; unchanged form. Sound.
- `work_queue_start_steps.py` (`work start` of accepted q1, one new initiative): `work start` is not changed by the plan's rule as read, so sound. Note S2 (a second initiative for the same request) is not asserted by any test (by search).
- Nothing else found that asserts the old behaviour (search: `Give the gate`, `Accepted lines`, `Drafts path`, `accepted` in tests/scenarios and tests/scripts).

## 5. A step the work-item skips

The step is `work start`'s (`workqueue_start.start`) as `work run` would take it. Probed the existing way (`work start`, probe B):

- Worker marker: `work start` runs under `SHOPSYSTEM_WORK_RUN_WORKER=w0` (`supervise_worker.py:59`, refused by `Run.check` supervise.py:73-75 and `Intake.check`): **creates i1** (S1). `run` refuses the same env (S1b). Run.
- Detached HEAD: `Run.check` refuses (supervise.py:82-84); `work start` **commits on the detached HEAD** (S3, log `5ce2f42 work: start i1, fulfilling q1`). `work run i1` then refuses (S3b). Run.
- Push: `work start` pushes nothing: HEAD ahead of origin/main after it (S4, pushed=False). Run; the later push is `push_unpushed` in run_all (read: supervise_all.py:33).
- Loose `.shop/work/` changes: `Run.check` refuses (supervise.py:85-89); `work start` commits only its own file (`workqueue.committed`, workqueue.py:264-278) and does not refuse. Read.
- Second initiative for a request: none (S2). Run.
- Effects only `work start` produces: a commit `work: start i<n>, fulfilling q<n>` of `.shop/work/i<n>/initiative.md`; the number is `_highest`+1 (workqueue_start.py:10-19). Refusals only it produces: `there is no request`, `is <status>, not accepted`, `spec/index.md ... is missing` and `gives no bounded-context id` (workqueue.py:42-46), `not a name` (workqueue.py:58-61). Read.

## 6. Defects

D1. `work start` makes an initiative inside a worker.
Repro: repo with `.shop/work/requests/q1.md` accepted; `SHOPSYSTEM_WORK_RUN_WORKER=w0 python3 scripts/work --root <repo> start q1` -> prints `i1`, rc 0. Then `... run` with the same env -> `work: it was started by a worker of another work run (of w0)`, rc 1. (probe S1, S1b)

D2. `work start` twice for one request makes two initiatives fulfilling it.
Repro: `work start q1` -> `i1` rc 0; `work start q1` -> `i2` rc 0; both initiative.md hold `fulfils: request/probe/q1`. (probe S2)

D3. `work start` on a detached HEAD commits there.
Repro: `git checkout --detach`; `work start q1` -> `i1`, rc 0, commit on the detached HEAD; `work run i1` -> `HEAD is detached`. (probe S3, S3b)

## 7. The file set

Production files (to change):
- scripts/supervise_all.py (67 lines; room 233): run_all calls the start for each accepted request no initiative fulfils, after the checks and before `runs` is taken (r103).
- scripts/supervise_brief.py (135; room 165): integrate_lines adds the ids of other initiatives' kept drafts that spec/ on the round's branch lacks (r102); brief gate branch lists the proposal's adds, changes, removes and terms (r104).
- scripts/supervise_rounds.py (134; room 166): run_round's integrate branch passes the ids (r102) — or the brief computes them itself.
- scripts/workqueue_start.py (53; room 247): only if the `work run` path must refuse what `work start` lets through (D1-D3); otherwise none. Read: start is shared.
- New module for the other drafts' ids (say scripts/supervise_drafts.py): a new concern under CLAUDE.md's rule, which needs a module-map row. Proposal, not decided.

Test files (to change):
- tests/scenarios/supervision_intake_steps.py (38; room 262): Givens/Then for r103 (accepted q1 no initiative; `work start` was run for q1; an initiative fulfils q1); or a new module.
- tests/scenarios/supervision_integrate_steps.py (91; room 209): Givens for r102 (spec on the branch; i2 drafts and p2 formulated; i3 p3 drafted) and the Then.
- tests/scenarios/supervision_proposal_steps.py (82; room 218): Givens for r104 (capability thing holds ids; p1 with adds, changes, removes; p2) and the Then on the gate brief.
- tests/scenarios/supervision_given.py (259; room 41) or supervision_world.py (173; room 127): shared helpers if needed. Prefer a new module to stay under 300.

Files on the change's path, edited or not (line count; room under 300):
- scripts/work (151; 149): cmd_run unchanged.
- scripts/supervise.py (248; 52): Run; unchanged unless a hook is needed.
- scripts/supervise_intake.py (112; 188): take after the starts; unchanged.
- scripts/supervise_change.py (52; 248): write_proposals; form unchanged.
- scripts/supervise_worker.py (247; 53): worker start, brief; unchanged.
- scripts/supervise_draft.py (81; 219): unchanged.
- scripts/workqueue.py (290; room 10): committed, requests, items; unchanged. Any growth here breaks the limit.
- scripts/workqueue_request.py (144; 156): accepted_lines; unchanged.
- scripts/workqueue_status.py (170; 130): open_names; unchanged.
- tests/scenarios/test_supervision.py (258; 42): binds the three scenarios; unchanged.
- tests/scenarios/supervision_rounds_steps.py (263; 37): tests read in part 4; unchanged.

`python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` printed nothing: no tracked Python file is over the limit.
