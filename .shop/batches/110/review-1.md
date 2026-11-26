---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-110/review-1
kind: review
batch: batch-110
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/133
head: 1e4cde2b274fb09e526b40329595918c1c845f98
range: 4630e966448a78ae9864cb59e2b1079dbea3e68b..1e4cde2b274fb09e526b40329595918c1c845f98
result: clean
---

# batch-110 review 1

## Verdict

The batch builds both items. Every requirement line of b673 (product#r8 to r13) and of b674 (product#r14) is built and has a scenario. No test was removed or weakened: the refusal Then now also checks that no traceback is printed, which makes it stricter. The features are what `features generate` writes, every run exits 0, the change is under the size limit, and the module map rows of `product_store.py` and `product_layer.py` were updated. Nothing needs fixing; two observations follow.

## Findings

### f1 Minor observation: a product detail holding an infinite or NaN number, or a DEL character, is written back as TOML that does not read
- item: b673
- where: scripts/product_store.py:28
The risk: r8 to r10 say the product detail is kept, and `render` writes each value of a detail back through `toml_edit.literal`, which uses `json.dumps`. I checked `literal` in scripts/toml_edit.py:18-28. For a float it gives `Infinity`, `-Infinity` or `NaN`, but TOML spells these `inf`, `-inf` and `nan`. For a string it leaves U+007F (DEL) unescaped, and a TOML basic string does not allow that character. Reproduction: write `.shop/product/product.toml` with `[p1]` holding `x = inf`, then run `spec actor "the developer"`. The file is rewritten with `x = Infinity`, and the next `spec product`, `spec actor` or `spec job` refuses it as a file that does not read. So the detail is lost rather than kept. No client writes such a value today. A fix would be for `_literal` to write `inf`, `-inf` and `nan` itself and to escape control characters, or for `render` to check its text with `tomllib.loads` before `kept` writes it.

### f2 Minor observation: a job's own extra keys are kept on a second declaration, but no scenario checks it
- item: b673
- where: scripts/product_layer.py:71
`declare_job` now merges the new job over the stored one, so keys of `[jobs."<id>"]` outside the form survive a second declaration of that job. This fits the item's title ("keep the product file's other keys"). However, r10's scenario puts its product detail only in a top-level `[p1]` table, so a job table holding an extra key or a subtable is never read, re-declared and written back by any test. A regression there would go unnoticed. A scenario or a script test of a job table with an extra key would cover it.
