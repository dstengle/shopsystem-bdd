# Branch review of i27: findings

**Verdict: DONE.** No finding is Critical, none is triaged fix now, and every check was run and verified. Two kinds of finding: Minor lint on lines w164 added, and observations about hardening `supervise_change.write_proposals`.

## Range and work-items

- Range: `3cbd0c52..bd4e1888` on `i25-review-findings-to-implementation`. Base 3cbd0c52 is the commit that added `.shop/work/i27/initiative.md` ("work start: i27 (fulfils q4)").
- w164 (supervision r91-r97, r66), green. Code commits: 0ca611cf, a4e922a6, 12d95e83 (between 4910049f `ready -> claimed` and 44e59393 `claimed -> done`).
- w165 (requests r19), green. Code commit: 34ee952c (after cc16fb45 `ready -> claimed`, before f547d55e `claimed -> done`). It holds the same code as the 6a4244bb that the implementer reported.
- w166 (work-queue r25), green. Code commit: 5c876c93 (after 117402c4 `ready -> claimed`, before 1a6567bd `claimed -> done`).
- Commits that belong to no work-item:
  - Coordinator commits: `work note` ×6, `work add` ×3, 9c9d4d00, e14a9ad1.
  - 9ed288cf (spec), 18cd9812 (features) and 5d1bd783 (the capability-proposals written by hand).
  - See finding F1.

## Suite

