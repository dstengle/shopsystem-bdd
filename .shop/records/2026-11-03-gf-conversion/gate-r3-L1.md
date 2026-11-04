---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-gate-r3-l1
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: draft
---

# Revision 3, layer 1 gate

The gate passed on `gf-conversion`. Its base was 7694e5aa (records: plan-r3). Every task branch was cut from main
by the harness and reset by its task to 7694e5aa before work, so all four merged without conflicts.

## Merged

| task | branch head | merge |
|---|---|---|
| S1 vocab cache | 184e12a0 | 46e5cb5c |
| S2 batched `git add` | d23ee4de | ca1eb7e9 |
| S3 the facts, `spec_context` | 8cfb66fd | 39bae621 |
| S4 `grammar/check.lp` | abe2ecb3 | a2e18df9 |

## Review

- **S1** matches the plan: `_by_print` keyed by `_fingerprint` is checked before any lexicon read; a miss reads the
  lexicon once and hands it to `sources(root, lex)` and `modules(lex)`. `_loaded` now caches the PGF, not the Vocab,
  so an edit that changes only the lexicon gets a new Vocab (Review Focus 4). The four tests test what the plan says,
  including the equal-size edit and the grammar touch. Known limit: an equal-size edit inside one mtime tick is not
  seen.
- **S2** matches the plan exactly; the mocked batch test and the real-repository test are both there.
- **S3** follows the plan's schema and its stated decisions. Extra facts beyond the design (`onot`, `ocond`,
  `rnone`, `named`) and `disj(Split,Base)` instead of `disj(R,K)` are listed in report-S3. `test_an_unknown_fun_is_
  refused_naming_it` and the every-fun coverage test are present (Review Focus 1). The module-map rows are in
  CLAUDE.md; the map condition of `test_revision_done` was checked inline (no module missing).
  - `spec_context._once` memoises `spec_lexicon.read` and `spec_grammar.sources` by patching the module globals
    during one read (16.6 s → 5.8 s on the live spec). It is not thread-safe; S5 should replace it with a proper
    per-read lexicon parameter or a parse cache when it owns `spec_grammar` callers. The remaining ~5 s is pgf
    parsing, so design §2's "model logic under 2 s" needs a cross-process cache of parse trees (S5/S8/S12).
  - `_define` stops at the first `GrammarError`, as today's `spec_solve.definitions` does; kept.
- **S4** matches the design's rules; its departures (soft `out/ok` per pair, the `can` filter, a uses/nouse index
  row, U recognised as ids `"U" <= R < "V"`, which fits `spec/universal.md`'s `[U1]`..) are reasoned in report-S4 and
  pinned by tests. `test_no_facts_no_atoms_no_warnings` covers Review Focus 3. check.lp does not read S3's `rnone`,
  `onot`, `ocond`; S5 decides whether they must reach the rules.

## Fixed by the gate

- S2 and S4 could not commit their reports (the harness refused the subagents' writes). The gate wrote
  `report-S2.md` and `report-S4.md` from their results and committed them with this record. No code was changed.

## Results

- `python3 scripts/tools size --limit 300`: exit 0.
- `timeout 600 python3 -m pytest -n 8 -q $SLOW --durations=8` (all eight old solver-driven files ignored):
  663 passed, 1 skipped, 125 subtests, in 19.0 s wall.
- Slowest: `test_e2e_codified.py::test_a_request_goes_through_the_requirements_system_into_delivery` at 11.2 s, over
  the 10 s ceiling. It is pre-existing (suite-cost.md measured 11.2 s) and S8 owns the ceiling. Next:
  `test_migrate_upgrade_codified.py` setup 3.1 s (was 13.2 s before S2).

## Left

- The e2e test above (S8).
- The thread-unsafe `_once` and the parse cost of `spec_context.load` (S5, S8, S12).
- check.lp's use of `rnone`/`onot`/`ocond`, and focusing only on brave-reported pairs (S5).
