---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools
title: Analysis tools
narrator: a session researching or reviewing a project's code
group: service
language: codified-2
rests_on: [design-decision/plugin-takes-the-dependencies-it-needs, design-decision/query-commands-answer-in-their-output]
retired: [g1, r1, g2, r2, g3, r3, g4, r4, g5, r5, g6, r6, g9, r9, g10, r10, g11, r11, g12, r12, g13, r13, g14, r14, g15, r15, g16, r16, g17, r17, g18, r18, g19, r19, g20, r20, g21, r21, g22, r22, g23, r23, g24, r24, g25, r25, g26, r26, g27, r27, g28, r28, g29, r29, g30, r30, g31, r31, g32, r32, g33, r33, g34, r34, g35, r35]
unbuilt: [r36, r37, r38, r39, r40, r41, r42, r43, r44, r45, r46, r47, r48, r49, r50, r51, r52, r53, r54, r55, r56, r57, r58, r59, r60, r61, r62, r63, r64, r65, r66, r67]
---

# Analysis tools

## Purpose
`scripts/tools` finds and installs a project's analysis tools in the project's own interpreter, and gives one
interface to them: a coverage map of which tests execute which code, the functions no test executed, the
references to a name, and the lint tools of `tools check`. It is not a test runner for the suite and edits no dependency
file; it prints what the tools found and names a tool that is missing rather than skipping it.

## Terms
- **Python interpreter** (noun): the Python `tools` runs the analysis tools with.
- **environment** (attribute of Python interpreter): whether pip installs into a virtualenv. Values: `virtualenv`, `system`.
- **present** (adjective of Python interpreter): a Python interpreter whose file exists.
- **analysis tool** (noun): a package `tools` probes and installs.
- **presence** (attribute of analysis tool): whether the interpreter has the tool, and whether pip can install it.
  Values: `installed`, `missing`, `uninstallable`.
- **coverage map** (noun): what `tools map` writes under `.shop/scratch/tools/coverage`, made at one commit.
- **present** (adjective of coverage map): `tools map` has written the coverage map.
- **map commit** (noun): the commit the coverage map was made at.
- **Python file** (noun): a tracked file with a `.py` extension or a `python` shebang, tests included.
- **function** (noun): a function or method of a Python file.
- **reference** (noun): a use of a name the project defines, written `path:line`.
- **finding** (noun): what ruff, vulture or import-linter reports.
- **dependency file** (noun): a file that lists a project's dependencies (`pyproject.toml`, `requirements.txt`, ...).
- **install** (verb, action): `tools` puts an analysis tool into the interpreter with pip. Forms: installs, installed. Frame: `tools` installs analysis tool.
- **replace** (verb, action): `tools` writes a new coverage map in place of the one before. Forms: replaces, replaced. Frame: `tools` replaces coverage map.

- **file system** (noun): the files and directories of a machine. This: the file system of the machine the command runs on.
- **the dot-venv interpreter** (proper noun): `.venv/bin/python`, the Python interpreter of the project's virtualenv `.venv`. Kind of: Python interpreter.
- **the venv interpreter** (proper noun): `venv/bin/python`, the Python interpreter of the project's virtualenv `venv`. Kind of: Python interpreter.
- **the active-virtualenv interpreter** (proper noun): `$VIRTUAL_ENV/bin/python`, the Python interpreter of the virtualenv that is active. Kind of: Python interpreter.
- **the running interpreter** (proper noun): `sys.executable`, the Python interpreter that runs the script of `tools`. Kind of: Python interpreter.
- **`ruff`** (proper noun): the linter ruff. Kind of: analysis tool.
- **`vulture`** (proper noun): the dead-code finder vulture. Kind of: analysis tool.
- **`coverage`** (proper noun): coverage.py, which `tools map` runs the tests under. Kind of: analysis tool.
- **`jedi`** (proper noun): the static analyser jedi, which `tools refs` reads the code with. Kind of: analysis tool.
- **`gf-rgl`** (proper noun): GF's resource grammar library. Kind of: analysis tool.
- **pinned version** (noun): an analysis tool at the one version the plugin pins for it, as `ruff==0.17.0`. Kind of: analysis tool.
- **pip command** (noun): the command `<interpreter> -m pip install <package>` that `tools install` runs for one analysis tool. Kind of: command.
- **make** (verb, action): `tools` writes a coverage map anew, in place of any before. Forms: makes, made. Frame: `tools` makes coverage map.
- **outcome** (attribute of test): what the last run of a test gave. Values: `passing`, `failing`.
- **execute** (verb, state): a test ran the code of a function when the coverage map was made, as the coverage map records. Forms: executes, executed. Frame: test executes function.
- **identifier** (noun): a name a Python file defines: a function, a class or a variable. Kind of: thing.
- **define** (verb, state): a Python file binds a name at its top level or in a class. Forms: defines, defined. Frame: Python file defines identifier.
- **heading** (noun): the line `== <tool> ==` `tools check` prints above an analysis tool's findings. Kind of: text.
- **log line** (noun): the one line `tools probe --log` prints for a researcher's notes: `Probe: tools -> ` and each analysis tool with its presence. Kind of: text.
- **size limit** (noun): the number of lines `tools size` allows a Python file. Kind of: thing.
- **the default size limit** (proper noun): 300 lines, the size limit of `tools size` when `--limit` gives none. Kind of: size limit.
- **exceed** (verb, state): a Python file has more lines than a size limit. Forms: exceeds, exceeded. Frame: Python file exceeds size limit.
- **test count** (noun): the number of tests that executed a function. Kind of: thing.
- **run count** (noun): the number of tests a coverage map was made from. Kind of: thing.
- **untested count** (noun): the number of functions of a Python file that no test executed. Kind of: thing.
- **dependency manifest** (noun): a file that lists a project's dependencies (`pyproject.toml`, `requirements.txt`, ...). Kind of: file.
- **reference count** (noun): the number of references to an identifier. Kind of: thing.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| pinned version | of | analysis tool | one |
| pip command | of | analysis tool | one |
| commit | of | coverage map | one |
| function | of | Python file | one |
| test | in | Python file | one |
| reference | to | identifier | one |
| heading | of | analysis tool | one |
| finding | of | analysis tool | one |
| finding | in | file | one |
| run count | of | coverage map | one |
| test count | of | function | one |
| untested count | of | Python file | one |
| reference count | of | identifier | one |
| Python interpreter | in | file system |  |
| coverage map | in | repository | one |

