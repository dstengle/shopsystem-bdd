---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-153/review-1
kind: review
batch: batch-153
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/176
head: d4c299422074b7a84377ab1af1af508673ae42a4
range: f561ce992d7da65cfe635b8e6e1c0b5f37144314..d4c299422074b7a84377ab1af1af508673ae42a4
result: clean
---

# batch-153 review 1

## Verdict

The batch builds all seven requirement lines of b793, b796 and b799. I found nothing to fix now. No tests were removed or weakened, and the `.feature` files are what `features generate` writes. Every check in `## Runs` exits 0 at `Head:`, and the change (+621 −70) is under the 1000-line limit. Two observations follow on how `work line --serves` reads the product file.

## Findings

### f1 Minor observation: `--serves` with a job's full id is refused even when the product holds the job under its name
- item: b799
- where: scripts/backlog_serves.py:39
`_job` lets a job through by `spec_read.JOB`, which accepts a job's name and also its full id `job/<path>/<name>`. It then checks the job against the product's job keys word for word:

```python
if (Path(root) / product_store.REL).is_file() and job not in product_store.read(root)["jobs"]:
```

`spec check` reads it differently. `model_product` compares jobs on both sides through `name_of`, which takes the last part of the id (scripts/model_product.py:62-72, 83). The risk I looked into was the two readers disagreeing on what "the product holds the job" means, and they do.

Reproduction: keep a product file that holds the job `keep-notes`, then run `work line b1 --serves work-queue#g1 job/example.org/keep-notes`. It is refused with `job outside the product`, but `spec check` would read the same `serves:` line as serving a job the product holds. No line uses the id form today, so this does not hold the merge. A fix would compare `name_of(job)` against the names of the product's jobs.

### f2 Minor observation: a malformed product file now blocks `work line --serves`
- item: b799
- where: scripts/backlog_serves.py:39
Once `.shop/product/product.toml` exists, `_job` calls `product_store.read`. That call refuses a file not in the product form (`product not in the product form`). Before this batch, `--serves` never read the product file. `spec check` treats the same file as a warning (`w_unformed_product`, scripts/model_product.py:55-58), not a refusal.

Reproduction: write a `product.toml` whose `jobs` is not a table, then run `work line b1 --serves work-queue#g1 start-work`. It is refused for a reason that has nothing to do with the job. r92 only covers a job the product does not hold. A gentler fix would skip the check, or name the file, when the product file does not read.
