---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools
title: Analysis tools
narrator: a session researching or reviewing a project's code
group: service
language: codified-1
rests_on: [design-decision/plugin-takes-the-dependencies-it-needs, design-decision/query-commands-answer-in-their-output]
retired: []
---

# Analysis tools

## Purpose
`scripts/tools` finds and installs a project's analysis tools in the project's own interpreter, and gives one
interface to them: a coverage map of which tests execute which code, the functions no test executed, the
references to a name, and the lint tools of `tools check`. It is not a test runner for the suite and edits no dependency
file; it prints what the tools found and names a tool that is missing rather than skipping it.

## Terms
- **interpreter** (kind): the Python `tools` runs the analysis tools with: the one `--python` gives, else
  `.venv/bin/python` or `venv/bin/python` under the current directory, else `$VIRTUAL_ENV/bin/python`, else the one
  running the script, the first of these whose file exists.
- **environment** (attribute of interpreter): whether pip installs into a virtualenv. Values: `virtualenv`, `system`.
- **analysis tool** (kind): a package `tools` probes and installs: coverage, pytest-cov, jedi, ast-grep, ruff,
  vulture, import-linter and hypothesis.
- **presence** (attribute of analysis tool): whether the interpreter has the tool, and whether pip can install it.
  Values: `installed`, `missing`, `uninstallable`.
- **coverage map** (kind): what `tools map` writes under `.shop/scratch/tools/coverage`: which test executed which
  line, made at one commit.
- **map commit** (kind): the commit the coverage map was made at.
- **Python file** (kind): a tracked file with a `.py` extension or a `python` shebang, tests included.
- **function** (kind): a function or method of a Python file.
- **reference** (kind): a use of a name the project defines, through an import or an alias included, written
  `path:line`; a definition is none.
- **test** (kind): one test of the suite, by its pytest id.
- **finding** (kind): what ruff, vulture or import-linter reports.
- **dependency file** (kind): a file that lists a project's dependencies (`pyproject.toml`, `requirements.txt`, ...).
- **use** (event): `tools` runs the analysis tools with an interpreter. Forms: uses, used.
- **install** (event): `tools` puts an analysis tool into the interpreter with pip. Forms: installs, installed.
- **replace** (event): Forms: replaces, replaced.

## Behaviour

### [g1] `--python` gives the interpreter
Restates: r1@0.29.
- [r1] Where `--python` is given, when the person runs `tools probe`, `tools` shall print the interpreter `--python`.

### [g2] `.venv/bin/python` is the interpreter when it exists
Restates: r1@0.29.
- [r2] When the person runs `tools probe`, `tools` shall print the interpreter.

```given
an interpreter `.venv/bin/python`
```

### [g3] `venv/bin/python` is the interpreter when it exists and `.venv/bin/python` does not
Restates: r1@0.29.
- [r3] When the person runs `tools probe`, `tools` shall print the interpreter.

```given
an interpreter `venv/bin/python`
```

### [g4] `$VIRTUAL_ENV/bin/python` is the interpreter when there is no project virtualenv
Restates: r1@0.29.
- [r4] When the person runs `tools probe`, `tools` shall print the interpreter.

```given
an interpreter `$VIRTUAL_ENV/bin/python`
```

### [g5] the interpreter running the script is the interpreter when there is no other
Restates: r1@0.29.
- [r5] When the person runs `tools probe`, `tools` shall print the interpreter `sys.executable`.

### [g6] `.venv/bin/python` comes before `venv/bin/python`
Restates: r1@0.29.
- [r6] When the person runs `tools probe`, `tools` shall print the interpreter `.venv/bin/python`.
- [r7] When the person runs `tools probe`, `tools` shall not print the interpreter `venv/bin/python`.

```given
an interpreter `venv/bin/python`
an interpreter `.venv/bin/python`
```

### [g7] `tools probe` prints each analysis tool and the interpreter
Restates: r3@0.29.
- [r8] When the person runs `tools probe`, `tools` shall print every analysis tool and the interpreter.
- [r9] When the person runs `tools probe`, `tools` shall exit successfully.

### [g8] `tools probe` exits with an error naming a missing analysis tool
Restates: r3@0.29.
- [r10] While an analysis tool is `missing`, when the person runs `tools probe`, `tools` shall exit with an error naming the analysis tool.

