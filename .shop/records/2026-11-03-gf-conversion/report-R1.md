---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-report-r1
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: done
---

# R1: the grammar: coordination, prepositions, definitions (revision 2, layer 1)

Commit 856058ea on `gfr/R1`, off 864f61e9. The package could not write this file (the harness refuses report files
from a subagent); the layer 1 gate wrote it from the package's returned notes.

## Built

- Req/ReqEng: the `VPs`/`VPor`/`Resps` categories. `Shall : Subj -> VPs`, `ShallNot : Subj -> VPor`, `OneVP`/`AndVP`,
  `OneVPor`/`OrVP`, `OneResp`/`AndResp` ("R1, and R2"). The EARS forms take `Resps`. `CondOr` added. `RefuseErr` and
  `CommitPush` deleted. Steps.gf is unchanged and `SCommits` stays.
- spec_typed: for each row (k1, word, k2, id) the modifier fun `rel_<k1>_<word>_<k2>` and a clause fun of the same
  name with `_Atom`.
- spec_typed_def.py (new): Def.gf/DefEng.gf with one `c_<cond>_<kind>_Def : Cond -> Def` per condition and kind.
  `spec_grammar.parse(grammar="Def")` refuses a tree holding any `_It` with "a definition names its subject as the
  <kind>".
- spec_tree: `parts()["resp"]` is a list of (polarity "Shall"|"ShallNot", subject, VP). `normal()` sorts `CondOr`
  lists and keeps the order of a list mixing and/or (the old code dropped the tail of such a list). The repeat guard
  now covers repeated VPs.
- grammar/corpus/core.txt (new): each line with its expected tree, generated numbers left out. Its `# row:` lines are
  stub rows; its `# guard:` lines mark the g13 line and q47 line 4, which are refused as "ambiguous: 2 trees" once
  the (work-item|initiative, with, result) row is added.
- refused.txt: the old "discard and start" line now parses, so it is replaced by 3 refusals that involve verb
  phrases.

## Checks (on gfr/R1 at 856058ea)

- The 4 R1 test files: 51 passed.
- `model parse` on the g13 line gives one tree, response `OneResp(Shall … (AndVP (t_status_6_Set …) (OneVP (Do
  e_ask …))))`.
- The `RefuseErr`/`CommitPush` grep finds nothing; the `SCommits` grep finds it.
- `features vocab --check --tests tests/scenarios` exits 0.
- unparsed.sh prints nothing on gf-conversion and on R1 (L0 baseline built from a `git archive` of gf-conversion).
- All 6 q47 lines parse. `tools size --limit 300` exits 0.
- Full suite: 32 failed and 22 errors, every traceback through features_generate / spec_logic / spec_logic_vocab /
  spec_solve (checked in the junit XML).

## Calls made under the delegation

- core.txt is parsed in the live glossary, because §4.2 needs whoever adds a conflicting row to see the refusal.
- Tests stood in for R2 with a stub lexicon (`relations()` only; supertype not needed in R1). The layer 1 gate
  replaced it with the real Lexicon plus `## Relations` rows.
- A relation clause between two instances is left to `<rel>_Given` until R6; otherwise every GivenR step would have
  two trees.
- `push` was not moved by R1 (layer 0 did it); spec/ was not touched.

## Asks

- R6: delete the `<relation>_Given` funs in `features_vocab.modules`, and the first rule of `spec_tree.guard` (it drops
  an `SAtom` over a `rel_*_Atom`), in the same change. Without that rule the GivenR steps get two trees.
- R2: `Def` in `model parse --grammar`; `Lexicon.words()` to include the words of `## Relations` rows (both done by R2).
- Layer 1 gate: the supervision corpus check and the dead legacy fallback in `spec_typed.rows` (both done, see
  gate-r2-L1.md).

## Module map row

| `scripts/spec_typed_def.py` | the generated Def grammar: a condition defined in the controlled language, and the refusal of a definition that says "it" (design-r2 §4.3) |
