# w199 implement report

## Budget

Part 1 (the work-item workers' stages: r4, r31, r45, r61, r129 to r133 for researcher, planner, implementer, reviewer):

1. scripts/supervise_outputs.py (new)
2. scripts/supervise_worker.py
3. scripts/supervise.py
4. scripts/supervise_brief.py
5. scripts/supervise_merge.py
6. CLAUDE.md
7. tests/scripts/stub_claude.py
8. tests/scenarios/supervision_outputs_steps.py (new)
9. tests/scenarios/test_supervision.py
10. tests/scenarios/supervision_then_workers.py
11. tests/scenarios/supervision_given.py
12. features/supervision.feature (features retire only)

Left for later parts: rounds (r86-r88, r115, r128 rows of rounds, r129 gate/formulate), answering sessions (r89, r90, r128), intake (r134), r132 round rows, `show()` of faults.

Suite at the start (brief's Suite record): 915 passed, 52 failed at 195b7ab2 (all failing are this work-item's scenarios, undefined steps).

## Part 1 — what changed

- scripts/supervise_outputs.py (new): the stage-output check (researcher's file set; planner's plan and file set; reviewer's findings) and r131's question naming what is missing. Module-map row added to CLAUDE.md.
- scripts/supervise_worker.py `outcome()`: no longer reads the status word. A result's questions, else the missing-output question, else None (r129, r131, r133). A researcher's DONE questions still go to the planner (see Open questions).
- scripts/supervise_merge.py: the question when the work-item's scenarios or the suite fail names "commits on which wN's scenarios and the whole suite pass" as missing (r131).
- tests/scripts/stub_claude.py: `DELIVERS`, a default output per stage (decision 3); `fields` with a null value withholds it.
- tests/scenarios/supervision_outputs_steps.py (new, imported in test_supervision.py): Givens "the <who>'s result gives ...", r61's, r4's r43 case, r45's researcher endings, and Thens for transition-after-end, questions, missing, planner's brief.
- Retired by `features retire` (replacements green): the 4 deprecated r4 scenarios, r61, r31 and r45. Unused steps removed: researcher_cut_short and ENDINGS (supervision_faults_steps.py), "implementer writing feature.txt and not committing it" (supervision_given.py).
- Commit: 947bdc50.

The plan contained no code (it names functions only); nothing was pasted.

## Red and green

Red: the brief's suite record, 52 failing, each an undefined Given or Then (the research notes part 1 shows the same, one run per scenario). I wrote the production edits and the steps together, then ran the module; I did not run each scenario red on its own first.
Green, `python3 -m pytest -q --work-item w199`: 24 failed, 185 passed (was 52 failed). Module with every scenario (`tests/scenarios/test_supervision.py --whole-suite`): 24 failed, 240 passed; the 24 are all accepted scenarios of this work-item not yet done, none previously green. I also ran tests/scripts and the other scenario modules once with `-x`: all passed.

Scenarios now green: r4 (5 rows), r31, r45 (4), r61, r130 (4), r131 (4), r132 researcher, planner, implementer, reviewer rows, r133, r129 researcher, planner, implementer, reviewer rows, r128 none yet.

## Still red (24), left for the next part

- r128 (5 rows): record a fault under `## Faults` of any node (round, answering session) and print it in `show()`; the Thens "`work run` recorded a fault of <node>" and "prints <node> with the fault" do not exist.
- r129 formulate row; r132 rows for gate, apply, formulate, integrate, intake, answering session.
- r87, r88 (3 rows each, plus r88's wording "ended in an error", "left no result `work run` can read"), r89 (3), r90 (3), r134 (Then undefined).
- Files for that part (all in the work-item's file set): scripts/supervise_rounds.py, supervise_faults.py, supervise_answers.py, supervise_intake.py, supervise.py (show); tests: supervision_session_faults_steps.py (new), supervision_rounds_steps.py, supervision_formulate_steps.py, supervision_then_workers.py, supervision_faults_steps.py, supervision_intake_steps.py; retire r87, r88, r89, r90, r115 deprecated scenarios once their replacements are green.

## Tests changed under an allowance

- tests/scenarios/supervision_given.py `researcher_asks` (the Given "the researcher gives <status>[, asking ...]"), setup: with no question given it now withholds the file set, so the deprecated r5 outline's NEEDS_CONTEXT row (a researcher giving only a status) still ends awaiting-answer; no assert changed. Plan part 4 said to remove that outline, but `features retire` is allowed only for the work-item's Retires list, which does not name it; so it is kept green.
- no other.

## Open questions

- **Conflict that stops r129's researcher row as the plan has it (decision 4).** The plan sends a researcher's questions to the planner and the work-item to researched. Three non-deprecated scenarios that are not this work-item's pin the opposite: r32 "when no work-item can make a transition and one is awaiting-answer, ..." (Given "the researcher gives QUESTION, asking ..."), r37 "no worker is started for a work-item after its transition to awaiting-answer", and the scenario of r36 "a question goes into the work-item's ## Questions before a section that follows it", plus the deprecated r5 outline's QUESTION and BLOCKED-asking rows. With decision 4 applied they went red (run: 6 failed). I kept the old behaviour (a researcher's questions with a status other than DONE: awaiting-answer; with DONE: the planner's brief), so the researcher row of r129 passes only for DONE. The person must rule: rewrite those scenarios to a planner's question, or keep a researcher's non-DONE question asking.
- The plan's part 5 cases: a plan or findings naming a missing file; an implementer that commits nothing (the check is the tests only, not that a commit exists); an empty change list; an answer session giving a question where one is open.
- A result with the status BLOCKED or HAND-BACK and no question and its stage's output now moves on (r133): an implementer so handing back with passing commits is merged. Left as the scenarios say.

## Files changed

scripts/supervise_outputs.py, scripts/supervise_worker.py, scripts/supervise_merge.py, CLAUDE.md, tests/scripts/stub_claude.py, tests/scenarios/supervision_outputs_steps.py, test_supervision.py, supervision_given.py, supervision_faults_steps.py, features/supervision.feature (retire only). 10 files.

## Size

`tools size --limit 300` printed nothing: no file over.
