---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools
title: Analysis tools
narrator: a session researching or reviewing a project's code
group: service
language: codified-2
rests_on: [design-decision/plugin-takes-the-dependencies-it-needs, design-decision/query-commands-answer-in-their-output]
retired: [g1, r1, g2, r2, g3, r3, g4, r4, g5, r5, g6, r6, g9, r9, g10, r10, g11, r11, g12, r12, g13, r13, g14, r14, g15, r15, g16, r16, g17, r17, g18, r18, g19, r19, g20, r20, g21, r21, g22, r22, g23, r23, g24, r24, g25, r25, g26, r26, g27, r27, g28, r28, g29, r29, g30, r30, g31, r31, g32, r32, g33, r33, g34, r34, g35, r35, g36, r36, g37, r37, g38, r38, g39, r39, g40, r40, g41, r41, g7, r7, g8, r8, g42, r42, g43, r43, g44, r44, g45, r45, g46, r46, g47, r47, g48, r48, g49, r49, g50, r50, g51, r51, g52, r52, g53, r53, g54, r54, g55, r55, g56, r56, g57, r57, g58, r58, g68, r68, g59, r59, g60, r60, g61, r61, g62, r62, g63, r63, g64, r64, g65, r65, g66, r66, g67, r67]
unbuilt: []
---

# Analysis tools

## Purpose
`scripts/tools` finds and installs a project's analysis tools in the project's own interpreter, and gives one
interface to them: a coverage map of which tests execute which code, the functions no test executed, the
references to a name, and the lint tools of `tools check`. It is not a test runner for the suite and edits no dependency
file; it prints what the tools found and names a tool that is missing rather than skipping it.

## Terms

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Relations

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Behaviour

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

- analysis-tools#r56@0.29: the CLI adapter's: the response envelope under --json (the decision "The response envelope", U16)
- analysis-tools#r53@0.29: the CLI adapter's: the response envelope under --json (the decision "The response envelope", U16)
- analysis-tools#r54@0.29: the CLI adapter's: the response envelope under --json (the decision "The response envelope", U16)
- analysis-tools#r55@0.29: the CLI adapter's: the response envelope under --json (the decision "The response envelope", U16)

## Moved

Every line moved to a new capability with a new id (the domain contract, 0.38.0).

| old | new |
|---|---|
| g36 | toolchain#g1 |
| r36 | toolchain#r1 |
| g37 | toolchain#g2 |
| r37 | toolchain#r2 |
| g38 | toolchain#g3 |
| r38 | toolchain#r3 |
| g39 | toolchain#g4 |
| r39 | toolchain#r4 |
| g40 | toolchain#g5 |
| r40 | toolchain#r5 |
| g41 | toolchain#g6 |
| r41 | toolchain#r6 |
| g7 | toolchain#g7 |
| r7 | toolchain#r7 |
| g8 | toolchain#g8 |
| r8 | toolchain#r8 |
| g42 | toolchain#g9 |
| r42 | toolchain#r9 |
| g43 | toolchain#g10 |
| r43 | toolchain#r10 |
| g44 | toolchain#g11 |
| r44 | toolchain#r11 |
| g45 | toolchain#g12 |
| r45 | toolchain#r12 |
| g46 | toolchain#g13 |
| r46 | toolchain#r13 |
| g47 | code-analysis#g1 |
| r47 | code-analysis#r1 |
| g48 | code-analysis#g2 |
| r48 | code-analysis#r2 |
| g49 | dropped |
| r49 | dropped |
| g50 | code-analysis#g3 |
| r50 | code-analysis#r3 |
| g51 | code-analysis#g4 |
| r51 | code-analysis#r4 |
| g52 | code-analysis#g5 |
| r52 | code-analysis#r5 |
| g53 | dropped |
| r53 | dropped |
| g54 | code-analysis#g6 |
| r54 | code-analysis#r6 |
| g55 | code-analysis#g7 |
| r55 | code-analysis#r7 |
| g56 | code-analysis#g8 |
| r56 | code-analysis#r8 |
| g57 | dropped |
| r57 | dropped |
| g58 | code-analysis#g9 |
| r58 | code-analysis#r9 |
| g68 | dropped |
| r68 | dropped |
| g59 | code-analysis#g10 |
| r59 | code-analysis#r10 |
| g60 | code-analysis#g11 |
| r60 | code-analysis#r11 |
| g61 | code-analysis#g12 |
| r61 | code-analysis#r12 |
| g62 | toolchain#g14 |
| r62 | toolchain#r14 |
| g63 | toolchain#g15 |
| r63 | toolchain#r15 |
| g64 | code-analysis#g13 |
| r64 | code-analysis#r13 |
| g65 | code-analysis#g14 |
| r65 | code-analysis#r14 |
| g66 | toolchain#g16 |
| r66 | toolchain#r16 |
| g67 | toolchain#g17 |
| r67 | toolchain#r17 |
