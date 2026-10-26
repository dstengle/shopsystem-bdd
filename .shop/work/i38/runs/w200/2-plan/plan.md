# Plan of w200: fix the findings of branch review 1 of i38

Work-item `.shop/work/i38/w200.md`, under supervision. It is drafted from the fix-now findings of branch review 1 (`.shop/work/i38/runs/branch-review/1/findings.md`), and only finding 1 is triaged fix now. Findings 2 and 4 to 8 are observations: this plan does not take them (see part 5). It takes finding 3, a wording fix, because the change is in the same function and r133 settles it.

## 1. What goes green

None of the accepted scenarios is red today: the notes' part 1 ran 63 passed. Every requirement w200 accepts (r4, r31, r32, r36, r37, r45, r61, r86-r90, r115, r128-r134) keeps its scenarios green. The work is the formulate half of r131 and r132, which no scenario pins honestly today:

- **supervision#r132**, outline "a <stage>'s result giving <output> is taken as its stage's output", row `formulate round` (features/supervision.feature:943). It is green today for the wrong reason. Its Given says the round gives "a scenario for thing#r4", but `stage_gives` (supervision_session_faults_steps.py:80) sets up nothing for a formulate round, and the stand-in commits no scenario (notes 4; finding 1). After this work it passes because the scenario exists.
- **supervision#r131**, outline "a <who> whose result gives neither a question nor <missing> ...". Its rows cover the researcher, planner, implementer and reviewer, and none covers a formulate round. Defect D1 (notes 6, probe P1) shows the formulate case is wrong today: a formulate round with no question and no scenario moves p1 from `approved` to `formulated`, and no question is asked.
- **supervision#r83**, scenario "when the formulate round `work run` started for a capability-proposal ends without giving a question, the proposal is formulated" (features:1378-1385). It is not in w200's accepts, but the formulate check breaks it (part 4). It must stay green.

No deprecated scenario is retired: the work-item has no Retires section.

## 2. Where the change lands

- `scripts/supervise_outputs.py`: a new formulate output in `missing`. For each id in the proposal's `adds` and `changes`, it looks for a non-deprecated scenario tagged `@r<n>` in that capability's feature file on the merged initiative branch, and names every requirement left without one. `question` gets the wording for that case.
- `scripts/supervise_rounds.py`: `run_round`'s formulate branch (147-158). When the round gives no question, it asks `supervise_outputs` for the formulate output first. If something is missing, it writes r131's question under the proposal's `## Questions` and moves the proposal to `awaiting-answer`, the way the apply branch does at 144-146. Only when nothing is missing does it move to `formulated`. The same file also loses "gave DONE, and" at 139 and 173, and "DONE" in the docstrings at 5, 115 and 170 (finding 3).
- `tests/scenarios/supervision_session_faults_steps.py`: `stage_gives` (line 80). For the `formulate round` stage, its stand-in now commits a scenario tagged for each requirement the row names ("a scenario for thing#r4").
- `tests/scenarios/supervision_formulate_steps.py`: `formulate_no_question` (lines 11-13), the r83 Given. Its stand-in commits a scenario for each requirement p1 adds (part 4).
- `tests/scripts/stub_claude.py`: only if the scenario commit is done through the stand-in's `DELIVERS` (lines 68-70), with an entry for an `initiative-round` of kind formulate. The file has 19 lines of room. If the commit fits in the step modules through the plan's fields, this file is not touched.
- `features/supervision.feature`: no edit by the implementer. The r131 formulate row comes from a feature-formulator hand-back (decision 4).

**Removed from the researcher's set:**
- `scripts/supervise.py`, `scripts/supervise_intake.py`, `scripts/supervise_answers.py`, `scripts/supervise_merge.py`, `scripts/supervise_analysis.py`, `agents/bdd-implementer.md`, `agents/bdd-task-reviewer.md`, `agents/initiative-round.md` and `spec/decisions/0039-work-item-lifecycle-as-run.md`. They carry findings 2 and 4 and defects D2-D4, which are observations that w200 does not take (part 5). Leaving `supervise.py` alone also keeps its 16 lines of room.
- `tests/scenarios/supervision_rounds_steps.py`: the Then `formulated_after_formulate` stays as it is, because it holds once its Givens are honest.
- `tests/scenarios/test_supervision.py`: no new step lives there.

## 3. Decisions

