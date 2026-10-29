NOT WRITTEN: /tmp/work-run-i59-hfzhnxml/i59-1-integrate/.shop/scratch/1-integrate/drafts/round-2/spec/capabilities/analysis-tools.md (a hook refused it as a "report file")
NOT WRITTEN: /tmp/work-run-i59-hfzhnxml/i59-1-integrate/.shop/scratch/1-integrate/drafts/round-2/spec/capabilities/analysis-tools.draft.md (the same hook refused it too)

The analysis-tools draft for q25 is not on disk. A hook refused both the round-2 path and the .draft.md fallback with "Subagents should return findings as text, not write report files". This reply file was allowed, so the draft's full content follows below, between the BEGIN DRAFT and END DRAFT markers. It needs copying to .../round-2/spec/capabilities/analysis-tools.md by a process the hook allows, or the hook relaxing for drafts paths. The draft follows the form of its sibling feature-file-tools: a whole frontmatter plus the changed Behaviour and Implementation sections. Purpose and Not yet are unchanged and not drafted. The Behaviour rows are exactly round 1's analysis-tools rows. Added: r59-r75. Removed and added to `retired`: r49, r17, r3, r4, r6, r7, r56, r53, r54, r55, r57, r16, r51. Each added line stands where the line it replaces stood; r53, r54 and r55 have no replacement. `rests_on` now names design-decision/commands-and-agents-answer-in-json in place of design-decision/query-commands-answer-in-their-output. In Implementation, "Refusals under r49" now points to r64. The exit-code line now reads "Exit code 0, and 1 only on a crash on an error `tools` does not handle (r63); `ok` is a JSON boolean (r60)." The change list, questions and cut sentences are those of round 1's reply, section "analysis-tools", with nothing new.

=== BEGIN DRAFT spec/capabilities/analysis-tools.md ===
## frontmatter
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools
title: Analysis tools
narrator: a session researching or reviewing a project's code
group: service
rests_on: [design-decision/plugin-takes-the-dependencies-it-needs, design-decision/commands-and-agents-answer-in-json]
retired: [r2, r12, r15, r18, r19, r20, r21, r22, r23, r24, r25, r26, r27, r28, r29, r30, r31, r32, r33, r34, r35, r49, r17, r3, r4, r6, r7, r56, r53, r54, r55, r57, r16, r51]
---

## Behaviour
- [r1] **When** `tools` needs an interpreter, `tools` shall use the first of these, in this order: the one `--python` gives, used as given; `.venv/bin/python` under the current directory, if that file exists; `venv/bin/python` under the current directory, if that file exists; `$VIRTUAL_ENV/bin/python`, if that file exists, wherever `$VIRTUAL_ENV` points; and else the interpreter running the script.
- [r59] `tools` shall give its output as one JSON object on stdout.
- [r60] The JSON object that `tools` gives shall hold the field `ok`.
- [r61] **When** `tools` neither refuses nor finds a tool missing, a lint finding or a file over the size limit, `tools` shall give `ok` true in its JSON object.
- [r62] **When** `tools` ends without crashing on an error it does not handle, `tools` shall exit successfully.
- [r63] **If** `tools` crashes on an error it does not handle, **then** `tools` shall exit with an error.
- [r64] **If** `tools` cannot do what it was asked, **then** `tools` shall give `ok` false in its JSON object, saying why, and change nothing.
- [r65] **If** a tool that `tools check`, `tools tests-of`, `tools untested` or `tools refs` needs is missing, **then** `tools` shall name it in its JSON object as missing rather than skip it, with `ok` false.

### Tools
- [r66] **When** `tools probe` is run, `tools` shall give in its JSON object each tool with its version, or as missing with what it is for, then the interpreter's path and whether it came from `--python`, the project's virtualenv or neither.
- [r67] **If** `tools probe` finds a tool missing, **then** `tools probe` shall give `ok` false in its JSON object.
- [r68] **When** `tools probe --log` is run, `tools` shall give inside a field of its JSON object one line, `Probe: tools -> ...`, naming every tool with its version or `missing`, for a researcher's notes.
- [r5] **When** `tools install` is run, `tools` shall install each missing tool into the interpreter with pip and edit no dependency file.
- [r58] **When** `tools install` installs ruff, `tools` shall install the one version of ruff the plugin pins.
- [r69] **If** `tools install` has a missing tool to install and the interpreter is not a virtualenv, **then** `tools` shall install nothing and say so in its JSON object for each missing tool, with `ok` false.
- [r70] **If** a tool is still missing after `tools install`, **then** `tools` shall give in its JSON object the tool, what it is for, what the workflow does without it, and the command that failed with the end of its error, with `ok` false.

### `map`, `tests-of`, `untested`, `refs`, `check`
- [r8] **When** `tools map` is run, `tools` shall run the suite once under coverage with a context per test, passing arguments after `--` to pytest, replace any earlier map in `.shop/scratch/tools/coverage`, and exit successfully whether or not the tests passed.
- [r71] **When** `tools map` is run, `tools` shall give in its JSON object the map's commit and its test count.
- [r9] **When** `tools tests-of <file>[:<function, Class.method or line range>]` is run, `tools` shall print each test that executed it in the last map, one a line, and how many of the map's tests that is, with the commit the map was made at.
- [r10] **Where** `--by-file` is given, **when** `tools tests-of` is run, `tools` shall print a count for each test file instead of each test.
- [r11] **When** no test in the map executed the target of `tools tests-of`, `tools` shall print that no test of the map executed it, with the commit the map was made at, and exit successfully.
- [r72] **If** the file given to `tools tests-of` has no function by the name given, **then** `tools` shall give `ok` false in its JSON object, saying the target cannot be read.
- [r13] **When** `tools untested <file>...` is run, `tools` shall print each function in the files that no test in the last map executed, how many they are and the commit the map was made at, and exit successfully however many there are.
- [r14] **When** `tools refs <name>` is run on a name the project defines, `tools` shall print every reference to it as `path:line`, including uses through an import or an alias and counting no definition as a reference, then one summary line with the number of references, the number of production files and, apart, of test files that contain them, and where the name is defined.
- [r73] **When** `tools check` is run, `tools` shall run ruff and vulture over the paths given, or in their place the Python files changed since `--base` and not deleted, and, where the project has import contracts, import-linter over the project, giving each one's findings under its own heading.
- [r74] **If** a tool that `tools check` runs finds something, **then** `tools check` shall give `ok` false in its JSON object.
- [r50] **When** `tools size` is run, `tools` shall print each tracked Python file over the size limit in the working tree, a Python file being one with a `.py` extension or a `python` shebang, tests included, with its line count.
- [r75] **If** any tracked Python file is over the size limit, **then** `tools size` shall give `ok` false in its JSON object.
- [r52] **Where** `tools size --limit <n>` is given, `tools size` shall use `<n>` lines as the size limit, and 300 lines otherwise.

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
- Refusals under r64 include: an interpreter that does not start (named, with the end of its error); `tests-of` or
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
- Exit code 0, and 1 only on a crash on an error `tools` does not handle (r63); `ok` is a JSON boolean (r60).
=== END DRAFT ===
