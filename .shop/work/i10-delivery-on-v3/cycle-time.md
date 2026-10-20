---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/cycle-time
kind: work-item
part_of: capability-proposal/cycle-time-supervision
status: drafted
wkind: capability
under: supervision
accepts: [supervision#r19-r20]
fileset: [scripts/supervise.py, scripts/workqueue.py, features/supervision.feature, tests/scenarios/test_supervision.py, tests/scripts/stub_claude.py, agents/code-scout.md, agents/bdd-implementer.md, skills/bdd-red-green/SKILL.md, pytest.ini, README.md]
---

# Shorter cycles

Goes green: supervision r19 (the researcher's brief gives the file set and accepted scenarios, and `--max-turns 25`)
and r20 (two ready work-items with disjoint file sets run at once, merges serialized). Also, from red-green r1 and
supervision's Implementation: pytest-xdist added (README's dependencies), `-n auto` in work run's test commands and in
pytest.ini's addopts if the suite stays green under it; the implementer's definition and bdd-red-green run only
`--work-item` scenarios, leaving the whole suite to work run. Measured on the next real run against the i8 runs'
stage times (.shop/records/measurements/fixture-runs/2026-10-20-i8-work-run-test-log.md).
