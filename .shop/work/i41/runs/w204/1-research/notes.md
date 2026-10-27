# w204 research notes

Checkout HEAD 6b5ae35e (brief base c2cbb99c). `tools map` made at 6b5ae35e, so its answers are current. `tools tests-of` on `Rounds.*` finds no test because the scenarios run `work run` as a subprocess, which coverage does not follow: those answers are `by search` below. Scenario runs: `python3 -m pytest -q -n 0 <node id>`. Probe: `.shop/scratch/w204-1-research/probe_rounds.py`, run `python3 -m pytest -q -s -n 0`. The probe calls the functions directly with stubs, not through `work run`.

## 1. Why each accepted scenario is red today

All nine are collected by node id (`tests/scenarios/test_supervision.py::...`) and each fails at its first step with `StepDefinitionNotFoundError` (run). Steps not yet defined are listed in full (read: grep of the step decorators).

- r140 `..._is_followed_by_a_new_integrate_round_for_the_proposal`: run fails at Given "i1 is started and fulfils the request q1, whose line 1 has the line outcome accepted". Also undefined (read): "the apply round for p1 applies nothing, giving that p1's answers give what its drafts do not hold"; Then "a round of the kind integrate was started for p1 after the apply round had ended" (rounds_steps:237 matches apply|formulate only). Code: `supervise_rounds.py` `AFTER` (line 20) and `Rounds.route` (53-62) send an awaiting-answer proposal to apply then approved; no integrate route exists for a proposal.
- r141 `..._its_questions_and_answers_the_initiatives_ledger_and_the_accepted_lines_of_the_request`: run fails at Given "i1 is started and fulfils the request q1, whose lines 1 and 3 have the line outcome accepted and line 2 the line outcome refused". Also undefined (read): "i1's ledger holds the line ..."; Then "the integrate round for p1 was given the question ... with its answer ..."; "it was given i1's ledger"; "it was given q1's lines 1 and 3, and not line 2". Code: `supervise_brief.py` `Briefs.brief` (32-96) takes `fulfils` from the proposal's own frontmatter (`integrate_lines`, 107-118), so for p1 "Request:" is empty; no ledger is named in any brief (grep `ledger` in scripts/supervise*.py: only the supervise_worker.py:29 comment and the `work note` grant).
- r142 `..._drafts_anew_from_its_answers_is_set_drafted_...`: run fails at Given "i1 is started and fulfils the request q1, whose line 1 has the line outcome accepted". Also undefined (read): Given "i1's capability-proposal p1 is awaiting-answer, written from the change list of i1's integrate round, whose drafts are kept at ..."; Given "p1's ## Questions section holds ..., given by its gate round, and its Answers section ..."; Given "the integrate round for p1 writes spec/capabilities/thing.md under its drafts path and gives DONE with a change list ..." (integrate_steps:65 is i1 only); Then "p1's transition to drafted was made once the integrate round for p1 had ended"; Then ".shop/work/i1/runs/i1/2-integrate/drafts/round-1/spec/capabilities/thing.md is as the first integrate round wrote it". Code: `Rounds.run_round` (87-173) names the run directory by the node: `self.run_dir(name, kind)` gives `runs/p1/<k>-integrate` for a proposal, not `runs/i1/`; `Changes.write_proposals` (supervise_change.py:68-88) writes `<capability>.md`, i.e. `thing.md`, beside `p1.md`, so it cannot set p1 drafted in place.
- r143 `..._keeps_its_status_while_the_integrate_round_started_for_it_runs`: run fails at Given "i1 is started and fulfils ...". Also undefined (read): Then "p1 was awaiting-answer while the integrate round for p1 ran"; Then "no transition of p1 was made between the start and the end of the integrate round for p1"; and the apply "applies nothing" Given as in r140. Code: no move happens during an integrate round today (`run_round` 88-93 sets `before = after` and moves at 163-168 only), so the step text is the only gap as far as read goes.
- r144 `..._the_proposal_is_approved`: run fails at Given "the apply round for p1 applies p1's drafts and gives DONE with a change list that adds thing#r4 on thing". Undefined (read): that Given (formulate_steps:36 matches "gives DONE with a change list ... on thing" only, not "applies p1's drafts and gives DONE"). Then "p1's transition to approved was made once the apply round had ended" is defined (rounds_steps:245). Code path (read): `run_round` apply branch (132-162) and `AFTER` give approved after a list; probe below shows the routing.
- r145 `..._adds_changes_and_removes_are_written_from_the_change_list_the_round_applied`: run fails at Given "the apply round for p1 applies p1's drafts and gives DONE with a change list that adds thing#r4 and changes thing#r2 on thing". Undefined: that Given only. The rest are defined (formulate_steps:41 and :74). Code (read): `rewrite_lists` (supervise_change.py:53-66) rewrites the three lists from the applied entries; this is already the r145 behaviour.
- r146 `..._a_formulate_round_is_started_for_the_proposal`: run fails at the same apply Given as r144. Then "a round of the kind formulate was started for p1 after the apply round had ended" is defined (rounds_steps:251). Code (read): approved routes to formulate (`route`/`AFTER`); probe confirms.
- r147 `..._has_given_its_output`: run fails at Given "i1 is started and fulfils ...". Also undefined (read): Given "the apply round for p1 applies nothing, giving that p1's answers give what its drafts do not hold, and no change list"; Then "no question naming the apply round's output as missing was written under p1's ## Questions" (outputs_steps:117 and :131 use other wording). Code: `run_round` 143-147 asks "The apply round of <p> gave no change list" whenever an apply has neither questions nor applied entries (r131 path), so the r147 pin is contradicted by today's code.
- r148 `..._is_the_only_capabilityproposal_of_the_initiative_for_its_capability`: run fails at Given "i1 is started and fulfils ...". Also undefined (read): Given "i1's capability-proposal p1, for thing, is awaiting-answer, ..." (answered_proposal regex, rounds_steps:21, needs "p1 is awaiting-answer, "); the apply "applies nothing" Given; Given "the integrate round for p1 gives DONE with a change list that adds thing#r4 and thing#r6 on thing" (integrate_steps:41 says i1); Then "i1 has one capability-proposal for thing, and it is p1" (undefined). Code: `write_proposals` (above) writes a second proposal for `thing` (probe).

