# Review of w191: fix the findings of branch review 1 of i32

**Verdict: DONE.** No finding is Critical and none is triaged fix now. The D1 crash (branch review 1, finding 1) is fixed; finding 5 (FURB167) is fixed. Two Minor findings in the new test file, and one observation.

## Commits reviewed

- Branch `work/w191` is gone. The range is `25a106bd work: w191 ready -> claimed` .. `4bb8f10d work: w191 claimed -> done` on the checked-out history.
- Leaving out `work run`'s own `work:` commit, it holds one commit: `32b5f1fa supervise_answers: a reviewer's item with no verdict from this run is not moved; re.MULTILINE`. This matches the implementer's `result.json` (`commits: ["32b5f1fa ..."]`).
- Files: `scripts/supervise_answers.py` (+5/-3), `tests/scenarios/supervision_delegation_steps.py` (1 line), `tests/scripts/test_supervise_answers.py` (new, 56 lines). They are exactly the work-item's fileset and the plan's final set. `4bb8f10d` touches only `.shop/`.

## Removed and weakened tests

None. Searched `git diff 25a106bd 32b5f1fa -- tests features` for:
- removed lines: there is one, `re.M` → `re.MULTILINE` at `tests/scenarios/supervision_delegation_steps.py:171`. It is the same flag, so the step asserts the same thing.
- `skip`, `xfail`, `parametrize`, removed `assert`s: none.

`features/` is unchanged. The plan's "Tests the decisions break" gives none, and that agrees with the commits.

## Allowances

The report gives `## Tests changed under an allowance: none`. The commits agree: the only existing test line changed is the alias edit, which changes no assert, expected value or case.

## Cannot verify

- **The red run.** The report says the new test failed with `KeyError: 'w1'` when the guard was disabled. That run is not in the commits. What I could check: the old code reached `self.verdicts[name]` on exactly the state the test builds (an item asked by its reviewer, no open question, no verdict), so the claim is consistent with the code.
- **The report's suite figures.** These are "885 passed at start" and "146 passed with `--work-item w191`". I did not run the suite, because `work run` runs it.

## Findings

### 1. Minor, w191, drop: `tools check` fails with RUF100 in the new test
- **Where:** `tests/scripts/test_supervise_answers.py:9` and `:10`, in `# noqa: E402`.
- **What is wrong:** E402 is not enabled in the project's ruff config, so ruff reports the directives as unused (RUF100). `tools check --base 25a106bd` exits 1 on them.
- **Why it matters:** every later review's check is red for this file.
- **Fix:** drop `E402` from both directives. Keep `F401` on line 9, or drop the directive there too if ruff accepts it.

### 2. Minor, w191, drop: vulture flags the stubs' unused `*args`
- **Where:** `tests/scripts/test_supervise_answers.py:36` (`commit(self, *args)`) and `:51` (`lambda *args: None`).
- **What is wrong:** vulture reports both as unused variables at 100% confidence.
- **Fix:** rename them to `*_args`, or whitelist them.

### 3. Minor, w191, observation: the item left by the fix waits silently for the person
- **Where:** `scripts/supervise_answers.py:85`.
- **What happens:** a reviewer's work-item that is awaiting-answer, has no open question and has no verdict from this run is now left as it is. Before the fix, the run crashed with a KeyError.
  - This serves r77 ("leaves it for the person otherwise") and decision 0069: no guard holds, so no transition is made. It is not code no line asks for.
  - `work run` names no reason, and the item has no open question to show the person.
- **The way out:** I verified it by reading. `work answer` (`scripts/workqueue_answer.py:35-77`) does not check for an open question. `work answer w1 "<text>" --accept` (or `--change`) still moves the item, and adds one more bullet under `## Answers`. So the item is not stuck. The plan and the report list this as an open case.
- **Reproduction:** `python3 -m pytest -q -p no:cacheprovider -n 0 tests/scripts/test_supervise_answers.py` gives 1 passed: no move, no session, nothing written.

### Checked, no finding
- **The other branches are unchanged.**
  - A non-reviewer's item still moves to `asked_from` (line 83-84).
  - A reviewer's item with a verdict from this run still moves through `reviewer_status` (line 85-86). That is r118 and r119's path.
  - With no target, the old fall-through to `uncommitted` → commit (line 89-90) still applies.
  - The risk I checked: `target` might be unbound or stale across loop iterations. It is reset to `None` at line 80 on every item.
- **A verdict recorded but the answer refused** (an answer with a line break, line 124-125): `left` becomes True, so no move is made. This was already the behaviour before the fix.
- **Size:** `tools size --limit 300` prints nothing. The touched files have 144, 202 and 56 lines.

## Checks

- **`tools check --base 25a106bd`** (exit 1):
  - ruff: 2 errors, both RUF100 in the new test (finding 1);
  - vulture: 2 unused `args` in the new test (finding 2);
  - import-linter: "the project states no import contracts".
- **`tools size --limit 300`:** no output, so no file is over the limit.
- **New test:** 1 passed.

## Commands run

- `git log --oneline -15`
- `git show --stat 32b5f1fa`
- `git diff 25a106bd 32b5f1fa`
- `git diff --stat 25a106bd 4bb8f10d`
- `cat -n scripts/supervise_answers.py` (lines 55-142)
- `sed -n 35,77p scripts/workqueue_answer.py`
- `grep -n ... scripts/workqueue_answer.py`
- `python3 -m pytest -q -p no:cacheprovider -n 0 tests/scripts/test_supervise_answers.py` → 1 passed
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 25a106bd` → exit 1 (above)
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` → no output
