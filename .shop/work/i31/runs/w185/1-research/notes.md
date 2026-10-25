# w185 research notes

Method: `tools refs` for names (supervise_rounds.run_round, due, move). `tools tests-of` has no map ("no map: make one with tools map"); not made, so every test list below is `by search` or `none`. Tools run from `/home/vscode/shopsystem-bdd/scripts`. Probe: `.shop/scratch/w185-1-research/probe_rounds.py` (stub worker `stub_claude.py` beside it), run as `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w185-1-research/probe_rounds.py`.

## 1. Why each scenario is red today

Run: `python3 -m pytest -q --tb=short -p no:cacheprovider "<node id>"` for each, node ids from `--collect-only`.

- r111 "an initiative that a work-item's transition leaves able to be done is set done before `work run` ends" (test_supervision.py::test_an_initiative_that…): red, StepDefinitionNotFoundError on Given "i1 is started and its work-item w1 is ready" (feature 865). No step matches: supervision_done_steps.py:11 needs "work-items w1 is green and w2 is withdrawn"; supervision_tests_steps.py:99,107,148 need "accepting". Then "w1 is green" and "i1's transition to done was made after w1's transition to green, before `work run` exited" have no definition (searched by text). Code: supervise.py:208-218 already runs set_done after pull (read). Not verified past the Given.
- r70 "a capability-proposal whose every question has an answer is given to an apply round with its answers": PASSES today (run). Steps rounds_steps.py:17, 208; brief answer_lines (supervise_brief.py:110-120) writes "Answer:" lines.
- r116 "…every question from its formulate round has an answer is given to a formulate round": red, undefined Then "a round of the kind formulate was started for p1, given the answer "One place."" (rounds_steps.py:208 `apply_started` takes only apply). Given matches answered_proposal (rounds_steps.py:17). Code: supervise_rounds.py:19, 46-48 send any awaiting-answer proposal with answers to apply (probe confirms).
- r114 "…the proposal's adds, changes and removes are written from the change list the round applied": red, undefined Givens: "i1's capability-proposal p1 is awaiting-answer, its adds naming …, given by its gate round, and its Answers section with "No."" (answered_proposal's regex needs "its ## Questions" straight after the status); "the apply round for p1 gives DONE with a change list that adds thing#r4 and changes thing#r2 on thing" (only apply_blocked, rounds_steps.py:234); "every other round ends and every worker gives DONE" (rounds_steps.py:98 has no "other"). Then "p1's adds name … and its removes name nothing" undefined. Code: supervise_rounds.py:99-106 reads `changes` only for integrate; :116 moves an apply without writing lists (probe: adds unchanged).
- r83 new "…ends without giving a question, the proposal is formulated": red, undefined Given "the formulate round for p1 gives DONE with no question" (no formulate-result step; the plan key `round:formulate` is read by none). Then "p1's transition to formulated…" is defined (rounds_steps.py:272). Code: AFTER map (supervise_rounds.py:19) gives approved→formulated already.
- r83 deprecated "…the proposal is formulated (deprecated)": PASSES today (run). Retired by w185.
- r112 "…gives questions, each is written under the proposal's ## Questions": red, undefined Given "the formulate round for p1 gives DONE with the questions …". The Then "p1's ## Questions holds "…" and "…"" matches rounds_steps.py:57 `questions_hold`, which calls gate_question (rounds_steps.py:37) unpacking four quoted strings, so it fails on two. Code: supervise_rounds.py:111 sets `asked` only for kind gate.
- r113 "…gives a question, the proposal is awaiting-answer": red, undefined Givens "the apply round for p1 ends, and the formulate round for p1 gives DONE with the question …" and Then "p1's transition from approved to awaiting-answer was made once the formulate round had ended"; "p1 is awaiting-answer" matches no step (rounds_steps.py:247 accepts only "drafted"). Code: supervise_rounds.py:111, 116 (probe: formulated).
- r115 Outline, four cases: red, undefined Givens "the gate round for p1 gives BLOCKED, asking …, and every worker gives DONE", "…ends in an error, and every worker gives DONE", "…ends at its turn limit, and …", "…ends with no error and before its turn limit, having written no result file, and …" (rounds_steps.py:229 matches only "session ends at its turn limit, its result giving …"). Then "w1 is green": no definition (searched, parsed patterns too). "it exits with an error" is defined (test_supervision.py:110). Code: supervise.py:205 `self.rounds()` runs before `self.pull` and `self.draft` (206-207); a Refused leaves pull_through unwound (probe).

## 2. What the system answers today

Probe 1, `probe_rounds.py` (four tests, each a real `work --root <repo> run i1`, stub worker writing STUB_PLAN's result per stage). Ran: `run`, 4 passed.

- r115 case (p1 drafted, w1 drafted, gate gives BLOCKED with a question): exit 1; stderr "work: the gate round of p1 (.shop/work/i1/runs/p1/1-gate) gave the outcome BLOCKED, and p1 keeps its status drafted: asks"; p1 drafted; w1 drafted (never moved); log has gate push/start/end only. Other node not taken through (r115 unmet).
- r113 case (p1 awaiting-answer, answered; apply DONE; formulate DONE with question "Are returns counted?"): p1 ends `formulated`; log `approved -> formulated` after formulate end; the question is not in `## Questions` (only "Is a shelf one place or a list?" there); the run then drafted w2 for p1 (`supervise_draft.draft_proposals`), so work-items came from a proposal with an open question. Exit 3 from w1's fixture suite failure (unrelated).
- r114 case (p1 awaiting-answer, adds thing#r4 thing#r5; apply DONE with changes adds thing#r4, changes thing#r2): p1 ends formulated with `adds: [thing#r4, thing#r5]`, `changes: []`; the apply's change list is not read.
- r116 case (p1 awaiting-answer from log line `approved -> awaiting-answer`, question from its formulate round, answer "One place."; all rounds DONE): log shows `apply start` then `apply end`, `approved -> formulated`; no formulate round started before formulated. The answer went to apply.
- r70 and r83-deprecated: passing scenarios (run, section 1).

Read, not run: the nearest cases. Zero questions and zero answers: due() sees 0 >= 0 and sends nothing (supervise_rounds.py:46-47). Answers one short of questions: waits. formulate with questions while Answers already holds the old answer: the open question is the one past Answers (supervise.py:188-191).

## 3. Old assumptions

Table: place | what it does today | what the requirement makes of it | tests that execute it | found by

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| supervise_rounds.py:19, :46-48 (AFTER map, due) | awaiting-answer with every answer → apply, whichever round asked | r116: an answer to a formulate round's question → formulate. The asking round must be known (see last row) | test_supervision.py r70, r80, r71 scenarios; supervision_rounds_steps.py (by search) | refs due; read; probe r116 |
| supervise_rounds.py:111 (`asked = … if kind == "gate"`) | a formulate round's questions are dropped | r112, r113: written under ## Questions; status awaiting-answer | none | read; probe r113 |
| supervise_rounds.py:116 (`move(name, before, after, asked)`, after fixed by AFTER) | status after a round set by its kind, not by its questions | r113: formulate with a question → awaiting-answer | test_supervision.py r83 deprecated and r83, r71 (by search) | read; probe r113 |
| supervise_rounds.py:99-110 (`entries`, `unknown`, refusals for integrate only) | an apply round's `changes` are never read | r114: adds/changes/removes written from the applied list | none | read; probe r114 |
| supervise_change.py:52-72 write_proposals | writes a proposal's three lists once, at integrate | r114: the same lists rewritten after apply | supervision_integrate_steps.py "adds naming" Thens (by search) | read |
| supervise_draft.py:36-54 draft_proposals | drafts work-items from a formulated proposal's adds/changes in the file | after r114 those are the applied lists; after r113 "formulated" means no open question | supervision_proposal_steps.py r72/r73 files written directly (by search) | read; probe r113 (w2 drafted) |
| supervise.py:205-207 pull_through (rounds() before pull/draft) | a Refused from a round skips every other node | r115: other nodes taken through their transitions first | test_supervision.py r86, r87, r88, r115 (by search); supervision_rounds_steps.py:229-244 | read; probe r115 |
| supervise.py:193-199 run() (show and asked after pull_through) | a Refused skips the status print and the awaiting-asker check | r115 says exit with error; the print of each node is not required by r115 but comes after the other nodes now move | test_supervision.py r88 checks only the message (by search) | read |
| workqueue.py:142-167 move() | log line carries before/after, no stage | r116 needs the asking round: the only record is `before` (drafted = gate, approved = formulate) or a field the plan adds | test_work_queue.py move tests (by search) | read |
| workqueue_answer.py:73-74 (proposal answer) | writes the answer only; status stays awaiting-answer | the route alone decides what the answer goes to | none (no test for answering a proposal found in search of supervision steps) | read |
| supervise_rounds.py:46-47 count rule | open questions = Questions past Answers, pairwise | holds for r112 (new questions appended after the answered ones) | none | read |

## 4. Tests the requirements make impossible to keep

tests-of gave no list (no map). Searched by text: tests asserting round behaviour in supervision_rounds_steps.py, test_supervision.py and supervision_proposal_steps.py.

- test_supervision.py r83 deprecated scenario (feature 1233): passes today and passes under the new code (the stand-in gives no question). Retires removes it: removal, not a conflict.
- test_supervision.py r70 scenario (feature 948; rounds_steps.py:17 Given writes no log line): passes today. It stays green only if awaiting-answer with no formulate provenance still goes to apply. Sound if that default is kept.
- rounds_steps.py:229-244 with features 1269-1293 (r86, r87, r88): the initiative holds only p1, so r115's "other nodes" are none; they stay sound. Checked by reading the feature lines and steps.
- test_supervision.py r115 Outline (feature 1296): red today; it is an accepted scenario, so it changes from red to green, not kept.
- Nothing else found asserting that a formulate round's questions are dropped or that an apply's change list is ignored: no test does either (by search).

## 5. A step the work-item skips

- The round's failure path (rounds() raising Refused, supervise_rounds.py:91-97, keep_round 141-150, `git merge --abort` 89). Effects only that path gives: the Refused message naming round and status; keep_round's commit of the stage directory and log lines with a push. When pull_through goes on past it (r115), these must still happen. Probe r115 shows the message and the log lines; the commit is read only.
- The formulate round's questions: the question argument of move (supervise.py:115-116, section 121-134) writes bullets under `## Questions`; it is reached only with `asked` set, which only gate sets (supervise_rounds.py:111). Probe r113 shows the write is missing.
- The apply round's change list: the integrate path's entries() refusal (supervise_change.py:13-31, supervise_rounds.py:99-103 "its result cannot be read"), the empty-list refusal (104-105, refuse_integrate 127-132) and the unknown-capability refusal (106-110, r107). An apply's list would skip all three and write unchecked ids into the proposal. Read only.
- An apply or formulate round that r116 bypasses for an answer to a formulate question: its branch merge into the initiative branch (supervise_rounds.py:84-85) and its approved transition are skipped. Read only.

## 6. Defects

Each reproduced with the probe above. Command for each: `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w185-1-research/probe_rounds.py::<name>`.

D1. A formulate round's question is dropped and the proposal is formulated: `test_r113_formulate_gives_question`. Output: `status: formulated`, `## Questions` holds only the old question, log `formulate end`, `approved -> formulated`, and w2 drafted from p1.

D2. An answer to a formulate round's question starts an apply round: `test_r116_formulate_question_answered`. Output: log `approved -> awaiting-answer`, then `apply start`/`apply end`, `awaiting-answer -> approved`, `approved -> formulated`. No formulate round.

D3. An apply round's change list is ignored: `test_r114_apply_change_list`. Output: `adds: [thing#r4, thing#r5]`, `changes: []`, status formulated.

D4. A gate round's BLOCKED stops the initiative's other nodes: `test_r115_gate_blocked_then_other_nodes`. Output: exit 1, w1 still `drafted`. (Accepted r115 says otherwise; listed so the plan sees it is a behaviour, not a missing step.)

## 7. The file set

Tests and features the scenarios need, then the production files.

Production:
- scripts/supervise_rounds.py: due() routes by the asking round (r116); run_round keeps formulate questions and moves to awaiting-answer (r112, r113); reads apply's change list (r114). Read: 150 lines.
- scripts/supervise_change.py: rewrite of a proposal's adds/changes/removes from the applied list (r114), reusing entries(). Read: 72 lines.
- scripts/supervise.py: pull_through runs pull and draft before a round's Refused propagates (r115). Read: 265 lines.
- scripts/workqueue.py: no change expected; the route can read the log's `before` (r116). Only a `stage` field in move's log line would touch it. Read: 290 lines, room 10.

Tests and features:
- features/supervision.feature: delete the r83 deprecated scenario (lines 1233-1240), as w185's Retires says. Read.
- tests/scenarios/supervision_rounds_steps.py: 275 lines, room 25. Generalise apply_started to any kind (r116 Then), add the formulate-result and gate BLOCKED/ending Givens, the proposal status Then for awaiting-answer, and the "approved to awaiting-answer" Then (r113). Not enough room: put them in a new module.
- tests/scenarios/supervision_formulate_steps.py (new module; CLAUDE.md module map needs its row): the Givens and Thens of r112, r113, r114, r115 and the r111 Givens. Read.
- tests/scenarios/test_supervision.py: 260 lines, room 40: one import line for the new module (the scenario bindings come from scenarios("supervision.feature")). Read.
- tests/scenarios/supervision_done_steps.py (39 lines): a Given for "i1 is started and its work-item w1 is ready" (r111). Read.

Modules on the change's path, edited or not (wc -l; room under 300; `tools size --limit 300` printed no file over the limit):
- scripts/supervise.py 265, room 35 (edited)
- scripts/supervise_rounds.py 150, room 150 (edited)
- scripts/supervise_change.py 72, room 228 (edited)
- scripts/workqueue.py 290, room 10 (not edited)
- scripts/supervise_draft.py 81, room 219 (not edited)
- scripts/supervise_brief.py 167, room 133 (not edited; gate/apply briefs and answer_lines)
- scripts/supervise_worker.py 251, room 49 (not edited; worker, session)
- scripts/supervise_analysis.py 80, room 220 (not edited; r111 analyse path)
- scripts/supervise_done.py 36, room 264 (not edited; r111 set_done)
- scripts/supervise_intake.py 123, room 177 (not edited; uses due() through supervise_rounds, refs)
- scripts/workqueue_answer.py 77, room 223 (not edited; proposal answer, section 3)
- tests/scenarios/supervision_rounds_steps.py 275, room 25 (edited)
- tests/scenarios/test_supervision.py 260, room 40 (edited)
- tests/scenarios/supervision_proposal_steps.py 153, room 147 (not edited; drafts from formulated files)
