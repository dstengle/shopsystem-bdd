---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools
title: Analysis tools
narrator: a session researching or reviewing a project's code
group: service
language: codified-2
rests_on: [design-decision/plugin-takes-the-dependencies-it-needs, design-decision/query-commands-answer-in-their-output]
retired: [g1, r1, g2, r2, g3, r3, g4, r4, g5, r5, g6, r6, g9, r9, g10, r10, g11, r11, g12, r12, g13, r13, g14, r14, g15, r15, g16, r16, g17, r17, g18, r18, g19, r19, g20, r20, g21, r21, g22, r22, g23, r23, g24, r24, g25, r25, g26, r26, g27, r27, g28, r28, g29, r29, g30, r30, g31, r31, g32, r32, g33, r33, g34, r34, g35, r35]
unbuilt: []
---

# Analysis tools

## Purpose
`scripts/tools` finds and installs a project's analysis tools in the project's own interpreter, and gives one
interface to them: a coverage map of which tests execute which code, the functions no test executed, the
references to a name, and the lint tools of `tools check`. It is not a test runner for the suite and edits no dependency
file; it prints what the tools found and names a tool that is missing rather than skipping it.

## Terms
- **Python interpreter** (noun): the Python `tools` runs the analysis tools with: the one `--python` gives, else the
  first of `.venv/bin/python`, `venv/bin/python` and `$VIRTUAL_ENV/bin/python` under the current directory that
  exists, else the one that executes `scripts/tools`. Kind of: file. This: the Python interpreter `tools` runs the analysis tools with.
- **environment** (attribute of Python interpreter): whether pip installs into a virtualenv. Values: `virtualenv`, `system`.
- **analysis tool** (noun): a package `tools` probes and installs. Kind of: thing.
- **presence** (attribute of analysis tool): whether the interpreter has the tool, and whether pip can install it.
  Values: `installed`, `missing`, `uninstallable`.
- **`ruff`** (proper noun): the linter ruff. Kind of: analysis tool.
- **`vulture`** (proper noun): the dead-code finder vulture. Kind of: analysis tool.
- **`coverage`** (proper noun): coverage.py, which `tools map` runs the tests under. Kind of: analysis tool.
- **`jedi`** (proper noun): the static analyser jedi, which `tools refs` reads the code with. Kind of: analysis tool.
- **`gf-rgl`** (proper noun): GF's resource grammar library. Kind of: analysis tool.
- **the plugin** (proper noun): the shopsystem-bdd plugin, whose `scripts/tools` this capability is. Kind of: thing.
- **pin** (verb, state): the plugin names the one version of an analysis tool that `tools install` installs. Forms: pins, pinned. Frame: the plugin pins version.
- **pip command** (noun): the command `<interpreter> -m pip install <package>` that `tools install` runs for one analysis tool. Kind of: text.
- **install** (verb, action): `tools` puts an analysis tool, or one version of it, into the Python interpreter with pip. Forms: installs, installed. Frame: `tools` installs analysis tool. Frame: `tools` installs version.
- **coverage map** (noun): what `tools map` writes under `.shop/scratch/tools/coverage`, made at one commit. Kind of: file.
- **make** (verb, action): `tools` writes a coverage map. Forms: makes, made. Frame: `tools` makes coverage map.
- **replace** (verb, action): `tools` writes a new coverage map in place of the one before. Forms: replaces, replaced. Frame: `tools` replaces coverage map.
- **Python file** (noun): a tracked file with a `.py` extension or a `python` shebang, tests included. Kind of: file.
- **function** (noun): a function or method of a Python file. Kind of: thing.
- **execute** (verb, state): a test ran the code of a function when the coverage map was made, or a Python interpreter runs a file. Forms: executes, executed. Frame: test executes function. Frame: Python interpreter executes file.
- **identifier** (noun): a name a Python file may define: a function, a class or a variable. Kind of: thing.
- **define** (verb, state): a Python file binds a name at its top level or in a class. Forms: defines, defined. Frame: Python file defines identifier.
- **reference** (noun): a use of a name the project defines, written `path:line`. Kind of: thing.
- **finding** (noun): what ruff, vulture or import-linter reports. Kind of: text.
- **heading** (noun): the line `== <tool> ==` `tools check` prints above an analysis tool's findings. Kind of: text.
- **log line** (noun): the one line `tools probe --log` prints for a researcher's notes, `Probe: tools -> ` and each analysis tool with its presence. Kind of: text.
- **size limit** (noun): the number of lines `tools size` allows a Python file. Kind of: thing.
- **exceed** (verb, state): a Python file has more lines than a size limit. Forms: exceeds, exceeded. Frame: Python file exceeds size limit.
- **fail** (verb, state): a test does not pass when it runs. Forms: fails, failed. Frame: test fails.
- **dependency file** (noun): a file that lists a project's dependencies (`pyproject.toml`, `requirements.txt`, ...). Kind of: file.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| version | of | analysis tool | one |
| pip command | of | analysis tool | one |
| commit | of | coverage map | one |
| test | in | coverage map |  |
| function | of | Python file | one |
| test | in | Python file | one |
| reference | to | identifier |  |
| heading | of | analysis tool | one |
| finding | of | analysis tool | one |
| finding | in | file | one |

