# Notes: research of w200 (fix the findings of branch review 1 of i38)

Checkout HEAD 177ec65c (w199 green, w200 drafted). Analysis tools: plugin 0.26.0 `tools`. `tests-of` has no map (`tools map` runs the suite, not run): tests are found `by search`. `refs` used for module functions; method calls (`self.outcome`) are not counted by `refs`.

## 1. Why each scenario is red today

None is red. Run: `python3 -m pytest -q -rfE --tb=line -p no:warnings tests/scenarios/test_supervision.py`: 63 passed in 5.11s. The file collects 63 of 253 (190 deselected in collection; cause not read). The 63 are the accepted tags' scenarios (`--collect-only` lists them), run in one invocation, not one node id each.

Gaps the branch review names, which no accepted scenario covers yet:
- a formulate round with no question and no scenario: no row (features/supervision.feature:919-923, r131, has no formulate row).
- the r132 formulate row (features:943) passes without the scenario its Given names (see 4 and 6).

## 2. What the system answers today

Probes: `.shop/scratch/w200-1-research/probe_formulate.py` (2 tests), `probe_implementer.py` (1 test). Run: `python3 -m pytest -q -s -p no:xdist -o addopts="" -p no:warnings .shop/scratch/w200-1-research/probe_formulate.py` (and `probe_implementer.py`). Each builds the scenario Background (`supervision_given.repository`) and, for formulate, an approved p1 adding thing#r4. The Background's w1 runs through its stages too (its stand-in gives DONE). The approved p1 is the probe's own, and the run formulates it.

- P1 (run): formulate round gives DONE, no question, no scenario for thing#r4 (no features/ dir). Exit 0. p1 `approved -> formulated`. Nothing asked, no scenario. The r132/r131 nearest case.
- P2 (run): formulate round gives DONE with the question "Are returns counted?". Exit 0. p1 `approved -> awaiting-answer`, commit "work: p1 approved -> awaiting-answer".
- P3 (run): implementer gives DONE, no question, commits nothing, its tests pass. Exit 0. w1 `ready -> claimed -> done -> green`. The merge's suite record: "Suite: 1 passed, 0 failed". No commit touches feature.txt. initiative.md stays `status: started`. stderr: "work run: the analysis session of i1 wrote no analysis record".

Nearest cases read, not probed:
- r4 merge (5 rows run): merge() supervise_merge.py:116-135 runs the tests on the rebased branch and merges; a branch with no commit passes (P3).
- r31 fileset: stage() supervise.py:171-174 writes fileset only when question is None and agent is bdd-planner.
- r36 section(): supervise.py:122-135 puts a bullet before the next `## ` heading; a missing `## Questions` is appended at the end.
- r45 cut short: cut_short() supervise_faults.py:139-153 and worker() supervise_worker.py:197-200: a cut-short session's result is not read.
- r86-r88, r115 rounds: rounds() supervise_rounds.py:63-76 and round() :78-84: a round's fault holds its node, the others go on.
- r128 faults: note() supervise_faults.py:96-102; show() supervise.py:238-257.
- r89/r90 answering: ask() supervise_answers.py:99-127: a session fault is noted and the answer is None; a `DONE` with no answer is None.
- r134 intake: take() supervise_intake.py:75-107: a question is written with workqueue_request.ask before the merge; the status is left as work turn set it.
- r37/r63 and r32: questions() supervise.py:189-192 counts the `## Questions` bullets past the `## Answers` ones; not read further.

## 3. Old assumptions

