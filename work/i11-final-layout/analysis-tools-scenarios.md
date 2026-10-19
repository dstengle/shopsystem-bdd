---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools-scenarios
kind: work-item
part_of: capability-proposal/final-layout-analysis-tools
status: drafted
wkind: capability
under: analysis-tools
accepts: [analysis-tools#r1-r35]
blocked_by: [work-item/pytest-bdd-suite]
fileset: [tests/scenarios/test_analysis_tools.py, tests/scripts/test_tools.py, scripts/tools, .gitignore]
---

# analysis-tools' scenarios as pytest-bdd

Goes green: every scenario of `features/analysis-tools.feature`, bound by
`scenarios("analysis-tools.feature")` in `tests/scenarios/test_analysis_tools.py`, with r8's map in
`.shop/scratch/tools/coverage`.

- Each test in `tests/scripts/test_tools.py` whose docstring is a scenario's title is that scenario's binding
  today: move what it sets up into Given steps, what it runs into When steps and what it asserts into Then
  steps, with `parsers.parse` or `parsers.re` where steps share a shape, then delete the test. Its
  `BindingTest` goes. Tests whose docstring is no title stay as they are.
- `scripts/tools`: `MAP = os.path.join(".shop", "scratch", "tools", "coverage")`, and its help text; nothing
  else changes. `.gitignore` gains `.shop/scratch/` (this work-item or the layout move, whichever lands first).
- A scenario that fails once bound is a finding, not a fix to make here: the docstring test passed, so the
  step definitions differ from it; compare them.
