---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-95/review-2
kind: review
batch: batch-95
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/118
head: 0e6e1f6982081154f484aa50432e1dfcac30cc90
range: 4cf9d17cb1f8d4fc04151dc18e238cea9e2afbcf..0e6e1f6982081154f484aa50432e1dfcac30cc90
result: clean
---

# batch-95 review 2

## Verdict

Both earlier findings are fixed. f1 is fixed by giving the refusal its own requirement line, checking#r94, an If line that takes precedence over r81 on the same trigger. It was laid with `work batch amend` and is built: `unbuilt:` is empty at the head. The code now checks the id form and the upstream's reach before it looks for adapter specs, so r88 and r89 keep their reasons. f2 is fixed: all three stale module-map rows are rewritten. The one new finding is an observation and does not hold the merge.

## Findings

### f4 Minor observation: two If lines both apply to an unreachable upstream that no adapter spec names, and the refusal meets only r89
- item: b593
- where: scripts/contract_obtain.py:124
Picture an upstream that is unreachable and that no adapter spec has as its provider. Both If lines apply on the same trigger:
- r89 asks the refusal to name the bounded context and the `bounded context unreachable` reason.
- r94 asks it to name the provider and the `no adapter spec has the provider` reason.

The code checks the reach first (`repo = reached(root, context)` before `holders(...)`), so it names only r89's reason. That order is what f1 asked for, and `test_an_unreachable_upstream_no_adapter_spec_has_is_unreachable` pins it. Still, no line says one If line takes precedence over another. Read literally, r94 is unmet in that state. The same holds for r88 (an id out of the context id form) beside r94.

Reproduction: `tests/scripts/test_contract_obtain.py::test_an_unreachable_upstream_no_adapter_spec_has_is_unreachable` gives that state. Its refusal's reason is `bounded context unreachable`, and it does not name `no adapter spec has the provider`.

Possible later fix: condition r94 on a reachable upstream whose id is in the context id form, or add a line that orders the refusals. No client hits this today; no scenario reaches that state.

## Earlier findings
- f1: fixed
- f2: fixed