```given
an analysis tool `vulture` that is `missing`
```

### [g9] `tools probe --log` prints one line for a researcher's notes
Restates: r4@0.29.
- [r11] When the person runs `tools probe --log`, `tools` shall print "Probe: tools ->" and every analysis tool.

### [g10] `tools install` installs a missing analysis tool and changes no dependency file
Restates: r5@0.29.
- [r12] While an interpreter is `virtualenv`, when the person runs `tools install`, `tools` shall install every analysis tool that is `missing`.
- [r13] While an interpreter is `virtualenv`, when the person runs `tools install`, `tools` shall not change `requirements.txt`.

```given
an interpreter `.venv/bin/python` that is `virtualenv`
the dependency file `requirements.txt` holds "pytest"
```

### [g11] `tools install` installs the one version of ruff the plugin pins
Restates: r58@0.29.
- [r14] While an analysis tool is `missing` and an interpreter is `virtualenv`, when the person runs `tools install`, `tools` shall install `ruff==0.17.0`.

```given
an analysis tool `ruff` that is `missing`
an interpreter `.venv/bin/python` that is `virtualenv`
```

### [g12] `tools install` installs nothing into an interpreter that is not a virtualenv
Restates: r6@0.29.
- [r15] While an analysis tool is `missing` and an interpreter is `system`, when the person runs `tools install`, `tools` shall not install `jedi`.
- [r16] While an analysis tool is `missing` and an interpreter is `system`, when the person runs `tools install`, `tools` shall exit with an error naming the analysis tool.

```given
an analysis tool `jedi` that is `missing`
an interpreter `.venv/bin/python` that is `system`
```

### [g13] an analysis tool still missing after `tools install` is printed with the failed command
Restates: r7@0.29.
- [r17] While an analysis tool is `uninstallable` and an interpreter is `virtualenv`, when the person runs `tools install`, `tools` shall exit with an error naming the analysis tool.
- [r44] While an analysis tool is `uninstallable` and an interpreter is `virtualenv`, when the person runs `tools install`, `tools` shall print `pip install`.

```given
an analysis tool `jedi` that is `uninstallable`
an interpreter `.venv/bin/python` that is `virtualenv`
```

### [g14] `tools map` writes the coverage map whether or not the tests pass
Restates: r8@0.29.
- [r18] When the person runs `tools map`, `tools` shall write `.shop/scratch/tools/coverage`.
- [r19] When the person runs `tools map`, `tools` shall exit successfully.

```given
a test `test_fails`
```

### [g15] `tools map` replaces the coverage map made before
Restates: r8@0.29.
- [r20] When the person runs `tools map`, `tools` shall replace the coverage map.

```given
a coverage map m1
```

### [g16] `tools map --json` prints the map commit and the number of tests
Restates: r56@0.29.
- [r21] Where `--json` is given, when the person runs `tools map`, `tools` shall print the map commit and the number of tests.

### [g17] `tools tests-of` prints each test that executed its target
Restates: r9@0.29.
- [r22] When the person runs `tools tests-of src/cart.py:total`, `tools` shall print every test, the number of tests and the map commit.

```given
a coverage map m1
```

### [g18] `tools tests-of --by-file` prints a count for each test file
Restates: r10@0.29.
- [r23] Where `--by-file` is given, when the person runs `tools tests-of src/cart.py:total`, `tools` shall print the Python file and the number of tests.

```given
a coverage map m1
a Python file `tests/test_cart.py`
```

### [g19] `tools tests-of` says that no test executed its target, and exits successfully
Restates: r11@0.29.
- [r24] When the person runs `tools tests-of src/cart.py:refund`, `tools` shall print "no test of the map executed" and the map commit.
- [r25] When the person runs `tools tests-of src/cart.py:refund`, `tools` shall exit successfully.

```given
a coverage map m1
```

### [g20] `tools tests-of --json` prints the tests, their number and the map commit
Restates: r53@0.29.
- [r26] Where `--json` is given, when the person runs `tools tests-of src/cart.py:total`, `tools` shall print every test, the number of tests and the map commit.

```given
a coverage map m1
```

### [g21] `tools tests-of` refuses a function its file does not have
Restates: r57@0.29, r49@0.29.
- [r27] If the person runs `tools tests-of src/cart.py:absent`, then `tools` shall exit with an error naming `src/cart.py:absent` and change nothing.

