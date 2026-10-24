# w137 research notes

w137 (under supervision) accepts supervision#r70, r80, r71, r83. Four accepted scenarios in features/supervision.feature (r70 at 865, r80 at 873, r71 at 881, r83 at 995). No `## Retires`.
No map: `tools tests-of` and `untested` report "no map", so every test list here is `by search`. `refs` names resolved; `refs` missed module-attribute calls (see part 3, row 6).
Code run: the worktree's own scripts/ (base f890f2), not the brief's Scripts path. Probes: `.shop/scratch/w137-2-research/probe_proposal.py`, repos under `.../repos/`, run `python3 -m pytest -q -s -n 0 <file>`. Previous stage (1-research) notes read for orientation; its P1-P7 agree with my runs below.

## 1. Why each scenario is red today

Command: `python3 -m pytest -q -p work_items --work-item w137 -n 0 <the four node ids in tests/scenarios/test_supervision.py>` (run): 4 failed.
- r70, `test_a_capabilityproposal_whose_every_question_has_an_answer_is_given_to_an_apply_round_with_its_answers`: StepDefinitionNotFoundError at its first Given (feature line 868, "i1's capability-proposal p1 is awaiting-answer, its ## Questions section with ... and its Answers section with ...").
- r80, `test_when_the_apply_round_..._the_proposal_is_approved`: same error, first Given (line 876).
- r71, `test_when_the_apply_round_..._a_formulate_round_is_started_for_the_proposal`: same error (line 884).
- r83, `test_when_the_formulate_round_..._the_proposal_is_formulated`: same error (line 998).

Missing step definitions (read, grep of tests/scenarios): no step names a capability-proposal file with Questions and Answers, "every round ends" (lines 869, 877, 885; "every round ends and every worker gives DONE" at 999), "a round of the kind ... was started for p1", or "... transition ... was made once the ... round had ended".
Missing in step support: `tests/scenarios/supervision_world.py` `item_text` (l.90-95) writes work-items only; no proposal writer.
Missing in code behind them (read):
- scripts/supervise.py `Run.items` (l.60-61) reads only work-items (through `workqueue.items`); `Run.pull(MOVABLE)` and `Run.run` (l.182-207) never see p1.
- scripts/supervise.py `Run.move` (l.101-108) would call `workqueue.move` with `approved` or `formulated`, which is refused (P11).
- scripts/supervise_brief.py `Briefs.brief` (l.19-51) is shaped for a work-item (its file, `under`, `runs/<name>`); no apply or formulate brief.
- scripts/supervise_worker.py `Workers.session` (l.199-206), `TOOLS` (l.31-37), `MAX_TURNS` (l.39): keyed by the four worker stages; no round stage.
- no script dispatches `initiative-round` (grep of scripts/: no match); agents/initiative-round.md exists (its `apply` and `formulate` jobs).

## 2. What the system answers today

Each probe: `run` (I ran it). Fake claude records starts to a file beside each repository; SHOPSYSTEM_WORK_RUN_WORKER removed from the environment (this session is a worker, and `work run` refuses under it).

