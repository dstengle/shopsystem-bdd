---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-gate-r2-done
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# Revision 2: "Done means", measured (R14)

Measured on `gfr/R14` at 93eb900c, which is off the layer 4 gate (43b78050). Each measurement lists its command,
its exit code and its output. `tests/scripts/test_revision_done.py` runs points 1, 2, 3, 6 and 7 as named tests,
along with what R14 deletes, and every one of them passes.

| # | the person's point | command | exit | output |
|---|---|---|---|---|
| 1 | no non-example given block | `model check --json`, rows with code v15m | 1 (the baseline's v10a/v17/v_d1 rows) | no v15m row; `test_no_given_line_that_is_not_example_data` passes |
| 2 | no repeated trigger | `model check --json`, rows with code v15k, v15l or v15n | 1 (as above) | none; `test_no_two_statements_share_a_trigger_and_a_condition` passes |
| 3 | terms | `model lexicon --check` | 0 | `366 terms, 0 problems` |
| 3 | | `grep -rn 'Means:' spec/` | 1 | nothing |
| 4 | one translation, conflicts found | `pytest` on `test_statement_is_a_tel_constraint`, `test_stops_at_horizon_1`, `test_chained_stops_at_horizon_2`, `test_engine_uses_imain` and `test_seeded_conflict` | 0 | `5 passed in 37.02s` |
| 4 | | `grep -rn 'HORIZON = ' scripts/` | 1 | nothing |
| 5 | Gherkin from traces, byte-stable | `PYTHONHASHSEED=1 features generate --check`, then the same with `=2` | 0, 0 | nothing |
| 5 | | `git diff --exit-code features/` | 0 | nothing |
| 5 | | `pytest tests/scripts/test_spec_trace.py -k 'byte_stable or related_while'` | 0 | `2 passed in 156.40s` |
| 6 | new requests go through it | `pytest tests/scripts/test_e2e_codified.py` | 0 | `1 passed` |
| 6 | | q47's six lines through `model parse --file` | 0 | six trees, lines 1 to 6 |
| 7 | suite and size | `pytest -q -p no:randomly -n auto` | 0 | `864 passed, 1 skipped, 125 subtests passed` (no failure, so none outside baseline-failures.txt) |
| 7 | | `tools size --limit 300` | 0 | nothing |
| 7 | | the P14 map-row loop over `scripts/*.py` | 0 | nothing (it named 7 modules before R14) |
| 7 | | `features vocab --check --tests tests/scenarios`; `grep -n SCommits grammar/*.gf scripts/*.py` | 0; 1 | `every step has one handler`; nothing |
| 8 | | `time model logic` | 0 | `no findings`, 32.5 s (no L4 warnings either) |
| 9 | | `model check`: `file:` and `unresolved:` rows compared with `comm -13` against baseline-model-check.txt | 1 | the comm output is empty. All 29 unresolved rows are in the baseline, so no abandoned-initiative row needed listing |

The plan's accept 5 names `tests/scripts/test_features_generate.py -k 'byte_stable or related_while'`. R6 put those
two tests (`test_byte_stable` and `test_related_while_enters`) in `tests/scripts/test_spec_trace.py`, so the
command above runs them from that file. Run against test_features_generate.py, the same `-k` selects nothing.

## Open point for the person: why `## Relations` rows remain (point 3; design-r2 §13, call 16)

Point 3 was that the lexicon should not have to spell out what "on" means each time. The entries that did that are
gone:

- Before revision 2 there were 61 relation entries, 28 of them for prepositions and 33 for verbs, and no rows.
- Now there are 0 relation entries. A relation entry of any word is a lexicon problem (v_t8), and it no longer
  becomes a relation. The relations are 64 rows of `## Relations` tables: 42 use a preposition and 22 use a verb.
  With `Kind of:` they expand to 76 relations.
- These words have more than one row:
  - of 6;
  - in, on, for and with 4 each;
  - changes and gives 3 each;
  - removes, adds, outside, broken by, changed by and added by 2 each.
- The 4 rows for `on` are:
  - question on node;
  - question on term;
  - question on request;
  - stage on work-item branch.
- The 4 rows for `for` are:
  - stage for node;
  - stage for request;
  - stage for question;
  - worker brief for work-item.
- Under revision 1, `for` had 7 entries. Supervision's six collapsed into one row, stage for node, because a
  work-item, an initiative and a proposal are each a kind of node.

Why the rows stay: a row has no gloss and no prose. It is three or four cells, from kind, word, to kind and an
optional cardinality. Together the rows form the domain model's relation table, and two things need it:

- Typed PP attachment: "a stage for the work-item w1" has one tree because only (stage, for, node) joins those two
  kinds.
- The logic's `rel/3` atoms.

If any preposition could join any two kinds, every prepositional phrase in a line would attach in more than one way,
and the one-tree guard would refuse most lines. So the grammar can't make the table unnecessary. What it does is
reduce each row to a fact about the domain, with no meaning to write.

The question for the person: is a rowed relation table, one row per kind pair and none per meaning, an acceptable
answer to point 3? The alternative is fewer, more general rows on supertypes, such as one `on` row for a question on
any node-like kind. That takes more `Kind of:` structure in the glossary.

## Handed back (not in R14's files; none of them blocks an accept)

Carried from the layer 4 gate. Each is in a file R14 does not own, or is a spec wording wish whose line already
parses after rewording:

- **The generator** (`spec_trace*.py`, `grammar/background.lp`):
  - a group whose only response is `shall not` gets no Then;
  - `#minimize` counts an instance once for each state it is used in (R6, R9);
  - the naming needs `.lower()`;
  - J1 (a JSON object) is refused by Steps;
  - an AndVP's later `the <kind>` does not bind to a restricted antecedent;
  - state 0 holds what the command writes;
  - the negated GivenK_A value in world_nodes;
  - R8's minimisation oddities (g53).
- **Grammar wishes:**
  - Where+While+When (R11);
  - an NP list for `Do` (R11);
  - an NP-or for U7 (R13);
  - whether U10 allows the tool list (R13).

  The packages reworded each line, and `unparsed.sh` prints nothing. R14 adds no fun, because every new
  coordination widens the ambiguity the one-tree guard has to settle.
- **Not placed:** "a deprecated scenario formulates no requirement" (r5-moved-content, R13). It belongs to
  design-model-check or model.lp.
