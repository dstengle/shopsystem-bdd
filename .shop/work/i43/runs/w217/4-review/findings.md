# Review of w217 (fix of branch review 1 of i43, finding 1; supervision r154-r157)

**Verdict: DONE.** Nothing is Critical and nothing is triaged fix now. The commit does what finding 1 of branch review 1 asked for, and stays inside the file set. Two Minor observations are noted below, both triaged drop.

## Commits reviewed

- `9d61d97ae87f696f4a4f75adeee02a8a05009110`: "supervise_review_read: commits of work answer, withdraw, retry and add belong to their work-item (r156)". This is the one commit the brief's `Commits:` gives. It comes after `ba199fc1 work: w217 ready -> claimed`.
- It matches the implementer's `result.json` `commits` (`9d61d97a`).
- Files: `scripts/supervise_review_read.py` (+3/-2) and `tests/scripts/test_supervise_review_read.py` (+23/-1). Both are in the work-item's `fileset:`.
- Nothing under `features/` was changed. The work-item has no Retires section.
- Suite: taken from the brief's record: 1033 passed, 0 failed at 9d61d97a. The expected failures are w212's 11 parked `test_requests.py` scenarios, which are not w217's.

## Removed and weakened tests

None. What I searched the diff of `tests/` for:
- deleted `def test_` functions;
- removed or changed `assert`s;
- parametrize cases;
- `skip` or `xfail`.

The diff only adds two tests and a helper `owners`, and widens the module docstring. `test_a_proposals_transition_commit_belongs_to_no_work_item` is unchanged, and it still passes.

## Allowances

The report's `## Tests changed under an allowance` is "none". No existing test changed, so there is nothing to hold.

## Cannot verify

- Nothing is left open that matters. The plan's "the four new cases are red today" is backed by the report's red run for `work answer`. I did not reproduce the red run myself (that would need the parent revision checked out). From the old regex `^work: (\S+) \S+ -> \S+$`, though, it is plain that none of the four subjects matches it.

## Findings

### 1. Minor · w217 · drop: `work add: <initiative>/<name>` does not check that the initiative is this one

- **Where:** `scripts/supervise_review_read.py:11` (group 2 takes `<name>` whatever the initiative is) and `:42-43`.
- **What:** a `work add: i99/w1 drafted` commit in the range would be given to this initiative's `w1`.
- **Why it hardly matters:** work-item numbers are global across initiatives (w202-w212 in i39, w215-w217 in i43), so two initiatives never share a name. The plan and the report name this as an open case. It is hardening for an input nothing makes today.
- **Fix, if ever wanted:** capture the initiative in the regex and compare it with `self.dir.name`.
- **Reproduction:** none run. It is reasoned from the regex and the numbering in `.shop/work/`.

### 2. Minor · w217 · drop: no scenario row pins the four subjects; only the unit test does

- **Where:** `tests/scenarios/supervision_branch_steps.py:144` (`gives_work_items`) still builds only `work: <name>` subjects.
- **Why:** this is plan decision 3 (reading A). A scenario changes only through a formulate round. The unit test `test_a_commit_of_work_answer_withdraw_retry_or_add_belongs_to_the_work_item_it_names` covers the behaviour. A row is for a later formulate round if it is wanted.

### What I verified

- **Risk:** the regex does not match the subjects `work` really writes. I checked `workqueue.py:105`, `:217` and `:242` and `workqueue_answer.py:74` and `:76`. Each format matches the new alternation. The real subjects in `ebbf1bea..9d61d97a` (`work add: i43/w217 drafted`, `work answer: w216 awaiting-answer -> ready`) match too.
- **Risk:** a proposal's `work answer: <proposal>` with no transition is now taken. It is not: it does not match the regex, and the new test asserts `none` for it.
- **Risk:** `name = found and (...)` gives `None` when there is no match. `None in names` is False, so the commit gets `none`. That is correct.
- **Behaviour against r156 and the Purpose:** no contradiction. Each commit is given with the work-item it belongs to, or none. No new observable behaviour beyond r156.

## Checks

- **`tools check --base ebbf1bea`:**
  - **ruff:** 19 errors. All of them are in files w217 did not touch: `.shop/work/i43/runs/review/2-apply/apply.py`, `tests/scenarios/supervision_branch_steps.py`, `tests/scenarios/test_supervision.py` and `tests/scripts/stub_claude.py`. They are the same 19 that branch review 1 found (its finding 3). None is in w217's two files.
  - **vulture:** clean.
  - **import-linter:** the project states no import contracts.
- **`tools size --limit 300`:** no output, so no file is over the limit.

## Commands run

- `git show --stat 9d61d97a`, `git show 9d61d97a -- scripts tests features`
- `git log --oneline ebbf1bea..9d61d97a --grep=w217`
- `grep -n` of `work add|withdraw|retry|answer` subjects in `scripts/workqueue.py` and `scripts/workqueue_answer.py`; `git log --format=%s ebbf1bea..9d61d97a`, filtered for those subjects
- `python3 <Scripts>/tools check --base ebbf1beaaa1fb5e4e3d29ffde673a5999a2cbd22`
- `python3 <Scripts>/tools size --limit 300`
- `python3 -m pytest -q -p no:cacheprovider tests/scripts/test_supervise_review_read.py`: 3 passed
- `git status --short`: clean
