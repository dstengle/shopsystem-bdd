# Review of w231 (supervision#r187)

**Verdict: DONE.** No Critical finding and nothing triaged fix now. The commit adds only the step definitions the r187 scenario lacked, plus their import. It changes no production code, no `features/` file and no existing test.

## Commits reviewed

- `afc4aa728368e474832b86eba156e1002466367f`: "supervision r187: steps for an integrate round merging ids into another capability's proposal" (from the brief's `Commits:`).
  - The implementer's result lists `4d09af70`. `git diff 4d09af70 afc4aa72 -- tests` is empty, and the message, author and date are the same, so `afc4aa72` is `4d09af70` as `work run` merged it. This is no finding.
- Files: `tests/scenarios/supervision_merge_steps.py` (new, 39 lines) and `tests/scenarios/test_supervision.py` (+1 import). Both are in the work-item's `fileset`.

## Removed and weakened tests

None. I looked for deleted lines in `tests/`, removed `assert`s, parametrize cases, and added skips or xfails. The diff is 40 insertions and 0 deletions, so there is nothing to compare. The existing `... on thing` step (`supervision_formulate_steps.py`) is untouched. The new patterns cannot match the single-capability lines at `features/supervision.feature:1075` and `:1161`, because the new Given needs the line to end in "on other".

## Allowances

The report's `## Tests changed under an allowance` says "none". That holds: no existing test changed.

## Cannot verify

- The report's red run (the `StepDefinitionNotFoundError` on the p2 Given). The research run reported it, and I did not rerun it at the base. It is consistent with the plan's notes, and with the base suite record, which lists this scenario as failing.
- The whole suite: per the brief, I took it from the suite record (1067 passed, 0 failed at afc4aa72, only the known `test_requests.py` expected failures).

## Findings

1. **Minor, drop**: `tests/scenarios/test_supervision.py:14`, ruff I001 (import block un-sorted).
   - What is wrong: the block was already out of order at the base (`supervision_branch_steps` before `supervision_answers_steps`, `supervision_review_steps` before `supervision_reintegrate_steps`). The new `supervision_merge_steps` line sits in its correct alphabetical place. `check --base` reports it only because the commit touched the file.
   - Why it matters: it is lint noise on a touched file, and it was not introduced here.
   - Fix: `ruff --fix` on that file, in whatever work next touches it.
2. **Minor, observation**: `tests/scenarios/supervision_merge_steps.py:17-21`, the p2 Given.
   - What is wrong: its `adds`/`changes` groups take one `\S+` token and are written verbatim into `[...]`. Its removes are fixed to "nothing" (`removes: []`). A future line naming two ids ("other#r1 and other#r7") or "nothing" for adds would not match, or would write `[nothing]`.
   - Reproduction: none needed. No feature line uses another form today (`grep -n "capability-proposal p2, for" features/*.feature` gives only line 1523).
   - Why it matters: it is hardening for later scenarios only.
   - Fix (optional): parse the groups with `names()`, as the Then does.
3. The p2 Given also writes `spec/capabilities/other.md`. This is setup that r107 requires: a change list naming a capability that neither spec nor drafts hold is refused. It is not behaviour that no line asks for, and the report states it. This is no finding.

Production behaviour: the plan and the report say `Changes.write_proposals` / `merge_lists` (`scripts/supervise_change.py`) already did the merge, so no production code changed. The scenario passing in this checkout confirms that r187 holds through `work run`. Nothing contradicts a Behaviour line or Purpose.

## Checks

- `tools check --base 156d2b2b` (the ready -> claimed commit):
  - ruff: 1 error, I001 at `tests/scenarios/test_supervision.py:14` (pre-existing order, finding 1).
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: printed nothing (no file over the limit).

## Commands run

- `git show --stat afc4aa72`, `git show afc4aa72 -- tests features scripts`, `git log --oneline -5 afc4aa72`
- `git show --stat 4d09af70`, `git diff 4d09af70 afc4aa72 --stat -- tests` (empty)
- `sed -n 1515,1532p features/supervision.feature`; `grep -n "def entry" -A12 tests/scenarios/supervision_formulate_steps.py`
- `grep -n "integrate round for p1 gives DONE with a change list" features/*.feature`; `grep -n "p2's adds name\|capability-proposal p2, for" features/*.feature tests/scenarios/*.py`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 156d2b2b`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `python3 -m pytest -q -W ignore tests/scenarios/test_supervision.py -k "... or integrate"`: 1 passed
- `git show 156d2b2b:tests/scenarios/test_supervision.py > .shop/scratch/w231-4-review/base_test_supervision.py` (scratch probe of the base import order)
