---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/pytest-bdd-suite
kind: work-item
part_of: capability-proposal/final-layout-analysis-tools
status: green
wkind: enabling
for: work-item/analysis-tools-scenarios
check: "python3 -m pytest -q from the root passes and collects every test python3 -m unittest discover -s tests/scripts runs, the same count; python3 -m pytest --collect-only -q tests/scenarios exits 0"
fileset: [pytest.ini, tests/scenarios/__init__.py, tests/scenarios/conftest.py, README.md, spec/index.md]
---

# The suite under pytest, with a home for step definitions

Goes green: nothing new; the suite runs under `python3 -m pytest` from the root, the unit tests unchanged.

- `pytest.ini` at the root: `[pytest]`, `testpaths = tests`, `bdd_features_base_dir = features/`; pytest's
  defaults otherwise.
- `tests/scenarios/` (a package) with `conftest.py`: the fixtures every step module shares, lifted from the
  helpers the unittest classes already have (`ModelTest`'s temporary repository and its writers in
  `tests/scripts/test_model.py`, `Workspace` in `test_features.py`, the project builders in `test_tools.py`):
  a fixture giving a fresh temporary directory as the root, a `run` fixture that runs a script
  (`scripts/model`, `scripts/features`, `scripts/tools`) with `sys.executable` and returns the completed
  process, and a `context` fixture (a dict) that steps use to pass the result from When to Then.
- The unit tests in `tests/scripts/` keep importing `binding` as they do (pytest's default import mode puts
  their directory on `sys.path`); check that pytest collects the same number of tests unittest runs.
- README's Testing and `spec/index.md`'s Testing say `python3 -m pytest` (the text is in the proposal's
  `spec-index.md`).

Dependencies: pytest and pytest-bdd, already named by design-decision/plugin-takes-the-dependencies-it-needs.
