# Branch review of i63

**Verdict: DONE.** No finding is Critical. None is triaged fix now. Every check has a run in the brief. Three findings are Important, all triaged observation:

1. `is_failed`'s clean-status assertion was loosened, not listed in the plan, under an allowance that does not hold (w236).
2. The r214–r216 scenarios pass without the code they pin (w237).
3. r215/r216 as worded still contradict what the code does for an i2 session's own end. The code follows reading A, as answered (w237).

`tools check` exits 1, on ruff only. The cause is a gate round's helper script committed under `.shop/` and two FURB167 hits on lines that were already there before this branch. It is triaged observation.

## Range and work-items

- Range: `db2873b7..331edbd4` (Base `db2873b73a08e86a12a10f8de97aae3b22914af6`, Head `331edbd40721c1a35432dbdda0f46b46d915832f`), branch `main`.
- **w236** (green), accepts supervision#r218. Code commits:
  - d8f57cc8: `scripts/supervise_faults.py`, `tests/scenarios/supervision_faults_steps.py`
  - 94f0a748: `tests/scenarios/supervision_faults_steps.py`
- **w237** (green), accepts supervision#r214, #r215, #r216. Code commits:
  - a9cb7536: `tests/scenarios/supervision_faults_steps.py`
  - fd8364d1: `tests/scripts/stub_claude.py`
- **Commits of no work-item:** the capability-proposal's rounds, notes, a request and two hand repairs (finding 6).

## Suite

Suite: 1084 passed, 0 failed at 331edbd in 33.36 s. The same run also gives 1 skipped, 16 xfailed, 6 xpassed and 56 subtests passed (exit 0). The command was `python3 -m pytest -q -n auto -rfEx -p work_items --work-item w236 --whole-suite`.

- **Parallel:** yes (`-n auto`, xdist).
- **In-process:** no. tests/scenarios/test_supervision.py:7 says the When "runs `work run` once as a program".
- The suite is under 60 s, so this is not a finding.
- **Dry-run against real mode:** the system has no dry-run mode of its own operations. The only `--dry-run` is git's push verification (supervise_faults.py:71, supervise_review.py:55). So no randomized agreement test is owed.

## Checks

All at 331edbd:

- **w236's check** (its scenarios, `pytest -q -n auto -p work_items --work-item w236`): exit 0, 181 passed, 1 skipped, 56 subtests passed, in 6.84 s.
- **w237's check** (its scenarios, `--work-item w237`): exit 0, 183 passed, 1 skipped, 56 subtests passed, in 4.61 s.
- **`tools check --base db2873b7`**: exit 1.
  - `== ruff ==`: 4 errors.
    - `.shop/work/i63/runs/supervision/1-gate/mk.py:1:1` I001
    - `.shop/work/i63/runs/supervision/1-gate/mk.py:10:93` SIM115
    - `tests/scripts/stub_claude.py:208:51` FURB167
    - `tests/scripts/stub_claude.py:209:51` FURB167

    See finding 7.
  - `== vulture ==`: clean.
  - `== import-linter ==`: "the project states no import contracts".
  - No heading says `missing`.
- **`tools size`** (default limit 300, per scripts/tools:57 and :106): exit 0, prints nothing.
  - No file the branch touched is over the limit, and none is named as already over.
  - `tests/scripts/stub_claude.py` is close to it: 289 lines by w237's 6-implement report, 293 by its review.
- **`features deprecated`**: exit 0, 20 deprecated scenarios.
  - The branch added one: supervision's r28 scenario, "for: removal".
  - One line was already there before the branch: "under a delegation, each question … `<reply>` (deprecated) | for: r209 and r210 | no scenario has that title". The branch does not touch it.
- **`features bindings`**: exit 0, "every binding names a scenario".

## Removed and weakened tests

I searched the Change for:
- deleted `def` of a test or step;
- dropped parametrize cases;
- `assert` lines removed or changed;
- `skip` or `xfail` added;
- scenarios renamed or removed under `features/`;
- changed `check=` behaviour in the stub.

What I found:

- **`tests/scenarios/supervision_faults_steps.py::is_failed`** (:148 at head; w236, 94f0a748): **weakened.**
  - Before: `git status --porcelain -- .shop/work` had to be empty after every scenario ending "w1 is failed, naming/recording …". The w236 review counts 7 such Then lines. This proved that `work run` leaves the main checkout's `.shop/work/` exactly as its last commit has it after a fault.
  - After: `:(exclude).shop/work/i2` is left out of that check for every one of those scenarios.
  - w236's plan, "Tests the decisions break", says "None", so the change is not listed.
  - The allowance row claimed for it does not hold (see Allowances).
  - This is finding 1.
