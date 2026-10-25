# plan of w194

Work-item: .shop/work/i33/w194.md, under supervision, accepts supervision#r120 and supervision#r121. It has no `## Retires` and no `## Rulings`.
Plan made from .shop/work/i33/runs/w194/1-research/notes.md, the capability, the feature file and the decisions on deprecated scenarios (0011, 0006) and red-green#r2, review#r10.

## 1. What goes green

- **supervision#r121**: Scenario Outline "a kept branch review whose result gives <outcome> and no question is taken as listing nothing to fix now", rows DONE, PARTIAL, BLOCKED, NEEDS_CONTEXT (features/supervision.feature:1023).
  Red today, every row: the Given "every worker gives DONE, and the branch reviewer's result gives <outcome>, with no question" has no step definition. Once it exists, the DONE row passes, and PARTIAL, BLOCKED and NEEDS_CONTEXT stay red: `Analyses.lists_nothing` in scripts/supervise_analysis.py returns true only when the status is DONE, so `measure initiative` is never run (notes §1 and the §2 probe).
- **supervision#r120**: Scenario "under a delegation, the session answering a reviewer's question is asked to say in its result whether its answer asks for a change or accepts the work-item as it is" (features/supervision.feature:1515).
  Red today only because its Then "the brief of the session answering "<question>" asks it to give in its result whether its answer asks for a change or accepts <work-item> as it is" has no step definition. `Answers.answer_brief` already adds the verdict ask (`VERDICT`) to a reviewer's question (probed, notes §2).
- **Deprecated scenarios this work replaces**: "a kept branch review that ended PARTIAL, with no question and no finding, does not list nothing to fix now, and no `measure initiative` is run (deprecated)" (feature:1050). It is tagged `@r75 @deprecated` and its `Deprecated for:` line names the r121 Outline. It passes today and fails once r121 is in. w194 has no `## Retires`, so the implementer may not remove it. That is the question below. The other deprecated r75 scenario (feature:1040, DONE) still passes and is not retired here: it is deprecated for the r75 Outline.

## 2. Where the change lands

- scripts/supervise_analysis.py: in `lists_nothing`, the review counts as listing nothing to fix now when its result gives no question, whatever its status. Drop the condition on DONE and rewrite the docstring to state r121's rule. The function is 80 lines, so there is plenty of room.
- tests/scenarios/supervision_analysis_steps.py: add the parameterised Given for r121's Outline. It writes the branch reviewer's result with the row's status and an empty question list. Under reading (a) of the question, also remove the step "…gives PARTIAL, with no question and no finding" (lines 37–40), which only the retired scenario uses.
- tests/scenarios/supervision_delegation_steps.py: add r120's Then. It finds the brief of the session given the question, using the file's existing `given_to` helper, and checks that the brief asks for a verdict: `change` when the answer asks for a change, `accept` when it takes the work-item as it is. The file is 202 lines, which leaves room.
- features/supervision.feature: only under reading (a): the scenario at :1050 removed with `features retire`, and nothing else in the file changes.

No other file changes. The notes checked these and found nothing to change: scripts/supervise_answers.py, supervise.py (the call at `pull_through` stays as it is), supervise_done.py, supervise_review.py, supervise_draft.py, tests/scenarios/test_supervision.py.

## 3. Decisions

1. Only the presence of a question decides whether a kept branch review lists nothing to fix now. The status does not count. This rests on supervision#r121.
2. A PARTIAL, BLOCKED or NEEDS_CONTEXT review with no question now leads on to `measure initiative`, the analysis session and `set_done` through the existing `pull_through` path, and nothing is added for it. supervision#r121 says such a review is "taken as listing nothing to fix now", and supervision#r75 and r105 follow from that.
3. r120 needs no change to production code. Only the step that observes the brief is added. This rests on supervision#r120, and the brief already meets it (notes §2).
4. The deprecated PARTIAL scenario is to be retired by this work. design-decision/held-scenarios (0011) says it "is retired by the work that turns its replacement green", and its replacement is r121's Outline. But red-green#r2 and decision 0006 let the implementer retire only a scenario that the work-item lists under Retires, and review#r10 grades any other change under features/ as Critical. w194 lists none: r73 matches on `@r<n>`, and this scenario is tagged r75. I cannot edit the work-item, so this stays open as a question.

## 4. Tests the decisions break

- tests/scenarios/test_supervision.py, the test bound to "a kept branch review that ended PARTIAL, with no question and no finding, does not list nothing to fix now, and no `measure initiative` is run (deprecated)". Decision 1 breaks it: it asserts that no `measure initiative` is run on a PARTIAL review with no question. Under reading (a) it is removed with its scenario (`features retire`) and its step. Under reading (b) it stays and fails.
- Nothing else breaks. The notes (§4, by search, since there is no coverage map) show that every other user of `reviewer_lists_nothing` uses DONE and is unchanged. No test asserts that a reviewer's brief lacks the verdict ask, and the r118/r119 tests and tests/scripts/test_supervise_answers.py are unaffected (run, passed).

## 5. Open cases

For the implementer to name, not to decide:
- A kept review whose result.json is missing, malformed or not an object. Today it does not list nothing (probe), and r121 does not say what it should do.
- A `questions` value that is null, an empty string, or a single non-empty string rather than a list (probe: null and "" count as no question; a non-empty string counts as a question).
- A result that has no `questions` key at all.
- Whether the new parameterised Given's pattern could also match the text of the old PARTIAL step, while both are still present.
