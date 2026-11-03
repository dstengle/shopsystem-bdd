---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-gate-r2-l4
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# Revision 2, layer 4 gate

The gate passed on `gf-conversion`. Its base was 07a79699, the layer 3 gate.

## Merged

gfr/R8 (4bf5b2f6), R9 (d630b961), R10 (7bf53709), R11 (0792f0a2), R12 (402da178) and R13 (1ece0150) were merged
in plan order, each with `--no-ff`. There were no conflicts.

## Shared changes and fixes

1. **R8 ask 1 / R12's commit handler** (`tests/scenarios/work_queue_handlers.py`): `ThenDoes commit` now reads
   every file committed since the When (`git diff --name-only <head> HEAD`), not only HEAD's.
2. **R8 ask 2** (`tests/scripts/test_spec_trace.py`): the `edited` fixture is now `copy_spec` only. R8 had already
   made its edits in the live spec. The ids were renamed through ids-supervision.tsv: g13 to g12, g25 to g24. The
   unused `G13` and `import re` were removed.
3. **R9 ask 1** (`work_queue_world.matches`): `(a|the) decisions index( <name>)?` matches `spec/decisions/index.md`.
4. **After the merge, `work_queue_world.matches`** answered false for `the <kind> <name>` when the kind was not a
   work-queue kind, even where supervision's `committed_names` had written the instance into the nodes. That broke
   5 supervision scenarios: commits of a stage, draft, measurement and feature. Now any `the … <name>` that
   has a node is compared with that node's file, as it was at 07a79699.
5. **R9/R12 key clash**: `GivenK_C observation` had two handlers, so `test_bound` failed. R9's handler did nothing.
   R12's handler records the observation, and work_queue_world reads that record. R12's handler is kept and R9's is
   deleted.
6. **role-boundaries g5 did not parse after the merge** (unparsed.sh printed it). The line has twelve backticked
   tokens, and GF's String literal slot read each one in 2 or 3 ways, giving 20 736 trees. The only good tree was
   number 20 115, past `LIMIT = 2000`. In R13's worktree it happened to come earlier, so the line parsed there.
   - Fix, written test first: `spec_grammar._literal` is a String callback for pgf's parse, so a literal slot no
     longer reads a lexicon word. The guard refused those trees anyway ("the code … is a lexicon word").
   - The line now gives 256 raw trees and parses in 0.05 s.
   - New test: `test_a_literal_slot_does_not_read_a_lexicon_word_so_long_coordinations_are_read_whole`. It failed
     with `before == 2000` and now passes. `test_a_backticked_lexicon_word_parses_only_as_the_word` now expects
     `before == 1`.
   - This changes `scripts/`, which is frozen for the layer's packages. It is a gate change between layers, as at
     layer 2.
7. **features/requests.feature regenerated**: R8's spec changed the cone, which adds `Given a request q1 that is
   `open`` to g1. Its 26 scenarios pass.
8. **model check `file:` rows**: 11 of this conversion's own records broke the record rules:
   - `kind: report` is not a record kind, so it is now `analysis`;
   - ids with capitals (`…-gate-r2-L0`, `…-report-R4`) are now lowercased.
   With those fixed, no `file:` or `unresolved:` row is outside `baseline-model-check.txt`.
9. **The allowance**: `gate-r2-L1-allowed.txt` is now empty.

## Checks

- Step 2 (terms that two packages defined): none. The same word appears in more than one capability only as a
  condition of different kinds (ahead, uncodified, uncommitted, dangling, unparsed, unmigrated) or in different
  categories (note: an event in delivery, a kind in work-queue). Lexicon: 366 terms, 0 problems. No Relations row
  is repeated, and `repository` is defined only in migration-tools. Nothing was moved to spec/index.md.
- Step 3, the references (check point 19): hits outside the excluded paths are only in
  - spec/restated.json (0.29 ids);
  - supervision_build.py, test_e2e_codified.py, test_supervise_formulate.py, test_supervise_outputs.py and
    test_features_generate.py (specs each test writes);
  - test_spec_read.py (0.29 ids, plus restated.json written by the test);
  - test_spec_solve.py (the logic fixture);
  - test_spec_trace.py: live supervision g2, g12 and g24, rewritten through ids-supervision.tsv, plus trials r98 and
    r99, lines the test itself adds.
- Step 4:
  - `model lexicon --check`: 366 terms, 0 problems.
  - `model restates`: 581 ids, 513 restated, 68 dropped, 0 missing.
  - `features generate --check`: exit 0.
  - `unparsed.sh`: prints nothing.
  - `model check`: no `file:` or `unresolved:` row outside the baseline, and no v15k, v15l, v15m or v15n row
    anywhere.
  - `model logic` (the whole spec, every U on): exit 0 with no findings, 33.4 s. This was R13's failing accept; it
    passes now that R8 has cleared supervision's L1s.
  - Full suite: 854 passed, 1 skipped, 0 failed. The comm against the baseline and the empty allowance prints
    nothing. test_e2e_codified passes.
- Per capability: r count equals g count in every capability file.
- Common checks: `tools size --limit 300` exits 0, `features vocab --check` (every step has one handler), and
  `tools check` is clean.

## Carried to R14

- From the package notes, the generator and engine:
  - A group whose only response is `shall not` gets no Then (R8, R9, R10, R11). Packages worked around it by adding
    a positive conjunct.
  - `background.lp`'s `#minimize` counts derived conditions (R9).
  - `spec_trace_steps` naming needs `.lower()` (R9, R11). The JSON object J1 is refused by Steps, so --json groups
    were dropped or reworded (R9, R12).
  - An AndVP's later `the <kind>` does not bind to a restricted antecedent (R12 ask 1).
  - State 0 holds what the command writes (R12 ask 5; see requests g1 above).
  - The negated GivenK_A value in world_nodes (R12 ask 3).
  - R8's minimisation oddities in g53 and others.
- Grammar wishes:
  - Where+While+When (R11);
  - an NP list for `Do` (R11);
  - an NP-or for U7 (R13);
  - R13's question whether U10 allows the tool list.
- Not placed: r5-moved-content's formulation line "a deprecated scenario formulates no requirement" (R13). It
  belongs to design-model-check or model.lp.
- Module-map rows for CLAUDE.md:
  - `tests/scenarios/supervision_handlers_more.py`: supervision Thens on merges, logs, takes, pushes, drafts (R8).
  - `tests/scenarios/migration_tools_handlers_conditions.py`: migration-tools' condition Givens, a repository's
    primitive conditions checked against the scenario's example data, and the untracked file built (R10).
  - R9, R11, R12 and R13 add no module.
- report-R8.md to report-R13.md were not written. Each package's Write was refused ('Subagents should return findings
  as text'). Their substance is in this record and in the package notes the orchestrator holds.