Note on the step texts: the nearest existing "i1 is proposed and fulfils the request q1, whose ..." (rounds_steps:153) takes only `proposed`; no "started" form exists.

## 2. What the system answers today (probes)

- Probe `test_routing_answered_awaiting_answer`, run: an awaiting-answer p1 with its question answered gives `('p1', 'apply', 'approved')`; with no answer, `None`. So the answer that r140 says must go back to integration goes to apply today, and the apply's move is to approved.
- Probe `test_routing_approved_after_apply`, run: an approved p1 gives `('p1', 'formulate', 'formulated')` (r146 path, unchanged).
- Probe `test_write_proposals_second_for_same_capability`, run: write_proposals for a change list naming `thing` with p1.md already holding `thing` writes `thing.md`; the proposals become `[('p1','awaiting-answer'), ('thing','drafted')]`. Today that case is not reached by routing: `Rounds.due` (35-51) starts an initiative integrate only when no proposal exists (line 40-41), so this duplicate is latent and appears only once r140 routes back to integrate.
- Deprecated scenarios r80, r114, r71: not run (run: `-m deprecated` collects none; the plain run of test_supervision.py collects only the 9 accepted ones, `-n 0`, the file's 265 items shown by the -k run). Read only.
- Not probed (read): an apply round with neither questions nor a list gets the r131 question (supervise_rounds.py:146-147); a probe of it needs the step stand-in that the r147 Givens lack. An integrate round for a proposal (new path) cannot be probed: no route exists.

## 3. Old assumptions

Requirements that change: r144 (approved after applied drafts; unchanged in its applied case), r145 and r146 (unchanged), r140/r147 (apply that applies nothing: new), r141/r142/r143/r148 (integrate for a proposal: new).

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise_rounds.py:Rounds.route, AFTER (lines 20, 53-62) | an awaiting-answer proposal goes to apply then approved; to formulate only when the log's last move into awaiting-answer came from approved | an apply that applies nothing (r140) routes to integrate for the proposal; the route needs a record of that outcome in the log or the result | none (map: no test executed; scenario tests run work run in a subprocess) | refs + read |
| scripts/supervise_rounds.py:Rounds.run_round apply branch (132-162) | apply with no list and no question asks the r131 question naming the missing change list | r147 takes an apply that applies nothing (answers give what drafts do not hold) as its output: no question | none | read |
| scripts/supervise_rounds.py:Rounds.run_round apply branch, `after = "approved"` (AFTER) | a proposal with applied entries moves to approved (r144) | unchanged for r144/r145/r146; the no-list case must not go to approved (r140) | none | read |
| scripts/supervise_rounds.py:Rounds.run_round, `label, _ = self.run_dir(name, kind)` (line 95) and `unknown(..., self.dir/"runs"/name/label)` (123) | the stage directory is keyed by the node (runs/p1/<k>-integrate for a proposal) | r142/r148: the earlier drafts are in runs/i1/2-integrate/drafts/round-1 and the second round's are kept beside them; the integrate for a proposal must keep the initiative's drafts path | none | read |
| scripts/supervise_change.py:Changes.write_proposals (68-88) | writes one file `<capability>.md` per capability, with status drafted | r142: the existing p1 is set drafted in place; r148: no second proposal for the capability | tests/scripts/test_supervise_change.py::test_two_entries_naming_one_capability_give_one_proposal_with_both_entries_ids (by map) | map + probe |
| scripts/supervise_change.py:Changes.rewrite_lists (53-66) | rewrites adds/changes/removes of the named proposal from the applied list (r114) | r145 (already): unchanged | none | refs (0 refs by name; called from supervise_rounds.py:144) + read |
| scripts/supervise_brief.py:Briefs.integrate_lines (107-118) and Briefs.brief (32-96) | "Request:" and accepted lines read from the node's own `fulfils`; no ledger line; Drafts path is the new round's `drafts`; the `kept` path is given for gate and apply only | r141: the proposal's integrate round gets the initiative's `fulfils` and ledger, the accepted lines, its questions and answers (answer_lines already reads the proposal's Q and A); r142: the earlier drafts path | tests-of: none (map: integrate_lines executed by no test) | tools tests-of + refs + read |
| scripts/supervise_brief.py:Briefs.brief, `item`/`read` (36-43) | for a proposal name, reads p1.md and runs/p1 | r141/r142 need the initiative's ledger and runs/i1 | none | read |
| scripts/supervise_outputs.py:question, unformulated (52-73) | formulate's scenario check | not changed by r140-r148 | none | read |
| scripts/supervise_rounds.py:Rounds.due (35-51) | starts an initiative integrate only when no proposal exists (r93) | r148: a proposal that exists must not start a second integrate by this rule; the new per-proposal route is needed | none | read |
| scripts/supervise_rounds.py:Rounds.run_round integrate branch (`before = after`, 88-93) | proposal integrate uses `after` as its status | r143: status kept during the round; r142: drafted at the end | none | read |

## 4. Tests the requirements make impossible to keep

Map: `tests-of` finds no test for Rounds.due/route/run_round (subprocess), so this list is by search: a search of the step decorators and the test modules for the phrases of the accepted scenarios (grep, part 1) and read of the named tests. No wider text search for old-behaviour assertions was run.

- tests/scripts/test_supervise_change.py::test_two_entries_naming_one_capability_give_one_proposal_with_both_entries_ids (executes write_proposals, by map; read): checked; it writes a first proposal for a capability with no existing proposal. Sound under r148 (r148 is the redraft case). Kept.
- Deprecated scenarios r80, r114, r71 in features/supervision.feature (not collected; read): they pin approved and formulate after an apply round, which r144 and r146 keep in the applied case. Their Retires entries retire them, so no conflict remains once they are retired.
- Scenario r131 in features/supervision.feature, outline row "apply round | p1 | ... leaves no result" (line 873) (read): its apply round gives no list and no question and expects a question naming the missing output. r147 pins the answers case as output; the no-list case still expects the question. Both readings in play: (a) an apply that applies nothing is recognised by something in its result (a field or question text) and gets no question; (b) it is recognised only by its answers, which the r131 row would contradict. Left to the plan.
- tests/scenarios/supervision_rounds_steps.py: `apply_did_its_work` (line 109-111) and `every_round_ends` (121-125) set the stand-in's apply to a change list; no step gives an apply round with no list and no question as r147 needs. A gap, not a failure.
- Verified sound (read, not run as a whole): the nine accepted scenarios as written; each fails only at its undefined steps, so nothing in them is an assertion that today's code would break.

## 5. A step the work-item skips

The new path (apply applies nothing -> integrate for the proposal) starts a round with no transition of the apply round itself. Existing way: a round that ends in `move` (supervise_rounds.py:163-164, `supervise.py:Run.move`) commits its stage directory and log lines, and a round that faults or refuses goes through `keep_round` (189-198), which commits the stage directory and log lines with no transition so the next run finds nothing uncommitted under .shop/work/ (r46). A no-list apply that starts a new integrate skips both: nothing commits the apply's stage directory and log lines before the integrate round starts. Effects only `move` produces (read): the commit message `work: <p> <before> -> <after>`, the `log.jsonl` "after" line that `Rounds.route` reads back (line 58-60). Effects only `keep_round` produces (read): the commit "work: <p> <kind> round <label> faulted" and the reset of `self.unlogged`. Not probed: no route exists. Marked read.

## 6. Defects

None reproduced today. The write_proposals duplicate (probe above) is latent: `Rounds.due` (line 40-41) starts an integrate round only with no proposal, so the duplicate needs the new route. The r131 question on an apply with no list is the specified behaviour (r131), not a defect, though it conflicts with r147 as read in part 1.

## 7. The file set

The work-item has no `fileset:` (none in its frontmatter); this list is by search and read.

Production (must change):
- scripts/supervise_rounds.py (198 lines, room 102): route the apply-applied-nothing case to integrate (r140), keep the apply's no-list output (r147), set the integrate's status and drafted at its end (r142, r143), run dir for the initiative (r142).
- scripts/supervise_change.py (88 lines, room 212): write_proposals sets the existing proposal drafted and writes no second one (r142, r148).
- scripts/supervise_brief.py (194 lines, room 106): integrate brief for a proposal takes `fulfils` from the initiative, the ledger, the earlier drafts path (r141, r142).
- scripts/supervise_worker.py (256 lines, room 44) only if the round's ledger or drafts path reach the brief through worker grants (read: its ROUNDS and `work note` grant at lines 29, 47).

Tests (must change, so the scenarios can run):
- tests/scenarios/supervision_rounds_steps.py (272 lines, room 28): Givens "applies p1's drafts and gives DONE ...", "applies nothing ...", Thens for integrate-after-apply, status kept, ledger; 28 lines of room is tight, a new module is likely needed (CLAUDE.md: a new concern gets a new module and a row).
- tests/scenarios/supervision_integrate_steps.py (201 lines, room 99): Givens for "the integrate round for p1 ...", "i1's capability-proposal p1 ... written from the change list", Then "i1 has one capability-proposal for thing".
- tests/scenarios/supervision_proposal_steps.py (152 lines, room 148): "i1's capability-proposal p1, for thing, is awaiting-answer".
- tests/scenarios/supervision_formulate_steps.py (83 lines, room 217): "the apply round for p1 applies ..." Given texts (the formulate module already holds the apply Givens).
- tests/scenarios/supervision_given.py (259 lines, room 41): "i1 is started and fulfils the request q1 ..." (the started form, next to proposed_fulfilling in supervision_rounds_steps.py:153).
- tests/scenarios/supervision_outputs_steps.py (134 lines, room 166): "no question naming the apply round's output as missing" (r147).

Modules on the change's path (read or searched; edited or not), with line counts and room:
- scripts/supervise.py (284, room 16): Run, move, section, held (176). Edited only if `move` or `held` changes.
- scripts/supervise_worker.py (256, room 44): run_dir (127), ROLES and grants, ROUNDS.
- scripts/supervise_faults.py (190, room 110): Fault, ended_of, fault_of used by run_round.
- scripts/supervise_outputs.py (73, room 227): output reading for formulate; r147's output test may read it.
- scripts/supervise_drafts.py (32, room 268): added_by_others (r102) fed to the integrate brief.
- scripts/workqueue.py (294, room 6): agrees, logged, move, frontmatter (route reads the log through `logged`). Almost at the limit: any addition there must split the module first.
- scripts/workqueue_request.py (186, room 114): accepted_lines (integrate brief).
- scripts/workqueue_note.py (21, room 279): `work note`, the ledger the round appends to.
- scripts/supervise_done.py (36, room 264): not on the path; listed for the initiative's done.
- tests/scenarios/test_supervision.py (265, room 35): the scenarios()/hook file.
- tests/scenarios/supervision_world.py (173, room 127): stand-in helpers: starts, log_lines, write, commit_all.
- tests/scripts/test_supervise_change.py (26, room 274): the one test that executes write_proposals.

Line counts from `wc -l`; `tools size --limit 300` printed no file over 300 lines (run). The files within 20 lines of the limit: scripts/workqueue.py (room 6) and scripts/supervise.py (room 16).

## Open reading (not decided here)

An apply round that applies nothing: r140/r147 read it as an output recognised in the round's result; r131 reads a result with neither questions nor a change list as missing output. Both readings are in the spec as written; the result form of "applies nothing" is defined nowhere in the spec (read: spec/capabilities/supervision.md; spec-integration.md has no such form).
