---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-gate-l1
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# Layer 1 gate: merge of P1–P4

## What merged

`gfc/P1` (f37d0ad0), `gfc/P2` (4c63f2b2, d69a715c), `gfc/P3` (5 commits, last 4e4e934c) and `gfc/P4` (ce403243)
were merged into `gf-conversion` in that order with `--no-ff`. There were no conflicts. P2's two files outside its
list are accepted: `grammar/Core.gf`/`CoreEng.gf` hold the shared categories, and `scripts/spec_typed.py` generates
`Lex`/`Typed`.

## Shared changes made at the merge

- **One GF lookup (P1's ask).** `spec_grammar.gf_binary()` now delegates to `tools_grammar.gf_binary()`, and
  `GF_INSTALL` is gone from `spec_grammar`. Test first: `test_gf_binary_is_the_one_lookup_of_tools_grammar`.
- **The U wording made one (P2's and P3's asks).** All ten lines of P3's `spec/universal.md` were refused by the
  grammar against the live glossary. `spec/universal.md` now uses the corpus wording (`grammar/corpus/universal.txt`),
  which is closer to domain model §7 than P3's. Its Reading section was rewritten for it, and the summary in
  `docs/design-model/design-model.md` (the paragraph on universal conditions) follows it.
  - U9 is reworded in both files to "A delivery shall change no file of an initiative outside the delivery." The
    corpus wording needed `initiative directory` as a kind, but it is a resource in the live glossary, and two entries
    for one word give a legacy v_t2 row. The fixture glossary gains `of (relation file → initiative)` for it.
  - U7 stays narrowed to the worktree, as P2 had it (no NP coordination of two kinds).
- **The live glossary given the U lines' words** (`spec/index.md`, no `Not:` words added):
  - `tool` and `worker` are now kinds, not actors. Domain model §2 makes worker a kind, and an actor takes no
    article, so "a worker" and "a tool" could not parse.
  - New kinds: `file`, `command`, `reason`, `JSON object`, `resource`.
  - New relations: `needs (stage → resource)`, `with (stage → result)`, `in (file → worktree)`,
    `of (file → initiative)`, `outside (initiative → delivery)`.
  - New events: `refuse`, `write` (written), `change`, `give` (given). New condition: `free (condition of resource)`.
- **Reports P1, P3 and P4** were written from the packages' returned notes. The harness refused the subagents' own
  writes.
- **Baselines.**
  - `baseline-model-check.txt` was refreshed, as P4 asked. The only differences are P4's two relabelled headers (v3 (8)
    and v_s3 (2)) and the five `kind 'design'/'analysis'` file rows that P4 removed.
  - `baseline-failures.txt` is unchanged.

## Gate outcomes (SHOPSYSTEM_GF unset; P1's install used)

- `python3 scripts/tools install`: everything already installed, including `gf 3.12 already installed`. Exit 0.
- `spec_lexicon.problems(spec_lexicon.read('.'))` gives `[]`. PASS.
- Every U1–U10 of `spec/universal.md` parses, each to exactly one tree. PASS.
- The suite: 23 failed, 1186 passed, 1 skipped. `comm -13` against `baseline-failures.txt` prints nothing, and a set diff gives 0 new and 0 gone. PASS.
- Common checks: `tools size --limit 300` exits 0, and ruff is clean on the changed Python.
- Package accepts rerun on the merged branch:
  - P1: probe `--json` versions, `gf --version`, and an idempotent install.
  - P3: `restated.json`, both v5 greps, and 32 C rows.
  - P4: no `kind 'design'` row, the banned codes absent from `model.lp`, and v_d5 and w_stale_proposed listed.
  - All PASS. P2's three test files pass, 35 tests.

## Carried forward

- **P5:**
  - KINDS still lists cross-context-request and acceptance-scenario, and the LEGACY kind bridge is still in place.
  - Emit `generates(G,S)` for codified scenarios, not `has_sc`.
  - The facts the new rules read are listed in `report-P4.md`.
  - In `scripts/model`, the contract text still says v_d2 and version 3.
  - `model_parse.glossary_entry` still keys a word by term alone, so the lexicon can't give a word both a kind entry
    and a resource entry while the legacy reader runs.
- **P6:** a resource can't be a noun phrase in the grammar: "an initiative directory" doesn't parse, and only
  Holds/IsFree/Hold name resources. The new kind `resource`, with `needs` and `free`, carries U2. A line about one
  named resource's contents needs a kind of its own.
- **P7:** typed Steps templates (GivenK_A …) are still to be generated, beside `spec_typed`.
- **P8:** agents and skills still cite the old section names of `docs/capability-format.md`.
- **P11:** `spec/capabilities/design-model-check.md` still names v18 and v_d2, and r113's v16a cutoff.
- **P14:**
  - v16a's date cutoff goes at compaction.
  - The CLAUDE.md module-map rows for `tools_grammar.py`, `spec_lexicon.py`, `spec_typed.py`, `spec_grammar.py`,
    `spec_tree.py`, `spec_read.py`, `grammar/` and `tests/toolchain.py`, as the reports give them.
- **U7:** a core fun for "X or Y" of two kinds, if two capabilities need it, would let U7 name the stage directory
  again.
- **Flake:** `test_supervision ... run_side_by_side` failed once under `-n auto` (seen by P2). It wasn't seen in this
  run.
