# w233 plan: supervision#r211

## 1. What goes green

- **supervision#r211**: when `work run` reads the delegation of an initiative's request, it reads the delegation the request has at that moment, whether it was given before or after the initiative started.
  - Scenario Outline "`work run` reads the delegation the request has when it reads it, the delegation given <when> the initiative started" (features/supervision.feature:1373-1386), examples `before` and `after`.
  - Why red (notes §1, run): both examples fail at their first Given (line 1376) with StepDefinitionNotFoundError. The only step that matches "i1 fulfils the request q1, which gives the delegation …" is anchored at the closing quote, and no step accepts the trailing ", given before|after i1 started". No later step ran, so their status is not yet known from a run.
- Retires: none. The work-item has no Retires section and no Rulings.

## 2. Where the change lands

- `tests/scenarios/supervision_delegation_steps.py`: add one Given for the "…, given <when> i1 started" form. The module docstring gains r211. The existing Given at line 14 stays as it is for the r78, r210 and glossary scenarios that use it. The file has 238 lines now. The new step must keep it at 300 or fewer.

No production file. The notes (§2, read) say `scripts/supervise_answers.py` (`Answers.delegation`) already reads the request on every call. `supervise.py` calls `answers()` at the head of every `pull_through`, and `supervise_raise.py` uses the same read. Nothing copies the delegation at start: `workqueue_start.py` writes none. This matches the researcher's file set.

## 3. Decisions

1. **What "after i1 started" means in the fixture.** For `after`, the step first writes and commits the initiative (status started, fulfils q1) with request q1 accepted and **no** `delegation` field. Then, in a separate later commit, it adds the delegation to q1, before `work run`. For `before`, the request carries the delegation in the same commit that starts the initiative, as the existing step does. Rests on supervision#r211 ("given before or after the initiative started"). The order of the commits is the only thing that separates the two examples, so the `after` fixture must give an initiative under way with no delegation.
2. **A new step, the old one unchanged.** The new step reuses the writing the existing Given does (initiative.md, q1.md, `context["delegation"]`) and does not copy it. The existing step's pattern stays anchored as it is, so no other scenario's matching changes. The Thens at lines 171-185 read `context["delegation"]`, so the new step sets it in both examples. Rests on supervision#r211 and on CLAUDE.md's size limit (the file has room for 62 lines).
3. **No production change.** The live read already does what r211 asks (notes §2). The plan adds no cache and no copy at start. Rests on supervision#r211.

None of these decisions changes what the narrator observes, so no question is raised.

## 4. Tests the decisions break

None. The existing Given at line 14 keeps its pattern, so the r78, r210 and glossary-proposal scenarios match exactly as before. `tests/scenarios/supervision_session_faults_steps.py:63` (its own fulfils-with-delegation Given) is not touched. The notes (§3) found no test that asserts a delegation copied at start. Production is unchanged, so no script test is affected. This was checked against the notes and the first 50 lines of the step file. The other delegation tests were not run.

## 5. Open cases

- The run stopped at line 1376, so lines 1377-1381 have not been run in this scenario. They are expected to match existing steps: line 1377 is the faults Given at supervision_faults_steps.py:127, line 1378 is used by r78, and lines 1380 and 1381 have the r210 and r78 forms with one named file. The implementer confirms this once the new Given is in and names any step that still does not match.
- Whether the `after` example should also show that a delegation **changed** after start (not only one added) is read and not the earlier one. The scenario covers only adding one. The implementer names this case and does not test it.
- What `work run` does when a delegation is **removed** after start. The scenarios do not cover it. The implementer names it and leaves it for a later requirement.
