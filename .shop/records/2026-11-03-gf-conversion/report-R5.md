---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-report-R5
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: done
---

# R5: the glossary rewritten (revision 2, layer 2)

Commit d71aa6c3 on `gfr/R5`, off 65dbc79a. The package could not write this file (the harness refuses report files
from a subagent); the layer 2 gate wrote it from the package's returned notes. Kind `design`, as the package asked:
kind `report` is a file problem in `model check`.

## What changed

- `spec/index.md`: the Glossary, and a new `## Relations` with 24 rows.
- The `## Terms` of 11 capabilities, and a new `## Relations` in 7 of them.
- New `r5-moved-content.md`: §1 the cut content by capability, verbatim, for layer 4 to turn into requirements; §2
  (generated) all 170 changed or removed entries with old and new text.
- The 22 entries over one sentence, and the glosses that held rules, cut to one sentence. Supervision's worker,
  round and review briefs, tool list, output, change list and log are one-sentence glosses.
- All 88 `Means:` fields gone: 11 became `Def` sentences, 77 primitive glosses. A new primitive condition `unfixed`
  (initiative) lets `complete` be a `Def`.
- New rows: supervision's (result, gives, question/output/change list). `Kind of: node` on initiative, proposal and
  work-item; `Kind of: proposal` on capability-proposal and glossary-proposal. Supervision's 4 local `for` entries
  that this covers were deleted.
- No Behaviour line, code or test changed; no new module.

## Point 3 counts (check point 16)

- Before: 61 relation entries (28 preposition, 33 verb), no rows.
- After: 49 rows plus 11 kept entries, 72 relations after expansion.
- Words with several rows: on 7 (4 once the ask below lands), of 6, in 4, for 3 (was 7), gives 3, changes 3, adds 2,
  removes 2, broken by 2, outside 2.

## Checks

| Check | Result |
|---|---|
| `model lexicon --check` | **9 problems** (was 134; plan asks 0): 6 v_t8, 3 v_t10, all on six preposition entries the checked-in features still need |
| `grep -rn 'Means:' spec/` | nothing |
| q47 lines, `model parse --file` | exit 0 |
| `unparsed.sh \| comm -13 unparsed-L1.txt -` | nothing |
| the 11 `Def` sentences, `--grammar Def` | all parse |
| `tools size --limit 300` | exit 0 |
| full suite | the base's 56 failures; common check prints nothing |
| scenario suite | 299 passed, 1 failed (the allowed formulate scenario) |
| `model check` against the base | 4 new v_t2 rows (closed, open, termless, unparsed) |

## Asks

1. **R6 or the layer 3 gate:** build the relation Given step funs and vocab rows in `features_vocab` from
   `spec_relations.sources(lex)` (the rows) instead of `lex.of('relation')`; handlers are keyed by (GivenR, word), so
   they keep working. Then delete the six kept preposition entries: index `for` (stage → node), `with` (stage →
   result), `on` (question → node); supervision `on` (question → work-item / glossary-proposal /
   capability-proposal). Turn the five verb entries the features use (fulfils, blocked by, adds, proposed in, kept
   in) into rows. The lexicon then has 0 problems. A trial move of index `for` to a row failed 38 supervision
   scenarios with StepDefinitionNotFoundError.
2. **R14 or the layer 2 gate:** `model_spec.term_word` keyed a condition `<term> of <kind>` only when its entry had
   no gloss; every condition now has one, so same-named conditions shared one term id (the 4 v_t2). Done by the
   layer 2 gate.
3. **R4:** `Lexicon.definition(term)` looked a condition up by name only, so open (work-item) got the open
   (initiative) sentence. Done by the layer 2 gate.
