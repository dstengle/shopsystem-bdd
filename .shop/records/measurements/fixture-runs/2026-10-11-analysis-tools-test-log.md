---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-11-analysis-tools-test-log
kind: measurement
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-11
---

# Analysis tools: test log (0.15.0)

Spec: `docs/superpowers/specs/2026-10-11-analysis-tools-design.md`.

## `scripts/tools`

`python3 -m unittest discover -s tests/scripts`: 93 OK, 9 in `test_tools.py`, run here against coverage 7.16,
pytest-cov 7.1 and jedi 0.20 (three are skipped where those are not installed). Pinned: a line a tool and the
interpreter; the one line for the plan's log; a project with no Python told so; `install` refusing an interpreter
that is not a virtualenv, with the tool, what it is for, what the workflow does without it and what was tried; the
map and `tests-of` for a function, a method, a line range and `--by-file`; `untested`; `refs` through an import
and through `import … as`; `check`'s three headings.

Two things the first runs showed, both fixed:

- jedi gave the import line for `from shelf.store import add as put` and not the calls of `put`. `refs` now
  follows an alias within its file.
- On kb, `refs` saw only references in the defining file: a package under `src/`, installed for development, is
  found at run time by an import hook jedi does not follow. `refs` gives jedi the `src` directory.

## On kb, in a scratch clone with its own virtualenv

`/home/vscode/scratch/shopsystem-bdd/kbmap/repo`, cloned from kb and never pushed; kb's own checkout and
virtualenv were not touched.

- **`install`.** With coverage, pytest-cov and jedi there already, it installed ast-grep, ruff, vulture,
  import-linter and hypothesis into the clone's `.venv`; `probe` then exits 0, and `git status` shows no file
  changed.
- **`map`.** 74 s, against 24 s for the suite: `111 failed, 763 passed`, the counts of kb's own record at that
  commit.
- **`tests-of`, at the commit before slice 163's hand-back.** The hand-back's commit changed 11 functions. Four are
  executed by 577 or 578 of the map's 874 tests, four by 153 to 176, three by 16 to 29. Taken by the lines it
  changed and not by function, 577. The six tests it broke are in two test files; `_append` and `_collections_at`,
  executed by 29 and 23 tests, lead to five of them. So for code on every call's path the map does not narrow the
  search for "tests the decisions break", and for code off it, it does. The scout's text was changed to say which
  it met, with the number.
- **`refs`.** `kb.changes.replacing`: one reference, `src/kb/servicer.py:81`. A search for the word: 17 lines in 9
  files, the others a test helper of the same name and prose. `kb.edits.apply`, `kb.composition.version_schema`
  and `kb.composition.conformed`: 1, 2 and 2, each the same as a search with the definition taken out. Each call
  about 0.2 s.
- **`check`** over three commits: four lint lines, vulture clean, "the project states no import contracts".

## A consequence sweep of batch 33's decision, at batch 33's base

The same clone at `75740ca`, the commit batch 33 started from, with a map made there. One dispatch each to a
Haiku and a Sonnet `code-scout`: the old assumption (an artifact is read, checked, linked, exported and imported
through its type's latest version, the only one held) and what replaces it.

| | Haiku | Sonnet |
|---|---|---|
| rows | 42 | 39 |
| tokens, time | 103k, 154 s | 64k, 77 s |
| tools called | `refs`, `tests-of`, `untested` | the same |

Against what batch 33 and 34 found late, each from a review:

| found late | by | in the Haiku table | in the Sonnet table |
|---|---|---|---|
| reads of an artifact behind its type go through the latest version (slice 163.1 added) | slice 162's task review | `read.py:_shown`, `_summary` | `read.py:_shown/stub/stubs`, `_summary`, `_resolved`, `query.py:_outward` |
| a type's change restates its artifacts' links (163.2, 163.3 added) | the same review | `sqlite_checks.py:_restated`, `drafting.py:_relinked` | `port.py Change.through/Relink.through`, `sqlite_checks.py:_restated` |
| an exported store does not import readably (batch 34) | batch 33's branch review | `export.py:written`, `_ordered`; four import rows | `export.py:_ordered`, `written`; `importing.py:_faults`, `_beneath` |
| a type another type's version reads can be removed (165.1 added) | slice 165's task review | not there | not there |

Three of the four were in both tables before a slice was cut. The fourth, a removal, is not a place that reads the
old form, and a sweep that starts from readers did not reach it. Each row gives the tests that execute its place
(`29 of 845`, `560/845`) and how it was found (`refs`, `by reading`, `search`).

One run each; the tables were scored by reading them against the four findings, not by a script.

## The scout on the small fixture

`/home/vscode/scratch/shopsystem-bdd/allow/`, variant Z: five tests the decisions break, two of them reaching the
changed function through a test helper and through a production module. Task research, headless.

- 0.14.0, three runs: all five named in each. On eleven files a search is enough, so this fixture shows no
  difference.
- 0.15.0, two runs, with a map: all five named; `tools refs`, `tests-of` and `untested` called; the notes say how
  each list was made ("Counts marked `by search` are grep results, a floor"; "Source: `tools tests-of
  shelf/store.py:9-11`, then each listed test read") and that the map is one test older than the suite.

## Not tested

- **Slicing's step 0** (probe, install, tell the person, log, map) and the sweep's rows being given owners: no
  planning session ran on this version.
- **"A guard names its test"** and **invariants**: text only. No project here has an `## Invariants` section.
- **Both reviewers' `tools check` and `Keep as a test:`.** Not run.
- **`check` on a project with import contracts.**
- **ruff's rules.** `check` runs ruff with whatever configuration ruff finds; on the kb clone, which has none of
  its own, it reported import-order lines. A project that has not chosen its lint rules may want to before its
  reviewers read this output.
- **A language other than Python**, beyond the one line that says none is known.
