# Branch review of i27 (review 2): findings

**Verdict: DONE.** No finding is Critical, none is triaged fix now, and I ran every check a work-item names and every tool the review calls for, and verified each. The code is unchanged since review 1 (`git diff --stat bd4e1888 HEAD` touches only `.shop/`), and every result below was taken again at b82d2c75. Five of the observations below (F3, F7, F8, the uncommitted measurement and the done status) are already raised as lines of request q5, which is accepted.

## Range and work-items

- **Range:** `3cbd0c52..b82d2c75` on `i25-review-findings-to-implementation`. Base 3cbd0c52 is the commit that added `.shop/work/i27/initiative.md` (`git log --diff-filter=A`).
- **w164** (supervision r91-r97, r66), green.
  - Code commits: 0ca611cf, a4e922a6, 12d95e83.
  - They sit between 4910049f `ready -> claimed` and 44e59393 `claimed -> done`.
- **w165** (requests r19), green.
  - Code commit: 34ee952c.
  - It sits between cc16fb45 `ready -> claimed` and f547d55e `claimed -> done`.
- **w166** (work-queue r25), green.
  - Code commit: 5c876c93.
  - It sits between 117402c4 `ready -> claimed` and 1a6567bd `claimed -> done`.
- **Commits that belong to no work-item:**
  - Coordinator and queue commits: `work note` ×6, `work add` ×3, 9c9d4d00, e14a9ad1.
  - 9ed288cf (spec), 18cd9812 (features) and 5d1bd783 (the proposals written by hand): see F1.
  - New since review 1, all under `.shop/` with no code:
    - afedc909 (branch review 1's stage directory);
    - 7d8572d6 (i27's measurement and analysis, committed by hand: see F10);
    - 5a049e83 to b82d2c75 (request q5, its outcomes, its turn and its intake round).

## Suite

`Suite: 860 passed, 0 failed at b82d2c75 in 21.70 s`

- Wall time is from `time`. pytest reported 21.41 s, plus 1 skipped and 56 subtests passed.
- **Parallel:** yes. `pytest.ini` has `addopts = -n auto`.
- **In-process:** no. The When steps run `scripts/work` as a subprocess, with a stand-in for `claude`.
- The suite runs under 60 s, so this is not a finding.

## Checks

- **w164** (`pytest --work-item w164`): 151 passed, 1 skipped.
- **w165** (`--work-item w165`): 143 passed, 1 skipped.
- **w166** (`--work-item w166`): 143 passed, 1 skipped.
- No plan names a check other than its accepted scenarios. Those scenarios are among the runs above, and among the full suite.
- **`tools check --base 3cbd0c52`** exits 1:
  - **ruff:** 7 errors.
    - 5 are on lines w164 added (F2):
      - `scripts/supervise_brief.py:74` ISC004;
      - `tests/scenarios/supervision_all_steps.py:111` FURB167 and `:127` RUF007;
      - `tests/scenarios/supervision_integrate_steps.py:72` FURB167;
      - `tests/scenarios/test_supervision.py:14` I001.
    - 2 were already there before Base: `tests/scripts/stub_claude.py:185` and `:186`, FURB167.
  - **vulture:** clean.
  - **import-linter:** "the project states no import contracts". The heading does not say `missing`; there are no contracts to check.
- **`tools size --limit 300`:** printed nothing. The largest files the branch touched: supervise.py 248, supervise_rounds.py 134.
- **`features deprecated`:** 3 deprecated scenarios, none touched by this branch: migration-tools @r15, work-queue @r1 and work-queue @r9 (see Feature files).
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** not applicable. The only `--dry-run` in `scripts/` is `git push --dry-run` (`supervise_review.py:41`, `supervise_faults.py:67`). That is git's own check, not a mode of this system.

## Removed and weakened tests

**What I searched:** every `-` line of `git diff 3cbd0c52 HEAD -- tests features`, for:
- deleted `def test_` functions;
- dropped parametrize or Examples rows;
- removed or loosened asserts;
- added skips or xfails;
- removed scenarios.

**Weakened, listed in the plan:** `tests/scenarios/supervision_rounds_steps.py:160` `second_not_refused` (w164, a4e922a6).
- **What it proved:** the second `work run` exits 0 with no `work:` error.
- **What it asserts now:** for the r84 scenario that started an integrate round, two things:
  - stderr does not contain "not committed" (r10's refusal);
  - a second integrate round was started.
- It no longer asserts the exit code, because r93 and r96 make that second run end in r96's error.
- The scenarios with no round keep the old assertion.
- w164's plan lists it under "4. Tests the decisions break", so this is not a finding.

**Signatures changed, nothing loosened:**
- `proposed_fulfilling` gained `status=` (default `proposed`, as before).
- `nothing_uncommitted` and `request_uncommitted` gained `context`. A literal path resolves to itself. The new-initiative phrases now resolve to the one new initiative, which is a stronger check than before.
- `stub_claude.wait_until` gained an optional `seconds`.

**`features/`:** additions only, all in 18cd9812. No scenario was removed.

## Allowances

- **w164:** one row, `second_not_refused`. It needs no allowance, because the plan lists it. I checked it against a4e922a6: only that step's assertions changed, as described above.
- **w165:** "none". I checked: 34ee952c only adds steps (`tests/scenarios/requests_write_steps.py`).
- **w166:** "none". I checked: 5c876c93 adds path resolution to two git Thens and a `spec/index.md` Given. No assertion was removed or loosened.

## Cannot verify

- **The probe of `supervise_change`'s change-list handling was not run.**
  - I wrote `.shop/scratch/i27-branch-review/probe_change.py`. It writes proposals into a temporary directory, for these change lists:
    - capability `initiative`;
    - capability `../../x`;
    - the same capability twice;
    - another capability's id;
    - a malformed id;
    - an entry with nothing;
    - a capability not in `spec/`.
  - `python3 .shop/scratch/i27-branch-review/probe_change.py` was refused ("This command requires approval"), as it was in review 1. I did not try another route, and I deleted the directory.
  - So F3-F5 rest on reading `scripts/supervise_change.py:13-52`. The reading is plain: line 46 is `path = self.dir / (one["capability"] + ".md")`, and nothing checks the name or the form of an id.
  - This probe is none of the checks a work-item names, and every one of those passed. The findings it bears on are observations.

## Findings

**F1. Minor | no work-item | observation.**
- **What:** 9ed288cf (spec), 18cd9812 (`features/`, 86 lines added, nothing removed) and 5d1bd783 (the three capability-proposals) were made by hand, not by a work-item.
- The ledger records why: i27 was bootstrapped by hand once, because the loop it fixes could not carry it.
- **Why it matters:** no plan, report or work-item review covers them. No work-item edited `features/`, so this is not the Critical finding of a work-item doing so.
- **Fix:** none, once r92 carries the next initiative.

**F2. Minor | w164 | drop.**
- **What:** the 5 ruff errors on lines w164 added (listed under Checks).
- **Why it matters:** noise in the next `tools check`.
- **Fix:** run `ruff check --fix`, and put parentheses around the string at `supervise_brief.py:74-76`.

**F3. Minor | w164 | observation.** `scripts/supervise_change.py:23-25,46`. The `capability` of a change list becomes a file name with no check.
- `initiative` (or `ledger`, or `w164`) would overwrite that node's file in the initiative directory, and `supervise_rounds.py:108-109` would commit it.
- `../../x` would write outside the initiative directory, and the file would be left uncommitted.
- A capability that `spec/capabilities/` does not have is accepted.
- Only the integrate agent's own result can send such a name today.
- **Fix:** refuse (`BadChanges`) a name that is not a `spec/capabilities/<name>.md` of the checkout. q5 line 3 is this line, accepted.

**F4. Minor | w164 | observation.** `scripts/supervise_change.py:21-31,46`. Two entries for one capability: the second file overwrites the first, and the first's ids are lost without a word.
- **Fix:** merge the entries or refuse them.

**F5. Minor | w164 | observation.** `scripts/supervise_change.py:27-29`. An id is only checked for being a non-empty string.
- `other#r9` under `thing` is accepted, which breaks r92's "on that capability".
- An id that is not of the form `<capability>#r<n>` / `term/<term>` is accepted, though the brief (`supervise_brief.py:74-76`) names that form.
- **Fix:** match `^<capability>#r\d+$|^term/[\w-]+$` in `entries`.

**F6. Minor | w164 | observation.** `scripts/supervise_rounds.py:107-109`. The proposal files are written before the commit.
- If the commit fails (GitFailed), they are left uncommitted, and the next `work run` is refused under r10.
- The stage directory already behaves the same way.
- **Fix:** remove the written files when the commit fails.

**F7. Minor | w164 | observation.** The gate and apply briefs do not name the kept drafts.
- Only the drafted proposal's body names the stage directory (`supervise_change.py:49`).
- `grep -n drafts scripts/supervise_brief.py` finds only the integrate brief.
- **Fix:** q5 line 4 asks for it, accepted.

**F8. Minor | w165 | observation.** `scripts/workqueue_request.py:87`. `--delegation ""` writes `delegation: ""`, which `supervise_answers` reads as no delegation.
- **Fix:** q5 line 5 asks for a refusal, accepted.

**F9. Minor | w166 | drop.** `scripts/workqueue_start.py:48`. The commit subject is `work: start i<n>, fulfilling q<n>`, which uses the prefix of `work run`'s own transition commits.
- Nothing keys on it: Base is found by `--diff-filter=A`, and `measure_build` drops `work: ` subjects only inside a work-item's window.
- **Fix:** use `work start: i<n> ...`.

**F10. Minor | no work-item | observation.** 7d8572d6 says `work run` "left them uncommitted": i27's measurement and analysis.
- No Behaviour line asks `work run` to commit them (r75, r76), so the code contradicts no line.
- **Fix:** q5 line 2 adds the line, accepted. Nothing in this branch is wrong against today's spec.

**No code that no line asks for:**
- `round_lock` serves r95.
- `BadChanges` and `refuse_integrate` serve r96 and the decision worker-results-are-files.
- The empty-directory cleanup in `start` serves r25 with r7.
- `commit(also=)` and the stub's `linger` are mechanism and test.

**No behaviour that contradicts a line or a Purpose:**
- r93's round makes no `proposed -> started` transition on a started initiative (`supervise_rounds.py:64-67`).
- r96 holds on every ending (`:88`, `:92`, `:115`).
- r94 and r97 share one guard (`supervise.py:206`).

**Risk I named and checked: a deadlock between `round_lock` and `lock`.** `round_lock` is taken only in `Rounds.round` (`supervise_rounds.py:60`). `rounds()` is called at `supervise.py:203` without holding `lock`, and inside the round `lock` is taken after `round_lock`. That is a single lock order, so there is no deadlock.

## Feature files

- **work-queue @r9 is deprecated, but its replacement's work-item is green.** w140 (i24, `accepts: [work-queue#r24, work-queue#r9]`) is green, so the deprecated scenario should have been retired with its binding.
  - It was already there before Base and belongs to no i27 work-item.
  - Observation: retire it in a work-item that lists it under Retires.
- **work-queue @r1 and migration-tools @r15:** the work-items that would accept the replacements (w89, w90, w86, w17) are withdrawn, so these deprecations are not stale. w50 (green) accepts r1-r7, but it predates the replacement scenario.
- No scenario was removed, and no binding names no scenario.

## Shape

- **Size limit 300:** met (`tools size` printed nothing).
- **"A new concern gets a new module and a row":**
  - met for `scripts/supervise_change.py` (CLAUDE.md:29);
  - met for `tests/scenarios/supervision_integrate_steps.py`, a `<capability>_*_steps.py` module.
- **The `scripts/supervise*.py` row (CLAUDE.md:28) is not met.** It names only "a capability-proposal's apply and formulate rounds (`supervise_rounds.py`)", but the module now also holds the integrate round's ending and the cross-initiative round lock (`supervise_rounds.py:15,55-61,95-116`).
  - Its docstring (`:1-3`) still names only r70, r71, r80 and r83.
  - Observation. The check that would show it fixed: the row and the docstring both name the integrate round and r95's lock.
- **The other rows the branch touched are met:**
  - `workqueue_start.py` (docstring `:1` names r25);
  - `workqueue_request.py`;
  - `scripts/work`;
  - `supervise_all.py` (`:27-29`);
  - `tests/scripts/` (the stub documents `linger` at `stub_claude.py:34-35`).
- **Import inside a function:** `tests/scenarios/work_queue_git_steps.py:64` imports `new_initiatives` inside `_resolved` to avoid an import cycle. Acceptable.
- **No unreached code or steps:** vulture is clean, `features bindings` is clean, and every step the branch added is used by a passing scenario.

## Coupling

- **New coupling:** none. The `changes` field is this plugin's own result. `threading.Lock` is standard library. The pytest-bdd calls are its published API.
- **Existing coupling, relied on again:** the `claude -p` result's `subtype` `error_max_turns` (`supervise_faults.py:153`).
  - If that subtype changed upstream, a turn-limit ending would look like another fault.
  - r91 keeps the drafts on every non-DONE ending (`keep_round`), so nothing would be lost. That independence from the subtype is what keeps this stable.

## Observations

One line each, with its reproduction:
- **F3:** capability `initiative` overwrites initiative.md. Read from `supervise_change.py:46`; the probe was refused approval.
- **F4:** duplicate capability entries: the last one wins. `supervise_change.py:21-31,46` (read).
- **F5:** another capability's id, or a malformed id, is accepted. `supervise_change.py:27-29` (read).
- **F6:** a failed commit leaves proposal files uncommitted. `supervise_rounds.py:107-109` (read).
- **F7:** the gate and apply briefs do not name the kept drafts. `grep -n drafts scripts/supervise_brief.py` finds only lines 68-76 (the integrate brief).
- **F8:** `work request ... --delegation ""` writes `delegation: ""`. `workqueue_request.py:87` (read).
- **F10:** `work run` left i27's measurement and analysis uncommitted. Commit 7d8572d6's subject.
- **Stale deprecation:** work-queue @r9 is still deprecated while w140 is green. `features deprecated`, then `grep -E '^(status|accepts)' .shop/work/i24*/w140.md`.
- **Stale module-map row:** CLAUDE.md:28 and `supervise_rounds.py:1-3` omit the integrate round and the round lock.
