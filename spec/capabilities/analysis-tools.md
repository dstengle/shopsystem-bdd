---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools
title: Analysis tools
narrator: an agent researching or reviewing a project's code
group: service
rests_on: [design-decision/plugin-takes-the-dependencies-it-needs]
retired: [r2, r12, r15, r18, r19, r20, r21, r22, r23, r24, r25, r26, r27, r28, r29, r30, r31, r32, r33, r34, r35]
---

# Analysis tools

## Purpose
`scripts/tools` finds and installs a project's analysis tools in the project's own interpreter, and gives one
interface to them: a coverage map of which tests execute which code, the functions no test executed, the
references to a name, and a lint check. It is not a test runner for the fast suite and edits no dependency
file; it reports what the tools found and names a tool that is missing rather than skipping it.

## Behaviour
- [r1] **When** `tools` needs an interpreter, `tools` shall use the first of these, in this order: the one `--python` gives, used as given; `.venv/bin/python` under the current directory, if that file exists; `venv/bin/python` under the current directory, if that file exists; `$VIRTUAL_ENV/bin/python`, if that file exists, wherever `$VIRTUAL_ENV` points; and else the interpreter running the script.
- [r49] **If** `tools` cannot do what it was asked, then `tools` shall exit non-zero, say why, and change nothing.
- [r17] **If** a tool that `tools check`, `tools tests-of`, `tools untested` or `tools refs` needs is missing, then `tools` shall name it as missing rather than skip it.

### Tools
- [r3] **When** `tools probe` is run, `tools` shall print each tool with its version, or as missing with what it is for, then the interpreter's path and whether it came from `--python`, the project's virtualenv or neither, and exit 1 when any tool is missing.
- [r4] **When** `tools probe --log` is run, `tools` shall print one line, `Probe: tools -> ...`, naming every tool with its version or `missing`, for a researcher's notes.
- [r5] **When** `tools install` is run, `tools` shall install each missing tool into the interpreter with pip and edit no dependency file.
- [r6] **If** `tools install` has a missing tool to install and the interpreter is not a virtualenv, then `tools` shall install nothing, say so for each missing tool, and exit 1.
- [r7] **If** a tool is still missing after `tools install`, then `tools` shall print the tool, what it is for, what the workflow does without it, and the command that failed with the end of its error, and exit 1.

### Map, tests-of, untested, refs, check
- [r8] **When** `tools map` is run, `tools` shall run the suite once under coverage with a context per test, passing arguments after `--` to pytest, replace any earlier map in `.shop/scratch/tools/coverage`, and exit 0 whether or not the tests passed.
- [r9] **When** `tools tests-of <file>[:<function, Class.method or line range>]` is run, `tools` shall print each test that executed it in the last map, one a line, and how many of the map's tests that is, with the commit the map was made at.
- [r10] **Where** `--by-file` is given, **when** `tools tests-of` is run, `tools` shall print a count for each test file instead of each test.
- [r11] **If** no test in the map executed the target of `tools tests-of`, or the file has no function by that name, then `tools` shall exit 1.
- [r13] **When** `tools untested <file>...` is run, `tools` shall print each function in the files that no test in the last map executed, how many they are and the commit the map was made at, and exit 0 however many there are.
- [r14] **When** `tools refs <name>` is run on a name the project defines, `tools` shall print every reference to it as `path:line`, including uses through an import or an alias and counting no definition as a reference, then one summary line with the number of references, the number of production files and, apart, of test files that contain them, and where the name is defined.
- [r16] **When** `tools check` is run, `tools` shall run ruff and vulture over the paths given, or in their place the Python files changed since `--base` and not deleted, and, where the project has import contracts, import-linter over the project, each under its own heading, and exit 1 when any reports.

## Implementation, may change
- The tools probed are coverage, pytest-cov, jedi, ast-grep, ruff, vulture, import-linter and hypothesis.
- A Python project is one with `pyproject.toml`, `setup.py`, `setup.cfg`, `pytest.ini`, `requirements.txt`,
  `tox.ini` or any `.py` file under the current directory. In any other, `probe`, `install` and `check` say in
  one line that no analysis tools are known for its language.
- `probe`'s interpreter line says `--python`, the project's virtualenv (`.venv`, `venv` or `$VIRTUAL_ENV` alike)
  or neither; with `--log` it is left out.
- `install` runs `<interpreter> -m pip install <package>` per missing tool, prints each tool it installed, and
  says so and exits 0 when every tool is present, virtualenv or not. Outside a virtualenv it prints, for each
  missing tool, what it is for, what the workflow does without it and that the interpreter is not a virtualenv.
- A missing coverage (`tests-of`, `untested`) or jedi (`refs`) is a refusal saying to run `tools install`; `check`
  names a missing tool under its heading.
- `map` runs `pytest -q --cov=. --cov-context=test`, writes the commit it was made at beside the data, prints
  pytest's last line, where the map is and the commit, and is its own command, never part of the fast suite.
  Code on the path of every call is executed by most of the suite, so the map narrows a search only for code
  off that path; a test that ran and failed counts.
- Refusals under r49 include: an interpreter that does not run (named, with the end of its error); `tests-of` or
  `untested` with no map (saying to run `tools map`); `map` that makes no map (naming the command and the end of
  its output); `tests-of` on a file that does not exist; `refs` on a name nothing in the project defines; `check`
  with a `--base` git cannot compare (git's error).
- `untested` prints each function as `<path>:<line> <name>`.
- When the interpreter is not the one running the script, the script re-runs itself under it.
- `refs` on a name the project defines exits 0 however many references there are.
- `refs` uses jedi, so it reads the code as the interpreter would and does not find a name built from a
  string. A test file is under a tests or test directory or named `test_*` or `*_test.*`.
- `check` treats `.importlinter` or a `[tool.importlinter` table in `pyproject.toml` as the project's import
  contracts, and says so under the import-linter heading when there are none; headings are `== <tool> ==`. A
  tool that prints nothing is reported clean under its heading; with no file to check, ruff and vulture say there
  is nothing to check and do not fail.
- Exit status: 0 success, 1 something is missing, refused or reported, 2 bad usage.

## Not yet
- Only Python projects are known; in any other, agents search by text and say that they did — trigger: a project in another language asks for its analysis tools.
