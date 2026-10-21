# Notes: size-check (analysis-tools r50-r52, `tools size`)

Method: `tools map` not run (it writes `.shop/scratch/tools/coverage` outside my scratch), so `tests-of` and `untested` are not run; counts are by search. `refs` not run: `size` is not a defined name. Probes: `.shop/scratch/size-check-1-research/probe_*.py`, run as `python3 -m pytest -q -s -n 0 .shop/scratch/size-check-1-research/<file>`. No CLAUDE.md exists in the checkout (Glob: none; `git log --all -- CLAUDE.md`: empty).

## 1. Why each accepted scenario is red today

Run: `python3 -m pytest -q -n 0 "<node id>"` for the four node ids (`test_size_prints_...`, `test_size_fails_when_one_...`, `test_size_uses_the_limit_...[--limit 250-250-251]`, `[-300-301]`). All four FAILED (run) at their first Given:
`StepDefinitionNotFoundError: Step definition is not found: Given "a Python project in git"` (feature lines 368, 381, 390).

- r50 scenario (feature 366-375): undefined after that Given: `it tracks ...` (lines 369, 370, 371), `it has an untracked src/draft.py of 500 lines` (372), `tools prints src/cart.py with 301 lines, ... and src/report.py with 350 lines` (374), `it prints no other file` (375). `the agent runs `tools size`` is defined (test_analysis_tools.py:22, generic). Code: `scripts/tools` `main()` (lines 66-87) has no `size` subcommand; no `tools_size` module exists (search `tools size|def size` in scripts/: no hit).
- r51 scenario (379-384): undefined: the same Given, `it tracks src/cart.py of 301 lines and src/total.py of 120 lines`. `it exits 1` is defined (test_analysis_tools.py:34). The command today returns 2 (probe P1).
- r52 outline (388-399): undefined: the same Given, `it tracks src/total.py of <within> lines and src/cart.py of <over> lines`, `tools prints src/cart.py with <over> lines`, `it does not print src/total.py`. The command today returns 2; `--limit` is not known either.

Step modules: `analysis_tools_code_steps.py`, `analysis_tools_map_steps.py`, `analysis_tools_probe_steps.py` (grep `@given|@when|@then`): no step matches `a Python project in git` alone (only `... in git with base commit {label}`, `... with no ref named {ref}`, `... whose Python files are unchanged since base commit {label}`). None of the four size Thens exists.

## 2. What the system answers today

Probe P1 (`probe_size.py`, run): a git project built as the Givens describe (src/cart.py 301 lines, tests/test_cart.py 320, src/total.py 300, README.md 900, bin/reprice shebang 400, src/report.py committed 200 then 350 in the working tree, untracked src/draft.py 500).
- `tools --python <py> size`: rc=2, stderr `tools: error: argument command: invalid choice: 'size' (choose from 'probe', 'install', 'map', 'tests-of', 'untested', 'refs', 'check')`.
- `tools --python <py> size --limit 250`: same, rc=2.
- `tools --help` (rc 0) lists seven commands; no size.

Probe P2 (`probe_existing.py`, run): a non-Python project (notes.txt, data/readme.md), `tools --python <py> probe`: rc=1, stderr `tools: no analysis tools are known for this project's language (looked for Python): agents search by text, and say so`.

Probe P3 (run): a Python project (pytest.ini, src/cart.py), `tools --python /bin/false probe` and `... check src/cart.py`: both rc=1, stderr `tools: /bin/false does not run: ` (empty end of error, since /bin/false prints nothing).

Probe P4 (run): `tools --python <py> probe --log` in the same kind of project: rc=0, `Probe: tools -> coverage 7.16.2, pytest-cov 7.1.0, jedi 0.20.0, ast-grep 0.51.0, ruff 0.17.0, vulture 2.16, import-linter 2.15, hypothesis 6.168.5`.

Nearest cases not probed (no code exists to run): size with no git, with an empty project, with a tracked file deleted in the working tree, `--limit 0`, `--limit -1`, `--limit abc`. Read: r50-r52 say nothing about them (see questions).

## 3. Old assumptions

Places that assume the limit is stated in CLAUDE.md, or that `tools size` already runs (read, grep):

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| agents/code-scout.md:22, :68 | tells the scout to read the repository's CLAUDE.md for its size limit, or write "no limit stated" | the limit has a second home, the tool's 300 default (r52); no CLAUDE.md exists in this checkout | none | search (`size limit`, `CLAUDE`) |
| spec/capabilities/code-research.md:27 (r11) | notes give each module's room "under the size limit CLAUDE.md states" | same | none (no features/ or tests/ file names code-research; search) | search |
| agents/architecture-reviewer.md:14, :39 | tells the reviewer to run "the size check" and paste its lines | the check exists after the change; today it refuses (P1) | none | search (`size`) |
| agents/bdd-branch-reviewer.md:62 | expects "the size check's output" in the review's Shape | same | none (test_measure.py:71,625 use the name only as a label) | search |
| agents/bdd-implementer.md, agents/bdd-task-reviewer.md | do not mention size at all (grep `size`) | the work-item's fileset says they gain the done check running `tools size` | none | search |
| skills/bdd-red-green/SKILL.md:90 | BLOCKED row: "no rule in CLAUDE.md says where the code goes" | assumes a CLAUDE.md; none exists | none | search |
| skills/slicing-into-increments/SKILL.md:85 | "a size limit the project's conventions state" | the limit is now also a tool default | none | search |
| scripts/tools_check.py:16 `cmd_check` | splits git's changed-path list with `.split()` | size must not copy this if it lists paths from git | the `--base` scenarios (test_analysis_tools.py, `check --base` ones) run it with names without spaces; they cannot see it (read) | search |
| scripts/tools CONTRACT (lines 13-52) and argparse choices (lines 66-87) | list seven commands and the exit statuses | must list `size` and its `--limit` | none (no test reads the help text; search for `CONTRACT`, `choose from`, `--help` in tests: no hit) | search |

