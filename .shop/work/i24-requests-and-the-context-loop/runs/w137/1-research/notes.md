# w137 research notes

Work-item w137 (`under: supervision`), accepts supervision#r70, r80, r71, r83. Accepted scenarios (features/supervision.feature): the four below. No `## Retires`. No `tools map`, so `tests-of` and `untested` are unavailable: every test list here is `by search`. `refs` used for names. Probes ran `work`, `model` by the brief's Scripts path (/home/vscode/shopsystem-bdd/scripts) against scratch repositories; pytest ran from the worktree.

Accepted scenarios and node ids (`tests/scenarios/test_supervision.py::`):
- a capability-proposal whose every question has an answer is given to an apply round with its answers (r70): `test_a_capabilityproposal_whose_every_question_has_an_answer_is_given_to_an_apply_round_with_its_answers`
- ... the apply round ... ends, the proposal is approved (r80): `test_when_the_apply_round_work_run_started_for_a_capabilityproposal_ends_the_proposal_is_approved`
- ... a formulate round is started for the proposal (r71): `test_when_the_apply_round_work_run_started_for_a_capabilityproposal_ends_a_formulate_round_is_started_for_the_proposal`
- ... the formulate round ... ends, the proposal is formulated (r83): `test_when_the_formulate_round_work_run_started_for_a_capabilityproposal_ends_the_proposal_is_formulated`

## 1. Why each scenario is red today

Command: `python3 -m pytest -q -p work_items --work-item w137 <the four node ids>` (run, 4 failed).
- r70: `StepDefinitionNotFoundError` at its first Given (features/supervision.feature:868): "i1's capability-proposal p1 is awaiting-answer, its ## Questions section with ... and its Answers section with ...". No step matches.
- r80: same error at its first Given (line 876).
- r71: same error at its first Given (line 884).
- r83: same error at its first Given (line 998).

Behind the steps (`read`, confirmed by grep): no step in tests/scenarios/supervision_*.py or test_supervision.py names a capability-proposal, "every round ends", "a round of the kind ... was started", or "transition ... was made once the ... round had ended". The Givens and Thens need a proposal file writer (supervision_world.py has `item_text` for work-items only) and a stand-in claude that answers round sessions (tests/scripts/stub_claude.py knows the four worker roles only; `read` of its roster by grep of AGENTS in supervision_world.py).

Behind the steps in the code (`read`):
- scripts/supervise.py `Run.items()` (l.60-61) and `Run.run()` (l.182-207): work-items only; no round, no transition for a proposal node.
- scripts/supervise.py `Run.move()` (l.101-108) and `commit()` (l.89-99): commit only the work-item file, its runs directory and log.jsonl; a proposal's file would not be committed.
- scripts/workqueue.py `STATUSES` (l.16-17): no `approved` or `formulated`; `move()` (l.137-160) refuses them (probe P4).
- scripts/supervise_brief.py: no brief for an apply or formulate round.
- agents/initiative-round.md exists, with the `apply` and `formulate` jobs; nothing in scripts/ dispatches it (`grep initiative-round scripts` = no match in supervise*.py).

## 2. What the system answers today

Probes (scratch repositories `scratch/answered`, `partly`, `drafted`, `moves`; initiative i1 holds only p1; stand-in claude `fake_claude.sh` records calls and exits 1; SHOPSYSTEM_WORK_RUN_WORKER removed from the env, because this session is itself a worker and `work run` refuses under it, as `supervise.Run.check()` l.65-67 says; the first run without that removal printed that refusal, exit 1).

