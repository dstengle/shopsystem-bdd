# plan of w194

Work-item: .shop/work/i33/w194.md, under supervision. It accepts supervision#r120, r121, r75 and r105, and its `## Retires` names the deprecated @r75 PARTIAL scenario (the answer to its first question, reading (a)).
Sources: for r120 and r121, the research notes (.shop/work/i33/runs/w194/1-research/notes.md). For r75 and r105 there are no notes. The second answer told me to plan them from the code, so I read scripts/supervise.py `pull_through`, scripts/supervise_analysis.py, scripts/supervise_done.py, scripts/workqueue_done.py, scripts/measure_write.py and the step modules named below. Earlier plan: 2-plan/plan.md.

## 1. What goes green

- **supervision#r121**: the Outline "a kept branch review whose result gives <outcome> and no question is taken as listing nothing to fix now" (feature:1023), with rows DONE, PARTIAL, BLOCKED and NEEDS_CONTEXT. Every row is red today because its Given "every worker gives DONE, and the branch reviewer's result gives <outcome>, with no question" has no step. Once that step exists, PARTIAL, BLOCKED and NEEDS_CONTEXT stay red: `Analyses.lists_nothing` counts a review as listing nothing only when its status is DONE (notes §1, the §2 probe).
- **supervision#r120**: the scenario "under a delegation, the session answering a reviewer's question is asked to say in its result whether its answer asks for a change or accepts the work-item as it is" (feature:1515). It is red only because its Then has no step. `Answers.answer_brief` already asks for the verdict (probed, notes §2).
- **supervision#r75**: the Outline "an initiative whose work-items are <work-items> and whose kept branch review lists nothing to fix now <measured>" (feature:1058).
  - The row "w1 is green and w2 is withdrawn / is measured" has all its steps defined and the behaviour already exists. It turns green once the stages it runs through are in.
  - The row "w1 is withdrawn and w2 is withdrawn / is not measured" is red in the code. `pull_through` (scripts/supervise.py, line 214) starts the branch review whenever every work-item is green or withdrawn. At line 222 it runs `analyse` (and so `measure initiative`) whenever the review lists nothing. No check anywhere asks for a green work-item. `measure initiative` has no such guard either: no script named measure* mentions green or withdrawn.
- **supervision#r105**: the Outline "an initiative whose work-items are <work-items>, its delivery otherwise closed, <set>" (feature:1454), rows "is set done / is done" and "is not set done / is not done". Both rows are red because of missing steps:
  - the Given "i1 is started and its work-items <work-items>": only the fixed text for "w1 is green and w2 is withdrawn" exists (supervision_done_steps.py:11);
  - the Given "i1's kept branch review lists nothing to fix now, and i1's measurement and analysis record are committed on the initiative branch";
  - the Then "i1 is not done" (only "i1 is done" exists).
  The code already satisfies r105. `set_done` (scripts/supervise_done.py) checks `workqueue_done.holds`, and that function already requires at least one green work-item (scripts/workqueue_done.py line 31). That is w192's work-queue#r23 change, and it is in this base.
