---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools-scenarios
kind: work-item
part_of: capability-proposal/final-layout-analysis-tools
status: green
wkind: capability
under: analysis-tools
accepts: [analysis-tools#r1, analysis-tools#r3-r11, analysis-tools#r13-r14, analysis-tools#r16-r17, analysis-tools#r49]
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

Accepts re-synced 2026-10-19 to the EARS lines (initiative/i13): analysis-tools#r2 -> r49; analysis-tools#r12 -> r49; analysis-tools#r15 -> r49; analysis-tools#r18 -> r6; analysis-tools#r19 -> r5; analysis-tools#r20 -> r5; analysis-tools#r21 -> r49; analysis-tools#r22 -> r4; analysis-tools#r23 -> r8; analysis-tools#r24 -> r49; analysis-tools#r25 -> r13; analysis-tools#r26 -> r49; analysis-tools#r27 -> r17; analysis-tools#r28 -> r17; analysis-tools#r29 -> r49; analysis-tools#r30 -> r14; analysis-tools#r31 -> r16; analysis-tools#r32 -> r49; analysis-tools#r33 -> r16; analysis-tools#r34 -> r16; analysis-tools#r35 -> r16.
