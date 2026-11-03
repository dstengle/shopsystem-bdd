---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-gate-r2-L1
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: done
---

# The GF conversion, revision 2: the layer 1 gate

**Passed.** On `gf-conversion`, after layer 0 (`gate-r2-L0.md`, taken by this gate first because it had not run).

## Merges

`gfr/R1` (856058ea), `gfr/R2` (5e4f779c), `gfr/R3` (410a22f8), in plan order, `--no-ff`. No conflicts: the three
packages own disjoint files.

## Shared changes made by the gate

1. **No stub left.** `spec_typed.rows` lost its legacy fallback (relation entries read through `lex.ids()` when the
   lexicon had no `relations()`): it is now `list(lex.relations())`, R2's real rows. The tests' `StubLexicon` (a
   dataclass subclass whose `rows` field shadowed R2's `Lexicon.rows`, and whose `words()` patched in the row words)
   is gone: `stubbed()` builds a real `spec_lexicon.Lexicon` with extra `spec_relations.Row`s, so a stub row goes
   through R2's own expansion and ids exactly as a `## Relations` row would. R1's ask that `Lexicon.words()` include
   the row words, and that `parse --grammar` take `Def`, were already done by R2.
2. **The supervision corpus check.** `model parse --file grammar/corpus/supervision.txt` exited 1 for two reasons
   outside R1: the file opens with a `#` comment line, and its sentences are written for the fixture glossary. Test
   first (`test_parse_a_file_skips_its_comment_lines`), `model parse --file` now skips `#` lines of a plain file (as
   the corpus tests' own reader does) and keeps file line numbers. The gate's check is run as
   `python3 scripts/model --root tests/scripts/fixtures/glossary parse --file grammar/corpus/supervision.txt`: exit 0,
   10 trees.
3. `report-R1.md` and `report-R3.md` written from the packages' returned notes (the harness refused report files
   from the subagents). R2's report is its own, committed on its branch.

## The gate's checks

| Check | Result |
|---|---|
| layer tests (the 9 R1–R3 test files) | 131 passed |
| `tools size --limit 300` | exit 0 |
| full suite | 34 failed, 761 passed, 1 skipped, 22 errors |
| common check against `baseline-failures.txt` + `gate-r2-L1-allowed.txt` (FAILED and ERROR lines) | prints nothing |
| `model parse --file` supervision corpus (fixture root) | exit 0 |
| `unparsed.sh > unparsed-L1.txt`; `comm -13 unparsed-L0.txt unparsed-L1.txt` | both empty: every Behaviour and U line parses |
| the g13 line merged with `and` | one tree, `WhileWhen … (Shall … (AndVP …))` |
| `RefuseErr`/`CommitPush` in Req; `SCommits` in Steps | none; present |
| `features vocab --check --tests tests/scenarios` | exit 0 |
| `release_external`/`def _ground` in spec_engine | none |
| `tools check` | clean |
| `model lexicon --check` (live) | v_t7 22, v_t8 28, v_t9 84, v_t10 0 (R5 clears them) |
| `model check --json` (live) | new: v15l 145, v15m 361, v15n 217 (layer 4 clears them); v17 25, v10a 19, v_d1 9 as at 864f61e9 |

## The allowance (`gate-r2-L1-allowed.txt`, 56 ids)

- **54** whose traceback passes through `features_generate.py`, `spec_logic.py`, `spec_logic_vocab.py` or
  `spec_solve.py` (checked in the junit XML; `test_supervise_formulate::test_a_new_model_check_row…` is the
  `features generate` subprocess failing at `features_generate.py:192`, `resp[2]` on R1's list of conjuncts). One of
  them is a scenario, `test_supervision::test_an_applied_capabilityproposal_is_formulated_by_features_generate`,
  which runs `features generate`; every scenario that runs only the checked-in features is green.
  `test_e2e_codified` is among them.
- **2 outside the traceback rule**, admitted by this gate because they are R2's required reports doing their job:
  - `test_spec_guarantees.py::test_the_lexicon_has_no_problem`: the live lexicon's v_t7–v_t9. R5's accept
    (`0 problems`) clears it in layer 2.
  - `test_model_output.py::LanguageCommandsTest::test_lexicon_lists_terms_by_category`: the legacy fixture glossary
    (`tests/scripts/fixtures/glossary`) has v_t7–v_t9. The fixture cannot be rewritten before layer 3, because the
    old readers and the scenario suite read its `Means:` and relation entries. **Plan amendment:** the plan says the
    allowance is empty after layer 4, but no layer 4 package owns the fixture (R2 named R14). So either the layer 3
    or 4 gate rewrites the fixture's glossary as a shared change once R6 has replaced the old readers, or this one id
    stays in the allowance until R14. The layer 3 gate decides.

## Asks carried forward

- **R4/R6 (from R2):** a relation id is `r_<k1>_<word>_<k2>` of the row before expansion, shared by every expanded
  row; read `lex.relations()` -> (k1, word, k2, rid), not `lex.ids()`.
- **R4/R6 (from R3):** the engine interface in `report-R3.md` (pools as `pool_size/2` under `#program always`, the
  background defines `pool/2`; `sub/2` and `own/2` facts for the cone).
- **R6 (from R1):** delete the `<relation>_Given` funs in `features_vocab.modules` and the first rule of
  `spec_tree.guard` (it drops an `SAtom` over a `rel_*_Atom`) in the same change; without the rule the GivenR steps
  get two trees. `spec_tree.py` is not R6's file in layer 3, so the layer 3 gate makes that one-rule change with R6's
  merge, or R6 asks for it.
- **R14:** v_t7–v_t10 as `model check` rules once the fixture glossary is rewritten (from R2); the module-map rows
  of `spec_typed_def.py` (report-R1), `spec_engine.py` with `grammar/cone.lp` (report-R3), `spec_relations.py` and
  `spec_read_given.py` (report-R2).
- **Layer 2 gate:** `model logic` took **310 s** on the layer 0 code (`gate-r2-L0.md`); the 60 s limit is far off
  unless R4's cone and incremental horizon cut it, so the cache of design-r2 §6.4 is likely needed.
