# w199 research notes

Method. No coverage map: `tools tests-of` and `untested` answer "no map", so test lists are `by search`. `tools refs` misses calls through `self.`: `outcome` shows 0 references, yet it is called at scripts/supervise.py:170 and scripts/supervise_merge.py:101; callers below are `by search`. `tools size --limit 300` prints nothing: no tracked file is over 300.
This session's pytest carries `PYTEST_ADDOPTS=--work-item w199` (the environment's own): it collects 76 of the feature's 275 items, the accepted scenarios. Other scenarios (retired r3, r5, r16, r112, r113 deprecated ones) cannot run here: `-p no:work_items` is refused by that option. They are `read` only.
Probe files: `.shop/scratch/w199-1-research/probe_faults.py`, `probe_research.py`, `probe_answers.py`. Run: `python3 -m pytest -q -s -n 0 -p no:cacheprovider -p no:warnings <path>`.

## 1. Why each scenario is red today

Command for each: `python3 -m pytest -q --tb=line -rfE tests/scenarios/test_supervision.py -k "<name>"` (run). First batch: 52 failed, 2 passed. Second batch: 3 passed.
Every red below is a Given or Then with no step definition (StepDefinitionNotFoundError); the When and Then were not reached. Line numbers are features/supervision.feature.

- r4, line 118 (5 cases): undefined Given "the implementer's result gives no question, the implementer committing feature.txt, and every other worker gives DONE" (line 122). Missing: the step, in tests/scenarios/supervision_given.py or a new module.
- r61, line 472: undefined Given "each implementer's result gives no question, each implementer committing a file named for its work-item…" (line 476).
- r31, line 682: undefined Given "the planner's result gives a plan, no question and a `fileset` of…" (line 686).
- r45, line 904 (4 cases): undefined Given "the researcher's session ends in an error" / "ends at its turn limit" / "exits with an error" / "leaves output that holds no JSON result" (line 908).
- r128, line 956 (5 cases): undefined Givens at lines 967 (researcher, turn limit), 968 (gate round, error), 969 (apply round, no result), 970 (integrate round, turn limit), 971 (answering session, error).
- r129, line 973 (5 cases): undefined Givens at lines 984-988: researcher's and planner's and implementer's and reviewer's result giving questions, and the formulate round's result.
- r130, line 990 (4 cases): undefined Givens at line 994 ("the <who>'s result gives no question and <output>").
- r131, line 1005 (4 cases): undefined Givens at line 1009 ("gives no question and no file set" / "no plan" / "commits … which fail" / "no findings").
- r132, line 1021 (10 cases, all red): undefined Given "the <stage>'s result gives <output>, and every other session gives DONE" (line 1025).
- r133, line 1043: undefined Given "the researcher's result gives the outcome BLOCKED, a file set of scripts/thing.py and no question…" (line 1047).
- r134, line 1052: Givens defined; undefined Then "q1 is awaiting-asker, as `work turn` set it when the round passed the turn" (line 1058).
- r89, line 1365 (3 cases): "ends in an error, its result file answering…" and "ends with no error and before its turn limit, having written no result file…" undefined (line 1370). The turn-limit case PASSES.
- r90, line 1393 (3 cases): undefined Given "…writes notes.md beside its brief and <ending>" (line 1397).
- r86, line 1524: PASSES.
- r87, line 1543 (3 cases): undefined Givens "the gate round for p1 ends in an error, its result giving the question…", "the apply round for p1 ends at its turn limit, its result giving a change list…", "the integrate round for i1 ends with no error…".
- r88, line 1569 (3 cases): the same three undefined Givens as r87.
- r115, line 1601 (3 cases): all PASS (error, turn limit, no result).

Code behind them: the red is vocabulary, so the code paths are judged by the probes in part 2 and by `read` in part 3.

## 2. What the system answers today

Each probe builds its own repository and stand-in in the scratch directory, and runs scripts/work run i1 through its entry point. Each is `run`.

