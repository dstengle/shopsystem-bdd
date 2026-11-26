---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-160/review-1
kind: review
batch: batch-160
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/183
head: 3840e14c0933772d3e342423752cc4b7a93c6a35
range: 701a6c6fe89994dbfd020c6022c95475d0c2495e..3840e14c0933772d3e342423752cc4b7a93c6a35
result: clean
---

# batch-160 review 1

## Verdict

The batch builds all eight requirement lines of b824, b826 and b827. I found nothing that has to be fixed before the merge. Every run in `## Runs` exits 0 at `Head:` and at the base, the two `.feature` files match what `features generate --check` writes, the change is under the size limit (+521 -103 against 1000), no test is removed or weakened, and the CLAUDE.md module map has a row for each changed or new module. I record two observations.

## Findings

### f1 Minor observation: r71's scenario still passes without the product id form check
- item: b827
- where: tests/scenarios/product_handlers_unformed.py:133
Here is what I read. The unformed world always writes a product file with an id. `world` sets `{"id": "example.org"}`, and only a Given of `has` changes it. r71's scenario has no such Given, so `spec product garden-i1` runs against a product that already has the id `example.org`. If you took out the `IDENT.fullmatch` check in `product_layer.declare` (scripts/product_layer.py:54), r70's check just below it would still refuse the request, because `example.org` is not `garden-i1`. That refusal names the same id, so every Then of r71 would still pass. This means the scenario cannot catch a lost r71 check. r71 has no While part, so its world should hold no product id. Hardening: in `runs`, write the product file with no id for r71's tag, as r74's Given does. Note also that the world's default id `example.org` does not itself match the product id form the batch adds.

### f2 Minor observation: v_t13's message now cuts the frame at its first sentence, which no line of the batch asks for
- item: b826
- where: scripts/spec_frames.py:156
`misread` now passes the frame text, and the word it could not read, through `_sentence`, which splits at the first `.` followed by whitespace. This changes what `spec check` and `spec lexicon --check` print for v_t13. None of drafting r101 or r102 asks for that. The nearest line is checking#r151 ("name the frame"), and it supports the change: the gloss after a `Frame:` is not part of the frame. So I am not asking for the code to go. The risk is a `Frame:` whose own text holds `. `, for example inside a backticked code. Its frame would be shown cut short in the message. Detection is not affected, because only the message text passes through `_sentence`.
