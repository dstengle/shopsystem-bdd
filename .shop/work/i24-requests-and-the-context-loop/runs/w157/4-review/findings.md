# Review of w157 (supervision#r77, branch review 1 F1)

**Verdict: DONE.** The change does what the plan's D1 and D2 say. Nothing under `features/` changed. No test was removed or weakened. The focused scenarios pass. There are two Minor findings, neither triaged fix now.

## Commits reviewed

The branch `work/w157` no longer exists. The commits were therefore taken from HEAD, between `bc5b8c1 work: w157 ready -> claimed` and `c2bb101 work: w157 claimed -> done`, leaving out `work run`'s own `work:` commits:

- `6e6d314 work run commits each delegated answer as it is written (r77)`. It changes `scripts/supervise_answers.py` (+9/-2), `tests/scenarios/supervision_delegation_steps.py` (+28) and `tests/scripts/stub_claude.py` (+5/-2).

The same range also holds `d04cc02 work retry back to green runs the done check (F5)`, which is w160's commit, not w157's.

The implementer's result lists `c4db04a`. `6e6d314` is that commit rebased at merge: the two have the same message and the same per-file stat, and `git diff c4db04a 6e6d314` differs only in other work-items' files (w158–w161 runs, the log, and w160's `scripts/workqueue.py`). This is no finding.

## Removed and weakened tests

None. The diff only adds to test files: two Givens and one Then in `supervision_delegation_steps.py`, plus a `question:` plan key in `stub_claude.py`. The plan key is merged last, so a plan without one gives the same step as before.

What I searched for: deleted `def` lines, removed or changed `assert` lines, parametrize lists, and added `skip`/`xfail` in the diff. I found none.

## Allowances

The report's `## Tests changed under an allowance` says "none". The commits agree: no existing test is changed.

## Cannot verify

- The report's figure for the suite at its start (823 passed, 1 failed). I did not run the whole suite, by rule.
- The red run the report describes (the `ValueError` on w1's answer, and the stderr naming w1.md as put back). It cannot be replayed without reverting the change. The mechanism is consistent with the code: `checkout_changes` runs at a worker's end (r28).

## Findings

### F1. Minor (observation): new ruff FURB167 at two lines the commits added

- **Where:** `tests/scenarios/supervision_delegation_steps.py:144` and `tests/scripts/stub_claude.py:184` use the alias `re.M`.
- **Why it matters:** `tools check` now reports these lines. Line 119 of the same steps file already uses `re.MULTILINE`.
- **Already there before:** `stub_claude.py:183` (`kind = ...`) was already flagged before these commits. `scripts/workqueue.py:244` I001 is w160's.
- **Fix:** write `re.MULTILINE` on both lines.
- **Reproduction:** `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base bc5b8c1...` lists 4 ruff errors, these two among them.
- **Belongs to:** w157.

### F2. Minor (observation): the per-answer commit is taken outside `self.lock`

- **Where:** `scripts/supervise_answers.py:76` (and the closing commit at `:81`) call `self.commit(...)`, and `:74` calls `self.section(...)`, without holding `self.lock`. `move()` (`supervise.py:110`) and `fail()` do hold it.
- **The risk I checked:** `supervise_all` runs several initiatives side by side in one checkout. Two of them could commit at once and collide on the git index.
- **What I found:** `answers()` runs at the start of `pull_through` (`supervise.py:201`), before this initiative's pool, so this initiative's own workers cannot collide with it. Another initiative's run could. The old closing commit and `section()` were already outside the lock, so this is not new. The change only adds one commit per answer.
- **Fix:** wrap the write and the commit in `with self.lock:`.
- **Reproduction:** none. No scenario runs two initiatives under a delegation together. This is hardening.
- **Belongs to:** w157.

### Checked and found sound

- **r28:** each answer is committed (with its run directory and the log) before the next session starts. `checkout_changes` stays exempt-free, so the r28 scenario still holds.
- **r38:** `commit()` pushes after each commit.
- **r89/r90:** a session that faults still raises from `ask()` after `keep_round`, before any per-answer commit. A session that leaves the question writes no answer, and its run directory is committed by the closing commit, because `uncommitted()` sees it.
- **The new `uncommitted()` guard:** it only skips a commit that would have been empty. Before, an empty closing commit would have raised a GitFailed. This handles the plan's open case 2. The commit message `work: <name> <s> -> <s>` is Implementation-level.
- **No code beyond the lines:** every new behaviour (a commit and push per answer) serves r77 together with r28/r38. The stand-in key and the steps are test aids.

## Commands run

- `git log --grep` to find the claim and done commits. `git log bc5b8c1..c2bb101`, `git show 6e6d314`, `git show --stat c4db04a`, `git diff c4db04a 6e6d314 --stat`.
- `git diff bc5b8c1 6e6d314 --stat -- features/`: empty.
- `python3 -m pytest -q tests/scenarios/test_supervision.py -k delegation`: 3 passed (the r77 outline's two examples and the new scenario).
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base bc5b8c14b3b6bc3b2e8788a42b69438ce88ffc7d`, by heading:
  - ruff: 4 errors (2 of them w157's, see F1).
  - vulture: clean.
  - import-linter: no contracts.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: printed nothing. The touched files have 128, 175 and 263 lines.
- `grep` for `re.M`, `self.lock` and `.answers()`, and reads of `supervise.py` (`commit`, `move`, `pull_through`).
