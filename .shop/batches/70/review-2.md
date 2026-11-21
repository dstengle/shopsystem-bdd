---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-70/review-2
kind: review
batch: batch-70
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/94
head: 3260f58eab7d292bb96fb63160529def256961ae
range: 6cbcdf9fb873266edd5948f61b1eada15fd02a48..3260f58eab7d292bb96fb63160529def256961ae
result: clean
---

# batch-70 review 2

## Verdict

The fix closes f1. r53's line is now laid again as r55 under its own group, g55, titled "An accepted context request resolved is delivered and its thread closed". `features/context-requests.feature` has two different titles at lines 674 (g54) and 686 (g55), so pytest-bdd no longer replaces one scenario with the other. The resolve scenario is back in the feature with all of its Thens: `delivered`, a kept resolution, the side set to `asker`, the entry on the request and the thread `closed`. These are the Thens retired r29's scenario checked.

The thread handlers now take g55 in place of g53: `GROUPS` in `tests/scenarios/requests_handlers_thread.py` and `ADDED` in `tests/scenarios/requested.py` both name it. r55 is out of `unbuilt:` on both branches. Nothing else in the tree still refers to `context-requests#r53` or g53. These files were changed to match: `spec/adapters/cli.toml`'s annotation, the spec corpus block (`Retires: r29. From: b68 r55.`) and the module map row in `CLAUDE.md`.

Every run exits 0 at `Head:`, and `features generate --check` among them shows the feature is the generated one. The size is 7 files, +32 -32, well under the limit. Nothing goes against a judgement decision: r53 was only ever laid on the batch branch and never merged, so taking it away under the amend does not edit a live requirement in place.

## Findings

None.

## Earlier findings
- f1: fixed
