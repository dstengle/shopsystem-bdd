# Research of w106: tools install pins ruff (analysis-tools r58)

Tools: `Scripts:` plugin 0.24.0 (`tools probe` not run: no map, `tools tests-of` refused "no map"). Searches by text where noted. Probe file: `.shop/scratch/w106-1-research/probe_ruff_pin.py`. Scratch directory is not listed by `git status --porcelain` (clean).

## 1. Why the scenario is red today

- Command: `python3 -m pytest -q "tests/scenarios/test_analysis_tools.py::test_install_puts_in_the_version_of_ruff_the_plugin_pins"` (run). Only accepted scenario collected: 1 of 65.
- Failure: `StepDefinitionNotFoundError: Given "the plugin pins one version of ruff"`, feature line 76. Red at the first undefined step; the When and Then are not reached.
- Missing step definitions (read, grep for "pins one", "at the version the plugin pins"): none in `tests/scenarios/`. Both the Given and the Then are needed.
- Missing code: `scripts/tools_env.py:cmd_install` line 93 runs `[python, "-m", "pip", "install", package]`; `package` is `"ruff"` from the `TOOLS` row at line 17. No version is passed (read, run through probe below).
- No pin exists in the repository (grep of the whole worktree except `.shop/`, `.claude-plugin/` and `hooks/`: none; `.claude-plugin` and `hooks` grepped for "ruff": none). Only version hint: `ruff.toml:2` comment "the rules ruff 0.17 applies" (read). It is a comment, not a pin.

## 2. What the system answers today

Probe: `python3 -m pytest -q -s -p no:xdist -o addopts="" .shop/scratch/w106-1-research/probe_ruff_pin.py` (run). Project in scratch, a fake virtualenv (from `analysis_tools_project.fake`) missing only ruff, `tools --python <fake> install`.

- Plugin's tools (0.24.0 `scripts/tools`): `rc: 0`, stdout `ruff installed`, pip calls `[['python','pip','install','ruff']]`.
- Worktree's `scripts/tools`: identical result.
- Caveat: the fake pip records arguments and installs nothing, so no real version is seen. Plugin and worktree `scripts/` could not be diffed: the sandbox refused a diff against the plugin cache (read).
- Nearest cases, read only: a pin that pip cannot satisfy would fail at the same `pip install` and print `Tried: <python> -m pip install ruff==X` with the end of its error (`cmd_install` lines 95-96, 102-103; r7 path). A non-virtualenv interpreter is refused before any pip call (line 88-90; r6), so the pin adds nothing there.
- Ruff already present: `every tool is present`, no pip call (line 83-86, read).

## 3. Old assumptions

Bare package name (`pip install ruff`, newest release) is the assumption the requirement replaces.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/tools_env.py:cmd_install (line 93) | runs `pip install <package>` with the bare name, so pip takes the newest release | the ruff call must name the pinned version; jedi and vulture calls are unchanged | test_analysis_tools.py install scenarios (r5, r6, r7) by search; the r58 scenario itself is red | refs gave 0 references (name is called from `scripts/tools` dispatch via `set_defaults`; read) and by search |
| scripts/tools_env.py: TOOLS row `("ruff", "ruff", ...)` (line 17) | the pip package for ruff is the bare name; also used by probe and check's `metadata.version` lookup | the pin needs a version source here or in a constant beside it | by search: tests/scripts/test_tools.py:test_probe_gives_a_line_a_tool_and_the_interpreter (run: part of `-k "install or probe"`, passed) | by search |
| scripts/tools (contract text, lines 24-27) | says `install runs '<interpreter> -m pip install <package>'` | the contract must say ruff installs at the pinned version | none (documentation text) | read |
| tests/scenarios/analysis_tools_probe_steps.py:installed_with_pip (line 185) | asserts `pip_calls == tools.split(" and ")`, exact bare names | unchanged for jedi and vulture; a `ruff==X` call would fail it if ruff were ever listed there | by search: the r5 scenario (feature lines 64-70) | by search; features grep: only the r5 scenario names jedi and vulture in an install |
| tests/scenarios/analysis_tools_project.py:pip_calls (line 153-154) | returns `call[3]`, the package argument as given | returns `ruff==X` for the new step; the Then must compare the version, not the bare name | none directly; used by installed_with_pip, nothing_installed, install_refused (run: not run separately) | by search |
| ruff.toml:2 (comment) | says the rules are those "ruff 0.17 applies" | stale if the pinned version differs from 0.17 | none (ruff run by `tools check` is faked in tests) | by search |

## 4. Tests the requirement makes impossible to keep

- `tools tests-of scripts/tools_env.py:cmd_install --by-file` refused: "no map: make one with tools map" (run). No map, so the list is by search only.
- Search of tests for the pip argument: only `installed_with_pip` and `pip_calls` (analysis_tools_probe_steps.py:185, analysis_tools_project.py:154) compare the argument; both are used for jedi and vulture only (feature lines 64-70 and the install refusals at 81-86 and 89-96, which name jedi). None lists ruff.
- Verified sound: the r5, r6, r7 scenarios and test_tools.py install refusal (lines 79-86) assert refusals and output, not ruff's argument; they keep passing (test_tools `-k "install or probe"`: 1 passed, 1 skipped (venv interpreter); the r5 scenario is not in the collected selection, so it was not run).
- Not impossible: the r58 Then compares what a fake records; it has to be written with a version source (see part 7).

## 5. A step the work-item skips

- The pinned call goes through the same loop as today (`cmd_install` lines 91-98): the non-virtualenv refusal (line 88-90), pip's failure report (line 95-96, 102-103) and the final exit (line 104) apply to it unchanged. Read.
- Nothing else is skipped: no check, no transaction, no signature. None found, read.

## 6. Defects

None. The one probe run (ruff install) shows what the requirement changes, not a wrong behaviour.

## 7. The file set

Production:
- `scripts/tools_env.py` (104 lines, room 196): the ruff install passes the pinned version (in TOOLS row or in `cmd_install`); the source of the pin is open (see questions).
- `scripts/tools` (118 lines, room 182): contract text lines 24-27 says the install takes the pinned version for ruff.

Tests:
- `tests/scenarios/analysis_tools_probe_steps.py` (268 lines, room 32): new Given "the plugin pins one version of ruff" and new Then "ruff is installed into the interpreter at the version the plugin pins"; the room is small: about 30 lines.
- `tests/scenarios/analysis_tools_project.py` (182 lines, room 118): `pip_calls` already returns the package argument; may need no change, or a helper for the version.
- `tests/scenarios/test_analysis_tools.py` (74 lines, room 226): binding by `scenarios("analysis-tools.feature")` only; no edit expected.

Modules on the change path, edited or not:
- `scripts/tools_env.py` 104 lines, room 196 (edited)
- `scripts/tools` 118 lines, room 182 (edited)
- `tests/scenarios/analysis_tools_probe_steps.py` 268 lines, room 32 (edited)
- `tests/scenarios/analysis_tools_project.py` 182 lines, room 118 (maybe edited)
- `tests/scenarios/test_analysis_tools.py` 74 lines, room 226 (not edited)
- `tests/scripts/test_tools.py` 134 lines, room 166 (optional: a unit test for the pinned command)
- `ruff.toml` 61 lines (no size limit: TOML, not Python; comment only if the pin is not 0.17)

## Questions

None blocking. Two readings for the plan, not decided here:
- The pin lives in `scripts/tools_env.py` (a constant beside TOOLS) or in a file the plugin ships. Nothing in the repository names a pin today.
- The version is not stated anywhere; `ruff.toml` names 0.17 in a comment only.
