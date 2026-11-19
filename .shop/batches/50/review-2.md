---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-50/review-2
kind: review
batch: batch-50
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/74
head: 6d17384c05548bef10925bc65e98dc2866ea54bc
range: 632de961b04e74d2e340b04bb4aa58201292409f..6d17384c05548bef10925bc65e98dc2866ea54bc
result: clean
---

# batch-50 review 2

## Verdict

The fix (1ce279f70) resolves f1, and I found nothing new. At Head, `tools check --base` exits 0, as it did at the base. The `check` parameter is gone from `model_rules.catalogue`, and its only caller, `cmd_rules` in `scripts/spec`, no longer passes it. The `# noqa: E402` is gone from `tests/scripts/test_model_catalogue.py`. `--check` still takes the path that does not write, because `catalogue` is called with `write=args.write` and `args.write` is false under `--check`. The risk I named was a caller still passing `check=`, which would now raise a TypeError. I searched the tree and found no such call: `scripts/batch_catalogues.py` uses `model_rules.rules`, `wrong` and `render`, never `catalogue`. The fix removes no test and weakens none. Every run exits 0, and the change is 3 files, +3 -3, well within the size limit.

## Findings

None.

## Earlier findings
- f1: fixed
