---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/plugin-scenarios-run-as-pytest-bdd
summary: "In this repository a script capability's scenarios run under pytest-bdd: one scenarios() call binds its feature file, its steps are step definitions under tests/scenarios/, and features bindings --unbound fails the suite when a scenario is bound by no test or by two."
date: 2026-10-19
status: proposed
source: [observation/2026-10-19-final-state-only]
by: "the person, 2026-10-19, rejecting design-decision/plugin-scenarios-run-as-unittest"
---

# 0048. Plugin scenarios run as pytest-bdd

## Decision

`python3 -m pytest` runs the whole suite from the repository's root (`pytest.ini`: `testpaths = tests`,
`bdd_features_base_dir = features/`). Each script capability's feature file is bound by one module,
`tests/scenarios/test_<capability with underscores>.py`, whose one binding is
`scenarios("<capability>.feature")`; its Given, When and Then steps are step definitions in that module, with
the fixtures the modules share in `tests/scenarios/conftest.py`. A scenario whose step has no definition
fails, so a scenario added to a feature file is red until it has steps.

`tests/scripts/test_bound.py` runs `features bindings --unbound` over the script capabilities' feature files
and fails when a scenario is bound by no test or by two. With the tag reading of `model check`, that keeps
the coverage it reports exact: every scenario that names a requirement is a test that runs.

Unit tests that bind no scenario stay in `tests/scripts/` as `unittest` tests, collected by pytest.
`tests/scripts/binding.py` and the docstring binding go, except for `batch-measurement`, whose scenarios keep
it until initiative i12 rewrites them.
