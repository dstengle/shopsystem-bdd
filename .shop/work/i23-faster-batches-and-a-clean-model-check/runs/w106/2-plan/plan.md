# Plan of w106: tools install pins ruff (analysis-tools#r58)

## 1. What goes green

- **analysis-tools#r58**: scenario "install puts in the version of ruff the plugin pins" (features/analysis-tools.feature, line 72).
  Red today at its Given "the plugin pins one version of ruff": there is no step definition for it (StepDefinitionNotFoundError). The Then "ruff is installed into the interpreter at the version the plugin pins" has no step definition either. Behind them, `cmd_install` in scripts/tools_env.py runs pip with the bare package name `ruff`, so pip takes the newest release, and the repository has no pin anywhere (notes, parts 1 and 2).
- The work-item retires no deprecated scenarios.

## 2. Where the change lands

- `scripts/tools_env.py`: add one constant naming the exact ruff version the plugin pins, next to the TOOLS table. `cmd_install` passes ruff to pip as the pinned requirement (`ruff==<pin>`). Jedi, vulture and the other tools are still installed by bare name. The TOOLS row for ruff is left as it is.
- `scripts/tools`: the contract text (lines 24-27) says that install puts ruff in at the version the plugin pins.
- `tests/scenarios/analysis_tools_probe_steps.py`: the new Given and the new Then (the file has 268 lines, so about 32 lines of room).
- `ruff.toml`: its comment on line 2 names the ruff version the rules are written for. It must name the same version as the pin (decision 2).

Removed from the researcher's set: `tests/scenarios/analysis_tools_project.py`. Its `pip_calls` already returns each package argument as given, so the Then can read `ruff==<pin>` from it unchanged. `tests/scenarios/test_analysis_tools.py` binds the scenario through the whole feature file, so it needs no edit. `tests/scripts/test_tools.py` gets no unit test: the scenario already drives the pinned call.

## 3. Decisions

1. **The pin is one exact version, kept as a constant in scripts/tools_env.py and shipped with the plugin.** It is not a range, and it is not a separate file. r58 says "the one version of ruff the plugin pins": one version, which only an exact pin gives. The scripts ship with the plugin, so a constant in them is something the plugin pins. Where the constant sits is something the narrator never sees. Rests on analysis-tools#r58.
2. **The pinned version is a release of the ruff 0.17 series. The implementer writes its exact patch number in the constant, and ruff.toml's comment names the same version.** The repository's ruff.toml says its rules are "the rules ruff 0.17 applies", so pinning that series keeps `tools check` matching the configuration the repository already has. Rests on analysis-tools#r58 together with analysis-tools#r16 (check runs ruff with the project's rules).
3. **The TOOLS row keeps the bare package name `ruff`. The pin is added only to the argument `cmd_install` gives pip.** Probe and check look up the installed version by that package name (notes, part 3). A pinned requirement string in that row would break the lookup. Rests on analysis-tools#r3.
4. **The pin applies only when install installs ruff.** If ruff is already present at another version, install does not reinstall it and still says every tool is present. r58 is worded "when `tools install` installs ruff", and r5 installs only missing tools. Rests on analysis-tools#r5 and #r58.
5. **The Given reads the pin the plugin ships from the production constant and records it in the scenario context. It does not set a pin of its own.** That way the scenario checks the pin the plugin actually ships. The implementer loads the constant the same way the existing step modules reach the scripts. The Then finds the fake pip's call for ruff in `pip_calls`. It asserts that this call names ruff at exactly the recorded version, that the version is one exact version, and that ruff appears in no other pip call. Rests on analysis-tools#r58.
6. **The pinned call goes through the same install loop as today.** The refusal when the interpreter is not a virtualenv (r6) and pip's failure report (r7) apply to the pinned call unchanged. The failure report names the command it ran, so it now shows `ruff==<pin>`. Rests on analysis-tools#r6 and #r7.

## 4. Tests the decisions break

None. What was checked (notes, parts 3 and 4, and the decisions above):
- `installed_with_pip` (analysis_tools_probe_steps.py) and `pip_calls` (analysis_tools_project.py) compare exact package arguments. They are used only in the scenarios that install jedi and vulture, and no scenario lists ruff among the tools installed by name, so the pinned argument breaks neither.
- `test_probe_gives_a_line_a_tool_and_the_interpreter` (tests/scripts/test_tools.py) reads the TOOLS row, which decision 3 leaves unchanged.
- The r6 and r7 scenarios, and the install refusal in test_tools.py, assert refusals and output, not ruff's argument.

There was no coverage map (`tools tests-of` refused), so this list comes from searches only.

## 5. Open cases

- The exact 0.17 patch release to pin. The implementer names it, in both the constant and ruff.toml's comment.
- Whether `tools probe` should report a ruff whose version is not the pin. The scenarios say nothing about it, and nothing here changes probe.
- How the r7 failure output reads when pip cannot satisfy the pin, for example offline or with the version not on the index. It follows the existing path (decision 6), and no scenario pins its wording.
