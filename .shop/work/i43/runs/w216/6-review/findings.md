# Review of w216, second pass (supervision r156 fix)

**Verdict: DONE.** The fix-now finding of review 4 is fixed as the person's answer asks. A transition commit now names a work-item only when the name is one of the initiative's work-items; any other name, a capability-proposal's included, gives `none`. Nothing is Critical, nothing is triaged fix now, and nothing under `features/` changed.

## Commits reviewed

- `449bed1449ac3e13cdad987774546ad50e0320d6`, "work run's branch review brief gives none for a capability-proposal's transition commit (r156)". Its parent is `eaa2ea69` (`work: w216 ready -> claimed`).
  - It is the one commit in the brief's `Commits:` line, and the implementer's result lists the same commit (`449bed14`). They match.
  - It changes two files: `scripts/supervise_review_read.py` (+3/-1) and a new `tests/scripts/test_supervise_review_read.py` (+33).
- Suite, taken from the brief's record: 1031 passed, 0 failed at 449bed14 in 34 s. The expected failures are the parked w212 `test_requests.py` scenarios.

## Removed and weakened tests

None. The diff deletes no test function, drops no parametrize case, removes or loosens no assertion and adds no skip or xfail. The only test change is one new file holding one new test.

## Allowances

The report's `## Tests changed under an allowance` says "none", so there are no rows to verify, and none was needed.

## Cannot verify

- The report's `--work-item w216: 187 passed, 1 skipped`. I did not re-run it; the whole-suite record covers it.

## Findings

### 1. Minor, observation: the new test file is outside the work-item's file set

- **Work-item:** w216.
- **Where:** `tests/scripts/test_supervise_review_read.py` (new).
- **What is wrong:** w216's `fileset:` does not list this file, and the log shows no claim of it. The report's Budget names it, but the work-item file does not.
- **Why it matters:** the file set is the claim, so another work-item could claim the same path without a conflict being seen. The risk is low: it is a new test file with no behaviour, and no other work-item names it.
- **Reproduction:**
  - `git show --stat 449bed14` lists the file.
  - The `fileset:` line of `.shop/work/i43/w216.md` does not include it.
  - `git log ebbf1bea..HEAD -- .shop/work/i43/w216.md` shows no claim commit after `eaa2ea69`.
- **Fix:** none needed now. A later item that touches the file claims it.

## What I verified

- **The fix (`supervise_review_read.py:35,42`).** `names` comes from `self.items()`, that is `supervise.Run.items`. That calls `workqueue.items` (`scripts/workqueue.py:109-114`), which yields only files with `kind: work-item`, so a capability-proposal's name is never in `names`.
- **The other way a commit is attributed.** `merged.get(sha)` reads only `merged` lines of log.jsonl, and those name work-items. So neither path can now give a non-work-item name.
- **The new test.** It exercises the exact case of the person's answer: `work: supervision approved -> awaiting-answer` expects `none`, and `work: w1 ready -> claimed` expects `w1`. It passes (`python3 -m pytest -q tests/scripts/test_supervise_review_read.py`: 1 passed).
- **Code no line asks for:** none. The change narrows r156's attribution to what r156 says.
- **Previous review's Minor findings 2-4** were triaged observation or drop and were not in scope. The ruff errors of finding 2 no longer show in this commit's range (below).

## Check results

- **tools check (`--base eaa2ea69`):**
  - ruff: all checks passed.
  - vulture: clean.
  - import-linter: the project states no import contracts.
- **tools size (`--limit 300`):** no output, so no file is over the limit.
- **features/:** untouched.

## Commands run

- `git show --stat --format='%H %P%n%s' 449bed14`
- `git show 449bed14 -- scripts tests`
- `git log --format='%h %s' -3 449bed14`
- `cat scripts/supervise_review_read.py`
- `grep -n "^def items" -A15 scripts/workqueue.py`, and `grep -n "def items" scripts/supervise*.py`
- `python3 <Scripts>/tools check --base eaa2ea69b804d5faff1dfb2f62d3b51f34ec106d`
- `python3 <Scripts>/tools size --limit 300`
- `git log --format='%h %s' ebbf1bea..HEAD -- .shop/work/i43/w216.md`
- `python3 -m pytest -q tests/scripts/test_supervise_review_read.py`
