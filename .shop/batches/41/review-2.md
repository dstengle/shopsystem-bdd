---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-41/review-2
kind: review
batch: batch-41
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/63
head: 4cdd5e0c4732f95bf5a899a2d2a0b73eefced5b0
range: c0b2a60058e88da83e179d14bead75afa0f24c33..4cdd5e0c4732f95bf5a899a2d2a0b73eefced5b0
result: clean
---

# batch-41 review 2

## Verdict

The fix for f1 does what the finding asked. It adds one bullet (+7 lines) to batches' `## Implementation, may change` section. The bullet covers everything `work batch merged` and `work accept` do that r40 does not ask for:
- `work accept` writes `request_lines` on the item, and a batch's renumbering carries it to the new ids.
- After the merge, a request is resolved through `work resolve`'s path, each line as `<cap>#r<n> <merge commit>`.
- The line `<q> resolved: delivered by <item>` is printed.
- A request that is not resolved (not `accepted`, an item that records no line of it, or a refused resolve) is left alone and named as `<q> not resolved (<why>); run work resolve`.

I checked the bullet against /home/vscode/shopsystem-bdd/.shop/worktrees/batch-41/scripts/batch_close.py:54-73. The statuses, the reasons and both printed lines match the code. All runs exit 0, as they do at the base, and the change is far under the size limit.

## Findings

None.

## Earlier findings
- f1: fixed
