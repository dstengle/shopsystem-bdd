# Notes of w114: tools install pins ruff (analysis-tools#r58)

Tools: plugin 0.24.0 `scripts/tools` (run). `probe --log` run: ruff 0.17.0 installed in the interpreter.
`refs cmd_install`: 0 references (refs, the dispatch at `scripts/tools:82` is not counted; read).
`tests-of`: refused "no map" (run). Making a map runs the whole suite, so tests are found by search.
`size --limit 300`: prints nothing, no file over 300 (run). No repository pin exists (grep of tracked files, read).

## 1. Why the scenario is red today

- Command: `python3 -m pytest -q "tests/scenarios/test_analysis_tools.py::test_install_puts_in_the_version_of_ruff_the_plugin_pins"` (run).
- Failed: `StepDefinitionNotFoundError: Given "the plugin pins one version of ruff"`, feature line 76. The When and Then are not reached.
- Missing step definitions: the Given (line 76) and the Then "ruff is installed into the interpreter at the version the plugin pins" (line 78). Neither text is in `tests/` (grep, read). The existing install Then, `{tools} are installed into the interpreter with pip` (`tests/scenarios/analysis_tools_probe_steps.py:182`), does not match it.
- Missing code: `scripts/tools_env.py:cmd_install` line 93 runs `[python, "-m", "pip", "install", package]`. `package` is the bare `"ruff"` of the TOOLS row, line 17 (read). Nothing passes a version: no constant, no requirements file, no plugin manifest names ruff (`git ls-files` grep, read). The only version text is the comment `ruff.toml:2` "the rules ruff 0.17 applies" (read).
- Once the steps exist, the When reaches the bare call: probe a (run) shows pip gets `ruff`. The Then would fail on that argument.

## 2. What the system answers today

Probe: `python3 -m pytest -q -s -p no:xdist -o addopts="" .shop/scratch/w114-1-research/probe_ruff_pin.py` (run, 4 passed). A stand-in interpreter answers the version query and logs pip calls; it installs nothing. Project is in scratch.

- a. Given: venv missing ruff. When `tools install`: rc 0, stdout `ruff installed`, pip calls `[["ruff"]]`. The Given and When of the scenario as today. r58 needs `ruff==<pin>` here.
- b. Nearest, not given by the scenario: ruff present at 0.18.0. rc 0, stdout `every tool is present`, no pip call.
- c. Nearest: not a virtualenv, missing ruff. rc 1, stdout `ruff is missing.` ... `Tried: <python> is not a virtualenv (--python): nothing is installed into it`; no pip call.
- d. Nearest: pip fails for ruff. rc 1, stdout `Tried: <python> -m pip install ruff`, then `e3`, `e4`, `e5`, `error: no matching distribution`; pip call `[["ruff"]]`.
- Plugin `probe --log` (run): `Probe: tools -> ... ruff 0.17.0 ...`: the interpreter running the script has ruff 0.17.0.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/tools_env.py:cmd_install (line 93) | pip gets the bare package name; pip takes the newest ruff | ruff's argument becomes `ruff==<pin>`; jedi and vulture unchanged | r5 scenario (`installed_with_pip`), r7 scenario (`failed_command`), by search; probe a (run) | read; search for `pip` |
| scripts/tools_env.py TOOLS row, line 17 `("ruff", "ruff", ...)` | one field is both the metadata lookup key (`versions`, `probed`, lines 53-83) and the pip argument | the pin must not go in this field, or probe and check lose the lookup (`metadata.version("ruff")`) | probe r3 and r4 scenarios, check r16 (`tests/scripts/test_tools.py:73`, `:128`), by search | read |
| tests/scenarios/analysis_tools_project.py:pip_calls (lines 153-154) | returns each pip argument as given | returns `ruff==<pin>` for ruff; the new Then compares that string | r5, r6, r7 scenarios (`installed_with_pip`, `still_missing`, `failed_command`, `nothing_installed`), by search | search for `pip_calls` |
| tests/scenarios/analysis_tools_probe_steps.py:installed_with_pip (lines 183-185) | compares the whole pip list with the names in the Then, `jedi and vulture` | unchanged: no scenario lists ruff among installed tools | r5 scenario, by search | search for `installed_with_pip` |
| scripts/tools, contract text (lines 24-25) | "install runs `<interpreter> -m pip install <package>`" | must say ruff is installed at the pinned version | none (text) | read |
| spec/capabilities/analysis-tools.md, Implementation (line 56) | "install runs `<interpreter> -m pip install <package>` per missing tool" | the spec's wording of the install does not name the pin; r58 does | none (text) | read |
| scripts/tools_check.py:21 (`python -m ruff check`) | runs whichever ruff the interpreter has | a ruff installed before the pin still runs; the rules in `ruff.toml` assume 0.17 | check r16 scenarios, faked ruff (`analysis_tools_code_steps.py:93`, `:103`), by search | read; search for `ruff` |
| ruff.toml:2 (comment) | "the rules ruff 0.17 applies" | stale only if the pin is outside the 0.17 series | none (`ruff.toml` is read by no test; grep) | grep |

