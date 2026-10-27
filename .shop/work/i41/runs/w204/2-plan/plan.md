# Plan of w204 (supervision r140-r148)

From the research notes at `.shop/work/i41/runs/w204/1-research/notes.md` (sections cited as §n).

## 1. What goes green

Every one of the nine is red today at its first step with `StepDefinitionNotFoundError` (§1). Behind the steps, the code is missing too:

- **supervision#r140**: "an apply round that applies nothing because the proposal's answers give what its drafts do not hold is followed by a new integrate round for the proposal". The "i1 is started and fulfils ..." Given, the "applies nothing" Given and the "integrate was started for p1 after the apply round had ended" Then are not defined. There is no route from an apply round to an integrate round for a proposal: `AFTER`/`Rounds.route` send an answered proposal to apply and then approved (§1, probe §2).
- **supervision#r141**: "an integrate round started for a capability-proposal that has answers is given its questions and answers, the initiative's ledger and the accepted lines of the request". The ledger Given and the brief Thens are not defined. `Briefs.integrate_lines` reads `fulfils` from the node's own file, so a proposal's brief has an empty Request, and no brief names the ledger (§1).
- **supervision#r142**: "a capability-proposal an integrate round drafts anew from its answers is set drafted, the earlier drafts kept where their round wrote them". Its Givens and Thens are not defined. `Changes.write_proposals` writes `thing.md` next to `p1.md` instead of setting p1 drafted (§1, §2).
- **supervision#r143**: "a capability-proposal keeps its status while the integrate round started for it runs". Only the step texts are missing. The integrate branch has to take the proposal's own status as `before`, not `after` (§1, §3).
- **supervision#r144**: "... ends having applied its drafts, the proposal is approved". Only the "applies p1's drafts and gives DONE with a change list ..." Given is missing. The behaviour exists today (§1).
- **supervision#r145**: "... the proposal's adds, changes and removes are written from the change list the round applied". The same Given is missing. `rewrite_lists` already does this (§1).
- **supervision#r146**: "... a formulate round is started for the proposal". The same Given is missing. The route already does this (§1, §2).
- **supervision#r147**: "an apply round that applies nothing because the proposal's answers give what its drafts do not hold has given its output". Its Givens and its Then are not defined. Today `run_round` asks the r131 question "gave no change list" for any apply round that gives neither questions nor a change list (§1).
- **supervision#r148**: "a capability-proposal an integrate round drafts anew from its answers is the only capability-proposal of the initiative for its capability". Its Givens and its Then are not defined. `write_proposals` writes a second proposal for `thing` (probe §2).

Retired by the work-item (deprecated scenarios in `features/supervision.feature`, all tagged `@deprecated`, none collected): @r80 "... the proposal is approved (deprecated)", @r114 "... adds, changes and removes are written from the change list the round applied (deprecated)", @r71 "... a formulate round is started for the proposal (deprecated)". The work-item's Retires section lists them under r144, r145 and r146.

## 2. Where the change lands

Production:
- `scripts/supervise_rounds.py`:
  - the route of an awaiting-answer proposal whose last round was an apply round that applied nothing goes to integrate, with `drafted` after (r140);
  - the apply branch takes that result as output: no r131 question, its stage directory committed with no transition (r147);
  - the integrate branch, run for a proposal, takes the proposal's status as `before`, does not start the initiative, and moves the proposal to `drafted` once only, at its end (r142, r143).