1. **What a formulate round's output is.** It is a non-deprecated scenario tagged `@r<n>` in the capability's feature file, on the initiative branch after the round's merge, for each requirement id in the proposal's `adds` and `changes`. Rests on supervision#r132 ("a formulate round's scenario for each requirement its proposal adds or changes"), and on finding 1's fix, which the work-item is drafted from.
2. **A formulate round with no question and a missing scenario** gets the r131 question under the proposal's `## Questions`, naming the requirements that have no scenario, and the proposal moves to `awaiting-answer`, not `formulated`. Rests on supervision#r131 and r130. r83 is read under the gate answer recorded in the proposal (`.shop/work/i38/supervision.md:35`): "r83 stays as written, r130 and r131 deciding whether the next transition happens". This answer is the ruling that settles the notes' reading A against reading B in favour of B, so it is not a question.
3. **The check lives in `supervise_outputs`, not in `run_round`.** r131's question is built only in `supervise_outputs.question`. Rests on supervision#r131 and r132 (one output reading for every stage), and on the branch review's Shape observation.
4. **The r131 formulate row is not written by the implementer.** An accepted scenario is the formulator's. Finding 1's fix names "an r131 formulate row through a formulate hand-back". The implementer's red for the check is that row. If the row is not in `features/supervision.feature` when the implementer starts, the implementer asks for it through its question, the same path w199 used for its r32, r36 and r37 hand-back. It does not write the row and does not code the check without a red. Rests on supervision#r131 and finding 1.
5. **The refusal wording** drops "gave DONE, and" and says only that the round gave no change list. The status word is no reason for anything. Rests on supervision#r133 and r96.

## 4. Tests the decisions break

- **features/supervision.feature:1378-1385, the r83 scenario**, through `formulate_no_question` (supervision_formulate_steps.py:11-13). Decision 2 breaks it, because p1 adds thing#r4 and the stand-in commits no scenario (notes 4). It is rewritten as setup only: the Given's stand-in also commits a non-deprecated scenario tagged for each requirement p1 adds. The Then stays: p1 moves to formulated once the formulate round has ended. Under the ruling, r83's transition is made when the round gives its output and no question, so the Given now supplies the output its round must give. The scenario text is unchanged.
- **features/supervision.feature:943, the r132 formulate row**, through `stage_gives` (supervision_session_faults_steps.py:80). Decision 1 breaks it, because today it commits no scenario. It is rewritten as setup only: the formulate round's stand-in commits the scenario for thing#r4 that the row's text names. The Then stays (no question naming a missing output; p1 formulated). This fixes the weakness the branch review found: the text claims an output that the step never set up.
- **`formulated_after_formulate`** (supervision_rounds_steps.py:259-261): not changed. It holds through the two rewrites above.
- **Other runs through a formulate round.** The notes searched `features/supervision.feature` and `tests/scenarios` for "formulat". I re-searched `tests/`: the only stand-in formulate rounds are in `supervision_session_faults_steps.py` and `supervision_formulate_steps.py`. Those that give questions (`formulate_gives_questions`, `formulate_questions`, `apply_ends_formulate_question`) do not reach the check. Some scenarios end every round through default stand-ins, for example r95's "every round ends, each round of the kind integrate, apply or formulate ..." in `supervision_all_steps.py`. Such a scenario may now leave its proposal `awaiting-answer` where it was `formulated` before. If its Then asserts nothing about formulated, it stays as it is. If one does go red on `formulated`, its stand-in is given the scenario commit (setup), and no Then is loosened.

## 5. Open cases

- **A requirement in `changes`** that the change list removes or retires rather than rewrites. Does it still need a scenario? r132 says "adds or changes". The implementer names how a removed id is read. It does not choose a reading silently.
- **The feature file's path.** `features/<capability>.feature`, or a capability's `formulated_as:`.
- **Where the scenario is read.** On the initiative branch after the merge, or on the round's branch before it, when the merge itself fails.
- **A scenario tagged `@deprecated`** whose replacement is not yet written. r132's "scenario for each requirement" is silent on whether it counts. Decision 1 counts only non-deprecated scenarios. Name any case where that refuses a proposal the person expects formulated.
- **Not taken here (observations, left to their owners):**
  - decision 0039's DONE guards (finding 2);
  - the intake, implementer-no-commit and analysis-record output checks (finding 4; D2, D3, D4);
  - the by-hand commits (finding 5);
  - the committed round scripts failing ruff (finding 6);
  - the deprecated-for-removal scenarios with no retirer (finding 7);
  - q8's resolution naming r113 (finding 8).
