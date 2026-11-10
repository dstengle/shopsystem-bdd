---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-29/review-1
kind: review
batch: batch-29
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/41
head: cf5f2b29e62c22eb1fba9a5e82528a9ff6340848
range: 6e10e78e5f89a35734b82cf425bd0da8428bc7a9..cf5f2b29e62c22eb1fba9a5e82528a9ff6340848
result: fix-now
---

# batch-29 review 1

## Verdict

The batch builds the requirement lines of b143, b144 and b150. One thing must be fixed before merge: `tools check` exits 1 at Head and 0 at the base, because of four ruff errors in b150's code and test. There are also three observations: the change is over the size limit, the generator's "overstated" test is narrower than the term's definition, and a handler is placed in another capability's module.

## Findings

### f1 Minor fix now: ruff fails on b150's new code and test
- item: b150
- where: scripts/model_spec.py:135
`tools check --base 6e10e78e` exits 1 at Head and exited 0 at the base. All four ruff errors are in b150's commit 150a8fb4:
```
scripts/model_spec.py:135:9: RET501 [*] Do not explicitly `return None` in function if it is the only possible return value
scripts/model_spec.py:135:9: PLR1711 [*] Useless `return` statement at end of function
tests/scripts/test_backlog_recodify.py:17:30: RUF100 [*] Unused `noqa` directive (non-enabled: `E402`)
tests/scripts/test_backlog_recodify.py:18:19: RUF100 [*] Unused `noqa` directive (non-enabled: `E402`)
```
The `return None` at the end of `SpecReading.parsed4` is its only return, and the two `# noqa: E402` comments on the `codified2_mixed` and `toolchain` imports of the test are unused. Fix: drop the trailing `return None`. The caller `parsed` already returns what `parsed4` gives, which is None either way. Then drop the two `noqa` comments, or run `ruff --fix` on both files.

### f2 Minor observation: the change is over the size limit
- item: -
- where: -
`## Size` gives 39 files, +1413 -75, against a limit of 1000 changed lines. b144 makes most of it: `spec_steps4.py` (195), `spec_rgl_steps.py` (100), `features_vocab4.py` (97), `features_generate4.py` (81), `test_spec_steps4.py` (110) and the Steps4 grammar. Next comes b143: `model_explain.py` (150) with its handlers and world conditions. b150 makes the least: `backlog_recodify.py`, `spec_language.py`, `test_backlog_recodify.py` and the reader changes.

### f3 Minor observation: an "overstated" Then entailed by the pack's definition alone is kept
- item: b144
- where: scripts/features_generate4.py:588
The term `overstated` (feature-file-tools) covers a Then that "a universal condition or a pack's definition entails". `entailed()` leaves a Then out only when `set(premises) & universal` is non-empty. The pack's definition of refuse is used only as the bridge that lets a universal condition fire. So a Then that only the CLI pack's definition entails stays in the feature: for example, the error exit of a line that says both "shall refuse the command" and "shall exit with an error". This is what I read in the code; no scenario covers such a line. r21's fixture (`declining`) only needs U1 through the bridge, so the line as tested passes. Hardening: either leave out a Then the bridge alone entails, or narrow the term's wording in a later item.

### f4 Minor observation: feature-file-tools' handler is reached through requests_handlers_issues
- item: b144
- where: tests/scenarios/requests_handlers_issues.py:195
r21's Then (`features does not write the file f1`) is dispatched from requests' `("ThenDoesNot", "write")` handler, which calls `feature_file_tools_handlers.unoverstated` when `generated` is in the context. The module map row for `requests_handlers_issues.py` says it holds "the handlers of the conversation on the issue". A feature-file-tools Then routed through it is outside that row, and any later scenario that sets `generated` will be diverted there silently. Moving the registration to a shared fallback (`world_fallbacks.py`, which holds the registry's fallbacks of keys one capability claimed) would keep the map true.
