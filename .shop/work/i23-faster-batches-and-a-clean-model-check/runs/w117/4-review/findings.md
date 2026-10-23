# Review of w117: v_w4 reads a work-item's accepts from its field

**Verdict: DONE.** No Critical finding, none triaged fix now. The change does what r106 and the capability's Implementation line ("A work-item's `accepts` facts are written from its `accepts` field, whether or not a scenario names the requirement (r106)") ask, and keeps the r27 file problem.

## Commits reviewed

Branch `work/w117` is gone. Commits taken from HEAD between `99715327 work: w117 ready -> claimed` and `bac68965 work: w117 claimed -> done`, leaving out `work:` commits:

- `aaeea80 model check: v_w4 reads a work-item's accepts from its field (r106)`: `scripts/model.lp` +1, `scripts/model_work.py` +1/-2, `tests/scenarios/design_model_check_one_each.py` +1.

These match the commit in the implementer's `result.json`. All three files are in the work-item's `fileset`. Nothing under `features/` changed.

## Removed and weakened tests

None. I checked the diff for deleted test functions, dropped parametrize cases or FIELDS entries, removed or loosened asserts, and added skip/xfail. The only test change adds one `FIELDS` entry (`"accepts thing#r2 and no check"`). The plan's "Tests the decisions break" says none, which agrees.

## Allowances

The report's `## Tests changed under an allowance` says "none". The commits agree: no existing test was changed.

## Cannot verify

- The report's red run (1 failed at the Then, 142 passed) can't be checked from the commits. Its cause matches the research's probe A, so it is plausible.
- The report's start-of-suite figure (721 passed, 1 failed). I did not run the whole suite: `work run` ran it.

## Findings

No finding.

Risks I checked:

1. **Something else reads `accepts(W, S)` as a scenario.** The fact's second argument is now a requirement, so any reader expecting a scenario would break. `grep accepts(` over `scripts/` and `tests/`: the only reader is `has_accepts` (`scripts/model.lp:65`), which ignores the second argument. `grep -rl accepts scripts/` also lists `supervise_merge.py`, `supervise_brief.py`, `workqueue.py`, `work` and `work_items.py`. None of them parses `accepts(` fact lines. The risk does not hold.
2. **r27 file problem lost.** `found` is still computed and still drives the problem at `scripts/model_work.py:193-194`. `tests/scripts/test_model_withdrawn.py` and the withdrawn/accept scenarios: 7 passed.
3. **New code that no Behaviour line asks for.** The one behaviour change is the `accepts` fact written for an unnamed or unknown requirement. It is visible in `model facts` and drops `v_w4`. The r106 line and the Implementation section's line at :106-107 ask for it. Not a finding.

Pre-existing, not in these commits: a malformed `accepts` reference that `resolve_req` refuses (`scripts/model_facts.py:89-97`) gives a dangling problem and no fact, so the work-item can also print `v_w4`. The plan lists this as an open case. These commits do not change it.

## Checks

- `tools check --base 99715327…`: ruff "All checks passed!"; vulture "clean"; import-linter "the project states no import contracts".
- `tools size --limit 300`: printed nothing. (`scripts/model.lp` is now 304 lines but is not a Python file.)

## Commands run

- `git log --format='%H %s' -15`, `git show --stat aaeea80`, `git diff 99715327 aaeea80`
- `grep -rn accepts scripts/*.lp scripts/model*.py`, `grep -rln accepts scripts/`, `grep -rn 'accepts(' scripts/ tests/`, `grep -rn "def resolve_req" -A 14 scripts/`
- `python3 -m pytest -q -n 0 tests/scenarios/test_design_model_check.py -k v_w4 tests/scripts/test_model_withdrawn.py`: 5 passed
- `python3 -m pytest -q -n 0 tests/scripts/test_model_withdrawn.py tests/scenarios/test_design_model_check.py -k "withdrawn or accept"`: 7 passed
- `python3 <Scripts>/tools check --base 99715327871ad2dab8008d2ec10699d41bb7910f`
- `python3 <Scripts>/tools size --limit 300`
