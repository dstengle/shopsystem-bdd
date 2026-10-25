# w180 plan: formulation#r23

## 1. What goes green

- `formulation#r23`, "When `formulating-features` runs an old scenario alone, `formulating-features` shall run it with `python3 -m pytest`." It has no scenario: there is no `features/formulation.feature` and no `@r23` tag of this capability in `features/` (the seven `@r23` hits belong to other capabilities; notes part 1). Nothing is red, and nothing turns green in the suite.
- `formulation` is `group: guarantees` (design-decision/workflow-capabilities-are-guarantees, 0065): it is checked by `measure` on real batches, and `--work-item w180` passes with no test (notes part 2, `scripts/work_items.py:123-131`, read). The work is skill text only.
- Retires: none (the work-item has no Retires section).

## 2. Where the change lands

- `skills/formulating-features/SKILL.md`: process step 4, the bracketed command that runs the old scenario alone: the interpreter becomes `python3 -m pytest`, and the selection names the scenario so that only it is collected (decision 2). Nothing else in the skill changes.

Left out, with why:
- `agents/initiative-round.md` line 20 ("one scenario by name"): still true under decision 2, which selects by a name; not changed.
- `skills/migrating-to-capabilities/SKILL.md:30`: the project's suite command, another concern; r23 does not reach it.
- `agents/feature-formulator.md`: has no Bash and runs nothing; unaffected.
- `features/formulation.feature` and a step module: a formulate round writes feature files (formulation#r1, design-decision/spec-writers-blind-to-code), not an implementer; not created here.
- No Python file changes; no size-limit concern.

## 3. Decisions

1. The command in step 4 uses `python3 -m pytest`, in place of `python -m pytest`. Rests on `formulation#r23`.
2. The command selects the old scenario alone, not by its spaced title. The notes show (D1, probes P2-P4) that `-k "<title with spaces>"` selects as much as no `-k` (143/877 on the suite, 11/11 in one file), while `-k` on the underscored test-function name pytest-bdd derives from the title selected one (1/877). So the skill tells the round to select by the scenario's bound test name (its title in the form pytest-bdd gives the test function), or by its node id, so that one test is collected; the implementer names the form in the skill text. Rests on `formulation#r23` ("runs an old scenario alone") and `formulation#r4`/`#r5`, whose pass/fail verdict is of the old scenario, not of the suite.
3. No scenario is written for r23 in this work-item; it is accepted as a guarantee measured on batches. Rests on design-decision/workflow-capabilities-are-guarantees and formulation#r1 (the formulate round writes scenarios).

## 4. Tests the decisions break

None. Verified from the notes (part 4): no test reads `SKILL.md`, `skills/`, `formulating-features` text or a `python -m pytest` string; `tests/scripts/test_agents.py` names `feature-formulator` only for role boundaries, which this change does not touch.

## 5. Open cases

- A scenario outline: its examples collect as several tests under one name; whether "alone" means all its examples, and how the skill says so.
- An old title that several feature files carry (step 4's `--file` bullet): the selection then has to name the capability's own feature file or test module.
- An old scenario with no binding, or whose test is marked `fixture` and so deselected by `pytest.ini`'s `-m "not fixture"`: the skill's "fails or is not collected" branch then applies; whether the skill says so for a deselected test.
- The `-n auto` from `pytest.ini` applies to the one-scenario run too; whether the skill needs to say anything about it.
- Why pytest accepted the spaced `-k` without refusing it (D1, cause not diagnosed) is for the implementer to note, not to fix in pytest.