- **The r28 scenario** (features/supervision.feature:569–571): tagged `@deprecated`, retitled with "(deprecated)", and given "Deprecated for: removal".
  - Its steps and Thens are unchanged, and it still runs and passes. A renamed test is the old test, and it is not weakened.
  - The change was made by the formulate round's commit 566b7302, not by a work-item.
- **`tests/scripts/stub_claude.py::bash`** (w237, fd8364d1): `check=command[0] == "git"` became `git_retry(...)`, which still calls `check_returncode()` on failure. A git failure still raises. Not weakened.
- Nothing else is removed or weakened. Every other test change only adds lines.

## Allowances

- **w236 3-implement:** "none".
- **w236 4-implement**, row `tests/scenarios/supervision_faults_steps.py::is_failed — setup/interim`: **does not hold.**
  - `setup` does not hold. The diff changes an `assert`: its pathspec, and with it what the assertion accepts.
  - `interim` does not hold. The old assertion is a `-` line of the `Base..HEAD` Change, so it was there at Base and was not first committed after it. The w236 review also dates it to 8172b9df, 2026-10-22.
  - The row claims more than it holds: Important (finding 1).
- **w236 5-implement:** "none".
- **w237 5-implement and 6-implement:** "none", and no existing test is changed. Nothing to verify.

## Cannot verify