## Behaviour

### [g7] `tools probe` prints each analysis tool and the Python interpreter
Restates: r3@0.29.
- [r7] While no analysis tool is `missing`, when the person runs `tools probe`, `tools` shall print every analysis tool and exit successfully.

### [g8] `tools probe` exits with an error naming a missing analysis tool
Restates: r3@0.29.
- [r8] While an analysis tool is `missing`, when the person runs `tools probe`, `tools` shall exit with an error naming the analysis tool.

### [g36] `tools probe --python` prints the Python interpreter it is given
- [r36] When the person runs `tools probe --python` on a Python interpreter, `tools` shall print the Python interpreter.

### [g37] the dot-venv interpreter is the Python interpreter when it exists
- [r37] While this file system holds the dot-venv interpreter, when the person runs `tools probe`, `tools` shall print the dot-venv interpreter.

### [g38] the venv interpreter is the Python interpreter when it exists and the dot-venv interpreter does not
- [r38] While this file system holds the venv interpreter and this file system does not hold the dot-venv interpreter, when the person runs `tools probe`, `tools` shall print the venv interpreter.

### [g39] the active-virtualenv interpreter is the Python interpreter when there is no project virtualenv
- [r39] While this file system holds the active-virtualenv interpreter and this file system does not hold the dot-venv interpreter and this file system does not hold the venv interpreter, when the person runs `tools probe`, `tools` shall print the active-virtualenv interpreter.

### [g40] the running interpreter is the Python interpreter when there is no other
- [r40] While this file system does not hold the dot-venv interpreter and this file system does not hold the venv interpreter and this file system does not hold the active-virtualenv interpreter, when the person runs `tools probe`, `tools` shall print the running interpreter.

### [g41] the dot-venv interpreter comes before the venv interpreter
- [r41] While this file system holds the dot-venv interpreter and this file system holds the venv interpreter, when the person runs `tools probe`, `tools` shall not print the venv interpreter.

### [g42] `tools probe --log` prints one log line for a researcher's notes
- [r42] When the person runs `tools probe --log`, `tools` shall print one log line.

### [g43] `tools install` installs a missing analysis tool and changes no dependency manifest
- [r43] While the environment of the dot-venv interpreter is `virtualenv`, when the person runs `tools install`, `tools` shall install every analysis tool whose presence is `missing` and change no dependency manifest.

```given
the dependency manifest `requirements.txt` holds "pytest"
```

### [g44] `tools install` installs the one version of `ruff` the plugin pins
- [r44] While `ruff` is `missing` and the environment of the dot-venv interpreter is `virtualenv`, when the person runs `tools install`, `tools` shall install the pinned version of `ruff`.

### [g45] `tools install` refuses to install into a Python interpreter that is not a virtualenv
- [r45] While an analysis tool is `missing` and the environment of the dot-venv interpreter is `system`, if the person runs `tools install`, then `tools` shall refuse the command and name the analysis tool.

