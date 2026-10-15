---
id: shopsystem-bdd/analysis-tools
title: Analysis tools
narrator: an agent researching or reviewing a project's code
group: service
rests_on: [decision/scripts-stdlib-only]
formulated_as: features/analysis-tools.feature
retired: []
---

# Analysis tools

## Purpose
`scripts/tools` finds and installs a project's analysis tools in the project's own interpreter, and gives one
interface to them: a coverage map of which tests execute which code, the functions no test executed, the
references to a name, and a lint check. It is not a test runner for the fast suite and edits no dependency
file; it reports what the tools found and names a tool that is missing rather than skipping it.

## Behaviour
- [r1] `tools` looks for the tools in the interpreter given by `--python`, or else in `.venv/bin/python`, `venv/bin/python` or `$VIRTUAL_ENV` under the current directory, or else in the interpreter running the script, and `tools probe` says which it used.
- [r2] **If** the project is not a Python project, `tools` says in one line that no analysis tools are known for its language and exits 1.
- [r3] **When** `tools probe` is run, `tools` prints one line per tool, its version or that it is missing and what it is for, then the interpreter, and exits 1 when any tool is missing.
- [r4] **When** `tools probe --log` is run, `tools` prints the one `Probe: tools -> ...` line to give `plan log`.
- [r5] **When** `tools install` is run, `tools` installs each missing tool into the interpreter with pip and edits no dependency file.
- [r6] **If** the interpreter is not a virtualenv, `tools install` refuses to install into it and says so.
- [r7] **If** a tool is still missing after `tools install`, `tools` prints the tool, what it is for, what the workflow does without it, and the command that failed with the end of its error, and exits 1.
- [r8] **When** `tools map` is run, `tools` runs the suite once under coverage with a context per test, passing arguments after `--` to pytest, and keeps the map in `.superpowers/tools/coverage`.
- [r9] **When** `tools tests-of <file>[:<function, Class.method or line range>]` is run, `tools` prints each test that executed it in the last map, one a line, and how many of the map's tests that is, with the commit the map was made at.
- [r10] **Where** `--by-file` is given, `tools tests-of` prints a count for each test file instead of each test.
- [r11] **If** no test in the map executed the target, or the file has no function by that name, `tools tests-of` exits 1.
- [r12] **If** no map has been made, `tools tests-of` refuses and says to make one with `tools map`.
- [r13] **When** `tools untested <file>...` is run, `tools` prints each function in the files that no test in the last map executed.
- [r14] **When** `tools refs <name>` is run, `tools` prints every reference to that function, class or name defined in the project as `path:line`, including uses through an import or an alias, with the count of production and test files.
- [r15] **If** nothing in the project is defined as `<name>`, `tools refs` exits 1.
- [r16] **When** `tools check` is run, `tools` runs ruff, vulture and, where the project has import contracts, import-linter, over the paths given or the Python files changed since `--base`, each under its own heading, and exits 1 when any reports.
- [r17] **If** a tool `tools check` would run is missing, `tools` names it as missing under its heading instead of skipping it.

## Implementation, may change
- The tools probed are coverage, pytest-cov, jedi, ast-grep, ruff, vulture, import-linter and hypothesis.
- A Python project is one with `pyproject.toml`, `setup.py`, `setup.cfg`, `pytest.ini`, `requirements.txt`,
  `tox.ini` or any `.py` file under the current directory.
- `install` runs `<interpreter> -m pip install <package>` per missing tool.
- `map` runs `pytest -q --cov=. --cov-context=test`, writes the commit it was made at beside the data, and is
  its own command, never part of the fast suite. Code on the path of every call is executed by most of the
  suite, so the map narrows a search only for code off that path; a test that ran and failed counts.
- When the interpreter is not the one running the script, the script re-runs itself under it.
- `refs` uses jedi, so it reads the code as the interpreter would and does not find a name built from a
  string. A test file is under a tests or test directory or named `test_*` or `*_test.*`.
- `check` treats `.importlinter` or a `[tool.importlinter` table in `pyproject.toml` as the project's import
  contracts, and says so under the import-linter heading when there are none; headings are `== <tool> ==`.
- Exit status: 0 success, 1 something is missing, refused or reported, 2 bad usage.

## Not yet
- Only Python projects are known; in any other, agents search by text and say that they did — trigger: a project in another language asks for its analysis tools.