## Behaviour

### [g36] `tools probe --python` prints the Python interpreter it is given
Restates: r1@0.29.
- [r36] When the person runs `tools probe` with the `--python` option set to a Python interpreter, `tools` shall print the Python interpreter.

### [g37] `.venv/bin/python` is the Python interpreter when it exists
Restates: r1@0.29.
- [r37] While the `.venv/bin/python` Python interpreter exists, when the person runs `tools probe` without the `--python` option, `tools` shall print the `.venv/bin/python` Python interpreter.

### [g38] `venv/bin/python` is the Python interpreter when it exists and `.venv/bin/python` does not
Restates: r1@0.29.
- [r38] While the `venv/bin/python` Python interpreter exists and the `.venv/bin/python` Python interpreter does not exist, when the person runs `tools probe` without the `--python` option, `tools` shall print the `venv/bin/python` Python interpreter.

### [g39] `$VIRTUAL_ENV/bin/python` is the Python interpreter when there is no project virtualenv
Restates: r1@0.29.
- [r39] While the `$VIRTUAL_ENV/bin/python` Python interpreter exists and the `.venv/bin/python` Python interpreter does not exist and the `venv/bin/python` Python interpreter does not exist, when the person runs `tools probe` without the `--python` option, `tools` shall print the `$VIRTUAL_ENV/bin/python` Python interpreter.

### [g40] the Python interpreter that executes `scripts/tools` is the Python interpreter when there is no other
Restates: r1@0.29.
- [r40] While the `.venv/bin/python` Python interpreter does not exist and the `venv/bin/python` Python interpreter does not exist and the `$VIRTUAL_ENV/bin/python` Python interpreter does not exist, when the person runs `tools probe` without the `--python` option, `tools` shall print a Python interpreter that executes the `scripts/tools` file.

### [g41] `.venv/bin/python` comes before `venv/bin/python`
Restates: r1@0.29.
- [r41] While the `.venv/bin/python` Python interpreter exists and the `venv/bin/python` Python interpreter exists, when the person runs `tools probe` without the `--python` option, `tools` shall not print the `venv/bin/python` Python interpreter.

### [g7] `tools probe` prints each analysis tool and the Python interpreter
Restates: r3@0.29.
- [r7] While no analysis tool is `missing`, when the person runs `tools probe`, `tools` shall print every analysis tool and exit successfully.

### [g8] `tools probe` exits with an error naming a missing analysis tool
Restates: r3@0.29.
- [r8] While an analysis tool is `missing`, when the person runs `tools probe`, `tools` shall exit with an error naming the analysis tool.

### [g42] `tools probe --log` prints one log line for a researcher's notes
Restates: r4@0.29.
- [r42] When the person runs `tools probe` with the `--log` option, `tools` shall print one log line and every analysis tool.

