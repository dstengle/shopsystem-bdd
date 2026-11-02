# Branch review of i55 (review 2)

**Verdict: DONE_WITH_CONCERNS.** w241 (supervision r212, r213) does what its plan says. Its only change under `features/` is removing the two deprecated scenarios its Retires section names (@r9, @r105). It adds one test step and changes no production code. Review 1's finding 1 is still open and is still Important, triaged fix now. i55's proposals still do not name requests r50–r58, work-queue r47 or supervision r184–r186, which commit deda9fa6 applied to the spec. Nothing builds them. `work list` still prints no turn for a request, which r50 asks for (scripts/workqueue_list.py:73-74). Every check has a run in the brief.

## Range and work-items

- Range: `c53a7c25e23b..9e21ad76a02b` on `main`. The initiative branch is `main`, so the range also holds the commits of i45, i47–i54 and i56–i64. Since review 1 (at 3d02f4a1), the range adds:
  - 583f7064 (branch review 1 of i55)
  - 792dc74e, 5d286cf8, 25f8e9ad, a700415c (the supervision formulate round), 6a59c634, 4804a724
  - w241's commits
- i55's work-items, all `green`:
  - **w239** (requests#r64): code commits cae12e0c and fce410f4. Reviewed in review 1.
  - **w240** (work-queue#r62): code commits 8b68f278 and aff8ddf1. Reviewed in review 1.
  - **w241** (supervision#r212, #r213): 7bb4eacf (add), e54e91ea, bad5d025, 7b658adb, 8c3caec6, **153518ea** (code), 48bc894e, 9e21ad76.
- i55's proposals are all `formulated`:
  - requests: adds r64, removes r14
  - work-queue: adds r62, removes r23
  - supervision: adds r212 and r213, removes r149, r32, r9 and r105

## Suite

Suite: 1086 passed, 0 failed at 9e21ad76 in 35.49 s (1 skipped, 13 xfailed, 8 xpassed, 56 subtests passed). Exit 0. Command: `python3 -m pytest -q -n auto -rfEx -p work_items --work-item w239 --whole-suite`.

- **Parallel**: yes (`-n auto`).
- **In-process**: no. The step definitions run each script as a subprocess (tests/scenarios/conftest.py `run` fixture, as review 1 verified; w241 did not touch it). The suite is under 60 s, so this is not a finding.
- **Dry-run and real mode**: the system has no dry-run mode of an operation, as review 1 established. w241 changed no production code. There is no agreement test to look for.
- **Count**: 1086 is review 1's 1089 less the r9 scenario and the two examples of the r105 outline, which w241 retired. The four r213 examples and the r212 scenario replace them in the count.

## Checks

All runs are at 9e21ad76.

- **w239's scenarios**: exit 0. 182 passed, 1 skipped, 56 subtests passed, in 6.44 s.
- **w240's scenarios**: exit 0. 187 passed, 1 skipped, 56 subtests passed, in 4.43 s.
- **w241's scenarios**: exit 0. 186 passed, 1 skipped, 56 subtests passed, in 4.92 s. The run lists the r212 scenario and all four r213 examples (the `withdrawn` one among them) in its warnings, so they ran.
- **tools check** (`--base c53a7c25`): exit 1.
  - `== ruff ==`: 28 errors, the same set as review 1.
    - 19 are in workflow scratch scripts under `.shop/work/i50`, `i59`, `i60` and `i63`.
    - The rest are in test files other initiatives touched.
    - The one file w241 touched, `tests/scenarios/supervision_proposal_steps.py`, has RUF100 at :102 and :146. Both are unused `noqa: E731`, and both were already there: they were :102 and :137 at the base and moved down 9 lines with w241's added step. w241's lines add none.
  - `== vulture ==`: `tests/scenarios/work_queue_status_steps.py:100: unused variable 'notes'`. This was already there (review 1, finding 4). w241 did not touch the file.
  - `== import-linter ==`: "the project states no import contracts". There is nothing to check.
- **tools size**: exit 0, no output. No tracked Python file is over 300 lines. w241's file is 213 lines.
- **features deprecated**: exit 0, 21 entries.
  - i55's formulate round a700415c left three still deprecated: @r32 ×2 ("when no work-item can make a transition and one is awaiting-answer …" and "`work run` prints a question that has no answer yet …") and @r149 ("a formulate round that formulates nothing …"). All three are "for: removal". See finding 2.
  - r163's pointer is still broken ("for: r209 and r210 | no scenario has that title"). It is not i55's.
- **features bindings**: exit 0, "every binding names a scenario".

## Removed and weakened tests

I searched w241's change and the commits added since review 1 for:
- deleted `def test_` functions and step definitions
- removed scenarios or examples
- changed parametrize cases
- removed or loosened `assert`s
- added skip or xfail marks

What I found:

- **w241, 153518ea**: the `@r9 @deprecated` scenario "when every work-item is green or withdrawn and no request whose asker is this context is in the asker's turn, `work run` exits successfully … (deprecated)" was removed.
  - It proved that `work run` exits 0 and prints each status when the work-items are all green or withdrawn.
  - It is listed under w241's Retires, and the plan names it in §1 and §4.
  - The r212 scenario covers the same ground and adds the proposal condition.
- **w241, 153518ea**: the `@r105 @deprecated` outline "an initiative whose work-items are <work-items>, its delivery otherwise closed, <set> (deprecated)" was removed, with its 2 examples.
  - It proved that an initiative is set done only with a green work-item.
  - It is listed under Retires and in plan §1.
  - The r213 outline repeats both examples and adds two.
- **Formulate round a700415c** (not a work-item): the r9, r105, r32 ×2 and r149 scenarios were deprecated. The r9 scenario was rewritten as r212 and the r105 outline as r213. Both rewrites add a condition and assert the same outcomes. No assertion was loosened.
- No step definition was removed or changed. One was added (`proposal_withdrawn`, supervision_proposal_steps.py:125-131).
- Review 1's list for w239 and w240 stands unchanged.

## Allowances

- **w241**: 3-implement says "none". The diff touches no existing test, so the claim holds.
- **w239 and w240**: as review 1 found, "none", and that holds.

## Cannot verify

- Nothing fails the review. Every check the role asks for has a run in the brief.
- The suite shows **8 xpassed**, up from 3 at review 1. `-rfEx` does not name xpassed tests, so I cannot tell which expected failures now pass. See Observation 3.

## Findings

### 1. Important, fix now (i55's capability-proposals; no work-item). The lines i55 applied are not on its proposals, so nothing builds them. Carried from review 1, still open

- **Where**:
  - spec/capabilities/requests.md r50–r58
  - spec/capabilities/work-queue.md r47
  - spec/capabilities/supervision.md:34 (r185), :81 (r186), :122 (r184)
  - the frontmatter of `.shop/work/i55/requests.md`, `work-queue.md` and `supervision.md`
  - scripts/workqueue_list.py:65 and :73-74
  - features/requests.feature:239 (@r34), :411 (@r39), :428 (@r41), :443 (@r43), :459 (@r13)
- **What is wrong**:
  - Commit deda9fa6 applied requests r50–r58, work-queue r47 and supervision r184–r186, and retired requests r13, r34, r39, r41 and r43.
  - No i55 proposal names them. requests adds only r64; work-queue only r62; supervision only r212 and r213.
  - No scenario in requests.feature, work-queue.feature or supervision.feature carries a requests r50–r58, work-queue r47 or supervision r184–r186 tag. The @r47 to @r58 tags in supervision.feature are supervision's own ids.
  - The formulate round's own ledger line (2026-11-02) says "r184 r185 r186 have no scenario".
  - Verified at HEAD: `listing` prints `request <name> <status>`, with no turn (workqueue_list.py:74). Its JSON gives `{"request", "status"}` only (:65). r50 says: "When `work list` is run, `work` shall print each request with its status and whose turn it is."
  - The @r13, @r34, @r39, @r41 and @r43 scenarios are still live under ids the spec has retired.
- **Why it matters**:
  - `work list` gives a wrong answer against r50.
  - Lines approved under the person's delegation (q21 lines 1–13) are left unbuilt.
  - r213 sets i55 done once this branch review lists nothing to fix now. Every other condition already holds, so i55 would close with these lines unbuilt.
- **Fix**: put the ids back on i55's proposals, by hand repair or through integrating-a-proposal:
  - requests: adds r50–r58; removes r13, r34, r39, r41, r43
  - work-queue: adds r47
  - supervision: adds r184, r185, r186
  
  Then let the formulate rounds tag or deprecate the scenarios and draft the work-items. The cross-repository lines (r52, r53, r56, r57, r58) can be held by w212's successor, as r39, r41 and r43 are now. The alternative is to retire those lines through integrating-a-proposal.

### 2. Minor, observation (i55's supervision formulate round a700415c; no work-item). Three deprecated scenarios that no work-item retires, and whose removal would leave r184 and r186 unpinned

- **Where**:
  - features/supervision.feature: the @r32 @deprecated scenarios at about :189 and :199
  - features/supervision.feature: the @r149 @deprecated scenario at about :1610
  - `.shop/work/i55/w241.md` Retires, which lists only the r212 and r213 replacements, of r9 and r105
- **What**:
  - r32 and r149 are retired from the spec, and their scenarios are "Deprecated for: removal".
  - No i55 work-item lists them under Retires, so they will stay in the feature files.
  - Their behaviour now lives in r184 (exit with an error, printing open questions) and r186 (the new integrate round), which have no scenario (finding 1).
- **Fix**: when finding 1 is fixed, re-tag these scenarios to r184 and r186 in the formulate round, or deprecate them for those ids, so that the work-items accepting r184 and r186 retire them.

### 3. Minor, observation (w239). An observation with no `date:` line is listed with the date "None". Carried from review 1

- **Where**: scripts/workqueue_list.py:52-54 and :78. The JSON gives `"date": null` (:67).
- **Reproduction**: read in the code, not run. `date.group(1) if date else None`, then `print("observation %s %s" % (observation, date))`.

### 4. Minor, observation (w240). vulture flags an unused `notes` at tests/scenarios/work_queue_status_steps.py:100. Carried from review 1

The hit was already there at the base. Reproduction: the `tools check` run at 9e21ad76, `== vulture ==`.

### 5. Minor, drop (w240). The `with_state` step's regex lost its space

In work_queue_status_steps.py, `whose work-items? (?P<items>…)` became `work-items?(?P<items>…)`. Carried from review 1.

### 6. Minor, drop (w241). `proposal_withdrawn` repeats the template of `proposal_in_status`

This is supervision_proposal_steps.py:125-131. It repeats the frontmatter template of `proposal_in_status` (:110) instead of widening that step's pattern. The plan's decision 2 left either way open. The pattern is anchored with `$`, and the other phrasings need a comma clause, so the bindings stay unambiguous. I verified that the risk of a collision with the step at :21 (`p1 is formulated…`) and the delegation step (`p1 is awaiting-answer, its ## Questions…`) does not hold.

### 7. Minor, observation (the range on `main`). Commits that belong to no work-item

Almost every commit outside w239's, w240's and w241's is marked `none`. They are other initiatives' work, and i55's own workflow commits: deda9fa6, 3611f76b, ddcb3e73, 19c0bc4d, 0e9fa09f, 047c6057, a700415c and 583f7064. These are spec applies, formulate rounds and the review record, not work-item code. The code commits of other initiatives are listed in review 1, finding 6, and have their own branch reviews. Fix: give the brief each commit's work-item across all initiatives, or start the range at the initiative's own commits.

## Shape (CLAUDE.md)

- **Size limit (300 lines)**: met. `tools size` prints nothing, and supervision_proposal_steps.py is 213 lines.
- **Module map, `tests/scenarios/`** (one `<capability>_*_steps.py` module a concern): met. The proposal Given is in `supervision_proposal_steps.py`, next to the existing proposal Givens (:21, :110).
- **Module map, `scripts/workqueue_done.py` and `scripts/supervise_done.py`**: w241 left them unchanged, as the plan's decision 3 says. r213's conditions are already there: `CLOSED_PROPOSAL = ("formulated", "withdrawn")`, verified in review 1. The `withdrawn` example passes in w241's run.
- **Reachability**: the retired r9 and r105 scenarios used only steps that the r212 and r213 scenarios also use (plan §1). No step was left unreached. Review 1's notes stand: `work show` with no target is reached only by the retired-id @r13 scenario (finding 1).
- **Code no line asks for**: none in w241, which adds only a test step serving r213's outline. Review 1 found none in w239 or w240.

## Coupling

- w241 adds no dependency.
- **pytest-bdd and pytest**: unchanged since review 1. pytest-bdd relies on private pytest APIs (`PytestRemovedIn10Warning` from pytest_bdd/compat.py:28 in the suite run), so the suite will break on pytest 10. What would make it stable: pin pytest below 10 together with pytest-bdd, or upgrade both together.
- **git**: review 1's notes stand: the porcelain path parsing in supervise_faults.py, and the `index.lock` stderr match in stub_claude.py.

## Observations

1. **Observation with no date.** It is listed with the date "None" (finding 3). Reproduction: read workqueue_list.py:52-54 and :78; not run.
2. **Unregistered tags.** Scenario tags r212 and r213, which i55's formulate round added, are not registered marks; nor are r209–r218 or `deprecated`. The suite warns `PytestUnknownMarkWarning: Unknown pytest.mark.r212` (and r213), 32 times each, so `--strict-markers` would fail. Reproduction: the warnings summary of the suite run at 9e21ad76.
3. **Unnamed xpassed tests.** The whole suite at 9e21ad76 has 8 xpassed, up from 3, and none is named because `-rfEx` has no `X`. A test that would show them: the same command with `-rX`. Not run.
4. **`work list` and r50.** `work list` prints no turn for a request (finding 1). Reproduction: read workqueue_list.py:73-74 at 9e21ad76. A test that would show it: an @r50 scenario, "work list prints q1 with open and the upstream's turn". Not run.
