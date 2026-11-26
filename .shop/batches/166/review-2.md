---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-166/review-2
kind: review
batch: batch-166
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/189
head: 25ae5c3fc3e59cf22b4a5f59be0086e63a845d49
range: dbc15d66aeb954fb0cb5ea874aeb00494e15f360..25ae5c3fc3e59cf22b4a5f59be0086e63a845d49
result: clean
---

# batch-166 review 2

## Verdict

The fix commit 6d8d853d6 resolves f1, and I found nothing new. `Lines` now numbers each verb's senses over the verbs grammar 4 reads. `spec_lf_np.Names` numbers `vocab.verbs` from 1, and `spec_lf_clause.sense` counts a verb's place among the entries of its word. The two numberings now agree, so the request pack's `refuse`, `return` and `name` (sense 1) are taken for the pack's, and the context's operation sense (sense 2) is taken for the operation.

All three callers pass grammar 4's verbs: model_domain passes `vocab.verbs`, adapter_annotate passes `spec_grammar4.sources(root)[0].verbs`, and product_coordination passes `rgl.verbs`. A pack's term carries the `Term.operation` default `""`, so the pack's sense reads as no operation and `packed` holds for it.

The new test `test_v_m4_a_refusal_by_the_request_packs_refuse_beside_the_contexts` covers the trigger path the finding named. The fixture's context redefines `refuse`, and the line on the refusal of a reservation, which uses the pack's `refuse`, still clears v_m4. Every check in `## Runs` exited 0, at the head and at the base. The change is 5 files, +38 -9, well under the limit.

## Findings

None.

## Earlier findings
- f1: fixed
