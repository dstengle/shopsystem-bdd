---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-130/review-2
kind: review
batch: batch-130
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/153
head: f24fe6d09fb806ec3896ad7a06f0cf30b8e12f4f
range: 06f4fa288a26a6cc07deb9be1b79f59f93166350..f24fe6d09fb806ec3896ad7a06f0cf30b8e12f4f
result: clean
---

# batch-130 review 2

## Verdict

The fix commit closes f1. `unthinged` now matches the subject that the regenerated Given records, so scenarios#r22 and #r25 get b298's world again. The fix adds no new problem, and every run exits 0 as it did at the base.

## Findings

### f5 Minor observation: nothing checks that scenarios#r22 and #r25 actually build the b298 world
- item: b716
- where: tests/scenarios/feature_file_tools_uses.py:135
f1 came about because `unthinged` quietly turned False and the plain catalogue example was used in its place, while every Then still passed. The fix brings the match back, but no step or assertion fails when `prepare` skips the `return`-worktree world, so a later change to the generated subject could break it the same way without anyone noticing. A cheap guard would be to assert in `prepare` that `unthinged(w)` is True whenever a "no frame … takes `thing`" fact exists. This is hardening and does not hold the merge.

## Earlier findings
- f1: fixed
