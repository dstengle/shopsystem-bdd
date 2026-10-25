# Review of w134

**Verdict: DONE_WITH_CONCERNS.** One finding is triaged fix now (Important): a no-initiative `work run` can exit
successfully after one initiative's thread crashed. The rest is sound. No change under `features/`, no test removed
or weakened, and the lint, dead-code and size checks are clean.

## Commits reviewed

The branch `work/w134` is gone, so I took the commits between `9cc45b1 work: w134 ready -> claimed` and
`d9571b5 work: w134 claimed -> done` on the checked-out branch, less `work run`'s `work:` commits (w154/w155
transitions 6f45945, 2eab4f4, 7422b3a, 03c6d2e, 1467128):

- `8f54c17` work run with no initiative takes every open initiative side by side (supervision r66, r81, r82):
  CLAUDE.md, scripts/{work, supervise.py, supervise_all.py (new), supervise_faults.py, supervise_pool.py,
  supervise_review.py, supervise_worker.py}, tests/scenarios/{supervision_all_steps.py (new), test_supervision.py}.

The implementer's result.json gives no hash in `commits` ("see git log work/w134: work run with no initiative ...").
That message matches 8f54c17 and only 8f54c17, so the commit is the one it means (Minor finding 5).

## Removed and weakened tests

None. I looked at `git diff 9cc45b1 d9571b5 -- tests/ features/`. It holds only additions: the new
`supervision_all_steps.py` (136 lines) and one import line in `test_supervision.py`. No test function is deleted, no
parametrize case dropped, no assertion changed, and no skip or xfail added. Nothing under `features/` changed. The
plan's "Tests the decisions break" says none, which agrees.

## Allowances

The report's `## Tests changed under an allowance` says "none", and the commits agree: no existing test changed.

## Cannot verify

- The report's green runs: `--work-item w134` 147 passed, 1 skipped; `--whole-suite` on test_supervision.py 155
  passed, 7 xfailed, four times in a row. I did not re-run them, because `work run` runs the suite before it merges.
- The report says r66 failed "about one run in four" on a push race before the push lock. Whether the lock removes
  every such flake cannot be seen from the commits.
- The report says the semaphore is "taken around every `claude -p` session". That is not so for the analysis session
  (finding 3).

## Findings

### 1. Important: a crashed initiative thread can end in exit 0 (fix now)
- **Where:** scripts/supervise_all.py:27-31 and :46-48.
- **What is wrong:** `take()` catches only `Refused`. Any other exception from `pull_through()` (`GitFailed`, `Fault`,
  `OSError`) ends that thread with a traceback from `threading.excepthook`. `run_all` then goes on and builds the exit
  code from node statuses alone. When the crashed initiative's nodes are, say, `drafted` or `researched`, nothing is
  failed or awaiting-answer, so `work run` exits 0.
- **Why it matters:** with one initiative the same exception propagates and `work run` exits non-zero. r82 asks for
  exit 0 only when no node of a taken initiative can make a transition, and a crashed initiative's nodes still can.
  So this is a wrong answer: the person and `work run`'s callers are told everything finished. It is also reachable:
  several git commands in the main checkout run outside the run's lock (finding 2), so `index.lock` races between
  threads raise `GitFailed`.
- **Fix:** catch `Exception` in `take()` (or record it in a `crashed` map next to `refused`). Name the initiative and
  the exception on stderr, and return 1 when any thread raised.

### 2. Important: commits in the main checkout outside the shared lock race across initiatives (observation)
- **Where:** checkout writes and commits that run without `self.lock` and were safe while only one initiative ran:
  - `Rounds.keep_round` (scripts/supervise_rounds.py:86-89, `git add` and `git commit`);
  - `git merge --abort` (scripts/supervise_rounds.py:68);
  - `Answers.answers`: `self.section(...)` and `self.commit(name, before, before)` (scripts/supervise_answers.py:74, :80);
  - `Drafts.draft_proposals` and `fix_work_item`: `workqueue.add`, which writes the file and commits;
  - `Merge.merge`: `git merge --ff-only` (supervise_merge.py:133). This one is probably safe: it runs under the lock
    taken at :104, but I did not trace every caller.
- **What is wrong:** plan decision 4 asks for "one lock over every change to the main checkout, its commits and pushes
  included". w134 put the branch review, `git_push` and the worker's end under the shared lock, but not these sites.
  - Two threads committing at once can fail with `fatal: Unable to create '.git/index.lock': File exists`, raised as
    `GitFailed`, which leads to finding 1.
  - A file that one initiative has written but not yet committed (an `## Answers` bullet, a drafted work-item) is not
    in any run's `own` or `unlogged`. Another initiative's worker ending inside that window would have
    `checkout_changes` (r28) put the file back and fail its own work-item, naming the other initiative's file.