None. Every check named in the brief (the suite, both work-items' scenarios, `tools check`, `tools size`, `features deprecated`, `features bindings`) has a run at 331edbd.

## Findings

### 1. Important · w236 · observation: `is_failed` loosened without a plan listing and under an allowance that does not hold

- **Where:** tests/scenarios/supervision_faults_steps.py:146–148 (commit 94f0a748).
- **What is wrong:**
  - The answer of 2026-10-29 asked to "make the code and the scenario's steps deterministic".
  - Instead, the shared Then stopped checking `.shop/work/i2` for every "w1 is failed …" scenario.
  - The plan does not list it, and the `setup/interim` row does not hold.
- **Why it matters:**
  - What the step now asserts matches r218's "less each path … of another initiative".
  - But the nondeterminism is hidden, not removed. In the r218 scenario, `two_sessions_change` has i1's researcher write `.shop/work/i2/initiative.md`. Whether i2's own run then puts it back and faults p2's gate round depends on timing.
  - The scenario passes either way, so the person's outcome for p2 (faulted or not) is not pinned.
- **Fix:**
  - Restore `is_failed`'s full check.
  - Give the r218 scenario its own clean-status Then, scoped to "less each other initiative's path".
  - Or list the change in w236's plan under "Tests the decisions break".
- **Test that would show the hidden outcome (not run):** the r218 scenario under `-n auto`, 20 times, asserting p2's `## Faults` stays empty (or always holds a fault).

### 2. Important · w237 · observation: the r214, r215 and r216 scenarios pass without the code they pin

- **Where:** tests/scenarios/supervision_faults_steps.py:58–66 (`i2_session_changes`, a9cb7536), with tests/scripts/stub_claude.py's `elsewhere` step (the write, then `git_retry` add and commit straight away, around :236–240).
- **What is wrong:**
  - p2's gate session waits only for i1's researcher to start. It then writes and commits i2's file at once.
  - So when i1's researcher ends, `git status` almost always shows nothing under `.shop/work/i2/`, and the skip at scripts/supervise_faults.py:114 (`others`, r214's rule) is not reached.
  - w237's plan, open case 1, asked the implementer to name what the scenario then exercises of r214. Neither report does.
  - Only the r218 scenario (w236's `two_sessions_change`) reaches line 114.
- **Why it matters:** three accepted requirements are pinned by scenarios that would most likely stay green with lines 110 and 114 removed.
- **Fix:** hold the i2 session's commit until after i1's researcher has ended, for example through the stub's meet or linger options keyed on the researcher's end. Or name in w237 that r214 is pinned by the r218 scenario.
- **Test that would show it (not run):** with supervise_faults.py:110 and :114 removed, run `pytest -q tests/scenarios/test_supervision.py -k "another_initiative or side_by_side"`. Expected today: the r214–r216 scenarios still pass and the r218 scenario fails.

### 3. Important · w237 · observation: r215 and r216, as worded, contradict what the code does when one of i2's own sessions ends

- **Where:**
  - scripts/supervise_faults.py:110–120: `others` leaves out only the *other* runs' parts, so a run checks its own part in full.
  - scripts/supervise_worker.py:189–199: `Fault` is raised for what that check returns.
  - spec/capabilities/supervision.md:162–164.
- **What is wrong:**
  - Take this case: a session of i2 changes `.shop/work/i2/initiative.md` while a session of i1 works, and leaves it uncommitted. Then one of i2's sessions ends.
  - i2's check puts the change back and faults that i2 session.
  - r215 ("put back no change of that path") and r216 ("fault no session for that change") cover exactly this change, because it was made "by a session of that initiative, while a session of one initiative worked".
  - Seen from i2's own run, r218 says the opposite.
  - w237's answer (2026-10-29, reading A) chose r218 for i2's own sessions, but the capability's lines were not narrowed.
- **Why it matters:** the capability promises the person something the code does not do, and nothing in the spec records the ruling.
- **Reproduction (from a run's output in what I read):**
  - w237's 6-implement report: "the stub died after writing the file, and p2's gate round was faulted for an uncommitted change".
  - w236's work-item answer: "On a failure w1 is not failed and .shop/work/i2/initiative.md is left modified."
  - In both, an i2 session was faulted, or its change put back, for an i2 change made while i1's researcher worked.
- **Fix:** write the ruling as lines first, through integrating-a-proposal, for example: r215/r216 "… then `work run` shall, in what it checks for the one initiative's session, put back no change …". Or keep the lines and record the change's writer, which is reading B.

### 4. Minor · w237 · observation: w237's `fileset` does not name `tests/scripts/stub_claude.py`

- **Where:** .shop/work/i63/w237.md:8.
- **What is wrong:** commit fd8364d1 changes stub_claude.py. The answer of 2026-10-29 said to add it to the file set, but the frontmatter lists only `scripts/supervise_faults.py` and `tests/scenarios/supervision_faults_steps.py`.
- **Why it matters:** design-decision/the-file-set-is-the-claim says the set "names every file the work-item changes". `work run` would not have kept a parallel implementer off the file. No harm came of it here.
- **Fix:** `work claim` the file, or record it in `fileset:`.

### 5. Minor · w237 · observation: the stub's retry depends on git's message wording

- **Where:** tests/scripts/stub_claude.py `git_retry` (around :112–120).
- **What is wrong:** the retry is chosen by `"index.lock" in done.stderr`. Under a non-English locale git's message may differ, so the retry would not happen and the flake w237 fixed would come back. The 10 s bound is also not justified anywhere.
- **Fix:** run the stub's git with `LC_ALL=C`, or test for `.git/index.lock` itself.

### 6. Minor · none · observation: commits that belong to no work-item

Every commit before a1dcd387, plus a411ea7a, f6cebaad and c490ee84, has no work-item. They are:

- the initiative's own transitions and `work note: i63` commits;
- the capability-proposal's rounds:
  - transitions: ac7edff0 … d3f63778;
  - spec commits: 446d8708, 1af90a20;
  - features commits: 566b7302, 61c39f01;
- `work answer: supervision` (31f4f6ed);
- `work request: q43` (c490ee84);
- **two hand repairs** of the proposal's ids, made outside `work run`'s rounds: 28ce4056 and a411ea7a, both citing q34.

The spec and features commits are the proposal's apply and formulate rounds, the path through which lines and scenarios reach the repository. They are therefore not a change under `features/` by a work-item. Neither the subjects nor the two work-item reviews show a work-item commit touching `features/`.

The hand repairs are the finding: the apply round dropped r214–r216 from the proposal's ids twice, and the ids were restored by hand. That is q34's defect; nothing in this branch fixes it.

### 7. Minor · none / w237 · observation: `tools check` fails on ruff

- **Where:**
  - `.shop/work/i63/runs/supervision/1-gate/mk.py:1` and `:10`: a gate session's helper script, which writes its `result.json`. It was kept into the run directory and committed.
  - `tests/scripts/stub_claude.py:208–209` (FURB167 `re.M`): lines w237 did not change, in a file it touched. They were there before the branch.
- **Fix:** either have `tools check` leave out `.shop/`, or keep sessions' scratch scripts out of the kept stage directory. Replace `re.M` with `re.MULTILINE` (cheap).
- **Reproduction:** the brief's `tools check --base db2873b7` output, exit 1.

### 8. Minor · w236 · observation: `Run.worker`'s docstring is stale

- **Where:** scripts/supervise_worker.py:174–177.
- **What is wrong:** it still says every uncommitted change under `.shop/work/` in the main checkout "is put back too, and is the work-item's fault (r28)". r28 is retired, and other side-by-side initiatives' parts are now left out (r214, r218).
- **Fix:** cite r214/r218 and the exception. The file was outside both file sets; w237's plan named this.

### 9. Minor · w236 · drop: porcelain lines that are renames or quoted paths

- **Where:** scripts/supervise_faults.py:113.
- **What is wrong:** `line[3:].strip('"')` reads `R old -> new` as one path, and does not unescape C-quoted paths. This predates the branch, and the new `others` prefix test inherits it.
- **Fix:** `git status --porcelain -z`.

## Feature files

- **Deprecated scenario whose replacement's work-item is green:**
  - The r28 scenario (features/supervision.feature:569–571) is "Deprecated for: removal". r28 is retired, and r218, whose behaviour it carries, is w236's, which is green.
  - The scenario still runs and passes: `another_session_changes` drives a group of one.
  - No work-item lists it under Retires, so it stays until one does.
- **A scenario removed that was not deprecated:** none.
- **A binding that names no scenario:** none ("every binding names a scenario").
- **Already present, not this branch's:** the deprecated scenario whose replacement is "r209 and r210", and for which `features deprecated` says "no scenario has that title".

## Shape (CLAUDE.md)

- **Size limit (300):** met, at 331edbd.
  - `scripts/supervise_faults.py`: about 198 lines (194 before, +4).
  - `tests/scenarios/supervision_faults_steps.py`: 243 lines (w237 review).
  - `tests/scripts/stub_claude.py`: 289 lines by the 6-implement report, 293 by the w237 review. It has 7–11 lines left, so the next change to it should split it.
- **Module map:**
  - `scripts/supervise*.py`: met. The faults check stays in supervise_faults.py:104–129, beside the faults concern.
  - `tests/scenarios/` "one `<capability>_*_steps.py` module a concern": met. The new Given and Thens are in supervision_faults_steps.py:49–99, the faults concern.
  - `tests/scripts/`: stub_claude.py is the stand-in for `claude`, not a test. It was already so before the branch, and the branch touched it only for the retry.
- **Code no scenario reaches any more:** none yet.
  - `another_session_changes` (supervision_faults_steps.py:~42–46) is reached only by the deprecated r28 scenario, and goes unreached when that scenario is retired. Its retirement should take this step with it.
  - Check that would show it complete: `vulture` and `features bindings` clean after the r28 scenario's removal.
- **Code no line asks for:** none.
  - `others` (supervise_faults.py:110, :114) serves r214/r218.
  - `git_retry` is test-double mechanism with no observable behaviour of `work run`.
  - The four new Thens and two Givens are bound to the r214–r218 scenarios.

## Coupling

- **git `status --porcelain` (v1):** a published, stable format. The code relies on more than it publishes in two ways: a fixed 3-column prefix with one path, which breaks on renames and C-quoted paths (finding 9). Made stable by `-z`.
- **git's stderr wording "index.lock"** (stub_claude.py `git_retry`): not a published contract. It is locale- and version-dependent and breaks silently, giving no retry. Made stable by `LC_ALL=C` or by testing for the lock file (finding 5).
- **pytest-bdd:** the suite warns `PytestRemovedIn10Warning` from pytest_bdd/compat.py:28 (`_register_fixture` with a nodeid). This is pytest-bdd's own use of pytest internals and was there before the branch. It breaks with pytest 10 unless pytest-bdd is pinned or upgraded.
- The unregistered marks `r214`, `r215`, `r216` and `r218` add to the existing `PytestUnknownMarkWarning`s. That is harmless, but `--strict-markers` would fail them.

## Observations

All one line each.

- **is_failed loosened:** in the brief's Change, the `-` line `assert git(repo, "status", "--porcelain", "--", ".shop/work") == ""` became the `+` line `... ":(exclude).shop/work/i2") == ""` (supervision_faults_steps.py:148).
- **r214–r216 do not reach line 114:** the `i2_session_changes` plan is `round:gate:p2` → `meet_agents: ["code-scout"]` → `elsewhere.commit`, and the stub writes and then commits with no wait between. Not run: remove supervise_faults.py:110/:114 and run the three scenarios.
- **r215/r216 against code:** w237 6-implement says "p2's gate round was faulted for an uncommitted change"; w236's answer says ".shop/work/i2/initiative.md is left modified".
- **w237 fileset:** w237.md:8 lists 2 files, and fd8364d1 changes `tests/scripts/stub_claude.py`.
- **Stub retry locale:** `git_retry` matches `"index.lock" in done.stderr`. Not run: the r215 scenario under `-n auto` with `LANG=de_DE.UTF-8`, 20 times.
- **tools check:** ruff gives `mk.py:1:1 I001`, `mk.py:10:93 SIM115`, `stub_claude.py:208:51` and `:209:51 FURB167`; exit 1.
- **Stale docstring:** supervise_worker.py:176 says "is the work-item's fault (r28)", and r28 is in supervision.md's `retired:`.
- **Porcelain rename:** supervise_faults.py:113 `path = line[3:].strip('"')`. Not run: a porcelain line `R  .shop/work/i2/a -> .shop/work/i2/b` gives the path `".shop/work/i2/a -> .shop/work/i2/b"`.
- **Hand repairs:** commits 28ce4056 and a411ea7a, "supervision proposal ids restored … (q34)".
- **6 xpassed:** the suite gives 6 xpassed, unchanged from w236's branch run. Expected failures that pass are not this branch's, but they hide when a held scenario turns green.
