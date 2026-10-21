---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/nested-run-refused
kind: work-item
part_of: capability-proposal/release-gate-supervision
status: drafted
wkind: capability
under: supervision
accepts: [supervision#r21]
fileset: [scripts/work, scripts/supervise.py, scripts/supervise_worker.py, tests/scenarios/test_supervision.py, tests/scenarios/supervision_*.py]
---

# `work run` refused when started by a worker of another `work run`

Goes green: supervision r21 (card pytest-python, choice A). A worker runs `python3 -m pytest` in its own worktree, so it can reach Python; a nested `work run` it starts must refuse, saying so. For after the 0.21.0 release.
