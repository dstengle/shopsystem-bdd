---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-183/review-1
kind: review
batch: batch-183
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/205
head: a4147c026aadba20757d589509c2a39d09ede13c
range: 3478b73780b58ac003407e48bb2bedad864a0423..a4147c026aadba20757d589509c2a39d09ede13c
result: fix-now
---

# batch-183 review 1

## Verdict

The batch builds b903's line applying#r51, b899's retirement of the laying area and the chore changes of b862 and b863. One finding must be fixed: the vulture part of `tools check` now fails, because b863 touched a test file. There is also one observation.

## Findings

### f1 Important fix now: `tools check` fails at Head on vulture in tests/scripts/test_docs_lines.py
- item: b863
- where: tests/scripts/test_docs_lines.py:63
The run `python3 scripts/tools check --base 3478b73...` exits 1 at Head and exited 0 at the base. Its output:

```
== vulture ==
tests/scripts/test_docs_lines.py:63: unused variable 'tools' (100% confidence)
tests/scripts/test_docs_lines.py:68: unused variable 'tools' (100% confidence)
...
tests/scripts/test_docs_lines.py:142: unused variable 'tools' (100% confidence)
```

`scripts/tools_check.py:61` runs vulture only on the paths the range changes. b863's commit 09c8a16c7 edits `test_a_scenario_missing_a_given_is_caught` (it renames `docs/tour.md` to `docs/internals-tour.md`), so this file is now scanned. Each test of the file takes the module fixture `tools` (line 59) as an argument it never uses. The pattern was already there, but the batch is what makes the check fail. The check fails red until it is fixed.

Fix, in this file, which is among b863's chore files: take the fixture with a `@pytest.mark.usefixtures("tools")` mark on each test, or on the module through `pytestmark`, and not as an argument. The fixture still runs `toolchain.require()` before each test, and the assertions stay as they are.

### f2 Minor observation: spec_composition.held still falls back to a capability's file stem
- item: b903
- where: scripts/spec_composition.py:35
b903's notes name the file-stem fallback in `backlog_retire_area.capabilities`, `spec_composition.held`, `domain_model`, `adapter_uses` and `spec_vocabulary`. The change routes `backlog_retire_area` and `adapter_uses` through the new `spec_read.area_of`. `held` still reads `_field(text, "area") or path.stem`.

What I checked:
- `domain_model._area` and `spec_vocabulary` read model files and vocabulary layers, not capability files, so they need no change.
- `held` names only capabilities that hold a live requirement. A capability of a retired area holds only retired ids, because `retire_area` refuses otherwise. So r51 holds as written: the laying capability is in no Composition row.

The two readers still disagree for a capability that has a live requirement, no `area:` and no model file of its stem. `held` puts it under an area named after its stem, which `area_of` says does not exist. Fix when this file is next touched: use `spec_read.area_of(root, path)` in `held`, and leave a capability in no area out of every row.
