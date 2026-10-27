# Review of w207 (fix the findings of branch review 3 of i39)

**Verdict: DONE.** No finding is Critical and none is triaged fix now.

## Commits reviewed

- The `work/w207` branch is gone. The range is `2b50f401 work: w207 ready -> claimed` .. `469cbcba work: w207 claimed -> done` on the checked-out history.
- Leaving out `work run`'s own `work:` commit, it holds one commit: `b8dab1b2` "Fix branch review 3 findings…". It touches `scripts/supervise_change.py`, `scripts/workqueue_list.py`, `scripts/workqueue_status.py`, `tests/scripts/test_supervise_change.py` and `tests/scripts/test_workqueue_list.py`.
- This is the commit the implementer's `result.json` lists, and all five files are in w207's fileset. The other files in `469cbcba` are `.shop/work/` run records.
- Nothing under `features/` changed.

## Removed and weakened tests

None. What I searched: the diff has only `+` lines in the two test files. No test function, assertion, parametrize case, skip or xfail is removed or loosened. Three tests are added:
- `test_a_round_started_for_one_proposal_leaves_another_held_proposals_drafts_path_as_it_was`
- `test_show_of_an_initiative_whose_ledger_is_not_utf8_is_refused_naming_the_ledger`
- `test_show_of_a_work_item_file_with_no_kind_is_refused_saying_it_has_no_kind`

## Allowances

The report's `## Tests changed under an allowance` says "none". The commits agree: no existing test was changed.

## Cannot verify

- The report's red run (3 failed before the fix). I did not check out the pre-fix code. On read, each new assertion fails against the old code:
  - the merge path rewrote the drafts sentence to `drafts/`;
  - `read_text` raised `UnicodeDecodeError`;
  - the old refusal text contains "None".
- D1 with `--json` (`work show i1 --json` on an undecodable ledger) has no test. On read it takes the same path: `workqueue_status.read` → `ledger` → `workqueue.read` runs before the output form is chosen.
- Carried from branch review 3: whether a real `claude -p` integrate round can read the upstream's spec (w202). Nothing in w207 bears on it.

## Findings

### 1. Minor, observation: the refusal for a non-UTF-8 ledger now also reaches `work status` and the SessionStart hook (w207)

- **What:** `scripts/workqueue_status.py:77-81` is shared by `status()`, which means `work status` and `open_text`, the SessionStart hook's text.
- **Before:** such a ledger gave a `UnicodeDecodeError` traceback there.
- **Now:** it gives a `Refused`, the same kind of refusal that `workqueue.read` already gives for an undecodable `initiative.md` on that path. This is r7 (`spec/capabilities/work-queue.md:40`), so no new class of outcome is added.
- **Hardening only:** I did not verify whether `migrate status --hook` catches `Refused` (the hook must always exit 0). This review did not change that risk.
- **Reproduction:** read `scripts/workqueue_status.py:77-88` and `:135-140`, and `scripts/migrate_session.py:22-24`.

### 2. Minor, drop: ruff B023 at `scripts/supervise_change.py:115` (from before w207)

- `tools check --base 2b50f401` reports B023 at `:88` (twice) and `:115`, and RUF100 at `tests/scripts/test_supervise_change.py:7`.
- All four come from before w207: branch review 3 lists them, with `:115` then at `:114`, moved down by w207's reordering.
- They are false positives: `re.sub` calls the lambda within the same iteration.

### Verified, not findings

- **Finding 2 of branch review 3** is fixed. In `supervise_change.py:108-111` the merge path returns before the drafts sentence is rewritten, so another held proposal keeps its own drafts pointer (supervision r108, r142). The own-proposal path is unchanged.
- **Finding 1 of branch review 3** is left as ruled in the ledger of 2026-10-27 (reading B, carried by q20). w207 adds no merge behaviour.
- **D1 and D3** are r7 refusals ("say why") on the paths of r36 and r37. The message wording is mechanism, not code that no line asks for.
- **Behaviour against r34-r39 and the Purpose:** no contradiction. `list` and `show` outputs are unchanged except for the two refusals.

## Checks

- `python3 -m pytest -q -n 0 -p no:cacheprovider tests/scripts/test_supervise_change.py tests/scripts/test_workqueue_list.py`: 7 passed.
- `tools check --base 2b50f401`:
  - **ruff:** 4 errors, all from before w207 (finding 2).
  - **vulture:** clean.
  - **import-linter:** "the project states no import contracts".
- `tools size --limit 300`: printed nothing.

## Commands run

- `git log --format=%H -1 --grep="^work: w207 ready -> claimed$" work/w207`: the branch is gone.
- `git log --format='%h %s' -12`
- `git show --stat b8dab1b2`
- `git diff 2b50f401 469cbcba --stat`
- `git diff 2b50f401 b8dab1b2`
- reads of `tests/scripts/test_supervise_change.py:1-30`, `scripts/supervise_change.py:95-126`, `tests/scripts/test_workqueue_list.py:1-25`, `scripts/workqueue.py:50-56`, `scripts/workqueue_status.py:135-145` and `scripts/migrate_session.py`
- greps for `ledger(`, `Refused` and r7
- the pytest, `tools check` and `tools size` runs above
