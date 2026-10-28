# Review of w226: retire the deprecated scenarios of i46

**Verdict: DONE.** No Critical finding, none triaged fix now.

## Commits reviewed

- 93531c6a "Retire the deprecated scenarios of r77, r92 and r104 (w226)": features/supervision.feature, 40 deletions. The brief gives this commit, and so does the implementer's result.json (`commits: ["93531c6a ..."]`). They match. Its parent is 990601f5 `work: w226 ready -> claimed`.

Suite: taken from the brief's record, which shows 1066 passed and 0 failed at 93531c6a, plus the listed expected failures in test_requests.py (w212's parked scenarios). I did not run the suite.

## Changes under features/

The diff only removes lines. It removes exactly the three scenarios the work-item lists under Retires. I matched each title word for word:

1. The @r77 outline "under a delegation, each question of the initiative goes to a session of its own, ... that <reply> (deprecated)". Its `Deprecated for:` line names the r163 outline. It went with its Examples table and the blank line after it.
2. The @r92 scenario "an integrate round's change list gives one drafted capability-proposal for each capability it names, with what it adds, changes and removes on that capability (deprecated)". It is deprecated for the r159 scenario.
3. The @r104 scenario "the gate round of a capability-proposal is asked only for the questions on the lines and terms that proposal adds, changes or removes (deprecated)". It is deprecated for the r168 scenario.

In the first hunk, the diff keeps the outline's `@r77 @deprecated` line and deletes the identical tag line of the next scenario. The result is the same as deleting the outline's own tag line: the scenario that follows ("a work-item with two questions…", Deprecated for: removal) keeps `@r77 @deprecated`.

The removed scenarios had no binding: `features bindings --unbound` says "every binding names a scenario". `git grep` at 93531c6a finds none of the three titles anywhere outside .shop/.

## Removed and weakened tests

None beyond the three retired scenarios' generated tests, which Retires allows.

What I searched for:
- **Tests outside the feature file:** the diff touches no file under tests/.
- **The three titles:** `git grep` at 93531c6a finds each nowhere.
- **Step definitions the removed scenarios used:** the step for w1's/p1's question going to a session of its own (supervision_delegation_steps.py:170), the step on the commit that wrote i1's capability-proposals (supervision_integrate_steps.py:185), and the gate-round brief steps for p1 (supervision_proposal_steps.py:156, :192). All stay in place, and each is still used by a remaining scenario (supervision.feature:1324-1325, :1485, :1724-1725).

## Allowances

The report's `## Tests changed under an allowance` says "none". The commit changes no test file, so this holds.

## Cannot verify

- That r159 and r168 were green before the commit ("183 passed, 1 skipped" with `--work-item w226`). This is a claim of the report and the research. The suite record shows them passing at 93531c6a, but not at the base.

## Findings

1. **Minor, drop.** Work-item w226 (scope, not code). The work-item accepts r159 and r168 only, yet it also retires the scenario deprecated for r163, which is w223's line. The plan's D1 rests this on supervision#r123. It is consistent with r123, since r163's work-item w223 is green. Noted only so the person can see that the retiring work-item's `accepts:` does not list every replacement it retires for.
2. **Minor, drop.** tests/scenarios/supervision_integrate_steps.py:185 and supervision_proposal_steps.py:156. The removed r92 and r104 scenarios may have been the only users of the "and the term" parts of these step patterns; their regexes may now keep options no scenario uses. This is polish and was not in the file set. I did not check it further.

## Checks

- `tools check --base 990601f5`:
  - ruff: nothing to check
  - vulture: nothing to check
  - import-linter: the project states no import contracts
- `tools size --limit 300`: printed nothing.
- `features bindings --unbound`: "every binding names a scenario".
- `git status --short`: clean.

## Commands run

- `cat` of the brief, the work-item, the plan, the report and result.json
- `git show --stat 93531c6a`; `git show 93531c6a -- features/`; `git log --oneline -3 93531c6a`
- `git grep` at 93531c6a for the three titles, for the removed steps' texts, and for the step definitions
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 990601f5`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `python3 /home/vscode/shopsystem-bdd/scripts/features bindings --unbound`
- `git status --short`