### [g43] `tools install` installs a missing analysis tool and changes no dependency file
Restates: r5@0.29.
- [r43] While the environment of the Python interpreter is `virtualenv`, when the person runs `tools install`, `tools` shall install every analysis tool whose presence is `missing` and change no dependency file.

```given
the dependency file `requirements.txt` holds "pytest"
```

### [g44] `tools install` installs the one version of `ruff` the plugin pins
Restates: r58@0.29.
- [r44] While `ruff` is `missing` and the environment of the Python interpreter is `virtualenv`, when the person runs `tools install`, `tools` shall install the version of `ruff` that the plugin pins.

### [g45] `tools install` refuses to install into a Python interpreter that is not a virtualenv
Restates: r6@0.29.
- [r45] While an analysis tool is `missing` and the environment of the Python interpreter is `system`, if the person runs `tools install`, then `tools` shall refuse the command and name the analysis tool.

### [g46] an analysis tool still missing after `tools install` is printed with its pip command
Restates: r7@0.29.
- [r46] While an analysis tool is `uninstallable` and the environment of the Python interpreter is `virtualenv`, when the person runs `tools install`, `tools` shall print the pip command of the analysis tool and exit with an error naming the analysis tool.

### [g47] `tools map` makes the coverage map whether or not the tests pass
Restates: r8@0.29.
- [r47] While a test fails, when the person runs `tools map`, `tools` shall make a coverage map and exit successfully.

### [g48] `tools map` replaces the coverage map made before
Restates: r8@0.29.
- [r48] While a coverage map exists, when the person runs `tools map`, `tools` shall replace the coverage map.

### [g49] `tools map --json` prints the commit of the coverage map and the number of its tests
Restates: r56@0.29.
- [r49] When the person runs `tools map` with the `--json` option, `tools` shall make a coverage map and print the commit of the coverage map and the number of tests in the coverage map.

### [g50] `tools tests-of` prints each test that executed its function
Restates: r9@0.29.
- [r50] While a coverage map exists, when the person runs `tools tests-of` on a function, `tools` shall print every test that executes the function, the number of tests that execute the function and the commit of the coverage map.

### [g51] `tools tests-of --by-file` prints each Python file that holds a test that executed the function
Restates: r10@0.29.
- [r51] While a coverage map exists, when the person runs `tools tests-of` with the `--by-file` option on a function, `tools` shall print every Python file that holds a test that executes the function.

### [g52] `tools tests-of` says that no test executed its function, and exits successfully
Restates: r11@0.29.
- [r52] While a coverage map exists, when the person runs `tools tests-of` on a function that no test executes, `tools` shall print the commit of the coverage map and exit successfully.

### [g53] `tools tests-of --json` prints the tests, their number and the commit of the coverage map
Restates: r53@0.29.
- [r53] While a coverage map exists, when the person runs `tools tests-of` with the `--json` option on a function, `tools` shall print every test that executes the function, the number of tests that execute the function and the commit of the coverage map.

### [g54] `tools tests-of` refuses a function its file does not define
Restates: r49@0.29, r57@0.29.
- [r54] While a coverage map exists, if the person runs `tools tests-of` on an identifier that no Python file defines, then `tools` shall refuse the command and name the identifier.

### [g55] `tools tests-of` refuses when there is no coverage map
Restates: r49@0.29.
- [r55] While no coverage map exists, if the person runs `tools tests-of` on a function, then `tools` shall refuse the command and name `tools map`.

### [g56] `tools untested` prints each function of a Python file that no test executed
Restates: r13@0.29.
- [r56] While a coverage map exists, when the person runs `tools untested` on a Python file, `tools` shall print every function of the Python file that no test executes and the commit of the coverage map and exit successfully.

### [g57] `tools untested --json` prints the functions, their number and the commit of the coverage map
Restates: r54@0.29.
- [r57] While a coverage map exists, when the person runs `tools untested` with the `--json` option on a Python file, `tools` shall print every function of the Python file that no test executes and the commit of the coverage map.

### [g58] `tools refs` prints each reference to an identifier and their number
Restates: r14@0.29.
- [r58] When the person runs `tools refs` on an identifier that a Python file defines, `tools` shall print every reference to the identifier and the number of references to the identifier and exit successfully.

