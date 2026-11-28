---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-183/review-2
kind: review
batch: batch-183
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/205
head: 14f2d0292f199b3ed124271f866ce22a885fb2f1
range: a4147c026aadba20757d589509c2a39d09ede13c..14f2d0292f199b3ed124271f866ce22a885fb2f1
result: clean
---

# batch-183 review 2

## Verdict

The fix closes f1. Every test in tests/scripts/test_docs_lines.py now takes the module fixture `tools` through `@pytest.mark.usefixtures("tools")` instead of an unused argument, and the run of `tools check` now exits 0 with vulture clean. Each test's body and assertions are as they were. The parametrize list of `test_a_sketch_context_s_features_are_current` still holds `docs-shop` and `docs-labels`. The module-scoped fixture at tests/scripts/test_docs_lines.py:58 still runs `toolchain.require()`. `size`, `features generate --check`, `features bindings --unbound` and `spec decisions --check` exit 0 at Head and at the base. The change is 1 file, +22 -11, well under the limit. Nothing new to fix.

## Findings

None.

## Earlier findings
- f1: fixed
