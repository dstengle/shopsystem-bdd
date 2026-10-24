# Plan of w121: --work-item delivers a work-item whose requirements are all guarantees

From the research notes (`1-research/notes.md`), the capability `supervision`, design-decision 0065 and the scenarios at features/supervision.feature:450-497.

## 1. What goes green

- **supervision#r56**, "a worker's pytest run that collects scenarios, none of which its work-item accepts, is refused when a requirement the work-item accepts is not of a guarantees capability" (:469). Red today: undefined Given "spec/capabilities/steady.md is a guarantees capability and spec/capabilities/other.md is not", and the Given "i1's work-item w1 is ready, accepting steady#r1 and other#r1" is undefined too, since the existing step only matches the literals thing#r1 and other#r1. The Then "was refused, saying that w1 accepts none …" exists already. The plugin's refusal happens today, but it does not depend on the capability.
- **supervision#r64**, "a worker's pytest run that collects scenarios, for a work-item every requirement of which is of a guarantees capability, deselects each of them" (:479). Red today: three undefined steps: Given "spec/capabilities/steady.md is a guarantees capability", Given "… accepting steady#r1 and steady#r2", and Then "… was not refused, and deselected "it waits" without running it". scripts/work_items.py refuses the run (probe A, exit 3) and reads no capability group.
- **supervision#r65**, "a worker's pytest run for a work-item every requirement of which is of a guarantees capability, left with no test, exits successfully" (:489). Red today: undefined Givens ("is a guarantees capability", "… which fails, and the repository holds no other test") and undefined Then "… exited successfully". The plugin refuses (probe B, exit 3). Once it deselects instead, pytest exits 5 because no test ran (probe H).
- **Retired:** "a worker's pytest run that collects scenarios, none of which its work-item accepts, is refused (deprecated)" (:459-467, `@r56 @deprecated`). It passes today. It is removed from the feature file, and because test_supervision.py binds by `scenarios("supervision.feature")`, its test goes with it.

## 2. Where the change lands

- `scripts/work_items.py`: reads whether each accepted requirement's capability is a guarantees capability. In the "scenarios collected, none accepted" branch it refuses only when some accepted requirement is not of a guarantees capability (r56). Otherwise it deselects every collected scenario through the same `pytest_deselected` call the normal path uses, keeping the non-scenario tests (r64, r55). When the work-item is all-guarantees and nothing is left to run, the session's exit status "no tests" becomes success (r65). The module docstring says it now reads capability frontmatter.
- `tests/scenarios/supervision_tests_steps.py`: the new Givens and Thens of the three scenarios. The literal "accepting other#r1" Given becomes a general accepting-one-or-two-requirements Given, which also serves "steady#r1", "steady#r1 and steady#r2" and "steady#r1 and other#r1". Also the "holds no other test" variant of the failing-scenario Given, and the Thens "was not refused, and deselected … without running it" and "exited successfully".
- `tests/scenarios/supervision_world.py`: a helper that writes `spec/capabilities/<cap>.md` with or without `group: guarantees` in its frontmatter, if the steps need one there to stay under 300 lines.
- `features/supervision.feature`: the deprecated scenario at :459-467 is removed (Retires).
- `tests/scripts/test_work_items.py`: unit cases for the guarantees path: deselect, exit 0 when nothing is left, and refusal when the requirements mix guarantees and non-guarantees capabilities.

Removed from the researcher's set:
- `tests/scenarios/test_supervision.py`: it binds by `scenarios()`, so the retired scenario disappears without an edit.
- `scripts/supervise_merge.py`: it needs no edit, because the plugin exiting 0 for a guarantees-only work-item is what its exit check at 128-130 needs.

Both are read-only context.

No new step module. The steps belong to the concern supervision_tests_steps.py already holds (the `--work-item` option). That file has 128 lines of room. If it would pass 300 lines, the implementer splits it by that limit (CLAUDE.md).

## 3. Decisions

1. **What counts as a guarantees capability.** A requirement `<cap>#r<n>` is of a guarantees capability exactly when `spec/capabilities/<cap>.md`, under the pytest rootdir, has `group: guarantees` in its frontmatter. This rests on supervision's Implementation line for r56/r64/r65 and on design-decision/workflow-capabilities-are-guarantees. It is the same notion model_facts/model.lp use. work_items.py stays standard-library-and-pytest: it reads the frontmatter line itself and does not import the model.
2. **A missing capability file (researcher's question I).** The requirement is *not* of a guarantees capability, so the run is refused under r56. This rests on decision 1: no file means no `group: guarantees` frontmatter. Any other reading would let a typo in `accepts:` turn the refusal off. The existing unit tests pin this reading: their consumer repo has no `spec/capabilities/` and they keep expecting the refusal. There is no separate "unknown" outcome.
3. **A probe next to an unaccepted scenario of a non-guarantees work-item (researcher's question F2).** The refusal stays as it is today and the probe does not run. This rests on supervision#r56: its condition (scenarios collected, none accepted, a requirement not of a guarantees capability) is met word for word, and r56 is the specific rule for that case. r55 keeps a non-scenario test in a run that is not refused (scenario :450 collects no scenario). This work-item changes neither behaviour, and no scenario or test is added for it.
4. **The deselect path's scope.** It covers the case of r64 only: scenarios collected, none accepted, all requirements guarantees. It deselects every collected scenario and keeps every non-scenario test. A guarantees work-item that does collect accepted scenarios keeps today's normal path (probe E). This rests on r64 and r55.
5. **The success exit.** r65 applies whenever the work-item is all-guarantees and the session ends with no test run. That covers both "everything deselected" (probe B) and "nothing collected" (probe H): r65 says "left with no test" without saying why. A run under `--work-item` for a work-item with a non-guarantees requirement keeps pytest's exit 5, and so does a run without `--work-item` (probe K). This rests on supervision#r65 and design-decision/exits-are-successful-or-errors.
6. **`--whole-suite` runs are unchanged.** That path keeps every test (Implementation line of r22/r43), and neither r64 nor r65 addresses it.

## 4. Tests the decisions break

None. What I verified (from the notes, section 4):
- tests/scripts/test_work_items.py: `test_a_work_item_none_of_whose_scenarios_are_collected_is_refused` and `test_a_non_scenario_does_not_save_a_run…`. Their repository has no `spec/capabilities/`, so under decision 2 they are still refused and stay as they are. The other six of the eight tests do not touch the changed branch.
- tests/scenarios/supervision_tests_steps.py:168, the Then "was refused, saying …", still holds for r56's new scenario.
- The r55 scenario (:450) collects no scenario, so it is untouched.
- The retired deprecated scenario is removed by the Retires section, not broken by a decision.
- The literal Given "i1's work-item w1 is ready, accepting other#r1" (:146) was used only by the retired scenario, so making it general breaks nothing.

## 5. Open cases (for the implementer to name, not to choose)

- How the general "accepting …" Given avoids matching the existing longer Givens "accepting thing#r1, w2 is drafted, …" and "accepting thing#r1, and w2 is awaiting-answer, …" (supervision_tests_steps.py:99, :107).
- How the "deselected "it waits" without running it" Then observes both halves, the deselection and the test not running, in the stub implementer's recorded pytest output.
- Under xdist (`-n auto`), whether the exit-status change takes effect in the controller process, where the session's exit status is set.
- The refusal still ends as an INTERNALERROR with exit 3 (notes D1), and a work-item with no `accepts:` line is reported as "no such work-item" (notes D2). Neither is in this work-item's requirements, so both are left as they are and named in the report.
- A requirement id with no `#` or no capability part in `accepts:`: the scenarios are silent about it.
