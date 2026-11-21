---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-63/review-2
kind: review
batch: batch-63
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/87
head: f19e5292b8a952a47649884e99ad1c657035a955
range: c743adad11e924655207a90f25dab2103fbd82c0..f19e5292b8a952a47649884e99ad1c657035a955
result: clean
---

# batch-63 review 2

## Verdict

The fix for f1 is right. With no paths and no `--base`, `tools check` now diffs `<base>...HEAD`, so it lints only the commits the branch made since it forked. The new scripts test would fail on the old code and passes on the new. There is nothing left to fix now; there is one observation about the `--base` path.

## Findings

### f4 Minor observation: `--base` still lints uncommitted edits and the base's later commits
- item: b490
- where: scripts/tools_check.py:26
The fix covers only the default base. `since = args.base or base() + "...HEAD"` reads as `args.base or (base() + "...HEAD")`, so `--base X` still runs a two-dot diff of the working tree against `X`. That run picks up uncommitted edits, and if `X` is a branch tip that has moved on, it picks up files only `X` changed. Today this does no harm: f1 and code-analysis#r16 are about the no-argument call, and the review check passes a commit sha (`--base 328a1cc...`). To reproduce: on a branch, change and commit a file on `main`, edit an unrelated tracked file without committing, then run `tools check --base main`. Both files get linted. A fix, if it is wanted, is to use `X...HEAD` for `--base` too.

## Earlier findings
- f1: fixed
