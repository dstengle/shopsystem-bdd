---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-report-p2
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# Report: P2, requirement grammar, lexicon and parser

Branch `gfc/P2`, off `gf-conversion`. Built test first. The figures, the calls the builder made and the notes for
later packages are in `p2-grammar.md`, beside this report.

## What was built

- `grammar/Req.gf`, `ReqEng.gf`: the core requirement grammar, with all six EARS forms (Ubiq, When, While, Where,
  If-then, and five complex forms). It extends the generated `Typed`, which extends `Lex`, which extends a new
  hand-written `grammar/Core.gf`/`CoreEng.gf` (the shared categories).
- `scripts/spec_lexicon.py`: `read`, `entry`, `ident`, `Lexicon.ids()` (numbered collisions), `problems`
  (v_t4–v_t6), `Lexicon.words()`.
- `scripts/spec_typed.py` (new): the generated `Lex`/`Typed` modules and their English.
- `scripts/spec_grammar.py`: `load(root, grammar)` (sha-keyed cache, compile into `mkdtemp`, then `os.rename`; the
  loser of a race discards its copy), `parse` -> `Parse(tree, refusal, trees, before)`, `linearise`, `tokenise`,
  `normalise`, `gf_binary`, `hint`.
- `scripts/spec_tree.py`: `guard` (literals, repeated members, "it"/"its" antecedents, gaps, a code read as a second
  object), `normal`, `parts`, `logic_only`, `nodes`, `show`.
- `tests/toolchain.py`: `require()` fails the test (and never skips it), naming `python3 scripts/tools install`.
- `grammar/corpus/`: one file per capability (19 files, 8–10 sentences each), `universal.txt` (U1–U10) and
  `refused.txt`.
- `tests/scripts/fixtures/glossary/`: a typed glossary from DOM §1–§8, plus a capability with `## Terms`.

## Acceptance checks

All checks ran with `SHOPSYSTEM_GF=/home/vscode/shopsystem-bdd/.shop/scratch/spike-cnl/gfc`, because P1 is not
merged.

| check | outcome |
|---|---|
| `python3 -m pytest -q tests/scripts/test_spec_grammar.py tests/scripts/test_spec_lexicon.py tests/scripts/test_spec_tree.py` | 33 passed |
| corpus: at least 8 sentences for each of the 19 capabilities, all six forms, U1–U10, backticked lexicon words and code literals; each has one tree and linearises back to its normalised text | passes (182 lines) |
| `refused.txt` is all refused: free phrasing, a value in the wrong slot, repeated members, a dangling "it" (plus a plain code, two verbs, no full stop) | passes |
| `ident` on `work-item`, `` `work run` ``, `spec lock` | `k_work_item`, `a_work_run`, `s_spec_lock` |
| a second `load` runs no gf (`_run_gf` patched to fail) | passes |
| two processes loading one new glossary both get a PGF, and one cache directory is left with no `.tmp-*` | passes |
| `p2-grammar.md` records the cold compile time (0.16–0.18 s) and the lines with more than one tree before the guard (166 of 182) | done |
| `python3 scripts/tools size --limit 300` | exit 0 (the largest new file, `spec_grammar.py`, has 229 lines) |
| full suite against `baseline-failures.txt` | nothing new on the second run. The first run had one extra failure, `test_supervision.py::...checked_without_the_paths_of_another_initiative_run_side_by_side`. It passes alone and passed on the rerun, so it is a timing flake under `-n auto` and does not come from P2 |
| `ruff check` on the new files | clean |

## Deviations from the plan

- Two new files are outside P2's owned list. `grammar/Core.gf` with `CoreEng.gf` holds the categories, because
  `Typed`'s funs need the core categories and `Typed` sits below `Req`. `scripts/spec_typed.py` keeps
  `spec_grammar.py` under 300 lines.
- U3, U5, U7, U9 and U10 are reworded to parse, and U7 is narrowed (the stage directory is dropped).
  `p2-grammar.md` lists each change for P3.
- `Parse` has a fourth field, `before` (the trees before the guard), and `refusal` is also set for an ambiguous
  line (`ambiguous: n trees`).
- The typed Steps funs are not generated. `load(root, "Steps")` works once P7 adds `grammar/Steps*.gf`.
