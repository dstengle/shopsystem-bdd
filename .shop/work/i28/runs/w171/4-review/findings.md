# Review of w171 (supervision#r102)

**Verdict: DONE.** No Critical finding, none triaged fix now. The change does what the plan says: `supervise_drafts` reads kept drafts at `<k>-integrate/drafts/round-<m>/spec/capabilities/*.md`, for every round of every integrate stage. Both @r102 scenarios pass.

## Commits reviewed

The branch `work/w171` is gone, so the commits were read from HEAD. They sit between `50bbc29d work: w171 ready -> claimed` and `666eb958 work: w171 claimed -> done`:

- `a414d2bd r102: read kept drafts where integrate rounds keep them (round-<m>)`: `scripts/supervise_drafts.py` (+6/-7) and `tests/scenarios/supervision_integrate_steps.py` (+19/-1).

This matches the implementer's `result.json` (`commits: [a414d2bd ...]`). The changed files are inside the work-item's fileset. Nothing under `features/` changed.

## Removed and weakened tests

None. What I searched for in the diff: deleted `def` lines, removed `assert` lines, parametrize changes, skip/xfail markers, and changed `@then` steps. The diff deletes one line in a test file. It is in the Given step `other_initiative` (line 149): the draft path `1-integrate/drafts/spec/capabilities/` became `1-integrate/drafts/round-1/spec/capabilities/`. No assertion or expected value changed. The deprecated @r102 scenario still asserts that the round is given thing#r4 and other#r1, and not thing#r1, r2 or r5. The plan lists this step under "Tests the decisions break" (decision 3).

## Allowances

- Deprecated @r102 scenario, step `other_initiative`, claimed as "setup … Interim". **Holds.**
  - Setup: the diff adds, removes or changes no `assert`, no expected value and no parametrize case. Only the fixture path changed.
  - Interim: the step was first committed in `55eea183`, after the base `4b7dca6c`. The test now matches plan decision 3.
  - The plan lists this test anyway, so it would not be a finding even without the allowance.

## Cannot verify

- The report's run figures ("144 passed, 1 skipped" for `--work-item w171`; "865 passed, 2 failed" at start). I did not run the whole suite or the work-item run. I ran only the two @r102 scenarios, and both passed.
- That every real integrate writer keeps its drafts under `round-<m>`. `supervise_brief.py:81` gives the writer `<stage>/drafts`, and the `round-<m>` level below it is the writer's own layout. The research notes found real drafts only under `round-1` (i25, i26). Nothing in the diff fixes that layout. The new reader depends on it, as the work-item's title says it should.

## Findings

1. **Minor, observation**: `scripts/supervise_drafts.py:19`, reading every round of a stage.
   - What: if a later round of one initiative drops an id that an earlier round drafted, the dropped id is still given, because the earlier round's draft is kept (r91).
   - Why it matters: the integrate round would avoid an id that no current draft holds. That is conservative: an id is wasted, but no collision results.
   - Status: plan decision 1 chose this. The report names it as an open question, and no line or scenario covers it.
   - Reproduction: by reading only, no probe. In a stage, `round-1/…/thing.md` adds r4 and `round-2/…/thing.md` does not; `added_by_others` still gives `thing#r4`.
   - Fix if wanted: read only the highest round of each stage. That needs a line first.
2. **Minor, observation**: `scripts/supervise_drafts.py:28-29`, "not yet applied" (r102) versus "spec/ does not hold" (the code).
   - What: the two differ for an id that spec/ holds but whose proposal is not applied.
   - Status: this predates the work-item (`55eea183`) and was not changed here. Named in the plan and the report. No reproduction run.

Already present, not from these commits: `tools check` ruff reports FURB167 (`re.M`) at `tests/scenarios/supervision_integrate_steps.py:107` and `:112`. Both lines are outside the diff's hunk (lines 146 onwards), so they were there before the commit.

## Risks verified

- Step-pattern collision (plan, open case 4): I grepped every `under \.shop/work/` Given pattern in `tests/scenarios/`. The new pattern requires `, started, whose capability-proposal`, which no other pattern matches. The old step at :144 requires `, started, whose kept drafts add`. Both scenarios ran and passed, so there was no ambiguity.
- Leftover callers of the removed `last_integrate`: grep of `scripts` and `tests` finds none.

## Tool results

- `tools check --base 50bbc29d`:
  - ruff: 2 FURB167 warnings, both already present (above).
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: no output, so no file is over the limit. The touched files have 32 and 188 lines.

## Commands run

- `git log --format=%H -1 --grep="^work: w171 ready -> claimed$" work/w171` → the branch is unknown, so I used HEAD.
- `git log --format='%h %s' -15`
- `git show --stat a414d2bd`, `git show a414d2bd`
- `grep -n "r102\]\|r91\]" spec/capabilities/supervision.md`, `grep -n -A12 "@r102" features/supervision.feature`
- `grep -n "under \\.shop/work/\|keeps a draft" tests/scenarios/*.py`
- `grep -n "drafts\|round-" scripts/supervise*.py`
- `git log --format='%h %s' 4b7dca6c..HEAD -- tests/scenarios/supervision_integrate_steps.py`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 50bbc29d`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `wc -l scripts/supervise_drafts.py tests/scenarios/supervision_integrate_steps.py`
- `grep -rn "last_integrate\|kept_drafts" scripts tests`
- `python3 -m pytest -q -p no:cacheprovider tests/scenarios/test_supervision.py -k "kept_drafts"` → 2 passed
