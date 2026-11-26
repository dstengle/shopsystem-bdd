---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-106/review-2
kind: review
batch: batch-106
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/129
head: ae6b8260d87e0c3ecc90624a306cc1167e02b0ab
range: 310e2c23e1dbcd0ff7559e33b48c100b2677f012..ae6b8260d87e0c3ecc90624a306cc1167e02b0ab
result: clean
---

# batch-106 review 2

## Verdict

The fix closes f1. `under()` now starts the second process with `os.execve(..., {**marked(), "TOOLS_UNDER": python})`, so that process carries the `shop` mark and prints no notice. I traced both cases.

- **`tools refs`**: the first process prints the notice once at `__main__`, then starts again with the mark. The second process removes the mark and prints nothing. One notice.
- **`shop tools refs`**: `shop` sets the mark and the first process removes it. `marked()` adds it back from `os.environ`, so the second process is silent too. No notice.

The new parametrized test in `tests/scripts/test_old_names.py` does make `under` run again. I checked that `tools_env.interpreter` returns the `--python` value as given (`py/python`). Its path differs from `sys.executable`, so the second process does start. Under the old code, `tools` would have printed the notice twice and the test's count of 1 would have failed, so the test catches the fault.

No test was removed or weakened. The change is 2 files, +14 -4, under the 1000-line limit. Every run exited 0, as it did at the base.

## Findings

None.

## Earlier findings
- f1: fixed