`Suite: 860 passed, 0 failed at bd4e1888 in 21.44 s` (pytest's own timing; 1 skipped, 56 subtests passed).

- **Parallel:** yes. `pytest.ini` gives `addopts = -n auto`.
- **In-process:** no. The `When` steps run `scripts/work` as a subprocess, with a stand-in for `claude` (`tests/scenarios/test_supervision.py:69`).
- The suite runs in under 60 s, so this is not a finding.

## Checks

- **w164** (`--work-item w164`): 151 passed, 1 skipped. Its 8 scenarios all PASSED when run by name: r91 ×2, r92, r93, r94, r95, r96 and r97. r66's scenario, and r84's two scenarios that use the rewritten step, also pass in the full suite.
- **w165** (`--work-item w165`): 143 passed, 1 skipped. `test_request_with_delegation_writes_the_delegation_given_in_the_request` PASSED.
- **w166** (`--work-item w166`): 143 passed, 1 skipped. `test_start_commits_the_initiative_it_writes_on_the_current_branch` PASSED. `-k start` on test_work_queue.py: 7 passed, r22 included. The implementer's report said r22 did not collect; it does now.
- **`tools check --base 3cbd0c52`**, exit 1:
  - **ruff:** 7 errors. 5 are on lines this branch added, all w164 (F2). 2 were already there: `tests/scripts/stub_claude.py:185`, `:186` FURB167, from commit 6e6d3143, before Base.
  - **vulture:** clean.
  - **import-linter:** "the project states no import contracts". Nothing missing.
- **`tools size --limit 300`**: printed nothing (clean).
- **`features deprecated`**: 3 deprecated scenarios, none of them touched by this branch: migration-tools @r15, work-queue @r1 and work-queue @r9. See "Feature files" below.
- **`features bindings`**: "every binding names a scenario".
- **Dry-run against real-mode test:** not applicable. No operation this branch touches has a dry-run mode. The only `--dry-run` in the code is `git push --dry-run` (`supervise_faults.py:67`, `supervise_review.py:41`): a git check, not a mode of the system's own.

## Removed and weakened tests

**What I searched:** every `-` line of `git diff 3cbd0c52 HEAD -- tests features`, looking for:
- deleted `def test_` functions and dropped parametrize or Examples rows;
- removed or loosened `assert` lines;
- added `skip` or `xfail`;
- removed scenarios.

**What I found:**
- `tests/scenarios/supervision_rounds_steps.py::second_not_refused` (w164, a4e922a6) is weakened.
  - **What it proved:** the second `work run` exited 0 with no `work:` error.
  - **What it asserts now,** when the scenario began an integrate round (r84's "ends DONE ... leaves nothing uncommitted" scenario): stderr does not contain the r10 refusal's words "not committed", and a second integrate round was started. Scenarios with no round keep the old assertion.
  - **Listed:** in w164's plan, part 4 ("Tests the decisions break"), so this is not a finding. I checked the r10 refusal: its text is "%s under %s %s not committed; ..." (`scripts/supervise.py:88`), so the new assertion tests the right words.
- Signatures changed but nothing weakened:
  - `proposed_fulfilling` gained a `status` parameter whose default is the old value.
  - `nothing_uncommitted` and `request_uncommitted` gained `context`. A literal path resolves to itself, and the new-initiative phrase now has to resolve to a directory that exists, which is stronger than before.
  - `stub_claude.wait_until` gained an optional `seconds`.
- **Feature files:** additions only, all in 18cd9812.

## Allowances

- **w164:** one row, `second_not_refused`. It gives no `setup`/`interim` kind, but the plan lists the test under part 4, so it needs no allowance. Verified against a4e922a6: the diff changes only that step's assertions, as described above.
- **w165:** "none". Verified: 34ee952c only adds steps.
- **w166:** "none". Verified: 5c876c93 adds a Given line (`spec/index.md`) and path resolution to the two git Thens. No assertion is removed or loosened.

## Cannot verify

- **The probe for F3-F5 was not run.** I wrote `probe_change.py` in `.shop/scratch/i27-branch-review/`, which I have since deleted.
  - It wrote proposals from change lists with these capabilities and ids: `initiative`, `../../x`, the same capability twice, another capability's id, a malformed id, and an entry with nothing.
  - Running it (`python3 .shop/scratch/i27-branch-review/probe_change.py`) was refused because the command needs approval.
  - F3-F5 therefore rest on reading `scripts/supervise_change.py:13-52`, not on a run. The reading is unambiguous: there is no check on the name, and `:46` is `path = self.dir / (one["capability"] + ".md")`.
- This is not one of the checks a work-item names. Every one of those was run and passed.

## Findings

- **F1. Minor | no work-item | observation.** Some commits in the range belong to no work-item:
  - 9ed288cf (spec), 18cd9812 (`features/`: 86 lines added) and 5d1bd783 (the three capability-proposals).
  - The ledger records them: i27 was bootstrapped by hand once, because the loop it fixes could not carry it (observation 2026-10-25-proposals-written-by-hand). They are the initiative's apply and formulate work.
  - The change under `features/` adds scenarios only. No work-item made it, so it is not the Critical finding of a work-item editing features.
  - **Why it matters:** these commits have no plan, report or work-item review behind them; this review is their only reading.
  - **Fix:** none needed, once r92 carries the next initiative.
- **F2. Minor | w164 | drop.** ruff errors on lines w164 added:
  - `scripts/supervise_brief.py:74` ISC004 (implicit string concatenation in a list);
  - `tests/scenarios/supervision_all_steps.py:111` FURB167 and `:127` RUF007;
  - `tests/scenarios/supervision_integrate_steps.py:72` FURB167;
  - `tests/scenarios/test_supervision.py:31` I001: `supervision_integrate_steps` is imported after `..._given` but sorts after `..._intake`.
  - **Why it matters:** lint noise for the next `tools check`.
  - **Fix:** `ruff check --fix` and parentheses around the brief's string. This is polish, cheap but not needed now.
- **F3. Minor | w164 | observation.** `scripts/supervise_change.py:13-31,46`. The change list's `capability` is used as a file name with no check.
  - **Overwrite:** `"initiative"` overwrites `.shop/work/<i>/initiative.md` with a proposal, and the commit (`supervise_rounds.py:108-109`) commits that. A work-item's name (`w164`) or `ledger` does the same.
  - **Escape:** `"../../x"` writes outside the initiative directory. That file is then not in the commit's paths list, so it is left uncommitted in the checkout.
  - **Why it matters:** data lost (the initiative's file), or a stray write. Only the agent's own result can send such a name today; the agent is told to give capability names.
  - **Reproduction:** the probe's case `capability 'initiative'` (not run, see Cannot verify). From the code: `path = self.dir / (one["capability"] + ".md")`.
  - **Fix:** refuse (BadChanges) a capability that is not a `spec/capabilities/<name>.md` of the worktree, or a name not matching `[a-z0-9-]+`, or one equal to an existing node's file. This is the plan's open case 1.
- **F4. Minor | w164 | observation.** `scripts/supervise_change.py:21-31`. Two entries for one capability: the second's file overwrites the first's, and the first's ids are lost without a word.
  - **Reproduction:** the probe's case "same capability twice" (not run).
  - **Fix:** merge the entries, or refuse with BadChanges.
- **F5. Minor | w164 | observation.** `scripts/supervise_change.py:27-29`. An id is checked only for being a non-empty string.
  - An id of another capability (`other#r9` under `thing`) is accepted. That breaks r92's "on that capability" and the scenario's "nothing of another's".
  - An id not of the form `<capability>#r<n>` / `term/<term>` is also accepted, though the brief names that form.
  - **Reproduction:** the probe's cases "another capability's id" and "an id not of the form" (not run). This is the plan's open case 2.
  - **Fix:** match `^<capability>#r\d+$|^term/[\w-]+$` in `entries`.
- **F6. Minor | w164 | observation.** `scripts/supervise_rounds.py:107-109`. `write_proposals` writes the files before `commit`.
  - A failed commit (GitFailed) leaves the proposal files in the checkout, uncommitted. The next `work run` is then refused by r10 ("not committed").
  - The same holds for the stage directory, so this is not new.
  - **Fix:** remove the written files when the commit fails, as `workqueue.committed` does.
- **F7. Minor | w164 | observation.** The gate and apply briefs (`scripts/supervise_brief.py`) do not name the drafts kept in `runs/<initiative>/<k>-integrate/drafts/`.
  - Only the drafted proposal's body names them: "The drafts of this proposal are in .shop/work/<i>/runs/<i>/<k>-integrate" (`supervise_change.py:48`).
  - The agent's gate text says "read each round's gate.md where it was written".
  - **Why it matters:** the carry to the gate rests on the agent following the proposal's body.
  - **Fix:** a Behaviour line naming the drafts in the gate and apply briefs, written through integrating-a-proposal. This is the plan's open case 5 and was also noted by w164's own review.
- **F8. Minor | w165 | observation.** `scripts/workqueue_request.py:87`. `--delegation ""` writes `delegation: ""`, which `supervise_answers.Answers.delegation` reads as no delegation.
  - The plan's open case. No client sends it.
  - **Fix:** refuse an empty delegation, or write no field.
- **F9. Minor | w166 | drop.** `scripts/workqueue_start.py:48`. The commit message `work: start i<n>, fulfilling q<n>` uses the prefix of work run's own commits, unlike `work note: ...` and `work add: ...`.
  - Nothing keys on it: Base is found with `--diff-filter=A` (`supervise_brief.py:16`), and `measure_build.py:88` drops `work: ` subjects only inside a work-item's window, where a start commit never falls.
  - **Fix:** `work start: i<n> ...`.

No finding is code that no line asks for:
- `round_lock` serves r95.
- `BadChanges` serves r96 and design-decision/worker-results-are-files ("a malformed result is a failed stage").
- The empty-directory cleanup in `start` serves r25 with work-queue r7.
- `commit(also=)` and the stub's `linger` are mechanism and test.

No behaviour contradicts a Behaviour line or a Purpose:
- r96 ("ends without a change list") holds on every ending. Non-DONE endings and faults already raise a Refused naming the round (`supervise_rounds.py:88,92`); DONE without `changes` raises the same at `:115`.
- r93's round makes no `proposed -> started` transition (`:65-67`).
- r94 and r97 share the guard at `scripts/supervise.py:206`.

## Feature files

- **work-queue @r9, a deprecated scenario whose replacement's work-item is green:** "`work <command>` commits the change it makes to a work-item on the current branch" is deprecated for "... or a capability-proposal ...". The replacement's work-item, w140 (i24, accepts work-queue#r9), is `green`, so the deprecated scenario should have been retired.
  - This was already there before Base; it belongs to no i27 work-item.
  - **Observation:** retire it with its binding in a work-item that lists it under Retires.
- **work-queue @r1 and migration-tools @r15:** their accepting work-items found by grep (w89, w90, w86, w17) are all `withdrawn`, so these deprecations are not stale by this test.
- No scenario was removed. No binding names no scenario.

## Shape

Measured against `CLAUDE.md`:
- **Size limit 300:** met. `tools size` printed nothing. The largest touched files are within the limit (supervise_rounds.py 134 lines).
- **"A new concern gets a new module and a row here":**
  - met for `scripts/supervise_change.py` (CLAUDE.md:29, the new row);
  - met for `tests/scenarios/supervision_integrate_steps.py` (a `<capability>_*_steps.py` module for the integrate-round concern).
- **The `scripts/supervise*.py` row (CLAUDE.md:28)** names "a capability-proposal's apply and formulate rounds (`supervise_rounds.py`)". `supervise_rounds.py` now also holds the integrate round's ending and the cross-initiative round lock (`:15`, `:55-61`, `:95-116`). The row is stale.
  - **Observation:** extend the row to "the integrate, apply and formulate rounds and the round lock".
  - **Check that would show it complete:** the row names every concern of `supervise_rounds.py`'s module docstring, which still says only r70, r71, r80, r83 (`supervise_rounds.py:1-3`, also stale).
- **Rows this branch touched:**
  - `scripts/workqueue_start.py`: met (docstring updated, `:1`).
  - `scripts/workqueue_request.py`: met.
  - `scripts/work`: met.
  - `scripts/supervise_all.py`: met. `run_all` shares one lock (`:27-29`).
  - `tests/scripts/`: met. The stub's `linger` key is documented in the docstring (`stub_claude.py:34-35`).
- `tests/scenarios/work_queue_git_steps.py:64` imports `new_initiatives` inside `_resolved`. That is local to avoid an import cycle with `work_queue_start_steps`; acceptable.
- **No unreached code or steps:** vulture is clean, and `features bindings` says every binding names a scenario. Every step w164-w166 added is used by a scenario that passed.

## Coupling

- **New coupling:** none. The `changes` field is this plugin's own agent result. `threading.Lock` is the standard library. The pytest-bdd `parsers.re` and `given`/`then` calls are its published API.
- **Already there, relied on again by the r91 turn-limit row:**
  - The `claude -p` result's `subtype` value `error_max_turns` (the stub gives it in `supervision_integrate_steps.py:53`; `work run` reads it in `supervise_faults.py:153`). That is Claude Code's result field. A rename upstream would make the turn-limit ending look like another fault; r91 keeps the drafts on any ending, so nothing would be lost.
  - **What would make it stable:** keeping the drafts independent of the subtype, which the code already does (`keep_round` on every non-DONE).

## Observations

One line each, with its reproduction:
- **F3:** a capability named `initiative` overwrites initiative.md. Code `supervise_change.py:46` (the probe was not run: approval refused).
- **F4:** duplicate capability entries: the last one wins. Code `supervise_change.py:21-31,46`.
- **F5:** another capability's id, or a malformed id, is accepted. Code `supervise_change.py:27-29`.
- **F6:** a failed commit leaves proposal files uncommitted. Code `supervise_rounds.py:107-109` (not probed).
- **F7:** the gate and apply briefs do not name the kept drafts. `grep -n drafts scripts/supervise_brief.py` gives only the integrate brief's lines 68 and 73.
- **F8:** `work request ... --delegation ""` writes `delegation: ""`, read as none. Code `workqueue_request.py:87`.
- **Stale deprecation:** work-queue @r9 is deprecated while w140 is green. `features deprecated`, then `grep accepts .shop/work/i24-*/w140.md`.
- **Stale module-map row:** the `supervise*.py` row and `supervise_rounds.py`'s docstring omit the integrate round and the round lock. CLAUDE.md:28, `supervise_rounds.py:1-3`.
