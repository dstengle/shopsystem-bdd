---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-157/review-2
kind: review
batch: batch-157
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/180
head: 1d6c92cc5abeb3737b27e8ec83cae73dcb14a5d6
range: 1b7c97d23bb626d61a1b99bb470f8d76b4a786d3..1d6c92cc5abeb3737b27e8ec83cae73dcb14a5d6
result: clean
---

# batch-157 review 2

## Verdict

All five earlier findings are fixed. f3 was fixed by changing r62's wording instead of rebinding its noun phrase. The line now reads coherently, but it no longer asks for the refusal to name the product actor, and the item's note asks for exactly that. That is one observation, not a finding to fix now. All the runs exit 0, and the change is well under the size limit.

## Findings

### f8 Minor observation: r62 no longer asks for the refusal to name the product actor, though b813's note and the module map still say it does
- item: b813
- where: spec/capabilities/product.md:189
The fix for f3 (ba8d73ed4, 7ef51427e) changed r62 to "...then the product service shall refuse the request." Before, it ended "...and name the product actor." The line is now consistent with itself: its corpus form has no `of(x6, x2)`, and the scenario ends at `Then the product service refuses this request`, which the existing refuse Then checks. But b813's note says "A job declared with no product actor is refused naming the product actor". The `scripts/product_layer.py` row of CLAUDE.md also still says "refused first, naming the product actor (product r62, b813)". No requirement now asks for the `--actor` naming on this path. The scenario also only checks that some refusal happens, so it cannot tell whether the product actor was checked first.

The rewording f3 suggested would have kept the naming: say "the product actor" as the request's parameter, the request pack's `the p` noun phrase. Suggestion: open an item (`work idea`) that adds back the naming in that form, retiring r62. Until then, drop "naming the product actor" from the r62 part of the product_layer row, or reword it to match.

## Earlier findings
- f1: fixed
- f2: fixed
- f3: fixed
- f4: fixed
- f5: fixed
