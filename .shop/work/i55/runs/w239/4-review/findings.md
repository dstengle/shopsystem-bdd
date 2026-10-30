# Review of w239 (requests r64)

**Verdict: DONE_WITH_CONCERNS.** The behaviour is right: `work list` prints each uncited observation with its date
(text and `--json`), `work status` no longer does, the r14 scenario is retired as the Retires section says, and no test
is removed or weakened. One Critical finding: the retire also deleted a line under `features/` that belongs to the
r64 scenario and not to the retired one (its `# formulates [r64]` provenance comment). The cause is how
`features retire` finds where a scenario ends. Restoring the line is a one-line fix.

## Commits reviewed

- `cae12e0c` work list prints uncited observations; retire the r14 status scenario (r64). This is the brief's `Commits:`.
  The implementer's result lists `49317acb` with the same message. `git diff 49317acb cae12e0c` over the four files
  the commit touches is empty, so `cae12e0c` is the same change after `work run` rebased it. No difference in content.
- Suite taken from the brief's record: 1087 passed, 0 failed at cae12e0c. The expected failures listed there are other
  work-items' and include no r64 scenario.

## Removed and weakened tests

What I searched for: deleted test functions and step definitions, removed scenarios, dropped parametrize cases,
assertions loosened, skips or xfails added, in the diff of `cae12e0c`. I also searched `tests/` for `uncited`,
`report=` and `"observations"` to find any test of `work status`'s observations.

- Scenario "status with no initiative prints, with its date, each observation no initiative's or request's source
  names (deprecated)" (@r14 @deprecated, features/requests.feature, was lines 468-478). It proved that `work status`
  prints the uncited observations with their dates and leaves out the cited ones. It was **removed**. The work-item
  lists it under Retires and the plan lists it under "Tests the decisions break", so it is allowed. It has no
  separate binding in tests/scenarios/test_requests.py (no hit for its name).
- Step definition `runs_status` ("the session runs `work status`", tests/scenarios/requests_show_steps.py:49). It was
  removed and replaced by `runs_list`. It is a step, not a test. Its only user in requests.feature was the retired
  scenario. The `work status` steps in work-queue.feature (lines 497, 514, 523) are bound elsewhere, and the suite
  record shows them passing.
- No other test was touched. The only `uncited` hits under tests/ are the model's `w_uncited_obs`, which this change
  does not affect.

## Allowances

The report's `## Tests changed under an allowance` says "none". No test changed outside the plan's list, so this holds.

## Cannot verify

- The report's red run (StepDefinitionNotFoundError before the change) and its green run
  (`--work-item w239`: 182 passed, 1 skipped). I did not rerun either. The brief's suite record agrees with them.

## Findings

### 1. Critical / fix now: a line under `features/` removed that the Retires section does not cover

- Where: features/requests.feature, before line 468 (`@r64`). The commit deletes `# formulates [r64] of spec/capabilities/requests.md`.
- What is wrong: the comment was added by the formulate commit `0e9fa09f` ("features: requests r64 formulated, r14's
  scenario deprecated"). It is the r64 scenario's provenance line; seven other scenarios in this file carry the same
  kind of line (lines 73, 89, 99, 110, 126, 137, 151, 478). The work-item allows only the removal of the deprecated r14
  scenario. Deleting this line is a change under `features/` that the Retires section does not cover.
- Why it happened: `features retire` (scripts/features_edit.py:125) removes the lines from `sc.start` to `sc.end`.
  `features_gherkin._parse` (scripts/features_gherkin.py:67) sets a scenario's `end` to the next scenario's first tag
  line. A comment line placed just before the next scenario's tags therefore counts as part of the retired block and
  is deleted with it.
- Why it matters: the r64 scenario's link back to its line is gone, and `features/` changed beyond what the work-item
  allows. No code reads the comment today (`grep formulates scripts/` shows only a code comment in model_facts.py:249),
  so behaviour and the suite are unaffected.
- Fix: put back `  # formulates [r64] of spec/capabilities/requests.md` directly above `  @r64`. Separately, as hardening of
  `features retire`, end a retired block before any comment lines that come right before the next scenario's tags.
  That is a tool change for another work-item.

### 2. Minor / observation: an observation with no `date:` line prints "None"

- Where: scripts/workqueue_list.py:53 and :78. `uncited` gives `None` as the date, and `listing` prints
  `observation <id> None` (JSON: `"date": null`).
- This behaviour is unchanged: the code was moved from workqueue_status.py as it was. r64 says "with its date", and
  every observation in the scenarios has a date. The implementer named this case among the open ones. It is hardening
  for an input no line names.
- Reproduction: I read the code only (the regex `(?m)^date: (\S+)` with a fallback of `None`). I did not run it.

No code the commits add lacks a line to ask for it. The `observations` JSON key and the text line serve r64 (decision 2
of the plan). Removing the observations from `work status` follows from r14 being retired. No Behaviour line asks
`work status` for observations any more (I grepped spec/capabilities for "observation").

## Checks

- `tools check --base c53a7c25`:
  - ruff: 28 findings, none in a file this commit touches. They are in `.shop/work/*/runs` scratch scripts and in
    other test modules.
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: no output. No tracked Python file is over the limit.
- workqueue_status.py still uses `re` and `Path` after `uncited` left it (lines 16, 20, 34, 85, 114, 130).

## Commands run

- `git show --stat cae12e0c`, `git show cae12e0c`, `git log --oneline -3 cae12e0c`
- `git show --stat 49317acb`, `git diff 49317acb cae12e0c --stat -- <four files>` (empty)
- `git log -S"# formulates [r64] of spec/capabilities/requests.md" -- features/requests.feature`, `git show 0e9fa09f --stat`
- `git diff c53a7c25 cae12e0c --stat -- tests features`
- `grep -n "formulates \[" features/requests.feature`, `grep -c` of the same over three feature files
- `grep -rn "runs .work status\|runs_status\|runs .work list" tests/ features/`
- `grep -n "r64\|list_prints\|status_with_no_initiative" tests/scenarios/test_requests.py` (no hit)
- Grep of `tests/` for `uncited|report=|"observations"`. Grep of `spec/capabilities` for `observation`. Grep of the repo,
  less `.shop/`, for status/observation mentions (no hit).
- Read scripts/features_edit.py `cmd_retire` and scripts/features_gherkin.py `_parse`.
- `python3 <Scripts>/tools check --base c53a7c25…`, `python3 <Scripts>/tools size --limit 300`
