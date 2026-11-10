# Grammar 4 complete (b240): addendum, the construct catalogue and the spec pack (phase 12.5)

The person put the construct catalogue in scope (quote-23, b240's notes), which the plan had left out ("Not in
scope", audit construct 9, reopening b124). This addendum adds one phase between 12 and 13 and changes what phases
13-23 do with a line that rests on a coined construct word. Everything else in `plan.md` holds: the branch, the
gate, the commit rules, the stops.

## Phase 12.5: the construct catalogue and the spec pack

**Goal:** a requirement line about the language names a construct by a code of a generated, tested catalogue, as a
line about a check names a rule by its code (`grammar/rules.md`, b123), never by a coined adjective.

- **The catalogue**, `grammar/constructs.md`, written by `model constructs --write` and checked by `model constructs
  --check` (as `model rules --write` and `--check`); do not edit. One entry a construct: its code (kebab-case, e.g.
  `rc-object`, `not-response`, `oblique-role`), its label, its form, the grammar functions it is made of, an
  example line, and the example's reading (the logical form `model parse --form` prints), and the lines citing the
  code.
- **Generated from the grammar:** the examples are parsed in one context that holds every function family grammar 4
  generates, `grammar/corpus/constructs/spec/index.md` (the codified-2 fixture's words, the time pack, a moment of a
  stage). Generation refuses, naming each: a function of that context's compiled grammar that no construct and no
  listed word or glue family covers; an example that does not parse to one tree, that a reading rule refuses, that
  does not linearise back word for word, or whose tree does not use its construct. So a new function family of the
  grammar cannot land without its catalogue entry.
- **Part of the corpus:** `tests/scripts/test_model_constructs.py` reads every entry's example and reading from the
  catalogue and fails when grammar 4 reads the example otherwise (as `test_spec_lf_read.py` reads language.md), and
  fails when the catalogue is not current.
- **The spec pack**, `grammar/packs/spec.md` (packs as b132 built them): `requirement`, `construct`, `rule`, `use`
  (Frame: requirement uses construct) and `violate` (Frame: thing violates rule). This repository imports it
  (`imports: [cli, spec]`); its own entries of the same words are marked `Redefines: spec.`
- Modules: `scripts/model_constructs.py` (generate, check, render) and `scripts/model_constructs_table.py` (the
  entries), each a row in CLAUDE.md's module map; `grammar/`'s row names the catalogue and the pack.
- Tests first: the catalogue's test, the pack's test and `model constructs --check` fail before the build.
- No requirement line is added in this phase.

## Phases 13-23: a line that rests on a coined construct word

Where a reworded line rests on a coined construct word (the audit's construct 9, about 90 lines: relative,
refraining, oblique, reframing, screening, embedding ...), it is reworded to name the construct by its code with the
spec pack's words: "a requirement that uses `rc-object`". A rule finding keeps naming its rule ("a term that
violates `v_t11`"). Phase 26's limit #1 lists only the coined words left after that. The rule labels in the
controlled language (b124's level 2) stay out of scope.
