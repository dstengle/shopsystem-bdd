# plan: w198, retire the deprecated scenarios of i37 (supervision)

## 1. What goes green

None of the accepted scenarios is red today. The research ran all 11 accepted test ids and all 11 pass. This work-item retires deprecated scenarios. It adds no behaviour.

- supervision#r121: "a kept branch review whose result gives <outcome> and no question is taken as listing nothing to fix now" (DONE, PARTIAL, BLOCKED, NEEDS_CONTEXT). It passes because `lists_nothing` in `supervise_analysis.py` already takes a missing question as nothing to fix.
- supervision#r75: "an initiative whose work-items are <work-items> and whose kept branch review lists nothing to fix now <measured>" (is measured, is not measured). It passes.
- supervision#r105: "an initiative whose work-items are <work-items>, its delivery otherwise closed, <set>" (is set done, is not set done). It passes.
- supervision#r120: "under a delegation, the session answering a reviewer's question is asked to say in its result whether its answer asks for a change or accepts the work-item as it is". It passes because `VERDICT` is appended to a reviewer's answer brief in `supervise_answers.py`.

Deprecated scenarios retired (the work-item's Retires section), each removed with `features retire`:
- supervision @r75: "when every work-item is green or withdrawn and the kept branch review lists nothing to fix now, `measure initiative` is run on the initiative (deprecated)"
- supervision @r102: "an integrate round is given every requirement id another initiative's kept drafts add that spec/ on the branch it starts from does not hold, whatever that initiative's capability-proposal's status (deprecated)"
- supervision @r105: "an initiative whose work-items are green or withdrawn, whose branch review lists nothing to fix now, whose measurement and analysis record are committed and whose requests are delivered is set done (deprecated)"
- migration-tools @r15: "`migrate run` on a repository with <change> refuses, naming it, exits non-zero and changes no file (deprecated)"
- work-queue @r1: "add with --part-of, --under and --accepts writes a drafted work-item with the fields given (deprecated)"
- work-queue @r23: "a command whose change leaves every work-item of an initiative green or withdrawn, and every request this context asked naming it delivered, sets the initiative to done (deprecated)"
- work-queue @r9: "`work <command>` commits the change it makes to a work-item on the current branch (deprecated)"

"Green" here means: all seven deprecated scenarios are gone, the 11 accepted tests still pass, and the whole suite stays green.

## 2. Where the change lands

- `features/supervision.feature`: remove the deprecated r75, r102 and r105 scenarios.
- `features/migration-tools.feature`: remove the deprecated r15 Outline.
- `features/work-queue.feature`: remove the deprecated r1, r23 and r9 scenarios.
- `tests/scenarios/supervision_integrate_steps.py`: remove the Given step `other_initiative`. Its text is "an initiative <i> under .shop/work/, started, whose kept drafts add <ids> on <capability>, and whose capability-proposal <p> for them is <status>". Added by decision D1.
- `tests/scenarios/test_work_queue.py`: remove the Then step `drafted`. Its text is ".shop/work/<i>/<w>.md is a drafted work-item <w>", the form without "whose". Added by decision D1.

No script changes. The research found no file over 300 lines, and removing these steps only makes the two step modules shorter.

## 3. Decisions

- **D0. Retire with `features retire`, one title at a time.** Pass `--file` wherever a title could match in more than one file. Do not edit the feature files by hand. This rests on the work-item's Retires section. The tests are generated from the feature files and none binds a deprecated title (`tests/` searched for "(deprecated)": no `@scenario` binding names any of the seven). So removing a scenario also removes its test.
- **D1. Remove each step definition that only a retired scenario used.** Two steps are used only by the scenarios this work-item retires:
  - `other_initiative` in `supervision_integrate_steps.py`. Only the deprecated r102 scenario uses it. The live r102 scenario builds the other initiatives with `started_with_proposal` and `keeps_draft`.
  - `drafted` in `test_work_queue.py`. Only the deprecated work-queue r1 scenario uses it, at line 11. The live scenarios use the "whose id is" forms bound in `work_queue_add_steps.py`.

  The helpers `ids_of`, `cap` and `full` that `other_initiative` calls stay, because other steps still use them. No check would catch the two dead steps (vulture runs at `--min-confidence 80`, which skips unused functions), so they are removed here, with the scenarios they served (Retires section). Every other step of the seven retired scenarios is shared with a live scenario:
  - supervision r75 and r105: per the notes.
  - migration r15: "it exits non-zero" is used at lines 128 and 142, among others; "migrate refuses, naming" is in the live r15 scenario.
  - work-queue r23: same steps as the live r23 scenario.
  - work-queue r9: same steps as the live r9 scenario, including the "add i1 w1" When step and the "with no work-item w1" Given step.
  - work-queue r1: its other steps are shared with the live r9 and r1 scenarios.
- **No behaviour decision is taken.** supervision#r75, #r105, #r120 and #r121 are already met by the code, and the work-item asks only for the retirements.

## 4. Tests the decisions break

None that must be rewritten. The tests that go away are the ones generated from the retired scenarios, and they go on purpose with D0:
- `tests/scenarios/test_supervision.py`: the two accepted deprecated tests (r75, r105) and the r102 deprecated test.
- The generated tests in `tests/scenarios/test_migration_tools.py` and `tests/scenarios/test_work_queue.py` for the r15, r1, r23 and r9 deprecated scenarios.

What I verified:
- `tests/scripts/test_bound.py` requires exactly one test per scenario of the bound feature files. Removing a scenario together with its generated test keeps it green (notes, section 4).
- D1 removes only step functions that no remaining scenario names, so no remaining test loses a step.

## 5. Open cases

- The research found three defects (notes, section 6) that no scenario of this work-item covers:
  - D1: the branch-review fix loop has no bound.
  - D2: a one-string `questions` that names a work-item is dropped by `fix_work_item`.
  - D3: an analysis that was cut short is never retried.

  Each one changes what the person running `work run` observes. None is in this work-item's `accepts` or Retires. The implementer names them in the result for a follow-up work-item or request, and does not fix them here.
- If `features retire` refuses a title (for example, if the Retires title of r102 differs from the feature file in any character), the implementer reports it and does not edit by hand.
