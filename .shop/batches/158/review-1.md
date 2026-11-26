---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-158/review-1
kind: review
batch: batch-158
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/181
head: f58e8e3c211b5a0ec3f542174c0bbc7981f9ccc9
range: 0a68fede8fb685eb45e05e6670466beb36d93424..f58e8e3c211b5a0ec3f542174c0bbc7981f9ccc9
result: fix-now
---

# batch-158 review 1

## Verdict

The batch builds all three items. b803 accepts a job given by its name or its id and names a product file that is not of the product form. b811 reports a slotless `Frame:` as a v_t13 naming the frame. b812 refuses each drop of something the product does not hold, and a context id outside the form. One check now fails at Head and passed at the base: ruff's import order in `scripts/backlog_serves.py`. It is to be fixed on b803.

## Findings

### f1 Important fix now: ruff I001, the new import in backlog_serves.py is out of order
- item: b803
- where: scripts/backlog_serves.py:13
The run `python3 scripts/tools check --base 0a68fede8` exits 1 at Head and exited 0 at the base. Its output:

```
== ruff ==
scripts/backlog_serves.py:13:1: I001 [*] Import block is un-sorted or un-formatted
Found 1 error.
```

b803's commit 0eea48bb5 put `from model_product import name_of` between `import product_store` and `import spec_read`. That breaks the sorted import block, so the review check that guards the repository's lint now fails. Fix: sort the block, for example with `ruff check --fix scripts/backlog_serves.py`, and commit it on b803's branch citing the finding.

### f2 Minor observation: a job id of another product counts as held when its last part matches
- item: b803
- where: scripts/backlog_serves.py:52
`_job` compares only `name_of(job)`, the last part of the id. So `work line b1 --serves work-queue#g1 job/other.org/start-work` passes against a product `example.org` that holds `start-work`, and the pair is stored with the foreign id. This is how `spec check` (model_product's `name_of`) reads it, and r97 asks for no more, so it is consistent. A check that the id's path is under the product's id would close it. No client sends such an id today.

### f3 Minor drop: groups g63-g67 of product.md are not in id order
- item: b812
- where: spec/capabilities/product.md:206
g63 is laid after g64-g67. It is cosmetic: the scenarios and the corpus read by id, so nothing depends on the order.