- **Retired** (the work-item's `## Retires`): "a kept branch review that ended PARTIAL, with no question and no finding, does not list nothing to fix now, and no `measure initiative` is run (deprecated)" (feature:1050, @r75). It passes today and fails once r121 is in.
- These deprecated scenarios stay, because w194 does not retire them: the r75 DONE scenario (feature:1040) and the r105 scenario (feature:1444). Both still pass under this plan, since their initiative has a green work-item.

## 2. Where the change lands

- **scripts/supervise_analysis.py**: `lists_nothing` stops looking at the status. A readable result with no question lists nothing (r121). Its docstring and the module docstring are rewritten to state r121.
- **scripts/supervise.py**: in `pull_through`, the step that leads on to `analyse` and `set_done` (line 222) also requires at least one of the initiative's work-items to be green (r75). The branch review itself is still started when every work-item is withdrawn: the r75 Then "ran no `measure initiative` … after the branch review was kept" asserts that exactly one branch review ended. The file is 271 lines, so the change must stay within its 29 lines of room; it needs about one. This file was not in the researcher's set. r75 adds it.
- **tests/scenarios/supervision_analysis_steps.py**: two changes.
  - Add the parameterised Given for r121's Outline: the reviewer's result gets the row's status and an empty question list.
  - Remove `reviewer_partial`, the step "…gives PARTIAL, with no question and no finding". Only the retired scenario uses it.
- **tests/scenarios/supervision_delegation_steps.py**: add r120's Then. It finds the brief of the session given the question, through `given_to`, and checks that the brief asks for the verdict (`change` or `accept`).
- **tests/scenarios/supervision_done_steps.py**: three changes for r105.
  - Turn the fixed Given "i1 is started and its work-items w1 is green and w2 is withdrawn" into a parameterised Given over "<name> is <status> and <name> is <status>". The deprecated r105 scenario and the r109 scenario keep working through the same text.
  - Add the Given "i1's kept branch review lists nothing to fix now, and i1's measurement and analysis record are committed on the initiative branch". It sets the stand-in's branch reviewer to give no question, and writes and commits a measurement (under .shop/records/measurements/) and an analysis record (under .shop/records/), named as `Dones.records_committed` matches them.
  - Add the Then "i1 is not done".
  The file is 55 lines.
- **features/supervision.feature**: remove the retired scenario (feature:1050) with `features retire`. Nothing else in the file changes.

These were checked and are not changed: scripts/supervise_answers.py, supervise_done.py, workqueue_done.py, supervise_review.py, supervise_draft.py, the measure scripts, and tests/scenarios/test_supervision.py.

## 3. Decisions

1. **The status of a kept review no longer counts.** A kept branch review lists nothing to fix now when its result gives no question, whatever its status. Rests on supervision#r121.
2. **No new path for non-DONE reviews.** A PARTIAL, BLOCKED or NEEDS_CONTEXT review with no question goes on to `measure initiative`, the analysis and `set_done` through the existing path. Rests on supervision#r121 ("taken as listing nothing"), with r75 and r105.
3. **r75 gets its own guard in `pull_through`.** The at-least-one-green condition for `measure initiative` is checked in `pull_through`, on the work-item statuses, in front of `analyse`. It is not taken from `workqueue_done.holds`. That function also requires every request naming the initiative to be delivered, which r75 does not ask for. Using it would hold back the measurement of an initiative whose request is not yet delivered, and the r75 Outline and the r76/r106 scenarios would then depend on requests. Rests on supervision#r75.
   - The second answer calls the shared done condition "measure initiative's guard". The code has no such guard: `analyse` runs `measure initiative` without one. r75's condition is therefore placed beside the existing r94/r97 check, which repeats the same statuses.
   - The same guard sits in front of `set_done`. That changes nothing a narrator sees, because `holds` already refuses an initiative with no green work-item (r105).
4. **The branch review still runs when every work-item is withdrawn.** It is not gated on a green work-item. The r75 Outline's "is not measured" Then asserts that one branch review ended. Rests on supervision#r75 and its scenario.
5. **r105 needs no production change.** Its condition is already in `set_done`, through `workqueue_done.holds` (work-queue#r23, w192). Rests on supervision#r105.
6. **r120 needs no production change.** Rests on supervision#r120 (notes §2).
7. **The PARTIAL scenario is retired here.** The deprecated scenario at feature:1050 and its step are removed with `features retire`. Rests on the work-item's `## Retires` (answer 1, reading (a)) and design-decision/held-scenarios (0011).

## 4. Tests the decisions break

- **tests/scenarios/test_supervision.py, the test bound to the deprecated PARTIAL scenario (feature:1050).** Decision 1 breaks it. It is removed with its scenario through `features retire`, and its step `reviewer_partial` goes with it (decision 7).
- **The deprecated r105 scenario (feature:1444) and the r109 scenario (feature:1470).** The step change in §2 does not break them. Their Given text "i1 is started and its work-items w1 is green and w2 is withdrawn" must still match the parameterised Given that replaces the fixed one. The implementer checks this by running both scenarios.
- **Nothing else.** What I checked:
  - Decision 3 changes only initiatives with no green work-item. A search of features/ for "is withdrawn and w? is withdrawn" or "are withdrawn" finds only the two new Outline rows. No scenario except r75's has every work-item withdrawn and expects a measurement.
  - No test under tests/ calls `lists_nothing`, `pull_through`, `set_done` or `analyse` directly (searched).
  - Every other user of `reviewer_lists_nothing` gives DONE and is unchanged (notes §4).
  - No test asserts that a reviewer's brief has no verdict ask (notes §4).

## 5. Open cases

For the implementer to name, not to decide:
- A kept review whose result.json is missing, malformed or not a JSON object. Today such a review does not list nothing. r121 does not say.
- A `questions` value that is null, an empty string, or a single string rather than a list (the probe in notes §2). The same applies to a result with no `questions` key at all.
- In r105's "is done" row, `analyse` runs `measure initiative` while a measurement is already committed. If the committed measurement has today's date, `measure initiative` refuses ("exists"; scripts/measure_write.py), the refusal goes to stderr, and `set_done` follows. If it has another date, a second measurement and an analysis session follow. The Given's choice of date decides which of these happens.
- An initiative with no green work-item now gets a branch review and nothing after it. Whether anything should tell the person that it is never measured or set done is left unsaid.
- Whether the parameterised r121 Given or the parameterised r105 Given could also match the text of another existing step.
