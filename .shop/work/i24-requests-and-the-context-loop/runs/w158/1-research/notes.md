# Research of w158 (r79, no-request initiative)

Tools: `tools refs` worked. `tools tests-of` refused: "no map" (its map runs the whole suite, not run). Test lists are by search, marked so. Probe: `.shop/scratch/w158-1-research/probe_integrate.py`, run as `python3 -m pytest -q -s -p no:xdist -o addopts="" <path>`; it runs `scripts/work` from the worktree, with `SHOPSYSTEM_WORK_RUN_WORKER` removed from its environment (this session is a worker, and `work run` refuses under it).

## 1. Why each scenario is red today

- **Scenario 1**, "a proposed initiative is given to an integrate round with the accepted lines of the request it fulfils" (features/supervision.feature:849). `python3 -m pytest -q "tests/scenarios/test_supervision.py::test_a_proposed_initiative_is_given_to_an_integrate_round_with_the_accepted_lines_of_the_request_it_fulfils"`: **1 passed** (run). Already green; the plan keeps it green.
- **Scenario 2**, "a proposed initiative that fulfils no request is given no integrate round, stays proposed and leaves nothing behind" (features/supervision.feature:857). The same form with `test_a_proposed_initiative_that_fulfils_no_request_is_given_no_integrate_round_stays_proposed_and_leaves_nothing_behind`: **1 failed**, `StepDefinitionNotFoundError: Step definition is not found: Given "i1 is proposed and fulfils no request"` (run). Missing step: `tests/scenarios/supervision_rounds_steps.py:96` matches only `whose (lines? ...)`.
  - Also undefined, by search (`read`; pytest-bdd stops at the first undefined step, so the run does not show them): Then "no round of the kind integrate was started for i1", "i1 is proposed", "no branch is made for a round", "nothing under .shop/work/ is left uncommitted". Searched every `tests/scenarios/*.py`; none matches. The nearest, `test_supervision.py:141`, has other text.
  - Behind the steps, in the code: `scripts/supervise_rounds.py:32-33` `Rounds.due()` returns `(initiative, "integrate", "started")` for every `proposed` initiative, with or without `fulfils`. Once the steps exist, the Then "no round ... integrate" would fail: probe case A shows the round is started (section 2).

## 2. What the system answers today

Command: `python3 -m pytest -q -s -p no:xdist -o addopts="" .shop/scratch/w158-1-research/probe_integrate.py` (3 passed). Each case runs `work run i1` twice, with `SHOPSYSTEM_WORK_CLAUDE=/bin/false`, in a repository made under the scratch directory with a bare remote.

- **Case A, the scenario's Given: i1 `proposed`, no `fulfils`.** `run`:
  - run 1: `EXIT 1`, stderr `work: there is no request  under .shop/work/requests` (empty id, two spaces).
  - run 2: `EXIT 1`, stderr `work: .shop/work/i1/log.jsonl under .shop/work is not committed; commit it before work run starts`.
  - After both: `git status` `M .shop/work/i1/log.jsonl`; branches `main`, `round/i1-1-integrate`; `initiative.md` `status: started`; log: `proposed -> started` (by work run), `integrate ... push verified`; commits `work: i1 proposed -> started`, `i1 proposed`, `base`.
- **Case B, nearest: `fulfils: q1`, q1 not kept.** As A, message `work: there is no request q1 under .shop/work/requests`; run 2 the same uncommitted-log refusal; `started`; branch `round/i1-1-integrate`.
- **Case C, nearest: `fulfils: q1`, q1 kept with its only line `refused`.** run 1: `EXIT 1`, `the integrate round of i1 (.shop/work/i1/runs/i1/1-integrate) faulted, and i1 keeps its status started: its round's session exited with an error (exit code 1)`. run 2: `EXIT 0`, nothing printed. Still `started`; the log has the integrate session's start and end, then a **branch-review** start and end (`bdd-branch-reviewer`); commit `branch review 1 of i1`. No work-item exists. See D2 and D3.
- `read`, not probed: a request whose `## Outcomes` lacks a line gives the same empty accepted set as case C (`scripts/workqueue_request.py:30-35`).

## 3. Old assumptions