- P1 `work run i1` on the answered case (p1 awaiting-answer; Questions "Is a title given twice one book or two?" and "Is the old reader kept?"; Answers "One book." and "No."): exit 0; no stdout, no stderr; 0 claude starts; p1 still awaiting-answer; git clean; 1 commit. `run`.
- P2 partly answered (two questions, one answer): identical to P1. `run`.
- P3 no answer (two questions, no Answers section): identical to P1. `run`.
- P4 no `## Questions` section at all: identical to P1. `run`. Read: `Run.held` (l.164-175) returns [] and `questions()` (l.177-180) is empty, so "every question has an answer" holds vacuously. Whether that starts apply is a decision for the plan; the two readings are (a) apply starts (vacuous truth) and (b) it does not (no question, nothing to apply).
- P5 drafted p1 (the status before r69's gate): exit 0, nothing started, p1 drafted. `run`.
- P6 already approved p1 (the store after r80): exit 0, nothing started, p1 approved. `run`.
- P7 `work status i1` on the answered case: prints "capability-proposal p1 awaiting-answer", no question lines (work-items' questions only). `run`.
- P8 `model check` on the answered case: exit 1, `file: .shop/work/i1/p1.md: status 'awaiting-answer' is not one of approved, drafted, formulated, merged, withdrawn` (two unresolved-reference lines from my fixture's missing capability are noise). `run`.
- P9 `work answer p1 "One book."` on an awaiting-answer p1 with no log.jsonl line: exit 1, stderr `work: log.jsonl gives no transition of p1 to awaiting-answer; work answer has no status to return it to`; nothing written. `run`.
- P10 same, with log.jsonl holding `{"work-item": "p1", "before": "drafted", "after": "awaiting-answer"}` as its last line (what r69's move writes): exit 0, stdout `p1 drafted`; p1 status becomes `drafted`; its `## Answers` gets `- 2026-10-24: One book.`; log's last line `before: awaiting-answer, after: drafted, by: work answer`. `run`.
- P11 `workqueue.move` of p1 to `approved`, then `formulated`: refused, "approved is no status of the work-item lifecycle; p1 is not moved" (formulated likewise); p1 unchanged. `run`.
- P12 `workqueue.move` of p1 to `awaiting-answer` while it is awaiting-answer: moved; log line has before = after = awaiting-answer. `run`.

Nearest cases the scenarios do not give: no answer (P3), partly answered (P2), no Questions section (P4), answered after the gate's move (P10, which lands in `drafted`, not in apply: defect D3).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise.py `Run.items` (l.60-61) | reads work-items of this initiative from `workqueue.items` | a proposal's status is read and moved (r70, r80, r71, r83) | by search: every `work run` scenario in tests/scenarios/test_supervision.py; none with an answered proposal passes | read; grep `items()` |
| scripts/supervise.py `Run.check` (l.63-73) | `workqueue.agrees` over work-items only | p1's log must agree with its file before a move | by search: test_supervision.py check scenarios | read |
| scripts/supervise.py `Run.run` (l.182-207) and `STAGES`/`MOVABLE` (l.27-33) | pulls work-items through four stages; exit 0/3/1 from their statuses | apply, then formulate, then formulated; the exit codes count p1 | by search: test_supervision.py r9, r32, r52, r82 scenarios | read |
| scripts/supervise.py `Run.move` (l.101-108) and `commit` (l.89-99) | `workqueue.move`, then commits p1.md, runs/p1 and log.jsonl (paths by name, so p1 works) | approved and formulated written on p1 through it | none: no test drives a proposal move | read; P11 |
| scripts/workqueue.py `STATUSES` (l.16-17), `move` (l.137-160) | the work-item lifecycle; `approved` and `formulated` refused | r80 and r83 write those on p1 | tests/scripts/test_work_items.py:122-134 (moves to `finished`, still refused: sound); tests/scenarios/test_work_queue.py:192-199 (work-item moves: sound) | refs `workqueue.move` (2 refs, both in workqueue.py: l.207, l.237); grep found supervise.py:103 and supervise_faults.py:83 too, which refs missed; P11 |
| scripts/workqueue.py `items` (l.100-105) | yields work-items only (`kind == work-item`) | every consumer then ignores proposals: supervise.py:61, supervise_pool.py:62, work:32,36 | by search: test_work_queue.py:234-236 `nothing_about` for the work show scenario (features/work-queue.feature:65-71, "it prints nothing about p1"); it breaks if `items` yields proposals and `show` does not filter | refs; grep |
| scripts/supervise_pool.py `choose` (l.59-84) | work-items only; statuses from `workqueue.items` and `self.items()` | rounds need no pool place for these four (r66 not accepted); a round run inside `Run.run` does not reach it | by search: supervision_parallel_steps.py (two and four workers) | refs; read |
| scripts/workqueue_answer.py `asked_from` and `ASKED_FROM` (l.7-21) | a `work answer` returns the work-item to the status its last move into awaiting-answer came from; `drafted` for a gate's move | after r69 and an answer, p1 goes to `drafted`, so r68 would start the gate again instead of r70's apply | by search: features/work-queue.feature:258-262 (r24, answer on a proposal; Givens have no log line, so it is refused, P9); not run | read; P9, P10 |
| scripts/model_work.py `STATUSES["capability-proposal"]` (l.11) | no `awaiting-answer` | `model check` on the state r69 leaves (D1) | by search: tests/scenarios/design_model_check_problems.py:96-99 (`built`, still refused: sound); tests/scripts/test_model.py capability-proposal statuses (none asserts awaiting-answer) | read; P8 |
| scripts/supervise_brief.py `Briefs.brief` (l.19-51) and `answer_lines` (l.53-63) | a work-item's brief; the n-th answer beside the n-th question | an apply round's brief gives the answers (r70); `answer_lines` can be reused | by search: tests/scenarios/supervision_answers_steps.py (work-item answers, r57) | read |
| tests/scripts/stub_claude.py `main` (l.169-184) | takes the brief's `Work-item:` (optional) and `Result file:` lines; `next()` with no default | a round's brief must carry a `Result file:` line, or the stand-in stops with StopIteration | by search: every stand-in scenario | read |
| agents/initiative-round.md (l.38, l.55) | a round appends its own ledger line and replies `BLOCKED` in prose, not as a result file | r80, r71, r83 transition "when the round ends"; a `BLOCKED` reply is no `result.json` (r45 makes that a fault) | none (no round exists) | read |
| scripts/workqueue_status.py `parts` (l.38-48) | already reads proposals and their status | none: P7 shows the proposal line | by search: tests/scenarios/work_queue_status_steps.py | read; P7 |

## 4. Tests the requirements make impossible to keep

No map: searched tests/ by name (`lifecycle`, `STATUSES`, `workqueue.move`, `items()`, `choose(`, `supervise`), by status (`approved`, `formulated`, `awaiting-answer`, `capability-proposal`) and by step text.
- tests/scripts/test_work_items.py:122-134 `test_a_move_to_a_status_outside_the_lifecycle_is_refused` (moves to `finished`): still refused after the change. Sound (read).
- tests/scenarios/test_work_queue.py:192-199 `move` step: work-item moves only. Sound (read by grep).
- tests/scenarios/test_work_queue.py:234-236 `nothing_about`, used by the `work show` scenario (features/work-queue.feature:65-71, "it prints nothing about p1"): becomes impossible to keep if `workqueue.items` yields proposals without `work show` filtering them. Sound today; a constraint on the plan.
- tests/scenarios/test_supervision.py:150-153 `one_commit_per_move` counts commits against `moves(repo)`, which filters w1 only. A p1 move adds a commit and a log line for p1 only: the count stays for w1. Sound (read).
- tests/scenarios/design_model_check_problems.py:96-99 "a status not in its kind's lifecycle" uses `built`: still refused if `awaiting-answer` is added. Sound (read by grep).
- tests/scripts/test_model.py (capability-proposal statuses `drafted`, `merged`, `formulated`, `withdrawn`, `approved` at l.129-196): none asserts `awaiting-answer` refused. Sound (by search).
- Supervision scenarios with a proposal in their Givens (r66, r68, r69, r72-r75, r81, r84, r85 and the r81 Outline) are undefined steps today: no passing test is made impossible. Sound (by search).
- Not run: features/work-queue.feature:258 (r24, answer on a proposal) and the work-queue `work show` scenarios; they were not executed here.
Result: no currently passing test fails because of the four requirements, unless `workqueue.items` changes without `work show` filtering (row above).

## 5. A step the work-item skips

A round for a proposal would not go through `Workers.worker()` (scripts/supervise_worker.py l.149-197). Every effect below is one only that step produces (`read`; no probe, because no round exists to run):
- `verify_push` before the start (r35; supervise_faults.py l.64-70): a push refusal would not stop a round; refusal "cannot verify that it can push the initiative branch ... before the apply stage".
- the start and end lines in log.jsonl with the session id (r8, r49; supervise_worker.py l.165 and l.172).
- `checkout_changes()` (r28; l.167-168, supervise_faults.py l.91-): a change in the main checkout's `.shop/work/` is not put back.
- `shutil.copytree(here, kept_at)` and `session.json` with the transcript path (r62; l.169-171).
- `cut_short()` (r45; l.179-181): a round ending in error or at its turn limit would not be a fault; r80, r71 and r83 would then transition it anyway.
- the `Fault` when no result file, or one that is not JSON (l.182-189), and `session_end()`.
- `keep_named` (r15; l.190): files a result names are not copied into the run directory.
- `Run.commit` (scripts/supervise.py l.89-99): a transition written without going through `Run.move` is not committed, and not pushed (r38).

## 6. Defects

D1. `model check` reports an awaiting-answer capability-proposal as a file problem, although the requirements give that status (r69). Reproduction: `python3 -m pytest -q -s -n 0 .shop/scratch/w137-2-research/probe_proposal.py::test_work_status_and_model_check`; output: `file: .shop/work/i1/p1.md: status 'awaiting-answer' is not one of approved, drafted, formulated, merged, withdrawn`, exit 1 (P8).

D2. `workqueue.move` logs a move to the status a work-item already has. Reproduction: `python3 -m pytest -q -s -n 0 .shop/scratch/w137-2-research/probe_proposal.py::test_workqueue_move_on_proposal`; the last line of `.shop/work/i1/log.jsonl` is `"before": "awaiting-answer", "after": "awaiting-answer", "by": "probe"` (P12). Nothing refuses a no-op move.

D3. `work answer` on a capability-proposal returns it to `drafted`, not to the status the gate started from. Reproduction: `python3 -m pytest -q -s -n 0 .shop/scratch/w137-2-research/probe_proposal.py::test_work_answer_after_gate_move`: stdout `p1 drafted`; p1 status `drafted`; log's last line `"after": "drafted", "by": "work answer"` (P10). Read: r68 starts a gate for a `drafted` proposal, so the loop from answering would reach a second gate, not r70's apply round. The plan decides what happens; this record gives the fact only. Without the log line, `work answer` on an awaiting-answer p1 is refused (P9).

## 7. The file set

Must change for the four scenarios to pass and everything that passes to keep passing:
- scripts/supervise.py (218 lines; room 82): `items`, `run`, `commit`, `move`: a proposal's path: apply when every question has an answer (r70), approved (r80), formulate (r71), formulated (r83). Found by read; refs `Run` (defined l.36, no other reference).
- scripts/workqueue.py (279; room 21): `STATUSES` and `move` accept `approved` and `formulated` for a capability-proposal (P11, refs); `items()` (decision: keep proposals out, or change `work show`). Room is 21 lines: the change must stay within it or split the module first.
- scripts/supervise_brief.py (110; room 190): an apply and a formulate round's brief, reusing `answer_lines` (l.53-63), with a `Result file:` line.
- scripts/supervise_worker.py (229; room 71): the round's session: `AGENT_PREFIX` + `initiative-round`, `TOOLS` and `MAX_TURNS` for the round stages (read: l.31-39, l.199-206).
- tests/scenarios/supervision_proposal_steps.py (new; name chosen by the plan): the Givens for p1 with Questions and Answers, "every round ends" (with and without "every worker gives DONE"), and the Thens for the round starts and the transitions. Found by grep of the step texts.
- tests/scenarios/supervision_world.py (173; room 127): a proposal file writer beside `item_text` (l.90-95).
- tests/scenarios/test_supervision.py (246; room 54): imports the new step module only (step registration).
- tests/scripts/stub_claude.py (258; room 42): a round brief's `Result file:` line is read at l.182; the agent is checked for existence under --plugin-dir (l.174), so `initiative-round` needs no change there. Any change is for the round's output shape only.

On the path, not required by the four scenarios (decide in the plan):
- scripts/model_work.py (219; room 81): D1, `awaiting-answer` for capability-proposal.
- scripts/workqueue_answer.py (48; room 252): D3, answer on a proposal (r24); not accepted here.
- scripts/supervise_pool.py (142; room 158): `choose` reads work-items only; needed only if rounds share the pool (r66, not accepted).
- scripts/work (147; room 153): `show` and the items it reads (l.32, l.36); unchanged for these four.
- scripts/supervise_faults.py (160; room 140), scripts/supervise_merge.py (135; room 165), scripts/supervise_review.py (77; room 223): read; the fault path of a round would run through them; unchanged for these four.
- scripts/workqueue_status.py (170; room 130): reads proposals already; no change.
- tests/scenarios/supervision_given.py (250; room 50): work-item Givens; reused by the new Givens only if it helps. Not changed for these four.

Size: `python3 <Scripts>/tools size --limit 300` printed nothing (exit clean); no tracked Python file is over 300. Line counts by `wc -l`.

Scratch: `.shop/scratch/w137-2-research/` (probe file, repos, fake claude, call logs). `git status --porcelain` was empty before and after my probes; the scratch directory is not listed (ignored).
