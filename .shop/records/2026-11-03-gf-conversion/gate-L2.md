---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-gate-l2
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# Layer 2 gate: merge of P5–P7

## What merged

`gfc/P5` (9eda895f), `gfc/P6` (db653147) and `gfc/P7` (ad33dafe) were merged into `gf-conversion` in plan order with
`--no-ff`. The three packages touched disjoint files, so there were no conflicts. P6's file outside its list,
`scripts/spec_logic_vocab.py`, is accepted: `spec_logic.py` would otherwise be 322 lines, and P2's `spec_typed.py` is
the precedent.

## Shared changes made at the merge

- **v_p3 reads given lines with the typed Steps grammar (P7's ask).** `SpecReading.given` in `scripts/model_spec.py`
  compiled only the core `Steps` grammar, which has no Given templates, so every given line would have been
  `given_unparsed`. It now calls `features_vocab.parse(features_vocab.load(root), "given", line)` and writes
  `given_unparsed(G, Line)` on a `StepError`. Test first:
  `test_model_spec.py::FactsTest::test_a_given_line_is_read_by_the_typed_steps_grammar` (red: it flagged the valid
  `an initiative i1 that is \`proposed\`` too; green after). P7's fixture repo gives no `given_unparsed`.
- **Reports P5, P6 and P7** were written from the packages' returned notes, because the harness refused the packages'
  own writes.
- No baseline was changed.

## Gate outcomes (SHOPSYSTEM_GF unset; P1's install used)

- `model --root tests/scripts/fixtures/logic/cluster logic --json`: exactly L1 [g5, r5, r2, U2], L2 [r3, r4], L3 [r9],
  L4 [g10], exit 1. These are the findings P6's test asserts. PASS.
- `model --root tests/scripts/fixtures/generate/broken check 2>&1 | grep -q '^v_p1 '`: matched
  (`v_p1  a requirement does not parse  (1)`). PASS.
- `features generate --check` on the live repo: exit 0, with 8 `skipped <c>: not codified` lines, one for each service
  capability. The plan says 10, but there are 8 service capabilities. PASS.
- Suite: 23 failed, 1285 passed, 1 skipped. `comm -13` against `baseline-failures.txt` prints nothing, and nothing is
  gone. PASS.
- Common checks: `tools size --limit 300` exits 0 (the largest files are `features_vocab.py` at 299 and
  `scripts/features` at 292). `tools check` is clean, and ruff is clean on the changed Python.
- Package accepts rerun on the merged branch:
  - P5: `model parse` exits 0 on the `proposed` line and 1 naming `` `drafted` `` on the other. `lexicon --check`
    exits 0 (148 terms, 0 problems). `restates spec-migration` exits 1, naming `spec-migration#r1`. P3's
    no-new-rows check is empty.
  - The P5, P6 and P7 test files all pass on the merged branch.
  - All PASS.

## Carried forward

- **P8:**
  - `## Terms` in a drafted extra file are not added to the lexicon by `spec_solve` (P6's note).
  - `model logic` and `spec_solve.run(extra=…)` are ready for the integrate check.
  - Agents and skills still cite the old capability-format section names (from L1).
- **P10 (and every converting package):**
  - Generation refuses `shall not` with DoTo/Exit/Commit, Hold with an actor subject outside logic-only groups, and
    condition atoms whose Means is not "its <attr> is [not] …" (P7 call 6). A capability needing one of these needs
    a Steps fun first, made by the orchestrator between layers.
  - `conftest.py`, `vocab.py` and `world_*.py` are frozen from now on.
- **P11:** `spec/capabilities/design-model-check.md` still names v18, v_d2 and r113's v16a cutoff (from L1).
- **P14:**
  - Delete `model_legacy.py`; `read_glossary_legacy`, `read_legacy_behaviour` and `legacy_scenario` in
    `model_facts`; the `ears` branch of `workqueue_lines.check`; and v_e1/v_e2 and the legacy has_sc clauses (v_s2,
    v_s3, v15f) in `model.lp`.
  - `model_work.py` resolves `<cap>#r<n>@0.29` only through `Model.nodes`. When the old references are migrated, it
    may want to see `@0.29` explicitly.
  - Optionally, make `spec_grammar`'s `_compile`, `_cache`, `_tree`, `_expr` and `_position` public, since
    `features_vocab` uses them.
  - Drop v16a's date cutoff (from L1).
  - Write the module-map rows of L1 (gate-L1.md) and of L2 (report-P5.md, report-P6.md, report-P7.md).
- **Plan text:** P7's accept says "10 today" service capabilities, but there are 8.
- **U7:** still leaves out the stage directory (from L1).