### [g46] an analysis tool still missing after `tools install` is printed with its pip command
- [r46] While an analysis tool is `uninstallable` and the environment of the dot-venv interpreter is `virtualenv`, when the person runs `tools install`, `tools` shall print the pip command of the analysis tool and exit with an error naming the analysis tool.

### [g47] `tools map` makes the coverage map whether or not the tests pass
- [r47] While a test is `failing`, when the person runs `tools map`, `tools` shall make a coverage map and exit successfully.

### [g48] `tools map` replaces the coverage map made before
- [r48] While this repository holds a coverage map, when the person runs `tools map`, `tools` shall replace the coverage map.

### [g49] `tools map --json` prints the commit of the coverage map and its run count
- [r49] When the person runs `tools map --json`, `tools` shall make a coverage map and print the commit of the coverage map and the run count of the coverage map.

### [g50] `tools tests-of` prints each test that executed its function
- [r50] While this repository holds a coverage map, when the person runs `tools tests-of` on a function, `tools` shall print every test that executes the function, the test count of the function and the commit of the coverage map.

### [g51] `tools tests-of --by-file` prints each Python file that holds a test that executed the function
- [r51] While this repository holds a coverage map, when the person runs `tools tests-of --by-file` on a function, `tools` shall print every Python file that holds a test that executes the function.

### [g52] `tools tests-of` says that no test executed its function, and exits successfully
- [r52] While this repository holds a coverage map, when the person runs `tools tests-of` on a function that no test executes, `tools` shall print the commit of the coverage map and exit successfully.

### [g53] `tools tests-of --json` prints the tests, their count and the commit of the coverage map
- [r53] While this repository holds a coverage map, when the person runs `tools tests-of --json` on a function, `tools` shall print every test that executes the function, the test count of the function and the commit of the coverage map.

### [g54] `tools tests-of` refuses a function that does not exist
- [r54] While this repository holds a coverage map, if the person runs `tools tests-of` on a function that no Python file has, then `tools` shall refuse the command and name the function.

### [g55] `tools tests-of` refuses when there is no coverage map
- [r55] While this repository holds no coverage map, if the person runs `tools tests-of` on a function, then `tools` shall refuse the command and name `tools map`.

### [g56] `tools untested` prints each function of a Python file that no test executed
- [r56] While this repository holds a coverage map, when the person runs `tools untested` on a Python file that has a function that no test executes, `tools` shall print the function, the untested count of the Python file and the commit of the coverage map and exit successfully.

### [g57] `tools untested --json` prints the functions, their count and the commit of the coverage map
- [r57] While this repository holds a coverage map, when the person runs `tools untested --json` on a Python file that has a function that no test executes, `tools` shall print the function, the untested count of the Python file and the commit of the coverage map.

### [g58] `tools refs` prints each reference to an identifier and their count
- [r58] When the person runs `tools refs` on an identifier that a Python file defines, `tools` shall print every reference to the identifier and the reference count of the identifier and exit successfully.

### [g59] `tools refs` refuses an identifier the project does not define
- [r59] If the person runs `tools refs` on an identifier that no Python file defines, then `tools` shall refuse the command and name the identifier.

### [g60] `tools check` prints each finding under its analysis tool's heading
- [r60] While a file holds a finding of an analysis tool, when the person runs `tools check` on the file, `tools` shall print the heading of the analysis tool and the finding and exit with an error naming the finding.

### [g61] `tools check` names a missing analysis tool
- [r61] While `vulture` is `missing`, when the person runs `tools check`, `tools` shall exit with an error naming `vulture`.

### [g62] `tools tests-of` refuses when `coverage` is missing, naming `tools install`
- [r62] While `coverage` is `missing`, if the person runs `tools tests-of` on a function, then `tools` shall refuse the command and name `coverage` and `tools install`.

### [g63] `tools refs` refuses when `jedi` is missing, naming `tools install`
- [r63] While `jedi` is `missing`, if the person runs `tools refs` on an identifier, then `tools` shall refuse the command and name `jedi` and `tools install`.

### [g64] `tools size` prints each Python file over its size limit, and exits with an error
- [r64] While a Python file exceeds a size limit, when the person runs `tools size --limit` on the size limit, `tools` shall print the Python file and exit with an error naming the Python file.

### [g65] `tools size` takes the default size limit when none is given
- [r65] While no Python file exceeds the default size limit, when the person runs `tools size`, `tools` shall exit successfully.

### [g66] `tools install` installs the RGL
- [r66] While `gf-rgl` is `missing` and the environment of the dot-venv interpreter is `virtualenv`, when the person runs `tools install`, `tools` shall install `gf-rgl`.

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
- Refusals (r21, r22, r27 among them) include: an interpreter that does not start (named, with the end of its
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
