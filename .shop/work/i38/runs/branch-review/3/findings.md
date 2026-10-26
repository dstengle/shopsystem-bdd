# Branch review 3 of i38 (re-review after the fix work-item w201)

**Verdict: DONE.** There is no Critical finding and none triaged fix now. Every check was run here at HEAD `e913fd6f` and passed.

Review 2's fix-now finding is fixed. That finding was that the formulate check asked guarantees capabilities for scenarios, so a proposal on one never became `formulated`.
- `unformulated` now skips every id whose capability has `group: guarantees`.
- A new row of the r132 outline pins this, and that row was red on the code before the fix.

Review 2's finding 3 (ruff I001 at `supervise_rounds.py:7`) is fixed too. Review 2's other findings are carried as observations, unchanged.

## Range and work-items

- **Range:** `50a40103..e913fd6f`. Base is the commit that added i38's `initiative.md`, and HEAD is `e913fd6f work: w201 done -> green`.
  - Reviews 1 and 2 covered `50a40103..922f5f6c` (findings in `.shop/work/i38/runs/branch-review/{1,2}/findings.md`).
  - This review reads the whole diff and looks most closely at `50e4c9ac..HEAD`.
- **w199** (green): content commits `be4e1c7c`, `36c7061f`, `e17b2b0f`, `a853a2ea`, `9052628d`, `1eea53ac`. These are unchanged since review 1.
- **w200** (green): `1e0eabf6`, `5e486d94`, `5b198dc9`, `684f1409`. These are unchanged since review 2.
- **w201** (green, the fix work-item from review 2's findings). It had two claims:
  - The first claim, `d3cd55f0..4e867bd6`, ended in a hand-back that asked for the scenario.
  - The second claim, `773c0199..2c2171fe`, holds `d0d62cdd` (import order) and `dcba3f4a` (the guarantees skip, the shared reader and the new Given). `d0d62cdd` is dated 22:48, during the first claim (it was the implementer's `32a16402`). When the branch was merged it was rewritten onto the second claim, with the same content.
- **Commits in the range that belong to no work-item:**
  - since review 2: `50e4c9ac` (review 2's own commit), `6941b590` (`work add`) and `7b081400` (a feature-formulator hand-back that adds the r132 guarantees row, made while w201 was awaiting-answer);
  - the ones reviews 1 and 2 listed.

  See Finding 4.

## Suite

`Suite: 947 passed, 0 failed at e913fd6f in 28.0 s` (1 skipped, 56 subtests passed; pytest reports 27.66 s, and `date` measured 27.96 s from start to end).

- **Parallel:** yes. `pytest.ini` gives `addopts = -n auto -m "not fixture"`.
- **In-process:** no. The step definitions start `scripts/work run` as a subprocess, with `tests/scripts/stub_claude.py` standing in for `claude`.
- The suite is under 60 s, so this is not a finding.

## Checks

| check | result |
|---|---|
| w201's check: `python3 -m pytest -q -rfEx -p work_items --work-item w201 --whole-suite` | 947 passed, 1 skipped, 0 failed (26.93 s) |
| w201's scenarios: `python3 -m pytest -q -p work_items --work-item w201` | 209 passed, 1 skipped, 0 failed |
| w200's scenarios: `--work-item w200` | 209 passed, 1 skipped, 0 failed |
| w199's scenarios: `--work-item w199` | 209 passed, 1 skipped, 0 failed. The `--whole-suite` checks of w199 and w200 are the suite run above. |
| w201's red-green | **Verified.** I ran `git show 773c0199:scripts/supervise_outputs.py` (the code before the fix) through `unformulated(tmp, ["steady#r4"])`, with `steady` as a guarantees capability, and it gave `['steady#r4']`. So the new row would put p1 into awaiting-answer, which is red. At HEAD, `pytest tests/scenarios/test_supervision.py -k "guarantees or formulate"` gives 16 passed. |
| `tools check --base 50a40103`: **ruff** | 11 errors, exit 1. **None is from w201.** The I001 at `supervise_rounds.py:7` is gone, so there is one fewer than review 2's 12. The 11 are: 8 in the committed round scripts under `.shop/work/i38/runs/supervision/` (Finding 5); `tests/scenarios/test_supervision.py:14` I001 (already present at Base); and `tests/scripts/stub_claude.py:195-196` FURB167 (on lines the branch did not touch). |
| `tools check`: **vulture** | clean |
| `tools check`: **import-linter** | "the project states no import contracts". There are no contracts to read and nothing to read in their place. |
| `tools size --limit 300` (the limit CLAUDE.md gives) | prints nothing. The files w201 touched have 73, 150, 128 and 198 lines. |
| `features deprecated` | 5 scenarios, each "for: removal": `features/supervision.feature:63-64` @r3 "a worker's outcome DONE makes the work-item's transition to its next status"; `:89-90` @r5 "an implementer's DONE whose <tests> fail ..."; `:332-333` @r16 "a researcher's DONE with questions ..."; `:1389-1390` @r112 and `:1398-1399` @r113 (the formulate round's questions). These are review 2's Finding 8, unchanged. Being for removal, none has a replacement, so none has a replacement whose work-item is green. |
| `features bindings` | "every binding names a scenario" |
| Dry run against real run, randomized | Not applicable. The system has no dry-run mode of an operation. The only `--dry-run` in `scripts/` is `git push --dry-run`, which is a check git provides before a push. |

## Removed and weakened tests

**Searched for:**
- in `git diff 50a40103 HEAD -- tests` and `git diff 50e4c9ac HEAD -- tests features`, deleted lines with `assert`, `def test`, `skip`, `xfail`, `parametrize`, `Scenario` or an Examples row;
- `git diff -w 50e4c9ac HEAD -- features tests`.

**Since review 2:** none removed or weakened.
- `git diff 50e4c9ac HEAD -- tests` deletes no line. The only change is one new `@given`, `guarantees_then_answered_proposal` (`tests/scenarios/supervision_session_faults_steps.py:98-103`). It composes the existing `capability` and `answered_proposal` helpers.
- Under `features/`, `git diff -w` shows a single added row (`features/supervision.feature:945`). Every other changed line of `7b081400` is the table realigned, with no other change.

**Across the branch:** the four deleted `assert` lines are all in `e17b2b0f` (w199). They are in the step definitions `apply_was_started`, `no_transition_after_apply` and `names_formulate_without_result`, which bound only retired, deprecated scenarios listed under w199's Retires. Review 1 lists them, and that list stands:
- 16 retired scenarios;
- the removed step definitions;
- the r131 work-item-only outline that w200 retired, all four of its rows kept in the replacement.

## Allowances

| report | test | kind | holds? |
|---|---|---|---|
| w201 3-implement | none | - | Agrees with `d0d62cdd`, which touches no test. |
| w201 4-implement | none | - | Agrees with `dcba3f4a`. Its test change is an added Given and changes no existing assert, expected value or case. |
| w199's five rows, w200's four rows | - | setup | Verified by reviews 1 and 2. Nothing of them changed after them. |

## Cannot verify

Nothing. Every check above was run here at HEAD `e913fd6f`.

## Findings

No finding is Critical, and none is triaged fix now.

### 1. Minor, w201, observation: the r132 line does not carry the guarantees exception that the code and its new row make (spec/capabilities/supervision.md:33; scripts/supervise_outputs.py:52-69)

r132 says "a formulate round's scenario for each requirement its proposal adds or changes" and names no exception. The exception rests on design-decision 0065 (workflow-capabilities-are-guarantees), which supervision `rests_on`, and is pinned by the new r132 row at `features/supervision.feature:945`.

This is not code no line asks for. The skip serves r83 and r132 read with a binding decision, as r56, r64, r65 and `model.lp` v15f already do.

- **Why it matters:** a reader of r132 alone gets a different answer from the system's.
- **Fix:** through integrating-a-proposal, add "... that is not of a guarantees capability" to r132, as r56 and r64 say it.

### 2. Minor, w201, observation: `is_guarantees` reads only the exact line `group: guarantees` (scripts/supervise_outputs.py:45-49)

A quoted value (`group: "guarantees"`) or a trailing space is read as not guarantees. Such a proposal would then be asked for a scenario again. This reading is unchanged from the one `work_items.guarantees` had before, now shared, and plan section 5 names it as an open case.
- **Reproduction:** in a probe on a temporary `spec/capabilities/{a,b,c}.md`, `[is_guarantees(tmp, c) for c in "abc"]` gave `[False, True, False]` for the quoted, CRLF and trailing-space forms. CRLF is read correctly, because `read_text` takes universal newlines.
- **Present state:** `grep -rn "^group:" spec/capabilities/` shows only the plain form. All 11 guarantees capabilities read as guarantees (code-research, delivery, formulation, planning, red-green, review, role-boundaries, spec-consistency, spec-integration, spec-migration, trials), and none of them has a feature file.
- **Fix, if wanted:** read the frontmatter as key/value pairs with the value's quotes and spaces stripped. `model_parse` reads the same frontmatter for v15f.

### 3. Minor, w201, observation: the pytest plugin now imports a `work run` module for a spec reading (scripts/work_items.py:21, :139)

- `work_items.guarantees` now calls `supervise_outputs.is_guarantees`. Plan decision 2 chose this so that `work run` does not import pytest, and it removes a duplicate reader.
- But reading a capability's group is a reading of `spec/capabilities/`, not "what a stage's result must give". That concern belongs to neither `supervise_outputs.py`'s module-map row nor `work_items.py`'s.
- **Fix:** a small module (for example `scripts/spec_group.py`, with a row in the module map) that both import. It is complete when `grep -n "group: guarantees" scripts/*.py` finds that module only (`model.lp` aside).

### 4. Minor, none (i38's run), observation, carried from reviews 1 and 2 (finding 6) and extended: commits outside any work-item or round

`7b081400` is a feature-formulator hand-back made between w201's `claimed -> awaiting-answer` (`4e867bd6`) and its answer (`bb5bf39b`). It is correct: it adds one row, and the rest of its change is whitespace realignment (`git diff -w` shows one added line).
- **Reproduction:** `git show --stat 7b081400 e9cfc7ff bf58a9b3 46b35719 33ba1e88 5d6c49ad 8c1d9d51`.
- **Fix:** as in review 1: hand-backs through a formulate round, and `work` commands for accepts and Retires.

### 5. Minor, none (the proposal's rounds), observation, carried from review 2 finding 7: committed round scripts fail ruff

8 of the 11 ruff errors are in `.shop/work/i38/runs/supervision/{2-apply/merge.py,3-formulate/deprecate.py,4-formulate/splice.py}`.

### 6. Important, i38 (the proposal's apply round `4be48031`), observation, carried from review 2 finding 5: design-decision 0039 still guards on `DONE`

`grep -c DONE spec/decisions/0039-work-item-lifecycle-as-run.md` gives 6. r133 says "make no transition from the outcome". No decision supersedes 0039, and the branch did not touch `spec/` after review 2.

This is not code, so it is triaged as an observation, as in reviews 1 and 2. The fix is a superseding decision.

### 7. Minor, w200, observation, carried from review 2 findings 2 and 4

- **Ranges.** `thing#r1-r3` is always lacking.
- **Gherkin synonyms.** `Scenario Template:` and `Example:` are not read by `supervise_outputs.scenario_ids` (`scripts/supervise_outputs.py:29-42`).
- **Changed requirements.** A changed requirement's old scenario still satisfies the formulate check.

For a guarantees capability, a range id is now skipped by its capability.

### 8. Minor, w199 / the proposal, observation, carried from review 2 findings 8 and 9

- `features deprecated` lists 5 "for: removal" scenarios, and nothing retires them.
- q8's resolution names the removed `supervision#r113`.
- There is no intake or implementer-commit output check.

## Shape

CLAUDE.md is checked rule by rule and module-map row by row, for what w201 touched.

**Rules:**
- **Size limit, 300 lines:** met. `tools size --limit 300` prints nothing. `supervise_outputs.py` has 73 lines, `work_items.py` 150, `supervision_session_faults_steps.py` 128 and `supervise_rounds.py` 198.
- **"A new concern gets a new module and a row here":** partly met. The guarantees reader is placed in `supervise_outputs.py`, whose row is the stage outputs (Finding 3).

**Module-map rows:**
- `scripts/supervise_outputs.py`: met for `unformulated`'s skip (`:61-62`). See Finding 3 for `is_guarantees` (`:45-49`).
- `scripts/work_items.py`: met. It is still the `--work-item` plugin, and `guarantees` (`:134-139`) keeps its own root resolution.
- `scripts/supervise*.py` (rounds): met. `supervise_rounds.py:10` has only the import reordered.
- `tests/scenarios/`: met. The new Given is in `supervision_session_faults_steps.py`, the module that binds the r131/r132 outlines' other Givens.

**Code no scenario reaches:** vulture is clean, and every binding names a scenario. `work_items.py` still uses `re` (lines 40-83).

**Code no line asks for:** none. The guarantees skip serves r83 and r132 read with 0065 (Finding 1), and the shared reader is mechanism.

## Coupling

- **Plugin scripts on PYTHONPATH:** new in w201, and internal to the plugin. `work_items`, loaded by `-p work_items`, now also needs `supervise_outputs` importable. `supervise_worker.with_scripts` (`:77-82`) puts the scripts directory *last* on PYTHONPATH. A consumer repository with its own top-level `supervise_outputs` module would therefore shadow it, as it already could shadow `work_items`. This repository's `conftest.py:7-10` appends the same directory. It is stable while both modules ship together. Prepending the directory, or giving the plugin a package namespace, would close the shadowing.
- **Claude Code CLI's JSON result:** unchanged since review 1. `how_ended` reads the documented `subtype`, `num_turns` and exit code.
- **Gherkin, as pytest-bdd reads it:** unchanged since review 2 (Finding 7).
- **pytest-bdd on pytest internals:** 542 warnings per run, with `PytestRemovedIn10Warning` among them. Pinning `pytest<10` would make it stable.

## Observations

1. The r132 line lacks the guarantees exception (Finding 1). See `sed -n 33p spec/capabilities/supervision.md` beside `features/supervision.feature:945`.
2. Only the exact group line is read (Finding 2). A probe gave `[False, True, False]` for quoted, CRLF and trailing-space frontmatters.
3. The spec reader sits in a stage-output module (Finding 3). `grep -n "from supervise_outputs" scripts/work_items.py` finds line 21.
4. Commits outside work-items (Finding 4). `git show --stat 7b081400`, and `git diff -w 50e4c9ac HEAD -- features` shows 1 added line.
5. Committed round scripts fail ruff (Finding 5). `tools check --base 50a40103` gives 8 errors under `.shop/work/i38/runs/`.
6. 0039 still guards on DONE (Finding 6). `grep -c DONE spec/decisions/0039-work-item-lifecycle-as-run.md` gives 6.
7. Ranges, synonyms and changed requirements (Finding 7). See review 2's reproduction.
8. Deprecated-for-removal scenarios, q8, and no intake output check (Finding 8). `features deprecated` lists 5.
9. Review 2's fix-now is verified fixed. At HEAD, `unformulated(root, ["planning#r1", "review#r2", "supervision#r132", "supervision#r3", "supervision#r999", "term/x", "nosuch#r1"])` gave `['supervision#r3', 'supervision#r999', 'nosuch#r1']`. The code before the fix gave `['steady#r4']` on a guarantees `steady`.
