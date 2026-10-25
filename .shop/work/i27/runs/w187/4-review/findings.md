# Review of w187 (fix the findings of branch review 8 of i27): findings

**Verdict: DONE.** No finding is Critical, and none is triaged fix now. F4 (two entries for one capability) is fixed, and a script test went red and then green. F11 got only a margin; its cause is still unknown. F2 is fixed only in part (one ruff error remains, one new one).

## Commits reviewed

- The branch `work/w187` is gone. The commits are those between `1b5a84f7 work: w187 ready -> claimed` and `8b3775cd work: w187 claimed -> done` on the checked-out history, less `work run`'s `work:` commits (`60726a98 work: w184 done -> green`).
- That leaves one commit: **bd765f03** "Fix branch review 8 findings: one proposal per capability, r95 margin, docs".
- The implementer's result lists **1bef04de**. It is the same commit before the rebase: same message and author date, parent 1b5a84f7. `git diff 1bef04de bd765f03 -- CLAUDE.md scripts tests` is empty. Not a difference.
- Files: CLAUDE.md, scripts/supervise_change.py, scripts/supervise_rounds.py (docstring only), tests/scenarios/supervision_all_steps.py, tests/scripts/test_supervise_change.py (new). All of them are in the work-item's fileset. Nothing under `features/` changed.

## Removed and weakened tests

None. **What I searched:** every `-` line of `git show bd765f03` under `tests/`. There are three:
- `supervision_all_steps.py:104` `linger` 1 -> 3. The stand-in waits *up to* that long for another worker to start (`stub_claude.py:35,208-210`). A longer wait makes an overlap more likely to show, so this is not weaker. The `ended < started` assertion is unchanged.
- `:111` `re.M` -> `re.MULTILINE`: the same flag.
- `:127` `zip(...)` -> `zip(..., strict=False)`: the same behaviour.

No test function was deleted, and no parametrize case, skip or xfail was touched. The plan's "Tests the decisions break" says none, and that agrees.

## Allowances

The report's `## Tests changed under an allowance` says "none". The only test-side change that could need one is the linger value. It adds, removes and changes no `assert`, no expected value and no parametrize case, so it would hold as `setup` anyway. Nothing to reject.

## Cannot verify

- The report's claim "Suite at start: 873 passed, 0 failed at 1b5a84f7". I did not run the whole suite.
- Whether F11 is fixed. Under load, the r95 failure was never captured. The report says no loaded repeat runs were made because no loop command was allowed. The cause (the lock, the linger, or the stand-in's record) is still open, as the plan's third branch allows. I ran r95 once alone and it passed. That does not show the flakiness is gone.

## Findings

**R1** (Minor, w187, observation). `tests/scenarios/supervision_all_steps.py:127`: F2's RUF007 is still there.
- **What is wrong:** the report says "F2: ruff fixes at the two lines". Adding `strict=False` does not fix the RUF007 that review 8 named at `:127` ("Prefer `itertools.pairwise()`").
- **Why it matters:** the report claims more than the commit does, and `check` keeps the error.
- **Fix:** `for (_, _, _, ended), (_, _, started, _) in itertools.pairwise(found):`.
- **Reproduction:** `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 1b5a84f7` gives `supervision_all_steps.py:127:49: RUF007`.

**R2** (Minor, w187, observation). `tests/scripts/test_supervise_change.py:7`: a new ruff error, RUF100 (the `# noqa: E402` is unused).
- **Why it matters:** it adds to `check`'s error count.
- **Fix:** remove the `noqa`.
- **Reproduction:** the same `tools check` run, which gives `RUF100 [*] Unused noqa directive`.

**R3** (Minor, w187, drop). `scripts/supervise_change.py:62`: the merge also drops a repeated id within a single entry's list. Before, the id was written twice.
- This serves r92 (a proposal lists *the* ids it adds, changes and removes), so it is not code that no line asks for. The report names it.
- One case is still open, as the report says: one id under `adds` in one entry and under `changes` in another is kept in both.

**What I checked against r92 / r91-r97 / r66.**
- **The risk I named:** the merge changes the order or content of proposals for distinct capabilities. That would break the r92 scenarios and the proposal ids of r92's "two initiatives" scenario.
  - **What I verified:** `merged` is an insertion-ordered dict keyed by capability. For distinct capabilities it gives the same entries in the same order as before. The four r92/r95 scenarios pass (`-k "one_at_a_time or change_list"`, 4 passed).
- No behaviour contradicts a line or the Purpose. The docstring and the CLAUDE.md row now name r91, r95 and r96, which closes review 8's "Shape" item.

## Checks

- **ruff** (`tools check --base 1b5a84f7`): 2 errors, both in w187's lines (R1, R2).
- **vulture:** clean.
- **import-linter:** "the project states no import contracts".
- **`tools size --limit 300`:** printed nothing.
- **`git status --short`:** empty, before and after.

## Commands run

- `git log --format='%h %s' -15`, `git show --stat bd765f03`, `git log --format='%H %P' -1 bd765f03`, `git show 1bef04de --stat`, `git diff 1bef04de bd765f03 --stat -- CLAUDE.md scripts tests`, `git show bd765f03`
- `python3 -m pytest -q -n0 -p no:cacheprovider tests/scripts/test_supervise_change.py` gave `1 passed`.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 1b5a84f7`: as above.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: no output.
- `python3 -m pytest -q -n0 -p no:cacheprovider -k "one_at_a_time or change_list" tests/scenarios/test_supervision.py` gave `4 passed in 14.71s`.
- `git status --short`: empty.
