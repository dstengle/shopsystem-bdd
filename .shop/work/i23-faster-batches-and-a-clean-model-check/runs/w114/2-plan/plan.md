# Plan of w114: tools install pins ruff (analysis-tools#r58)

From the research notes, `runs/w114/1-research/notes.md`.

## 1. What goes green

- **analysis-tools#r58**: `features/analysis-tools.feature`, "install puts in the version of ruff the plugin pins" (line 73).
  - It is red because there is no step definition for the Given "the plugin pins one version of ruff" (line 76). The run stops there with `StepDefinitionNotFoundError`. The Then "ruff is installed into the interpreter at the version the plugin pins" (line 78) has no definition either. The existing install Then, `{tools} are installed into the interpreter with pip`, does not match it.
  - Once the steps exist, the When still hands pip the bare `ruff`: `scripts/tools_env.py:cmd_install` line 93 passes the TOOLS row's package field, and no pin exists anywhere in the repository (notes §1, probe a). So the Then would fail.
- Retired scenarios: none. The work-item has no Retires section.

## 2. Where the change lands

- `scripts/tools_env.py`: add one constant beside TOOLS holding the plugin's ruff pin. `cmd_install` hands pip the pinned requirement (`ruff` with `==` and the pin) for ruff only. The TOOLS row's package field stays the bare name, because `probe` and `check` use it as the metadata lookup key (notes §3).
- `scripts/tools`: the contract text at lines 24–25 says that install puts in ruff at the version the plugin pins.
- `tests/scenarios/analysis_tools_probe_steps.py`: add the new Given and the new Then. The file is 270 lines, so 30 lines of room. Six blank lines at 237–242 can go if the pair needs them. The file must stay at 300 lines or fewer.

Not in the set:
- `ruff.toml`: its comment at line 2 ("the rules ruff 0.17 applies") stays true under decision D1, so it needs no edit.
- `tests/scenarios/analysis_tools_project.py`, `tests/scenarios/test_analysis_tools.py`, `tests/scripts/test_tools.py` and `scripts/tools_check.py` are on the change's path but need no edit (notes §7).

## 3. Decisions

- **D1. The pin is ruff 0.17.0.**
  - Why: r58 says the plugin pins "the one version". The repository's own rules, `ruff.toml:2`, are written for ruff 0.17, and 0.17.0 is the version the plugin's interpreter has today (notes, `probe --log`).
  - Rests on: analysis-tools#r58.
- **D2. The Given and the Then read the pin from the constant in `scripts/tools_env.py`, never from a literal of their own.**
  - The Then asserts that the interpreter's pip calls hold exactly one call for ruff, with the pinned requirement as its argument. It reads them through the existing `pip_calls` helper.
  - Why: a later change of the pin then needs one edit and no test edit.
  - The Given states the plugin's pin and sets nothing up. The project from the first Given is already missing ruff.
  - Rests on: analysis-tools#r58 ("the version the plugin pins").
- **D3. A ruff already present at another version is left alone, and install still says every tool is present.**
  - This is what happens today (notes §5, probe b).
  - Why: r58 applies only "when `tools install` installs ruff", and r5 installs only missing tools.
  - Rests on: analysis-tools#r5 and #r58. Nothing is added for this case.
- **D4. Only ruff is pinned. jedi, vulture and the other tools keep the bare package name.**
  - Why: r58 names ruff alone. This keeps the r5 and r7 scenarios' assertions on jedi and vulture as they are.
  - Rests on: analysis-tools#r58 and #r5.
- **D5. The refusal for an interpreter that is not a virtualenv, and the failure report, stay as they are.**
  - The refusal comes before the pinned call. The failure report prints the command it ran, so it will show the pinned requirement for ruff (notes §5).
  - Rests on: analysis-tools#r6 and #r7.
- **D6. The `Tried:` label on the not-a-virtualenv refusal (notes §6) is not fixed here.**
  - Why: it is outside r58, and the work-item accepts only r58. It is left as a defect for a later work-item.

## 4. Tests the decisions break

None.

- By the notes' search and reads, no existing test asserts ruff's pip argument.
- `installed_with_pip` (r5) checks jedi and vulture, which D4 leaves unchanged.
- `failed_command` (r7) checks the command for jedi.
- `install_refused`, `still_missing` (r6) and `nothing_installed` check that pip was never called, and D5 leaves that path unchanged.
- `tests/scripts/test_tools.py:79-86` never reaches the pip call.
- The probe and check tests (`test_tools.py:73`, `:128`) use the TOOLS package field as the lookup key, and D1/D4 keep that field unchanged.

## 5. Open cases

- Whether `0.17.0` is still published is not checked against a package index. The scenario fakes pip, so it cannot tell. The implementer names it if they learn otherwise.
- The spec's Implementation line (`spec/capabilities/analysis-tools.md:56`, "install runs `<interpreter> -m pip install <package>`") does not mention the pin. It is outside this work-item's file set. The implementer names it for a spec edit rather than editing it here.
- Design-decision 0035 names the plugin's own dependencies in its documentation. Whether the ruff pin, a dependency of the project rather than of the plugin, should also be named there is not settled by the scenario. The implementer names it if they think it applies.