- P-a researcher BLOCKED, file set given, no question (probe_research test 1). exit 3; w1 drafted to awaiting-answer; question "code-scout gave BLOCKED: the stand-in's code-scout". No planner started. r133 wants researched.
- P-b researcher DONE, question "Is the old reader kept?", file set (test 2). w1 drafted to researched; the planner's brief (runs/w1/2-plan/brief.md line 11) holds the question. No question on w1. Matches r129 for DONE (brief path via supervise_brief.py:126-136).
- P-c researcher DONE, no file set, no question (test 3). w1 drafted to researched with no question. r131 wants awaiting-answer naming the file set.
- P-d researcher PARTIAL, question, file set (test 4). w1 drafted to awaiting-answer; the question is on w1's ## Questions. No planner started. r129 wants researched and the planner's brief.
- P-e researcher DONE with `fileset` in its result (test 5). w1.md after: no `fileset:` line. Only the planner's file set is written (scripts/supervise.py:171). r132 counts a researcher's file set as its output; nothing writes it.
- P-f gate round ends in error (probe_faults gate_error). exit 1; stderr "the gate round of p1 (.shop/work/i1/runs/p1/1-gate) faulted, and p1 keeps its status drafted: its round's session ended on an error during execution (error_during_execution…)". p1.md: no ## Faults, no status change, nothing printed by `show`.
- P-g gate round, no result file (gate_noresult). exit 1; stderr "…its round wrote no result file; its session ended as a success (success, 1 turns, exit code 0)". No ## Faults. "left no result `work run` can read" is absent.
- P-h gate round gives BLOCKED, no question (gate_blocked). exit 1; stderr "…gave the outcome BLOCKED, and p1 keeps its status drafted: the stand-in's initiative-round". No ## Faults.
- P-i answering session ends in error under a delegation (probe_answers test 1). exit 1; stderr "the session answering w1's question faulted: its answerer's session ended on an error during execution…". w1.md unchanged, question unanswered (r89 holds). Commit "work: w1 answer round 1-answer faulted" keeps the stage directory (r90 holds). No ## Faults on w1 (r128 wants one).
- P-j answering session, no result file (test 2). exit 1; the same shape, "its answerer wrote no result file; its session ended as a success".
- Nearest cases not probed (read): gate round with a question and a non-DONE status (supervise_rounds.py:113 refuses, the question is lost); planner with no plan (outcome() returns none on DONE, so the work-item moves to ready); intake round with a question (supervise_intake.py:88-112 writes the question, no status change).
- Extra nearest case from P-a/P-b: a researcher's DONE questions reach the planner only because supervise_brief.py:132 reads them on DONE. That keys on status (part 3).

## 3. Old assumptions

