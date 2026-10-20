---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/fixture-scenarios-under-pytest-bdd
summary: "A workflow capability's scenarios are pytest-bdd scenarios tagged @fixture, deselected from the unit suite, whose When runs a fixture case headless three times and whose Then passes only when every run passes."
date: 2026-10-19
status: proposed
revisit_when: "a fixture scenario's verdict changes between two suite runs on one plugin tree"
revisit_signal: requests
source: [design-decision/workflow-scenarios-run-as-fixture-sessions]
by: "(its open question); /home/vscode/scratch/shopsystem-bdd/ids/ (make_ids.py, score.py, run.sh)"
---

# 0043. Fixture scenarios run under pytest-bdd

## Decision

A workflow capability's feature file has the feature tag `@fixture`; pytest-bdd makes it the marker
`fixture`, and the repository's `pytest.ini` has `addopts = -m "not fixture"`, so `python3 -m pytest` runs the
unit suite only. `python3 -m pytest -m fixture [path]` runs them. The harness is test code under `tests/workflow/`:
fixture cases (a builder that makes a throwaway repository and the prompt the session is given), the run (`claude
-p <prompt> --plugin-dir <this checkout> --model sonnet --output-format stream-json --dangerously-skip-permissions`
in that repository), and the checks over what a run left. A Given binds a case, a When runs it, a Then checks every
run. Each case runs `--fixture-runs` times (default 3), once for all the scenarios bound to it, and a Then passes
when `--fixture-pass` runs (default all) pass. Runs are kept under `--fixture-dir` (default
`~/.cache/shopsystem-bdd/fixture-runs/`) by the plugin's tree hash and reused, so a rerun after a change to a check
costs nothing. `--fixture-record <label>` writes the verdicts, costs and times as a measurement record under
`.shop/records/measurements/fixture-runs/`.

## Alternatives

Two of three runs; one run per scenario. A contract that one run in three breaks is broken that often in a consuming
repository.
