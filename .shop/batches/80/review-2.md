---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-80/review-2
kind: review
batch: batch-80
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/104
head: e118d5d90d9dbd52aa611c4cebeb507f4922c9b0
range: e4956254bc509cf154e78efa1524544e469e729f..e118d5d90d9dbd52aa611c4cebeb507f4922c9b0
result: clean
---

# batch-80 review 2

## Verdict

Both earlier findings are fixed. One minor observation, which does not hold the merge.

## Findings

### f6 Minor observation: the new test of f1 builds the tree by hand and never parses a line
- item: b543
- where: tests/scripts/test_spec_one_thing.py:44
`test_a_response_request_with_a_plural_object_is_found` builds the tree `["k_service_ActReq_k_service", "PPos", ["q_remove_1_1", ...]]` itself and calls `plural` on it. That shows `plural` now finds a plural object under `_ActReq_`. It does not show that a real line is refused end to end. Such a line would be "the notes service shall remove every note with ...", going through spec_grammar4.py:204-206 and the `spec_one_thing.refusal` message.

The risk was that the real fun name differs from the hand-built one. I checked it: `spec_rgl_ops.py:148` generates `"%s_ActReq_%s" % (D, S)` with `Pol -> S_Req -> D_Act`, which is the shape the test builds. `spec_grammar4.py:204` calls `plural` on every tree. So the risk is small.

A cheap way to close it: a parse test in the domain-model fixture, asserting that such a line is refused with "a request acts on one thing".

## Earlier findings
- f1: fixed
- f2: fixed