The requirements replace "the status word decides the transition" (design-decision 0039, r3, r5, r16, r112, r113) with "what the result gives decides it" (r128-r133). The table lists where the old form still stands.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/supervise.py:32-38 STAGES (comment, `after`) | maps a status to stage, agent and the status the success moves to; comment says "the status its DONE moves the work-item to" | the transition is the output, not DONE (r130, r133): comment stale; `after` used only when there is no question | many (stage() on every worker path); by search | refs (STAGES), read |
| scripts/supervise.py:8 docstring | "what is not DONE goes to the person as a question" | r133, r131: not the status | none (docstring) | read |
| scripts/supervise_rounds.py:139 | apply round's refusal text "gave DONE, and ..." for any status | r133: the status word is no fact; wording only | none (no test asserts the text; by search) | read, grep "gave DONE" |
| scripts/supervise_rounds.py:173 refuse_integrate | text "gave DONE" for any status | as above; r96 names the round | none (by search) | read, grep |
| scripts/supervise_rounds.py:5, :115, :170 | "DONE with no change list", "ended DONE" | r96 is "no change list", not status | none (comments) | read |
| scripts/supervise_rounds.py:147-158 formulate branch | no question: moves to `formulated`; no output check | r132: formulate output is a scenario per requirement; r131 question if missing (P1) | r83 scenario (features:1378-1385 via supervision_formulate_steps.py:11-13); r132 formulate row (features:943 via supervision_session_faults_steps.py:80); by search | read, P1 |
| scripts/supervise_outputs.py:12-25 missing() | roles researcher, planner, reviewer only; implementer returns None | r132 adds formulate (and the implementer's commits, see 5) | r131 rows, by search | read, refs (missing) |
| scripts/supervise_intake.py:76 docstring; take() :75-107 | "does not end DONE"; no output check | r131/r134: intake output is a line outcome or a question per line | intake scenarios, by search (supervision_intake_steps.py) | read |
| scripts/supervise_answers.py:101 docstring; :141-142 prompt | "a DONE with no answer"; the brief tells the session to give `DONE` | r120/r89: the answer field and the verdict decide; status not read | r89/r90 and r77/r78 rows, by search | read |
| agents/bdd-implementer.md:55, :59 | "`work run` merges only `DONE`"; "for anything but DONE, what the person is asked" | false today: merge() decides on tests and commits (P3); r4/r132 | none (agent text is not run by tests) | read |
| agents/bdd-task-reviewer.md:60 | DONE_WITH_CONCERNS sends the work-item to the person | r130/r131: the findings decide (outputs.missing) | none | read |
| agents/initiative-round.md:28 and :62 | "A DONE with no change list is an error"; "BLOCKED" for apply with no approval | r96 by change list; r133: BLOCKED decides nothing | none | read |
| agents/code-scout.md:83, agents/bdd-planner.md:49 | "questions: a list, empty when DONE" | r129 reads questions only | none | read |
| spec/decisions/0039-work-item-lifecycle-as-run.md:19-21, :25, :29, :41 | guards on DONE ("drafted -> researched: DONE, ...") | r133 forbids it; no decision supersedes it | none (a decision) | read; review finding 2 |
| features/supervision.feature:64 (deprecated) | "a worker's outcome DONE makes the work-item's transition..." | r133 contradicts its title | its own scenario, by search; not run | read |
| tests/scripts/stub_claude.py:14, :261 | the stand-in's default status is "DONE" | none: a stand-in default | all supervision scenarios, by search | read |

`tools refs outcome` gives 0 (method calls are not counted); by search, its callers are supervise.py:171 and supervise_merge.py:101.

## 4. Tests the requirements make impossible to keep

`tests-of` has no map; these are `by search` (features, step files and tests read by text).

- features/supervision.feature:1378-1385, the r83 scenario "when the formulate round `work run` started for a capability-proposal ends without giving a question, the proposal is formulated" (`@r83`, not deprecated). Given: "the formulate round for p1 gives DONE with no question" (supervision_formulate_steps.py:11-13), no scenario for thing#r4. Then "p1's transition to formulated". Passes today (P1 shows its path). It cannot keep passing as written if the formulate check lands. Two readings, not decided:
  - Reading A: r83 stands; the formulate output rule (r132) does not apply when a formulate round gives no question. The scenario keeps passing; branch review finding 1 is not fixed.
  - Reading B: r132 applies; the scenario's Given must add a scenario for thing#r4 (a new step or a changed Given), and r131's formulate row takes the no-scenario case.
- features/supervision.feature:943, the r132 formulate row: stage_gives (supervision_session_faults_steps.py:80) skips the formulate round, so the row's Given commits no scenario. It passes today for the wrong reason (branch review finding 1; read, and its accepted run passes). With the check, its Then fails unless the stand-in commits the scenario (tests/scripts/stub_claude.py:68-70 DELIVERS has no initiative-round entry).
- supervision_rounds_steps.py:259-261 formulated_after_formulate: its Then is the same as the r132 formulate row's; it stands or falls with reading A/B.
- features:1388-1403 (deprecated formulate-questions scenarios): unaffected; the questions path is kept.

Looked at and sound: the apply and integrate rows (features:941-942, the r87/r88 rows at :1427-1442), the planner and implementer rows of r131 and r132, and the r129 formulate row (features:892); none depends on the formulate branch's no-question move (searched by text for "formulat" in features/supervision.feature and tests/scenarios). The 63 accepted scenarios pass today (section 1).

## 5. A step the work-item skips

- Formulate round, supervise_rounds.py:147-158: the existing way gives an apply round the output check (:144-146, the r131 question) and every worker the outcome() check (supervise_worker.py:247-256: outputs.missing, outputs.question). Effects only that step produces: a question under the node's `## Questions` naming the missing output, and awaiting-answer. The formulate path produces neither. Shown by P1 (run).
- Intake round, supervise_intake.py:88-107: no outcome() step. A result with neither a line outcome nor a question is "ended" (keep(..., "ended") at :107), no question, the request stays open, and the next run starts the round again. Effect the step would give: a question naming the missing line outcome. Read.
- Implementer, supervise_merge.py:116-135: merge() checks the tests on the branch only; the commit output of r132 is not checked when there is no commit (outputs.missing returns None for the implementer, supervise_outputs.py:12-25). Effect missing: a question that says commits are missing; the only question merge() gives is for failing tests. Shown by P3 (run).
- Analysis session, supervise_analysis.py analyse(): no output check; no record means a stderr line only ("is no fault"). set_done() (supervise_done.py:31) returns silently when the records are not committed. Shown by P3 (run): exit 0, initiative stays `started`.
- Answering session, supervise_answers.py:120-127: no output check beyond an answer that is one non-blank line (no r131 question). Effect missing: a question naming the missing answer. Read.

## 6. Defects

D1. A formulate round that gives DONE with no question and no scenario moves the proposal to formulated. Reproduction: `python3 -m pytest -q -s -p no:xdist -o addopts="" -p no:warnings .shop/scratch/w200-1-research/probe_formulate.py -k no_question_no_scenario`: exit 0; p1 `approved -> formulated`; no scenario for thing#r4; no question. Expected per r131/r132: a question naming the missing scenario and awaiting-answer. Run.

D2. An implementer that commits nothing, with its tests passing, is merged, done and green. Reproduction: `python3 -m pytest -q -s -p no:xdist -o addopts="" -p no:warnings .shop/scratch/w200-1-research/probe_implementer.py`: exit 0; w1 `claimed -> done -> green`; no commit touches feature.txt; no question. Expected per r132 ("commits ... on which the scenarios and the suite pass"). Run.

D3. An analysis session that writes no record: exit 0, the initiative stays `started`, the reason only on stderr. Reproduction: the same probe_implementer.py run: stderr "work run: the analysis session of i1 wrote no analysis record", initiative.md `status: started`, exit 0. Whether exit 0 is a defect depends on r76's reading. Run.

D4. An intake round giving neither a line outcome nor a question is recorded "ended", and the request stays open with no question. Reproduction: read supervise_intake.py:88-107 (no output check; keep(..., "ended") at :107). Not run.

D5. Wording: the apply and integrate refusals say "gave DONE" for any status (supervise_rounds.py:139, :173). Reproduction: `grep -n "gave DONE" scripts/supervise_rounds.py` gives 139 and 173 (also read in the file). Read.

From the branch review (findings.md; not re-run): deprecated-for-removal scenarios r3, r5, r16, r112, r113 with no retirer (finding 7); q8's resolution cites the removed r113 (`model check` v3, finding 8); ruff errors in committed round scripts under .shop/work/i38/runs (finding 6); by-hand commits to w199's accepts and Retires (finding 5).

## 7. The file set

Production files w200 must change (for its scenarios and the findings' fixes):
- scripts/supervise_rounds.py (192 lines; room 108): the formulate output check at 147-158; "gave DONE" at 139, 173; docstrings 5, 115, 170. Found: read, P1.
- scripts/supervise_outputs.py (30 lines; room 270): a formulate role (a scenario per id in adds and changes) and its question. Found: read, refs (missing).
- scripts/supervise.py (284 lines; room 16): the comment at 32 and the docstring at 8, if the text is fixed. Room 16: any new code here nearly breaks the limit.
- scripts/supervise_merge.py (135 lines; room 165): only if D2 is fixed (a commit check before the merge, at 116-135). Found: read, P3.
- scripts/supervise_intake.py (118 lines; room 182): docstring at 76; an output check if D4 is fixed. Found: read.
- scripts/supervise_analysis.py (80 lines; room 220): only if D3 is fixed. Found: read, P3.
- scripts/supervise_answers.py (146 lines; room 154): docstring 101 and the prompt at 141-142, if the answer text changes. Found: read.
- tests/scenarios/supervision_session_faults_steps.py (106 lines; room 194): stage_gives at line 80 (the formulate skip). Found: read.
- tests/scenarios/supervision_formulate_steps.py (83 lines; room 217): the r83 Given at 11-13 under reading B, and any new step for the r131 formulate row. Found: read.
- tests/scenarios/supervision_rounds_steps.py (262 lines; room 38): formulated_after_formulate at 259-261, if its Then changes. Found: read.
- tests/scripts/stub_claude.py (281 lines; room 19): DELIVERS at 68-70, for a formulate round's scenario commit. Found: read.
- tests/scenarios/test_supervision.py (265 lines; room 35): binds the feature; changes only if a new step function lives here. Found: read.
- features/supervision.feature (not Python; no size limit): an r131 formulate row after :923; the r83 scenario at :1378-1385 under reading B; the r132 formulate row's Given at :943. Found: read.
- spec/decisions/0039-work-item-lifecycle-as-run.md (a decision, not code): the DONE guards at lines 19-21, 25, 29, 41 (review finding 2). Found: grep, read.
- agents/bdd-implementer.md (:55, :59), agents/bdd-task-reviewer.md (:60), agents/initiative-round.md (:28, :62): text that says what `work run` does. Found: read.

Modules on the change path, edited or not (line count by `wc -l`; room = 300 - lines, the limit CLAUDE.md gives; `tools size --limit 300` printed nothing):
- scripts/supervise.py 284 (room 16); scripts/supervise_worker.py 256 (room 44); scripts/supervise_rounds.py 192 (room 108); scripts/supervise_outputs.py 30 (room 270); scripts/supervise_merge.py 135 (room 165); scripts/supervise_intake.py 118 (room 182); scripts/supervise_answers.py 146 (room 154); scripts/supervise_analysis.py 80 (room 220); scripts/supervise_done.py 36 (room 264); scripts/supervise_faults.py 190 (room 110); scripts/supervise_draft.py 122 (room 178).
- scripts/workqueue.py 294 (room 6): on the path (move, agrees, logged), not edited; any new code here breaks the limit.
- tests/scenarios/test_supervision.py 265 (room 35); tests/scenarios/supervision_session_faults_steps.py 106 (room 194); tests/scenarios/supervision_formulate_steps.py 83 (room 217); tests/scenarios/supervision_rounds_steps.py 262 (room 38); tests/scripts/stub_claude.py 281 (room 19).
