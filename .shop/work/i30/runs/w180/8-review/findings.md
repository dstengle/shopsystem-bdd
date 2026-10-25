# Review of w180 (formulation#r23), after the fix of review 6's F1

**Verdict: DONE.** Nothing is fix now and nothing is Critical. Review 6's F1 is fixed. Step 4 now gives pytest-bdd's naming, says to find the node id by collecting the tests, and treats a selection that collects zero tests or several as no verdict ("fix the selection, or stop (r22)"). A passing scenario can no longer be removed because it was not collected, so formulation#r4 holds. Two Minor findings remain, neither fix now.

## Commits reviewed

- The branch `work/w180` is gone, so the commits were taken from HEAD. The last claim is `ce37512e work: w180 ready -> claimed` and the last done is `5ee2e95a work: w180 claimed -> done`. Between them, the one w180 commit is `4f1d4641 formulating-features: derive the old scenario's test name as pytest-bdd does, and take no collection as a verdict (formulation#r4, r23)`. It changes 2 lines of `skills/formulating-features/SKILL.md`. The other commits in that range are `7109a88c` (branch review 5 of i26) and `ef803ad1` (i26 done), which are not w180's.
- The implementer's result (stage 7) lists `1a2b008e`. Its `+`/`-` lines have the same md5 as 4f1d4641's (`1996771b…`), and its message is the same. The result's summary leaves off the "(formulation#r4, r23)" suffix, but the commit has it. No difference.
- The earlier cycle's commit `75cd7fda` (1 line, the same file) was reviewed in 6-review. I re-read it here as the base of the fix.
- Files touched by w180 in all cycles: only `skills/formulating-features/SKILL.md`. Nothing under `features/`, `tests/` or `scripts/`.

## Removed and weakened tests

None. Neither commit (4f1d4641, 75cd7fda) touches a test file. I checked with `git show --stat`.

## Allowances

The report's `## Tests changed under an allowance` is "none". Nothing to check.

## Cannot verify

- **Behaviour on real batches.** formulation is `group: guarantees`. r23 has no scenario, and no test reads the skill text.
- **Whether formulate sessions inherit a `--work-item` filter.** 6-review raised this. My session also needs `--work-item ""` to collect scenarios. If formulate sessions inherit the filter, the collect-and-grep step finds nothing. Under the new text that means no verdict and a stop (r22), not a removal, so it is now safe, though it would stop rounds.

## Findings

### F1. Minor, observation (w180): the stated derivation drops underscores that pytest-bdd keeps

- **Where:** `skills/formulating-features/SKILL.md:26`.
- **What is wrong:** The skill says "every character that is not a letter, a digit or a space dropped". pytest-bdd drops non-word characters (`\W`), so it keeps `_`. 16 `Scenario:` titles in `features/*.feature` contain `_`.
- **Reproduction:**
  - The title is "a requirement or scenario using an avoided word is v_t1", in `features/design-model-check.feature`.
  - Collected, its test is `tests/scenarios/test_design_model_check.py::test_a_requirement_or_scenario_using_an_avoided_word_is_v_t1`.
  - The skill's rule gives `..._is_vt1`. `python3 -m pytest --co -q -n 0 --work-item "" -k test_a_requirement_or_scenario_using_an_avoided_word_is_vt1 tests/scenarios` gave `no tests collected (753 deselected)`.
- **Why it matters (little):** The same bullet says "Do not trust the derived name: find the node id with `--collect-only -q | grep`". It also says a collection of zero is no verdict. So the wrong name leads to a re-selection or a stop, never to a removal. r4 is safe.
- **Fix:** Say "every character that is not a letter, a digit, an underscore or a space". Or drop the derivation and keep only the collect-and-grep step.

### F2. Minor, drop (w180): the commit subject says the opposite of the text

- **Where:** commit 4f1d4641's subject, "take no collection as a verdict".
- **What is wrong:** The skill text says no collection is *no* verdict. The text is right; only the history is misleading.
- **Fix:** None now. Rewriting merged history is not cheap.

## Checks

- `tools check --base ce37512e`: ruff "nothing to check"; vulture "nothing to check"; import-linter "the project states no import contracts".
- `tools size --limit 300`: printed nothing. No tracked Python file is over the limit, and w180 touches none.
- `features/`: unchanged.
- **Code no line asks for:** none. The text serves r23 (`python3 -m pytest`), r4/r5 (the verdict) and r22 (stop).

## Commands run

- `git log --format='%H %s' -1 --grep="^work: w180 ready -> claimed$" work/w180` gave "unknown revision" (the branch is gone).
- `git log --format='%H %s' --grep=w180 HEAD`
- `git log --format='%h %s' dd5882ee^..5ee2e95a`; `git log --stat ce37512e..5ee2e95a`
- `git show 4f1d4641`; `git show --stat 4f1d4641 75cd7fda`; `git log -1 --format=%B 1a2b008e`
- `git show <c> --format= | grep '^[+-] ' | md5sum` for 1a2b008e and 4f1d4641
- `head -40 tests/scenarios/test_supervision.py`; `grep` on `conftest.py`; `cat pytest.ini`
- `grep -n` for r4, r5, r22 and r23 in `spec/capabilities/formulation.md`
- `grep -h -E "^\s*Scenario( Outline)?:" features/*.feature | grep -c "_"`
- `python3 -m pytest --co -q -n 0 --work-item "" tests/scenarios/test_supervision.py | grep speccapabilities` (the collect-and-grep form works: 1 node id)
- `python3 -m pytest --co -q -n 0 --work-item "" tests/scenarios | grep avoided_word_is_v`, and the same with `-k ..._vt1`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base ce37512e`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
