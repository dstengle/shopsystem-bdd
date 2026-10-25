# review of w196

**Verdict: DONE.** No Critical finding and nothing to fix now. Two Minor observations.

## Commits reviewed

- The claim commit is `00964b0e` (`work: w196 ready -> claimed`). The branch `work/w196` is gone, so the commits are those from `00964b0e` to HEAD, less `ed893f5c work: w196 claimed -> done`.
- That leaves one commit: `45922c8e supervision: retire by the deprecated scenario's replacement (r73), draft the retire work-item (r123, r124)`. It is the one commit the implementer's result.json lists, so the two match.
- Files: `features/supervision.feature` (-20), `scripts/supervise.py` (+4), `scripts/supervise_draft.py`, `scripts/workqueue.py` (1 line), `tests/scenarios/supervision_proposal_steps.py`, the new `tests/scenarios/supervision_retire_steps.py`, and `tests/scenarios/test_supervision.py` (+1 import). Every file is in the work-item's fileset.

## features/

- The only change removes the two `@r73 @deprecated` scenarios that the work-item lists under Retires. They are "… lists under its Retires each deprecated scenario of a requirement it accepts (deprecated)" and "… whose changes name a range … (deprecated)".
- Their bindings went with them, and nothing else under `features/` changed.
- A grep of the worktree outside `.shop` finds no remaining reference to either title.

## Removed and weakened tests

I searched the diff for deleted `def`s, parametrize changes, `assert` lines removed or loosened, and skip or xfail added.

- `thing_feature_deprecated` (a Given in supervision_proposal_steps.py) was removed. It wrote features/thing.feature with two deprecated scenarios, tagged by their own @r. Only the two retired scenarios used it. Plan §4 lists it.
- `retires_listed` (a Then in supervision_proposal_steps.py) was removed. It proved that the drafted thing work-item lists "it used to wait" and neither "it used to answer" nor "it waits". Only the two retired scenarios used it. Plan §4 lists it.
- `retires_listed_by_replacement` is new. It binds a different Then text and asserts the old checks plus "it answers", so it is not a weakened rewrite.

No other test was removed or weakened.

## Allowances

The report lists none, which is right: the two removed steps served only the retired scenarios. Nothing to verify.

## Cannot verify

- The report's suite figures: 148 passed and 1 skipped for `--work-item w196`, and 365 passed for test_supervision plus tests/scripts. As told, I did not run the suite.
- That the removal was done with `features retire` and not by hand. The diff is a clean removal of exactly the two scenarios, which is consistent with it.

## Checks

- `tools check --base 00964b0e`:
  - **ruff**: 3 hits. They are workqueue.py:248 (I001, a local import inside `moved_to`), supervision_proposal_steps.py:102 (RUF100 noqa) and test_supervision.py:14 (I001 on the star-import block). All three are on lines the commit did not change, so they were there before. The import the commit added (`supervision_retire_steps`) sits in sorted order.
  - **vulture**: 1 hit, `base` unused at supervision_proposal_steps.py:66 in `drafted`, which the commit did not change. It was there before.
  - **import-linter**: no contracts.
- `tools size --limit 300`: no output, so no file is over. The touched files are supervise.py 275, supervise_draft.py 122, workqueue.py 294, supervision_proposal_steps.py 152 and supervision_retire_steps.py 114 lines.

## Risks checked

- **`deprecated()` resolves a replacement by title.** It uses `load`, `description` and `effective_tags` from features_gherkin. `effective_tags` includes Examples tags, and `Path(path).stem` gives the capability. A title found in no file, or in two, is skipped, as the report says. This is correct for every line.
- **The guard against drafting twice.** draft_retires skips every deprecated scenario already listed `- "<title>" (` under the `## Retires` of a work-item that is not withdrawn. A green retire work-item therefore does not loop the run. This is correct.
- **When pull_through drafts.** It drafts only when nothing was refused and every item is green or withdrawn. It then pushes and pulls again, before the review and the measure check. This matches r124.
- **The workqueue.add Retires line.** It now takes `(cap @tag)` from each entry's `cap#rN`. Its only callers with `retires` are the two in supervise_draft.py, and both pass `cap#rN`. This is correct.

## Findings

1. **Minor, observation (w196)**, scripts/supervise_draft.py:73-74
   - **What:** the retire work-item copies `accepts` (and `under`) from the last-drafted green holder. In scenario 1063 it accepts `other#r4` and is under `other`, which means it re-accepts a requirement that is already green. r123 names only the proposal it goes under.
   - **Why it matters:** the retire work-item's research and plan see an accepted requirement whose work is already done. `--work-item` also runs other#r4's scenarios for it.
   - **Fix:** none needed now; plan decision 5 chose this deliberately, mirroring r74, and the implementer raised the same concern. If it proves noisy, write a line on what a retire work-item accepts.
   - **Reproduction:** read scenario 1063 with lines 72-74. The drafted item has `part_of` …/p2, `under: other` and `accepts: [other#r4]`.
2. **Minor, observation (w196 accepts r73, but the code predates it)**, scripts/supervise_draft.py:117-119
   - **What:** the fix work-item for a kept branch review's findings (r74) is drafted with no `retires=`. r73 now reads "When `work run` drafts a work-item …", which covers every drafting. A fix work-item accepting a requirement whose replacement scenario has a deprecated predecessor therefore lists no Retires.
   - **Why it matters:** in practice r123's retire work-item picks those scenarios up later, so nothing is lost. No scenario covers this case and the commit did not touch this code.
   - **Fix:** if wanted, pass `retires=self.retires(accepts)` there. Note that r123's guard would then see those entries.
   - **Reproduction:** read lines 117-119; no `retires` argument is passed.

## Commands run

- `git log --format=%H -1 --grep="^work: w196 ready -> claimed$"` gave 00964b0e.
- `git log --oneline -5 work/w196` failed: the revision is unknown, the branch is gone.
- `git log --oneline 00964b0e..HEAD` and `git branch -a`
- `git show --stat 45922c8e`, then `git show 45922c8e -- scripts/` and `git show 45922c8e -- features tests`
- `sed -n 1015,1090p features/supervision.feature`
- `grep -n ... scripts/features_gherkin.py` (load, description, effective_tags, REQ_TAG, natural)
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 00964b0e...`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `wc -l` of the touched files
- `git diff 00964b0e HEAD --stat` of workqueue.py and test_supervision.py, plus `sed` of the lines ruff and vulture flagged
- A grep for the retired titles outside `.shop`: no matches
- `grep -n workqueue.add scripts/*.py` and `sed -n 100,122p scripts/supervise_draft.py`