### [g68] `tools refs --json` prints the references to an identifier and their number
Restates: r55@0.29.
- [r68] When the person runs `tools refs` with the `--json` option on an identifier that a Python file defines, `tools` shall print every reference to the identifier and the number of references to the identifier.

### [g59] `tools refs` refuses an identifier the project does not define
Restates: r49@0.29.
- [r59] If the person runs `tools refs` on an identifier that no Python file defines, then `tools` shall refuse the command and name the identifier.

### [g60] `tools check` prints each finding under its analysis tool's heading
Restates: r16@0.29.
- [r60] While a file holds a finding of an analysis tool, when the person runs `tools check` on the file, `tools` shall print the heading of the analysis tool and the finding and exit with an error naming the finding.

### [g61] `tools check` names a missing analysis tool
Restates: r17@0.29.
- [r61] While `vulture` is `missing`, when the person runs `tools check`, `tools` shall exit with an error naming `vulture`.

### [g62] `tools tests-of` refuses when `coverage` is missing, naming `tools install`
Restates: r17@0.29.
- [r62] While `coverage` is `missing`, if the person runs `tools tests-of` on a function, then `tools` shall refuse the command and name `coverage` and `tools install`.

### [g63] `tools refs` refuses when `jedi` is missing, naming `tools install`
Restates: r17@0.29.
- [r63] While `jedi` is `missing`, if the person runs `tools refs` on an identifier, then `tools` shall refuse the command and name `jedi` and `tools install`.

### [g64] `tools size --limit` prints each Python file over the size limit, and exits with an error
Restates: r50@0.29, r51@0.29, r52@0.29.
- [r64] While a Python file exceeds a size limit, when the person runs `tools size` with the `--limit` option set to the size limit, `tools` shall print the Python file and exit with an error naming the Python file.

### [g65] `tools size` takes 300 lines as the size limit when `--limit` gives none
Restates: r52@0.29.
- [r65] While no Python file exceeds the `300` size limit, when the person runs `tools size` without the `--limit` option, `tools` shall exit successfully.

### [g66] `tools install` installs the RGL
- [r66] While `gf-rgl` is `missing` and the environment of the Python interpreter is `virtualenv`, when the person runs `tools install`, `tools` shall install `gf-rgl`.

### [g67] `tools probe` reports the RGL
- [r67] When the person runs `tools probe`, `tools` shall print `gf-rgl`.

## Implementation, may change
- A reviewer passes the repository's own limit from its `CLAUDE.md` as `--limit`.
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
  pytest's last line, where the map is and the commit, and is its own command, never part of the suite.
  Code on the path of every call is executed by most of the suite, so the map narrows a search only for code
  off that path; a test that ran and failed counts.
- Refusals (r54, r55, r59 among them) include: an interpreter that does not start (named, with the end of its
  error); `tests-of` or `untested` with no map (saying to run `tools map`); `map` that makes no map (naming the command and the end of
  its output, and keeping the last map); `tests-of` or `untested` on a file that does not exist; `refs` on a
  name nothing in the project defines; `check` with a `--base` git cannot compare (git's error).
- `untested` prints each function as `<path>:<line> <name>`.
- When the interpreter is not the one running the script, the script re-executes itself under it.
- `refs` on a name the project defines exits 0 however many references there are.
- `refs` uses jedi, so it reads the code as the interpreter would and does not find a name built from a
  string. A test file is under a tests or test directory or named `test_*` or `*_test.*`.
- `check` treats `.importlinter` or a `[tool.importlinter` table in `pyproject.toml` as the project's import
  contracts, and says so under the import-linter heading when there are none; headings are `== <tool> ==`. A
  tool that prints nothing is shown clean under its heading; with no file to examine, ruff and vulture say
  `nothing to check` and do not fail.
- Exit code: 0 success, 1 something is missing, refused or found, 2 bad usage.

## Not yet
- Only Python projects are known; in any other, agents search by text and say that they did — trigger: a project in another language asks for its analysis tools.

## Dropped
