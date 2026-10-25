# Review of w134 (second review, after the answer of 2026-10-25)

**Verdict: DONE.** No finding is Critical, and none is triaged fix now. The first review's one fix-now finding
(a thread that crashes can end in exit 0) is now an observation. The person's answer of 2026-10-25 accepts the
work-item as it stands and records that case for a later line. No change under `features/`, no test removed or
weakened, and ruff, vulture and size are clean.

## Commits reviewed

The branch `work/w134` is gone: `git log ... work/w134` gives "unknown revision". So I took the commits between
`9cc45b1 work: w134 ready -> claimed` and `d9571b5 work: w134 claimed -> done` on the checked-out branch. I left out
`work run`'s `work:` commits, which are w154's and w155's transitions: 6f45945, 2eab4f4, 7422b3a, 03c6d2e and 1467128.

- `8f54c17` work run with no initiative takes every open initiative side by side (supervision r66, r81, r82).
  It changes CLAUDE.md and scripts/{work, supervise.py, supervise_all.py (new), supervise_faults.py, supervise_pool.py,
  supervise_review.py, supervise_worker.py}. It adds tests/scenarios/supervision_all_steps.py and changes
  tests/scenarios/test_supervision.py (one line).

The `commits` field of the implementer's result.json gives no hash: it says "see git log work/w134: work run with no
initiative ...". That message matches 8f54c17 and only 8f54c17, so the two agree (Minor 5).

## Removed and weakened tests

None. `git diff --stat 9cc45b1 d9571b5 -- features/ tests/` shows additions only: the new
`supervision_all_steps.py` (136 lines) and one import line in `test_supervision.py`. I searched for deleted test
functions, dropped parametrize cases, changed asserts and added skip or xfail, and found none. Nothing under
`features/` changed. The plan's "Tests the decisions break" also says none.

## Allowances

The report's `## Tests changed under an allowance` says "none". The commits agree: no existing test changed.

## Cannot verify

- The report's green runs: `--work-item w134` gave 147 passed, 1 skipped, and `--whole-suite` on
  test_supervision.py gave 155 passed, 7 xfailed, four times. I did not re-run the suite, because `work run` runs it
  before it merges.
- The report says r66 failed about one run in four on a push race until `git_push` took the lock. The commits cannot
  show whether every such flake is gone.
- The report says `slots` is taken around every `claude -p` session. That is not so for the analysis session
  (Minor 3).

## Findings

### 1. Important: an initiative thread that crashes can end in exit 0 (observation, by the answer of 2026-10-25)
- **Where:** scripts/supervise_all.py:27-31 and :46-48.
- **What is wrong:** `take()` catches only `Refused`. A `GitFailed`, `Fault` or `OSError` from `pull_through()`
  ends that thread, and `threading.excepthook` only prints it. The exit code then comes from node statuses alone, so
  it can be 0 although the crashed initiative's nodes can still move. With one initiative, the same exception exits
  non-zero.
- **Triage:** the first review triaged this fix now. The person's answer of 2026-10-25 accepts the work-item as it
  stands: no line pins this case, and it is recorded as an observation for a later line (commit 217fe11).
- **Reproduction:** none run here. It needs a `GitFailed` timed inside one thread, and this session may run no
  Python other than pytest. The reasoning is a reading of the code: `take` catches only `Refused`, and :46-48 read
  only `refused` and `nodes`.
- **Fix (for the later line):** record any other exception in `take()` next to `refused`, name the initiative on
  stderr, and exit 1.

### 2. Important: some writes to the main checkout run outside the shared lock (observation)
- **Where:**
  - `Rounds.keep_round`: the add and commit at scripts/supervise_rounds.py:86-89, and `merge --abort` at :68;
  - the section and commit of the delegated answers in scripts/supervise_answers.py;
  - `workqueue.add` in drafting.
- **What is wrong:** plan decision 4 asks for "one lock over every change to the main checkout". These writes were
  safe while only one initiative ran. With several initiatives, two threads can race on `.git/index.lock`, which
  leads to finding 1. Another initiative's worker can also end while such a file is written but not committed, and
  r28's `checkout_changes` would then put that file back.
