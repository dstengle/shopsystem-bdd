# Plan: size-check (analysis-tools r50-r52, `tools size`)

## 1. What goes green

- **analysis-tools#r50**: "size prints each tracked Python file over the limit in the working tree, with its line count". Red: the first Given `a Python project in git` has no step definition (StepDefinitionNotFoundError); the `it tracks ...`, `it has an untracked ...`, `tools prints ... with N lines` and `it prints no other file` steps are undefined too; `scripts/tools` has no `size` subcommand (argparse refuses it, rc 2, probe P1).
- **analysis-tools#r51**: "size fails when one tracked Python file is over the limit". Red: same missing Given and `it tracks src/cart.py of 301 lines and src/total.py of 120 lines`; the command returns 2 today, not 1.
- **analysis-tools#r52**: "size uses the limit --limit gives, and 300 lines without it" (two examples, `--limit 250` and none). Red: same missing Given, the `it tracks src/total.py of <within> lines and src/cart.py of <over> lines` step, `tools prints src/cart.py with <over> lines` and `it does not print src/total.py` are undefined; `--limit` is unknown.

The work-item retires no deprecated scenario.

The work-item also asks for this repository's CLAUDE.md (module map, 300 lines for code and tests), and for the reviewers and the implementer's done check to run `tools size`. No scenario covers these; they are prose.

## 2. Where the change lands

- `scripts/tools`: a `size` subcommand with `--limit` (an integer, default 300) wired in `main()`, and a `size` line in the CONTRACT/`--help` text with its exit statuses. Design-decision plugin-takes-the-dependencies-it-needs says a script's `--help` stays its contract.
- `scripts/tools_size.py` (new): asks git for the tracked files, keeps the Python ones (a `.py` extension or a first line that is a `python` shebang), counts each one's lines as the working tree has them, prints those over the limit with their counts, and exits 1 when there are any.
- `tests/scenarios/test_analysis_tools.py`: imports the new step module, as it already does for each `analysis_tools_*_steps` module.
- `tests/scenarios/analysis_tools_size_steps.py` (new): the Givens `a Python project in git`, `it tracks ...` (the list form, the shebang form, and the committed-then-edited form), `it has an untracked ... of N lines`, and the Thens `tools prints ... with N lines`, `it prints no other file` and `it does not print ...`.
- `tests/scenarios/analysis_tools_project.py`: only if the new steps need a helper there. `put()` stages everything before it commits, so the untracked file has to be written outside it, and the edited file has to be changed after its commit.
- `CLAUDE.md` (new): the module map and the size limit, 300 lines for code and tests (the work-item says so).
- `agents/architecture-reviewer.md`, `agents/bdd-branch-reviewer.md`, `agents/bdd-task-reviewer.md`: "the size check" becomes running `tools size --limit <the CLAUDE.md limit>` and pasting its lines.
- `agents/bdd-implementer.md`: its done check runs `tools size`.
- `agents/code-scout.md`: it reads the limit from CLAUDE.md, and when CLAUDE.md states none it uses the `tools size` default of 300 instead of "no limit stated".

Removed from the researcher's set: `scripts/tools_env.py`. It is on the path (`Refused`), but nothing in it is edited.

## 3. Decisions

- **D1. CLAUDE.md is created** with the module map and the 300-line limit, and the agent prompts point at it. The researcher asked about this, and the work-item settles it: its "Goes green" names "this repository's CLAUDE.md (module map, 300 lines for code and tests)", and CLAUDE.md is in its fileset. The capability's Implementation line "A reviewer passes the repository's own limit from its CLAUDE.md as `--limit`" agrees.
- **D2. `size` does not go through the Python-project gate or the interpreter check** (`probed()`), and does not re-run itself under the project's interpreter. In a project with no tracked Python file it prints nothing and exits 0. This rests on #r50 and #r51: there is no file to print, and exit 1 needs a file over the limit. It also rests on the Implementation section, which lists only `probe`, `install` and `check` as giving the "no analysis tools are known" line. `--python` is accepted but has no effect on `size`.
- **D3. Outside a git repository, `size` refuses**: it exits non-zero with git's error and changes nothing. Rests on #r49: the tracked files cannot be listed.
- **D4. A `--limit` that is not an integer is bad usage** and exits 2, from argparse. Rests on the Implementation exit-status line (2 is bad usage) and on #r49.
- **D5. Tracked paths are read from git with NUL-separated output, never split on whitespace**, so a path with a space is counted under its real name. This avoids the defect the researcher found in `check --base` (scripts/tools_check.py:16). Rests on #r50 ("each tracked Python file"). That defect is not fixed here; it is outside this work-item.
- **D6. The printed line is the repository-relative path and its line count**, one file a line. The step text "prints src/cart.py with 301 lines" is what pins this. Lines are counted as the file's newline-terminated lines, like `wc -l`, plus a last line with no newline at its end.
- **D7. The output order is sorted by path**, so it is stable. Rests on #r50: the scenario pins the set of files printed, not their order, so the Then step checks the set.

## 4. Tests the decisions break

None. Checked:
- tests/scripts/test_tools.py: its six tests run probe, install, map, untested, refs and check. None asserts the command list or the help text.
- tests/scenarios/test_analysis_tools.py and the analysis_tools_*_steps modules: none asserts the command list. The `it exits` step asserts no Traceback in stderr, and `size` must keep to that.
- No test reads agents/*.md or CLAUDE.md (the researcher's search).

The new Then texts must not collide with existing patterns: `tools prints {tool}, what it is for...` (probe_steps) and `tools prints test_total and test_checkout, one a line` (map_steps). Name the new patterns so that neither matches them.

## 5. Open cases (for the implementer to name, not to choose)

- A tracked file deleted in the working tree: skipped, refused, or reported. r50 says "in the working tree"; the scenarios are silent.
- `--limit 0` or a negative `--limit`: accepted as given, or refused as bad usage.
- Whether the help text names the 300 default.
- This repository fails `tools size` today: tests/scripts/test_plan.py 766, tests/scripts/test_measure.py 700, scripts/measure 644, scripts/plan 423. Other i15 work splits them. Until it does, the implementer's and reviewers' done check will report these four. Name how the prompts treat files over the limit that the change did not touch.
- The other prose that assumes CLAUDE.md is outside this file set: spec/capabilities/code-research.md r11, skills/bdd-red-green/SKILL.md:90 and skills/slicing-into-increments/SKILL.md:85. Leave them.
