# Review of w180 (formulation#r23)

**Verdict: DONE_WITH_CONCERNS.** The diff does what r23 asks: the interpreter is `python3 -m pytest`. But the new rule for selecting the old scenario by name gives the wrong name for most titles. The skill's next bullet then reads "not collected" as permission to replace or remove the scenario. That way a passing scenario can leave the suite, which r4 forbids. One Important finding, triaged fix now.

## Commits reviewed

- Claim commit: `225d3ed2 work: w180 ready -> claimed`. The branch `work/w180` is gone, so these are the commits between the claim commit and `5d20b71e work: w180 claimed -> done` on HEAD, less `work run`'s own commits.
- One commit is w180's: `75cd7fda formulating-features: run an old scenario alone with python3 -m pytest, selected by test name (formulation#r23)`. It changes 1 line of `skills/formulating-features/SKILL.md`.
- The implementer's results list `a4fd9482` (stage 3), `06496c00` (stage 4) and `be7b9477` (stage 5). These are rebases of the same change: the `+`/`-` lines of all four commits have the same md5 (`c8aecd69…`). No difference.
- The other commits in the range (w181's, branch reviews, `work add`) belong to other work-items.

## Removed and weakened tests

None. The commit touches only `skills/formulating-features/SKILL.md`: no file under `tests/`, `features/` or `scripts/`. Searched with `git show --stat 75cd7fda`.

## Allowances

The report's `## Tests changed under an allowance` is "none" in all three stages. Nothing to check.

## Cannot verify

- **Whether the formulate round inherits a `--work-item` filter.** My session's environment deselects every scenario by default. `python3 -m pytest --co -q -n 0 tests/scenarios/test_work_queue.py` gave `no tests collected (69 deselected)`, also with `-o addopts=""` and with `-m ""`. Adding `--work-item ""` collected them (`202 tests collected` for test_supervision.py). This points to an inherited `--work-item` option, probably in `PYTEST_ADDOPTS` (I was not allowed to run `env` to confirm). The research notes saw the same thing (P1: 143/877, every scenario deselected).
  - If `initiative-round` formulate sessions run with the same environment, every old scenario is "not collected" when run alone. The skill would then replace every passing scenario instead of deprecating it.
  - This is not w180's change, but it decides whether the skill's step 4 can work at all under `work run`.
- **Behaviour on real batches.** formulation is `group: guarantees`, and r23 has no scenario. Nothing in the suite checks the skill text.

## Findings

### F1. Important, fix now (w180): the derived test name is wrong for most titles, and "not collected" then removes a passing scenario

- **Where:** `skills/formulating-features/SKILL.md:26`.
- **What is wrong:** The skill says the test name is the title "lower case with underscores". pytest-bdd also drops every character that is not a letter, digit or space: hyphens, apostrophes, slashes and backticks. For example, the title "a change list naming a capability that neither spec/capabilities/ nor the round's drafts have gives no capability-proposal for it, and `work run` exits with an error naming it" becomes `test_a_change_list_naming_a_capability_that_neither_speccapabilities_nor_the_rounds_drafts_have_gives_no_capabilityproposal_for_it_and_work_run_exits_with_an_error_naming_it`.
- **Reproduction:**
  - `python3 -m pytest --co -q -n 0 --work-item "" -k "a_change_list_naming_a_capability_that_neither_spec_capabilities_nor_the_round_s_drafts_have_gives_no_capability_proposal_for_it_and_work_run_exits_with_an_error_naming_it" tests/scenarios/test_supervision.py` gives `no tests collected (202 deselected)`.
  - The same command with pytest-bdd's real name gives `1/202 tests collected`.
  - 370 of the 470 `Scenario:` titles in `features/*.feature` contain such a character.
- **Why it matters:**
  - The skill's next bullet says: "It fails or is not collected … replace or remove it as before." A round that follows the rule literally collects nothing for a scenario that passes today, and then replaces or removes it. That contradicts formulation#r4 (keep a passing old scenario, deprecated) and loses the test.
  - The new "check with `--collect-only` that one test is collected" does not say what to do when the count is zero or more than one. Zero matches "not collected" exactly.
  - The `"<its node id>"` form has the same derivation problem.
- **Fix:** In step 4, say how to get the real name:
  - pytest-bdd lower-cases the title, drops every character that is not a letter, digit or space, then puts underscores for the spaces, with the `test_` prefix.
  - Better: find the node id with `python3 -m pytest --collect-only -q | grep` on a distinctive word of the title.
  - Say that a selection collecting no test, or more than one, is not a verdict. The round fixes the selection, or stops (r22). Only a run of the one collected test decides between r4 and r5.

### F2. Minor, observation (w180): `-k` matches substrings, so the check collects more than one test with nothing said about what to do

- **Where:** `skills/formulating-features/SKILL.md:26`.
- **What is wrong:** `-k test_x` also selects `test_x_deprecated` and any longer title that starts with the same words. It also selects every example of an outline. The plan's section 5 left outlines and titles shared by several files unchosen, and the skill says nothing when more than one test is collected.
- **Reproduction:** `-k "a change list naming a capability"` (with spaces) collected `202 tests`, the whole file. That confirms the research's D1 for the spaced form. I ran no probe for the prefix case.
- **Fix:** Covered by F1's fix: select by node id, and treat a count other than one as no verdict.

## Checks

- **`tools check --base 225d3ed2`:**
  - ruff: 4 errors, in `scripts/supervise_analysis.py:4`, `scripts/supervise_brief.py:89`, `tests/scenarios/supervision_proposal_steps.py:96` and `tests/scenarios/test_supervision.py:14`. None is in a file w180's commit touched; they come from the other work-items' commits in the range.
  - vulture: clean.
  - import-linter: the project states no import contracts.
- **`tools size --limit 300`:** printed nothing. No tracked Python file is over the limit, and w180 touched none.
- **features/:** unchanged by w180.
- **Code no line asks for:** none. The change is skill text serving r23 and r4/r5.

## Commands run

- `git log --format=%H -1 --grep="^work: w180 ready -> claimed$" work/w180` gave "unknown revision" (the branch is gone). The same without the branch gave 225d3ed2.
- `git log --format='%h %s' 225d3ed2..HEAD | grep -i -E 'w180|formulating-features'`
- `git log --format='%h %s' 225d3ed2..5d20b71e`
- `git show --stat 75cd7fda`; `git show 75cd7fda`
- `git show <c> --format= | grep '^[+-] ' | md5sum` for 75cd7fda, be7b9477 and a4fd9482
- `python3 -m pytest --co -q -n 0 [-m "" | -o addopts="" | --work-item ""] tests/scenarios/test_{supervision,work_queue}.py` (the deselection probes)
- `python3 -m pytest --co -q -n 0 --work-item "" -k <literal underscored | pytest-bdd name | spaced> tests/scenarios/test_supervision.py`
- `grep -h -E "^\s*Scenario( Outline)?:" features/*.feature | wc -l`, and the same with `grep -c` for titles with punctuation
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 225d3ed2`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
