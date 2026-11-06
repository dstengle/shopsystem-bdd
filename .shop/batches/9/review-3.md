---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-9/review-3
kind: review
batch: batch-9
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/24
head: 4eec885d253a0d8b2d4ddbcfb859a19a7e3e2ba5
range: 4eec885d253a0d8b2d4ddbcfb859a19a7e3e2ba5..4eec885d253a0d8b2d4ddbcfb859a19a7e3e2ba5
result: fix-now
---

# batch-9 review 3

## Verdict

The person's review comment on the pull request (2026-11-06T16:56:16Z), recorded as this review: one finding to fix before the merge.

## Findings

### f6 Important fix now: a post GitHub accepted is left in place, and a retry posts it again, when the commit recording its URL fails
- item: b36
- where: scripts/request_post.py:135
The person's words: "Major issue: if GitHub accepts the comment/issue but the subsequent commit that records its URL fails, the operation reports failure while leaving the remote post in place (`scripts/request_post.py:135-136`, and issue creation at `scripts/request_moves.py:188-189`). Retrying can create duplicate comments or issues, and a newly created issue may be orphaned from its local request. Please add recovery or idempotency handling for this post-success/bookkeeping-commit failure."
