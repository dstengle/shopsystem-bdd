# Report w106

## Budget
scripts/tools_env.py, scripts/tools, tests/scenarios/analysis_tools_probe_steps.py, ruff.toml

## Changed
- tools_env.py: `RUFF_PIN = "0.17.0"`; cmd_install passes `ruff==0.17.0` for ruff, others by name; TOOLS row unchanged.
- scripts/tools contract text; ruff.toml comment names 0.17.0.
- Steps: Given "the plugin pins one version of ruff" (reads RUFF_PIN from scripts/tools_env.py's text, since `import tools_env` in the test process gave a module without it, i.e. another tools_env.py on sys.path); Then asserts exactly one pip call, `ruff==<pin>`, pin is x.y.z.

## Red / green
- Red: `python3 -m pytest -q tests/scenarios/test_analysis_tools.py::test_install_puts_in_the_version_of_ruff_the_plugin_pins` -> StepDefinitionNotFoundError: Given "the plugin pins one version of ruff" (expected: undefined step, no pin).
- Green: same test passes; `--work-item w106`: 137 passed, 1 skipped; test_analysis_tools.py + tests/scripts/test_tools.py: 6 passed, 1 skipped.
- Suite at start (brief): 670 passed, 4 failed (incl. test_install_puts_in_the_version_of_ruff_the_plugin_pins, the target); not rerun.
- `tools size --limit 300`: no output (no file over).

## Tests changed under an allowance
none

## Open questions
- Whether 0.17.0 exists on the index could not be checked (no network/pip query allowed); the exact patch release is a concern.
- Whether probe should report a ruff not at the pin: unchosen.

## Other
Plan contained no code. Commit: 5cb2bcf.
Concern: patch number 0.17.0 unverified against PyPI.
