---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-20-formulation-deprecates-test-log
kind: measurement
about: capability/missingmass.io/shopsystem/shopsystem-bdd/formulation
date: 2026-10-20
---

# Test log: formulation deprecates a passing scenario whose line changed, on the final layout

Case T-formulate (formulation r1, r4, r6, r7, r11): a shelf fixture on the final layout with working code
(`shelf.py`), `features/keep-items.feature` (r1, r2) bound by `tests/test_keep_items.py`, and an approved change
of line r2 (counts different titles, a title held twice once), committed after the formulated state. The old r2
scenario passes today. Harness: `/home/vscode/scratch/shopsystem-bdd/formulate/` (`make_formulate.py`, `run.sh`,
`score.py`). Plugin: this working copy at commit 71da2bb, `claude -p --model sonnet --plugin-dir`, the person's yes
given in the prompt, "commit the feature files and the rebound tests, then stop".

## Runs t1 to t3

Each run: one commit, changing `features/keep-items.feature` and `tests/test_keep_items.py` only.

| check | t1 | t2 | t3 |
|---|---|---|---|
| old r2 scenario tagged `@deprecated`, keeps `@r2` | yes | yes | yes |
| " (deprecated)" at the end of its title | yes | yes | yes |
| `Deprecated for:` names the new scenario's title | yes | yes | yes |
| new scenario tagged `@r2`, one for the line | yes | yes | yes |
| r1 scenario byte for byte | yes | yes | yes |
| test of the old scenario rebound to the new title | yes | yes | yes |
| `features bindings`: every binding names a scenario | yes | yes | yes |
| `model check`: no v_s1, v_s2, v_t1 (0 violations, 0 file problems) | yes | yes | yes |
| `shelf.py` untouched, tree clean | yes | yes | yes |
| old scenario run alone (`pytest -q -k`) before deprecating | yes | yes | yes |

3 of 3 pass. `features deprecate` was run in each (4 or 5 mentions in the transcript); `pytest` of the result:
2 passed (the new scenario has no test yet, slicing's).

Not measured: `--for-removal` for a removed line; a title held by several feature files (`--file`); a changed
line whose old scenario fails today (r5).