## 4. Tests the requirements make impossible to keep

None. `tests-of` was not run (no map). By search: the requirements add a subcommand and change no existing function's behaviour. Checked:
- tests/scripts/test_tools.py (134 lines, six tests: `test_probe_gives_a_line_a_tool_and_the_interpreter` (asserts 9 lines), `test_install_refuses_...`, `test_the_map_says_...`, `test_untested_names_...`, `test_refs_follow_...`, `test_check_heads_...`): none asserts the list of commands or an argument error; all run commands this change leaves as they are. Sound.
- tests/scenarios/test_analysis_tools.py and the analysis_tools_*_steps.py: no assertion on the command list; `it exits` (test_analysis_tools.py:34-46) asserts no `Traceback` in stderr, which `size` must keep to. Sound.
- No test reads agents/*.md or skills/*.md (grep `agents/`, `SKILL.md` in tests: none).

## 5. A stage the work-item skips

`size` does not call `tools_env.probed()` (tools_env.py:61-66). That function holds two stages the other commands go through:
- (a) the Python-project gate. Its only effect: exit 1 with the one line of "no analysis tools are known" (P2, run). `size` would skip it: a project with no Python prints nothing and exits 0 (not stated by r50-r52; see questions).
- (b) the interpreter-runs check (`versions()`, tools_env.py:53-58). Its only effect: exit 1 with `<python> does not run: <end of stderr>` (P3, run). `size` needs no interpreter, so it has no effect to lose; `--python` would be ignored by `size`. Read.
- (c) the `under()` re-exec (scripts/tools:56-59, used only by tests-of, untested, refs). Read: size does not need it.

## 6. Defects

### D1: `check --base` splits changed paths on whitespace
Probe `probe_space.py` (run): a git repo; base commit with src/old.py; then commit `src/my cart.py` (`import os`, unused).
Command: `python3 <worktree>/scripts/tools --python <py> check --base <base>` in that repo.
Came back (rc=1):
```
== ruff ==
cart.py:1:1: E902 No such file or directory (os error 2)
src/my:1:1: E902 No such file or directory (os error 2)
Found 2 errors.
== vulture ==
Error: .../spaced/src/my could not be found.
== import-linter ==
the project states no import contracts
```
Expected: ruff and vulture check `src/my cart.py` (ruff would report F401). The split comes from scripts/tools_check.py:16 `done.stdout.split()`.

## 7. The file set

Production:
- scripts/tools (99 lines, room 201): add a `size` subparser with `--limit` (int, default 300) in `main()` lines 66-87, its import, and its CONTRACT line. Read + P1.
- scripts/tools_size.py (new; the fileset's `scripts/tools_*.py` covers it): list tracked files (`.py` or a `python` shebang), count lines in the working tree, print those over the limit, exit 1 when any. Read of tools_check.py and tools_env.py.
- On the path, not required to edit: scripts/tools_env.py (105 lines, room 195): `Refused` is the error path `main()` already catches.

Tests:
- tests/scenarios/test_analysis_tools.py (70 lines, room 230): add the import of the new step module (it imports each `analysis_tools_*_steps` by `*`).
- tests/scenarios/analysis_tools_size_steps.py (new): the Givens `a Python project in git`, `it tracks ...`, `it has an untracked ... of N lines`, and the Thens `tools prints ... with N lines`, `it prints no other file`, `it does not print ...`. Check no existing pattern matches these Then texts: `tools prints {tool}, what it is for...` (probe_steps:190) and `tools prints test_total and test_checkout, one a line` (map_steps:168) are exact or differ.
- tests/scenarios/analysis_tools_project.py (183 lines, room 117): `put()` runs `git add -A` before committing, so it cannot leave `src/draft.py` untracked; the step must write that file itself. `started()` writes pytest.ini and src/cart.py only when no `.git` exists (read).

Work-item files that no accepted scenario needs (read): agents/architecture-reviewer.md (52 lines), agents/bdd-branch-reviewer.md (71), agents/bdd-task-reviewer.md (69), agents/bdd-implementer.md (56), agents/code-scout.md (90): prose only. CLAUDE.md: absent; the work-item names it; no scenario reads it.
features/analysis-tools.feature (399 lines, not Python, so not counted): already holds r50-r52; no change needed.

Modules on the change's path, with line counts and room under the 300 limit (r52 default; no CLAUDE.md states another):
- scripts/tools: 99 lines, room 201
- scripts/tools_env.py: 105 lines, room 195
- scripts/tools_size.py (new): room 300 before writing
- tests/scenarios/test_analysis_tools.py: 70 lines, room 230
- tests/scenarios/analysis_tools_project.py: 183 lines, room 117

Tracked Python files over 300 lines now (wc, search for shebang and .py), which `tools size` would print and fail on this repo; not edited here:
- tests/scripts/test_plan.py 766, tests/scripts/test_measure.py 700, scripts/measure 644 (shebang), scripts/plan 423 (shebang).
Every other tracked Python file is under 278 lines (wc, sorted tail).

## Questions for the plan (both readings given)
- CLAUDE.md is absent. The work-item's file set and the agent prompts assume it. Reading A: create it with the module map and the limit. Reading B: the limit is the 300 default only, and the prompts stay as they are.
- Unspecified by r50-r52: non-Python project (exit 0 and print nothing, or refuse as probe does); no git; a tracked file deleted in the working tree; `--limit` with 0, a negative or a non-number.
