# Branch review 4 of i39 (Requests go through one shared tool)

**Verdict: DONE_WITH_CONCERNS.** One finding is triaged fix now: finding 1 of review 3, carried because it is still true. `scripts/supervise_change.py:79-89,108-111` merges a redraft round's ids into another held capability-proposal. No Behaviour line asks for this: the line is only in q20, line 3, and q20 is still `open` with `turn: upstream`, so the line is not integrated. This is a re-review of a fix work-item, and on a re-review code no line asks for stays fix now.

One check could not be verified, carried from reviews 1 to 3: whether a real `claude -p` integrate round can read the upstream's spec outside its worktree (w202).

w207 fixes review 3's finding 2 (data left invalid): on the merge path, the other proposal keeps its own drafts path. It also adds two r7 refusals:
- an undecodable ledger is refused, naming the file (D1);
- a work-item with no `kind` is refused with "has no kind" (D3, review 3's O2).

No change under `features/` and no removed or weakened test anywhere in the range.

## Range and work-items

- **Range:** `b4c4ad5e..199e8dd3` on `main`.
  - Reviews 1 to 3 covered up to `ba907c58`. I re-ran every check on the whole range.
  - I read in full only what changed after `ba907c58`. `git diff --numstat ba907c58 HEAD -- tests features scripts` shows only w207's five files.
- **w202** (spec-integration#r44, `green`): `6e3c4f04` and `fe844bb3`. Unchanged.
- **w205** (work-queue#r34-r39, `green`): `a033c460` and `bf231ddc`. Unchanged, except where w206 and w207 change `scripts/workqueue_list.py`.
- **w206** (fix of branch review 2, `green`): `e4e61321`. Unchanged, except where w207 changes `scripts/supervise_change.py:105-118`.
- **w207** (fix of branch review 3, accepts work-queue#r34-r39, `green`):
  - Its commits run from `2b50f401 work: w207 ready -> claimed` to `469cbcba work: w207 claimed -> done`.
  - Leaving out `work run`'s own commits, that is `b8dab1b2` "Fix branch review 3 findings…". It touches `scripts/supervise_change.py`, `scripts/workqueue_list.py`, `scripts/workqueue_status.py`, `tests/scripts/test_supervise_change.py` and `tests/scripts/test_workqueue_list.py`. All five are in its fileset.
- **Other commits after review 3:**
  - `f68503e8` commits branch review 3 (`work run`).
  - `76781005` is `work add`.
- **Commits that belong to no work-item:** none new. `2ae8e313` (the hand restoration) is carried as O6.
  - The range also holds the commits of i40 and i41 (w203 and w204, with their rounds). They are on the same `main`, and each sits inside its own initiative's `work:` bracket.

## Suite

`Suite: 968 passed, 16 failed at 199e8dd3 in 26.76 s` (`python3 -m pytest -q -p no:cacheprovider`; wall time 26.6 s by `time`).

- **Parallel:** yes, `-n auto` from `pytest.ini`.
- **In-process:** no. The steps drive `scripts/work` as a subprocess. The suite runs under 60 s, so this is not a finding.
- **The 16 failures** are the same 16 as in reviews 2 and 3. Each is a formulated scenario with no work-item yet:
  - 14 requests scenarios
  - design-model-check @r120 (the v17 scenario)
  - supervision @r135
- **The 3 more passes than review 3** are w207's three new unit tests.
- **With `-p work_items --work-item w207 --whole-suite`:** `968 passed, 1 skipped, 16 xfailed in 27.30s`. Nothing fails.

## Checks

- **w202** (`-p work_items --work-item w202`): 151 passed, 1 skipped, 56 subtests passed in 6.33 s.
- **w205** (`--work-item w205`): 157 passed, 1 skipped, 56 subtests passed in 3.97 s.
- **w206** (`--work-item w206`): 157 passed, 1 skipped, 56 subtests passed in 3.98 s.
- **w207** (`--work-item w207`): 157 passed, 1 skipped, 56 subtests passed in 4.18 s. With `--whole-suite`: as above, 0 failed and 16 xfailed.
- **w207's unit tests** (`-n 0 tests/scripts/test_supervise_change.py tests/scripts/test_workqueue_list.py`): 7 passed in 3.35 s.
- **`tools check --base b4c4ad5e`:**
  - **ruff:** 28 errors, the same set as review 3. The `supervise_change.py` B023 that was at `:114` is now at `:115`, moved down by w207's reordering.
    - `scripts/supervise_change.py:88` B023, twice (w206); `:115` B023 (w204). All three are false positives (Minor, drop).
    - `tests/scripts/test_supervise_change.py:7` RUF100 (w204)
    - `tests/scenarios/supervision_reintegrate_steps.py:13` F401 and `:137` FURB167 (w204)
    - `tests/scenarios/test_supervision.py:14` I001 (w204)
    - `tests/scenarios/test_work_queue.py:7` I001 (from before base)
    - `tests/scenarios/work_queue_list_steps.py:79` RUF015 (w205, drop)
    - 19 errors in round helper scripts committed under `.shop/work/{i39,i41}/runs/` (O5)
  - **vulture:** `tests/scenarios/work_queue_status_steps.py:77`, unused `notes`. The line is from before base.
  - **import-linter:** "the project states no import contracts". It is not `missing`.
- **`tools size --limit 300`:** printed nothing and exited 0.
- **`features deprecated`:** 14 deprecated scenarios, as in review 3.
  - Their replacements have no `green` work-item: design-model-check @r120, requests @r44 and @r45.
  - The other 11 are deprecated for removal.
  - None is due for retirement.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** not applicable. No operation the branch touches has a dry-run mode.

## Removed and weakened tests

None.

**What I searched for:**
- `git diff --numstat ba907c58 HEAD -- tests features` shows 0 deleted lines in the tests (12 and 22 added) and no file under `features/`.
- w207 adds three tests and changes no existing one:
  - `test_a_round_started_for_one_proposal_leaves_another_held_proposals_drafts_path_as_it_was`
  - `test_show_of_an_initiative_whose_ledger_is_not_utf8_is_refused_naming_the_ledger`
  - `test_show_of_a_work_item_file_with_no_kind_is_refused_saying_it_has_no_kind`
- Review 3's search of the earlier range stands: no `skip`, `xfail` or `parametrize` was added, and no assert was changed.

## Allowances

- **w207 `3-implement/report.md`:** "none". This holds: no existing test changed.
- **w206, w205 and w202:** as in review 3, they hold.

## Cannot verify

- **(w202, carried from reviews 1 to 3)** Whether a real integrate round, `claude -p` with `Read` and no `--add-dir`, can read the upstream's `spec/` at a path outside its worktree. Only a real session would show it, and I do not start one.

## Findings

### 1. Important, fix now (code no line asks for): a redraft round merges its ids into another held proposal's lists (w206, carried from review 3)

- **Where:** `scripts/supervise_change.py:79-89` (`merge_lists`) and `:108-111`, called from `scripts/supervise_rounds.py:195`.
- **What is wrong:** no Behaviour line in `spec/capabilities/supervision.md` asks for the merge. r92, r142 and r148 speak only of the proposal being drafted anew, and a grep of the file for merge or union finds only the branch merges of r4, r18 and r61.
- **Where the line is:** only in q20, line 3 (`.shop/work/requests/q20.md`). q20 is still `status: open` and `turn: upstream`, as at review 3.
- **What w207 did:** its plan, decision 1, keeps the merge on the ledger's ruling of 2026-10-27 and makes no change. The w207 stage review called this "already ruled".
- **Why it is still fix now:** behaviour reaches code only through a line. On a re-review, code no line asks for stays fix now until that line is written.
- **Fix:** integrate q20 line 3 through integrating-a-proposal and formulate its scenario. Or have the person confirm that i39 closes with the line carried by q20.
- **Note:** the merge itself is right. It keeps the other proposal's applied ids, and since w207 it also keeps that proposal's drafts path.

### 2. Minor, observation: the SessionStart hook still exits 1 with a traceback on an undecodable ledger (w207 touches this path; the risk is from before it)

- **The risk:** w207's D1 changes `scripts/workqueue_status.py:77-79` to read the ledger through `workqueue.read`, so a non-UTF-8 ledger now raises `Refused`. That path is shared by `open_text`, which the SessionStart hook reaches through `migrate status --hook`. The hook must exit 0 (`scripts/migrate_session.py:5`).
- **What I verified, by reading:**
  - `scripts/migrate_upgrade.py:168-170` calls `work_text(root)` with no `try`.
  - `scripts/migrate:53` catches only `Failed`.
  - Only `migrate compacting` (`migrate_session.py:50-53`) catches `Refused`.
  - So under the hook, a non-UTF-8 ledger gives an uncaught `Refused`. Before w207 it gave an uncaught `UnicodeDecodeError` (`git show ba907c58:scripts/workqueue_status.py:79`, `read_text(encoding="utf-8")`).
  - A non-UTF-8 `initiative.md` gives the same outcome from before base.
- **Not run:** a probe (`probe_hook.py`: a git repository with an open initiative and its ledger as `b"\xff\xfe"`, then `migrate status --hook`) needed approval, and the harness did not give it. The outcome above is from reading the code only.
- **Why it is an observation:** w207 changed the exception's class, not the outcome. No client writes a non-UTF-8 ledger: `work note` writes UTF-8.
- **Fix:** have `migrate_upgrade.run` catch `workqueue.Refused` around `work_text` on the hook path, as `migrate_session.run` does.
- **Keep as a test:** run `migrate status --hook` in a repository with an open initiative whose `ledger.md` holds `b"- 2026-01-01: \xff\xfe\n"`, and assert exit 0 and no `Traceback` in stderr.

### 3. Minor, observation: an id can land in both `adds` and `removes` (w206, carried from review 3, F3)

- **Where:** `scripts/supervise_change.py:85-88`. Each field is merged on its own.
- **Status:** unchanged by w207. It waits on the q20 line 3 that settles which list wins.

### 4. Minor, observation: a first integrate round also merges (w206, carried from review 3, F4)

- **Where:** `supervise_rounds.py:195` passes `name`, which is the initiative for its first round.
- **The gap:** q20 line 3 covers only a round "started for a capability-proposal". Widen it when it is taken in.

### 5. Minor, observation: a proposal merged into still has its lists replaced at its own apply round (w207, open case named by its plan §5 and its report)

- **What:** after the merge, p2 keeps its own drafts path (finding 2 of review 3 is fixed). But its apply round's change list replaces its lists (`rewrite_lists`, r114/r145). Its own drafts do not hold the merged ids, so the apply can drop them.
- **Why it is an observation:** this is the q20 line's to settle. No round in i39 reaches it, since every other proposal had been applied when the redraft ran.

### 6. Minor, drop: ruff B023 at `scripts/supervise_change.py:88` (twice) and `:115` (w206, w204)

- These are false positives: `re.sub` calls the lambda within the same iteration.

### Carried, unchanged

- **O6, Minor, observation (no work-item):** `2ae8e313` is a commit made by hand outside any work-item or round.
- **Minor, drop (w205):** RUF015 at `tests/scenarios/work_queue_list_steps.py:79`.

### Review 3's findings, now resolved

- **Finding 2 (data left invalid):** fixed by w207.
  - In `supervise_change.py:108-111`, the merge path `continue`s before the drafts sentence is rewritten, which rests on r108 and r142.
  - `test_a_round_started_for_one_proposal_leaves_another_held_proposals_drafts_path_as_it_was` asserts that p2 still says "The drafts of this proposal are in old/." It passes, and on read it fails against `ba907c58`, where the merge path fell through to the rewrite at `:112-115`.
  - The own-proposal path is unchanged.
- **O2 (w205, "is a None"):** fixed by w207's D3 (`workqueue_list.py:64-65`). It is an r7 refusal on r37's path.

## Shape

- **CLAUDE.md, size limit 300:** met. `tools size` printed nothing.
- **Module map, `scripts/supervise_change.py`:** met. w207 only reorders the merge branch within `write_proposals`.
- **Module map, `scripts/workqueue_status.py`** (`work status`): w207 changes `ledger(root, directory)`, which `work show <initiative>` (r36) reaches through `workqueue_status.read`.
  - As in reviews 2 and 3, this row should read `work show <initiative>` once `work status` is retired (decision 0072).
- **Module map, `scripts/workqueue_list.py`:** met. The refusal is in `work_item`, the module's `work show <work-item>`.
- **`tests/scripts/` row ("tests of the scripts that no scenario drives"):** `test_workqueue_list.py` grows by two subprocess tests of `work show`, which r36 and r37 drive.
  - The refusals they check are edges no scenario names, which is why they are here.
  - Observation, as in review 3: move them into the work-queue scenarios once a line names these refusals. A check that shows it complete: `tests/scripts/test_workqueue_list.py` holds no `work show` or `work list` call.
- **Carried from earlier reviews:**
  - `spec_integration_steps.py` holds two concerns (r44, r45).
  - The no-target `show` goes dead when requests#r13, work-queue r3 and r11 are retired.
- **Reachability:** w207 adds no step definitions. `merge_lists` is reached only by the unit tests and by a real redraft round (finding 1).

## Coupling

- **`raised.jsonl`:** as in review 3. Nothing writes it yet; the writers would be requests#r29 and supervision#r135, both xfail. Its form is given only in `workqueue_list.py`. What would make it stable: state the form in the Implementation section of work-queue or requests.
- **q20:** w206's merge is promised only by an open request (finding 1). q20 also carries work-queue r48 and r40.
- **Carried from reviews 1 to 3:**
  - the upstream's spec is read from a working-tree path (w202);
  - Claude Code's `-p` read scope (w202);
  - pytest-bdd's private `__scenario__` (`work_items.py`) and its 560 `PytestRemovedIn10Warning`s.

## Observations

- **F2 (w207 path):** the hook on a non-UTF-8 ledger. Reproduction: read `scripts/migrate_upgrade.py:168-170`, `scripts/migrate:53` and `scripts/workqueue_status.py:77-79`. The probe described in finding 2 was not run (no approval).
- **F3 (w206):** an id lands in both `adds` and `removes`. Reproduction: review 3's probe gave `adds: [other#r1, other#r2, other#r3]` and `removes: [other#r3, other#r1]`. The code at `:85-88` is unchanged.
- **F4 (w206):** the first integrate round merges. Reproduction: read `supervise_rounds.py:195` against q20 line 3.
- **F5 (w207):** the merged ids can be dropped on the other proposal's apply. Reproduction: read `supervise_rounds.py:166-167` (`rewrite_lists` on apply) against `supervise_change.py:108-111`.
- **O1, O3, O4 (w205):** carried from review 3 with the same reproductions.
- **O5:** round helper scripts are committed under `.shop/work/*/runs/` and fail ruff (19 of the 28 errors). Reproduction: the `tools check` output above.
- **O6:** `2ae8e313`, a commit made by hand. Reproduction: `git show --stat 2ae8e313`.

The scratch directory `.shop/scratch/i39-branch-review/` held only `probe_hook.py`, which was not run, and it is deleted.
