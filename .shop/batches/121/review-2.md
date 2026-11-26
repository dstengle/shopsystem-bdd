---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-121/review-2
kind: review
batch: batch-121
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/144
head: 8fb6dba0516e7ef1391d4447458a4a39b082103b
range: 78a31713f80748518b6c169d67a675a8d6e607a1..8fb6dba0516e7ef1391d4447458a4a39b082103b
result: clean
---

# batch-121 review 2

## Verdict

Both earlier findings are fixed. With no product file, `work context keep` now keeps any id, as shop#r1 says. shop#r6 refuses only while the product has an id, and the refusal now uses the reason that `shop.keep` declares. Every run exits 0. One observation about a test that no longer checks what its name says.

## Findings

### f7 Minor observation: the test of an id the product id covers no longer has a product id
- item: b666
- where: tests/scripts/test_shop_contexts.py:39
`test_an_id_the_product_id_covers_out_of_the_context_id_form_is_kept` still writes no `.shop/product/product.toml`. Before the fix, `product_id` fell back to `example.org/home`, so the test checked that a covered id with an odd last part (`A B`) is kept. Now `product_id` returns `""` and `keep` skips the coverage check entirely. The test passes whatever `covers` does with an id outside the context id form, so its name says more than it checks. No assertion was removed, so this is an observation, not a weakened test. Suggested change: write a product file with id `example.org/home` in this test, as the new refusal test does at line 54, so it again runs the covered branch of shop#r6.

## Earlier findings
- f1: fixed
- f2: fixed
