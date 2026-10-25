# Plan of w184 (supervision r110, r117, r19)

From the researcher's notes, `.shop/work/i30/runs/w184/1-research/notes.md` (cited as "notes §n").

## 1. What goes green

- **supervision#r19**: "a researcher is given the work-item's file set and accepted scenarios, and a limit of 80 turns" (features/supervision.feature:405). Red today because the researcher gets `--max-turns 40`: the research entry of `MAX_TURNS` in scripts/supervise_worker.py is 40. The file-set and accepted-scenario Thens already pass (notes §1).
- **supervision#r117**: "when the gate round `work run` started for a capability-proposal gives no question, one question asking for the approval of the proposal's lines as drafted is written under its ## Questions" (feature:1453). Red today: the Given "the gate round's result gives no question, and every round ends" has no step, and the Then "p1's ## Questions holds one question, asking for the approval of p1's lines as drafted" falls into the existing quoted-question step, which would fail on it. In the code, `run_round` takes an empty question list from a gate with none, and `move` writes nothing, so the proposal sits `awaiting-answer` with no question and the next `due()` starts apply unasked (notes §1, defect D1).
- **supervision#r110**: "when the work-item drafted for a kept branch review's findings turns green, the next branch review of the initiative is started before `work run` exits" (feature:1461). Red today: the Given with a first and a second reviewer result and both Thens have no step, and the stand-in gives one result per agent. In the code, `pull_through` in scripts/supervise.py runs one branch review per run. Once the fix is pulled, nothing reviews again (notes §1).
- **Retired**: "a researcher is given the work-item's file set and accepted scenarios, and a limit of 40 turns (deprecated)" (feature:393, @r19 @deprecated). It passes today and cannot hold after r19. It is retired with the `features retire` command, named by its title (notes §4).

## 2. Where the change lands

- `scripts/supervise_worker.py`: the researcher's turn limit goes from 40 to 80.
- `scripts/supervise_rounds.py`: when a gate round gives no question, `run_round` asks one approval question. The question goes through the same `move` as a gate's own questions, in the same commit and push.
- `scripts/supervise.py`: in `pull_through`, a fix's green is followed by another branch review, run through `branch_review` (decision 2), until a kept review lists nothing or no fix goes green. When a review lists nothing, analysis follows it as today.
- `tests/scenarios/supervision_rounds_steps.py`: the new Given for a gate result with no question. A Then for the approval question. The quoted-question Then is narrowed (decision 4).
- `tests/scenarios/supervision_proposal_steps.py`: the new Given that gives the first and the second reviewer results. The Then "one work-item was drafted in i1 for the two findings, and it is green". The existing r74 Given gives its findings only to the first reviewer session (section 4).
- `tests/scenarios/supervision_then_workers.py`: the Then "after that work-item turned green a second session of bdd-branch-reviewer was started, before `work run` exited". The file has 279 lines and 21 lines of room. If the Then does not fit, it goes into `supervision_proposal_steps.py` instead (184 lines of room), and this file stays unedited.
- `tests/scripts/stub_claude.py`: the stand-in can give one agent a different result for each session, in the order the sessions start.
- `features/supervision.feature`: the 40-turn scenario is retired with `features retire`.

Read on the path, not expected to change: `scripts/supervise_draft.py` (`fix_work_item`, one fix for each findings path), `scripts/supervise_review.py` (`branch_review`), `scripts/supervise_analysis.py` (`lists_nothing`). They stay in the file set because the loop calls them. The implementer edits them only if the loop cannot be built on them as they are.

## 3. Decisions

1. **The loop after a fix (the researcher's Q1): reading (a).** Each kept review that lists findings to fix now gets its fix work-item (r74). Each fix that turns green gets the next branch review (r110). This goes on until a kept review lists nothing to fix now (then r75 measure and r76 analysis follow), or until a fix does not turn green in this run. A one-re-review-then-exit reading (b) would leave a drafted fix, or a review owed by r110, untaken before the end, and r111 forbids that ("a transition ... leaves a node able to make another transition ... before it ends"). It rests on supervision#r110, #r74 and #r111. It is not a question for the person, because the requirements settle it.
2. **The next review goes through `branch_review`, not through `pull` alone.** `branch_review` checks the push before the review and pushes the commit after it. The fix's commits are pushed (as today, after `fix_work_item`) before its review. Rests on supervision#r110 and the push requirements `branch_review` already serves (notes §5).
3. **The approval question is written by `move` with the gate's transition.** It is written exactly as a gate's own question would be, and the proposal goes `awaiting-answer` with it (r69, r85). Its text asks for approval of the proposal's lines as drafted and names the proposal. `due()`'s rule that counts answers against questions is left as it is: after r117 a gate always leaves at least one question, so the zero-question case from D1 no longer arises. No requirement asks for a further guard. Rests on supervision#r117, #r69 and #r70.
4. **The two "p1's ## Questions holds" Thens are kept apart by their text.** The existing quoted-question step (feature:1243) matches only text that begins with a quoted question. The approval Then is a step of its own, which checks that `## Questions` holds exactly one item and that the item asks for approval of p1's lines as drafted. Rests on supervision#r117 and the scenario text.
5. **The stand-in's results for each session.** When an agent's plan holds several results, the stand-in gives them in the order the agent's sessions start. Every later session gets the last result. A plan that holds a single result behaves as it does today. This is a test-only choice and serves the r110 Given.

## 4. Tests the decisions break

- features/supervision.feature:393, the 40-turn scenario: removed by `features retire` (r19, the work-item's Retires). It asserts `--max-turns 40`, which r19 makes false.
- features/supervision.feature:1028 (r74), through the Given at supervision_proposal_steps.py:44: decision 1 breaks it. Today the stand-in gives every bdd-branch-reviewer session the same two findings. Under the loop, every re-review drafts another fix, and either the Then "one work-item was drafted ... part of p1" (which asserts exactly one) fails or the run never ends. The step is rewritten so that "the branch reviewer's result" is the first review's result, holding the two findings, and later reviewer sessions list nothing (decision 5). The scenario text and its Then stay as they are, and the Then still asserts exactly one fix work-item, part of p1, naming the first review's findings.md.
- feature:1232 (r68) and feature:1387 (r104), gates that "every round ends" with no question: decision 3 now leaves an approval question there. Their Thens assert on the brief only, so they are kept unchanged (notes §4, read).
- feature:557, :591, :1034–1050 and the analysis/done scenarios whose single review lists nothing: the loop does not change them, because the first review ends it. Kept (notes §4).
- The quoted-question Then (feature:1243): kept. Decision 4 narrows its pattern without changing what it asserts.

## 5. Open cases

- A reviewer that never lists nothing: under decision 1 the loop runs as long as every fix turns green. The scenarios say nothing about a bound. The implementer names this case and does not pick a bound.
- A re-review whose kept result cannot be read, or that is not DONE: the scenarios do not say whether the loop stops quietly or exits with an error. The implementer names it and follows what `branch_review` does for a first review today.
- A fix that ends `awaiting-answer` or `failed` instead of `green`: no next review follows in this run (r110 is on green). Analysis is not reached either, since the last kept review listed findings. Named, not chosen.
- The exact wording of the approval question, beyond asking for approval of the proposal's lines as drafted and naming the proposal.
