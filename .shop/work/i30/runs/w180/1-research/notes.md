# w180 research: formulation#r23

Tool use: `tools` ran (`refs`, `tests-of`, `untested` not needed: no function changes). Accepted scenarios found `by search`. Brief gave no `Accepted scenarios:` and no `File set:` line. Scripts: `/home/vscode/shopsystem-bdd/scripts`.

Requirement: `formulation#r23` (spec line 25, approved 2026-10-25, commit 31738369): "When `formulating-features` runs an old scenario alone, it shall run it with `python3 -m pytest`."

## 1. Why each scenario is red today

No accepted scenario exists. By search:
- `grep @r23 features/` gives 7 hits, all in other capabilities' feature files: work-queue.feature:56,74; supervision.feature:509; feature-file-tools.feature:235; migration-tools.feature:454; design-model-check.feature:190,716.
- `features/formulat*` matches nothing (Glob); no `features/formulation.feature`.
- `tests/scenarios/` has no formulation step module (`ls | grep -i formul`: none).

So `formulation#r23` has no scenario, and nothing is red. Missing: a scenario tagged `@r23` in `features/formulation.feature` and its step module. Nothing run for part 1.

## 2. What the system answers today

Run in the worktree, `--collect-only` only, no test executed:
- P1 `python3 -m pytest -q --collect-only -p no:cacheprovider`: `143/877 tests collected (734 deselected)` (pytest.ini `addopts = -n auto -m "not fixture"`). run
- P2 `... -k "retiring a deprecated scenario removes its block" tests/scripts/test_features_scenarios.py`: `11 tests collected`. Unfiltered same file: `11 tests collected`. run
- P3 `... -k "retiring a deprecated scenario removes its block"` (whole suite): `143/877`, same as P1. run
- P4 `... -k "retiring_a_deprecated"` (whole suite): `1/877`. run
- P5 `python3 -m pytest -q -p no:cacheprovider --work-item w180 --co`: `143/877` kept, the same as P1. The work-item accepts only formulation#r23, which has no scenario. run
- P6 same with `-k no_such_zz_name`: `no tests collected (877 deselected)`. run

Reading (read): `scripts/work_items.py:123-131`: a work-item whose capabilities are all `group: guarantees`, left with no test, exits OK. `formulation` is `group: guarantees` (spec frontmatter line 5). So `--work-item w180` cannot fail on a scenario of formulation#r23: none exists. Exit code not seen in a run; read only.

Nearest cases: the spaced `-k` form (P2, P3) selects as much as no `-k`. The skill's own form is not narrowed.

## 3. Old assumptions

Found by search for `python -m pytest` (excluding `.shop/`) and the "run one scenario" wording. Tests executing each: none, since these are skill and agent text that no test reads (`grep tests/ for SKILL.md|skills/` finds none).

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| skills/formulating-features/SKILL.md:26 (process step 4) | runs old scenario alone with `python -m pytest -q -k "<its name>"` | must read `python3 -m pytest`; the `-k "<its name>"` form does not narrow to a title with spaces (P2, P3) | none | search |
| agents/initiative-round.md:20 | the round runs "one scenario by name" for `features deprecate` | same run, same name form | none | search |
| skills/migrating-to-capabilities/SKILL.md:30 | `python -m pytest` as the project's suite command | different concern, not changed by r23 | none | search |
| agents/feature-formulator.md:4 (tools line) | `Read, Glob, Grep, Write`, no Bash | cannot run the old scenario; the run is the round's (initiative-round, which has Bash) | none | read |

## 4. Tests the requirements make impossible to keep

None. The change is skill text. No Python function or branch changes. Searched tests for `SKILL.md`, `skills/`, `formulating-features`, `python -m pytest`: none assert the skill's text (`tests/scripts/test_agents.py:7` only names `feature-formulator` in `SPEC_WRITERS` for role boundaries; the agent has no Bash, unaffected). Method: by search.

## 5. A step the work-item skips

The work-item adds no path. The check the work-item would hold to, a scenario of formulation#r23, never lands: no scenario exists (part 1), and the guarantees rule (part 2, read) lets w180 pass with no test. The existing run path (skill step 4) is the one r23 changes; it has no step left out (read).

## 6. Defects

D1. The skill's `-k "<its name>"` does not narrow to one scenario with a spaced title.
- `python3 -m pytest -q --collect-only -p no:cacheprovider -k "retiring a deprecated scenario removes its block" tests/scripts/test_features_scenarios.py` gives `11 tests collected`; without `-k` the same file gives `11`.
- `... -k "retiring a deprecated scenario removes its block"` on the whole suite gives `143/877`, the same as no `-k`.
- Code-scout's template says `-k` refuses a title with spaces; here pytest did not refuse it. Cause not diagnosed.

## 7. The file set

- `skills/formulating-features/SKILL.md`: line 26, `python -m pytest -q -k "<its name>"` to `python3 -m pytest` (the `-k` form is the planner's choice). Found by grep. 136 lines.
- `agents/initiative-round.md`: line 20 "one scenario by name" only if the planner changes the `-k` form. Not required by r23. 61 lines.
- `features/formulation.feature` (new) and its step module: needed for the scenario r23 lacks. A formulate round writes the feature file, not this work-item. Not created by me.
- Python modules on the path, edited or not: `scripts/work_items.py` (131 lines, room 169 under 300), `conftest.py` (10 lines, room 290), `pytest.ini` (4 lines). None is edited by r23.
- Markdown has no size limit (`CLAUDE.md` limits tracked Python files). `python3 .../tools size --limit 300` printed nothing: no tracked Python file is over 300.
