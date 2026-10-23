# Review of w114: tools install pins ruff (analysis-tools#r58)

**Verdict: DONE.** Nothing is Critical and nothing is to fix now. There is one Minor observation.

## Commits reviewed

The branch `work/w114` is gone. The commits are those between `91fb2a1 work: w114 ready -> claimed` and `2248e89 work: w114 claimed -> done` on HEAD, less `work:` commits:

- `8f76e50 tools install pins ruff (analysis-tools#r58)`: `scripts/tools`, `scripts/tools_env.py`, `tests/scenarios/analysis_tools_probe_steps.py` (+22/-5).

This matches the implementer's `result.json` `commits` list exactly. All three files are in the work-item's `fileset`.

## Changes under features/

None. `git diff 91fb2a1 2248e89 --stat -- features/` is empty.

## Removed and weakened tests

None. I read the whole diff of `tests/` and looked for deleted functions, changed asserts, parametrize cases, skips and xfails. It adds one helper (`ruff_pin`), one Given and one Then. The only removal is three blank lines at about line 237 of `analysis_tools_probe_steps.py`. No existing step or assert was touched. The plan's "Tests the decisions break" is "None", which agrees.

## Allowances

The report lists none ("none … no test touched"). That holds: no test's asserts changed.

## Cannot verify

- Whether `ruff==0.17.0` is published on the package index. The scenario fakes pip, and the plan and report both leave this open.
- The report's suite figures (694 passed, `--work-item w114` 137 passed). I did not run the whole suite. I ran the focused r58 scenario myself and it passes.
- The report says `import tools_env` in the tests resolves to another copy. That is why the step reads the pin from the file's text. I did not chase this; it is outside the diff.

## Findings

### 1. Minor (observation): the capability's Implementation text does not mention the pin

- Where: `spec/capabilities/analysis-tools.md:56`. It still says install runs `<interpreter> -m pip install <package>` for each missing tool. For ruff the package is now `ruff==<pin>`.
- Why it matters: the spec's mechanism text is now incomplete next to `scripts/tools`' contract, which was updated. r58, the Behaviour line itself, is correct.
- Fix: a spec edit through the usual proposal path, adding "(ruff at the version the plugin pins)". It is outside this work-item's fileset, and the plan and report already name it.
- Work-item: w114.
- Reproduction: `grep -n "pip install" spec/capabilities/analysis-tools.md` shows line 56 without the pin.

### Risks checked and found sound

- **The TOOLS package field stays the metadata lookup key.** The pin is applied in `cmd_install` only (`requirement = ... if name == "ruff" else package`), and the TOOLS row is unchanged. So probe and check still look up `ruff` and are unaffected.
- **The step asserts behaviour, not just the constant.** The Then compares the faked interpreter's actual pip calls with `ruff==<RUFF_PIN>`. A `cmd_install` that dropped the pin would fail it. The Given checks that the constant exists and is a version. Reading the pin by regex couples the step to the line's form `RUFF_PIN = "…"`. That is acceptable under plan D2.
- **Code no line asks for:** none. The pin is r58, and the contract text describes it.
- **Decision 0035** covers the plugin's own dependencies, not the project's tools. The ruff pin does not contradict it.

## Checks

- `tools check --base 91fb2a1`:
  - ruff: All checks passed!
  - vulture: clean
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: prints nothing. The touched files are within the limit.

## Commands run

- `git log --oneline -15`
- `git log --format=%H -1 --grep="^work: w114 ready -> claimed$"` and the same for `claimed -> done`
- `git log --stat 91fb2a1..2248e89`
- `git diff 91fb2a1 8f76e50`
- `git diff 91fb2a1 2248e89 --stat -- features/ tests/`
- `head -20 tests/scenarios/analysis_tools_probe_steps.py`
- `grep -n "r58|r5|rests_on|pin" spec/capabilities/analysis-tools.md`
- `sed -n 65,85p features/analysis-tools.feature`
- `cat` of decisions 0035 and 0058
- `python3 <Scripts>/tools check --base 91fb2a1de510dfcc37d4c4121ae1cab5f0021395`
- `python3 <Scripts>/tools size --limit 300`
- `python3 -m pytest -q tests/scenarios/test_analysis_tools.py -k "ruff or install"`: 1 passed (the r58 scenario).
