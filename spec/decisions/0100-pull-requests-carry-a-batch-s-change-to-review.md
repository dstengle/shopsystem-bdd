---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/pull-requests-carry-a-batch-s-change-to-review
summary: "Submitting a batch opens a draft pull request, a clean review marks it ready, the person merges it on the host and the merge is read back."
date: 2026-11-19
status: accepted
tier: judgement
---

# 0100. Pull requests carry a batch's change to review

## Decision

A batch's proposed change is a draft pull request opened when the batch is submitted; a clean review marks it ready; the person merges it on the issue host, and closing the batch reads the merge. The pull request is the review adapter's; the requirements say proposed change, submit and merge.