r79 and r84 give an integrate round to every proposed initiative, and its brief needs a readable request. The rows are the places that still make that assumption.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_rounds.py:Rounds.due (32-33) | every `proposed` initiative is due `integrate`, with or without `fulfils` | due only with a readable request that has accepted lines (scenario 2; r79) | scenario 1 (passes) through `rounds()`; scenario 2 cannot run (undefined Given) | refs (due, rounds); read |
| scripts/supervise_rounds.py:Rounds.round (48-49) | calls `start_initiative` before the brief is written | the no-request path must not reach it (r10: change nothing) | scenario 1; the r84 scenario (features/supervision.feature:1043) via `proposed_fulfilling` | refs (start_initiative); read |
| scripts/supervise_rounds.py:Rounds.start_initiative (81-86) | writes `started`, logs, commits, pushes | as above | as above | refs |
| scripts/supervise_brief.py:Briefs.integrate_lines (66-70) | reads `fulfils`, calls `workqueue_request.accepted_lines` with no check | not to be reached with an empty or missing request | scenario 1 only | refs (integrate_lines: one caller, brief:38); read |
| scripts/workqueue_request.py:accepted_lines (30-35), path_of (18-22) | refuse a missing request with `there is no request ...` | the refusal must come before any change (r10), not after `started` is written | none by search (`accepted_lines` is called by `supervise_brief.py:70` as `workqueue_request.accepted_lines`, which `tools refs` missed: it reported 0 references) | search (refs missed it); read |
| scripts/supervise.py:Run.pull_through (202-210) | `all(s in (green, withdrawn) for _, s in items())` is True for an initiative with no work-items, so `branch_review()` runs | with no request, no round and no work-item, nothing is to be reviewed (r27 and r75 for zero items: not stated) | none by search (no test runs a zero-item initiative to a branch review; see 4) | read; probe C run 2 |
| scripts/supervise_review.py:Reviews.unread (19-33), branch_review (35) | any commit on the initiative branch that no review read starts a review | i1's own `proposed` commit is unread, so a review would start for a no-request initiative | by search: the branch-review steps (see 4) | read; probe C |
| scripts/supervise_answers.py:Answers.answers (35-40) | returns None without `fulfils`; else `path_of`, which refuses a missing request | for case B the refusal would come here too, before rounds | by search: supervision_answers_steps.py | refs (path_of); read |
| scripts/supervise_all.py:run_all (19-49) | takes every open initiative; each `pull_through` in a thread; a Refused prints and exits 1 | the no-initiative run would give a proposed no-request initiative the same refusal or the ruling's exit | none: no test runs `work run` with no initiative over a proposed initiative (by search: `proposed` appears in no such test) | read; search |
| model.lp:253-255 (v16a) | an initiative dated after 2026-10-23 that fulfils no request breaks `model check` | the spec already requires a dated initiative to fulfil a request; scenario 2's initiative is undated, so v16a does not apply | design-model-check r113 (features/design-model-check.feature:819) | search |

## 4. Tests the requirements make impossible to keep

`tools tests-of` refused (no map). By search over `tests/scenarios/` and `tests/scripts/`:

- Searched `integrate|proposed`: `supervision_rounds_steps.py` (integrate_started, proposed_fulfilling); `supervision_given.py:171` (`another_session_commits`: i2 `proposed` committed by another session while `work run i1` runs; i2 is not taken; keeps); `work_queue_start_steps.py:38-44` (`work start`, no `work run`; keeps); `migration_session_steps.py:32,37` (initiatives set up for migration, not run; keeps).
- Result: **none** can no longer pass. No test asserts that a proposed initiative with no `fulfils` gets an integrate round. Scenario 1 keeps passing: it gives `fulfils: q1` with lines.
- Not verified: whether any branch-review test runs an initiative with zero work-items. Searched only which files mention branch review: `supervision_review_steps.py`, `supervision_given.py`, `supervision_then_workers.py`, `supervision_faults_steps.py`, `supervision_proposal_steps.py`, `supervision_analysis_steps.py`, `supervision_world.py`. A fix that leaves D3 reachable would need that checked.

## 5. A step the work-item skips

The work-item's path for a proposed initiative with no request leaves out the integrate round's steps. Each effect below is produced only by the existing way (probe case A and C, `run`):

- the transition `proposed -> started` and its commit (`work: i1 proposed -> started`), which r84 makes at round start (case A).
- the `push verified` log line for stage `integrate`, from `verify_push` in `worker()` (case A).
- the `round/i1-1-integrate` branch and its worktree (case A).
- the integrate session's start and end lines in log.jsonl (case C, run 1 and run 2 logs).
- the refusal of the request, which the existing way gives after `started` is written (cases A, B).
- `read`: `push_unpushed()` runs before the rounds (`supervise.py:194`) on either path, so no effect is lost there.

