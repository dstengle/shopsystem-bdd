# Review of w241 (supervision#r212, supervision#r213)

**Verdict: DONE.** No Critical finding, nothing triaged fix now.

## Commits reviewed

- 153518ea "supervision r212 r213: bare-status withdrawn Given; retire deprecated r9 and r105 scenarios"
  (the brief's `Commits:`, the same commit as the implementer's result lists). Diff: `features/supervision.feature` −26 lines, `tests/scenarios/supervision_proposal_steps.py` +9 lines. No production code changed.
- Suite taken from the brief's record: 1086 passed, 0 failed at 153518ea. The report's start figure was 1089; the 3 fewer are the retired r9 scenario (1) and the two examples of the retired r105 outline (2).

## Changes under features/

- Removed `@r9 @deprecated` scenario "when every work-item is green or withdrawn … (deprecated)": listed under the work-item's Retires (supervision @r212). Allowed.
- Removed `@r105 @deprecated` outline "an initiative whose work-items are <work-items>, its delivery otherwise closed, <set> (deprecated)" with its two examples: listed under Retires (supervision @r213). Allowed.
- Nothing else under `features/` changed (checked the full diff).

## Removed and weakened tests

Searched the diff for removed test functions, parametrize cases, assertions, skip/xfail, and removed or rewritten scenarios/examples.
- Only the two retired deprecated scenarios above (r9: proved `work run` exits 0 printing statuses when all work-items are green/withdrawn and no asker-turn request; r105: proved done only with a green work-item). Both are the Retires section's and their replacements (r212 scenario, r213 outline) cover the same plus the proposal condition. The plan's "Tests the decisions break" says none other; none other found.
- No step definition removed or changed; one step added.

## Allowances

The report's `## Tests changed under an allowance` is "none"; the diff touches no existing test. Nothing to verify.

## Cannot verify

- That r212's scenario was green before the work (report and plan say so); I did not rerun it, the brief's suite record shows it passing at 153518ea (not in the expected-failure list).

## Findings

None at Critical, Important or fix now.

- **Minor / drop** — `tests/scenarios/supervision_proposal_steps.py:125-131`: the new `proposal_withdrawn` step repeats the frontmatter template of `proposal_in_status` (line 110) rather than widening that step's pattern with an optional clause. The plan (decision 2) left either open; the `$` anchor and the existing step's required ", its …" clause keep the bindings unambiguous, and `tools size` reports the file (213 lines) under the limit. Polish only.

Verified risk: that the bare `withdrawn` Given could collide with the step at line 21 (`p1 is formulated…`) or line 110 (`…, its adds|changes naming …`): the line-110 pattern requires a comma clause, line 21 requires "formulated", so the new `$`-anchored pattern binds only "i1's capability-proposal p1 is withdrawn" (feature line 1895's example).

Code no line asks for: none; the commit adds only a test step serving r213's outline.

## tools

- `tools check --base c53a7c25`:
  - ruff: 28 hits; the two in the touched file (`supervision_proposal_steps.py:102`, `:146` RUF100 unused `noqa: E731`) are pre-existing (lines 102 and 137 at base, the latter shifted by the 9 added lines); none in the added lines. The rest are in files the commit did not touch (`.shop/work/...` scratch scripts, other tests).
  - vulture: `tests/scenarios/work_queue_status_steps.py:100` unused `notes`, not touched by the commit.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: prints nothing; no file over.

## Commands run

- `git show --stat 153518ea`, `git show 153518ea`
- `cat` of plan.md, report.md, result.json (3-implement)
- `sed -n 95,125p tests/scenarios/supervision_proposal_steps.py`; `sed -n 1880,1900p features/supervision.feature`
- `grep` for proposal Given patterns and feature uses; `grep -n "r212\|r213" spec/capabilities/supervision.md`
- `git show c53a7c25:tests/scenarios/supervision_proposal_steps.py | grep -n "noqa: E731"`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base c53a7c25e23bac68cae83b147c9dd66a2e6c6227`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `wc -l tests/scenarios/supervision_proposal_steps.py`; `git status --short`