Each row is `read`, with the probe where one shows it. "tests that execute it" is `by search`: scenarios in tests/scenarios/test_supervision.py drive scripts/work run, and no map exists to narrow them.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_worker.py:outcome (244-251) | DONE gives no question whatever the questions; any other status gives its questions or "X gave S" | r129-r133: decided by the output and the questions, not the status word | test_supervision.py scenarios of r4, r61, r31, r130, r131, r132, r133 (by search) | grep `outcome(`; refs gives 0 (self-call) |
| scripts/supervise.py:stage (156-173) | question from outcome() routes the node to awaiting-answer; the researcher's question too | r129: a researcher's questions go into the planner's brief, node to researched | P-d; r129 scenarios (by search) | read; P-d |
| scripts/supervise.py:stage (171) | `fileset` written only for bdd-planner | r132: a researcher's file set is its output | P-e; r132 researcher row (by search) | read; P-e |
| scripts/supervise.py:stage (170-173) | no check that a stage's output is present; reviewer DONE goes to green | r131: a missing output asks the person | P-c; r131 rows (by search) | read; P-c |
| scripts/supervise.py:step (145-149) | planned to ready with no worker | r130/r131 do not name planned; no output check | none (no scenario reaches planned without a planner) | read |
| scripts/supervise_brief.py:research_questions (126-136) | the planner gets the researcher's questions only when its status is DONE | r129: any status with questions; r133 says status decides nothing | r16 deprecated scenario (features line 393, read); P-b | read; P-b |
| scripts/supervise_rounds.py:run_round (113-117) | a round whose status is not DONE is kept and refused, questions unread | r129/r133: a gate, apply or formulate round's questions go to the node; status decides nothing | r87/r88 non-deprecated (by search); r115 (PASS) | read; P-h |
| scripts/supervise_rounds.py:run_round (106-112) | a round's fault becomes Refused naming it; keep_round only; no record on the node | r128: recorded and printed as a fault of the node | P-f, P-i; r128 rows (by search) | read; P-f |
| scripts/supervise_rounds.py:run_round (119-125) | integrate DONE without change list refused | r96 (not in this item's accepts): unchanged | r96 scenarios (by search) | read |
| scripts/supervise_faults.py:fail (79-90) | records a fault only for work-items (status failed, ## Faults) | r128: a fault of the node, of any kind | P-f, P-i (by search) | read |
| scripts/supervise_faults.py:cut_short / session_end (127-156) | wording "ended on an error during execution", "ended as a success" | r88: the words "ended in an error", "left no result `work run` can read" | P-f, P-g; r88 rows (by search) | read; P-f, P-g |
| scripts/supervise.py:show (238-245) | prints a fault only for a failed node | r128: prints each node with its fault | none for proposals (no scenario prints one) | read |
| scripts/supervise_intake.py:take (88, 108) | intake DONE gate; questions written before merge | r133 generalised; r134: status stays as work turn wrote it | r134 (by search; Then undefined) | read |
| scripts/supervise_answers.py:ask (119-125) | an answer is written only on DONE with a non-empty answer; faults refused | r133 (output decides); r89/r90 keep the unanswered path | r89 turn-limit case (PASS); r90 (by search) | read; P-i, P-j |
| scripts/supervise_merge.py:claimed (101-106) | implementer's DONE gates the merge through outcome() | r130/r131 implementer rows; r4 cases | r4 scenarios (by search) | grep `self.outcome(`; read |

## 4. Tests the requirements make impossible to keep

Searched: `tests/` for BLOCKED, keeps its status, faulted, no transition (`by search`). Found only the step files below. No map.

- tests/scenarios/supervision_rounds_steps.py:247-250, "the apply round gives BLOCKED" (given). Used by the retired r87 scenario (line 1533). Retired: removed with it. Not a conflict once retired.
- tests/scenarios/supervision_formulate_steps.py:49-50, "the gate round gives BLOCKED", used by the retired r115 deprecated outline. Retired likewise.
- features/supervision.feature lines 150-163, deprecated r5 "a researcher that gives <outcome> makes the work-item's transition to awaiting-answer": QUESTION and BLOCKED rows contradict r129 and r133. Not in the work-item's Retires list. Not run here (`read`). The plan must retire it or the test fails.
- features/supervision.feature lines 135-148, deprecated r5 "an implementer's DONE whose tests fail makes…awaiting-answer": consistent with r4 (a refused merge asks), `read`. Not in Retires: the plan decides.
- features/supervision.feature line 63, deprecated r3 "a worker's outcome DONE makes the transition": consistent with r133 for DONE (`read`).
- features/supervision.feature line 393, deprecated r16 researcher's DONE questions to the planner's brief: consistent with the new spec, passes today (`read`).
- features/supervision.feature lines 1505-1520, deprecated r112/r113 formulate questions: consistent with r129's formulate row (`read`).
- tests/scripts/test_supervise_answers.py:46-50, a reviewer's item with no verdict stays: read, sound (the verdict path is r120's, not changed).
- tests/scripts/test_agents.py:79-85 (r44 PARTIAL in briefs): read, sound.
- none else found by search for the accepted requirements.

## 5. A step the work-item skips

- Round and answering-session faults. The existing way for a worker's fault is `Run.fail()` (scripts/supervise_faults.py:79-90): status to failed, `## Faults` bullet, commit, push, the fault kept for the exit (`self.faults`). A round fault takes `keep_round()` only (scripts/supervise_rounds.py:183-192): commit and push of the stage directory. Effects only `fail()` produces: the `## Faults` bullet, the printed fault line (supervise.py:243-245), and the failed-push note. Shown by P-f, P-i (no ## Faults). Read: workqueue.py:15-18 lists `failed` among the statuses and :155 lets a capability-proposal move to its own list plus those, so a proposal can be failed; r86 and r88 keep its status. The plan must pick which.
- Researcher's file set. The planner's way writes it with `write_fileset()` (supervise.py:136-142), gated on bdd-planner and a non-empty list (supervise.py:171). The researcher has no such step. Effect only that step produces: a `fileset:` line in the work-item (research_lines reads it, supervise_brief.py:142). Shown by P-e.
- Intake question path. `take()` writes each question with workqueue_request.ask, then merges (supervise_intake.py:88-99), with no status change. Read.
- Answer on a non-DONE answering session. The answer is dropped with no record (supervise_answers.py:119-120). Read.

## 6. Defects

Each is against the capability text as it stands (spec/capabilities/supervision.md). Commands: the probe test names above.

D1. r128: a round's fault is not recorded or printed under its node. Repro: `python3 -m pytest -q -s -n 0 -p no:cacheprovider -p no:warnings .shop/scratch/w199-1-research/probe_faults.py -k gate_error`. Came back: exit 1, p1.md with no `## Faults`, stderr only. Same for the answering session (probe_answers.py test 1: w1.md no `## Faults`).
D2. r88 wording: the error and no-result messages lack "ended in an error" and "left no result `work run` can read". Repro: probe_faults.py `-k "gate_error or gate_noresult"`. Came back: "ended on an error during execution" and "wrote no result file; its session ended as a success".
D3. r133: a researcher's BLOCKED with a file set goes to awaiting-answer. Repro: probe_research.py `-k blocked`. Came back: exit 3, "w1 awaiting-answer", question "code-scout gave BLOCKED: the stand-in's code-scout".
D4. r131/r132: a researcher's DONE with no file set goes to researched without a question. Repro: probe_research.py `-k nofileset`. Came back: "drafted → researched", planner started, no question naming the file set.
D5. r129: a researcher's PARTIAL with a question goes to awaiting-answer, not into the planner's brief. Repro: probe_research.py `-k partial`. Came back: "drafted → awaiting-answer", question on w1's ## Questions, no planner.
D6. Conflict, for the plan (read, not run): r129 says a session whose result gives questions sends them to the node's ## Questions and makes it awaiting-answer. r87 (non-deprecated) says a round cut short brings no transition. A gate round that gives BLOCKED with a question is neither: today it is refused and p1 stays drafted (probe_faults.py gate_blocked, with no question). Reading A: r129 applies, the question goes to p1 and p1 is awaiting-answer. Reading B: a non-DONE round is refused as today, as r87's deprecated scenario held.

## 7. The file set

Production files, each with the change and the reading that shows it:
- scripts/supervise.py (275 lines, room 25): stage() outputs and question routing (r129-r132); show() prints faults of any node (r128); researcher's file set (decide). Read, P-a to P-e.
- scripts/supervise_worker.py (251, room 49): outcome() decides by output, not status (r129-r133). Read; callers at supervise.py:170 and supervise_merge.py:101.
- scripts/supervise_rounds.py (192, room 108): round faults recorded under the node (r128); non-DONE round with questions (r129/r133, D6); error wording (r88). Read; P-f, P-g, P-h.
- scripts/supervise_faults.py (161, room 139): fail() for any node (r128); session_end wording (r88). Read.
- scripts/supervise_answers.py (144, room 156): answering fault recorded (r128); DONE gate (r133). Read; P-i, P-j.
- scripts/supervise_intake.py (123, room 177): take() DONE gate (r133/r134). Read.
- scripts/supervise_brief.py (171, room 129): research_questions keyed on DONE (r129). Read; P-b.
- scripts/supervise_merge.py (135, room 165): claimed() via outcome() (r4/r130/r131). Grep.

On the change's path, edit not expected:
- scripts/workqueue.py (294, room 6): lifecycle statuses; any addition there breaches 300. Read.
- scripts/workqueue_request.py (186, room 114): ask() and the intake's requests; no change expected. Read.
- scripts/supervise_pool.py (143, room 157): pull and choose, unchanged. Read.
- scripts/supervise_review.py (82, room 218): branch review, unchanged. Read.
- scripts/supervise_draft.py (122, room 178), scripts/supervise_all.py (83, room 217), scripts/supervise_done.py (36, room 264), scripts/supervise_analysis.py (80, room 220): unchanged. Read.

Test files:
- tests/scenarios/test_supervision.py (262, room 38): imports the step modules and `scenarios(...)`; add the new step module's import. Read.
- New module, e.g. tests/scenarios/supervision_outputs_steps.py: Givens "the <who>'s result gives …" for r129-r134, r4, r31, r45. New file, room 300.
- tests/scenarios/supervision_given.py (265, room 35): too little room for the new Givens; keep to the one step module above.
- tests/scenarios/supervision_rounds_steps.py (288, room 12): round Givens for r87/r88/r128 ("ends at its turn limit", "ends in an error", "no result"). Must go in a new module or a split.
- tests/scenarios/supervision_then_workers.py (279, room 21): planner brief and w1's fault Thens for r129 and r128.
- tests/scenarios/supervision_intake_steps.py (99, room 201): the r134 Then "q1 is awaiting-asker…". Read.
- tests/scenarios/supervision_faults_steps.py (199, room 101): Thens for "recorded as a fault". Read.
- tests/scripts/stub_claude.py (274, room 26): no change needed: status, subtype, result, fields and questions cover every Given. Read.
- features/supervision.feature (1780): retire lists and the r5 deprecated researcher outline (D6 and part 4). Read.

Counts are `wc -l`; room is 300 minus the count.
