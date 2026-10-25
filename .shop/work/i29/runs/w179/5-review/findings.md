# Review of w179 (supervision#r15: a result field too long to be a file name is taken as no file)

**Verdict: DONE.** No Critical finding, nothing to fix now. The change is the plan's change (D1–D3) and nothing else.

## Commits reviewed

The branch `work/w179` is gone, so the commits are taken from HEAD, between `eca9d404 work: w179 ready -> claimed` and `7c3b0a9a work: w179 claimed -> done`:

- `0c654848` keep_named: a result value the file system refuses as a name names no file (r15). Touches `scripts/supervise_worker.py` (+6/−2) and `tests/scenarios/supervision_given.py` (+6).

Every other commit in that range belongs to other work (i26, i28, i30, w176, w181) or is one of `work run`'s own `work:` commits, and none touches w179's file set.

Both implementer results (stage 3 and stage 4) list `f0695846`. That commit was made on the earlier branch, before the work-item went to awaiting-answer at `3269d4cd`. `0c654848` makes the same change: `git show` of each gives identical diffs with the same blob ids (`d6e9a8a7..c4526c16`, `50c2b139..a6fcd3da`). The hashes differ only because the commit was carried onto the branch again; the content is the same, so this is not a finding.

## Removed and weakened tests

None. I searched the range's diff of `features/` and `tests/`: only `tests/scenarios/supervision_given.py` changes, by one added `@given` (6 lines). No test function was deleted, no parametrize case dropped, no assert removed or loosened, and no skip or xfail added. `features/` is untouched.

## Allowances

Both reports' `## Tests changed under an allowance` sections say "none". That agrees with the commits: there are no rows to check.

## Cannot verify

- The stage-3 report's red run (`assert 'awaiting-answer' == 'green'` with OSError errno 36): I have only the report's word for it. The stage-4 session could not reproduce a red run because the fix was already committed.
- Whole-suite status: by the brief, the six failures are i29's r105–r109, accepted by w181. I did not run the whole suite.

## Findings

### 1. Minor (observation): the catch takes any OSError as "no file", not only a refused name
`scripts/supervise_worker.py:233-237`: `except (OSError, ValueError)` also skips a value whose `resolve()`/`is_file()` fails for reasons other than the name, for example a permission error on a directory in the path or a symlink loop. Such a value is then silently not copied. No client sends this today and no line names it. It also follows D1 of the plan, which chose the file system's refusal as the test. It is hardening only.
Reproduction: none run. A worker would have to name a file under a directory it cannot stat inside its own worktree, which no stage does.

Nothing else. The code serves r15 ("each file the worker's result names") and adds no observable behaviour: no log line, no output, no status (plan D3). Both files stay under 300 lines (251 and 265).

## Commands run

- `git log --format='%H %s' -1 --grep="^work: w179 ready -> claimed$"` → eca9d404; the same for `claimed -> done` → 7c3b0a9a
- `git log --stat eca9d404..7c3b0a9a`
- `git show 0c654848`, `git show f0695846 -- scripts/... tests/...` → identical diffs
- `git log --all -- .shop/work/i29/runs/w179/3-implement/report.md` → 3269d4cd (claimed -> awaiting-answer)
- `git diff --stat eca9d404 7c3b0a9a -- features/ tests/` → only supervision_given.py, +6
- `python3 <Scripts>/tools check --base eca9d404…`: ruff: All checks passed; vulture: clean; import-linter: the project states no import contracts
- `python3 <Scripts>/tools size --limit 300`: prints nothing (no file over)
- `python3 -m pytest -q -p no:cacheprovider tests/scenarios/test_supervision.py -k "sentence_longer or names_is_copied"` → 2 passed
- `git status --short` → clean