P1. `python3 -m pytest -q -s -n 0 .shop/scratch/w137-1-research/probe_proposal.py` (test "answered, awaiting-answer") — the Givens of r70, r80, r71, r83 (p1 awaiting-answer, Questions with two questions, Answers with "One book." and "No.") then `work run i1`. Returned: exit 0; no stdout; no stderr; stand-in calls none; p1 still `status: awaiting-answer`; git clean. `run`.
P2. same probe, "partly answered" (two questions, one answer; nearest case). Returned: exit 0, nothing started, p1 awaiting-answer. `run`.
P3. same probe, "drafted" (p1 drafted, no questions; the status before r69's gate). Returned: exit 0, nothing started, p1 drafted. `run`.
P4. same probe, "moves": `workqueue.move(root, 'i1', 'p1', s, by='probe')` for each status. Returned: `approved refused: approved is no status of the work-item lifecycle; p1 is not moved`; `formulated refused: ...`; `awaiting-answer moved` (log line `before` and `after` both awaiting-answer). `run`.
P5. `python3 -m pytest -q -s -n 0 .shop/scratch/w137-1-research/probe_model.py` — on the answered repository, `python3 <Scripts>/model check`: `file: .shop/work/i1/p1.md: status 'awaiting-answer' is not one of approved, drafted, formulated, merged, withdrawn`, plus two unresolved references from my probe repository's missing thing capability (noise). Exit 1. `run`.
P6. same probe, `work show` (answered repo): empty stdout, exit 0 (it lists work-items only). `run`.
P7. same probe, `work status i1`: `initiative i1 started`, `capability-proposal p1 awaiting-answer`, no question lines printed (the proposal's questions are not printed; work-items' are). `run`.

Nearest cases not given: no answer at all for a proposal with questions (`read`: the same as P2 with zero answers — `questions()` returns the questions, so no apply round would start); a proposal awaiting-answer with no `## Questions` at all: `held()` returns [], so `questions()` is empty and "every question has an answer" holds vacuously — `read`, not probed; the plan must decide.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise.py `Run.items` (l.60-61) and `Run.run` (l.182-207) | reads work-items only; prints statuses and exits 0/3/1 from them | a proposal node must be read and moved; p1 awaiting-answer with answers starts apply, then formulate | by search: the `work run` scenarios of tests/scenarios/test_supervision.py (no test with a proposal passes today; all proposal Givens undefined) | read; refs |
| scripts/supervise.py `Run.commit` (l.89-99) | commits the work-item file, `runs/<name>` and log.jsonl only, then pushes | a proposal's transition writes p1.md; it must be committed on the initiative branch (r7 applies the same way) | none (no test drives a proposal move) | read |
| scripts/workqueue.py `STATUSES` (l.16-17) and `move` (l.137-160) | the work-item lifecycle; `approved`, `formulated` refused | r80 and r83 write those statuses on p1 | by search: tests/scripts/test_work_items.py:122 (refuses `finished`; still true); tests/scenarios/test_work_queue.py:190-199 (work-item statuses) | refs (1 reference, workqueue.py:145); P4 |
| scripts/workqueue.py `items` (l.100-105) | yields kind work-item only | `Run.items` and the pool's `choose` use it; a proposal's status would come from elsewhere | by search: tests/scenarios/test_work_queue.py `work show` scenarios (no proposal listed, by design today) | refs (supervise.py:61, supervise_pool.py:62, work:31,35) |
| scripts/model_work.py `STATUSES["capability-proposal"]` (l.11) | lacks `awaiting-answer` | a proposal in the state r69 gives is a model file problem today (P5) | by search: tests/scripts/test_model*.py and design-model-check scenarios use `built`, `drafted`, `merged`; none asserts awaiting-answer | read; P5 |
| scripts/workqueue_status.py `parts` (l.38-48) | already reads proposal status and questions | none: it reads any status; P7 shows it works | by search: tests/scenarios/work_queue_status_steps.py | read; P7 |
| scripts/workqueue_answer.py `answer` (l.16-47) | answers an awaiting-answer work-item; returns it to the status its log's last move into awaiting-answer came from | a proposal's answer (r24, work-queue) has no such log origin; the apply round needs the answer written | by search: tests/scenarios/test_work_queue.py:258-307 (proposal answer scenario) | read (lines 16-20 and 31-47 only; rest not read) |

## 4. Tests the requirements make impossible to keep

No map, so by search. Searched tests/ for proposal statuses and for the functions above:
- tests/scripts/test_work_items.py:122-134 `test_a_move_to_a_status_outside_the_lifecycle_is_refused` moves to `finished`. Still refused after the change: sound.
- tests/scenarios/test_work_queue.py:70-82, 190-199: work-item moves and proposal files written as status fixtures. Sound.
- tests/scenarios/test_supervision.py and supervision_*.py: every `work run` scenario with a proposal in its Givens is an undefined step today (r66, r68, r69, r81 Outline (features/supervision.feature:1015 `capability-proposal p1 | awaiting-answer`), r84, r85, r72, r73, r74, r75 do not touch proposal nodes). No passing scenario has an answered awaiting-answer proposal, so none is made impossible. Sound by search.
- tests/scripts/test_model.py, test_model_reading.py, design-model-check steps: capability-proposal statuses `drafted`, `merged`, `formulated`, `withdrawn`, `approved`; none asserts that `awaiting-answer` is refused. Sound by search.
Result: none of the passing tests can no longer pass; the four scenarios and r66/r81 need new steps.

## 5. A step the work-item skips

The proposal rounds (apply, formulate, gate) are a new path that would not go through `Workers.worker()` (scripts/supervise_worker.py l.149-197), which does for each worker (`read`):
- `verify_push` before the start (r35) — a push refusal (`supervise_faults.py` l.64-78) would not stop a round. Effect only this step produces: refusal "cannot push the initiative branch".
- the start and end lines in log.jsonl (r8, r49) and the `session` id.
- `checkout_changes()` (r28): a change in the main checkout is put back and the item failed.
- `shutil.copytree(here, kept_at)` and `session.json` with the transcript path (r62).
- `cut_short()` and `session_end()` (r45): a round ending in error or turn limit is a fault.
- `keep_named` (r15) copying files the result names.
- the `Fault` raised when a result file is missing or not JSON (l.187-189).
Probe of the existing way: none run (the rounds do not exist). P1 shows that nothing starts for an answered proposal, so the skipped effects are not exercised today.

## 6. Defects

D1. `model check` reports an `awaiting-answer` capability-proposal as a file problem, though work-queue r24 and supervision r69 give that status.
Reproduction: `scratch/answered` (p1 awaiting-answer, two questions, two answers), `python3 /home/vscode/shopsystem-bdd/scripts/model check` in that repository → `file: .shop/work/i1/p1.md: status 'awaiting-answer' is not one of approved, drafted, formulated, merged, withdrawn`, exit 1 (P5).

D2. `workqueue.move` logs a move to the status a work-item already has.
Reproduction: P4's `awaiting-answer moved`; `.shop/work/i1/log.jsonl` gets `{"work-item": "p1", "before": "awaiting-answer", "after": "awaiting-answer", ...}`. Nothing refuses a no-op move.

D3 (note, not a crash). `work show` lists no capability-proposal while `work status i1` does (P6, P7).

## 7. The file set

Must change for the four scenarios (`read` unless said):
- scripts/supervise.py (218 lines; room 82): `items`, `run`, `commit`, `move`: a proposal node path — start apply when every question has an answer (r70), transition to approved (r80), start formulate (r71), transition to formulated (r83).
- scripts/workqueue.py (272; room 28): `STATUSES` and `move` accept `approved` and `formulated` for a capability-proposal (refs: one reference, l.145).
- scripts/supervise_brief.py (110; room 190): an apply round's brief, given the answers, reusing `answer_lines` (l.53-63).
- scripts/supervise_worker.py (229; room 71): the round's session path (section 5); TOOLS and AGENT_PREFIX for the `initiative-round` agent (agents/initiative-round.md).
- tests/scenarios/supervision_proposal_steps.py (new; names to be chosen by the plan): the Givens of p1 with Questions/Answers, "every round ends", the Thens for round kinds and transitions.
- tests/scenarios/supervision_world.py (173; room 127): a proposal file writer beside `item_text`.
- tests/scenarios/test_supervision.py (246; room 54): imports the new step module only.
- tests/scripts/stub_claude.py (258; room 42): answers an apply or formulate round session (its roster is the four worker roles, `read` by grep).

Not required by the four scenarios, but on the path (decide in the plan):
- scripts/model_work.py (216; room 84): D1.
- scripts/supervise_pool.py (142; room 158): `choose()` (l.59-84) only work-items; needed only if rounds share the pool (r66, not accepted here).
- scripts/workqueue_answer.py (48; room 252): answer on a proposal (r24), not accepted here.
- scripts/supervise_faults.py (160; room 140), scripts/supervise_merge.py (135; room 165), scripts/supervise_review.py (77; room 223): on the path, not changed for these four (`read`).
- scripts/work (138; room 162): `show` lists work-items only (D3).
- scripts/workqueue_status.py (170; room 130): reads proposals already; no change.

Size: `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` printed nothing (no tracked Python file over 300). Line counts by `wc -l` and Grep count.

Scratch: `.shop/scratch/w137-1-research/` holds probe_proposal.py, probe_model.py, fake_claude.sh, repositories and remotes; `git status --porcelain` is empty (the scratch directory is ignored).
