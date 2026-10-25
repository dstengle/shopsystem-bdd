# Review of w150: Retires covers a requirement named through a range (supervision#r73)

**Verdict: DONE.** No finding is Critical and none is fix now. The change does what r73 asks for a range, and the range scenario is green.

## Commits reviewed

The branch `work/w150` is gone, so I used the commits on the checked-out history between `b7da917 work: w150 ready -> claimed` and `f9253c8 work: w150 claimed -> done`, leaving out `work run`'s own `work:` commits:

- `6cee628 work run's Retires covers a requirement named through a range (supervision#r73)`: `scripts/supervise_draft.py` (+2/-1) and `tests/scenarios/supervision_proposal_steps.py` (+1/-1).

This is the one commit the implementer's `result.json` lists. The files changed match the work-item's `fileset`.

## Removed and weakened tests

None. What I searched:
- `git diff --stat b7da917 f9253c8 -- features tests`: one file only, `tests/scenarios/supervision_proposal_steps.py`, one line.
- That line is the step helper `named()`. Its regex `\w+#r\d+` became `\w+#r\d+(?:-r\d+)?`. No test function was removed. No `assert`, expected value or parametrize case changed, and no skip or xfail was added.
- The only caller of `named()` is the Given at line 25. For the single ids that the r72 Givens pass, it returns the same ids as before. For a range it now keeps the range, which is the fixture fix D3/D-c in the plan.

Nothing changed under `features/`.

## Allowances

The report's `## Tests changed under an allowance` says "none". It calls the `named` edit fixture setup. Measured against the `setup` test, that holds: the diff adds, removes or changes no assert, no expected value and no case. Nothing is to be verified here.

## Cannot verify

- The report's "Suite at start: 812 passed, 1 failed": I did not run the whole suite, as the brief says.
- The report's "Red: ... 1 failed, 143 passed": a red run from before the change cannot be checked from the commits. The research notes' run (§1) and their probes agree with it.

## Findings

1. **Minor, observation**: `scripts/supervise_draft.py:31-34`, from w150's commits (a defect that was already there, now also reachable through a range). If a `@deprecated` scenario has two `@r` tags and both fall in the accepted set, `retires()` returns it once per tag, so `## Retires` lists it twice. With ranges this is now more likely: `thing#r2-r3` covers both tags of a scenario tagged `@r2 @r3`. The research reproduced it: `retires("thing", ["thing#r2","thing#r3"])` → `[('it used to do both','r2'), ('it used to do both','r3')]` (notes §2, D2). It matters because r73 says "each scenario", and a duplicated line is noise for the narrator, not a wrong retirement. The plan left this as an open case on purpose. The fix: deduplicate by title, but only once a line or scenario decides whether one line per scenario is the intended output.
2. **Minor, observation**: `scripts/model_parse.py:100-104`, reached from `supervise_draft.py:31`. A reversed range (`thing#r6-r3`) is left unexpanded, so it matches no tag, and `retires()` silently lists nothing. No client writes a reversed range today. I found this by reading `expand`: the `int(a) <= int(b)` guard keeps the raw ref. The fix, if it is ever needed: a line that refuses a reversed range when the proposal is read.
3. **Minor, drop**: `tests/scenarios/supervision_proposal_steps.py:17`. `named()` still uses `\w+`, so a hyphenated capability name such as `work-queue#r3` would be read as `queue#r3`. This was already there and is fixture only. Today's scenarios use only `thing`.

Risks I named and checked:
- Does `expand` take the full `<cap>#r<a>-r<b>` refs that `retires` passes it, and return `<cap>#r<n>` refs that the `split("#")` that follows still handles? I read `model_parse.py:96-105`: yes.
- Does importing `model_parse` into `supervise_draft` break an import contract? `tools check` reports that the project states no import contracts. The import adds no cycle: `model_parse` imports nothing from `supervise*` (read).

## Checks

- `tools check --base b7da917`:
  - ruff: All checks passed.
  - vulture: one item, `tests/scenarios/supervision_proposal_steps.py:50` unused variable `base`. It was already there (`git show b7da917:...` has `def drafted(repo, base=0)`) and is not in the diff.
  - import-linter: "the project states no import contracts".
- `tools size --limit 300`: printed nothing. No file is over the limit.

## Commands run

- `git log --format='%H %s' -1 --grep="^work: w150 ready -> claimed$"` → b7da917. The same for `claimed -> done` → f9253c8.
- `git log --format='%h %s' --stat b7da917..f9253c8`
- `git show 6cee628 -- scripts tests`
- `git diff --stat b7da917 f9253c8 -- features tests`
- `sed -n 90,110p scripts/model_parse.py`
- `git show b7da917:tests/scenarios/supervision_proposal_steps.py | sed -n 48,52p`
- `grep -n "named(" tests/scenarios/supervision_proposal_steps.py`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base b7da917...` (exit 1: vulture's pre-existing item)
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` (no output)
- `python3 -m pytest -q -o addopts="" tests/scenarios/test_supervision.py -k "lists_under_its_retires"` → 2 passed
