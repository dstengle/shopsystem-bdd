# Review of w172: fix the findings of branch review 1 of i28

**Verdict: DONE.** The one fix-now finding of branch review 1 (finding 1, the integrate brief's label) is fixed as that review proposed. The brief now writes `Ids drafted elsewhere (number added lines above each on the same capability): <ids or none>` (`scripts/supervise_brief.py:79`), which is the label `agents/initiative-round.md:27` and `skills/integrating-a-proposal/SKILL.md:23` tell the round to look for. The r102 step now asserts that label. There is no Critical finding and nothing is triaged fix now. One Minor finding: the report says it cleared a ruff error that is still there.

## Commits reviewed

The branch `work/w172` is gone. So the commits are those on HEAD between `015fea21 work: w172 ready -> claimed` and `df6a187d work: w172 claimed -> done`, leaving out `work:` commits:

- `a1ff989a` supervise_brief: label the other initiatives' ids as the round's instructions name them; r102 step asserts the label. It changes `scripts/supervise_brief.py` (+4 −4) and `tests/scenarios/supervision_integrate_steps.py` (+5 −3).

This matches the implementer's `result.json` `commits` list (`a1ff989a`). Both files are inside the work-item's `fileset`. Nothing under `features/` or `spec/` changed.

## Removed and weakened tests

None.

What I searched for in the diff of `tests/`: deleted test functions or steps, dropped parametrize cases, removed or loosened `assert`s, added skip/xfail marks, and rewritten assertions.

- `integrate_given_ids`:
  - Before, it asserted that each given id appears anywhere in the brief.
  - Now it asserts that the brief has a line starting "Ids drafted elsewhere", and that each given id is on that line.
  - This is stricter: it passes on fewer briefs than before.
- `different_ids` and `listed`: only `re.M` became `re.MULTILINE`. The behaviour is the same.

## Allowances

- `integrate_given_ids`, interim: **holds**.
  - The step was first committed in `55eea183`, which is after Base `4b7dca6c`. `git show 4b7dca6c:...` does not contain the step.
  - It now asserts what plan decision D2 says: the brief carries the "Ids drafted elsewhere" label with the given ids on that line.
  - The change only tightens the step, so it did not need an allowance anyway.

## Cannot verify

- The report's red/green runs (`--work-item w172`: red 2 failed, then green 146 passed) and its full-suite figure at start (867 passed). I did not run the suite, as the brief instructs; `work run` runs it.

## Findings

### 1. Minor, w172, drop: the report claims the ISC004 fix, but the error is still there

- **Where:** `scripts/supervise_brief.py:82`.
- **What is wrong:** `tools check --base 015fea21` still reports `ISC004 Unparenthesized implicit string concatenation in collection` on this line. The report's "Changed" section says "Also fixed ruff ... ISC004", and plan §2 said to clear it. Only the quoting of that line changed (to single quotes); the implicit concatenation inside the list is still there.
- **Why it matters:** Ruff fails on a line this commit touched, and the report says something that is not true. It has no effect on behaviour.
- **Fix:** put the concatenated string in parentheses inside the list, or join the strings with `+`.
- **Triage:** drop. This is lint polish, and branch review 1 already triaged ruff as drop.

## Risk checked outside the diff

- **The risk:** a stub or another step might match the old wording ("take none of them"), so changing the label could silently break it.
- **What I verified:** `grep -rn "take none\|drafted elsewhere" scripts tests` finds only the new brief line and the new step. The old wording is gone, and nothing else depends on it.

## Commands run

- `git log --format='%H %s' -1 --grep="^work: w172 ready -> claimed$"` (the branch `work/w172` is gone, so I searched HEAD)
- `git log --oneline -15`
- `git show --stat a1ff989a` and `git show a1ff989a -- scripts tests features spec`
- `git log 4b7dca6c..015fea21 -S"def integrate_given_ids" -- tests/scenarios/supervision_integrate_steps.py` gave `55eea183`
- `git show 4b7dca6c:tests/scenarios/supervision_integrate_steps.py | grep integrate_given_ids` found nothing
- `grep -n "drafted elsewhere" agents/initiative-round.md skills/integrating-a-proposal/SKILL.md`
- `grep -rn "take none\|drafted elsewhere" scripts tests`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 015fea21`:
  - ruff: 1 error (ISC004 at `supervise_brief.py:82`)
  - vulture: clean
  - import-linter: the project states no import contracts
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: printed nothing (no file is over the limit)
