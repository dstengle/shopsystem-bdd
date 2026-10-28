# w226 notes (research)

Tools: `tools` present; `tools tests-of` answered "no map" (not made, per brief). Counts by `refs` or search as marked.

## 1. Why each scenario is red today

Command run once: `python3 -m pytest -q --work-item w226` (run):
183 passed, 1 skipped, 56 subtests passed, 0 failed. Both accepted scenarios are collected (their tests appear in the warnings) and neither fails. Neither is red.

- features/supervision.feature:1507 (@r159, change list split per capability): green. Code: scripts/supervise_change.py `Changes.write_proposals` (line 94), called from scripts/supervise_rounds.py:205 (read).
- features/supervision.feature:1757 (@r168, gate asked only on lines the proposal changes): green. Code: scripts/supervise_brief.py `brief` (line 41), gate question limit at lines 76-81 (read).

The work-item only retires three deprecated scenarios; no code change is needed for its accepted scenarios.

## 2. Old assumptions

r159 and r168 replace r92 and r104 (both in spec's `retired:`). Table by search (no map):

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| features/supervision.feature:1302 (outline "that <reply>", @r77 @deprecated) | deprecated scenario, Deprecated for: the r163 outline (line 1334) | w226's Retires bullet 1 removes it; its replacement r163 is accepted by w223, not w226 (see conflict A) | its generated test, tests/scenarios/test_supervision.py:61 `scenarios(...)` | read, by search |
| features/supervision.feature:1474 (@r92 @deprecated, change-list split) | deprecated scenario, Deprecated for: the r159 title (line 1507) | removed by Retires bullet 2 | generated test, test_supervision.py:61 | read, by search |
| features/supervision.feature:1484 (@r92 @deprecated, two initiatives, different ids) | deprecated for removal | not named by Retires; stays deprecated (see conflict B) | generated test, test_supervision.py:61 | read, by search |
| features/supervision.feature:1706 (@r104 @deprecated, gate questions) | deprecated scenario, Deprecated for: the r168 title (line 1757) | removed by Retires bullet 3 | generated test, test_supervision.py:61 | read, by search |
| scripts/supervise_change.py:1 (docstring) | cites "r92, r96, r107, r114" | comment only; r92 retired, r159 is the live id | none | read |
| scripts/supervise_brief.py:132 (docstring), :79 (comment "r104") | cite retired r92, r104 | comment only; r168 is the live id | none | read |
| scripts/supervise_rounds.py:146 (comment "r96, r92") | cites retired r92 | comment only | none | read |
| scripts/supervise_brief.py:43 and scripts/supervise_answers.py:1,66,132 | cite r77 (retired in spec) | comment only; r163 is live | none | read |

No function reads the old scenarios' text: a search of scripts/ for r159|r168|r163|r92|r104|r77 found only the comments above, and a search of tests/ for "Deprecated for" hit only the features-tool tests, which use their own fixtures (tests/scripts/test_features_scenarios.py, test_features_deprecating.py), not supervision.feature. So no code rows beyond comments.

## 3. Tests the requirements make impossible to keep

None found. The requirements r159 and r168 already hold in code, so no test asserting their current behaviour breaks. Retiring a scenario only removes its generated test (test_supervision.py:61 `scenarios("supervision.feature")`); no hand-written test names a removed scenario (search of tests/ for the three titles, by search: only the feature file).

Checked and found sound (by search, not run):
- tests/scripts/test_supervise_change.py:14, 32, 50 call `Changes.write_proposals` and assert the per-capability split; the code is unchanged, so they hold.
- tests/scripts/test_bound.py:13-27 runs `features bindings --unbound` on features/supervision.feature; removing scenarios leaves no unbound scenario. Not run.

## 4. The file set

- features/supervision.feature: delete the three deprecated scenarios named in Retires: the outline at lines 1301-1318 (@r77, Retires bullet 1, see conflict A), lines 1474-1483 (@r92, bullet 2), lines 1706-1716 (@r104, bullet 3). File is 1961 lines; not Python, so no size limit applies. Found by read.
- Step modules tests/scenarios/supervision_*_steps.py: unchanged; steps used only by the removed scenarios may become unused, which pytest-bdd does not fail on. Not in the file set unless a check (features bindings) says otherwise. Found by read.

Modules on the change's path, edited or not (line counts by wc; room under 300):
- scripts/supervise_change.py: 140 lines, room 160 (writes r159's proposals; not edited).
- scripts/supervise_rounds.py: 274 lines, room 26 (calls write_proposals at line 205; not edited).
- scripts/supervise_brief.py: 216 lines, room 84 (gate brief, r168; not edited).
- tests/scripts/test_supervise_change.py: 63 lines (not edited).
- tests/scenarios/test_supervision.py: 268 lines, room 32 (binds supervision.feature; not edited).

Size check: `tools size --limit 300` printed nothing (no tracked Python file over 300).

## Conflicts for the planner (both readings)

A. Retires bullet 1 names the r163 outline (supervision.feature:1302). Its replacement r163 is accepted by w223 (`.shop/work/i46/w223.md:7`), not w226 (accepts r159, r168). Reading 1: keep bullet 1 as drafted; r73 names "a requirement the work-item accepts", so this reads against r73. Reading 2: drop bullet 1; w223 retires it.

B. features/supervision.feature:1484 (@r92, "Deprecated for: removal") is not named by Retires. Reading 1: leave it (as drafted). Reading 2: add it to Retires; r123/r73 name only replacement scenarios, so it is outside them.

C. Duplicate: `.shop/work/i46/w224.md:7` also accepts supervision#r159 and supervision#r168, the same accepted requirements as w226. Both would draft the same retirements.

Scratch directory `.shop/scratch/1-research/` is untracked in the checkout but `git status --porcelain` printed nothing at the end (ignored).