```given
a coverage map m1
```

### [g22] `tools tests-of` refuses when there is no coverage map
Restates: r49@0.29.
- [r28] If the person runs `tools tests-of src/cart.py:total`, then `tools` shall exit with an error naming `tools map` and change nothing.

### [g23] `tools untested` prints each function no test executed
Restates: r13@0.29.
- [r29] When the person runs `tools untested src/cart.py`, `tools` shall print the function, the number of functions and the map commit.
- [r30] When the person runs `tools untested src/cart.py`, `tools` shall exit successfully.

```given
a coverage map m1
a function `refund`
```

### [g24] `tools untested --json` prints the functions, their number and the map commit
Restates: r54@0.29.
- [r31] Where `--json` is given, when the person runs `tools untested src/cart.py`, `tools` shall print the function, the number of functions and the map commit.

```given
a coverage map m1
a function `refund`
```

### [g25] `tools refs` prints each reference and a summary
Restates: r14@0.29.
- [r32] When the person runs `tools refs total`, `tools` shall print the reference and the number of references.

```given
a reference `src/shop.py:4`
```

### [g26] `tools refs --json` prints the references and the summary
Restates: r55@0.29.
- [r33] Where `--json` is given, when the person runs `tools refs total`, `tools` shall print the reference and the number of references.

```given
a reference `src/shop.py:4`
```

### [g27] `tools refs` refuses a name the project does not define
Restates: r49@0.29.
- [r34] If the person runs `tools refs nowhere`, then `tools` shall exit with an error naming `nowhere` and change nothing.

### [g28] `tools check` prints each finding under its tool's heading
Restates: r16@0.29.
- [r35] When the person runs `tools check src`, `tools` shall print the finding and "== ruff ==".
- [r36] When the person runs `tools check src`, `tools` shall exit with an error naming the finding.

```given
a finding `F401`
```

### [g29] `tools check` names a missing analysis tool
Restates: r17@0.29.
- [r37] While an analysis tool is `missing`, when the person runs `tools check src`, `tools` shall exit with an error naming the analysis tool.

```given
an analysis tool `vulture` that is `missing`
```

### [g30] `tools tests-of` names a missing coverage as missing
Restates: r17@0.29.
- [r38] While an analysis tool is `missing`, when the person runs `tools tests-of src/cart.py:total`, `tools` shall exit with an error naming the analysis tool.
- [r45] While an analysis tool is `missing`, when the person runs `tools tests-of src/cart.py:total`, `tools` shall print `tools install`.

```given
an analysis tool `coverage` that is `missing`
```

### [g31] `tools refs` names a missing jedi as missing
Restates: r17@0.29.
- [r39] While an analysis tool is `missing`, when the person runs `tools refs total`, `tools` shall exit with an error naming the analysis tool.
- [r46] While an analysis tool is `missing`, when the person runs `tools refs total`, `tools` shall print `tools install`.

```given
an analysis tool `jedi` that is `missing`
```

### [g32] `tools size` prints each tracked Python file over the limit and exits with an error
Restates: r50@0.29, r51@0.29, r52@0.29.
- [r40] When the person runs `tools size --limit 3`, `tools` shall print the Python file.
- [r41] When the person runs `tools size --limit 3`, `tools` shall exit with an error naming the Python file.

```given
the Python file `big.py` holds:
  a = 1
  b = 2
  c = 3
  d = 4
```

### [g33] `tools size` counts a file with a `python` shebang as a Python file
Restates: r50@0.29.
- [r42] When the person runs `tools size --limit 3`, `tools` shall exit with an error naming the Python file.

```given
the Python file `bin/tool` holds:
  #!/usr/bin/env python3
  a = 1
  b = 2
  c = 3
```

### [g34] `tools size` takes 300 lines as the limit when none is given
Restates: r52@0.29.
- [r43] When the person runs `tools size`, `tools` shall exit successfully.

```given
the Python file `big.py` holds:
  a = 1
  b = 2
  c = 3
  d = 4
```

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
- Refusals under r49 include: an interpreter that does not start (named, with the end of its error); `tests-of` or
  `untested` with no map (saying to run `tools map`); `map` that makes no map (naming the command and the end of
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
