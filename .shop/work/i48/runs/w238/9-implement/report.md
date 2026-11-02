## Budget
scripts/supervise_change.py, tests/scripts/test_supervise_change.py

## Changed
- r188 was committed earlier (440352d6): `redraft_lists` keeps ids the change list does not name. r188 scenario passes.
- r189: glossary branch of `write_proposals` writes into the glossary-proposal the round was started for (found by kind), keeping unnamed terms; no second glossary.md. Unit test added.

## Runs
Suite record: 1084 passed, 0 failed at 440352d6 (with listed expected failures).
Final `--work-item w238`: 182 passed, 1 failed: the r189 scenario. Its failure is the assertion `len(rounds(repo,"integrate","g1")) == 1`: only an apply round for g1 started. This branch does not hold w242 (supervision r221, on main), which sends an applied-nothing glossary-proposal back to an integrate round. I may not merge/rebase, so I could not run r189 with it. The unit test covers my glossary branch.
tests/scripts/test_supervise_change.py: 4 passed.

## Tests changed under an allowance
none beyond the earlier p1 assertion rewrite in 440352d6 (plan part 4).

## Open questions
Plan part 5 cases: integrate round for a capability-proposal/initiative naming glossary while a glossary-proposal is held (fresh glossary.md write unchanged); same id in two lists.

Plan contained no code. Size check: no file over 300 printed.