The work-item must decide whether a no-request initiative is refused before `started` is written (the r10 reading), or left with no change and no error (the ruling's reading). Dropping the round drops every effect above, whichever it chooses.

## 6. Defects

### D1. A proposed initiative with no request is moved to `started` and refused on the first run

Reproduction: `python3 -m pytest -q -s -p no:xdist -o addopts="" .shop/scratch/w158-1-research/probe_integrate.py`, case A. It came back:

- run 1: `EXIT 1`, `work: there is no request  under .shop/work/requests`.
- run 2: `EXIT 1`, `work: .shop/work/i1/log.jsonl under .shop/work is not committed; commit it before work run starts`.
- `initiative.md` `status: started`; branch `round/i1-1-integrate`; `git status` `M .shop/work/i1/log.jsonl`.

The ruling of 2026-10-25 says the first run exits as r9, r32 and r52 give, not with an error. Case B shows the same for a missing request.

### D2. A faulted integrate round leaves the initiative `started`; the next run does not re-run it

Reproduction: case C, `fulfils: q1`, q1's line 1 `refused`, `SHOPSYSTEM_WORK_CLAUDE=/bin/false`. run 1: `EXIT 1`, `the integrate round of i1 ... faulted, and i1 keeps its status started`. run 2: `EXIT 0`. The initiative stays `started`: `due()` no longer returns integrate for it (`supervise_rounds.py:32`).

Reading conflict, no judgment: r84 writes `started` at round start; r86 says a round that fails keeps "the proposal's or initiative's status", which before the round was `proposed`. The run's message says it kept `started`.

### D3. An initiative with no work-items is given a branch review

Reproduction: case C run 2, the same command as D2. Log: `stage: branch-review` start and end with `bdd-branch-reviewer`; commit `branch review 1 of i1`; no work-item exists. Cause: `pull_through` (`supervise.py:205`) treats zero work-items as all `green`, and `branch_review()` finds i1's own commits unread (`supervise_review.py:19-33`). r27 and r75 do not say whether "every work-item green" holds for zero work-items. Recorded, not judged.

## 7. The file set

Production files:

- `scripts/supervise_rounds.py` (97 lines; room 203). `due()` returns integrate for a `proposed` initiative only when its `fulfils` names a readable request with accepted lines; `round()` makes that check before `start_initiative` (r10). Found by refs (due, round, start_initiative) and probe cases A to C.
- `scripts/supervise_brief.py` (129 lines; room 171), only if the check goes in `integrate_lines` rather than `due()`. Found by refs (integrate_lines).
- `scripts/supervise.py` (247 lines; room 53), only if the zero-item branch review (D3) is guarded in `pull_through` (line 205). Found by probe C run 2 and read.
- `scripts/supervise_review.py` (82 lines; room 218), only if the guard goes in `branch_review` rather than `pull_through`. Found by read.
- `scripts/workqueue.py` (286 lines; room 14), only if the check is written as a new function there; read only otherwise (`agrees`, `frontmatter`).
- `scripts/workqueue_request.py` (142 lines; room 158): read only; `path_of` and `accepted_lines` are the request reads the check would use.

Test files:

- `tests/scenarios/supervision_rounds_steps.py` (201 lines; room 99). Add the Given "i1 is proposed and fulfils no request" and the Thens "no round of the kind integrate was started for i1", "i1 is proposed", "no branch is made for a round", "nothing under .shop/work/ is left uncommitted". Found by search (section 1).
- `tests/scenarios/test_supervision.py` (252 lines; room 48). Binds the two scenarios; no change expected. Found by collect-only.

Modules on the change's path, not edited (lines from `wc -l`; room under 300):

- `scripts/supervise.py` (247; room 53), `scripts/supervise_all.py` (66; room 234), `scripts/supervise_answers.py` (121; room 179), `scripts/supervise_worker.py` (247; room 53), `scripts/work` (150; room 150), `scripts/workqueue.py` (286; room 14).

`tools size` was not run; the counts are `wc -l`. CLAUDE.md gives the 300-line limit.

## Commands and files used
- Read: the brief, the work-item, `spec/capabilities/supervision.md`, `CLAUDE.md`, `features/supervision.feature` 848-865, `tests/scenarios/supervision_rounds_steps.py`, `tests/scenarios/supervision_world.py`, `tests/scenarios/supervision_given.py` 160-185, `tests/scenarios/test_supervision.py` 125-150, `scripts/supervise.py`, `scripts/supervise_rounds.py`, `scripts/supervise_brief.py`, `scripts/supervise_review.py` 1-70, `scripts/supervise_worker.py` 120-180, `scripts/workqueue.py` 180-220, `scripts/workqueue_request.py` 1-60, `scripts/supervise_all.py`, `runs/branch-review/1/findings.md`.
- `tools refs` on accepted_lines, path_of, start_initiative, integrate_lines. `tools tests-of`: refused (no map).
- Scenario runs: the two node ids above. Probe: the file above, 3 cases.
- Scratch: `.shop/scratch/` is git-ignored; `git status --porcelain` is clean.