- `scripts/supervise_change.py`: `write_proposals` rewrites in place an existing proposal of the initiative whose `argues` is the named capability: its lists, its drafts sentence, and status `drafted` through the move. It writes no second file for that capability (r142, r148).
- `scripts/supervise_brief.py`: the integrate brief for a proposal takes `fulfils` and the accepted lines from `initiative.md`. It names the initiative's `ledger.md` and puts it in Read, gives the proposal's questions and answers (`answer_lines`), and gives the earlier drafts path to read under a label apart from "Drafts path:" (r141, r142).
- `agents/initiative-round.md` (added: the researcher's set lacks it). The apply bullet says how a round that applies nothing, because the answers give what the drafts do not hold, says so in its result. The integrate bullet says that a round given a proposal's questions, answers and ledger drafts that proposal anew. Without these lines no real round can give the result that decision D1 reads.

Tests:
- `tests/scenarios/supervision_given.py`: the "i1 is started and fulfils the request q1, whose ..." Given.
- `tests/scenarios/supervision_formulate_steps.py`: the "the apply round for p1 applies p1's drafts and gives DONE with a change list ..." Given (r144-r146), and the "applies nothing, giving that ... [and no change list]" Given.
- `tests/scenarios/supervision_proposal_steps.py`: "i1's capability-proposal p1, for thing, is awaiting-answer, ...", "... written from the change list of i1's integrate round, whose drafts are kept at ...", and "p1's ## Questions section holds ..., and its Answers section ...".
- `tests/scenarios/supervision_integrate_steps.py`: "the integrate round for p1 [writes ... under its drafts path and] gives DONE with a change list ...", and "i1 has one capability-proposal for thing, and it is p1".
- `tests/scenarios/supervision_reintegrate_steps.py` (new). `supervision_rounds_steps.py` has 28 lines of room (§7), so a new module holds: the ledger Given; the r140, r141 and r143 Thens (integrate started after apply, given the question with its answer, given the ledger, given lines 1 and 3 and not 2, awaiting-answer while it ran, no transition between start and end); r142's "transition to drafted made once the integrate round for p1 had ended" and "... thing.md is as the first integrate round wrote it". CLAUDE.md's map already covers `tests/scenarios/` as one `<capability>_*_steps.py` module a concern, so no row is added.
- `tests/scenarios/supervision_rounds_steps.py`: widened only if its "a round of the kind (apply|formulate) was started for p1 after ..." Then is the one extended to integrate. Otherwise that Then goes in the new module.
- `tests/scenarios/supervision_outputs_steps.py`: "no question naming the apply round's output as missing was written under p1's ## Questions" (r147).
- `tests/scenarios/test_supervision.py`: loads the new step module, if step modules are loaded there.
- `tests/scenarios/supervision_world.py`: only if the stand-in needs a helper to give an apply result with the applies-nothing field.

Taken out of the researcher's set, because no decision below changes them: `scripts/supervise_worker.py` (Read lines in the brief are enough, and no grant changes), `scripts/supervise.py`, `scripts/supervise_faults.py`, `scripts/supervise_outputs.py`, `scripts/supervise_drafts.py`, `scripts/workqueue.py` (6 lines of room, so this plan leaves it alone), `scripts/workqueue_request.py`, `scripts/workqueue_note.py` and `tests/scripts/test_supervise_change.py`. That test stays sound (§4).

## 3. Decisions

- **D1. How an apply round says it applied nothing.** The apply result gives this in a field of its own, beside `changes`. It names that the proposal's answers give what its drafts do not hold. It is not the `status` word, because r133 says no transition comes from the outcome. It is not inferred from an empty result. An apply round with neither questions, nor a change list, nor this field still gets the r131 question. This takes the only reading that holds r131, r132 and r147 together; reading (b) in §4 would contradict r131. Rests on supervision#r131, #r133, #r147 and design-decision/worker-results-are-files (a stage's own fields). The implementer names the field and writes it into the stand-in's Given and the apply bullet of `agents/initiative-round.md`.
- **D2. What such an apply does to the proposal.** It writes no question and makes no transition: p1 stays awaiting-answer. Its stage directory, and its log lines if any, are committed with no transition, the same way the asked-on-awaiting-answer path commits. Then the next due round runs before `work run` ends. This closes §5's skipped commit. Rests on supervision#r147, #r140, #r111 and capability r46 (nothing left uncommitted under .shop/work/).
- **D3. How the route finds it.** For an awaiting-answer proposal, the route reads the proposal's latest stage directory under `runs/<p>/`. If that directory is an apply round whose result gives the D1 field, the route is integrate, with `drafted` after. Otherwise the route is unchanged (formulate after a move from approved, otherwise apply). The route reads the committed result file, not a new log field, so `workqueue.py` is not touched. Rests on supervision#r140 and design-decision/worker-results-are-files.
- **D4. Where the new integrate round runs.** Its stage directory is keyed by the proposal, `runs/p1/<k>-integrate`, as every round of p1's is (`run_dir`). Its drafts are kept there (r91). The earlier `runs/i1/<k>-integrate/drafts/round-<n>/` is not written. In p1's file, the sentence "The drafts of this proposal are in ..." is rewritten to the new kept path, so that the next gate and apply rounds read the drafts of the round that wrote the proposal. Rests on supervision#r142, #r91, #r108.
- **D5. Status during and after the integrate round.** `before` is p1's own status, taken as the other rounds take it. Nothing moves when the round starts. The move to `drafted` is made at its end, in one commit with the rewritten p1. A fault keeps the status (r86), and so does a change list that is missing or unreadable (r96, which also exits with an error naming the round). Rests on supervision#r142, #r143, #r86, #r96.
- **D6. Redraft in place.** When the change list names the capability that an existing proposal of the initiative `argues`, that proposal is the one rewritten: its id, its file and its `## Questions`/`## Answers` sections are kept, and its lists are replaced by the entries for that capability. A capability the list names that has no proposal in the initiative gets a new one, as today (r92). Rests on supervision#r148, #r142, #r92.
- **D7. The proposal's integrate brief.** It gets the request from `initiative.md`'s `fulfils` and only the lines with outcome accepted (`accepted_lines`). It names `.shop/work/<initiative>/ledger.md` and lists it under Read. It gets the proposal's questions with their answers, the requirement ids of other initiatives' drafts (r102), the new Drafts path, and the earlier drafts path to read only. Rests on supervision#r141, #r102, #r142.

## 4. Tests the decisions break

None. What was verified:
- `tests/scripts/test_supervise_change.py::test_two_entries_naming_one_capability_give_one_proposal_with_both_entries_ids`: there is no existing proposal for the capability there, so D6 leaves its path as it is. It is kept.
- The r131 apply case: under D1 a result with nothing at all is still asked. The row at `features/supervision.feature:873` ("apply round | p1 | ... leaves no result") is a no-result fault row, and no decision here changes it.
- The deprecated @r80, @r114 and @r71 scenarios are retired by the work-item and not collected.
- The `supervision_rounds_steps.py` stand-ins `apply_did_its_work` and `every_round_ends` give a change list, so D1-D3 leave them on the applied path.

## 5. Open cases

- What the stand-in's integrate round for p1 gives under "every other round ends" in r140, r141, r143 and r147. If it gives no change list, r96 exits with an error and the scenario's Then must still hold. The implementer names what the stand-in gives.
- After the redraft, the new gate round adds its questions under the kept `## Questions`, and the earlier answers still count toward the `due` check. Whether any count of earlier answers lets apply start before the person answers the new gate is a case no scenario covers.
- A redraft whose change list names another capability that already has a proposal in the initiative: r148 speaks only of p1's own capability.
- An apply round that gives the D1 field together with a change list or with questions.
- A second apply round that applies nothing after a redraft, which loops back to integrate.
