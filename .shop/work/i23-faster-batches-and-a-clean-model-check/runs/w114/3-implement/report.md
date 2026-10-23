## Budget
- scripts/tools_env.py
- scripts/tools
- tests/scenarios/analysis_tools_probe_steps.py

## Changed
- tools_env.py: `RUFF_PIN = "0.17.0"`; install hands pip `ruff==0.17.0` for ruff only.
- scripts/tools: contract text says ruff is installed at the pinned version.
- probe steps: Given "the plugin pins one version of ruff", Then "ruff is installed ... at the version the plugin pins". The pin is read from the text of scripts/tools_env.py (not imported: `import tools_env` in the tests resolved to another copy, because conftest appends scripts/ to sys.path).

## Red / green
- Red 1: `python3 -m pytest -q "tests/scenarios/test_analysis_tools.py::test_install_puts_in_the_version_of_ruff_the_plugin_pins"` -> StepDefinitionNotFoundError for the Given (expected: no steps).
- Red 2 (steps written): fails on the pin not existing in tools_env (pin absent; expected before code).
- Green: `python3 -m pytest -q --work-item w114` -> 137 passed, 1 skipped. test_analysis_tools.py + tests/scripts/test_tools.py: 6 passed, 1 skipped.
- Suite at start: 694 passed, 1 failed (test_install_puts_in_the_version_of_ruff_the_plugin_pins), plus listed expected failures. Whole suite not run by me.
- size --limit 300: prints nothing.

## Tests changed under an allowance
none (removed 4 blank lines in the steps file at 237-242 area to keep room; no test touched)

## Open questions
none beyond the plan's: 0.17.0 not checked against a package index; spec Implementation line (spec/capabilities/analysis-tools.md:56) does not mention the pin, outside file set; decision 0035 doc mention unsettled.

The plan contained no code. Commit: 8f76e50.

Someone can now: `tools install` puts in ruff==0.17.0.
