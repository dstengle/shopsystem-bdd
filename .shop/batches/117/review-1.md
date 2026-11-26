---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-117/review-1
kind: review
batch: batch-117
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/140
head: 643f277f0e64bed33b0f493aed20b4711fa3684a
range: 888fdf7ffbc41fef0ea67f5b3290200b98f9c428..643f277f0e64bed33b0f493aed20b4711fa3684a
result: clean
---

# batch-117 review 1

## Verdict

The batch builds all ten lines of b643 (checking#r114-r123). The new rules in `scripts/model.lp` fire in the states the lines name and name what each line asks for. The three `w_unserved_cap` exemptions match r120-r122 and decision 0144. Every run exits 0, as it did at the base. The change is under the size limit (976 changed lines against 1000), and the module map has a row for `scripts/model_product.py` and the reworded `product_trace.py` row. No test is removed or weakened: the `address#2` edits in the corpus and the factoring fixture record the parser's new sense numbering, and the commit says why. Nothing needs fixing now; there are two observations.

## Findings

### f1 Minor observation: a product file not of the product form becomes a `spec check` file problem, which no line names
- item: b643
- where: scripts/model_product.py:44
`read_product` catches product_store's `Refused` and adds `"<REL>: <why>"` to `self.problems`. So a hand-edited `.shop/product/product.toml` that is not of the product form now makes `spec check` fail in this bounded context. No line of checking r114-r123 asks for that outcome. It is the reasonable alternative to a traceback, so it does not hold the merge. A later item could give it a line, for example "While the product file does not conform to the product form, if the person validates this specification, then the specification service shall fail the check and name the product file". Reproduction: write `jobs = 3` into `.shop/product/product.toml` and run `spec check`; it exits 1 naming the file.

### f2 Minor observation: every `spec check` of a context whose groups serve a job now loads the whole context and derives each job's trace
- item: b643
- where: scripts/model_product.py:85
When any group has a `serves:` line, `read_traces` calls `spec_context.load(self.root)` and `product_trace.joined` for each job served or held here. This happens even when the shop keeps no product file: `jobs` is then `{}` and `needs` returns `[]`, but `own` and `reached` still parse the context's facts and walk the request chain. Those trace facts are only needed when the product holds a job. I checked the risk: this repository's capabilities have no `serves:` line, so its own `spec check` is unaffected today. A consumer with served groups pays the extra cost on every check. A cheap guard is to skip `read_traces` when `product["jobs"]` is empty.