- **Reproduction:** none run. The fault depends on timing: two initiatives, one faulting a round or answering under a
  delegation while the other's worker ends. Found by `grep -n '"commit"\|self.commit(\|"merge"\|"add"\|with self.lock'
  scripts/supervise*.py` and by reading each site.
- **Fix:** take `self.lock` around `keep_round`'s add, commit and merge-abort, around the answers' section-and-commit,
  and around drafting's `workqueue.add`. Or register those writes in `own` until they are committed.

### 3. Minor: the analysis session does not take the shared session slot (observation)
- **Where:** scripts/supervise_analysis.py:61.
- **What is wrong:** `self.session(...)` for the analysis runs without `with self.slots`. With several initiatives,
  one initiative's analysis can run while the others' workers already fill `.shop/delivery.toml`'s limit. That makes
  limit + 1 sessions. r60 speaks of "workers", so whether the analysis session counts is arguable. Plan decision 4
  says round sessions are included, and the report claims every session takes a slot.
- **Fix:** wrap the call in `with self.slots:`, as w134 did for the branch review.

### 4. Minor: scripts/supervise_review.py was edited outside the file set (observation)
- **What happened:** the report's "Outside the file set" says so, with its reason: the branch review's
  copy-and-commit raced another initiative's r28 check. The change is needed and sound: the copy, the log and the
  commit now run under the lock, and the kept directory is in `own` while uncommitted.
- **Why it matters:** the file set is the claim (design-decision/the-file-set-is-the-claim). Another work-item
  claiming supervise_review.py at the same time would have got no conflict warning. Any clash would surface at rebase.
- **Fix:** nothing to do now. Noted for the initiative's record.

### 5. Minor: the implementer's result.json `commits` holds prose, not hashes (drop)
- **What is wrong:** `"commits": ["see git log work/w134: ..."]` names no commit, so a reviewer cannot check the
  listed commits against the branch mechanically. It was matched by its message here.

### 6. Minor: a no-op filter in supervise_all.py:43 (drop)
- **What is wrong:** `if n != run.initiative` in the proposals list never removes anything. `proposals()` returns
  file stems, and the initiative's file is `initiative.md`, so its stem is "initiative", not the initiative's name.

## Behaviour against the lines

- **r66:** every open initiative is taken through `open_names`; done and abandoned ones are excluded. Each initiative
  runs in a thread with its own `Run`, and its order is unchanged (answers, rounds, drafting, pool), so one session of
  an initiative runs at a time.
- **r81 and r82:** each taken initiative is printed with its status, then its nodes. The exit is 1 on a failed node or
  a refusal, 3 on awaiting-answer, else 0. With no open initiative it prints nothing and exits 0.
- **Answer of 2026-10-24 (Reading A):** w134 builds no gate round, and every initiative uses the one checked-out
  branch.
- **Code no line asks for:** none found. Printing proposals' statuses and naming a refusal on stderr serve r81/r82's
  "printing the status of each initiative".

## Outside these commits (not w134's)

`Answers.answers` writes the answer to question 1 into the file and then asks question 2. That second session's
worker end runs `checkout_changes`, which would put back answer 1, since the file is not in `own`. That holds even in
a run of one initiative. It is a risk of the commits that built supervise_answers.py, not of w134's.

## Commands run

- `git log --format=%H -1 --grep="^work: w134 ready -> claimed$" work/w134` → unknown revision (branch gone)
- `git log --format='%H %s' -1 --grep=...ready -> claimed$` / `...claimed -> done$` → 9cc45b1 / d9571b5
- `git log --format='%h %an %s' 9cc45b1..d9571b5`
- `git show --stat 8f54c17`; `git show 8f54c17 -- scripts/ CLAUDE.md tests/scenarios/test_supervision.py`;
  `git show 8f54c17:tests/scenarios/supervision_all_steps.py`
- `git diff --stat 9cc45b1 d9571b5 -- features/ tests/` → only the two test files, additions only
- `grep` for lock, commit, session and `slots` sites in scripts/supervise*.py; `grep "meet"` in tests/ and scripts/
  (the stub supports `meet`)
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 9cc45b191bb3...`:
  - ruff: All checks passed
  - vulture: clean
  - import-linter: no contracts stated
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` → prints nothing. The touched files are at
  most 247 lines (supervise.py).