- **Reproduction:** none. It depends on timing. Found by reading `with self.lock` against the git calls; see
  `grep -n "self.lock\b|git_push(" scripts/supervise*.py` below.
- **Fix:** take `self.lock` around these writes, or register them in `own` until they are committed.

### 3. Minor: the analysis session takes no shared slot (observation)
- **Where:** scripts/supervise_analysis.py:61. `self.session(...)` runs without `with self.slots`.
- **What is wrong:** an analysis can run while the other initiatives' workers already fill the limit, which makes
  limit + 1 sessions. r60 speaks of workers, so whether the analysis counts is arguable.
- **Fix:** wrap the call in `with self.slots:`.

### 4. Minor: supervise_review.py was edited outside the file set (observation)
- **What happened:** the report discloses it and gives the reason: the branch review's copy and commit raced
  another initiative's r28 check.
- **Verified:** the copy, the log and the commit now run under `self.lock`. The kept directory is in `own` until it
  is committed. The session takes a slot outside the lock, so the semaphore and the lock cannot deadlock.
- **Why it matters:** the claim on supervise_review.py was not declared (design-decision/the-file-set-is-the-claim).
- **Fix:** nothing to do now. It is noted for the initiative's record.

### 5. Minor: the `commits` field of result.json holds prose, not hashes (drop)

### 6. Minor: a filter that never removes anything (drop)
- **Where:** supervise_all.py:43, `n != run.initiative`.
- **Why:** `proposals()` keeps only `kind: capability-proposal` files, and `initiative.md`'s stem is "initiative", so
  the filter never removes anything.

## Behaviour against the lines

- **r66:** `open_names` leaves out initiatives that are done or abandoned. Each taken initiative runs in its own
  thread with its own `Run`, and keeps its own order (answers, rounds, draft, pull). The step "no two sessions of i1
  ran at the same time" checks the order within an initiative, and the gate-meet step checks that the initiatives
  run side by side.
- **r81 and r82:** each initiative is printed with its status, then its nodes. The exit is 1 on a failed node or a
  refusal, 3 on awaiting-answer, and 0 otherwise. With no open initiative, nothing is printed and the exit is 0.
- **r60:** one `Semaphore(limit)` is shared and taken around the workers' sessions and the branch review's session.
  `read_delivery` sets a semaphore per run during `check()`, and `run_all` then replaces it with the shared one. So
  the shared semaphore is the one that counts.
- **Risk checked:** `git_push` now takes `self.lock`, and it is called while the lock is already held (for example
  at supervise_faults.py:82-87). `self.lock` is a `threading.RLock` (supervise.py:53, supervise_all.py:20), so it
  cannot deadlock.
- **Answer of 2026-10-24 (Reading A):** w134 adds no gate round, and every initiative commits on the one
  checked-out branch.
- **Code no line asks for:** none. The proposals' statuses and a refusal named on stderr serve r81/r82's "printing
  the status of each initiative it took".

## Commands run

- `git log --format=%H -1 --grep="^work: w134 ready -> claimed$" work/w134` gave "unknown revision" (the branch is
  gone).
- `git log --format='%H %s' --grep="^work: w134 "` gave 9cc45b1 (ready -> claimed) and d9571b5 (claimed -> done).
- `git log --format='%h %s' 9cc45b1..d9571b5`
- `git log --stat ... --invert-grep --grep='^work: '`
- `git show 8f54c17 -- scripts CLAUDE.md tests/scenarios/test_supervision.py`
- `git show 8f54c17:tests/scenarios/supervision_all_steps.py`
- `git diff --stat 9cc45b1 d9571b5 -- features/ tests/` showed additions only.
- `grep -n "self.lock\b|self.lock =|git_push(|Semaphore|self.limit" scripts/supervise*.py`
- `grep -n -B3 "self.session(" scripts/supervise*.py`
- `grep` for `questions`, `faulted`, `proposals` and `items` in scripts/supervise*.py
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 9cc45b191bb3...`:
  - ruff: All checks passed!
  - vulture: clean
  - import-linter: the project states no import contracts
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` printed nothing. The touched files are at
  most 251 lines.
