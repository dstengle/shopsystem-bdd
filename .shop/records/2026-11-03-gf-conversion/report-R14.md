---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-report-r14
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: done
---

# R14: legacy removed, map written, "Done means" measured (revision 2, layer 5)

Commits 93eb900c (code) and d388ca5f (`gate-r2-done.md`) on `gfr/R14`, off 43b78050. The package could not write
this file (the harness refuses report files from a subagent); the layer 5 gate wrote it from the package's notes.

## What changed

- `Term.means` is deleted. A relation entry of any word is now a v_t8 problem and gives no row:
  `spec_relations.sources` and the legacy reading are gone, and so is `features_vocab`'s relation-entry owner
  branch. `spec_tree` had no shim left.
- `SCommits` is deleted from `Steps.gf`/`StepsEng.gf` and from `features_vocab`'s maps. The `ThenCommits` handler
  is deleted from `supervision_handlers_what.py`, together with its tracked/pushed/COMMITTED helpers.
- CLAUDE.md map: new rows for features_vocab_gf, spec_relations, spec_typed_def, spec_read_given, spec_engine
  (with cone.lp), spec_trace, spec_trace_steps, supervision_handlers_more and migration_tools_handlers_conditions.
  spec_logic's row now covers spec_logic_np, and 8 stale rows are rewritten.
- Docs: grammar.md's v_s rules now match model.lp (the v_s2/v_s3 drift is fixed). The v_t8 wording is updated in
  grammar.md, capability-format.md, design-model.md, the checking-spec-consistency skill and `scripts/model`'s help.
- New test file `tests/scripts/test_revision_done.py` covers the design-r2 §2 measurements and R14's deletions. It
  was written first: 4 tests went red, then green.
- `gate-r2-done.md` has each measurement with its command, exit code and output, plus call 16 for the person.

## Checks (on gfr/R14)

Accepts 1 to 9 pass. Lexicon: 366 terms, 0 problems. Full suite: 864 passed, 1 skipped. `model logic`: 32.5 s,
no findings. Accept 5's test command ran from test_spec_trace.py (see below).

## Asks

1. Plan accept 5 names `test_features_generate.py -k 'byte_stable or related_while'`, but R6 put those tests in
   `tests/scripts/test_spec_trace.py`. (The layer 5 gate amended the plan.)
2. Files changed outside R14's ownership: `scripts/spec_relations.py` (legacy `sources()` deleted, v_t8 widened),
   `tests/scripts/test_spec_relations.py`, `tests/scripts/test_spec_lexicon.py`, the docs listed above and
   `scripts/model`'s help text. Layer 5 has only R14, so nothing conflicts.
3. Handed back as follow-ups. None of them fails a check, and all are listed in `gate-r2-done.md`:
   - the shall-not-only group gets no Then;
   - background.lp's `#minimize`;
   - naming with `.lower()`;
   - J1;
   - AndVP binding;
   - state-0 writes;
   - the GivenK_A negation;
   - g53 minimisation;
   - the grammar wishes (Where+While+When, an NP list for Do, an NP-or for U7, U10's tool list);
   - the unplaced "deprecated scenario" line.

   R14 added no grammar fun, because every line handed back already parses after rewording.
