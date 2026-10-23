# Review of w116 (design-model-check#r27)

**Verdict: DONE.** No Critical finding and nothing to fix now. There is one Minor observation and one Minor drop.

## Commits reviewed
- The branch `work/w116` no longer exists. The commits were taken between `52f6973 work: w116 ready -> claimed` and `344ef0e work: w116 claimed -> done`.
- That range holds one commit that is not a `work:` commit: `495a420 model check: r27 exempts guarantees requirements and a green work-item's retired id; model.lp names only a proposal's real statuses`. It is the only commit the implementer's result.json lists, so the two match.
- Files changed: scripts/model.lp (-1), scripts/model_work.py (+4/-1), tests/scenarios/design_model_check_given.py (+11), tests/scenarios/design_model_check_problems.py (+11). These are the work-item's fileset exactly.
- Nothing under `features/` changed (`git diff --stat 52f6973 495a420 -- features tests` lists only the two step modules).

## Removed and weakened tests
None.
- What I searched for in `git diff 52f6973 495a420`: removed lines in test files, removed or loosened asserts, dropped parametrize cases, added skip or xfail, renamed tests. Both test files have only additions.
- The one change to an existing test function is a second `@then` alias, "it prints no file problem naming {named}", on `no_file_problem_named`. The body is unchanged, so the existing phrasing asserts exactly what it did before.

## Allowances
The report's `## Tests changed under an allowance` says "none". The commits agree: they contain no changed assert, no changed expected value and no changed case.

## Cannot verify
- The report says the full suite was green at the end (714 at start with the 3 w116 scenarios red; `--work-item w116` 150 passed, 1 skipped). I did not run the whole suite (`work run` runs it). The focused r27, guarantees, retired and malformed scenarios pass (12 passed).

## Risks checked
- **Read order**: the guarantees exemption reads the `group` fact, so capabilities must be read before work. `Model.read` (scripts/model_facts.py:99-109) calls `read_capabilities` before `read_work`. Holds.
- **`int(n)` crash**: could the reference lack `#r<n>`? `resolve_req` (model_facts.py:89-97) returns `{cap}#r{n}` or None, and None is skipped before this code runs. No crash.
- **model.lp**: the removed rule made a capability-proposal closed at built, delivered, ruled, green or refused. None of these is in the proposal lifecycle (`STATUSES` in model_work.py), and each is already a file problem. A proposal is still closed at `formulated` (its own rule) and `withdrawn` (its own rule), as r36 says. The rule for other part kinds is unchanged.
- **Behaviour against r27**: guarantees requirements are exempt. A retired id is exempt only when the work-item is green, so a drafted work-item accepting a retired id still gets the file problem (plan decision 2). Withdrawn is unchanged. All of this agrees with r27's row.
- **Code no line asks for**: none. Every change in observable behaviour comes from r27's row.

## Findings

### F1 (Minor, observation): a guarantees capability's nonexistent requirement accepted by a work-item is now silent
- Work-item: w116.
- Where: scripts/model_work.py:191-194.
- What is wrong: the exemption tests only that the accepted reference's capability is in the guarantees group. It does not test that the requirement exists. A work-item that accepts `thing#r9`, when guarantees `thing` has no r9, now gets no file problem, no unresolved reference and no violation. Before this commit it got "accepts ...thing#r9, which no scenario names yet". In the service group the same input still gets that file problem.
- Why it matters: a reference typed wrong in `accepts` on a guarantees capability is no longer caught by anything. r27 exempts "a requirement of a capability that is … guarantees", and a missing id is not such a requirement. But no line says what a missing requirement in `accepts` should be (the researcher's D3, the plan's open case 1). So this is hardening, not a wrong answer against a line.
- Fix: exempt only when the requirement exists (`int(n) in self.caps[cap]["reqs"]`). Or settle D3 with a line that makes a missing requirement in `accepts` unresolved.
- Reproduction: `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w116-4-review/test_probe_r27.py` gave:
  - guarantees, drafted, `thing#r9`: problems [] and unresolved [].
  - service, drafted, `thing#r9`: problems [".shop/work/i1/w1.md: accepts capability/ex.com/prod/ctx/thing#r9, which no scenario names yet"].
  - guarantees, drafted, `thing#r2`: problems [] (as r27 says).

### F2 (Minor, drop): the guarantees test scans every fact for each accepted reference
- Work-item: w116.
- Where: scripts/model_work.py:192.
- What: `("group", [cap, "guarantees"]) in [(f, list(a)) for f, a in self.facts]` builds a list of all facts for each accepted reference. `self.caps[cap]["group"] == "guarantees"` (model_facts.py:43, 199) would read the same thing directly. The `found` scan on the line above is already linear in the facts, so this changes no complexity class.
- Triage: drop.

## Checks
- `tools check --base 52f6973`:
  - ruff: All checks passed!
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: printed nothing. tests/scenarios/design_model_check_problems.py is exactly 300 lines, at the limit but not over it.

## Commands run
- `git log --format=%H -1 --grep="^work: w116 ready -> claimed$" work/w116`: the branch is gone.
- `git log --format='%h %s' -3 HEAD`, `git log --stat 52f6973..344ef0e`, `git diff 52f6973 495a420`
- `git show 495a420:scripts/model_work.py` (lines 160-200); reads of scripts/model_facts.py (read order, resolve_req, retired, group); grep of model.lp for guarantees; grep of features/design-model-check.feature for the r27 scenarios
- `python3 -m pytest -q -n 0 tests/scenarios/test_design_model_check.py -k "r27 or guarantees or retired or malformed"`: 12 passed
- `python3 <Scripts>/tools check --base 52f6973`; `python3 <Scripts>/tools size --limit 300`; `wc -l` of the touched files
- The probe above, written to .shop/scratch/w116-4-review/
- `git status --porcelain`: clean
