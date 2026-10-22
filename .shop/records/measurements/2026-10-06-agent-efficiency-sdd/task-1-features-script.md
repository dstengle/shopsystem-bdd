---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-06-agent-efficiency-sdd-task-1
kind: measurement
about: capability/missingmass.io/shopsystem/shopsystem-bdd/feature-file-tools
date: 2026-10-07
---

# Agent efficiency task 1: the features script, implementer report

Implementer report for task 1 of the 2026-10-06 agent-efficiency plan (0.10.0): scripts/features built test-first, with its RED/GREEN counts and the count check against a clone of shopsystem-knowledge (132 scenarios, per-tag counts equal to pytest's). The brief is Task 1 of .shop/records/archive/plans/2026-10-06-agent-efficiency.md (verbatim there). Commits 41ccb37..8382992.

Archived from `.superpowers/sdd/2026-10-06-agent-efficiency/task-1-report.md` (git-ignored scratch), text as it was.

---

# Task 1 report: the features script

Implemented scripts/features (stdlib Python, executable, --help carries the contract) and tests/scripts/test_features.py (brief's tests verbatim).

## TDD
RED: `python3 -m unittest discover -s tests/scripts` -> Ran 15 tests, FAILED (failures=14); the script did not exist (the 15th, malformed slice -> exit 2, passed by accident because the interpreter also exits 2 on a missing file).
GREEN: same command -> Ran 15 tests, OK.
Honesty note: I wrote the script in one pass against all 15 tests rather than one test at a time; no behaviour beyond the tests and the contract bullets was added.

## Step 5 (real repository, read-only)
Clone at $SCRATCH/sk. `features count --by-tag` -> total 132. The clone's own interpreter could not import kb, so pytest ran with /home/vscode/shopsystem-knowledge/.venv/bin/python (cache disabled, run in the clone). `pytest --collect-only -q -m slice-<n>`: slice-1 2, slice-22 10, slice-58 11, slice-50.14 6, slice-55.1 3, slice-50.18.2 10, total 132; all equal the script's counts. Original repository untouched (git status clean).

## Files
scripts/features, tests/scripts/test_features.py.

## Self-review
Dead code from a first draft of cmd_tag removed. Examples rows are included in the "steps" comparison of verify-moved (so a moved outline losing rows is caught); the contract does not forbid it. Edits re-parse every file before writing (invalid result refused, nothing written).

## Concerns
Length ~330 lines; fine. Comment lines directly before the next scenario's tags stay with the previous block.
