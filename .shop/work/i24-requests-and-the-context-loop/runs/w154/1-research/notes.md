# w154 research notes

Method: `tools tests-of` and `untested` have no map (`no map: make one with tools map`); I did not make one, so every test list here is `by search`. `tools refs` used for `Rounds` (0 refs) and `keep_round` (1 production ref). Code read from this worktree; `Scripts:` path given by the brief. Probes are `run`; what I read is `read`.

Accepted: supervision#r86, r87, r88. Scenarios: test_supervision.py node ids `test_when_a_round_work_run_started_for_a_capabilityproposal_{ends_at_its_turn_limit_the_proposal_keeps_its_status | gives_an_outcome_other_than_done_no_transition_is_made_from_it | leaves_no_result_it_can_read_work_run_exits_with_an_error_naming_the_round_and_how_it_ended}`.

## 1. Why each scenario is red today

Command for each: `python3 -m pytest -q -p no:warnings "tests/scenarios/test_supervision.py::<node id>"` (run). All three stop at `StepDefinitionNotFoundError` on the first undefined step.

- **r86, turn limit.** Undefined Given (feature line 1053): "the gate round's session ends at its turn limit, its result giving the question ... on p1". Undefined Then (line 1056): "p1 is drafted" (the only `is <status>` Then is `awaiting-answer`, test_supervision.py:129). Code already does the right thing (probe a-turn, §2). Missing: a Given that sets the stub's plan to `subtype: error_max_turns` with questions (supervision_rounds_steps.py:42-49 sets only DONE).
- **r87, non-DONE outcome.** Undefined Given (line 1062): "the apply round gives BLOCKED, asking ...". Then at line 1064, "a round of the kind apply was started for p1", does not match supervision_rounds_steps.py:134, which needs ", given the answers ...". Undefined Then (line 1065): "log.jsonl gives no transition made after the apply round had ended". Code gap: the round makes the transition (D2), so this Then would fail once the steps exist.
- **r88, no readable result.** Undefined Given (line 1071): "the apply round ends, and the formulate round's session ends with no error and before its turn limit, having written no result file". Undefined Then (line 1073): "`work run` names the formulate round of p1 and that it left no result it can read". `it exits with an error` exists (test_supervision.py:100). Code gap for the Then: the real message says "wrote no result file", not "left no result it can read" (§2, c-formulate), so the Then needs a matching text. Stub gap: both the apply and formulate rounds start with agent `initiative-round` (supervise_rounds.py:58) and stub_claude.py:181 picks the plan by agent, so one plan cannot make apply DONE and formulate no-result. The plan needs a key by round kind (the brief's heading `# <kind> of p1`, written by supervise_brief.py:55).

## 2. What the system answers today

Probes: `.shop/scratch/w154-1-research/probe_rounds.py` and `probe_keep.py`. Command: `python3 -m pytest -q -s -n 0 .shop/scratch/w154-1-research/probe_rounds.py` (run). Each case is a scratch repository under `.shop/scratch/w154-1-research/cases/<case>/`, `scripts/work run i1` from this worktree, the stand-in claude as workers. Stand-in plan keyed by agent, so every round gets the same plan. Exit 0 in the cases with `measure initiative` refused: the stand-in's session.json lacks usage, so measure refuses after the branch review (stub artifact, not counted).

| case (start status) | stand-in plan for every round | exit | p1 after | what came back |
|---|---|---|---|---|
| a-turn (drafted) | gate: error_max_turns, question | 1 | drafted | stderr: "the gate round of p1 (.shop/work/i1/runs/p1/1-gate) faulted, and p1 keeps its status drafted: its round's session ended at its turn limit (error_max_turns, 26 turns, exit code 1); work run takes no outcome from it, whatever its result file says". Commit `work: p1 gate round 1-gate faulted` holds runs/ and log only; pushed (main == origin/main); branch `round/p1-1-gate` kept; one worktree (removed). |
| a-done (drafted) | gate: DONE, question | 0 | awaiting-answer | baseline; question under `## Questions`; log `drafted -> awaiting-answer`. |
| a-blocked (drafted) | gate: BLOCKED, question | 0 | awaiting-answer | D1: transition made and question written. |
| a-blocked-q (drafted) | as a-blocked | 0 | awaiting-answer | p1.md `## Questions`: "Is a title given twice one book or two? Readings: one book (recommended), two books". |
| b-blocked (awaiting-answer, Q and A) | apply: BLOCKED, "Is the old reader kept?" | 3 | formulated | D2: apply round then `awaiting-answer -> approved`, formulate round started, `approved -> formulated`. "Is the old reader kept?" written nowhere. The run then drafted w1 from p1's adds and ran it (probe-only noise; its suite is empty). |
| b-done (awaiting-answer) | DONE | 3 | formulated | baseline, same path as b-blocked. Exit 3 is w1's empty suite. |
| c-formulate (approved) | result: none | 1 | approved | stderr: "the formulate round of p1 (.shop/work/i1/runs/p1/1-formulate) faulted, and p1 keeps its status approved: its round wrote no result file; its session ended as a success (success, 1 turns, exit code 0)". Commit `work: p1 formulate round 1-formulate faulted`; branch kept. Starts from approved so only formulate runs (stub keys by agent). |
| c-apply (awaiting-answer) | result: none | 1 | awaiting-answer | same shape, "the apply round of p1 ...". |
| c-apply-turn (awaiting-answer) | error_max_turns | 1 | awaiting-answer | "the apply round of p1 ... its round's session ended at its turn limit (...)". |

Leftovers after a-turn (probe_keep.py, run): branches `main`, `round/p1-1-gate`; one worktree; `main` equal to `origin/main`; runs dir holds brief.md, result.json, session.json.

Nearest cases read, not run: (read) `Rounds.due` (supervise_rounds.py:35-36) starts `apply` for an `awaiting-answer` proposal with no `## Questions` and no `## Answers`, because 0 >= 0. A proposal with no questions is therefore sent to apply with no answers. (read) `Rounds.round` for kind `integrate` writes `started` before the session (§3, row 4).

## 3. Old assumptions

Requirements r86-88 change what a round's result does. Today a round's result is taken as an outcome whatever its status.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_rounds.py:Rounds.round (58-74) | takes `data` whatever `status` says; calls `move(name, before, after, asked)` unconditionally | must check `status`: a non-DONE status keeps the status, makes no transition, and raises | by search: the proposal scenarios in supervision.feature (15 lines `capability-proposal p1 is`), all with DONE; none with a non-DONE round | read; run (a-blocked, b-blocked) |
| scripts/supervise_rounds.py:Rounds.round, line 72 `asked = ... if kind == "gate"` | questions written only for a gate round, whatever its status | a non-DONE gate: r85 writes its questions? r86/r87 keep status. Reading to settle: see Questions | none (no test gives a non-DONE gate) | read; run a-blocked-q |
| scripts/supervise_rounds.py:Rounds.rounds and Rounds.due (28-45) | loops `while due` and expects every round to move the status | if a non-DONE round returns without a transition and without raising, `due()` returns the same round, which starts again with a new run directory, forever. The round must raise, as the fault path does | by search: as row 1 | read |
| scripts/supervise_rounds.py:Rounds.start_initiative (76-81), called from round (48-50) | `proposed -> started` written, logged and committed before the integrate session starts (r84) | r86 keeps the initiative's status when its round is non-DONE or faults; the status is already `started` when the round starts. Conflict, see Questions | by search: supervision_rounds_steps.py:117 `started_with_round` (the r84 scenario) | read |
| scripts/supervise_worker.py:Workers.worker (161-209) and outcome (235-242) | returns the result's `data` for any status not cut short; `outcome()` maps a non-DONE status to a question for work-items only (supervise.py:165 and supervise_merge.py:101) | the round could reuse `outcome()`; rounds do not call it | by search: work-item scenarios with a question (supervision_faults_steps.py) | read; `tools refs` gives 0 for the method |
| scripts/supervise_rounds.py:keep_round (83-92) | commits the stage directory and log lines, pushes, drops `unlogged` and `own`, only on a fault | a non-DONE round must reach it too, or its stage directory and log stay uncommitted (see §5) | none: grep for "faulted" in tests/ finds nothing | `tools refs` (1 production ref, supervise_rounds.py:69); run a-turn |

## 4. Tests the requirements make impossible to keep

By search (no map). No test gives a round a non-DONE status: `grep -rn "BLOCKED\|faulted" tests/` finds nothing, and the round plans in tests (supervision_rounds_steps.py:44, 49, 83, 89; supervision_delegation_steps.py:44) are all DONE.

- Found sound: the gate, apply and formulate DONE scenarios (supervision_rounds_steps.py:69-158, test_supervision.py r68-r71, r80, r83, r85) keep passing: a DONE result still transitions after the round ends.
- Found sound: `started_with_round` (supervision_rounds_steps.py:117-123) asserts `started` before the integrate session. It still passes whichever reading of §3 row 4 is chosen, unless the plan rolls the status back on a fault.
- Found sound: test_agents.py:43 (starters are `initiative-round`) unaffected.
- Nothing in tests/ asserts that a non-DONE round transitions. So no existing test is broken by r86-88; the three scenarios are the only ones they make red.

## 5. A step the work-item skips

The non-DONE path must not stop at `return`. The existing way for a faulted round is `keep_round` (run a-turn):
- commits `runs/<name>/<k>-<stage>/` and `log.jsonl` (`work: p1 gate round 1-gate faulted`), run;
- pushes that commit, `git_push`, so `main == origin/main` after it, run;
- keeps the round branch `round/p1-1-gate`, run;
- raises the Refused that names the round and how it ended, run.

A non-DONE path that returns without `keep_round` would leave the stage directory and log lines uncommitted. The next run's check refuses uncommitted changes under `.shop/work/` (supervise.py:85, r46), read. A non-DONE gate path that writes questions goes through `move()`, which commits the transition itself (run, a-blocked: `work: p1 drafted -> awaiting-answer`). A non-DONE path must not use it, read.

## 6. Defects

**D1. A gate round that gives BLOCKED moves the proposal (r86, r87).**
Reproduce: `python3 -m pytest -q -s -n 0 .shop/scratch/w154-1-research/probe_rounds.py::test_a_gate_blocked` (run).
Came back: exit 0; p1 `awaiting-answer`; log `drafted -> awaiting-answer, by work run`; commit `work: p1 drafted -> awaiting-answer`; `## Questions` written. Requirement: keep `drafted`, no transition, exit with an error.

**D2. An apply round that gives BLOCKED moves the proposal on, through formulate to formulated (r86, r87).**
Reproduce: `python3 -m pytest -q -s -n 0 .shop/scratch/w154-1-research/probe_rounds.py::test_b_apply_blocked` (run).
Came back: exit 3; p1 `formulated`; starts: `# apply of p1`, `# formulate of p1`; log `awaiting-answer -> approved`, then `approved -> formulated`; the asked question "Is the old reader kept?" written nowhere.

**D3 (question, not a defect as stated).** `work run i1` exits 0 while p1 is `awaiting-answer` (a-done, a-blocked). r81 gives the error only for a run with no initiative (its example names a proposal awaiting-answer). Reproduce: `probe_rounds.py::test_a_gate_done_baseline`.

## 7. The file set

Production (must change):
- scripts/supervise_rounds.py (92 lines; room 208): `Rounds.round`: check `status`; a non-DONE keeps the status, makes no `move`, calls `keep_round`, raises Refused naming the round and how it ended; the gate's questions per the Questions reading. Found by runs b-blocked, a-blocked and read of round() and rounds().

Tests and stand-in (must change):
- tests/scripts/stub_claude.py (258 lines; room 42): the plan must be keyed by round kind (the brief's `# <kind> of <name>` heading), so apply and formulate can differ. Found by search: stub_claude.py:181 and supervise_rounds.py:58.
- tests/scenarios/supervision_rounds_steps.py (158 lines; room 142): the Givens for a turn-limit gate, a BLOCKED apply and an apply-then-formulate with no result; the Then for the apply round without `given the answers` (line 134 regex); the Then "log.jsonl gives no transition made after the apply round had ended"; the Then "names the formulate round of p1 and that it left no result it can read" (match the real text). Found by search (feature lines 1053-1073, §1).
- tests/scenarios/test_supervision.py (250 lines; room 50): the Then "p1 is drafted" if not placed in rounds_steps. Found by search (test_supervision.py:129).

Not changed, checked: scripts/supervise.py (237; room 63; `run()` lets the Refused out, read); scripts/supervise_worker.py (242; room 58; `worker()` already raises a Fault for cut-short and no-result sessions; read); scripts/supervise_faults.py (160; room 140; `cut_short` and `session_end` already name the end, run c-apply-turn); scripts/work (147; room 153; the CLI prints the Refused, run); scripts/workqueue.py (286; room 14; `move`, used by round, unchanged); scripts/supervise_merge.py (135; not on the proposal path, read); features/supervision.feature (not changed; scenarios fixed).

## Questions for the plan

1. §3 row 2 (r85 vs r86/r87): does a non-DONE gate round write its questions under `## Questions`? r85 says "ends"; r86/r87 keep the status and make no transition. Reading A: questions written, status kept (so the question list grows on a proposal still `drafted`). Reading B: nothing written, the round faults.
2. §3 row 4 (r84 vs r86): an integrate round starts the initiative at `started` before its session. When it gives BLOCKED or faults, should the initiative (A) stay `started` (the status r84 gives), or (B) go back to `proposed`? r86 says "keep the status", which reads either as the status before the round or the status the round began with.
3. D3: should `work run <initiative>` with a proposal `awaiting-answer` exit with an error, as r81 requires for a run with no initiative? I have not decided it.
4. The Then for r88 (feature line 1073) names "left no result it can read"; the message says "wrote no result file". Change the step's match or the message?
