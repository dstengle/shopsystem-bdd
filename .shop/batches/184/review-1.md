---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-184/review-1
kind: review
batch: batch-184
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/206
head: 98936119c63ecbd0262b4bfca77799f65b89615d
range: 4f5962b26defa71c395f85a56403c48962f630f3..98936119c63ecbd0262b4bfca77799f65b89615d
result: fix-now
---

# batch-184 review 1

## Verdict

The batch builds b868: `docs/tutorial.md` covers product, actor and jobs, context, capability, model, lines, batch, merge and plays. `docs/index.md` links it in two places. `tests/scripts/test_docs_tutorial.py`, with its helper `tests/scripts/docs_tutorial.py`, replays the page in a tmp_path folder, using `stub_gh.py` and `toolchain.require()`, and compares the result with `docs/examples/notes-cli/`. Each module has its row in `docs/reference/modules.md`. Commit f14833384 touches only the item's chore files. One finding must be fixed before the merge: the change breaks the `tools check` run, which passed at the base. The change is also over the size limit.

## Findings

### f1 Important fix now: ruff fails on an unused unpacked variable in docs_tutorial.py
- item: b868
- where: tests/scripts/docs_tutorial.py:37
`python3 scripts/tools check --base 4f5962b26` exits 1 at Head and exited 0 at the base. Its output is:

```
== ruff ==
tests/scripts/docs_tutorial.py:37:13: RUF059 Unpacked variable `fence` is never used
Found 1 error.
```

The line is `fence, lang, body, at, file = open_` in `steps`, and `fence` is never read after it. The batch added this check failure, so the repository's checks are red until it is fixed. Fix: unpack it as `_, lang, body, at, file = open_` (or `_fence`), then run `tools check` again.

### f2 Minor observation: the change is over the size limit
- item: b868
- where: -
`## Size` gives 5 files, +1036 -1, against a limit of 1000 changed lines. Almost all of it comes from b868's new page `docs/tutorial.md` (772 lines). The test and its helper add 259 lines, and both stay under the 300-line file limit. The item is rated `large`, and a page that walks the whole loop is long by nature, so this does not hold the merge.
