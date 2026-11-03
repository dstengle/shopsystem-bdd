---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-gate-r2-l5
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# Revision 2, layer 5 gate

The gate passed on `gf-conversion`. Its base was 43b78050, the layer 4 gate.

## Merged

gfr/R14 (d388ca5f, code at 93eb900c) was merged with `--no-ff`. There were no conflicts.

## Shared changes

1. **report-R14.md** was written from the package's notes. The package could not write it, because the harness
   refuses report files from a subagent.
2. **Plan amendment** (R14 ask 1): accept 5's test command in plan-r2.md now names
   `tests/scripts/test_spec_trace.py`, where R6 put `test_byte_stable` and `test_related_while_enters`.
3. **Ownership** (R14 ask 2): R14's changes outside its owned files are accepted. These are spec_relations.py,
   its tests, test_spec_lexicon.py, the docs and `scripts/model`'s help. Layer 5 had no other package, so nothing
   conflicts.
4. **Follow-ups** (R14 ask 3) are not done in this gate, because none fails a check. They stay listed in
   `gate-r2-done.md` and `report-R14.md` for the orchestrator:
   - the shall-not-only no-Then;
   - background.lp `#minimize`;
   - `.lower()` naming;
   - J1;
   - AndVP binding;
   - state-0 writes;
   - the GivenK_A negation;
   - g53 minimisation;
   - the grammar wishes;
   - the "deprecated scenario" line.

## The layer's gate (R14's accepts, re-run on the merged gf-conversion)

| # | check | result |
|---|---|---|
| 1, 2 | `model check --json`: rows v15k, v15l, v15m, v15n | none |
| 3 | `model lexicon --check` | `366 terms, 0 problems`, exit 0 |
| 3 | `grep -rn 'Means:' spec/` | nothing |
| 3 | relation counts and call 16 | in gate-r2-done.md |
| 4 | the five named tests | `5 passed` |
| 4 | `grep -rn 'HORIZON = ' scripts/` | nothing |
| 5 | `features generate --check` under PYTHONHASHSEED 1 and 2 | exit 0, exit 0 |
| 5 | `git diff --exit-code features/` | 0 |
| 5 | `pytest tests/scripts/test_spec_trace.py -k 'byte_stable or related_while'` | `2 passed` |
| 6 | `pytest tests/scripts/test_e2e_codified.py` | `1 passed` |
| 6 | q47's lines through `model parse --file` | exit 0 |
| 7 | full suite `pytest -q -p no:randomly` | 864 passed, 1 skipped, 0 failed (314 s) |
| 7 | the comm against baseline-failures.txt and the empty allowance | prints nothing |
| 7 | `tools size --limit 300` | exit 0 |
| 7 | the P14 map-row loop over `scripts/*.py` | no missing row |
| 7 | `features vocab --check --tests tests/scenarios` | exit 0 |
| 7 | `grep -n SCommits grammar/*.gf scripts/*.py` | nothing |
| 8 | `time model logic` | `no findings`, 33.1 s |
| 9 | `model check`: file:/unresolved: rows compared with comm against baseline-model-check.txt | empty; no abandoned-initiative rows to list |

## Other checks

- `.shop/scratch/unparsed.sh` prints nothing.
- `tools check` on the Python files changed since 43b78050 is clean (ruff, vulture).
- The 1.0.0 conversion grep (`v_p*`, `v15f`–`v15n`, `v_t4`–`v_t6`, `v_s1`–`v_s3`) on `model check` finds nothing.
- The allowance file `gate-r2-L1-allowed.txt` stays empty.
