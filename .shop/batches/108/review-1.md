---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-108/review-1
kind: review
batch: batch-108
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/131
head: 0da3f86c31e7273bf098b12a5283010e108d2ce8
range: 232d5d62af8accbf2ecf6aa88734485005e81354..0da3f86c31e7273bf098b12a5283010e108d2ce8
result: clean
---

# batch-108 review 1

## Verdict

The batch builds all seven lines of b602, r1 to r7. `spec product`, `spec actor` and `spec job` keep the product file in one commit. They refuse a job's statement, actor or need, and a need that closes a cycle, each naming its option. Every run exits 0 at the head as at the base, and the change is 681 lines against a limit of 1000. Nothing is to fix now; two hardening observations follow.

## Findings

### f1 Minor observation: the product file's unknown keys are dropped on the next write
- item: b602
- where: scripts/product_store.py:28
`read` keeps only `id`, `purpose`, `actors` and each job's `actors`, `statement` and `needs`. `kept` then writes the whole file again from that dict. Any other key in `.shop/product/product.toml` is silently removed by the next `spec product`, `spec actor` or `spec job`. This covers a key added by hand or by a later item (b642's domain map, b641's `serves:`). A file whose `jobs` or `actors` has the wrong type (`jobs = 3`) reaches `.items()` and crashes as broken, where a refusal belongs. No line names either case today, and only these commands write the file. Reproduction: add `subdomains = ["x"]` to the file, then run `spec actor "the developer"`. The key is gone in the commit. Fix when a later item adds a part: keep the other keys, or refuse a file of another shape naming the file.

### f2 Minor observation: a job whose statement's situation holds a comma is refused
- item: b602
- where: scripts/product_layer.py:35
`FORM` reads the situation as `[^,]+\S` and the actor as `\S[^,]*?`, so neither may hold a comma. A statement such as `When a change, once reviewed, is wanted, the developer wants it built, so they can ship it.` reads as the job statement form, but it is refused naming `--statement`. r4 asks only for refusing a statement of another form, so this is an edge that no line names. Fix if the person wants it: let the situation run to the last `, <actor> wants`.