## 4. Tests the requirements make impossible to keep

`tests-of` refused (no map), so the list is by search of `tests/` for pip, install and ruff.

- None can no longer pass as it is. The pin changes only ruff's pip argument, and no test asserts ruff's pip argument today.
- Verified sound, by read: `tests/scripts/test_tools.py:79-86` (refusal for a non-virtualenv; it never reaches line 93).
- Verified sound, by read: `installed_with_pip` (r5, jedi and vulture), `failed_command` (r7, asserts `Tried: ... -m pip install jedi`), `install_refused` and `still_missing` (r6, `pip_calls == []`), `nothing_installed`.
- The red scenario itself is the one test the work-item must turn green.

## 5. A step the work-item skips

- The pin is not checked against a ruff already present. Probe b (run): ruff 0.18.0 installed gives `every tool is present`, rc 0, no pip call. r58 says "when install installs ruff", so the requirement leaves this path open. Under it, `tools check` runs the 0.18.0 ruff (`tools_check.py:21`, read).
- The not-virtualenv refusal (probe c, run) comes before the pinned call, so it applies to the pinned call unchanged (read: lines 88-90).
- pip failure (probe d, run) prints the command it ran, so the message would show `ruff==<pin>` (read: lines 95-96, 102-103).

## 6. Defects

### A refusal labelled `Tried:` tried nothing

- Reproduction: `python3 -m pytest -q -s -p no:xdist -o addopts="" .shop/scratch/w114-1-research/probe_ruff_pin.py::test_c_not_a_virtualenv_refuses_ruff` (run).
- Came back: `Tried: <path>/venv/bin/python is not a virtualenv (--python): nothing is installed into it`, rc 1, no pip call.
- No command was run, yet the line is labelled `Tried:`. The shared format is `scripts/tools_env.py:102`, fed by line 89.
- Not fixed; the plan decides what to do about it.

## 7. The file set

Changes (each on the search or run that showed it):

- `scripts/tools_env.py`, 104 lines, room 196: one pin constant beside TOOLS; `cmd_install` passes `ruff==<pin>` for ruff only (read; probe a).
- `scripts/tools`, 118 lines, room 182: contract text lines 24-25 says ruff is installed at the pinned version (read).
- `tests/scenarios/analysis_tools_probe_steps.py`, 270 lines, room 30: new Given "the plugin pins one version of ruff" and Then "ruff is installed into the interpreter at the version the plugin pins" (run: the undefined Given; grep). Room is about 30 lines; the pair fits. The file has six blank lines at 237-242.
- `ruff.toml`, 61 lines, TOML so no size limit: comment line 2 changes only if the pin is outside 0.17.x (grep).

On the change's path, not edited:

- `scripts/tools_check.py`, 35 lines, room 265: imports TOOLS; package field unchanged (read).
- `tests/scenarios/analysis_tools_project.py`, 182 lines, room 118: `pip_calls` returns the argument as given; no edit needed (read).
- `tests/scenarios/test_analysis_tools.py`, 74 lines, room 226: binds the whole feature file; no edit (read).
- `tests/scripts/test_tools.py`, 134 lines, room 166: probe and refusal tests; no edit expected (search).

## Open choices, both readings

- Exact pin. Reading A: `ruff==0.17.0`, the version installed here (probe, run). Reading B: another 0.17.x patch, which the implementer picks. Nothing in the repository or offline choice confirms a release exists; not checked against an index.
- A ruff already present at another version (probe b). Reading A: install leaves it alone and says `every tool is present`, as r58's wording allows. Reading B: install reports the mismatch. The requirement does not decide it.
- Where the Then reads the pin: from the constant, imported from `tools_env`, or a literal string in the step.
