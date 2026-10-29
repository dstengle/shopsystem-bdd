# Review of w237 (supervision r214, r215, r216)

**Verdict: DONE.** Nothing is Critical and nothing is triaged fix now. One Important finding: the r214 scenario does not, in the usual case, exercise the leaving-out it pins. It is triaged observation. Three Minor findings follow it.

## Commits reviewed

- a9cb7536 "Steps for r214-r216: another initiative's change is not checked, put back or faulted": tests/scenarios/supervision_faults_steps.py, +36 lines.
- fd8364d1 "stub_claude: git commands retry while index.lock is held": tests/scripts/stub_claude.py, +15/-4 lines.

How they match the implementer's results:
- 5-implement's result names 482257b0. `git diff 482257b0 a9cb7536 --stat` differs only under `.shop/`, so it is the same change as work run merged it.
- 6-implement's result gives no hash ("see git log: ..."). Its subject matches fd8364d1.
- No difference beyond that.

Suite: taken from the brief's record, 1084 passed and 0 failed at fd8364d1. The expected failures listed there are requests and work-queue scenarios unrelated to w237.

## Removed and weakened tests

None.
- What I searched for: removed `def test_`, removed or loosened `assert`, parametrize cases dropped, skip or xfail added, changed existing steps.
- What I found: the diff to supervision_faults_steps.py only adds lines. The diff to stub_claude.py changes how the stand-in runs git and asserts nothing.
- The plan's "Tests the decisions break" says none, and none was broken.

## Allowances

The report's `## Tests changed under an allowance` is "none" in both 5-implement and 6-implement. Nothing to verify.

## Cannot verify

- That the scenarios hold "on every run, alone and under -n auto", as the answer requires. The report claims three green runs in a row. I ran the three scenarios once (3 passed). One run cannot show the flake is gone.
- Whether 10 s is a long enough bound for `git_retry` on a loaded CI machine.

## Findings

### 1. Important, observation: the r214 scenario passes without the leaving-out it pins
**Where:** tests/scenarios/supervision_faults_steps.py:59-67 (`i2_session_changes`), with tests/scripts/stub_claude.py:224-240.

**What is wrong:** p2's gate session waits for i1's researcher (code-scout) to start. Then the stub's `elsewhere` step writes `.shop/work/i2/initiative.md` and commits it straight away (`git_retry(["add", ...])`, `git_retry(["commit", ...])`), before the gate session ends. The i2 path is uncommitted only for the moment between the write and the commit.

When i1's researcher ends, `Faults.checkout_changes` (scripts/supervise_faults.py:104-129) runs `git status`. That status almost always shows nothing under `.shop/work/i2/`, so the skip at line 114 (`others`, which is r214's rule) is not reached. Removing lines 110 and 114 would most likely leave all three scenarios green.

The plan's open case 1 asked the implementer to say what the scenario exercises of r214 if the stub could not hold i2's commit until after the researcher's end. Neither report says.

**Why it matters:** r214 is accepted with a scenario that does not, in the usual case, pin it. r215 and r216 still hold as outcomes.

**Fix:** keep the i2 file uncommitted until i1's researcher has ended. For example, the gate step waits on `ended_in` or lingers before the commit, or the researcher itself is held until after the write. Alternatively, name in the work-item that r214 is pinned by the earlier `two_sessions_change` scenario (r218) and not by this one.

**Reproduction (reasoning, not run):** the stub's order in `main` is meet_agents, then the `elsewhere` write and commit, then the result. No wait sits between the write and the commit. I did not edit code to prove it, because the review changes nothing.

### 2. Minor, drop: the Given's step commits what its text says is left uncommitted
**Where:** tests/scenarios/supervision_faults_steps.py:59-60.

**What is wrong:** the scenario's Given says the i2 session changes the file "without committing it". The step commits it, as "another session's commit", inside that session.

**Why it is minor:** this follows the coordinator's answer ("that i2 session's own end takes it in"), and the docstring says so. The step's words and what it does still differ. Finding 1 is the consequence.

**Fix:** none in the steps. If the line's wording is to change, it goes through the features binding.

### 3. Minor, drop: the work-item's `fileset` does not list tests/scripts/stub_claude.py
**Where:** .shop/work/i63/w237.md:8.

**What is wrong:** the answer of 2026-10-29 says to add stub_claude.py to w237's file set. The frontmatter still lists only the two original files, and the commit fd8364d1 changes stub_claude.py.

**Fix:** add it to `fileset` (the work-item file is work run's or the coordinator's to edit).

### 4. Minor, drop: ruff reports FURB167 in stub_claude.py, already there before w237
**Where:** tests/scripts/stub_claude.py:208-209.

**What is wrong:** `tools check` reports two FURB167 (`re.M`) on lines w237's commits did not change. They come from the file being touched. Already present at the base.

## Checks

- `tools check --base eeb9110e` (the claim commit):
  - ruff: 2 errors, both FURB167 at stub_claude.py:208-209, already there before w237 (finding 4).
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: prints nothing. supervision_faults_steps.py has 243 lines and stub_claude.py has 293.
- No change under `features/`. No production code changed, as reading A and D3 require.
- `git_retry` in `bash()` keeps the old behaviour of raising on a git failure (`check_returncode`), and non-git commands are unchanged.

## Commands run

- `git log --stat a9cb7536^..fd8364d1`; `git diff a9cb7536^ fd8364d1`
- `git log --oneline -3 482257b0`; `git log --oneline -8`; `git diff 482257b0 a9cb7536 --stat`
- `sed -n 180,260p tests/scripts/stub_claude.py`; greps of `checkout_changes`, `meet_agents`, `keep_round`, `faulted`, `code-scout`, and r214-r216 in features/supervision.feature
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base eeb9110e`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `wc -l` on the two changed files
- `python3 -m pytest -q tests/scenarios/test_supervision.py -k "another_initiative or side_by_side" -p no:cacheprovider`: 3 passed
- `git status --short`: clean
