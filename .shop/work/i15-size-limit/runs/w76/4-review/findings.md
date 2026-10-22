# Review: size-check (i15-size-limit)

**Verdict: DONE.** No finding is Critical or triaged fix now. `tools size` does what r50-r52 say and the four scenarios pass. There are four Minor findings, all in lint, the CLAUDE.md map or hardening.

## Commits reviewed

The branch `work/size-check` no longer exists. The commits come from the checked-out history, between `b8bc20d work: size-check ready -> claimed` and `95458c4 work: size-check claimed -> done`, leaving out work run's `work:` commits:

- `60b55ca` tools size: tracked Python files over the line limit (analysis-tools r50-r52). Touches scripts/tools, scripts/tools_size.py (new), tests/scenarios/analysis_tools_size_steps.py (new) and tests/scenarios/test_analysis_tools.py.
- `25269d9` CLAUDE.md with module map and 300-line limit; reviewers, implementer and scout use tools size. Touches CLAUDE.md (new) and agents/{architecture-reviewer,bdd-branch-reviewer,bdd-implementer,bdd-task-reviewer,code-scout}.md.

These match the implementer's `result.json` (`commits`: 60b55ca, 25269d9). Every file is in the work-item's fileset. Nothing under `features/` changed: `git diff b8bc20d 25269d9` has no features/ path.

## Removed and weakened tests

None. I searched the diff b8bc20d..25269d9 for any `-` line in tests/: the only test changes are one added import line in test_analysis_tools.py and a new steps module. No test function was deleted, no parametrize case dropped, no assert removed or loosened, and no skip or xfail added. This matches plan §4 ("None").

## Allowances

The report's `## Tests changed under an allowance` says "none", so there are no rows to check.

## Cannot verify

- The report's red run (4 failed on StepDefinitionNotFoundError, then Then failures) and the starting suite record "602 passed, 4 failed at b8bc20d". These cannot be seen from the commits.
- The report's claim that `tools size` "was not run (shell refuses it)". I ran it, and it prints the four files already over (below). The report does not include those lines.
- Whether the changed agent prompts make agents run `tools size`. The prompts are prose; no scenario covers them.

## Findings

### F1. Minor: new import breaks the sorted import block (observation)
- tests/scenarios/test_analysis_tools.py:15. `from .analysis_tools_size_steps import *` comes before `from .analysis_tools_project import ...`, so ruff reports `I001 Import block is un-sorted`. Lines 12-14 already had RUF100, so the new line repeats an existing pattern. The I001 comes from this placement.
- Why it matters: `tools check` reports on a file the commits touched.
- Fix: move the line below the `analysis_tools_project` import.
- Work-item: size-check.

### F2. Minor: ruff findings in the new module (drop)
- scripts/tools_size.py:10 `PLW1510 subprocess.run without explicit check`, and :44 `UP031` (percent format). tests/scenarios/analysis_tools_size_steps.py:14 `UP031`.
- Why it matters: lint noise only. The returncode is checked by hand at :11, and the other tools_*.py modules use the same style.
- Fix: `check=False` and f-strings, if the project wants ruff clean.
- Work-item: size-check.

### F3. Minor: the CLAUDE.md module map leaves out modules and states a naming rule the tree does not follow (observation)
- CLAUDE.md:10-22. The map has no row for `scripts/measure`, `scripts/plan`, `scripts/work`, `scripts/workqueue.py` or `scripts/model.lp`. The `tests/scenarios/` row says "one `<capability>_*_steps.py` module a concern", but many existing modules do not end in `_steps.py`: `design_model_check_given.py`, `supervision_world.py`, `feature_file_tools_files.py`, `migration_old.py` and others (`ls tests/scenarios/`).
- Why it matters: the architecture and branch reviewers now check "each module-map row, met or not", so they will report this row as unmet on code this work-item did not write. The map also does not say where the measure, plan and work code belongs.
- Fix: add rows for the missing scripts, and phrase the steps row as `<capability>_*.py`.
- Work-item: size-check.

### F4. Minor: `size` covers only the current directory and refuses non-UTF-8 names with a traceback (observation)
- scripts/tools_size.py:10. `git ls-files -z` is run in the cwd, so `tools size` run from a subdirectory lists only that subtree. Paths come out relative to it, so the counts are right, but r50's "each tracked Python file" is narrowed. Also, `text=True` decodes git's output strictly, so a tracked filename that is not valid UTF-8 raises UnicodeDecodeError with a traceback instead of a refusal (r49).
- Reproduction: read only. My shell does not allow `cd` or creating a git repository in scratch, so neither was run. The risk is from the code: `subprocess.run(["git","ls-files","-z"], ..., text=True)` with no `cwd=` and no `errors=`.
- Why it matters: no client does either today. CLAUDE.md and the prompts run it from the repository root.
- Fix: list from `git rev-parse --show-toplevel` (or use `--full-name` and open from the top), and decode with `errors="surrogateescape"`.
- Work-item: size-check.

### Read and found sound
- Deleted tracked file: `line_count` raises OSError and is skipped (report's open question; plan §5 left it open). A tracked submodule or a symlink to a directory is skipped the same way.
- Outside git: git's stderr is passed through and the exit is 1 (plan D3, r49).
- `--limit abc` exits 2 through argparse (D4). Paths are read NUL-separated (D5). Output is sorted, in the form `<path> <n>` (D6, D7).
- Step patterns: `prints_files` needs `, ` or ` and ` after the first "lines", so it cannot take the single-file r52 Then. The `it tracks` regex needs `\S+ of N lines`, so it does not take the shebang or edited forms. Running the four scenarios shows each step binds as meant.
- The CONTRACT gains a `size` entry (decision 0035: `--help` stays the contract).
- Purpose and Behaviour lines: no contradiction. `size` installs nothing and edits no dependency file. r17 does not name `size`.

## Checks run

- `python3 -m pytest -q -n 0 tests/scenarios/test_analysis_tools.py -k size` → 4 passed, 52 deselected.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base b8bc20d`:
  - == ruff ==: 10 errors. The four in this change are in F1 and F2. The rest (test_analysis_tools.py:12-14 RUF100, :42 and :54 UP031) were there before.
  - == vulture ==: clean.
  - == import-linter ==: the project states no import contracts.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` → exit 1. It prints scripts/measure 644, scripts/plan 423, tests/scripts/test_measure.py 700 and tests/scripts/test_plan.py 766. All four were **already over**, and none was touched by these commits. The files the commits touched are under the limit: scripts/tools 107 lines, tools_size.py 46, analysis_tools_size_steps.py 68, test_analysis_tools.py 71.
- `git log --stat b8bc20d..95458c4` and `git diff b8bc20d 25269d9`: the commits and their diff, read once.
