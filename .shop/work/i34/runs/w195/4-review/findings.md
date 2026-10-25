# Review of w195 (supervision#r122)

**Verdict: DONE.** No Critical finding and none triaged fix now. The commit does what r122 and its outline ask. There are four Minor findings: three observations and one drop.

## Commits reviewed

The branch `work/w195` is gone, so I took the commits between `23d63b30 work: w195 ready -> claimed` and `e1065200 work: w195 claimed -> done`, leaving out `work run`'s own `work:` commits:

- `f682b013` supervision r122: the whole suite expects red for scenarios a proposal adds or changes. It touches `scripts/work_items.py` (+21/-2), `tests/scenarios/supervision_proposal_steps.py` (+15) and `tests/scenarios/supervision_tests_steps.py` (+11/-1).

This is the one commit the implementer's `result.json` lists, so the commits and the result agree. Every file is inside the work-item's fileset. `supervise_merge.py` is in the fileset but was not edited; the plan marked that edit as a comment only.

## Removed and weakened tests

None. I searched the diff for:
- deleted `def test_`/step functions
- removed `assert` lines
- removed parametrize cases
- added skip/xfail marks
- changes under `features/`

The one change to an existing test is `counted_as`. Its body moved into `check_counted(repo, context, stage, counted)`, and `counted_as` calls it with stage `"merge"`. The record filter, the `len(records) == 1` assertion and the failing/expected check are textually the same, so it proves what it proved before. The plan lists no "Tests the decisions break" (none), and none is needed.

## Allowances

The report's `## Tests changed under an allowance` is "none". The commits agree: no existing test's asserts changed.

## Cannot verify

- The report says "Suite at start: 913 passed, 9 failed" and gives the green run `--work-item w195` as 154 passed, 1 skipped. I did not run the whole suite; `work run` runs it.
- The report says the `approved` rows reach the suite runs with p1 `awaiting-answer`, because the planned formulate round asks a question. It reads that way from the step code, but I did not trace the proposal's status in the run log.

## Findings

### F1 Minor: observation. `scripts/work_items.py:107-109`: the xfail reason is wrong for proposals
`open_` mixes proposals in with work-items. The reason then reads "expected: accepted by p1, neither green nor withdrawn", but a proposal neither accepts nor is green. This text shows in `-rx` output. The suite record holds only names (`supervise_merge.py` suite_record), so no count is wrong; only the message misleads. **Fix:** give each source its own reason text, e.g. "added or changed by p1, neither formulated nor withdrawn". The `expect_red` docstring (line 97) also still names work-items only, though the plan (§2) said to update it.

### F2 Minor: observation. `scripts/work_items.py:78-80`: a `merged` or status-less proposal counts as expected forever
Following r122's text and its outline row, any status other than `formulated`/`withdrawn` counts, and so does no `status:` line at all. That includes `merged`, a status `work run` never writes; `model_work.SETTLED` treats it as closed. This repository has 45 capability-proposals still `merged`, though decision 0065 says they become `formulated`. Their requirements cover spec-integration, formulation, red-green, review, delivery and others.

**Reproduction:**
- `grep -rl "^kind: capability-proposal" .shop/work | xargs grep -h -m1 "^status:" | sort | uniq -c` gave 113 formulated, 45 merged, 4 withdrawn.
- All 45 argue guarantees capabilities, which have no feature file (`ls features/`), so no scenario here is masked today.

In a consumer repository with a leftover `merged` proposal on a capability that has scenarios, every failing scenario of those requirements would be xfailed for good. The code follows the line: this is a spec question (researcher's Q1, settled by plan decision 2 from the accepted row), not a code fault. **Fix, if wanted:** a request to narrow r122 to the statuses `work run` writes (drafted, awaiting-answer, approved), or to migrate the `merged` leftovers to `formulated` as 0065 says.

### F3 Minor: observation. `tests/scenarios/supervision_proposal_steps.py:126-139`: the `approved` rows do not see `approved` at the suite runs
To keep p1 out of `formulated`, the step makes the formulate round ask a question. p1 then stands `awaiting-answer` when the suites run (the step's docstring and the report both say so). So the "approved" rows show the same behaviour as the awaiting-answer rows. The rule is a status blacklist, so `approved` would be expected too, and nothing is wrong today. Still, a later change to an allowlist that dropped `approved` would not turn these rows red. **Fix:** none cheap within `work run`'s lifecycle. The report names it; leave it as noted.

### F4 Minor: drop. `scripts/work_items.py:82`: `adds:`/`changes:` are read only as one-line `[...]` lists
A YAML block list would be ignored. Every proposal in this repository uses the one-line form (grep above), and `accepts:` is read the same way.

## Checks

- `tools check --base 23d63b30`:
  - ruff: 1 hit (`supervision_proposal_steps.py:118` RUF100). It predates the commit (`git show 23d63b30:...` line 118).
  - vulture: 1 hit (`supervision_proposal_steps.py:73` `base`). It predates the commit too.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: no output, so no file is over the limit. The touched files are 150, 168 and 218 lines.
- Focused run: `python3 -m pytest -q --tb=line -k "whole_suite_is_run" tests/scenarios/test_supervision.py` gave 10 passed.
- Code no line asks for: none. `proposals()` and the xfail serve r122; the step functions serve the accepted outline.
- Changes under `features/`: none.

## Commands run

- `git log --all --format='%H %s' --grep="^work: w195"`
- `git log --stat 23d63b30..e1065200`
- `git diff 23d63b30 f682b013`
- `grep -n` over `scripts/work_items.py` and the step module (helpers, `DIR`)
- grep over `.shop/work` for capability-proposal statuses, `adds:`/`changes:` and `argues:`
- `grep` over spec/capabilities and spec/decisions for `merged`; `sed -n 22,40p` of decision 0065
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 23d63b30...`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `wc -l` of the touched files
- `git show 23d63b30:tests/scenarios/supervision_proposal_steps.py | grep -n "noqa\|base"`
- `python3 -m pytest -q --tb=line -k "whole_suite_is_run" tests/scenarios/test_supervision.py`
