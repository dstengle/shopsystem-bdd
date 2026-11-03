---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-report-p3
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# Report: P3, the spec format, typed glossary, universal conditions and design model v5 docs

Branch `gfc/P3` (5 commits on `gf-conversion`). Written by the layer 1 merge from the package's returned notes: the
harness refused the package's own write of this file.

## What was built

- `scripts/spec_read.py` (230 lines): `capability(path)` returns `Capability(path, name, frontmatter, groups,
  dropped, retired, problems)`. Each `Group` is `(id, title, restates[(cap, n)], given[(line, Block|None)],
  requirements[Requirement(id, text, line_no)], line_no)`. `Block(kind, lines)` is a docstring or a table (`.rows`).
  Also `codified(path)`, `universal(root)` giving `Universal(id, text, line_no)`, `read_universal(root)` and
  `restated(root)`. Nothing raises; problems read `<line>: <what>`.
- `model_parse.glossary_entry` accepts a `(category ...)` after the term, drops backticks and refuses a malformed
  category. A word with entries for several kinds is defined once: the entry with a definition sentence keeps the
  bare key; an attribute or condition entry that opens with `Values:` or `Means:` is keyed `<term> of <kind>`; a
  relation is always keyed `<term> of K1 to K2`. Without this, v_t2 or unresolved rows appeared, because old
  proposals name term/status, term/outcome, term/line-outcome, term/failed and term/fault.
- `spec/index.md`: the glossary as 133 typed entries (10 actors, 60 kinds, 12 attributes, 9 conditions, 25
  relations, 8 events, 9 resources), marker `language: codified-1`. `failed` is kept as a condition beside the value;
  `fault` is kept as a kind for the 0.29 lines (P12 may retire it); `run` is dropped (the core `Runs` would make lines
  ambiguous); `session` stays a kind. No new `Not:` words (they would hit unconverted lines).
- `spec/universal.md` with U1-U10, one `shall` each; `spec/restated.json` (581 keys, `<cap>#r<n>`, `{text, line}`,
  frozen from 96818f71).
- `docs/design-model/` rewritten as v5: `design-model.md` §10.1 holds C1-C32 and §10.2 the rule codes, `grammar.md`
  is v5, `how-we-got-here.md` gains a v4→v5 section, README says design model v5. `docs/capability-format.md`
  rewritten.

## Checks

- `pytest tests/scripts/test_spec_read.py tests/scripts/test_model_glossary.py`: 23 passed.
- `restated.json` assert, both `design model v5` greps, 32 `| C<n>` rows: PASS.
- `model check` against `baseline-model-check.txt`: no new rows, none gone. `tools size --limit 300` exits 0
  (`model_parse.py` 287 lines). The suite: 23 failed, all in the baseline. ruff clean.

## Asks (handled at the layer 1 merge, see gate-L1.md)

- Make the U wording one with P2's corpus.
- Check the lexicon gate on the new glossary.
- Agents and skills still cite old section names of `docs/capability-format.md` ('Requirement ids', 'Writing the
  behaviour section', 'Glossary'); P8 should point them at the new sections.
- Module-map row: `scripts/spec_read.py` | the codified spec files read: a capability's groups, requirements,
  `given` blocks, `Restates:` and `## Dropped`; `spec/universal.md`; `spec/restated.json`; the per-file marker
  `language: codified-1`.
