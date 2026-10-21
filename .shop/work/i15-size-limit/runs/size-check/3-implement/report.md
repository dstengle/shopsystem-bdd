# Report: size-check

## Budget
1. scripts/tools
2. scripts/tools_size.py (new)
3. tests/scenarios/test_analysis_tools.py
4. tests/scenarios/analysis_tools_size_steps.py (new)
5. CLAUDE.md (new)
6. agents/architecture-reviewer.md
7. agents/bdd-branch-reviewer.md
8. agents/bdd-task-reviewer.md
9. agents/bdd-implementer.md
10. agents/code-scout.md

## What changed
- `tools size [--limit N]` (scripts/tools, new scripts/tools_size.py): git ls-files -z, `.py` or python shebang, working-tree line count, prints `<path> <n>` sorted, exit 1 if any. No interpreter/probe gate (plan D2).
- New steps module tests/scenarios/analysis_tools_size_steps.py, imported in test_analysis_tools.py.
- CLAUDE.md (new, module map + 300 limit); the three reviewer prompts, implementer (done check) and code-scout updated.

## Red and green
- Red: `python3 -m pytest -q -n 0 --work-item size-check` -> 4 failed, StepDefinitionNotFoundError on `a Python project in git`. After the steps were written: Then failures (`AssertionError: []`, `assert 2 == 1`, argparse "invalid choice: 'size'"), as expected: no `size` command.
- Green: same command -> 4 passed. Also tests/scenarios/test_analysis_tools.py + tests/scripts/test_tools.py -> 61 passed, 1 skipped.
- Starting suite record: 602 passed, 4 failed at b8bc20d (the four size scenarios).
- Own repo `tools size` was not run (shell refuses it); per plan it reports test_plan.py, test_measure.py, scripts/measure, scripts/plan as already over.

## Tests changed under an allowance
none

## Open questions
- Tracked file deleted in the working tree: currently skipped (unchosen by scenarios).
- `--limit 0` / negative: accepted as given.
- Outside git: exits 1 with git's error.
- Plan contained no code; nothing pasted.

## Outside the file set
none

## Files changed
scripts/tools, scripts/tools_size.py, tests/scenarios/{test_analysis_tools,analysis_tools_size_steps}.py, CLAUDE.md, agents/{architecture-reviewer,bdd-branch-reviewer,bdd-task-reviewer,bdd-implementer,code-scout}.md
Commits: 60b55ca, 25269d9
