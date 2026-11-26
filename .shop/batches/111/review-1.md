---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-111/review-1
kind: review
batch: batch-111
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/134
head: ce577fb1c92bd4515d39a4de86f5ac075f821e4a
range: 96193bcceb85b6207d9592087e40c326c1a06c70..ce577fb1c92bd4515d39a4de86f5ac075f821e4a
result: clean
---

# batch-111 review 1

## Verdict

The batch builds all seven lines of b642 (product#r15-r21). `spec subdomain` and `spec context` keep, refuse and name as the lines say. The model, the vocabulary, the CLI table, the corpus, the module map and the docs are all in step. Every run exits 0 at `Head:`, and the change is 523 lines against a limit of 1000. I found nothing to fix now; three observations follow.

## Findings

### f1 Minor observation: r20's refusal names the context's id, while the line names the product's
- item: b642
- where: scripts/product_map.py:359
r20 is read with "the id" bound to the id of this product. In grammar/corpus/spec/product.md the response is `name(e3, subject: x6, object: x5)`, and x5 is `of(x5, x4)`, the product's id. The generated scenario agrees: "the product service names the id i2". The refusal's structured reference is `names=["parameter:id"]`, though, and that parameter is the bounded context's id, so a `--json` envelope names the other id. The scenario passes only because the free text holds both ids (`... lies outside the product's id example.org`). The text already names the product's id, so no line is answered wrong. If the line meant the id the person gave, it should be reworded under a new id. If it meant the product's id, the reference could name it rather than the parameter.

### f2 Minor observation: a bounded context with no subdomain is kept
- item: b642
- where: scripts/product_cli.py:308
Decision 0128 says a bounded context addresses one or more subdomains, and r18 and r19 both say "with a subdomain". `--addresses` is optional, though, and `declare_context` keeps a context with `addresses = []`. Reproduction: run `shop spec context example.org/x --shop s` on a product whose id is `example.org`. It exits 0 and keeps `[contexts."example.org/x"]` with `addresses = []`. No line names this case, so it is hardening: either require one `--addresses`, or let a later line say how a context with none is refused.

### f3 Minor observation: one context can be kept under two keys
- item: b642
- where: scripts/product_map.py:337
`covers` accepts the id with or without its `bounded-context/` prefix. `declare_context` then stores the id exactly as given. So `spec context bounded-context/example.org/x` and `spec context example.org/x` keep two entries for one context. `shop_contexts.covers` (scripts/shop_contexts.py:28) accepts only the prefixed form, so the two modules now disagree on the id form. Fix: normalise the key before storing it, or refuse the form the context id form does not allow.
