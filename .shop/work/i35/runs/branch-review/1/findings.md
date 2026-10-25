# branch review of i35

**Verdict: DONE_WITH_CONCERNS.** No finding is Critical and none is triaged fix now. The suite is green at HEAD, and so are w196's scenarios. Two things go to the person:

1. Six deprecated scenarios on this branch have green replacements. Under the branch's own r123/r124, they would get a retire work-item before this review started, and none was drafted. I could not establish whether the `work run` that started this review was running HEAD's code.
2. A read-only probe that would have settled point 1 by running it was refused by this session's permissions, so it rests on my reading of the code and data.

## Range and work-items

- Range: `3fbe46ea..bd7b11b4` (base `3fbe46ea`, "work: start i35, fulfilling q12", which adds `.shop/work/i35/initiative.md`).
- Work-items: **w196** (supervision; accepts supervision#r73, r123, r124; green).
  - Its commits run from `00964b0e work: w196 ready -> claimed` to `ed893f5c work: w196 claimed -> done`.
  - Less `work run`'s own commits, that leaves one: `45922c8e supervision: retire by the deprecated scenario's replacement (r73), draft the retire work-item (r123, r124)`.
- Commits outside any work-item are `work run`'s own rounds for the capability-proposal and the initiative, so none of them is a finding:
  - `dd7a3049`: apply round 2, changing `spec/capabilities/supervision.md` (r73 changed, r123 and r124 added, per answers 1-6).
  - `5651dd93`: formulate round 3. It changes `features/supervision.feature`: the old r73 pair deprecated, and four scenarios added.
  - `d8a9e3a4`: approved -> formulated. It also commits the formulate round's directory, `splice.py` included (see M3).
  - The rest are `work note`, `work answer` and transition commits.

## Suite

`Suite: 924 passed, 0 failed at bd7b11b4 in 27.7 s` (pytest's line: `924 passed, 1 skipped, 56 subtests passed in 27.38s`; wall 27.68 s).

- **Parallel:** yes (`pytest.ini` addopts `-n auto`).
- **In-process:** no. The step definitions run `work run` as a subprocess (`tests/scenarios/conftest.py:27-34`).
- The suite is under 60 s, so this is no finding.

## Checks

- **w196's check** (its scenarios), `python3 -m pytest -q -p no:warnings --work-item w196`: 148 passed, 1 skipped, 56 subtests passed in 6.11 s. The work-item names no other check.
- **`tools check --base 3fbe46ea`:**
  - **ruff:** 6 hits. None is on a line w196 changed.
    - `.shop/work/i35/runs/supervision/3-formulate/splice.py:1,4,7`: SIM115, three hits. This file was committed by the formulate round (`d8a9e3a4`), new on this branch; see M3.
    - `scripts/workqueue.py:248`: I001. Already there: the local import in `moved_to`, a line the branch did not touch.
    - `tests/scenarios/supervision_proposal_steps.py:102`: RUF100. Already there: the `noqa: E731` line is unchanged, only moved up by the deletions.
    - `tests/scenarios/test_supervision.py:14`: I001. Already there: it is the star-import block. The one import the branch added, `supervision_retire_steps`, sits in sorted order between `request` and `rounds`.
  - **vulture:** 1 hit, `tests/scenarios/supervision_proposal_steps.py:66`, `base` unused in `drafted`. Already there: the function is unchanged.
  - **import-linter:** "the project states no import contracts". No heading says `missing`.
- **`tools size --limit 300`:** no output, so no tracked Python file is over the limit. The touched files are all under it: supervise.py 275, supervise_draft.py 122, workqueue.py 294, supervision_retire_steps.py 114.
- **`features deprecated`:** 7 deprecated scenarios:
  - migration-tools @r15;
  - supervision @r75, @r102, @r105;
  - work-queue @r1, @r9, @r23.
  - See F1.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** no operation the branch touches has a dry-run mode. The only `--dry-run` uses are `git push --dry-run` probes, in supervise_review.py:41 and supervise_faults.py:67. Not applicable.

## Removed and weakened tests

I searched the diff of `tests/` and `features/` for deleted `def`s, parametrize changes, removed or loosened `assert`s, added skip or xfail, and rewritten Thens.

- **`thing_feature_deprecated`** (Given, removed from `tests/scenarios/supervision_proposal_steps.py`).
  - What it did: it wrote two `@deprecated` scenarios tagged by their own @r.
  - Who used it: only the two old r73 scenarios that w196 retires.
  - Plan §4 lists it.
- **`retires_listed`** (Then, removed from the same file).
  - What it proved: the drafted thing work-item lists "it used to wait" and neither "it used to answer" nor "it waits".
  - Who used it: only the retired scenarios.
  - Plan §4 lists it.
  - Its successor `retires_listed_by_replacement` (supervision_retire_steps.py:71-78) makes the same three assertions and adds a fourth ("it answers"), so it is not a weakening.
- **The two old r73 scenarios**, "… lists under its Retires each deprecated scenario of a requirement it accepts (deprecated)" and "… whose changes name a range … (deprecated)".
  - w196 removed them (`45922c8e`, -20 lines of `features/supervision.feature`).
  - Both are under w196's `## Retires`. I checked that the commit changes nothing else under `features/`.

No other test was removed or weakened.

## Allowances

The report's `## Tests changed under an allowance` says "none". That is right: the two steps that went served only scenarios the work-item retires. There is nothing to verify.

## Cannot verify

- **Whether the `work run` that started this review ran HEAD's `draft_retires`.**
  - By reading HEAD's code against this branch's data, `Drafts.draft_retires()` would draft a work-item now (F1).
  - The plugin's `scripts/supervise_draft.py` holds the same function now. Its file time and how it compares to this branch were refused by this session's permissions.
  - My read-only probe was refused too. It imported `supervise_draft` and printed `deprecated()` and each replacement's holders, writing nothing.
  - So I cannot tell whether the runner's code was older or the drafting failed.

## Findings

**F1. Important, w196, observation (unverified; see Cannot verify):** this branch went to its branch review while six deprecated scenarios have green replacements, and r124 says the r123 retire work-item comes first.

- **Where:** features/supervision.feature:1091 (@r75), :1413 (@r102), :1487 (@r105); features/work-queue.feature:7 (@r1), :71 (@r23), :282 (@r9).
- **The holders, read from `.shop/work/*/w*.md`.** These are the non-withdrawn work-items that accept the replacements' requirements:
  - supervision#r75: w139, w153, w194, all green.
  - supervision#r102: w170, w171, w172, all green.
  - supervision#r105: w181, w194, both green.
  - work-queue#r1: w50, green.
  - work-queue#r9: w140, green.
  - work-queue#r23: w130, w160, w192, all green.
  - Every other work-item in `.shop/work` is green or withdrawn.
- **Why the guard does not stop it:** none of the six is listed in the form the guard matches (`- "<title>" (`). w194 lists a different r75 scenario. w100 names the r9 one inside a prose bullet and is green, yet the scenario is still there.
- **What HEAD's code would draft:** under r123 and r124, `pull_through` (scripts/supervise.py:212-215) would have drafted one work-item in i35 before this review. It would retire these six, under w194's `part_of` (the highest-numbered holder).
- **The seventh:** migration-tools @r15 is rightly left out. Its holders w17 and w86 are withdrawn, so no green replacement is there.
- **Why it matters:** answer 3 of the proposal asks for exactly these to be retired ("supervision @r75, @r102, @r105; work-queue @r9, @r23"). This review of i35 is not the last one if the code is right.
- **Fix:** run `work run i35` again with HEAD's scripts. If no retire work-item is drafted, that is a defect in `deprecated()` or `draft_retires()`, and it is fix now.
- **Reproduction:** `features deprecated` (above), plus a grep of `^accepts:` and `^status:` in `.shop/work/*/w*.md` for those requirements.

**F2. Important, w196, observation:** the r74 fix work-item is drafted with no `## Retires`, though r73 now covers every drafting.

- **Where:** scripts/supervise_draft.py:117-119 (`fix_work_item`, which calls `workqueue.add` with no `retires=`).
- **What is wrong:** w196 rewrote r73 to "**When** `work run` drafts a work-item, …", which covers every drafting.
- **Why it matters:** wrong today only in the file written. The fix item copies the `accepts` of a work-item that was already green, so r123 has already taken those scenarios before the first review. Nothing is lost on any path a client takes today.
- **Fix:** pass `retires=self.retires(accepts)` there. r123's guard then sees those entries.
- **Reproduction:** read lines 117-119.

**F3. Minor, w196, observation:** the retire work-item copies `under` and `accepts` from the last-drafted green holder, so it re-accepts requirements that are already done.

- **Where:** scripts/supervise_draft.py:72-74.
- **What it does:** in scenario 1063 it is drafted with `under: other` and `accepts: [other#r4]`. On this branch (F1) it would accept w194's `[supervision#r120, r121, r75, r105]` while retiring work-queue scenarios too.
- **Why it is not "code no line asks for":** `work add` requires both fields. r123's "under the capability-proposal of the last-drafted work-item" fixes `part_of`, and copying `under` and `accepts` from that same work-item mirrors r74's fix work-item. That is mechanism, not new observable behaviour. The plan (decision 5) and the implementer's report both flag it.
- **Fix:** if it proves noisy, write a line on what a retire work-item accepts.

**F4. Minor, w196, observation:** in the fix loop (scripts/supervise.py:224-230), a later branch review starts without `draft_retires` running again.

- **Why it is narrow:** r124 says "before it starts a branch review", and this path skips the drafting before every review after the first. Only a replacement that turns green during the fix loop is affected, for example one in another initiative run side by side by `supervise_all`'s threads. No client path does this today.
- **Fix:** call the retire drafting before each `branch_review()` in the loop.
- **Reproduction:** read lines 224-230.

**F5. Minor, w196, drop:** the second Then of 1076 orders the measurement after the drafting only through file mtimes (supervision_retire_steps.py:108-114). That is a weak proof, but adequate while the measurement is uncommitted in that fixture.

## Shape

- **Size limit (300):** met for every touched file (see Checks).
- **Module map:**
  - `scripts/supervise_draft.py`: the row reads "the work-items of a formulated capability-proposal and of a branch review's fix-now findings". It now also drafts the r123 retire work-item, and neither the row nor the module docstring (lines 1-3) names that, though plan §2 said the docstring would name r123. **Minor, observation:** add "and the work-item retiring deprecated scenarios whose replacements are green (r123)" to both. Check: `grep -n r123 CLAUDE.md scripts/supervise_draft.py` shows both.
  - `scripts/supervise*.py` (supervise.py:212-215): met. The four added lines sit in `pull_through`, which is the run's concern.
  - `scripts/workqueue.py:103`: met. The Retires line now takes `(capability @tag)` from each entry's `cap#rN`, and both callers pass that form (supervise_draft.py:48 and :67).
  - `tests/scenarios/`: met. The new `supervision_retire_steps.py` follows `<capability>_*_steps.py` and is imported in `test_supervision.py:39`.
- **Step definitions no scenario reaches:** none added. `features bindings` is clean, and the two dead steps were removed with their scenarios.

## Coupling

No new dependency on another project. `deprecated()` relies only on this repository's `features_gherkin` (`load`, `description`, `effective_tags`, `REQ_TAG`, `natural`). The steps use `git merge-base --is-ancestor`, which is git's published interface.

## Observations

- F1: `features deprecated` lists six deprecated scenarios whose replacements' holders are all green, and i35 holds no retire work-item (`.shop/work/i35` has only w196.md). Unverified; see Cannot verify.
- F2: scripts/supervise_draft.py:117-119 calls `workqueue.add` with no `retires=` (read).
- F3: scenario 1063's drafted item has `under: other` and `accepts: [other#r4]` (supervision_retire_steps.py:80-87 with supervise_draft.py:72-74).
- F4: supervise.py:224-230 calls `branch_review()` again with no `draft_retires()` before it (read).
- M3, Minor, observation (formulate round, `d8a9e3a4`): `.shop/work/i35/runs/supervision/3-formulate/splice.py` is a round's helper committed with its run directory. It gives `tools check` three SIM115 hits and counts as a tracked Python file. The fix is to keep round helpers in `.shop/scratch` or exclude `.shop/work/*/runs/` from `tools check`. Reproduction: `tools check --base 3fbe46ea` (above).
- Module map and docstring for r123 (Shape): `grep -n r123 CLAUDE.md scripts/supervise_draft.py` gives nothing.

Note: one of my shell commands changed the session's directory to `.shop/work` partway through. No write happened there, and `git status --short` is empty at the end. The scratch directory `.shop/scratch/i35-branch-review/` has been deleted.
