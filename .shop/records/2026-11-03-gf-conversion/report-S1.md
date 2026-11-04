---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-report-s1
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: final
---

# Report S1: the step vocabulary loaded once per state of its files

## What changed

- `scripts/features_vocab.py`: `load(root)` looks its `_fingerprint(root)` up in the module-level `_by_print`
  before it reads anything. On a hit it returns the same `Vocab`. On a miss it reads the lexicon once, passes it
  to `spec_grammar.sources(root, lex)` and to `modules(lex)`, and builds a new `Vocab`.
- `_fingerprint(root)` is the resolved root, then `(relative path, st_mtime_ns, st_size)` for every file under
  `root/spec` (sorted `rglob`, files only) and for every `spec_grammar.GRAMMARS.glob("*.gf")`.
- `scripts/spec_grammar.py`: `sources(root, lex=None)` reads the lexicon only when no `lex` is passed.
- `tests/scripts/test_features_vocab.py`: four new tests. `test_a_second_load_reads_nothing`,
  `test_a_cold_load_reads_the_lexicon_once`, `test_an_edit_of_equal_size_reloads` and `test_a_grammar_edit_reloads`.

## Calls made

- **`_loaded` keeps the loaded PGF, keyed by sha, not the `Vocab`.** The plan says `load` "keeps the sha-keyed
  `_loaded`". If `_loaded` held the `Vocab`, an edit that changes the lexicon but not the GF sources would get the
  old `Vocab` back, with the old lexicon in it. A changed definition sentence is such an edit. This is the case
  `test_an_edit_of_equal_size_reloads` pins: its edit of "a unit of delivery" changes no GF source. So a
  fingerprint miss always builds a new `Vocab` over the current lexicon, and it reuses the compiled and loaded
  grammar when the sources are unchanged.
- **The new tests use their own fixture, `spec_repo`.** It is a plain `tmp_path` copy of
  `fixtures/generate/repo`. The file's existing `repo` fixture runs the old `features generate`, and these tests
  do not need that.

## Test runs

- `pytest -n 4 tests/scripts/test_features_vocab.py -k "load or reload"` before the change: 4 failed (expected).
- `pytest -n 4 tests/scripts/test_features_vocab.py tests/scripts/test_spec_grammar.py`: 48 passed, 4.5 s wall.
- `pytest tests/scenarios --ignore=tests/scenarios/test_supervision.py --durations=5` (xdist, the repository's
  default worker count):
  - after the change: 203 passed, **4.4 s wall, 66 s CPU user**;
  - at `gf-conversion` head on the same machine just before: 203 passed, 7.1 s wall, 151 s CPU user.

  suite-cost measured 26.6 s and expected 19.7 s. Those were on a busier run, so the ratio is the figure to
  compare: CPU roughly halves.
- `python3 scripts/tools size --limit 300`: exit 0. `ruff check` on the three files: clean.

## Left open

- The fingerprint uses mtime_ns and size, as the plan says. An edit of equal size that lands on the same
  timestamp tick as the stat before it would be missed. Kernels with multigrain timestamps make that unlikely,
  and the test passes here.
