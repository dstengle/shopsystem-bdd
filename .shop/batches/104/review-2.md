---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-104/review-2
kind: review
batch: batch-104
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/127
head: f91d73bc7e806743c8b5dec86c3ab6ced0fa1581
range: efb0fc527ed0acc359cc947983fd5de7c1b497ae..f91d73bc7e806743c8b5dec86c3ab6ced0fa1581
result: clean
---

# batch-104 review 2

## Verdict

The fix is right and adds nothing else. `caught` still accepts every argument `parse_args` and `parse_known_args` are called with, and `tools check` now exits 0 at Head. No new findings.

## Findings

None.

## Earlier findings
- f1: fixed
